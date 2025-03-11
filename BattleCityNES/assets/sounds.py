# Battle City Game - Sound Manager Module
# Handles loading and playing game sounds

import pygame

class SoundManager:
    """Class to manage game sounds"""
    
    def __init__(self):
        # Initialize sound system
        pygame.mixer.init()
        
        # Create dummy sounds (since we can't load actual files)
        self.sounds = {}
        
        # Create basic beep sounds with different parameters
        self._create_dummy_sounds()
        
        # Set default volume
        self.set_volume(0.7)
    
    def _create_dummy_sounds(self):
        """Create dummy sounds with pygame's synthesizer"""
        
        # Start game sound
        self.sounds["start_game"] = self._create_synth_sound(440, 500)  # A4, 500ms
        
        # Menu sounds
        self.sounds["menu_move"] = self._create_synth_sound(330, 100)  # E4, 100ms
        self.sounds["menu_select"] = self._create_synth_sound(523, 200)  # C5, 200ms
        
        # Game sounds
        self.sounds["shoot"] = self._create_synth_sound(880, 100)  # A5, 100ms
        self.sounds["explosion"] = self._create_synth_sound(110, 300)  # A2, 300ms
        self.sounds["brick_hit"] = self._create_synth_sound(220, 50)  # A3, 50ms
        self.sounds["brick_break"] = self._create_synth_sound(293, 100)  # D4, 100ms
        self.sounds["steel_hit"] = self._create_synth_sound(440, 50)  # A4, 50ms
        self.sounds["player_hit"] = self._create_synth_sound(550, 200)  # C#5, 200ms
        self.sounds["enemy_hit"] = self._create_synth_sound(440, 100)  # A4, 100ms
        self.sounds["powerup"] = self._create_synth_sound(660, 200)  # E5, 200ms
        self.sounds["base_destroyed"] = self._create_synth_sound(165, 500)  # E3, 500ms
        self.sounds["game_over"] = self._create_synth_sound([392, 349, 330, 294], 1000)  # G4-F4-E4-D4, 1000ms
        self.sounds["level_complete"] = self._create_synth_sound([523, 659, 784], 1000)  # C5-E5-G5, 1000ms
        self.sounds["pause"] = self._create_synth_sound(523, 100)  # C5, 100ms
        self.sounds["unpause"] = self._create_synth_sound(659, 100)  # E5, 100ms
    
    def _create_synth_sound(self, frequency, duration):
        """Create a simple synthesized sound
        
        Args:
            frequency: Frequency in Hz or list of frequencies
            duration: Duration in milliseconds
        
        Returns:
            pygame.mixer.Sound object
        """
        sample_rate = 44100
        bits = 16
        
        # Handle both single frequency and chords/sequences
        if isinstance(frequency, list):
            # Create a chord or sequence
            frequencies = frequency
            samples_per_freq = int(duration / len(frequencies))
            buffer = bytearray()
            
            for freq in frequencies:
                sample_count = int(samples_per_freq * sample_rate / 1000)
                period = int(sample_rate / freq)
                amplitude = 2**(bits - 2) - 1
                
                for i in range(sample_count):
                    if i % period < period / 2:
                        # Square wave
                        value = amplitude
                    else:
                        value = -amplitude
                    
                    # Add value to buffer (assuming 16-bit signed little-endian)
                    buffer.extend([value & 0xFF, (value >> 8) & 0xFF])
        else:
            # Create a single tone
            sample_count = int(duration * sample_rate / 1000)
            period = int(sample_rate / frequency)
            amplitude = 2**(bits - 2) - 1
            buffer = bytearray()
            
            for i in range(sample_count):
                if i % period < period / 2:
                    # Square wave
                    value = amplitude
                else:
                    value = -amplitude
                
                # Add value to buffer (assuming 16-bit signed little-endian)
                buffer.extend([value & 0xFF, (value >> 8) & 0xFF])
        
        return pygame.mixer.Sound(buffer=bytes(buffer))
    
    def set_volume(self, volume):
        """Set volume for all sounds
        
        Args:
            volume: Volume level from 0.0 to 1.0
        """
        for sound in self.sounds.values():
            sound.set_volume(volume)
    
    def play_sound(self, sound_name):
        """Play a sound by name
        
        Args:
            sound_name: Name of the sound to play
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    # Convenience methods for playing specific sounds
    def play_start_game(self):
        self.play_sound("start_game")
    
    def play_menu_move(self):
        self.play_sound("menu_move")
    
    def play_menu_select(self):
        self.play_sound("menu_select")
    
    def play_shoot(self):
        self.play_sound("shoot")
    
    def play_explosion(self):
        self.play_sound("explosion")
    
    def play_brick_hit(self):
        self.play_sound("brick_hit")
    
    def play_brick_break(self):
        self.play_sound("brick_break")
    
    def play_steel_hit(self):
        self.play_sound("steel_hit")
    
    def play_player_hit(self):
        self.play_sound("player_hit")
    
    def play_enemy_hit(self):
        self.play_sound("enemy_hit")
    
    def play_powerup(self):
        self.play_sound("powerup")
    
    def play_base_destroyed(self):
        self.play_sound("base_destroyed")
    
    def play_game_over(self):
        self.play_sound("game_over")
    
    def play_level_complete(self):
        self.play_sound("level_complete")
    
    def play_pause(self):
        self.play_sound("pause")
    
    def play_unpause(self):
        self.play_sound("unpause")
