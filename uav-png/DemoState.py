import pygame
from .engine.GameState import GameState
from .engine.GameStateManager import GameStateManager
from .engine.InputManager import InputManager
from .Uav import Uav
from .SwarmManager import SwarmManager
from .Map import Map


class DemoState(GameState):
    def __init__(self):
        self.swarm_manager = SwarmManager()
        # Create UAVs (example values)
        uav1 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=150,
            y=300,
            size=30,
            connection_range=100,
        )
        uav2 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=800,
            y=210,
            size=30,
            connection_range=50,
        )
        uav3 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=300,
            y=300,
            size=30,
            connection_range=70,
        )
        uav4 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=700,
            y=200,
            size=30,
            connection_range=100,
        )
        uav5 = Uav(
            remain_energy=100,
            min_speed=1,
            max_speed=10,
            buffer_data=50,
            x=500,
            y=900,
            size=30,
            connection_range=100,
        )

        # Add UAVs to the SwarmManager
        self.swarm_manager.add_uav(uav1)
        self.swarm_manager.add_uav(uav2)
        self.swarm_manager.add_uav(uav3)

        self.ground_map = Map(
            AoI=[
                (20, 8),
                (20, 9),
                (20, 10),
                (20, 11),
                (20, 12),
                (20, 13),
                (20, 14),
                (20, 15),
                (20, 16),

                (21, 8),
                (21, 9),
                (21, 10),
                (21, 11),
                (21, 12),
                (21, 13),
                (21, 14),
                (21, 15),
                (21, 16),

                (22, 8),
                (22, 9),
                (22, 10),
                (22, 11),
                (22, 12),
                (22, 13),
                (22, 14),
                (22, 15),
                (22, 16),

                (23, 8),
                (23, 9),
                (23, 10),
                (23, 11),
                (23, 12),
                (23, 13),
                (23, 14),
                (23, 15),
                (23, 16),

                (24, 8),
                (24, 9),
                (24, 10),
                (24, 11),
                (24, 12),
                (24, 13),
                (24, 14),
                (24, 15),
                (24, 16),

                (25, 8),
                (25, 9),
                (25, 10),
                (25, 11),
                (25, 12),
                (25, 13),
                (25, 14),
                (25, 15),
                (25, 16),

                (26, 8),
                (26, 9),
                (26, 10),
                (26, 11),
                (26, 12),
                (26, 13),
                (26, 14),
                (26, 15),
                (26, 16),
            ],
            width=30,
            height=20,
            wind_direction=(0.5, 0.5),
            wind_strength=10,
        )

    def update(self):
        self.ground_map.update()
        self.swarm_manager.update()

    def handle_events(self):
        self._handle_game_state()
        self.ground_map.handle_events()
        self.swarm_manager.handle_events(self.ground_map)

    def render(self):
        self.ground_map.draw()
        self.swarm_manager.draw()

    def clean(self):
        pass

    def _handle_game_state(self):
        if InputManager().is_key_down(pygame.K_ESCAPE):
            GameStateManager().pop_state()
