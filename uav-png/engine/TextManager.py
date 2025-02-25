import pygame
from .Singleton import Singleton
from .Window import Window


@Singleton
class TextManager:
    def __init__(self):
        pygame.font.init()
        self.font_cache = {}

    def get_font(self, font_path, font_size):
        """Retrieve a cached font or create a new one."""
        font_key = (font_path, font_size)
        if font_key not in self.font_cache:
            self.font_cache[font_key] = pygame.font.Font(font_path, font_size)
        return self.font_cache[font_key]

    def print(
        self,
        window: Window,
        text: str,
        position,
        font_path=None,
        font_size=24,
        color=(255, 255, 255),
        max_width=None,
    ):
        """
        Draw text on the screen, with optional line wrapping.
        Args:
            text (str): The text to display.
            position (tuple): (x, y) position to draw the text.
            font_path (str): Path to a custom font file (optional).
            font_size (int): Font size for the text.
            color (tuple): Text color as an (R, G, B) tuple.
            max_width (int): Maximum width for text wrapping (optional).
        """
        try:
            # Scale font size based on zoom factor
            font_size = int(font_size * window.zoom_factor)
            font = self.get_font(font_path, font_size)

            # Split text into lines if max_width is provided
            lines = []
            if max_width:
                words = text.split(" ")
                current_line = []
                for word in words:
                    current_line.append(word)
                    rendered_line = font.render(" ".join(current_line), True, color)
                    if rendered_line.get_width() > max_width:
                        current_line.pop()
                        lines.append(" ".join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(" ".join(current_line))
            else:
                lines = [text]

            # Pre-render all lines
            rendered_lines = [font.render(line, True, color) for line in lines]

            # Draw each line with adjusted position based on zoom
            y_offset = 0
            total_text_height = sum(line.get_height() for line in rendered_lines)
            for rendered_line in rendered_lines:
                text_width, text_height = rendered_line.get_size()
                x = position[0] - text_width // 2
                y = position[1] + y_offset - (total_text_height) // 2
                window.screen.blit(rendered_line, (x, y))
                y_offset += text_height
        except Exception as e:
            print(f"Error drawing font: {e}")
