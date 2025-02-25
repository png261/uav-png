import pygame
from Singleton import Singleton


@Singleton
class SoundManager:
    def __init__(self):
        """Initialize the sound manager."""
        pygame.mixer.init()  # Initialize the mixer module
        self.sounds = {}  # Dictionary to hold sound objects
        self.music_playing = False

    def load_sound(self, name, file_path):
        """
        Load a sound effect into the manager.

        Args:
            name (str): Name to reference the sound.
            file_path (str): Path to the sound file.
        """
        self.sounds[name] = pygame.mixer.Sound(file_path)

    def play_sound(self, name, loops=0, maxtime=0, fade_ms=0):
        """
        Play a sound effect.

        Args:
            name (str): Name of the sound to play.
            loops (int): Number of times to loop the sound (default is 0).
            maxtime (int): Maximum time to play the sound in milliseconds (default is 0).
            fade_ms (int): Fade-in time in milliseconds (default is 0).
        """
        if name in self.sounds:
            self.sounds[name].play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        else:
            print(f"Sound '{name}' not found!")

    def stop_sound(self, name):
        """
        Stop a sound effect.

        Args:
            name (str): Name of the sound to stop.
        """
        if name in self.sounds:
            self.sounds[name].stop()
        else:
            print(f"Sound '{name}' not found!")

    def play_music(self, file_path, loops=-1, start=0.0, fade_ms=0):
        """
        Play background music.

        Args:
            file_path (str): Path to the music file.
            loops (int): Number of times to loop the music (default is -1 for infinite).
            start (float): Position to start playback (in seconds).
            fade_ms (int): Fade-in time in milliseconds (default is 0).
        """
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
        self.music_playing = True

    def stop_music(self, fade_ms=0):
        """
        Stop the background music.

        Args:
            fade_ms (int): Fade-out time in milliseconds (default is 0).
        """
        pygame.mixer.music.fadeout(fade_ms)
        pygame.mixer.music.stop()
        self.music_playing = False

    def set_volume(self, name, volume):
        """
        Set the volume of a sound effect.

        Args:
            name (str): Name of the sound.
            volume (float): Volume level (0.0 to 1.0).
        """
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        else:
            print(f"Sound '{name}' not found!")

    def set_music_volume(self, volume):
        """
        Set the volume of the background music.

        Args:
            volume (float): Volume level (0.0 to 1.0).
        """
        pygame.mixer.music.set_volume(volume)

    def is_music_playing(self):
        """
        Check if music is currently playing.

        Returns:
            bool: True if music is playing, False otherwise.
        """
        return self.music_playing
