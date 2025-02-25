from .engine.TextureManager import TextureManager
from .Cell import CellState
from .GroundMap import GroundMap
import numpy as np


class Uav:
    def __init__(
        self,
        remain_energy: float,
        min_speed: float,
        max_speed: float,
        buffer_data,
        pos: [float, float],
        size: float = 30,
        connection_range=10,
    ):
        self.pos = pos
        self.size = size
        self.remain_energy = remain_energy
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.buffer_data = buffer_data
        self.force_vector = (0, 0)
        self.connection_radius = connection_range
        self.swarm = None
        self.cell_target = None

    def set_cell_target(self, cell):
        self.cell_target = cell

    def scan(self, ground_map: GroundMap):
        for cell in ground_map.cells.values():
            if cell.state == CellState.NOT_SCANNED:
                if cell.rect.collidepoint(self.pos):
                    cell.state = CellState.SCANNED
                    cell.update_value(0)

    def update(self):
        pass

    def handle_events(self, ground_map: GroundMap):
        if self.cell_target != None and self.cell_target.rect.collidepoint(self.pos):
            self.cell_target = None
        self.scan(ground_map)

    def draw(self):
        from .Game import Game

        TextureManager().draw_texture(
            Game().getWindow(),
            name="uav",
            position=[self.pos[0] - self.size // 2, self.pos[1] - self.size // 2],
            scale=(self.size, self.size),
        )

        Game().getWindow().draw_circle(self.pos, 3, "green")

    def calculate_force(self, target_pos: [float, float], uavs):
        force_vector = np.array(target_pos) - self.pos

        for uav in uavs:
            if uav != self and np.linalg.norm(uav.pos - self.pos) < 50:
                force_vector += self.pos - uav.pos

        force_magnitude = (force_vector[0] ** 2 + force_vector[1] ** 2) ** 0.5
        if force_magnitude > 0:
            force_vector /= force_magnitude
        self.force_vector = force_vector

    def move(self, target_pos: [float, float], uavs):
        if self.cell_target:
            self.calculate_force(self.cell_target.rect.center, uavs)
        else:
            self.calculate_force(target_pos, uavs)

        self.pos += self.force_vector

    def clean(self):
        pass
