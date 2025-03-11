# Battle City Game - Utilities Module
# Utility functions for the game

import pygame
import os
import xml.etree.ElementTree as ET
from io import BytesIO

def load_svg(filename, width, height):
    """
    Load an SVG file and convert it to a Pygame surface
    
    This is a simplified function that creates a colored rectangle
    instead of actually loading SVG files since we can't load external
    images. In a real implementation, this would use proper SVG loading.
    """
    # Create a surface with the specified dimensions
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Parse the filename to determine what to draw
    if "tank_base" in filename:
        pygame.draw.rect(surface, (0, 200, 0), (0, 0, width, height))
        pygame.draw.rect(surface, (0, 150, 0), (width // 4, 0, width // 2, height))
    elif "tank_cannon" in filename:
        pygame.draw.rect(surface, (0, 100, 0), (width // 2 - 2, 0, 4, height // 2))
    elif "bullet" in filename:
        pygame.draw.circle(surface, (255, 255, 0), (width // 2, height // 2), width // 4)
    elif "brick_wall" in filename:
        # Draw brick pattern
        brick_color = (180, 100, 30)
        for y in range(0, height, height // 4):
            offset = 0 if y % (height // 2) == 0 else width // 4
            for x in range(offset, width, width // 2):
                pygame.draw.rect(surface, brick_color, (x, y, width // 4, height // 4))
    elif "steel_wall" in filename:
        # Draw steel wall
        pygame.draw.rect(surface, (150, 150, 150), (0, 0, width, height))
        pygame.draw.rect(surface, (200, 200, 200), (2, 2, width - 4, height - 4))
    elif "water" in filename:
        # Draw water
        water_color = (0, 0, 200, 200)
        surface.fill(water_color)
        # Add some wave lines
        for y in range(0, height, height // 4):
            pygame.draw.line(surface, (100, 100, 255, 150), (0, y), (width, y), 2)
    elif "base" in filename:
        # Draw base (flag)
        pygame.draw.rect(surface, (200, 200, 200), (0, 0, width, height))
        pygame.draw.rect(surface, (150, 0, 0), (width // 4, height // 4, width // 2, height // 2))
        pygame.draw.line(surface, (255, 255, 255), (width // 2, height // 4), 
                        (width // 2, height * 3 // 4), 2)
    elif "bush" in filename:
        # Draw bush (green circle)
        bush_color = (0, 150, 0, 180)
        pygame.draw.circle(surface, bush_color, (width // 2, height // 2), width // 2)
        pygame.draw.circle(surface, (0, 100, 0, 180), (width // 3, height // 3), width // 4)
        pygame.draw.circle(surface, (0, 100, 0, 180), (width * 2 // 3, height // 3), width // 4)
    elif "powerup_shield" in filename:
        # Draw shield powerup
        pygame.draw.rect(surface, (200, 200, 0), (0, 0, width, height))
        pygame.draw.circle(surface, (0, 0, 0, 0), (width // 2, height // 2), width // 3, 3)
    elif "powerup_freeze" in filename:
        # Draw freeze powerup
        pygame.draw.rect(surface, (0, 200, 200), (0, 0, width, height))
        pygame.draw.line(surface, (255, 255, 255), (width // 4, height // 2), 
                        (width * 3 // 4, height // 2), 2)
        pygame.draw.line(surface, (255, 255, 255), (width // 2, height // 4), 
                        (width // 2, height * 3 // 4), 2)
    elif "powerup_life" in filename:
        # Draw life powerup
        pygame.draw.rect(surface, (200, 0, 0), (0, 0, width, height))
        pygame.draw.rect(surface, (255, 255, 255), (width // 4, height // 3, width // 2, height // 3))
        pygame.draw.rect(surface, (255, 255, 255), (width // 3, height // 4, width // 3, height // 2))
    elif "explosion" in filename:
        # Draw explosion (orange/yellow circle)
        pygame.draw.circle(surface, (255, 200, 0), (width // 2, height // 2), width // 2)
        pygame.draw.circle(surface, (255, 100, 0), (width // 2, height // 2), width // 3)
        pygame.draw.circle(surface, (255, 255, 0), (width // 2, height // 2), width // 4)
    
    return surface
