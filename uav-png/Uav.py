from .engine.TextureManager import TextureManager
from .Cell import CellState
from .Map import Map


class Uav:
    def __init__(
        self,
        remain_energy: float,
        min_speed: float,
        max_speed: float,
        buffer_data,
        x: float = 100,
        y: float = 100,
        size: float = 30,
        connection_range=10,
    ):
        self.x = x
        self.y = y
        self.size = size
        self.remain_energy = remain_energy
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.buffer_data = buffer_data
        self.force_vector = [0, 0]
        self.connection_radius = connection_range
        self.swarm = None  # Initially, each UAV is its own swarm
        self.cell_target = None

    def set_cell_target(self, cell):
        self.cell_target = cell

    def scan(self, ground_map: Map):
        for cell in ground_map.cells.values():
            if cell.state == CellState.NOT_SCANNED:
                if cell.rect.collidepoint((self.x, self.y)):
                    cell.state = CellState.SCANNED
                    cell.update_value(0)

    def update(self):
        pass

    def handle_events(self, ground_map: Map):
        if self.cell_target != None and self.cell_target.rect.collidepoint(
            (self.x, self.y)
        ):
            self.cell_target = None
        self.scan(ground_map)

    def draw(self):
        from .Game import Game

        TextureManager().draw_texture(
            Game().getWindow(),
            name="uav",
            position=(self.x - self.size // 2, self.y - self.size // 2),
            scale=(self.size, self.size),
        )

        Game().getWindow().draw_circle(self.x, self.y, 3, "green")

    def calculate_force(self, centroid_x, centroid_y, uavs):
        force_x = centroid_x - self.x
        force_y = centroid_y - self.y

        for uav in uavs:
            if uav != self:
                distance = ((uav.x - self.x) ** 2 + (uav.y - self.y) ** 2) ** 0.5
                if distance < 50:
                    force_x += self.x - uav.x
                    force_y += self.y - uav.y

        # normalize the force vector
        force_magnitude = (force_x**2 + force_y**2) ** 0.5
        if force_magnitude > 0:
            force_x /= force_magnitude
            force_y /= force_magnitude
        self.force_vector = [force_x, force_y]

    def move(self, centroid_x, centroid_y, uavs):
        if self.cell_target != None:
            self.calculate_force(
                self.cell_target.rect.centerx, self.cell_target.rect.centery, uavs
            )
        else:
            self.calculate_force(centroid_x, centroid_y, uavs)

        self.x += self.force_vector[0]
        self.y += self.force_vector[1]

    def transmit_data(self):
        if self.buffer_data > 0:
            print("Transmitting data...")
            self.buffer_data -= (
                1  # Assuming transmitting data consumes 1 unit of buffer data
            )
        else:
            print("No data to transmit.")
