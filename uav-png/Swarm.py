from .Uav import Uav
from .Cell import CellState
import math
from .Map import Map


class Swarm:
    def __init__(self, uavs: list[Uav], x: float, y: float):
        self.uavs = uavs  # List of UAV objects
        self.centroid_x = x
        self.centroid_y = y
        self.force_vector = [0, 0]
        self.centroid_radius = None
        self.calculate_radius()
        self.target_centroid_x = None
        self.target_centroid_y = None
        self.cells_in_swarm = []

    def is_moving(self):
        return (
            abs(self.centroid_x - self.target_centroid_x) > 1
            and abs(self.centroid_y - self.target_centroid_y) > 1
        )

    def update(self):
        self.centroid_x += self.force_vector[0]
        self.centroid_y += self.force_vector[1]

        for uav in self.uavs:
            if self.is_moving():
                uav.move(self.centroid_x, self.centroid_y, self.uavs)
            else:
                if uav.cell_target == None:
                    if self.cells_in_swarm:
                        closest_cell = None
                        min_distance = float("inf")  # Start with a very large distance

                        for cell in self.cells_in_swarm:
                            # Calculate the distance from the UAV to the center of the cell
                            distance = math.sqrt(
                                (cell.rect.centerx - uav.x) ** 2
                                + (cell.rect.centery - uav.y) ** 2
                            )

                            # If this cell is closer, update the closest cell and distance
                            if distance < min_distance:
                                closest_cell = cell
                                min_distance = distance
                        uav.set_cell_target(closest_cell)

            uav.move(self.centroid_x, self.centroid_y, self.uavs)
            uav.update()

    def handle_events(self, ground_map: Map):
        first_time = self.target_centroid_x == None and self.target_centroid_y == None
        if first_time:
            self.chose_target(ground_map)

        self.calculate_force(ground_map)

        if not self.is_moving() and len(self.cells_in_swarm) == 0:
            self.scan_done(ground_map)

        for uav in self.uavs:
            uav.handle_events(ground_map)

        self.cells_in_swarm = []
        for cell in ground_map.cells.values():
            # Calculate distance from swarm centroid to the cell center
            distance = math.sqrt(
                (cell.rect.centerx - self.centroid_x) ** 2
                + (cell.rect.centery - self.centroid_y) ** 2
            )

            # If the cell is within the swarm's radius, check its state
            if distance <= self.centroid_radius:
                if (
                    cell.state != CellState.SCANNED
                    and cell.state != CellState.NO_INTEREST
                ):
                    self.cells_in_swarm.append(cell)

    def scan_done(self, ground_map: Map):
        if (
            self.target_centroid_x
            and self.target_centroid_y
            and abs(self.target_centroid_x - self.centroid_x) < 1
            and abs(self.target_centroid_y - self.centroid_y) < 1
        ):
            self.calculate_force(ground_map)
            ground_map.update_cluster()
            self.chose_target(ground_map)

    def chose_target(self, ground_map: Map):
        if not ground_map.clusters:
            return

        """Choose the nearest and highest priority cluster."""
        best_score = -float("inf")
        best_cluster = None

        for label, cluster in ground_map.clusters.items():
            # Get the centroid of the cluster
            cluster_x, cluster_y = cluster["centroid"]
            priority = cluster.get(
                "priority_score", 1
            )  # Default priority is 1 if not defined

            # Calculate the distance from the swarm's centroid to the cluster's centroid
            distance = math.sqrt(
                (cluster_x - self.centroid_x) ** 2 + (cluster_y - self.centroid_y) ** 2
            )

            # Avoid division by zero in case distance is zero
            if distance == 0:
                distance = 0.1  # Small non-zero value to prevent division by zero

            # Calculate weighted score (higher priority and closer distance are better)
            score = priority / (distance**2)

            # Choose the cluster with the highest score
            if score > best_score:
                best_score = score
                best_cluster = cluster
                self.target_cluster_label = label

        # Set the target centroid to the best cluster's centroid
        if best_cluster:
            self.target_centroid_x, self.target_centroid_y = best_cluster["centroid"]

    def draw(self):
        from .Game import Game

        Game().getWindow().draw_circle(self.centroid_x, self.centroid_y, 5, "blue")
        Game().getWindow().draw_circle(
            self.centroid_x, self.centroid_y, self.centroid_radius, "blue", 2
        )
        for cell in self.cells_in_swarm:
            Game().getWindow().draw_rect(
                color=cell.state_colors.get(cell.state),
                rect=cell.rect,
                border=1,
                border_color="black",
            )

        for uav in self.uavs:
            uav.draw()

    def calculate_force(self, ground_map: Map):
        force_vector = [0.1, 0.1]

        # Calculate the force vector to move the swarm centroid to the cluster centroid
        distance_to_target = (
            (self.target_centroid_x - self.centroid_x) ** 2
            + (self.target_centroid_y - self.centroid_y) ** 2
        ) ** 0.5

        # Calculate the direction towards the target centroid
        force_x = (self.target_centroid_x - self.centroid_x) / distance_to_target
        force_y = (self.target_centroid_y - self.centroid_y) / distance_to_target

        # Apply the force based on the cluster and other cells
        force_vector[0] += force_x
        force_vector[1] += force_y

        # Normalize the force vector to avoid overshooting
        norm = (force_vector[0] ** 2 + force_vector[1] ** 2) ** 0.5
        if norm != 0:
            force_x = force_vector[0] / norm
            force_y = force_vector[1] / norm

        # Store the calculated force vector
        self.force_vector = (force_x, force_y)

    def calculate_radius(self):
        """Calculate the swarm radius as the maximum distance from the centroid plus the UAV connection radius."""
        new_radius = 0
        for uav in self.uavs:
            new_radius += uav.connection_radius
        new_radius /= len(self.uavs)

        # Swarm radius is the maximum distance from centroid plus UAV connection radius
        self.centroid_radius = new_radius

    def merge(self, other_swarm):
        """Merge two swarms into one."""
        self.uavs.extend(other_swarm.uavs)
        self.calculate_new_centroid()
        self.calculate_radius()

    def calculate_new_centroid(self):
        """Calculate the new centroid of the merged swarm."""
        total_x = sum(uav.x for uav in self.uavs)
        total_y = sum(uav.y for uav in self.uavs)
        self.centroid_x = total_x / len(self.uavs)
        self.centroid_y = total_y / len(self.uavs)

    def is_near(self, other_swarm):
        """Check if this swarm is near another swarm."""
        distance = math.sqrt(
            (self.centroid_x - other_swarm.centroid_x) ** 2
            + (self.centroid_y - other_swarm.centroid_y) ** 2
        )
        return distance < self.centroid_radius
