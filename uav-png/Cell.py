from pygame import Rect
from .Game import Game
from .engine.TextManager import TextManager
from enum import Enum


class CellState(Enum):
    NOT_SCANNED = 0
    SCANNED = 1
    UNREACHABLE = 2
    UNKNOWN = 3
    NO_INTEREST = 4


class Cell:
    def __init__(
        self,
        rect: Rect,
        value: int,
        state: CellState = CellState.UNKNOWN,
    ):
        self.rect = rect
        self.value = value
        self.state = state
        self.state_colors = {
            CellState.NOT_SCANNED: "pink",
            CellState.SCANNED: "green",
            CellState.UNREACHABLE: "red",
            CellState.UNKNOWN: "blue",
            CellState.NO_INTEREST: "gray",
        }

    def update_value(self, new_value: int):
        self.value = new_value

    def update_state(self, new_state: CellState):
        self.state = new_state

    def update(self):
        pass

    def handle_events(self):
        pass

    def draw(self):
        Game().getWindow().draw_rect(
            color=self.state_colors.get(self.state),
            rect=self.rect,
            border=1,
            border_color="white",
        )
        TextManager().print(
            Game().getWindow(),
            str(self.value),
            (
                self.rect.left + self.rect.width // 2,
                self.rect.top + self.rect.height // 2,
            ),
        )
