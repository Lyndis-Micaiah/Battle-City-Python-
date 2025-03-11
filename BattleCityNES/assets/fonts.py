# Battle City Game - Fonts Module
# This module would normally handle loading custom fonts
# Since we're using pygame's built-in fonts, this is just a stub file

import pygame

def get_font(size):
    """Get a font with the specified size
    
    Args:
        size: Font size in points
    
    Returns:
        pygame.font.Font: The loaded font
    """
    return pygame.font.Font(None, size)
