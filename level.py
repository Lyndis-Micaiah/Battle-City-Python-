"""
Level module for Battle City game
"""
import json
import os
import pygame
from constants import *

class Level:
    """
    Level class that handles level loading and rendering
    """
    def __init__(self, level_number, game):
        """
        Initialize a level
        
        Args:
            level_number (int): Level number to load
            game (Game): Game instance
        """
        self.game = game
        self.level_number = level_number
        self.base_destroyed = False
        
        # Load level data
        self.load_level(level_number)
    
    def load_level(self, level_number):
        """
        Load level data from JSON file
        
        Args:
            level_number (int): Level number to load
        """
        # Try to load from file
        try:
            with open(f"levels/level{level_number}.json", 'r') as f:
                level_data = json.load(f)
            
            self.width = level_data.get("width", 26)
            self.height = level_data.get("height", 26)
            self.grid = level_data.get("grid", [])
            self.player_start = level_data.get("player_start", [SCREEN_WIDTH // 2, SCREEN_HEIGHT - TILE_SIZE])
            self.enemy_spawns = level_data.get("enemy_spawns", [[0, 0], [SCREEN_WIDTH - TILE_SIZE, 0], [SCREEN_WIDTH // 2, 0]])
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, generate a default level
            self.generate_default_level(level_number)
    
    def generate_default_level(self, level_number):
        """
        Generate a default level layout
        
        Args:
            level_number (int): Level number to generate
        """
        # Set default dimensions
        self.width = 20
        self.height = 15
        
        # Create empty grid
        self.grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        
        # Set player start position
        self.player_start = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - TILE_SIZE]
        
        # Set enemy spawn positions
        self.enemy_spawns = [
            [0, 0],
            [SCREEN_WIDTH - TILE_SIZE, 0],
            [SCREEN_WIDTH // 2, 0]
        ]
        
        # Add base at the bottom center
        base_x = self.width // 2
        base_y = self.height - 2
        self.grid[base_y][base_x] = BASE
        
        # Add walls around the base
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            wall_x = base_x + dx
            wall_y = base_y + dy
            
            if 0 <= wall_x < self.width and 0 <= wall_y < self.height:
                self.grid[wall_y][wall_x] = BRICK
        
        # Add more terrain based on level number
        if level_number == 1:
            self._add_level1_terrain()
        elif level_number == 2:
            self._add_level2_terrain()
        elif level_number == 3:
            self._add_level3_terrain()
    
    def _add_level1_terrain(self):
        """
        Add terrain for level 1
        """
        # Add some brick walls
        for i in range(3, self.width - 3, 2):
            for j in range(3, self.height - 5, 2):
                self.grid[j][i] = BRICK
        
        # Add some steel walls
        for i in range(5, self.width - 5, 6):
            self.grid[5][i] = STEEL
        
        # Add water
        for i in range(2, 5):
            for j in range(9, 12):
                self.grid[j][i] = WATER
        
        # Add grass
        for i in range(self.width - 5, self.width - 2):
            for j in range(9, 12):
                self.grid[j][i] = GRASS
    
    def _add_level2_terrain(self):
        """
        Add terrain for level 2
        """
        # Create a more complex layout with all terrain types
        
        # Add brick walls pattern
        for i in range(2, self.width - 2, 3):
            for j in range(2, self.height - 5, 3):
                self.grid[j][i] = BRICK
                
                if j + 1 < self.height:
                    self.grid[j+1][i] = BRICK
                    
                if i + 1 < self.width:
                    self.grid[j][i+1] = BRICK
        
        # Add steel walls at strategic positions
        for i in range(4, self.width - 4, 8):
            self.grid[7][i] = STEEL
            self.grid[7][i+1] = STEEL
        
        # Add water area
        for i in range(10, 15):
            for j in range(3, 6):
                self.grid[j][i] = WATER
        
        # Add some grass for cover
        for i in range(5, 10):
            for j in range(8, 10):
                self.grid[j][i] = GRASS
        
        # Add some ice for slippery terrain
        for i in range(15, 18):
            for j in range(8, 11):
                self.grid[j][i] = ICE
    
    def _add_level3_terrain(self):
        """
        Add terrain for level 3
        """
        # Create a challenging layout
        
        # Add "maze" of brick walls
        for i in range(1, self.width - 1, 2):
            for j in range(1, self.height - 4, 2):
                self.grid[j][i] = BRICK
        
        # Add steel wall barrier
        for i in range(3, self.width - 3):
            self.grid[self.height // 2][i] = STEEL
        
        # Create openings in the barrier
        self.grid[self.height // 2][self.width // 4] = EMPTY
        self.grid[self.height // 2][self.width // 4 * 3] = EMPTY
        
        # Add water moat
        for i in range(0, self.width):
            if i < self.width // 3 or i > self.width * 2 // 3:
                self.grid[self.height - 5][i] = WATER
        
        # Add grass for cover near base
        for dx in range(-2, 3):
            for dy in range(-2, 0):
                x = self.width // 2 + dx
                y = self.height - 2 + dy
                if 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == EMPTY:
                    self.grid[y][x] = GRASS
        
        # Add ice at corners
        for i in range(0, 3):
            for j in range(0, 3):
                self.grid[j][i] = ICE
                self.grid[j][self.width - 1 - i] = ICE
    
    def get_tile(self, x, y):
        """
        Get the tile type at the specified grid position
        
        Args:
            x (int): Grid x-coordinate
            y (int): Grid y-coordinate
        
        Returns:
            int: Tile type
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return EMPTY
    
    def set_tile(self, x, y, tile_type):
        """
        Set the tile type at the specified grid position
        
        Args:
            x (int): Grid x-coordinate
            y (int): Grid y-coordinate
            tile_type (int): Tile type to set
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_type
    
    def get_player_start_position(self):
        """
        Get the player tank starting position
        
        Returns:
            list: [x, y] position
        """
        return self.player_start
    
    def get_enemy_spawn_positions(self):
        """
        Get the enemy tank spawn positions
        
        Returns:
            list: List of [x, y] positions
        """
        return self.enemy_spawns
    
    def get_base_position(self):
        """
        Get the position of the base
        
        Returns:
            tuple: (x, y) position or None if not found
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == BASE:
                    return (x * TILE_SIZE, y * TILE_SIZE)
        
        return None
    
    def upgrade_base_walls(self):
        """
        Upgrade walls around the base to steel (for shovel power-up)
        """
        base_pos = self.get_base_position()
        if not base_pos:
            return
        
        base_x = base_pos[0] // TILE_SIZE
        base_y = base_pos[1] // TILE_SIZE
        
        # Upgrade walls around the base
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]:
            wall_x = base_x + dx
            wall_y = base_y + dy
            
            if 0 <= wall_x < self.width and 0 <= wall_y < self.height:
                # Only upgrade if it's a wall already (brick or steel)
                if self.grid[wall_y][wall_x] == BRICK:
                    self.grid[wall_y][wall_x] = STEEL
    
    def draw(self, surface):
        """
        Draw the level
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Get tile sprites
        tile_sprites = self.game.sprites.tiles
        
        # Draw tiles
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                
                if tile != EMPTY:
                    # Convert grid coordinates to pixel coordinates
                    pixel_x = x * TILE_SIZE
                    pixel_y = y * TILE_SIZE
                    
                    # Draw the tile sprite
                    surface.blit(tile_sprites[tile], (pixel_x, pixel_y))
