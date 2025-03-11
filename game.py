"""
Main game module that handles the game loop and state management
"""
import pygame
import time
import random
from constants import *
from level import Level
from tank import PlayerTank, EnemyTank
from sprites import Sprites
from menu import Menu
from assets.sounds import SoundManager

class Game:
    """
    Main game class that handles game loop and state management
    """
    def __init__(self):
        """
        Initialize the game
        """
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battle City NES")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Load sprites
        self.sprites = Sprites()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Create the menu
        self.menu = Menu(self)
        
        # Game state
        self.state = MENU
        self.current_level = 1
        self.score = 0
        
        # Initialize other attributes that will be set in reset_game
        self.level = None
        self.player = None
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.power_ups = []
        self.enemy_spawn_timer = 0
        self.enemies_left = 0
        self.enemies_on_screen = 0
        
        # Flags
        self.enemy_freeze = False
        self.freeze_timer = 0
        
    def reset_game(self):
        """
        Reset the game to start a new level or game
        """
        # Load the level
        self.level = Level(self.current_level, self)
        
        # Create the player
        player_start_pos = self.level.get_player_start_position()
        self.player = PlayerTank(player_start_pos[0], player_start_pos[1], self)
        
        # Clear game objects
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.power_ups = []
        
        # Reset enemy spawn
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.enemies_left = MAX_ENEMY_COUNT
        self.enemies_on_screen = 0
        
        # Reset flags
        self.enemy_freeze = False
        self.freeze_timer = 0
        
    def run(self):
        """
        Main game loop
        """
        running = True
        
        while running:
            # Check for exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle events based on game state
                if self.state == MENU:
                    self.menu.handle_event(event)
                elif self.state == PLAYING:
                    self.handle_playing_event(event)
                elif self.state == PAUSE:
                    self.handle_pause_event(event)
                elif self.state == GAME_OVER or self.state == VICTORY:
                    self.handle_end_game_event(event)
            
            # Update game logic based on state
            if self.state == MENU:
                self.menu.update()
            elif self.state == PLAYING:
                self.update_playing()
            # Other states don't need continuous updates
            
            # Render the game
            self.render()
            
            # Cap the frame rate
            self.clock.tick(FPS)
    
    def handle_playing_event(self, event):
        """
        Handle events during gameplay
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = PAUSE
    
    def handle_pause_event(self, event):
        """
        Handle events during pause screen
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.state = PLAYING
    
    def handle_end_game_event(self, event):
        """
        Handle events during game over or victory screen
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = MENU
    
    def update_playing(self):
        """
        Update game logic during gameplay
        """
        current_time = pygame.time.get_ticks()
        
        # Update player
        if self.player.lives > 0:
            self.player.update()
        
        # Spawn enemies
        self.spawn_enemies(current_time)
        
        # Update enemies if not frozen
        if not self.enemy_freeze:
            for enemy in self.enemies:
                enemy.update()
        else:
            # Check if freeze timer expired
            if current_time - self.freeze_timer > 10000:  # 10 seconds freeze
                self.enemy_freeze = False
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            
            # Remove bullets that are marked for deletion
            if bullet.to_remove:
                self.bullets.remove(bullet)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            
            # Remove explosions that are done
            if explosion.done:
                self.explosions.remove(explosion)
        
        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            
            # Remove collected power-ups
            if power_up.collected:
                self.power_ups.remove(power_up)
        
        # Check win condition
        if self.enemies_left <= 0 and len(self.enemies) == 0:
            self.handle_level_complete()
        
        # Check lose condition
        if self.player.lives <= 0 or self.level.base_destroyed:
            self.handle_game_over()
    
    def spawn_enemies(self, current_time):
        """
        Spawn enemies based on timer
        """
        if (self.enemies_left > 0 and self.enemies_on_screen < MAX_ENEMIES_ON_SCREEN and 
                current_time - self.enemy_spawn_timer > ENEMY_SPAWN_DELAY):
            # Reset the timer
            self.enemy_spawn_timer = current_time
            
            # Get spawn positions
            spawn_positions = self.level.get_enemy_spawn_positions()
            if spawn_positions:
                # Choose a random spawn position
                pos = random.choice(spawn_positions)
                
                # Determine tank type (with more advanced tanks appearing later)
                tank_type = random.choices(
                    [BASIC_TANK, FAST_TANK, POWER_TANK, ARMOR_TANK],
                    weights=[0.5, 0.3, 0.15, 0.05],
                    k=1
                )[0]
                
                # Create the enemy tank
                enemy = EnemyTank(pos[0], pos[1], self, tank_type)
                self.enemies.append(enemy)
                
                # Update counters
                self.enemies_left -= 1
                self.enemies_on_screen += 1
    
    def handle_level_complete(self):
        """
        Handle level completion
        """
        if self.current_level < LEVEL_COUNT:
            # Move to the next level
            self.current_level += 1
            self.reset_game()
        else:
            # Victory - completed all levels
            self.state = VICTORY
            self.sound_manager.play_sound(GAME_OVER_SOUND)  # Use game over sound for victory too
    
    def handle_game_over(self):
        """
        Handle game over
        """
        self.state = GAME_OVER
        self.sound_manager.play_sound(GAME_OVER_SOUND)
    
    def render(self):
        """
        Render the game based on current state
        """
        # Clear the screen
        self.screen.fill(BLACK)
        
        if self.state == MENU:
            self.menu.draw(self.screen)
        elif self.state == PLAYING or self.state == PAUSE:
            # Draw the level
            self.level.draw(self.screen)
            
            # Draw the player
            if self.player.lives > 0:
                self.player.draw(self.screen)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # Draw bullets
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            # Draw explosions
            for explosion in self.explosions:
                explosion.draw(self.screen)
            
            # Draw power-ups
            for power_up in self.power_ups:
                power_up.draw(self.screen)
            
            # Draw UI elements
            self.draw_ui()
            
            # Draw pause screen if paused
            if self.state == PAUSE:
                self.draw_pause_screen()
        
        elif self.state == GAME_OVER:
            self.draw_game_over_screen()
        
        elif self.state == VICTORY:
            self.draw_victory_screen()
        
        # Update the display
        pygame.display.flip()
    
    def draw_ui(self):
        """
        Draw UI elements like score, lives, remaining enemies
        """
        # Create a font object
        font = pygame.font.SysFont('Arial', 20)
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 40))
        
        # Draw level
        level_text = font.render(f"Level: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (10, 70))
        
        # Draw remaining enemies
        enemies_text = font.render(f"Enemies: {self.enemies_left + len(self.enemies)}", True, WHITE)
        self.screen.blit(enemies_text, (10, 100))
    
    def draw_pause_screen(self):
        """
        Draw the pause screen overlay
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.SysFont('Arial', 48)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        # Instructions
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Press ESC to continue", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(text, text_rect)
    
    def draw_game_over_screen(self):
        """
        Draw the game over screen
        """
        # Background
        self.screen.fill(BLACK)
        
        # Game over text
        font = pygame.font.SysFont('Arial', 64)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Score
        font = pygame.font.SysFont('Arial', 32)
        text = font.render(f"Score: {self.score}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(text, text_rect)
        
        # Instructions
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Press ENTER to return to menu", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(text, text_rect)
    
    def draw_victory_screen(self):
        """
        Draw the victory screen
        """
        # Background
        self.screen.fill(BLACK)
        
        # Victory text
        font = pygame.font.SysFont('Arial', 64)
        text = font.render("VICTORY!", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Final score
        font = pygame.font.SysFont('Arial', 32)
        text = font.render(f"Final Score: {self.score}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(text, text_rect)
        
        # Instructions
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Press ENTER to return to menu", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(text, text_rect)
    
    def add_explosion(self, x, y, size):
        """
        Add an explosion at the given position
        """
        from sprites import Explosion
        explosion = Explosion(x, y, size, self)
        self.explosions.append(explosion)
        self.sound_manager.play_sound(EXPLOSION_SOUND)
    
    def spawn_power_up(self, x, y):
        """
        Randomly spawn a power-up at the given position
        """
        from sprites import PowerUp
        if random.random() < 0.3:  # 30% chance to spawn a power-up
            power_up_type = random.randint(0, 7)  # Choose a random power-up type
            power_up = PowerUp(x, y, power_up_type, self)
            self.power_ups.append(power_up)
    
    def start_game(self):
        """
        Start a new game
        """
        self.current_level = 1
        self.score = 0
        self.reset_game()
        self.state = PLAYING
        self.sound_manager.play_sound(GAME_START_SOUND)
