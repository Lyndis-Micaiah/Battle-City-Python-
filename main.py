#!/usr/bin/env python3
# Battle City Game - Main File
# Main entry point for the Battle City game recreation

import pygame
import sys
import os
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

def main():
    """Main function to start the game"""
    # Set environment variable for headless/Replit environment
    os.environ['SDL_VIDEODRIVER'] = 'x11'
    
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()  # For sound
    
    try:
        # Set up the display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        # Fallback for headless environments
        print("Warning: Unable to set video mode. Using fallback surface.")
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.display.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    print(f"Game initialized with screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    while True:
        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Pass events to game object
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Control the game speed
        clock.tick(FPS)

if __name__ == "__main__":
    main()
