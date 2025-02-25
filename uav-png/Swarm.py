from .Uav import Uav
from .Cell import CellState
from .GroundMap import GroundMap
import numpy as np


class Swarm:
    def __init__(self, uavs: list[Uav], centroid: [float, float]):
        self.uavs = uavs
        self.centroid = np.array(centroid)
        self.force_vector = np.array([0.0, 0.0])
        self.radius = None
        self.calculate_radius()
        self.target_cluster = None
        self.cells_in_swarm = []

    def is_moving(self):
        return (
            self.target_cluster
            and np.linalg.norm(self.target_cluster.centroid - self.centroid) > 1
        )

    def update(self):
        self.centroid += self.force_vector

        for uav in self.uavs:
            if self.is_moving():
                uav.move(self.centroid, self.uavs)
            else:
                if uav.cell_target is None and self.cells_in_swarm:
                    closest_cell = min(
                        self.cells_in_swarm,
                        key=lambda cell: np.linalg.norm(cell.rect.center - uav.pos),
                    )
                    uav.set_cell_target(closest_cell)

            uav.move(self.centroid, self.uavs)
            uav.update()

    def handle_events(self, ground_map: GroundMap):
        if not self.target_cluster:
            ground_map.update_cluster()
            self.chose_target(ground_map)
            return

        self.calculate_force(ground_map)

        is_scan_done = not self.is_moving() and len(self.cells_in_swarm) == 0
        if is_scan_done:
            self.scan_done(ground_map)
            self.is_moving

        self.cells_in_swarm = [
            cell
            for cell in ground_map.cells.values()
            if np.linalg.norm(np.array(cell.rect.center) - self.centroid) <= self.radius
            and cell.state not in {CellState.SCANNED, CellState.NO_INTEREST}
        ]

        for uav in self.uavs:
            uav.handle_events(ground_map)

    def scan_done(self, ground_map: GroundMap):
        self.calculate_force(ground_map)
        ground_map.update_cluster()
        self.chose_target(ground_map)

    def chose_target(self, ground_map: GroundMap):
        if not ground_map.clusters:
            return

        """Choose the nearest and highest priority cluster."""
        self.target_cluster = max(
            ground_map.clusters,
            key=lambda cluster: cluster.important_score
            / (max(np.linalg.norm(cluster.centroid - self.centroid), 0.1) ** 2),
            default=None,
        )

    def draw(self):
        from .Game import Game

        Game().getWindow().draw_circle(self.centroid, 5, "blue")
        Game().getWindow().draw_circle(self.centroid, self.radius, "blue", 2)

        for uav in self.uavs:
            uav.draw()

    def calculate_force(self, ground_map: GroundMap):
        distance_to_target = np.linalg.norm(
            self.target_cluster.centroid - self.centroid
        )
        force = (self.target_cluster.centroid - self.centroid) / distance_to_target
        force_vector = [0.1, 0.1] + force

        norm = (force_vector[0] ** 2 + force_vector[1] ** 2) ** 0.5
        if norm != 0:
            force = force_vector / norm

        self.force_vector = force

    def calculate_radius(self):
        """Calculate the swarm radius as the average UAV connection radius."""
        self.radius = sum(uav.connection_radius for uav in self.uavs) / len(self.uavs)

    def merge(self, other_swarm):
        """Merge two swarms into one."""
        self.uavs.extend(other_swarm.uavs)
        self.calculate_new_centroid()
        self.calculate_radius()

    def calculate_new_centroid(self):
        """Calculate the new centroid of the merged swarm."""
        self.centroid = sum(uav.pos for uav in self.uavs) / len(self.uavs)

    def is_near(self, other_swarm):
        """Check if this swarm is near another swarm."""
        distance = np.linalg.norm(other_swarm.centroid - self.centroid)
        return distance < self.radius

    def clean(self):
        pass
