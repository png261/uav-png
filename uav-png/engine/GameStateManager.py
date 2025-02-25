from collections import deque
from .Singleton import Singleton


@Singleton
class GameStateManager:
    def __init__(self):
        self.states = deque()  # Use deque for faster stack operations

    def push_state(self, state):
        """Push a new state onto the stack."""
        self.states.append(state)

    def pop_state(self):
        """Remove the current state from the stack."""
        if self.states:
            self.states.pop()

    def switch_state(self, state):
        """Replace the current state with a new one."""
        if self.states:
            self.states.pop()
        self.states.append(state)

    def handle_events(self):
        """Forward events to the current state."""
        if self.states:
            current_state = self.states[-1]  # Store the reference
            current_state.handle_events()

    def update(self):
        """Update the current state."""
        if self.states:
            current_state = self.states[-1]  # Store the reference
            current_state.update()

    def render(self):
        """Render the current state."""
        if self.states:
            current_state = self.states[-1]  # Store the reference
            current_state.render()

    def clean(self):
        """Clean up the current state."""
        if self.states:
            current_state = self.states[-1]  # Store the reference
            current_state.clean()
