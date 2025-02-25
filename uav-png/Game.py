import pygame
import os
from .config import IMAGE_DIR
from .engine.Singleton import Singleton
from .engine.GameStateManager import GameStateManager
from .engine.InputManager import InputManager
from .engine.Window import Window
from .MenuState import MenuState
from .engine.TextureManager import TextureManager


@Singleton
class Game:
    def __init__(self, width: int = 1200, height: int = 800, fps: int = 60):
        pygame.init()
        self.isRunning = True
        self.FPS = fps
        self.window = Window(width, height, self.FPS)
        self.loadTexture()
        GameStateManager().push_state(MenuState())

    def loadTexture(self):
        TextureManager().load_texture("uav", os.path.join(IMAGE_DIR, "uav.png"))

    def update(self):
        GameStateManager().update()

    def handle_event(self):
        self.window.handle_FPS()
        InputManager().update()

        if InputManager().is_quit():
            self.quit()

        GameStateManager().handle_events()

    def render(self):
        self.window.fill("white")
        GameStateManager().render()
        pygame.display.flip()

    def quit(self):
        self.isRunning = False

    def clean(self):
        GameStateManager().clean()
        pygame.quit()

    def getWindow(self):
        return self.window
