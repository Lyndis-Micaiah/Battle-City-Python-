# Battle City Game - Sprites Module
# Contains base sprite classes and implementations

import pygame
import math
from constants import TILE_SIZE, BULLET_SPEED, EXPLOSION_DURATION
from utils import load_svg

class GameObject(pygame.sprite.Sprite):
    """Base class for all game objects"""
    def __init__(self, game, x, y, image_path, *groups):
        super().__init__(*groups)
        self.game = game
        self.image = load_svg(image_path, TILE_SIZE, TILE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        """Update method to be overridden by child classes"""
        pass

class Wall(GameObject):
    """Base class for walls"""
    def __init__(self, game, x, y, image_path, destructible=False, *groups):
        super().__init__(game, x, y, image_path, *groups)
        self.destructible = destructible

class BrickWall(Wall):
    """Destructible brick wall"""
    def __init__(self, game, x, y, *groups):
        super().__init__(game, x, y, "assets/brick_wall.svg", True, *groups)
        self.health = 4  # Can be hit 4 times before being destroyed
    
    def damage(self):
        """Reduce wall health when hit"""
        self.health -= 1
        # Modify appearance based on damage
        alpha = 255 * (self.health / 4)
        self.image.set_alpha(int(alpha))
        if self.health <= 0:
            self.game.sound_manager.play_brick_break()
            self.kill()
            return True
        self.game.sound_manager.play_brick_hit()
        return False

class SteelWall(Wall):
    """Indestructible steel wall"""
    def __init__(self, game, x, y, *groups):
        super().__init__(game, x, y, "assets/steel_wall.svg", False, *groups)
    
    def damage(self):
        """Steel walls can't be damaged by regular bullets"""
        self.game.sound_manager.play_steel_hit()
        return False

class Water(GameObject):
    """Water tile - impassable but bullets go through"""
    def __init__(self, game, x, y, *groups):
        super().__init__(game, x, y, "assets/water.svg", *groups)
        # Animate water by cycling alpha
        self.animation_timer = 0
        self.alpha_dir = 1  # 1 for increasing, -1 for decreasing
        self.alpha = 200
    
    def update(self):
        """Animate water by changing alpha"""
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.alpha += 2 * self.alpha_dir
            if self.alpha >= 230:
                self.alpha_dir = -1
            elif self.alpha <= 180:
                self.alpha_dir = 1
            self.image.set_alpha(self.alpha)

class Bush(GameObject):
    """Bush tile - can be passed through, provides cover"""
    def __init__(self, game, x, y, *groups):
        super().__init__(game, x, y, "assets/bush.svg", *groups)
        # Make slightly transparent
        self.image.set_alpha(200)

class Base(GameObject):
    """Player base that must be defended"""
    def __init__(self, game, x, y, *groups):
        super().__init__(game, x, y, "assets/base.svg", *groups)
        self.destroyed = False
    
    def destroy(self):
        """Handle base destruction"""
        if not self.destroyed:
            self.destroyed = True
            self.game.sound_manager.play_base_destroyed()
            # Change image to destroyed base
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((0, 0, 0))
            pygame.draw.rect(self.image, (100, 100, 100), 
                             (0, 0, TILE_SIZE, TILE_SIZE))
            pygame.draw.line(self.image, (255, 0, 0), (0, 0), 
                            (TILE_SIZE, TILE_SIZE), 3)
            pygame.draw.line(self.image, (255, 0, 0), (TILE_SIZE, 0), 
                            (0, TILE_SIZE), 3)

class Bullet(GameObject):
    """Bullet class for tank projectiles"""
    def __init__(self, game, x, y, direction, owner, *groups):
        super().__init__(game, x, y, "assets/bullet.svg", *groups)
        self.direction = direction  # 0: up, 1: right, 2: down, 3: left
        self.owner = owner  # Reference to the tank that fired the bullet
        
        # Rotate image based on direction
        if direction == 1:  # right
            self.image = pygame.transform.rotate(self.image, -90)
        elif direction == 2:  # down
            self.image = pygame.transform.rotate(self.image, 180)
        elif direction == 3:  # left
            self.image = pygame.transform.rotate(self.image, 90)
        
        # Adjust rect for the rotated image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Set velocity based on direction
        self.vx, self.vy = 0, 0
        if direction == 0:  # up
            self.vy = -BULLET_SPEED
        elif direction == 1:  # right
            self.vx = BULLET_SPEED
        elif direction == 2:  # down
            self.vy = BULLET_SPEED
        elif direction == 3:  # left
            self.vx = -BULLET_SPEED
        
        # Play sound
        self.game.sound_manager.play_shoot()
    
    def update(self):
        """Move the bullet and check for collisions"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Check if bullet is out of screen bounds
        if (self.rect.right < 0 or self.rect.left > self.game.screen.get_width() or
            self.rect.bottom < 0 or self.rect.top > self.game.screen.get_height()):
            self.kill()
            return

class PowerUp(GameObject):
    """Base class for power-ups"""
    def __init__(self, game, x, y, type_str, *groups):
        image_path = f"assets/powerup_{type_str}.svg"
        super().__init__(game, x, y, image_path, *groups)
        self.type = type_str
        self.blink_timer = 0
        self.visible = True
        
    def update(self):
        """Make power-up blink"""
        self.blink_timer += 1
        if self.blink_timer >= 30:  # Toggle visibility every 30 frames (0.5 seconds at 60 FPS)
            self.blink_timer = 0
            self.visible = not self.visible
            if self.visible:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(100)

class Explosion(GameObject):
    """Explosion effect when tanks or bullets are destroyed"""
    def __init__(self, game, x, y, size=1.0, *groups):
        super().__init__(game, x, y, "assets/explosion.svg", *groups)
        
        # Resize based on explosion size
        width = int(TILE_SIZE * size)
        height = int(TILE_SIZE * size)
        self.image = load_svg("assets/explosion.svg", width, height)
        
        # Center the explosion
        self.rect = self.image.get_rect(center=(x, y))
        
        # Explosion animation
        self.timer = 0
        self.duration = EXPLOSION_DURATION
        self.alpha = 255
        
        # Play sound
        self.game.sound_manager.play_explosion()
    
    def update(self):
        """Update explosion animation"""
        self.timer += 1
        
        # Calculate fade out
        self.alpha = 255 * (1 - (self.timer / self.duration))
        self.image.set_alpha(int(self.alpha))
        
        # Remove explosion when animation complete
        if self.timer >= self.duration:
            self.kill()
