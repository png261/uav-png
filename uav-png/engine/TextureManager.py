import pygame
from .Singleton import Singleton
from .Window import Window


@Singleton
class TextureManager:
    def __init__(self):
        """Initialize the texture manager."""
        self.textures = {}  # Dictionary to hold loaded textures

    def load_texture(self, name, file_path, colorkey=None, scale=None):
        """
        Load a texture (image) into the manager.

        Args:
            name (str): Name to reference the texture.
            file_path (str): Path to the texture file.
            colorkey (tuple): RGB tuple for transparency (optional).
            scale (tuple): New size to scale the image to, as (width, height) (optional).
        """
        try:
            texture = pygame.image.load(
                file_path
            ).convert_alpha()  # Load with alpha support

            if colorkey is not None:
                texture.set_colorkey(colorkey)

            if scale is not None:
                texture = pygame.transform.scale(texture, scale)

            self.textures[name] = texture
        except pygame.error as e:
            print(f"Error loading texture '{file_path}': {e}")

    def get_texture(self, name):
        """
        Get a loaded texture by name.

        Args:
            name (str): Name of the texture.

        Returns:
            pygame.Surface: The texture surface, or None if not found.
        """
        return self.textures.get(name, None)

    def draw_texture(self, window: Window, name, position, rotation=0, scale=None):
        """
        Draw a texture to the screen.

        Args:
            screen (pygame.Surface): The surface to draw the texture on.
            name (str): Name of the texture to draw.
            position (tuple): (x, y) position to draw the texture.
            rotation (float): Degrees to rotate the texture (optional).
            scale (tuple): New size to scale the texture to, as (width, height) (optional).
        """
        texture = self.get_texture(name)
        if texture is None:
            print(f"Texture '{name}' not found!")
            return

        # Apply rotation and scaling if needed
        if rotation != 0 or scale is not None:
            texture = texture.copy()  # Avoid modifying the original
            if scale is not None:
                scale = (
                    int(scale[0] * window.zoom_factor),
                    int(scale[1] * window.zoom_factor),
                )
                texture = pygame.transform.scale(texture, scale)
            if rotation != 0:
                texture = pygame.transform.rotate(texture, rotation)

        # Draw the texture with adjusted position based on zoom
        rect = texture.get_rect(topleft=position)
        window.draw_image(texture, rect)

    def unload_texture(self, name):
        """
        Remove a texture from the manager.

        Args:
            name (str): Name of the texture to remove.
        """
        if name in self.textures:
            del self.textures[name]
        else:
            print(f"Texture '{name}' not found!")

    def clear_textures(self):
        """Clear all loaded textures."""
        self.textures.clear()
