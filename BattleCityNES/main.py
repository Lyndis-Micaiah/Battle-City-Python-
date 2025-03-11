#!/usr/bin/env python3
# Battle City Game - Main File
# Main entry point for the Battle City game recreation

import pygame
import sys
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

def main():
    """Main function to start the game"""
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()  # For sound
    
    # Flags for display mode
    fullscreen = False
    flags = pygame.SCALED  # Add SCALED flag for better fullscreen scaling
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle Alt+Enter to toggle fullscreen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and (pygame.key.get_mods() & pygame.KMOD_ALT):
                    # Toggle fullscreen
                    fullscreen = not fullscreen
                    
                    if fullscreen:
                        # Get current display info
                        display_info = pygame.display.Info()
                        # Switch to fullscreen mode (scaled)
                        screen = pygame.display.set_mode(
                            (display_info.current_w, display_info.current_h),
                            pygame.FULLSCREEN | pygame.SCALED
                        )
                        print(f"Switched to fullscreen mode: {display_info.current_w}x{display_info.current_h}")
                    else:
                        # Switch back to windowed mode
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
                        print(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                    
                    # Update game screen reference
                    game.screen = screen
            
            # Pass other events to game object
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
