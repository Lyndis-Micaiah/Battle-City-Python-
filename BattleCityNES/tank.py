"""
Tank module for Battle City game
"""
import pygame
import random
from constants import *

class Tank:
    """
    Base class for all tanks
    """
    def __init__(self, x, y, game):
        """
        Initialize a tank
        
        Args:
            x (int): X position
            y (int): Y position
            game (Game): Game instance
        """
        self.x = x
        self.y = y
        self.direction = UP
        self.game = game
        
        # Movement
        self.dx = 0
        self.dy = 0
        self.speed = 2
        
        # Shooting
        self.reload_time = 1000  # milliseconds
        self.last_shot_time = 0
        self.power = 1
        
        # Health and stats
        self.health = 1
        self.lives = 1
    
    def move(self, dx, dy):
        """
        Move the tank
        
        Args:
            dx (int): X direction (-1, 0, 1)
            dy (int): Y direction (-1, 0, 1)
        """
        # Set direction based on movement
        if dx > 0:
            self.direction = RIGHT
        elif dx < 0:
            self.direction = LEFT
        elif dy > 0:
            self.direction = DOWN
        elif dy < 0:
            self.direction = UP
        
        # Calculate new position
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check for collisions with level boundaries
        if new_x < 0 or new_x > SCREEN_WIDTH - TILE_SIZE or new_y < 0 or new_y > SCREEN_HEIGHT - TILE_SIZE:
            return False
        
        # Create a new rectangle for collision testing
        new_rect = pygame.Rect(new_x, new_y, TILE_SIZE, TILE_SIZE)
        
        # Check for collisions with terrain
        if self.check_terrain_collision(new_rect):
            return False
        
        # Check for collisions with other tanks
        if self.check_tank_collision(new_rect):
            return False
        
        # Update position
        self.x = new_x
        self.y = new_y
        return True
    
    def check_terrain_collision(self, rect):
        """
        Check if the tank collides with terrain
        
        Args:
            rect (pygame.Rect): Rectangle for collision testing
        
        Returns:
            bool: True if collision occurred, False otherwise
        """
        # Get surrounding tiles
        tile_x1 = int(rect.left // TILE_SIZE)
        tile_y1 = int(rect.top // TILE_SIZE)
        tile_x2 = int((rect.right - 1) // TILE_SIZE)
        tile_y2 = int((rect.bottom - 1) // TILE_SIZE)
        
        # Check each tile
        for tile_x in range(tile_x1, tile_x2 + 1):
            for tile_y in range(tile_y1, tile_y2 + 1):
                # Skip if out of bounds
                if (tile_x < 0 or tile_x >= self.game.level.width or 
                        tile_y < 0 or tile_y >= self.game.level.height):
                    return True
                
                tile = self.game.level.get_tile(tile_x, tile_y)
                
                # Check if tile is solid
                if tile in [BRICK, STEEL, WATER, BASE]:
                    return True
        
        return False
    
    def check_tank_collision(self, rect):
        """
        Check if the tank collides with other tanks
        
        Args:
            rect (pygame.Rect): Rectangle for collision testing
        
        Returns:
            bool: True if collision occurred, False otherwise
        """
        # Check collision with player
        if self != self.game.player and self.game.player.lives > 0:
            if rect.colliderect(self.game.player.get_rect()):
                return True
        
        # Check collision with enemies
        for enemy in self.game.enemies:
            if self != enemy and rect.colliderect(enemy.get_rect()):
                return True
        
        return False
    
    def shoot(self):
        """
        Fire a bullet
        """
        current_time = pygame.time.get_ticks()
        
        # Check if can shoot again (reload time passed)
        if current_time - self.last_shot_time < self.reload_time:
            return
        
        # Update last shot time
        self.last_shot_time = current_time
        
        # Calculate bullet starting position
        if self.direction == UP:
            bullet_x = self.x + TILE_SIZE // 2
            bullet_y = self.y
        elif self.direction == RIGHT:
            bullet_x = self.x + TILE_SIZE
            bullet_y = self.y + TILE_SIZE // 2
        elif self.direction == DOWN:
            bullet_x = self.x + TILE_SIZE // 2
            bullet_y = self.y + TILE_SIZE
        elif self.direction == LEFT:
            bullet_x = self.x
            bullet_y = self.y + TILE_SIZE // 2
        
        # Create and add bullet
        from sprites import Bullet
        bullet = Bullet(bullet_x, bullet_y, self.direction, self, self.game)
        self.game.bullets.append(bullet)
        
        # Play sound effect
        self.game.sound_manager.play_sound(TANK_FIRE_SOUND)
    
    def hit(self):
        """
        Handle tank getting hit by a bullet
        
        Returns:
            bool: True if tank is destroyed, False otherwise
        """
        self.health -= 1
        
        if self.health <= 0:
            self.lives -= 1
            
            if self.lives <= 0:
                # Tank is destroyed
                return True
            else:
                # Reset tank
                self.health = 1
        
        return False
    
    def get_rect(self):
        """
        Get the collision rectangle for the tank
        
        Returns:
            pygame.Rect: Rectangle for collision detection
        """
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
    
    def draw(self, surface):
        """
        Draw the tank
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        raise NotImplementedError("Subclasses must implement this method")


class PlayerTank(Tank):
    """
    Player-controlled tank
    """
    def __init__(self, x, y, game):
        """
        Initialize the player tank
        """
        super().__init__(x, y, game)
        
        # Player specific attributes
        self.lives = PLAYER_LIVES
        self.speed = PLAYER_SPEED
        self.power = 1
        self.level = 1
        
        # Shield effect
        self.shield = False
        self.shield_timer = 0
        self.shield_duration = 10000  # 10 seconds
        
        # Invincibility effect
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 10000  # 10 seconds
        
        # Respawn protection
        self.spawn_protection = True
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_protection_duration = 3000  # 3 seconds
    
    def update(self):
        """
        Update player tank state
        """
        current_time = pygame.time.get_ticks()
        
        # Update spawn protection
        if self.spawn_protection and current_time - self.spawn_timer > self.spawn_protection_duration:
            self.spawn_protection = False
        
        # Update shield effect
        if self.shield and current_time - self.shield_timer > self.shield_duration:
            self.shield = False
        
        # Update invincibility effect
        if self.invincible and current_time - self.invincible_timer > self.invincible_duration:
            self.invincible = False
        
        # Handle movement input
        keys = pygame.key.get_pressed()
        moved = False
        
        if keys[pygame.K_UP]:
            moved = self.move(0, -1)
        elif keys[pygame.K_RIGHT]:
            moved = self.move(1, 0)
        elif keys[pygame.K_DOWN]:
            moved = self.move(0, 1)
        elif keys[pygame.K_LEFT]:
            moved = self.move(-1, 0)
        
        # Play movement sound
        if moved:
            self.game.sound_manager.play_sound(TANK_MOVE_SOUND)
        
        # Handle shooting input
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def hit(self):
        """
        Handle player tank getting hit
        
        Returns:
            bool: True if tank is destroyed, False otherwise
        """
        # Ignore hit if invincible or has shield or spawn protection
        if self.invincible or self.shield or self.spawn_protection:
            return False
        
        return super().hit()
    
    def respawn(self):
        """
        Respawn the player tank at the starting position
        """
        # Get player start position
        start_pos = self.game.level.get_player_start_position()
        self.x = start_pos[0]
        self.y = start_pos[1]
        
        # Reset attributes
        self.direction = UP
        self.health = 1
        
        # Enable spawn protection
        self.spawn_protection = True
        self.spawn_timer = pygame.time.get_ticks()
    
    def upgrade(self):
        """
        Upgrade the player tank
        """
        self.level = min(self.level + 1, 4)
        
        # Upgrade stats based on level
        if self.level >= 2:
            self.reload_time = 800  # Faster reload time
        
        if self.level >= 3:
            self.power = 2  # Can destroy steel walls
        
        if self.level >= 4:
            self.speed = 3  # Faster movement
    
    def draw(self, surface):
        """
        Draw the player tank
        """
        # Draw tank sprite
        tank_sprite = self.game.sprites.player_tank[self.direction]
        surface.blit(tank_sprite, (self.x, self.y))
        
        # Draw shield effect if active
        if self.shield or self.spawn_protection or self.invincible:
            # Draw shield as a semi-transparent circle
            shield_surface = pygame.Surface((TILE_SIZE + 10, TILE_SIZE + 10), pygame.SRCALPHA)
            
            if self.shield:
                color = (0, 0, 255, 128)  # Blue
            elif self.invincible:
                color = (255, 255, 0, 128)  # Yellow
            else:  # spawn protection
                color = (255, 255, 255, 128)  # White
            
            pygame.draw.circle(shield_surface, color, (TILE_SIZE // 2 + 5, TILE_SIZE // 2 + 5), TILE_SIZE // 2 + 5)
            surface.blit(shield_surface, (self.x - 5, self.y - 5))


class EnemyTank(Tank):
    """
    AI-controlled enemy tank
    """
    def __init__(self, x, y, game, tank_type=BASIC_TANK):
        """
        Initialize an enemy tank
        
        Args:
            x (int): X position
            y (int): Y position
            game (Game): Game instance
            tank_type (int): Type of tank
        """
        super().__init__(x, y, game)
        
        self.tank_type = tank_type
        
        # Set attributes based on tank type
        if tank_type == BASIC_TANK:
            self.speed = ENEMY_SPEED
            self.health = 1
            self.reload_time = 2000
            self.power = 1
        elif tank_type == FAST_TANK:
            self.speed = ENEMY_SPEED * 1.5
            self.health = 1
            self.reload_time = 1500
            self.power = 1
        elif tank_type == POWER_TANK:
            self.speed = ENEMY_SPEED * 0.8
            self.health = 1
            self.reload_time = 1200
            self.power = 2  # Can destroy steel walls
        elif tank_type == ARMOR_TANK:
            self.speed = ENEMY_SPEED * 0.7
            self.health = 4
            self.reload_time = 2000
            self.power = 1
        
        # AI attributes
        self.move_timer = pygame.time.get_ticks()
        self.move_delay = random.randint(500, 2000)
        self.direction_change_probability = 0.02
    
    def update(self):
        """
        Update enemy tank state and AI
        """
        current_time = pygame.time.get_ticks()
        
        # Shoot with a certain probability
        if random.random() < 0.02:  # 2% chance per frame to try shooting
            self.shoot()
        
        # Move with delay
        if current_time - self.move_timer > self.move_delay:
            # Reset timer
            self.move_timer = current_time
            self.move_delay = random.randint(500, 2000)
            
            # Try to move towards player or base
            target = self.get_target()
            self.move_towards(target)
        else:
            # Continue moving in current direction with a chance to change
            if random.random() < self.direction_change_probability:
                self.direction = random.randint(0, 3)
            
            # Move based on current direction
            if self.direction == UP:
                self.move(0, -1)
            elif self.direction == RIGHT:
                self.move(1, 0)
            elif self.direction == DOWN:
                self.move(0, 1)
            elif self.direction == LEFT:
                self.move(-1, 0)
    
    def get_target(self):
        """
        Decide whether to target the player or the base
        
        Returns:
            tuple: (x, y) position to target
        """
        # Target player with 70% probability if player is alive
        if self.game.player.lives > 0 and random.random() < 0.7:
            return (self.game.player.x, self.game.player.y)
        
        # Otherwise target the base
        base_pos = self.game.level.get_base_position()
        if base_pos:
            return base_pos
        
        # Fallback to random position
        return (random.randint(0, SCREEN_WIDTH - TILE_SIZE), 
                random.randint(0, SCREEN_HEIGHT - TILE_SIZE))
    
    def move_towards(self, target):
        """
        Move towards the target position
        
        Args:
            target (tuple): (x, y) position to move towards
        """
        dx = 0
        dy = 0
        
        # Determine predominant direction to target
        if abs(target[0] - self.x) > abs(target[1] - self.y):
            # Move horizontally
            if target[0] > self.x:
                dx = 1
            else:
                dx = -1
        else:
            # Move vertically
            if target[1] > self.y:
                dy = 1
            else:
                dy = -1
        
        # Try to move in the calculated direction
        moved = self.move(dx, dy)
        
        # If couldn't move, try the other direction
        if not moved:
            if dx != 0:
                # Try vertical
                dy = 1 if random.random() < 0.5 else -1
                moved = self.move(0, dy)
                
                if not moved:
                    # Try other vertical
                    moved = self.move(0, -dy)
            else:
                # Try horizontal
                dx = 1 if random.random() < 0.5 else -1
                moved = self.move(dx, 0)
                
                if not moved:
                    # Try other horizontal
                    moved = self.move(-dx, 0)
        
        # If still couldn't move, choose random direction
        if not moved:
            self.direction = random.randint(0, 3)
    
    def draw(self, surface):
        """
        Draw the enemy tank
        """
        # Draw tank sprite
        tank_sprite = self.game.sprites.enemy_tanks[self.tank_type][self.direction]
        surface.blit(tank_sprite, (self.x, self.y))
        
        # Draw health bar for armor tanks
        if self.tank_type == ARMOR_TANK and self.health > 0:
            health_width = (TILE_SIZE * self.health) // 4
            pygame.draw.rect(surface, RED, (self.x, self.y - 5, TILE_SIZE, 3))
            pygame.draw.rect(surface, GREEN, (self.x, self.y - 5, health_width, 3))
