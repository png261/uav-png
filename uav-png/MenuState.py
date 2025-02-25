from .engine.GameState import GameState
from .engine.GameStateManager import GameStateManager
from .engine.Button import Button


class MenuState(GameState):
    def __init__(self):
        self.buttons = []
        from .DemoState import DemoState

        button = Button(x=450, y=300, width=300, height=100)
        button.set_title("Start Demo")
        button.set_border(2)
        button.set_font_size(40)
        button.on_click(lambda: GameStateManager().push_state(DemoState()))
        self.buttons.append(button)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_events(self):
        pass

    def render(self):
        from .Game import Game

        Game().getWindow().fill("white")

        for button in self.buttons:
            button.draw(Game().getWindow())

    def clean(self):
        pass
