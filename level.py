# Battle City Game - Level Module
# Handles level loading, rendering, and game logic

import pygame
import json
import random
from constants import TILE_SIZE, POWERUP_SPAWN_CHANCE, FREEZE_DURATION
from sprites import (
    BrickWall, SteelWall, Water, Bush, Base, PowerUp, Explosion
)
from tanks import PlayerTank, EnemyTank

class Level:
    """Class to manage level data and game objects"""
    
    def __init__(self, game, level_number):
        self.game = game
        self.level_number = level_number
        
        # Sprite groups
        self.walls = pygame.sprite.Group()
        self.water_tiles = pygame.sprite.Group()
        self.bushes = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_tanks = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        
        # Player and base
        self.player = None
        self.base = None
        
        # Enemy spawn data
        self.enemy_spawn_points = []
        self.enemy_types = []
        self.enemy_count = 0
        self.max_enemies = 0
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        self.spawn_timer = 0
        
        # Load level data
        self.load_level(level_number)
    
    def load_level(self, level_number):
        """Load level data from JSON file"""
        try:
            with open(f"levels/level{level_number}.json", "r") as file:
                level_data = json.load(file)
            
            # Parse level layout
            self._parse_layout(level_data["layout"])
            
            # Set enemy data
            self.max_enemies = level_data["enemy_count"]
            self.enemy_types = level_data["enemy_types"]
            
        except Exception as e:
            print(f"Error loading level: {e}")
            # Create a simple default level if loading fails
            self._create_default_level()
    
    def _parse_layout(self, layout):
        """Parse level layout data"""
        rows = len(layout)
        cols = len(layout[0]) if rows > 0 else 0
        
        for y in range(rows):
            for x in range(cols):
                # Handle potential string index errors
                if x >= len(layout[y]):
                    print(f"Warning: Layout row {y} is shorter than expected")
                    continue
                    
                tile = layout[y][x]
                pos_x = x * TILE_SIZE
                pos_y = y * TILE_SIZE
                
                # Skip empty spaces
                if tile == ' ':
                    continue
                    
                if tile == "B":  # Brick wall
                    BrickWall(self.game, pos_x, pos_y, self.walls)
                elif tile == "S":  # Steel wall
                    SteelWall(self.game, pos_x, pos_y, self.walls)
                elif tile == "W":  # Water
                    Water(self.game, pos_x, pos_y, self.water_tiles)
                elif tile == "G":  # Bush (grass)
                    Bush(self.game, pos_x, pos_y, self.bushes)
                elif tile == "P":  # Player start position
                    self.player = PlayerTank(self.game, pos_x, pos_y)
                elif tile == "E":  # Enemy spawn point
                    self.enemy_spawn_points.append((pos_x, pos_y))
                elif tile == "X":  # Base
                    self.base = Base(self.game, pos_x, pos_y)
    
    def _create_default_level(self):
        """Create a simple default level if loading fails"""
        # Create base
        self.base = Base(self.game, 240, 448)
        
        # Create player
        self.player = PlayerTank(self.game, 240, 400)
        
        # Create some walls around base
        for x in range(208, 272, 16):
            BrickWall(self.game, x, 416, self.walls)
        
        BrickWall(self.game, 208, 432, self.walls)
        BrickWall(self.game, 208, 448, self.walls)
        BrickWall(self.game, 272, 432, self.walls)
        BrickWall(self.game, 272, 448, self.walls)
        
        # Create some random walls
        for _ in range(30):
            x = random.randint(0, 31) * TILE_SIZE
            y = random.randint(0, 25) * TILE_SIZE
            if random.random() < 0.7:
                BrickWall(self.game, x, y, self.walls)
            else:
                SteelWall(self.game, x, y, self.walls)
        
        # Create some water and bushes
        for _ in range(10):
            x = random.randint(0, 31) * TILE_SIZE
            y = random.randint(0, 25) * TILE_SIZE
            Water(self.game, x, y, self.water_tiles)
            
            x = random.randint(0, 31) * TILE_SIZE
            y = random.randint(0, 25) * TILE_SIZE
            Bush(self.game, x, y, self.bushes)
        
        # Set enemy spawn points
        self.enemy_spawn_points = [
            (0, 0), (240, 0), (480, 0)
        ]
        
        # Set enemy data
        self.max_enemies = 10
        self.enemy_types = [1, 1, 1, 2, 2, 3]
    
    def handle_event(self, event):
        """Handle input events for level objects"""
        if self.player:
            self.player.handle_event(event)
    
    def update(self):
        """Update level state and game objects"""
        # Update player
        if self.player:
            self.player.update()
        
        # Update enemy tanks
        self.enemy_tanks.update()
        
        # Update bullets
        self.bullets.update()
        
        # Update water animations
        self.water_tiles.update()
        
        # Update powerups
        self.powerups.update()
        
        # Update effects
        self.effects.update()
        
        # Check bullet collisions
        self._handle_bullet_collisions()
        
        # Check powerup collisions
        self._handle_powerup_collisions()
        
        # Spawn enemies
        self._spawn_enemies()
    
    def draw(self, screen):
        """Draw all level objects"""
        # Draw water
        self.water_tiles.draw(screen)
        
        # Draw base
        if self.base:
            screen.blit(self.base.image, self.base.rect)
        
        # Draw walls
        self.walls.draw(screen)
        
        # Draw powerups
        self.powerups.draw(screen)
        
        # Draw player
        if self.player:
            screen.blit(self.player.image, self.player.rect)
        
        # Draw enemy tanks
        self.enemy_tanks.draw(screen)
        
        # Draw bullets
        self.bullets.draw(screen)
        
        # Draw bushes on top (for cover)
        self.bushes.draw(screen)
        
        # Draw effects
        self.effects.draw(screen)
    
    def _handle_bullet_collisions(self):
        """Handle collisions between bullets and other objects"""
        for bullet in list(self.bullets):
            # Check collision with walls
            wall_hit = pygame.sprite.spritecollideany(bullet, self.walls)
            if wall_hit:
                if hasattr(wall_hit, 'damage'):
                    destroyed = wall_hit.damage()
                    if destroyed:
                        # Spawn powerup with small chance
                        if random.random() < POWERUP_SPAWN_CHANCE:
                            self._spawn_powerup(wall_hit.rect.x, wall_hit.rect.y)
                
                Explosion(self.game, bullet.rect.centerx, bullet.rect.centery, 0.5, self.effects)
                bullet.kill()
                continue
            
            # Check collision with base
            if self.base and bullet.rect.colliderect(self.base.rect):
                self.base.destroy()
                Explosion(self.game, bullet.rect.centerx, bullet.rect.centery, 0.5, self.effects)
                bullet.kill()
                continue
            
            # Check collision with player bullets
            for other_bullet in self.bullets:
                if bullet != other_bullet and bullet.rect.colliderect(other_bullet.rect):
                    Explosion(self.game, bullet.rect.centerx, bullet.rect.centery, 0.5, self.effects)
                    bullet.kill()
                    other_bullet.kill()
                    break
            
            # Check collision with enemy tanks
            if bullet in self.bullets and bullet.owner == self.player:
                enemy_hit = pygame.sprite.spritecollideany(bullet, self.enemy_tanks)
                if enemy_hit:
                    if enemy_hit.hit():
                        self.enemies_destroyed += 1
                    
                    Explosion(self.game, bullet.rect.centerx, bullet.rect.centery, 0.5, self.effects)
                    bullet.kill()
                    continue
            
            # Check collision with player tank
            if bullet in self.bullets and bullet.owner != self.player and self.player:
                if bullet.rect.colliderect(self.player.rect):
                    if self.player.hit():
                        Explosion(self.game, bullet.rect.centerx, bullet.rect.centery, 0.5, self.effects)
                    bullet.kill()
                    continue
    
    def _handle_powerup_collisions(self):
        """Handle collisions between player and powerups"""
        if not self.player:
            return
        
        powerup_hit = pygame.sprite.spritecollideany(self.player, self.powerups)
        if powerup_hit:
            self.player.add_powerup(powerup_hit.type)
            powerup_hit.kill()
    
    def _spawn_enemies(self):
        """Spawn enemy tanks"""
        if self.enemies_spawned >= self.max_enemies:
            return
        
        if len(self.enemy_tanks) < 4:  # Maximum 4 enemy tanks at a time
            self.spawn_timer += 1
            if self.spawn_timer >= 180:  # Spawn every 3 seconds (180 frames at 60 FPS)
                self.spawn_timer = 0
                
                if len(self.enemy_spawn_points) > 0:
                    # Choose random spawn point
                    spawn_point = random.choice(self.enemy_spawn_points)
                    
                    # Choose random enemy type
                    enemy_type = random.choice(self.enemy_types)
                    
                    # Create enemy tank
                    EnemyTank(self.game, spawn_point[0], spawn_point[1], enemy_type, self.enemy_tanks)
                    
                    self.enemies_spawned += 1
    
    def _spawn_powerup(self, x, y):
        """Spawn a random powerup"""
        powerup_type = random.choice(["shield", "freeze", "life"])
        PowerUp(self.game, x, y, powerup_type, self.powerups)
    
    def reset_player(self):
        """Reset player position"""
        # Find player spawn point
        spawn_x, spawn_y = 240, 400  # Default position
        
        self.player.respawn(spawn_x, spawn_y)
    
    def is_completed(self):
        """Check if level is completed"""
        return self.enemies_destroyed >= self.max_enemies and len(self.enemy_tanks) == 0
    
    def is_game_over(self):
        """Check if game is over (base destroyed or player out of lives)"""
        return (self.base and self.base.destroyed) or self.game.lives <= 0
    
    def freeze_enemies(self):
        """Freeze all enemy tanks"""
        for enemy in self.enemy_tanks:
            enemy.freeze(FREEZE_DURATION)
