"""
Adversarial Search: Dominoes AI Agent
Algorithm: Minimax with Alpha-Beta Pruning

Description:
    Implements an AI agent for a Dominoes-style game where players place
    1x2 tiles on a grid. The agent uses the Minimax algorithm with Alpha-Beta
    pruning to determine the optimal move, maximizing its future options
    while minimizing the opponent's.
"""

import math
import copy

class DominoesGame:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0

    def get_board(self):
        return self.board

    def is_legal_move(self, row, col, vertical):
        """Checks if a move is within bounds and on empty tiles."""
        if row < 0 or col < 0: 
            return False
        
        # Check bounds and occupancy
        if vertical:
            if row + 1 >= self.rows or col >= self.cols:
                return False
            # Check if both tiles are empty (False means empty)
            return not (self.board[row][col] or self.board[row+1][col])
        else:
            if row >= self.rows or col + 1 >= self.cols:
                return False
            return not (self.board[row][col] or self.board[row][col+1])

    def legal_moves(self, vertical):
        """Generates a list of all valid coordinates for the current player."""
        return [(r, c) for r in range(self.rows) 
                for c in range(self.cols) 
                if self.is_legal_move(r, c, vertical)]

    def perform_move(self, row, col, vertical):
        """Updates the board state with a move."""
        self.board[row][col] = True
        if vertical:
            self.board[row+1][col] = True
        else:
            self.board[row][col+1] = True

    def game_over(self, vertical):
        """Returns True if the current player has no legal moves."""
        return not self.legal_moves(vertical)

    def copy_game(self):
        """Creates a deep copy of the game state for recursion."""
        return DominoesGame(copy.deepcopy(self.board))

    def utility(self, vertical):
        """
        Heuristic Evaluation Function:
        (My Moves) - (Opponent's Moves).
        """
        return len(self.legal_moves(vertical)) - len(self.legal_moves(not vertical))

    def max_value(self, vertical, alpha, beta, depth, limit, leaf_count):
        """Maximizing player (AI) logic."""
        if self.game_over(vertical) or depth == limit:
            return self.utility(vertical), None, leaf_count + 1
        
        v_best = -math.inf
        move_best = None
        
        for move in self.legal_moves(vertical):
            row, col = move
            new_game = self.copy_game()
            new_game.perform_move(row, col, vertical)
            
            # Recursively call min_value for the opponent
            v_curr, _, leaf_count = new_game.min_value(not vertical, alpha, beta, depth + 1, limit, leaf_count)
            
            if v_curr > v_best:
                v_best, move_best = v_curr, move
            
            # Alpha-Beta Pruning
            alpha = max(alpha, v_best)
            if v_best >= beta:
                return v_best, move_best, leaf_count
                
        return v_best, move_best, leaf_count

    def min_value(self, vertical, alpha, beta, depth, limit, leaf_count):
        """Minimizing player (Opponent) logic."""
        if self.game_over(vertical) or depth == limit:
            return self.utility(vertical), None, leaf_count + 1
        
        v_best = math.inf
        move_best = None
        
        for move in self.legal_moves(vertical):
            row, col = move
            new_game = self.copy_game()
            new_game.perform_move(row, col, vertical)
            
            # Recursively call max_value for the AI
            v_curr, _, leaf_count = new_game.max_value(not vertical, alpha, beta, depth + 1, limit, leaf_count)
            
            if v_curr < v_best:
                v_best, move_best = v_curr, move
            
            # Alpha-Beta Pruning
            beta = min(beta, v_best)
            if v_best <= alpha:
                return v_best, move_best, leaf_count
                
        return v_best, move_best, leaf_count

    def get_best_move(self, vertical, limit):
        """Root function to start the Minimax search."""
        value, move, visited = self.max_value(vertical, -math.inf, math.inf, 0, limit, 0)
        return move, value, visited

def create_dominoes_game(rows, cols):
    # Initialize empty board (False = Empty, True = Occupied)
    board = [[False for _ in range(cols)] for _ in range(rows)]
    return DominoesGame(board)

if __name__ == '__main__':
    print("=== Adversarial Search Demo: Dominoes ===")
    
    # Setup a 3x3 board
    game = create_dominoes_game(3, 3)
    
    # Simulate a previous move to make it interesting
    # Blocking the center
    game.perform_move(1, 1, False) 
    
    print("Current Board State (True=Occupied):")
    for row in game.get_board():
        print(row)
    
    print("\nThinking...")
    
    # AI plays Vertical (True) with a search depth limit of 4
    best_move, score, leaves = game.get_best_move(vertical=True, limit=4)
    
    print(f"AI selected move: {best_move}")
    print(f"Heuristic Score: {score}")
    print(f"Leaf nodes evaluated: {leaves}")
