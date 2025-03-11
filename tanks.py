# Battle City Game - Tanks Module
# Contains tank-related classes for player and enemies

import pygame
import random
import math
from constants import (
    TILE_SIZE, PLAYER_SPEED, ENEMY_SPEED, SHOOT_COOLDOWN,
    RESPAWN_INVULNERABLE_TIME, POWERUP_DURATION, TANK_TYPES
)
from utils import load_svg
from sprites import Bullet, Explosion

class Tank(pygame.sprite.Sprite):
    """Base class for all tanks"""
    def __init__(self, game, x, y, tank_type=0, *groups):
        super().__init__(*groups)
        self.game = game
        
        # Set tank properties based on type
        self.type = tank_type
        self.speed = TANK_TYPES[tank_type]["speed"]
        self.health = TANK_TYPES[tank_type]["health"]
        
        # Tank appearance
        self.base_image = load_svg("assets/tank_base.svg", TILE_SIZE, TILE_SIZE)
        self.cannon_image = load_svg("assets/tank_cannon.svg", TILE_SIZE, TILE_SIZE)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Initialize tank position and direction
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 0  # 0: up, 1: right, 2: down, 3: left
        self.move_timer = 0
        
        # Shooting mechanics
        self.shoot_cooldown = 0
        self.max_bullets = TANK_TYPES[tank_type]["max_bullets"]
        self.bullets = []
        
        # Apply tank appearance based on type
        self._update_appearance()
    
    def _update_appearance(self):
        """Update tank appearance based on type and direction"""
        # Clear the image
        self.image.fill((0, 0, 0, 0))
        
        # Rotate base and cannon images based on direction
        rotated_base = pygame.transform.rotate(self.base_image, -90 * self.direction)
        rotated_cannon = pygame.transform.rotate(self.cannon_image, -90 * self.direction)
        
        # Get the rect for the rotated images
        base_rect = rotated_base.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
        cannon_rect = rotated_cannon.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
        
        # Apply tank color based on type
        self.image.blit(rotated_base, base_rect)
        self.image.blit(rotated_cannon, cannon_rect)
    
    def move(self, dx, dy):
        """Move tank by the given amount"""
        # Save original position
        old_x, old_y = self.rect.topleft
        
        # Move tank
        self.rect.x += dx
        self.rect.y += dy
        
        # Check for collisions with walls and other tanks
        collided = self._check_collisions()
        
        # Revert position if collision occurred
        if collided:
            self.rect.topleft = (old_x, old_y)
    
    def _check_collisions(self):
        """Check for collisions with walls and other tanks"""
        # This will be overridden by child classes
        return False
    
    def shoot(self):
        """Fire a bullet if cooldown has expired and max bullets not reached"""
        if self.shoot_cooldown <= 0 and len(self.bullets) < self.max_bullets:
            # Calculate bullet spawn position based on direction
            bx, by = self.rect.center
            if self.direction == 0:  # up
                by -= TILE_SIZE // 2
            elif self.direction == 1:  # right
                bx += TILE_SIZE // 2
            elif self.direction == 2:  # down
                by += TILE_SIZE // 2
            elif self.direction == 3:  # left
                bx -= TILE_SIZE // 2
            
            # Create and add bullet
            bullet = Bullet(self.game, bx, by, self.direction, self, self.game.level.bullets)
            self.bullets.append(bullet)
            
            # Reset cooldown
            self.shoot_cooldown = SHOOT_COOLDOWN
            
            return True
        return False
    
    def update(self):
        """Update tank state"""
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Update bullets
        self.bullets = [b for b in self.bullets if b.alive()]

class PlayerTank(Tank):
    """Player-controlled tank"""
    def __init__(self, game, x, y, *groups):
        super().__init__(game, x, y, 0, *groups)  # Type 0 is the player tank
        self.lives = 3
        self.speed = PLAYER_SPEED
        self.respawn_timer = 0
        self.invulnerable_timer = 0
        self.powerups = {
            "shield": 0,
            "freeze": 0,
            "speed": 0
        }
        
        # For blinking effect when invulnerable
        self.blink = False
        self.blink_timer = 0
    
    def handle_event(self, event):
        """Handle input events for player tank"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shoot()
    
    def update(self):
        """Update player tank state"""
        super().update()
        
        # Handle respawn timer
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            return
        
        # Handle invulnerability timer
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            
            # Blinking effect
            self.blink_timer += 1
            if self.blink_timer >= 5:
                self.blink_timer = 0
                self.blink = not self.blink
            
            if self.blink:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
        
        # Handle powerup timers
        for powerup in list(self.powerups.keys()):
            if self.powerups[powerup] > 0:
                self.powerups[powerup] -= 1
        
        # Get keyboard state for movement
        keys = pygame.key.get_pressed()
        
        # Calculate movement direction
        dx, dy = 0, 0
        new_direction = self.direction
        
        if keys[pygame.K_UP]:
            dy = -self.speed
            new_direction = 0
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            new_direction = 1
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            new_direction = 2
        elif keys[pygame.K_LEFT]:
            dx = -self.speed
            new_direction = 3
        
        # Apply speed powerup if active
        if self.powerups["speed"] > 0:
            dx *= 1.5
            dy *= 1.5
        
        # Update direction and appearance if changed
        if new_direction != self.direction:
            self.direction = new_direction
            self._update_appearance()
        
        # Move tank
        if dx != 0 or dy != 0:
            self.move(dx, dy)
    
    def _check_collisions(self):
        """Check for collisions with walls, water, and other tanks"""
        # Check collisions with walls and water
        for wall in self.game.level.walls:
            if self.rect.colliderect(wall.rect):
                return True
        
        for water in self.game.level.water_tiles:
            if self.rect.colliderect(water.rect):
                return True
        
        # Check collisions with enemy tanks
        for enemy in self.game.level.enemy_tanks:
            if self.rect.colliderect(enemy.rect):
                return True
        
        # Check if out of bounds
        if (self.rect.left < 0 or self.rect.right > self.game.screen.get_width() or
            self.rect.top < 0 or self.rect.bottom > self.game.screen.get_height()):
            return True
        
        return False
    
    def hit(self):
        """Handle player tank getting hit"""
        # Ignore if invulnerable
        if self.invulnerable_timer > 0 or self.powerups["shield"] > 0:
            return False
        
        # Create explosion
        Explosion(self.game, *self.rect.center, 1.5, self.game.level.effects)
        
        # Notify game of player hit
        self.game.player_hit()
        
        return True
    
    def respawn(self, x, y):
        """Respawn player tank"""
        self.rect.topleft = (x, y)
        self.direction = 0
        self._update_appearance()
        self.bullets = []
        self.shoot_cooldown = 0
        self.invulnerable_timer = RESPAWN_INVULNERABLE_TIME
    
    def add_powerup(self, powerup_type):
        """Add a powerup to the player tank"""
        if powerup_type == "shield":
            self.powerups["shield"] = POWERUP_DURATION
            self.game.sound_manager.play_powerup()
        elif powerup_type == "freeze":
            self.powerups["freeze"] = POWERUP_DURATION
            self.game.level.freeze_enemies()
            self.game.sound_manager.play_powerup()
        elif powerup_type == "life":
            self.game.lives += 1
            self.game.sound_manager.play_powerup()
        elif powerup_type == "speed":
            self.powerups["speed"] = POWERUP_DURATION
            self.game.sound_manager.play_powerup()

class EnemyTank(Tank):
    """Enemy tank with AI behavior"""
    def __init__(self, game, x, y, tank_type=1, *groups):
        super().__init__(game, x, y, tank_type, *groups)
        self.speed = ENEMY_SPEED
        
        # AI behavior variables
        self.move_timer = 0
        self.move_duration = random.randint(30, 90)  # Frames to move in current direction
        self.shoot_timer = random.randint(30, 90)
        self.frozen = False
        self.frozen_timer = 0
    
    def update(self):
        """Update enemy tank state and AI behavior"""
        super().update()
        
        # Skip update if frozen
        if self.frozen:
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.frozen = False
            return
        
        # Update movement timer
        self.move_timer += 1
        
        # Change direction randomly or when hitting obstacle
        if self.move_timer >= self.move_duration:
            self.direction = random.randint(0, 3)
            self._update_appearance()
            self.move_timer = 0
            self.move_duration = random.randint(30, 90)
        
        # Move in current direction
        dx, dy = 0, 0
        if self.direction == 0:  # up
            dy = -self.speed
        elif self.direction == 1:  # right
            dx = self.speed
        elif self.direction == 2:  # down
            dy = self.speed
        elif self.direction == 3:  # left
            dx = -self.speed
        
        # Try to move
        old_x, old_y = self.rect.topleft
        self.rect.x += dx
        self.rect.y += dy
        
        # Check for collisions
        if self._check_collisions():
            # Revert position and choose a new direction
            self.rect.topleft = (old_x, old_y)
            self.direction = random.randint(0, 3)
            self._update_appearance()
            self.move_timer = 0
        
        # Try to shoot periodically
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            # Aim at player or base sometimes
            if random.random() < 0.3:
                self._aim_at_target()
            
            self.shoot()
            self.shoot_timer = random.randint(30, 90)
    
    def _check_collisions(self):
        """Check for collisions with walls, water, and other tanks"""
        # Check collisions with walls and water
        for wall in self.game.level.walls:
            if self.rect.colliderect(wall.rect):
                return True
        
        for water in self.game.level.water_tiles:
            if self.rect.colliderect(water.rect):
                return True
        
        # Check collisions with other enemy tanks
        for enemy in self.game.level.enemy_tanks:
            if enemy != self and self.rect.colliderect(enemy.rect):
                return True
        
        # Check collision with player tank
        if self.rect.colliderect(self.game.level.player.rect):
            return True
        
        # Check if out of bounds
        if (self.rect.left < 0 or self.rect.right > self.game.screen.get_width() or
            self.rect.top < 0 or self.rect.bottom > self.game.screen.get_height()):
            return True
        
        return False
    
    def _aim_at_target(self):
        """Try to aim at the player or base"""
        # Choose target (player or base)
        if random.random() < 0.7:
            target = self.game.level.player.rect.center
        else:
            target = self.game.level.base.rect.center
        
        # Calculate direction to target
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        
        # Determine which direction to face
        if abs(dx) > abs(dy):
            # Horizontal axis
            if dx > 0:
                self.direction = 1  # right
            else:
                self.direction = 3  # left
        else:
            # Vertical axis
            if dy > 0:
                self.direction = 2  # down
            else:
                self.direction = 0  # up
        
        # Update appearance
        self._update_appearance()
    
    def hit(self):
        """Handle enemy tank getting hit"""
        self.health -= 1
        
        if self.health <= 0:
            # Create explosion
            Explosion(self.game, *self.rect.center, 1.5, self.game.level.effects)
            
            # Add score
            self.game.add_score(TANK_TYPES[self.type]["points"])
            
            # Remove tank
            self.kill()
            return True
        
        return False
    
    def freeze(self, duration):
        """Freeze the enemy tank"""
        self.frozen = True
        self.frozen_timer = duration
