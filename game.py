# Battle City Game - Game Module
# Handles the main game loop and state

import pygame
from enum import Enum, auto
from level import Level
from ui import MenuUI, GameUI
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_PLAYER_LIVES
from assets.sounds import SoundManager

class GameState(Enum):
    """Enum to track the current game state"""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    LEVEL_COMPLETE = auto()

class Game:
    """Main game class that manages the game state and components"""
    
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.MENU
        self.current_level_num = 1
        self.level = None
        self.menu_ui = MenuUI(self)
        self.game_ui = GameUI(self)
        self.score = 0
        self.lives = MAX_PLAYER_LIVES
        self.sound_manager = SoundManager()
        self.last_state_change = pygame.time.get_ticks()
        self.state_delay = 1000  # Delay in milliseconds for state transitions
        
    def handle_event(self, event):
        """Handle pygame events based on current game state"""
        if self.state == GameState.MENU:
            self.menu_ui.handle_event(event)
        elif self.state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = GameState.PAUSED
                self.sound_manager.play_pause()
            else:
                if self.level:
                    self.level.handle_event(event)
        elif self.state == GameState.PAUSED:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.PLAYING
                    self.sound_manager.play_unpause()
                elif event.key == pygame.K_q:
                    self.state = GameState.MENU
        elif self.state in (GameState.GAME_OVER, GameState.VICTORY, GameState.LEVEL_COMPLETE):
            if event.type == pygame.KEYDOWN and pygame.time.get_ticks() - self.last_state_change > self.state_delay:
                if self.state == GameState.LEVEL_COMPLETE:
                    self.current_level_num += 1
                    if self.current_level_num > 3:  # We have 3 levels
                        self.state = GameState.VICTORY
                    else:
                        self.start_level()
                else:
                    self.state = GameState.MENU
    
    def update(self):
        """Update game based on current state"""
        if self.state == GameState.PLAYING:
            if self.level:
                self.level.update()
                
                # Check for level completion or game over
                if self.level.is_completed():
                    self.state = GameState.LEVEL_COMPLETE
                    self.sound_manager.play_level_complete()
                    self.last_state_change = pygame.time.get_ticks()
                    self.add_score(1000)  # Bonus for completing level
                elif self.level.is_game_over():
                    self.state = GameState.GAME_OVER
                    self.sound_manager.play_game_over()
                    self.last_state_change = pygame.time.get_ticks()
    
    def draw(self):
        """Draw the game based on current state"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.MENU:
            self.menu_ui.draw(self.screen)
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            if self.level:
                self.level.draw(self.screen)
            self.game_ui.draw(self.screen)
            
            if self.state == GameState.PAUSED:
                # Draw pause overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))  # Semi-transparent black
                self.screen.blit(overlay, (0, 0))
                
                # Draw pause text
                font = pygame.font.Font(None, 48)
                text = font.render("PAUSED", True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
                
                font = pygame.font.Font(None, 24)
                text = font.render("Press ESC to resume or Q to quit", True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                self.screen.blit(text, text_rect)
        
        elif self.state == GameState.GAME_OVER:
            font = pygame.font.Font(None, 48)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 24)
            text = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(text, text_rect)
            
            text = font.render("Press any key to return to menu", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(text, text_rect)
        
        elif self.state == GameState.VICTORY:
            font = pygame.font.Font(None, 48)
            text = font.render("VICTORY!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 24)
            text = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(text, text_rect)
            
            text = font.render("Press any key to return to menu", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(text, text_rect)
        
        elif self.state == GameState.LEVEL_COMPLETE:
            font = pygame.font.Font(None, 48)
            text = font.render(f"LEVEL {self.current_level_num} COMPLETE!", True, (255, 255, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 24)
            text = font.render("Press any key to continue", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(text, text_rect)
    
    def start_game(self):
        """Start a new game"""
        self.score = 0
        self.lives = MAX_PLAYER_LIVES
        self.current_level_num = 1
        self.start_level()
        self.state = GameState.PLAYING
        self.sound_manager.play_start_game()
    
    def start_level(self):
        """Start or restart the current level"""
        self.level = Level(self, self.current_level_num)
        self.state = GameState.PLAYING
    
    def player_hit(self):
        """Handle player being hit"""
        self.lives -= 1
        self.sound_manager.play_player_hit()
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
            self.sound_manager.play_game_over()
            self.last_state_change = pygame.time.get_ticks()
        else:
            self.level.reset_player()
    
    def add_score(self, points):
        """Add points to the player's score"""
        self.score += points
