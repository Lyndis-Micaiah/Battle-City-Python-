"""
Utility functions for Battle City game
"""
import pygame
import math
import random
from constants import *

def distance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points
    
    Args:
        x1 (float): X coordinate of first point
        y1 (float): Y coordinate of first point
        x2 (float): X coordinate of second point
        y2 (float): Y coordinate of second point
    
    Returns:
        float: Distance between the points
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def direction_to_target(x1, y1, x2, y2):
    """
    Calculate the direction to move from (x1, y1) to (x2, y2)
    
    Args:
        x1 (float): X coordinate of source point
        y1 (float): Y coordinate of source point
        x2 (float): X coordinate of target point
        y2 (float): Y coordinate of target point
    
    Returns:
        int: Direction constant (UP, RIGHT, DOWN, LEFT)
    """
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) > abs(dy):
        # Horizontal movement is larger
        if dx > 0:
            return RIGHT
        else:
            return LEFT
    else:
        # Vertical movement is larger
        if dy > 0:
            return DOWN
        else:
            return UP

def grid_to_pixel(grid_x, grid_y):
    """
    Convert grid coordinates to pixel coordinates
    
    Args:
        grid_x (int): Grid X coordinate
        grid_y (int): Grid Y coordinate
    
    Returns:
        tuple: (pixel_x, pixel_y)
    """
    return (grid_x * TILE_SIZE, grid_y * TILE_SIZE)

def pixel_to_grid(pixel_x, pixel_y):
    """
    Convert pixel coordinates to grid coordinates
    
    Args:
        pixel_x (int): Pixel X coordinate
        pixel_y (int): Pixel Y coordinate
    
    Returns:
        tuple: (grid_x, grid_y)
    """
    return (pixel_x // TILE_SIZE, pixel_y // TILE_SIZE)
