import numpy as np
from config import ROWS, COLUMNS

class Board:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the board to its initial state."""
        self.grid = np.zeros((ROWS, COLUMNS))
        
    def is_valid_move(self, col):
        """Check if a move is valid in the given column."""
        return self.grid[0][col] == 0
        
    def get_next_open_row(self, col):
        """Get the next available row in the given column."""
        for row in range(ROWS-1, -1, -1):
            if self.grid[row][col] == 0:
                return row
        return None
        
    def drop_piece(self, row, col, player):
        """Place a piece on the board."""
        self.grid[row][col] = player
        
    def check_win(self, player):
        """Check if the given player has won."""
        # Check horizontal
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if (self.grid[row][col] == player and
                    self.grid[row][col+1] == player and
                    self.grid[row][col+2] == player and
                    self.grid[row][col+3] == player):
                    return True, [(row, col+i) for i in range(4)]

        # Check vertical
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if (self.grid[row][col] == player and
                    self.grid[row+1][col] == player and
                    self.grid[row+2][col] == player and
                    self.grid[row+3][col] == player):
                    return True, [(row+i, col) for i in range(4)]

        # Check diagonal (positive slope)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if (self.grid[row][col] == player and
                    self.grid[row-1][col+1] == player and
                    self.grid[row-2][col+2] == player and
                    self.grid[row-3][col+3] == player):
                    return True, [(row-i, col+i) for i in range(4)]

        # Check diagonal (negative slope)
        for row in range(3, ROWS):
            for col in range(3, COLUMNS):
                if (self.grid[row][col] == player and
                    self.grid[row-1][col-1] == player and
                    self.grid[row-2][col-2] == player and
                    self.grid[row-3][col-3] == player):
                    return True, [(row-i, col-i) for i in range(4)]
                    
        return False, []
        
    def is_full(self):
        """Check if the board is full."""
        return not np.any(self.grid == 0)
        
    def get_valid_moves(self):
        """Return a list of valid column moves."""
        return [col for col in range(COLUMNS) if self.is_valid_move(col)] 