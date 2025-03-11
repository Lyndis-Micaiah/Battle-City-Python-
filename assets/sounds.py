"""
Sound manager for Battle City game
"""
import pygame
import os
from constants import *

class SoundManager:
    """
    Manages loading and playing sound effects
    """
    def __init__(self):
        """
        Initialize the sound manager
        """
        # Make sure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Dictionary to store sound effects
        self.sounds = {}
        
        # Load sound effects
        self.load_sounds()
        
        # Sound settings
        self.sound_enabled = True
        self.volume = 0.7
        pygame.mixer.set_num_channels(8)  # Set number of simultaneous sounds
    
    def load_sounds(self):
        """
        Load all sound effects
        
        Note: In a real implementation, you'd load actual sound files. 
        Here we're creating placeholder beep sounds with varying frequencies.
        """
        # Create placeholder sounds with different parameters
        self._create_sound(TANK_MOVE_SOUND, frequency=220, duration=100)
        self._create_sound(TANK_FIRE_SOUND, frequency=440, duration=100)
        self._create_sound(EXPLOSION_SOUND, frequency=110, duration=300)
        self._create_sound(BRICK_HIT_SOUND, frequency=330, duration=50)
        self._create_sound(STEEL_HIT_SOUND, frequency=660, duration=50)
        self._create_sound(POWER_UP_SOUND, frequency=880, duration=200)
        self._create_sound(GAME_START_SOUND, frequency=440, duration=500)
        self._create_sound(GAME_OVER_SOUND, frequency=220, duration=1000)
    
    def _create_sound(self, sound_name, frequency=440, duration=100):
        """
        Create a beep sound with the given frequency and duration
        
        Args:
            sound_name (str): Name of the sound
            frequency (int): Frequency in Hz
            duration (int): Duration in milliseconds
        """
        pygame.mixer.Sound
        # We're using pygame's Sound constructor with a bytes buffer
        # This creates a simple sine wave tone at the specified frequency
        sample_rate = 44100  # CD quality audio
        bits = 16  # 16 bits per sample
        
        # Calculate the number of samples
        num_samples = int(duration * sample_rate / 1000)
        
        # Generate a sine wave
        buf = bytearray(num_samples * 2)  # 2 bytes per sample for 16-bit audio
        
        # Create a sound with a decreasing amplitude
        import array
        import math
        
        samples = array.array('h', [0] * num_samples)  # signed short integer array
        
        for i in range(num_samples):
            # Sine wave with decreasing amplitude
            amplitude = 32767 * (1 - i / num_samples)  # 32767 is max amplitude for 16-bit audio
            samples[i] = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
        
        # Convert the array to bytes
        sample_bytes = samples.tobytes()
        
        # Create the pygame Sound object
        self.sounds[sound_name] = pygame.mixer.Sound(buffer=sample_bytes)
        self.sounds[sound_name].set_volume(self.volume)
    
    def play_sound(self, sound_name):
        """
        Play a sound effect
        
        Args:
            sound_name (str): Name of sound to play
        """
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            # Tank movement sound is played in a separate channel to prevent overlap
            if sound_name == TANK_MOVE_SOUND:
                if not pygame.mixer.Channel(0).get_busy():
                    pygame.mixer.Channel(0).play(self.sounds[sound_name])
            else:
                self.sounds[sound_name].play()
    
    def toggle_sound(self):
        """
        Toggle sound on/off
        """
        self.sound_enabled = not self.sound_enabled
    
    def set_volume(self, volume):
        """
        Set volume for all sounds
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
