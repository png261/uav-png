from .Cell import Cell, CellState
from pygame import Rect
from sklearn.cluster import DBSCAN, KMeans
import numpy as np


class Map:
    def __init__(
        self,
        AoI,
        width: float,
        height: float,
        wind_direction: (float, float),
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

        # Calculate the dynamic cell size based on the window size and map size
        self.cell_size_x = (
            Game().getWindow().width // self.width
        )  # Cell size based on map width
        self.cell_size_y = (
            Game().getWindow().height // self.height
        )  # Cell size based on map height

        # Choose the smaller of the two to ensure cells fit in both directions
        self.cell_size = min(self.cell_size_x, self.cell_size_y)

        # Create grid of cells that fit the screen
        for x in range(0, self.width):
            for y in range(0, self.height):
                # Calculate the rectangle for each cell
                rect = Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                # Determine cell value and state based on AoI (Area of Interest)
                cell_value = 0
                cell_state = CellState.NO_INTEREST
                if (x, y) in AoI:
                    cell_value = 1
                    cell_state = CellState.NOT_SCANNED

                # Create and store the cell
                cell = Cell(rect, cell_value, cell_state)
                self.cells[(x, y)] = cell

        self.clusters = self.apply_dbscan(self.AoI)

    def update_cluster(self, method="dbscan", n_clusters=3):
        if not self.updating_cluster:
            newAoI = [cell for cell in self.AoI if self.cells[cell].value > 0]
            if not newAoI:
                return

            if method == "dbscan":
                self.clusters = self.apply_dbscan(newAoI)
            elif method == "kmeans":
                self.clusters = self.apply_kmeans(newAoI, n_clusters)
            self.updating_cluster = False

    def apply_dbscan(self, AoI, eps=1.0, min_samples=1):
        coordinates = np.array([list(cell) for cell in AoI])
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        dbscan.fit(coordinates)
        clusters = {}
        for label in set(dbscan.labels_):
            if label == -1:
                continue
            cluster_points = coordinates[dbscan.labels_ == label]
            centroid = np.mean(cluster_points, axis=0)
            distances = np.linalg.norm(cluster_points - centroid, axis=1)
            radius = np.max(distances)
            clusters[label] = {
                "centroid": centroid * self.cell_size,
                "points": cluster_points,
                "radius": radius * self.cell_size,
                "priority_score": len(cluster_points),
            }
        return clusters

    def apply_kmeans(self, AoI, n_clusters=3):
        coordinates = np.array([list(cell) for cell in AoI])
        if len(coordinates) < n_clusters:
            n_clusters = len(coordinates)  # Adjust to avoid errors
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        labels = kmeans.fit_predict(coordinates)
        clusters = {}
        for label in set(labels):
            cluster_points = coordinates[labels == label]
            centroid = np.mean(cluster_points, axis=0)
            distances = np.linalg.norm(cluster_points - centroid, axis=1)
            radius = np.max(distances)
            EXTEND_RADIUS = self.cell_size // 2
            clusters[label] = {
                "centroid": centroid * self.cell_size,
                "points": cluster_points,
                "radius": radius * self.cell_size + EXTEND_RADIUS,
                "priority_score": len(cluster_points),
            }
        return clusters

    def update(self):
        """Update all cells."""
        for cell in self.cells.values():
            cell.update()

    def handle_events(self):
        """Handle events for all cells."""
        for cell in self.cells.values():
            cell.handle_events()

    def draw(self):
        """Draw all cells and clusters."""
        for cell in self.cells.values():
            cell.draw()

        from .Game import Game
        from .engine.TextManager import TextManager

        # Draw clusters (centroids and radii)
        for cluster in self.clusters.values():
            centroid_x, centroid_y = cluster["centroid"]

            # Draw centroid as a small filled circle
            Game().getWindow().draw_circle(centroid_x, centroid_y, 20, "red")

            # Draw the cluster radius as a circle with a radius equal to the cluster's radius
            cluster_radius = cluster["radius"]
            Game().getWindow().draw_circle(
                centroid_x, centroid_y, cluster_radius, "red", 2
            )

            TextManager().print(
                window=Game().getWindow(),
                text=str(cluster["priority_score"]),
                position=(
                    centroid_x,
                    centroid_y,
                ),
                color="black",
                font_size=30,
            )

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
        self.cell_size_x = (
            self.window_width // self.width
        )  # New cell size based on map width
        self.cell_size_y = (
            self.window_height // self.height
        )  # New cell size based on map height

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
