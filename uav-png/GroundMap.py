from .Cell import Cell, CellState
from pygame import Rect
from sklearn.cluster import DBSCAN, KMeans
from .Cluster import Cluster
import numpy as np
import threading


class GroundMap:
    def __init__(
        self,
        AoI,
        width: float,
        height: float,
        wind_direction: [float, float],
        wind_strength: float,
    ):
        self.cells = {}
        self.wind_direction = wind_direction
        self.wind_strength = wind_strength
        self.width = width
        self.height = height
        self.AoI = AoI
        self.updating_cluster = False
        from .Game import Game

        self.cell_size = min(
            Game().getWindow().width // self.width,
            Game().getWindow().height // self.height,
        )

        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                cell_value = 0
                cell_state = CellState.NO_INTEREST
                if (x, y) in AoI:
                    cell_value = 1
                    cell_state = CellState.NOT_SCANNED

                cell = Cell(rect, cell_value, cell_state)
                self.cells[(x, y)] = cell

        self.clusters = []

    def update_cluster(self, method="dbscan", n_clusters=3):
        if not self.updating_cluster:
            self.updating_cluster = True
            thread = threading.Thread(
                target=self._run_clustering, args=(method, n_clusters), daemon=True
            )
            thread.start()

    def _run_clustering(self, method, n_clusters):
        """Performs clustering in a separate thread."""
        remainAoI = [cell for cell in self.AoI if self.cells[cell].value > 0]
        if not remainAoI:
            self.updating_cluster = False
            return

        if method == "dbscan":
            clusters = self.apply_dbscan(remainAoI)
        elif method == "kmeans":
            clusters = self.apply_kmeans(remainAoI, n_clusters)
        else:
            self.updating_cluster = False
            return

        # Updating clusters safely after computation
        self.clusters = clusters
        self.updating_cluster = False

    def apply_dbscan(self, AoI, eps=1.0, min_samples=1) -> list[Cluster]:
        coordinates = np.array([list(cell) for cell in AoI])
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        dbscan.fit(coordinates)
        clusters = []
        for label in set(dbscan.labels_):
            if label == -1:
                continue
            cluster_points = coordinates[dbscan.labels_ == label]
            centroid = np.mean(cluster_points, axis=0) * self.cell_size
            distances = np.linalg.norm(cluster_points - centroid, axis=1)
            radius = np.max(distances) * self.cell_size

            clusters.append(
                Cluster(
                    centroid=centroid,
                    radius=radius,
                    important_score=len(cluster_points),
                )
            )
        return clusters

    def apply_kmeans(self, AoI, n_clusters=3) -> list[Cluster]:
        coordinates = np.array([list(cell) for cell in AoI])
        if len(coordinates) < n_clusters:
            n_clusters = len(coordinates)
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        labels = kmeans.fit_predict(coordinates)
        clusters = {}
        for label in set(labels):
            cluster_points = coordinates[labels == label]
            centroid = np.mean(cluster_points, axis=0) * self.cell_size
            distances = np.linalg.norm(cluster_points - centroid, axis=1)
            radius = np.max(distances) * self.cell_size

            clusters.append(
                Cluster(
                    centroid=centroid,
                    radius=radius,
                    important_score=len(cluster_points),
                )
            )
        return clusters

    def update(self):
        """Update all cells."""
        for cell in self.cells.values():
            cell.update()

        for cluster in self.clusters:
            cluster.update()

    def handle_events(self):
        """Handle events for all cells."""
        for cell in self.cells.values():
            cell.handle_events()

        for cluster in self.clusters:
            cluster.handle_events()

    def draw(self):
        for cell in self.cells.values():
            cell.draw()

        for cluster in self.clusters:
            cluster.draw()

    def update_state(
        self,
        new_points=None,
        new_wind_direction=None,
        new_wind_strength=None,
    ):
        """Update the map state with new parameters."""
        if new_points is not None:
            self.AoI = new_points
            self._rebuild_cells()

        if new_wind_direction is not None:
            self.wind_direction = new_wind_direction

        if new_wind_strength is not None:
            self.wind_strength = new_wind_strength

    def _rebuild_cells(self):
        """Rebuild cells based on updated AoI or screen size."""
        self.cells.clear()  # Clear existing cells

        # Recalculate cell size based on the window size
        self.cell_size_x = self.window_width // self.width
        # New cell size based on map width
        self.cell_size_y = self.window_height // self.height
        # New cell size based on map height

        # Choose the smaller of the two to ensure cells fit in both directions
        self.cell_size = min(self.cell_size_x, self.cell_size_y)

        # Recreate the grid with updated cell size
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                # Determine cell value and state based on AoI
                cell_value = 0
                cell_state = CellState.NO_INTEREST
                if (x, y) in self.AoI:
                    cell_value = 1
                    cell_state = CellState.NOT_SCANNED

                # Create and store the cell
                cell = Cell(rect, cell_value, cell_state)
                self.cells[(x, y)] = cell

    def clean(self):
        self.cells.clear()
        self.clusters.clear()
