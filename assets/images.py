# Battle City Game - Images Module
# This module would normally handle loading and processing images
# Since we're using SVG vectors instead, this is just a stub file

import pygame
from utils import load_svg

def get_image_surface(name, width, height):
    """Get a surface with the specified dimensions for the given image name
    
    Args:
        name: Name of the image (without file extension)
        width: Width of the surface
        height: Height of the surface
    
    Returns:
        pygame.Surface: The loaded and processed image
    """
    return load_svg(f"assets/{name}.svg", width, height)
