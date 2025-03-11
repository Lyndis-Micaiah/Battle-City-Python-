# Battle City Game - UI Module
# Handles game UI, menus, and text rendering

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class MenuUI:
    """Class to handle the game menu UI"""
    
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 36)
        self.menu_items = ["Start Game", "How to Play", "Quit"]
        self.selected_item = 0
        self.blink_timer = 0
        self.show_cursor = True
        
        # How to play screen
        self.how_to_play = False
        self.instruction_font = pygame.font.Font(None, 24)
        self.instructions = [
            "Arrow Keys: Move tank",
            "Space: Fire",
            "ESC: Pause game",
            "",
            "Defend your base from enemy tanks!",
            "Destroy all enemy tanks to complete a level.",
            "Collect power-ups for special abilities:",
            "  - Shield: Temporary invulnerability",
            "  - Freeze: Temporarily stop enemy tanks",
            "  - Life: Extra life",
            "",
            "Press any key to return to menu"
        ]
    
    def handle_event(self, event):
        """Handle menu input events"""
        if self.how_to_play:
            if event.type == pygame.KEYDOWN:
                self.how_to_play = False
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                self.game.sound_manager.play_menu_move()
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                self.game.sound_manager.play_menu_move()
            elif event.key == pygame.K_RETURN:
                self._select_menu_item()
    
    def _select_menu_item(self):
        """Handle menu item selection"""
        if self.selected_item == 0:  # Start Game
            self.game.start_game()
            self.game.sound_manager.play_menu_select()
        elif self.selected_item == 1:  # How to Play
            self.how_to_play = True
            self.game.sound_manager.play_menu_select()
        elif self.selected_item == 2:  # Quit
            pygame.quit()
            import sys
            sys.exit()
    
    def draw(self, screen):
        """Draw the menu UI"""
        # Clear screen
        screen.fill((0, 0, 0))
        
        if self.how_to_play:
            self._draw_how_to_play(screen)
        else:
            self._draw_main_menu(screen)
    
    def _draw_main_menu(self, screen):
        """Draw the main menu"""
        # Draw title
        title_text = self.title_font.render("BATTLE CITY", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Draw tank decoration
        self._draw_tank_decoration(screen, SCREEN_WIDTH // 2 - 120, 100)
        self._draw_tank_decoration(screen, SCREEN_WIDTH // 2 + 120, 100)
        
        # Draw menu items
        for i, item in enumerate(self.menu_items):
            if i == self.selected_item:
                color = (255, 255, 0)  # Yellow for selected item
                
                # Blink cursor
                self.blink_timer += 1
                if self.blink_timer >= 30:
                    self.blink_timer = 0
                    self.show_cursor = not self.show_cursor
                
                # Draw cursor
                if self.show_cursor:
                    cursor_text = ">"
                    cursor = self.menu_font.render(cursor_text, True, color)
                    cursor_rect = cursor.get_rect(midright=(SCREEN_WIDTH // 2 - 10, 200 + i * 50))
                    screen.blit(cursor, cursor_rect)
            else:
                color = (200, 200, 200)  # Light gray for unselected items
            
            # Draw menu item
            text = self.menu_font.render(item, True, color)
            text_rect = text.get_rect(midleft=(SCREEN_WIDTH // 2, 200 + i * 50))
            screen.blit(text, text_rect)
        
        # Draw credits
        credits = self.instruction_font.render("NES Battle City Recreation", True, (150, 150, 150))
        credits_rect = credits.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(credits, credits_rect)
    
    def _draw_how_to_play(self, screen):
        """Draw the how to play screen"""
        # Draw title
        title_text = self.menu_font.render("HOW TO PLAY", True, (255, 255, 0))
        title_rect = title_text.get_rect(midtop=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Draw instructions
        for i, line in enumerate(self.instructions):
            text = self.instruction_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(midleft=(50, 100 + i * 30))
            screen.blit(text, text_rect)
    
    def _draw_tank_decoration(self, screen, x, y):
        """Draw a decorative tank"""
        # Simple tank drawing
        pygame.draw.rect(screen, (0, 200, 0), (x - 15, y - 10, 30, 20))
        pygame.draw.rect(screen, (0, 150, 0), (x - 10, y - 20, 20, 40))
        pygame.draw.rect(screen, (0, 200, 0), (x - 3, y - 30, 6, 20))

class GameUI:
    """Class to handle in-game UI elements"""
    
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, screen):
        """Draw game UI elements"""
        # Draw score
        score_text = self.font.render(f"SCORE: {self.game.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f"LIVES: {self.game.lives}", True, (255, 255, 255))
        lives_rect = lives_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(lives_text, lives_rect)
        
        # Draw level number
        level_text = self.font.render(f"LEVEL: {self.game.current_level_num}", True, (255, 255, 255))
        level_rect = level_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
        screen.blit(level_text, level_rect)
        
        # Draw remaining enemies
        if self.game.level:
            enemies_remaining = self.game.level.max_enemies - self.game.level.enemies_destroyed
            enemies_text = self.font.render(f"ENEMIES: {enemies_remaining}", True, (255, 255, 255))
            enemies_rect = enemies_text.get_rect(topleft=(10, 40))
            screen.blit(enemies_text, enemies_rect)
        
        # Draw active powerups
        if self.game.level and self.game.level.player:
            powerup_y = 40
            for powerup, time in self.game.level.player.powerups.items():
                if time > 0:
                    # Convert time to seconds
                    seconds = time // 60
                    powerup_text = self.font.render(f"{powerup.upper()}: {seconds}s", True, (255, 255, 0))
                    powerup_rect = powerup_text.get_rect(topright=(SCREEN_WIDTH - 10, powerup_y))
                    screen.blit(powerup_text, powerup_rect)
                    powerup_y += 25
