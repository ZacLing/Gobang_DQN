import numpy as np

class AgentPlayer:
    def __init__(self):
        self.first = True

    def move_chess(self, chess_map, is_pos, player=0, strategy='only_offense'):
        if self.first:
            self.first = False
            return [8, 8]
        if strategy == 'only_offense' or 'oo':
            return self.only_offense(chess_map, is_pos, player)

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
                    if chess_map[1-player, n_pos[0], n_pos[1]] == 1:
                        break
                    if chess_map[player, n_pos[0], n_pos[1]] == 1:
                        score += 50 ** i
                    score += 0
            eval_map[pos[0], pos[1]] = score
            p = np.argmax(eval_map)
            p = np.unravel_index(p, chess_map[0, :, :].shape)
            # print(eval_map)
        return p


