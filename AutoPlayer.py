import numpy as np

class AutoPlayer:
    def __init__(self):
        self.map = None

    def game_tree(self, board, player, depth):
        if depth == 0:
            return self.evaluate(board)

        if player == 1:
            best_value = -np.inf
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    if board[i, j] == 0:
                        new_board = np.copy(board)
                        new_board[i, j] = player
                        value = self.game_tree(new_board, 2, depth - 1)
                        best_value = max(best_value, value)
        else:
            best_value = np.inf
            for i in range(board.shape[0]):
                for j in range(board.shape[1]):
                    if board[i, j] == 0:
                        new_board = np.copy(board)
                        new_board[i, j] = player
                        value = self.game_tree(new_board, 1, depth - 1)
                        best_value = min(best_value, value)

        return best_value

    def evaluate(self, board):
        return np.sum(board == 1) - np.sum(board == 2)

    def get_map(self, board):
        self.map = board
        best_value = -np.inf
        best_i = -1
        best_j = -1
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i, j] == 0:
                    new_board = np.copy(self.map)
                    new_board[i, j] = 2
                    value = self.game_tree(new_board, 2, 2)
                    if value > best_value:
                        best_value = value
                        best_i = i
                        best_j = j
        self.map[best_i, best_j] = 2
        return self.map, best_i, best_j
