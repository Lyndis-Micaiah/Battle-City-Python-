"""
Menu module for Battle City game
"""
import pygame
from constants import *

class Menu:
    """
    Menu system for the game
    """
    def __init__(self, game):
        """
        Initialize the menu
        
        Args:
            game (Game): Game instance
        """
        self.game = game
        
        # Menu state
        self.selection = 0
        
        # Menu options
        self.options = [
            "Start Game",
            "Instructions",
            "Quit"
        ]
        
        # Instructions text
        self.instructions = [
            "How to Play:",
            "Arrow Keys - Move tank",
            "Space - Fire",
            "ESC - Pause game",
            "",
            "Objective:",
            "Destroy all enemy tanks",
            "Protect your base",
            "",
            "Power-ups:",
            "S - Shield",
            "F - Freeze enemies",
            "L - Extra life",
            "G - Grenade (destroy all enemies)",
            "H - Helmet (invincibility)",
            "C - Clock (extra time)",
            "V - Shovel (upgrade base walls)",
            "* - Star (upgrade tank)"
        ]
        
        # Menu background
        self.background = self._create_background()
        
        # Show instructions flag
        self.show_instructions = False
    
    def _create_background(self):
        """
        Create menu background with tank pattern
        
        Returns:
            pygame.Surface: Background surface
        """
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(BLACK)
        
        # Draw tank patterns in background
        tank_sprite = self.game.sprites.player_tank[0]  # Up-facing tank
        enemy_sprite = self.game.sprites.enemy_tanks[BASIC_TANK][0]  # Basic enemy tank
        
        # Draw player tanks at the corners
        background.blit(tank_sprite, (20, 20))
        background.blit(tank_sprite, (SCREEN_WIDTH - 20 - TILE_SIZE, 20))
        background.blit(tank_sprite, (20, SCREEN_HEIGHT - 20 - TILE_SIZE))
        background.blit(tank_sprite, (SCREEN_WIDTH - 20 - TILE_SIZE, SCREEN_HEIGHT - 20 - TILE_SIZE))
        
        # Draw enemy tanks randomly
        for i in range(5):
            x = (SCREEN_WIDTH // 6) * (i + 1) - TILE_SIZE // 2
            background.blit(enemy_sprite, (x, 100))
        
        return background
    
    def handle_event(self, event):
        """
        Handle menu input events
        
        Args:
            event (pygame.event.Event): Event to handle
        """
        if self.show_instructions:
            # Handle events in instructions screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.show_instructions = False
        else:
            # Handle events in main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selection = (self.selection - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selection = (self.selection + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
    
    def select_option(self):
        """
        Handle menu option selection
        """
        if self.selection == 0:
            # Start Game
            self.game.start_game()
        elif self.selection == 1:
            # Instructions
            self.show_instructions = True
        elif self.selection == 2:
            # Quit
            pygame.quit()
            import sys
            sys.exit()
    
    def update(self):
        """
        Update menu state
        """
        # Nothing to update in the menu for now
        pass
    
    def draw(self, surface):
        """
        Draw the menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw background
        surface.blit(self.background, (0, 0))
        
        if self.show_instructions:
            self.draw_instructions(surface)
        else:
            self.draw_main_menu(surface)
    
    def draw_main_menu(self, surface):
        """
        Draw the main menu
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw title
        title_font = pygame.font.SysFont('Arial', 64)
        title_text = title_font.render("BATTLE CITY", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title_text, title_rect)
        
        # Draw options
        option_font = pygame.font.SysFont('Arial', 36)
        
        for i, option in enumerate(self.options):
            # Highlight selected option
            if i == self.selection:
                color = GREEN
                # Draw tank cursor
                tank_sprite = pygame.transform.scale(self.game.sprites.player_tank[RIGHT], (24, 24))
                surface.blit(tank_sprite, (SCREEN_WIDTH // 2 - 140, 250 + i * 50))
            else:
                color = WHITE
            
            text = option_font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            surface.blit(text, rect)
        
        # Draw copyright
        copyright_font = pygame.font.SysFont('Arial', 16)
        copyright_text = copyright_font.render("© 2023 Python Clone of Battle City NES", True, WHITE)
        copyright_rect = copyright_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        surface.blit(copyright_text, copyright_rect)
    
    def draw_instructions(self, surface):
        """
        Draw the instructions screen
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Fill with semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 48)
        title_text = title_font.render("INSTRUCTIONS", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        surface.blit(title_text, title_rect)
        
        # Draw instructions text
        text_font = pygame.font.SysFont('Arial', 24)
        
        for i, line in enumerate(self.instructions):
            color = WHITE
            # Make headers yellow
            if line.endswith(":"):
                color = YELLOW
            
            text = text_font.render(line, True, color)
            rect = text.get_rect(left=100, top=120 + i * 30)
            surface.blit(text, rect)
        
        # Draw return instruction
        return_font = pygame.font.SysFont('Arial', 20)
        return_text = return_font.render("Press ESC or ENTER to return to menu", True, WHITE)
        return_rect = return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(return_text, return_rect)
