import numpy as np

class AgentPlayer:
    def __init__(self, flag=False, strategy='only_offense'):
        self.strategy = strategy
        self.first = flag

    def move_chess(self, chess_map, is_pos, player=0):
        if self.first:
            self.first = False
            return [8, 8]
        if self.strategy == 'only_offense' or 'oo':
            return self.only_offense(chess_map, is_pos, player)
        if self.strategy == 'only_offense' or 'oo':
            return self.

    def only_offense(self, chess_map, is_pos, player):
        eval_map = np.zeros((15, 15))
        # try_map = chess_map[player, :, :] - chess_map[1 - player, :, :]
        direction = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for pos in is_pos:
            score = 0
            for move in direction:
                n_pos = pos.copy()
                for i in range(4):
                    n_pos += move
                    if (-1 in n_pos) or (15 in n_pos):
                        break
                    if chess_map[1-player, n_pos[0], n_pos[1]] == 1 or chess_map[player, n_pos[0], n_pos[1]] == 0:
                        break
                    if chess_map[player, n_pos[0], n_pos[1]] == 1:
                        score += 5 * 10 ** i
                    score += 0
            eval_map[pos[0], pos[1]] = score
        p = np.argmax(eval_map)
        # print(np.max(eval_map))
        p = np.unravel_index(p, chess_map[0, :, :].shape)
        return p

    def search_tree(self, board, is_pos, player):
        best_score = -np.inf
        for pos in is_pos:
            new_pos = is_pos[:is_pos.index(pos)] + is_pos[is_pos.index(pos)+1:]
            new_board = board
            new_board[player, pos[0], pos[1]] = 1
            score = self.search_tree()

        return
    def minmax_search(self, chess_map, is_pos, player):
        board = chess_map.copy()
        p = self.search_tree(board, is_pos, player)
        return p


