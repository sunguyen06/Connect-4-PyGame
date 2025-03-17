import pygame
import random
from board import Board
from ui import UI
from config import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.ui = UI(screen)
        self.reset_game()
        
        # Load sounds
        self.button_sound = pygame.mixer.Sound(BUTTON_SOUND)
        self.piece_sound = pygame.mixer.Sound(PIECE_SOUND)
        self.error_sound = pygame.mixer.Sound(ERROR_SOUND)
        
        # Set volumes
        self.button_sound.set_volume(VOLUME)
        self.piece_sound.set_volume(VOLUME)
        self.error_sound.set_volume(VOLUME)
        
    def reset_game(self):
        """Reset the game state."""
        self.board.reset()
        self.current_player = random.randint(1, 2)
        self.game_over = False
        self.turns = 0
        self.winning_pieces = []
        
    def handle_click(self, pos):
        """Handle mouse click events."""
        if self.ui.in_menu:
            action = self.ui.handle_menu_click(pos)
            if action:
                self.button_sound.play()
                if action == "exit":
                    return True
                elif action == "play":
                    self.reset_game()
            return False
            
        if self.ui.in_instructions:
            if self.ui.handle_instructions_click(pos):
                self.button_sound.play()
            return False
            
        if self.game_over:
            # Handle game over screen clicks
            if self.ui.play_again_rect.collidepoint(pos):
                self.button_sound.play()
                self.reset_game()
            elif self.ui.quit_rect.collidepoint(pos):
                self.button_sound.play()
                self.ui.in_menu = True
        else:
            # Handle game board clicks
            col = self.get_column(pos[0])
            if col is not None:
                if self.board.is_valid_move(col):
                    row = self.board.get_next_open_row(col)
                    self.piece_sound.play()
                    
                    # Animate piece drop
                    self.ui.animate_piece_drop(self.current_player, col, row)
                    
                    # Place the piece after animation
                    self.board.drop_piece(row, col, self.current_player)
                    
                    # Check for win
                    won, winning_pieces = self.board.check_win(self.current_player)
                    if won:
                        self.winning_pieces = winning_pieces
                        self.game_over = True
                    elif self.board.is_full():
                        self.game_over = True
                        self.current_player = 3  # Draw
                    else:
                        self.current_player = 3 - self.current_player  # Switch players (1->2 or 2->1)
                        self.turns += 1
                else:
                    self.error_sound.play()
        return False
        
    def get_column(self, x):
        """Get the column number based on x coordinate."""
        for i, pos_x in enumerate(PIECE_X):
            if abs(x - pos_x) < PIECE_SIZE/2:
                return i
        return None
        
    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.handle_click(event.pos):
                        running = False
                        
                if event.type == pygame.MOUSEMOTION and not (self.ui.in_menu or self.ui.in_instructions):
                    self.ui.update_hover_piece(event.pos, self.current_player, self.game_over)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.ui.in_instructions:
                            self.ui.in_instructions = False
                            self.button_sound.play()
                        elif not self.ui.in_menu:
                            self.ui.in_menu = True
                    
            # Draw everything
            self.ui.draw(self.board, self.current_player, self.game_over, self.winning_pieces)
            pygame.display.flip() 