#!/usr/bin/env python3
"""
Battle City NES Clone
Main entry point for the game
"""
import pygame
import sys
from game import Game

def main():
    """
    Main function to initialize and run the game
    """
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Start the game
    game = Game()
    game.run()
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
