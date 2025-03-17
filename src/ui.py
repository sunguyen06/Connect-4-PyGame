import pygame
import time
from config import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.game_over = False
        self.in_menu = True
        self.in_instructions = False
        
        # Load images
        self.board_image = pygame.image.load(BOARD_IMAGE)
        self.blur_image = pygame.transform.scale(pygame.image.load(BLUR_IMAGE), (WIDTH, HEIGHT))
        self.instructions_image = pygame.image.load(INSTRUCTIONS_IMAGE)
        
        # Load fonts
        self.large_font = pygame.font.Font(FONT_PATH, 120)
        self.medium_font = pygame.font.Font(FONT_PATH, 100)
        
        # Create rectangles for buttons
        self.play_again_rect = pygame.Rect((WIDTH - 774)/2, 300, 774, 120)
        self.quit_rect = pygame.Rect((WIDTH - 279)/2, 450, 279, 120)
        
        # Menu buttons
        self.play_rect = pygame.Rect((WIDTH - 282)/2, 180, 282, 120)
        self.instructions_rect = pygame.Rect((WIDTH - 840)/2, 330, 840, 120)
        self.exit_rect = pygame.Rect((WIDTH - 280)/2, 480, 280, 120)
        
        # Back button for instructions
        self.back_rect = pygame.Rect(0, 0, 80, 80)
        
    def draw_board_background(self):
        """Draw the background color."""
        self.screen.fill(GRAY)
        
    def draw_pieces(self, board):
        """Draw all the pieces on the board."""
        for row in range(ROWS):
            for col in range(COLUMNS):
                if board.grid[row][col] == 1:
                    pygame.draw.circle(self.screen, RED, (PIECE_X[col], PIECE_Y[row]), PIECE_SIZE//2)
                elif board.grid[row][col] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (PIECE_X[col], PIECE_Y[row]), PIECE_SIZE//2)
                    
    def draw_board_overlay(self):
        """Draw the board overlay on top of the pieces."""
        self.screen.blit(self.board_image, (0, 0))
                    
    def draw_hover_piece(self, x, player):
        """Draw the hovering piece at the top of the screen."""
        if not self.game_over:
            color = RED if player == 1 else YELLOW
            for i, pos_x in enumerate(PIECE_X):
                if abs(x - pos_x) < PIECE_SIZE/2:
                    pygame.draw.circle(self.screen, color, (pos_x, 50), PIECE_SIZE//2)
                    break
                    
    def draw_winning_pieces(self, winning_pieces, player):
        """Highlight the winning pieces."""
        color = RED if player == 1 else YELLOW
        for row, col in winning_pieces:
            # Draw a larger circle behind the piece for highlighting
            pygame.draw.circle(self.screen, WHITE, (PIECE_X[col], PIECE_Y[row]), PIECE_SIZE//2 + 5)
            pygame.draw.circle(self.screen, color, (PIECE_X[col], PIECE_Y[row]), PIECE_SIZE//2)
            
    def draw_game_over(self, player):
        """Draw the game over screen."""
        self.screen.blit(self.blur_image, (0, 0))
        
        # Draw win/draw message
        if player == 3:
            text = "It was a draw!"
        else:
            text = "Red Wins!" if player == 1 else "Yellow Wins!"
        text_surface = self.medium_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH/2, 100))
        self.screen.blit(text_surface, text_rect)
        
        # Draw buttons
        play_again_text = self.large_font.render("PLAY AGAIN?", True, YELLOW)
        quit_text = self.large_font.render("QUIT", True, RED)
        
        play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 360))
        quit_rect = quit_text.get_rect(center=(WIDTH/2, 510))
        
        self.screen.blit(play_again_text, play_again_rect)
        self.screen.blit(quit_text, quit_rect)
        
    def animate_piece_drop(self, player, col, final_row):
        """Animate a piece dropping to its position."""
        color = RED if player == 1 else YELLOW
        start_y = 50
        end_y = PIECE_Y[final_row]
        
        while start_y < end_y:
            # Draw background and existing pieces
            self.draw_board_background()
            self.draw_pieces(self.board)
            
            # Draw the falling piece
            start_y += ANIMATION_SPEED
            current_y = min(start_y, end_y)
            pygame.draw.circle(self.screen, color, (PIECE_X[col], current_y), PIECE_SIZE//2)
            
            # Draw the board overlay
            self.draw_board_overlay()
            pygame.display.flip()
            
            # Check for skip animation
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
                    
            time.sleep(0.01)
            
    def update_hover_piece(self, pos, current_player, game_over):
        """Update the position of the hovering piece."""
        self.game_over = game_over
        if not game_over:
            # Clear previous hover piece
            pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, PIECE_SIZE))
            self.draw_hover_piece(pos[0], current_player)
            
    def draw_menu(self):
        """Draw the main menu screen."""
        self.screen.fill(DARK_BLUE)
        
        # Draw title
        title_text = self.large_font.render("CONNECT 4", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH/2, 90))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        play_text = self.large_font.render("PLAY", True, YELLOW)
        instructions_text = self.large_font.render("INSTRUCTIONS", True, ORANGE)
        exit_text = self.large_font.render("EXIT", True, RED)
        
        play_rect = play_text.get_rect(center=(WIDTH/2, 240))
        instructions_rect = instructions_text.get_rect(center=(WIDTH/2, 390))
        exit_rect = exit_text.get_rect(center=(WIDTH/2, 540))
        
        self.screen.blit(play_text, play_rect)
        self.screen.blit(instructions_text, instructions_rect)
        self.screen.blit(exit_text, exit_rect)
        
    def draw_instructions(self):
        """Draw the instructions screen."""
        self.screen.blit(self.instructions_image, (0, 0))
        
        # Draw back button
        pygame.draw.rect(self.screen, DARK_BLUE, self.back_rect)
        back_text = self.medium_font.render("<", True, WHITE)
        back_rect = back_text.get_rect(center=(40, 40))
        self.screen.blit(back_text, back_rect)
        
    def handle_instructions_click(self, pos):
        """Handle clicks on the instructions screen."""
        if self.back_rect.collidepoint(pos):
            self.in_instructions = False
            return True
        return False

    def handle_menu_click(self, pos):
        """Handle clicks on the menu screen."""
        if self.play_rect.collidepoint(pos):
            self.in_menu = False
            return "play"
        elif self.instructions_rect.collidepoint(pos):
            self.in_instructions = True
            return "instructions"
        elif self.exit_rect.collidepoint(pos):
            return "exit"
        return None

    def draw(self, board, current_player, game_over, winning_pieces):
        """Main draw method that handles all rendering."""
        if self.in_menu:
            self.draw_menu()
            return
            
        if self.in_instructions:
            self.draw_instructions()
            return
            
        self.board = board  # Store reference to board for animations
        
        # Draw in correct layer order
        self.draw_board_background()
        self.draw_pieces(board)
        
        if winning_pieces:
            self.draw_winning_pieces(winning_pieces, current_player)
            
        self.draw_board_overlay()
        
        if not game_over:
            # Get current mouse position and draw hover piece
            pos = pygame.mouse.get_pos()
            self.draw_hover_piece(pos[0], current_player)
            
        if game_over:
            self.draw_game_over(current_player) 