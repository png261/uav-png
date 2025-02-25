import pygame
from pygame import Rect
import numpy as np


class Window:
    def __init__(self, width, height, FPS):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.background_image = None
        self.zoom_factor = 1.0  # Zoom factor (1.0 means no zoom)

    def set_background_image(self, img_path):
        self.background_image = pygame.image.load(img_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.width, self.height)
        )

    def draw_background_image(self):
        if self.background_image:
            scaled_background = pygame.transform.scale(
                self.background_image,
                (
                    int(self.width * self.zoom_factor),
                    int(self.height * self.zoom_factor),
                ),
            )
            self.screen.blit(scaled_background, (0, 0))

    def draw_image(self, texture, position, scale=None, rotation=0):
        """
        Draw an image at a specific position on the screen.

        Args:
            texture (pygame.Surface): The image texture.
            position (tuple): (x, y) position to draw the image.
            scale (tuple): (width, height) to resize the image (optional).
            rotation (float): Degrees to rotate the image (optional).
        """
        if scale is None:
            scale = (texture.get_width(), texture.get_height())
        scale = (int(scale[0] * self.zoom_factor), int(scale[1] * self.zoom_factor))

        texture = pygame.transform.scale(texture, scale)
        if rotation != 0:
            texture = pygame.transform.rotate(texture, rotation)
        self.screen.blit(texture, position)

    def draw_rect(self, color, rect: Rect, radius=0, border=0, border_color="black"):
        """
        Draw a box with rounded corners, adjusted for zoom.

        Args:
            color (tuple): The color of the box as an (R, G, B) tuple.
            rect (tuple): The rectangle dimensions (x, y, width, height).
            radius (int): The corner radius in pixels.
            border (int): Width of the border (0 for no border).
            border_color (tuple): Border color as an (R, G, B) tuple (optional).
        """
        rect = Rect(
            int(rect.x * self.zoom_factor),
            int(rect.y * self.zoom_factor),
            int(rect.width * self.zoom_factor),
            int(rect.height * self.zoom_factor),
        )

        # Draw the main box
        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=int(radius * self.zoom_factor),
        )

        # Draw the border if specified
        if border > 0 and border_color is not None:
            pygame.draw.rect(
                self.screen,
                border_color,
                rect,
                width=int(border * self.zoom_factor),
                border_radius=int(radius * self.zoom_factor),
            )

    def draw_circle(self, centroid: (float, float), radius, color, width=0):
        """Draw a circle at the zoomed coordinates."""
        centroid = (np.array(centroid) * self.zoom_factor).astype(int)
        radius = int(radius * self.zoom_factor)
        pygame.draw.circle(self.screen, color, centroid, radius, width=width)

    def fill(self, color: pygame.Color):
        """Fill the entire screen with the zoomed background color."""
        self.screen.fill(color)

    def handle_FPS(self):
        """Handle the frame rate limit."""
        self.clock.tick(self.FPS)

    def getScreen(self):
        """Return the game screen."""
        return self.screen

    def zoom_in(self, zoom_amount=0.1):
        """Zoom in by the given amount."""
        self.zoom_factor += zoom_amount
        if self.zoom_factor > 3.0:  # Limit zoom in
            self.zoom_factor = 3.0

    def zoom_out(self, zoom_amount=0.1):
        """Zoom out by the given amount."""
        self.zoom_factor -= zoom_amount
        if self.zoom_factor < 0.1:  # Limit zoom out
            self.zoom_factor = 0.1
