import pygame
import sys
from game import Game
from config import WIDTH, HEIGHT

def main():
    pygame.init()
    pygame.mixer.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")
    
    # Create and run the game
    game = Game(screen)
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 