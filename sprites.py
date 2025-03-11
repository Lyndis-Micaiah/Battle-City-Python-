"""
Game sprites module for Battle City
"""
import pygame
import math
import random
from constants import *

class Sprites:
    """
    Handles loading and managing sprites
    """
    def __init__(self):
        """
        Load all game sprites
        """
        # Create dummy surfaces for now (would be replaced by actual sprite sheet)
        self.player_tank = self._create_tank_surface(GREEN)
        self.enemy_tanks = {
            BASIC_TANK: self._create_tank_surface(RED),
            FAST_TANK: self._create_tank_surface(BLUE),
            POWER_TANK: self._create_tank_surface(YELLOW),
            ARMOR_TANK: self._create_tank_surface(GRAY)
        }
        
        self.bullet = self._create_bullet_surface()
        
        self.tiles = {
            BRICK: self._create_brick_surface(),
            STEEL: self._create_steel_surface(),
            WATER: self._create_water_surface(),
            GRASS: self._create_grass_surface(),
            ICE: self._create_ice_surface(),
            BASE: self._create_base_surface()
        }
        
        self.explosion_small = self._create_explosion_surface(16)
        self.explosion_large = self._create_explosion_surface(32)
        
        self.power_ups = {
            SHIELD: self._create_power_up_surface("S"),
            FREEZE: self._create_power_up_surface("F"),
            EXTRA_LIFE: self._create_power_up_surface("L"),
            GRENADE: self._create_power_up_surface("G"),
            HELMET: self._create_power_up_surface("H"),
            CLOCK: self._create_power_up_surface("C"),
            SHOVEL: self._create_power_up_surface("V"),
            STAR: self._create_power_up_surface("*")
        }
    
    def _create_tank_surface(self, color):
        """
        Create a tank surface with specified color
        """
        surfaces = []
        
        # Create tank surfaces for all four directions
        for direction in range(4):
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            
            # Draw tank body
            pygame.draw.rect(surface, color, (4, 4, TILE_SIZE - 8, TILE_SIZE - 8))
            
            # Draw tank cannon
            if direction == UP:
                pygame.draw.rect(surface, color, (TILE_SIZE // 2 - 2, 0, 4, TILE_SIZE // 2))
            elif direction == RIGHT:
                pygame.draw.rect(surface, color, (TILE_SIZE // 2, TILE_SIZE // 2 - 2, TILE_SIZE // 2, 4))
            elif direction == DOWN:
                pygame.draw.rect(surface, color, (TILE_SIZE // 2 - 2, TILE_SIZE // 2, 4, TILE_SIZE // 2))
            elif direction == LEFT:
                pygame.draw.rect(surface, color, (0, TILE_SIZE // 2 - 2, TILE_SIZE // 2, 4))
            
            # Draw tracks
            pygame.draw.rect(surface, BLACK, (2, 6, 4, TILE_SIZE - 12))
            pygame.draw.rect(surface, BLACK, (TILE_SIZE - 6, 6, 4, TILE_SIZE - 12))
            
            surfaces.append(surface)
        
        return surfaces
    
    def _create_bullet_surface(self):
        """
        Create bullet surfaces for all directions
        """
        bullet_surfaces = []
        
        for direction in range(4):
            # Create bullet surface
            if direction == UP or direction == DOWN:
                surface = pygame.Surface((4, 8), pygame.SRCALPHA)
            else:
                surface = pygame.Surface((8, 4), pygame.SRCALPHA)
            
            # Fill the bullet with white color
            surface.fill(WHITE)
            
            bullet_surfaces.append(surface)
        
        return bullet_surfaces
    
    def _create_brick_surface(self):
        """
        Create a brick tile surface
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((204, 102, 0))  # Brown
        
        # Draw brick pattern
        brick_width = TILE_SIZE // 4
        brick_height = TILE_SIZE // 4
        
        for row in range(0, TILE_SIZE, brick_height):
            offset = brick_width // 2 if (row // brick_height) % 2 == 1 else 0
            for col in range(offset, TILE_SIZE, brick_width):
                pygame.draw.rect(surface, (255, 153, 51), (col, row, brick_width - 1, brick_height - 1))
        
        return surface
    
    def _create_steel_surface(self):
        """
        Create a steel tile surface
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(GRAY)
        
        # Draw steel pattern
        pygame.draw.line(surface, (50, 50, 50), (0, 0), (TILE_SIZE, 0), 2)
        pygame.draw.line(surface, (50, 50, 50), (0, 0), (0, TILE_SIZE), 2)
        pygame.draw.line(surface, (200, 200, 200), (0, TILE_SIZE - 1), (TILE_SIZE, TILE_SIZE - 1), 2)
        pygame.draw.line(surface, (200, 200, 200), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE), 2)
        
        return surface
    
    def _create_water_surface(self):
        """
        Create a water tile surface
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((0, 102, 204))  # Blue
        
        # Draw water pattern
        for i in range(0, TILE_SIZE, 8):
            pygame.draw.line(surface, (51, 153, 255), (0, i), (TILE_SIZE, i), 2)
        
        return surface
    
    def _create_grass_surface(self):
        """
        Create a grass tile surface
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((51, 153, 51))  # Green
        
        # Draw grass pattern
        for _ in range(20):
            x = random.randint(0, TILE_SIZE - 2)
            y = random.randint(0, TILE_SIZE - 2)
            pygame.draw.line(surface, (102, 204, 0), (x, y), (x + 2, y + 2), 1)
        
        return surface
    
    def _create_ice_surface(self):
        """
        Create an ice tile surface
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((204, 255, 255))  # Light blue
        
        # Draw ice pattern
        for _ in range(10):
            x = random.randint(0, TILE_SIZE - 5)
            y = random.randint(0, TILE_SIZE - 5)
            pygame.draw.rect(surface, WHITE, (x, y, 5, 5))
        
        return surface
    
    def _create_base_surface(self):
        """
        Create a base tile surface
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(BLACK)
        
        # Draw eagle symbol
        pygame.draw.polygon(surface, YELLOW, [
            (TILE_SIZE // 2, 5),
            (5, TILE_SIZE - 5),
            (TILE_SIZE - 5, TILE_SIZE - 5)
        ])
        
        # Draw base border
        pygame.draw.rect(surface, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 2)
        
        return surface
    
    def _create_explosion_surface(self, size):
        """
        Create an explosion animation frames
        """
        frames = []
        
        # Create 3 frames of increasing size
        for scale in [0.5, 0.75, 1.0, 0.75, 0.5]:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw explosion as a circle and lines
            center = size // 2
            radius = int(size // 2 * scale)
            
            pygame.draw.circle(surface, YELLOW, (center, center), radius)
            pygame.draw.circle(surface, RED, (center, center), int(radius * 0.7))
            
            # Draw lines from center
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x = center + int(math.cos(rad) * radius)
                y = center + int(math.sin(rad) * radius)
                pygame.draw.line(surface, YELLOW, (center, center), (x, y), 2)
            
            frames.append(surface)
        
        return frames
    
    def _create_power_up_surface(self, label):
        """
        Create a power-up surface with the given label
        """
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Draw power-up box
        pygame.draw.rect(surface, WHITE, (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surface, RED, (2, 2, TILE_SIZE - 4, TILE_SIZE - 4), 2)
        
        # Draw label
        font = pygame.font.SysFont('Arial', 18)
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
        surface.blit(text, text_rect)
        
        return surface


class Bullet:
    """
    Bullet class for player and enemy tanks
    """
    def __init__(self, x, y, direction, owner, game):
        """
        Initialize a bullet
        
        Args:
            x (int): X position
            y (int): Y position
            direction (int): Direction (UP, RIGHT, DOWN, LEFT)
            owner (Tank): The tank that fired this bullet
            game (Game): Game instance
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.owner = owner
        self.game = game
        self.to_remove = False
        
        # Calculate bullet speed based on direction
        if direction == UP:
            self.dx = 0
            self.dy = -BULLET_SPEED
        elif direction == RIGHT:
            self.dx = BULLET_SPEED
            self.dy = 0
        elif direction == DOWN:
            self.dx = 0
            self.dy = BULLET_SPEED
        elif direction == LEFT:
            self.dx = -BULLET_SPEED
            self.dy = 0
        
        # Set bullet power based on owner
        self.power = 1
        if hasattr(owner, 'power'):
            self.power = owner.power
    
    def update(self):
        """
        Update bullet position and check for collisions
        """
        # Move the bullet
        self.x += self.dx
        self.y += self.dy
        
        # Get bullet rect for collision detection
        bullet_rect = self.get_rect()
        
        # Check if bullet is out of bounds
        if (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT):
            self.to_remove = True
            return
        
        # Check collision with terrain
        self.check_terrain_collision(bullet_rect)
        
        # Check collision with tanks
        self.check_tank_collision(bullet_rect)
        
        # Check collision with other bullets
        self.check_bullet_collision(bullet_rect)
    
    def check_terrain_collision(self, bullet_rect):
        """
        Check and handle collision with terrain
        """
        # Get tile coordinates
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        # Check surrounding tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = tile_x + dx
                check_y = tile_y + dy
                
                # Skip if out of bounds
                if check_x < 0 or check_x >= self.game.level.width or check_y < 0 or check_y >= self.game.level.height:
                    continue
                
                # Get tile and create rect
                tile = self.game.level.get_tile(check_x, check_y)
                tile_rect = pygame.Rect(check_x * TILE_SIZE, check_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                # Check collision
                if tile_rect.colliderect(bullet_rect):
                    if tile == BRICK:
                        # Destroy brick
                        self.game.level.set_tile(check_x, check_y, EMPTY)
                        self.game.sound_manager.play_sound(BRICK_HIT_SOUND)
                        self.to_remove = True
                        self.game.add_explosion(self.x, self.y, 'small')
                        return
                    
                    elif tile == STEEL:
                        # Steel can only be destroyed by power bullets
                        if self.power > 1:
                            self.game.level.set_tile(check_x, check_y, EMPTY)
                            self.game.sound_manager.play_sound(STEEL_HIT_SOUND)
                        else:
                            self.game.sound_manager.play_sound(STEEL_HIT_SOUND)
                        
                        self.to_remove = True
                        self.game.add_explosion(self.x, self.y, 'small')
                        return
                    
                    elif tile == WATER:
                        # Bullets pass through water
                        pass
                    
                    elif tile == BASE:
                        # Destroy base
                        self.game.level.set_tile(check_x, check_y, EMPTY)
                        self.game.level.base_destroyed = True
                        self.game.sound_manager.play_sound(EXPLOSION_SOUND)
                        self.to_remove = True
                        self.game.add_explosion(self.x, self.y, 'large')
                        return
    
    def check_tank_collision(self, bullet_rect):
        """
        Check and handle collision with tanks
        """
        # Check collision with player
        if self.owner != self.game.player and self.game.player.lives > 0:
            if bullet_rect.colliderect(self.game.player.get_rect()):
                # Player hit by enemy bullet
                self.to_remove = True
                self.game.player.hit()
                self.game.add_explosion(self.x, self.y, 'large')
                return
        
        # Check collision with enemies
        for enemy in self.game.enemies[:]:
            if self.owner != enemy and bullet_rect.colliderect(enemy.get_rect()):
                # Enemy hit by bullet
                self.to_remove = True
                
                # Handle enemy hit
                if enemy.hit():  # Returns True if enemy is destroyed
                    self.game.enemies.remove(enemy)
                    self.game.enemies_on_screen -= 1
                    
                    # Award points based on enemy type
                    points = {
                        BASIC_TANK: 100,
                        FAST_TANK: 200,
                        POWER_TANK: 300,
                        ARMOR_TANK: 400
                    }
                    self.game.score += points.get(enemy.tank_type, 100)
                    
                    # Chance to spawn power-up
                    self.game.spawn_power_up(enemy.x, enemy.y)
                
                self.game.add_explosion(self.x, self.y, 'large' if enemy.health <= 0 else 'small')
                return
    
    def check_bullet_collision(self, bullet_rect):
        """
        Check and handle collision with other bullets
        """
        for bullet in self.game.bullets:
            if bullet != self and not bullet.to_remove and bullet_rect.colliderect(bullet.get_rect()):
                # Bullets collide with each other
                self.to_remove = True
                bullet.to_remove = True
                self.game.add_explosion(self.x, self.y, 'small')
                return
    
    def get_rect(self):
        """
        Get the collision rectangle for the bullet
        """
        if self.direction == UP or self.direction == DOWN:
            return pygame.Rect(self.x - 2, self.y - 4, 4, 8)
        else:
            return pygame.Rect(self.x - 4, self.y - 2, 8, 4)
    
    def draw(self, surface):
        """
        Draw the bullet
        """
        bullet_sprite = self.game.sprites.bullet[self.direction]
        rect = self.get_rect()
        surface.blit(bullet_sprite, rect)


class Explosion:
    """
    Explosion animation
    """
    def __init__(self, x, y, size, game):
        """
        Initialize an explosion
        
        Args:
            x (int): X position
            y (int): Y position
            size (str): 'small' or 'large'
            game (Game): Game instance
        """
        self.x = x
        self.y = y
        self.game = game
        self.size = size
        
        # Set frames based on size
        if size == 'small':
            self.frames = self.game.sprites.explosion_small
            self.frame_size = 16
        else:
            self.frames = self.game.sprites.explosion_large
            self.frame_size = 32
        
        self.current_frame = 0
        self.animation_speed = 5  # frames to wait before changing animation frame
        self.frame_counter = 0
        self.done = False
    
    def update(self):
        """
        Update explosion animation
        """
        self.frame_counter += 1
        
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame += 1
            
            # Mark as done when animation is complete
            if self.current_frame >= len(self.frames):
                self.done = True
    
    def draw(self, surface):
        """
        Draw the explosion
        """
        if not self.done and self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]
            rect = pygame.Rect(
                self.x - self.frame_size // 2,
                self.y - self.frame_size // 2,
                self.frame_size,
                self.frame_size
            )
            surface.blit(frame, rect)


class PowerUp:
    """
    Power-up item that can be collected by the player
    """
    def __init__(self, x, y, power_type, game):
        """
        Initialize a power-up
        
        Args:
            x (int): X position
            y (int): Y position
            power_type (int): Type of power-up
            game (Game): Game instance
        """
        self.x = x
        self.y = y
        self.power_type = power_type
        self.game = game
        self.collected = False
        
        # Lifespan of the power-up (10 seconds)
        self.lifespan = 600  # 60 FPS * 10 seconds
        self.counter = 0
        
        # Blinking effect
        self.visible = True
        self.blink_counter = 0
    
    def update(self):
        """
        Update power-up state
        """
        # Update counter
        self.counter += 1
        
        # Blink when about to disappear
        if self.counter > self.lifespan - 180:  # Start blinking 3 seconds before disappearing
            self.blink_counter += 1
            if self.blink_counter >= 10:
                self.blink_counter = 0
                self.visible = not self.visible
        
        # Remove if lifespan is over
        if self.counter >= self.lifespan:
            self.collected = True
            return
        
        # Check collision with player
        if self.game.player.lives > 0:
            if pygame.Rect(
                self.x, self.y, TILE_SIZE, TILE_SIZE
            ).colliderect(self.game.player.get_rect()):
                self.collected = True
                self.apply_effect()
                self.game.sound_manager.play_sound(POWER_UP_SOUND)
                self.game.score += 500  # Bonus points for collecting power-up
    
    def apply_effect(self):
        """
        Apply the power-up effect
        """
        if self.power_type == SHIELD:
            # Shield protects player for a time
            self.game.player.shield = True
            self.game.player.shield_timer = pygame.time.get_ticks()
        
        elif self.power_type == FREEZE:
            # Freeze all enemies
            self.game.enemy_freeze = True
            self.game.freeze_timer = pygame.time.get_ticks()
        
        elif self.power_type == EXTRA_LIFE:
            # Give player an extra life
            self.game.player.lives += 1
        
        elif self.power_type == GRENADE:
            # Destroy all enemies on screen
            for enemy in self.game.enemies[:]:
                self.game.add_explosion(enemy.x, enemy.y, 'large')
                self.game.score += 100  # Points for each destroyed enemy
                self.game.enemies.remove(enemy)
                self.game.enemies_on_screen -= 1
        
        elif self.power_type == HELMET:
            # Temporary invincibility
            self.game.player.invincible = True
            self.game.player.invincible_timer = pygame.time.get_ticks()
        
        elif self.power_type == CLOCK:
            # Add time (not implemented in this version)
            pass
        
        elif self.power_type == SHOVEL:
            # Upgrade base walls to steel
            self.game.level.upgrade_base_walls()
        
        elif self.power_type == STAR:
            # Upgrade player tank
            self.game.player.upgrade()
    
    def draw(self, surface):
        """
        Draw the power-up
        """
        if self.visible:
            power_up_sprite = self.game.sprites.power_ups[self.power_type]
            surface.blit(power_up_sprite, (self.x, self.y))
