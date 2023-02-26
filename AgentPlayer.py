# import numpy as np

class AgentPlayer:
    def __init__(self, flag=False, strategy='mms', ratio=1, depth=3):
        self.strategy = strategy
        self.first = flag
        self.ratio = ratio  # 进攻的系数   小于1 进攻型   大于1 防守型
        self.DEPTH = depth  # 搜索深度
        self.next_point = [0, 0]  # AI下一步最应该下的位置
        self.list_all = []
        self.list1 = []
        self.list2 = []
        self.list3 = []
        for i in range(15 + 1):
            for j in range(15 + 1):
                self.list_all.append((i, j))
        self.cut_count = 0
        self.search_count = 0
        self.shape_score = [(50, (0, 1, 1, 0, 0)),
                            (50, (0, 0, 1, 1, 0)),
                            (200, (1, 1, 0, 1, 0)),
                            (500, (0, 0, 1, 1, 1)),
                            (500, (1, 1, 1, 0, 0)),
                            (5000, (0, 1, 1, 1, 0)),
                            (5000, (0, 1, 0, 1, 1, 0)),
                            (5000, (0, 1, 1, 0, 1, 0)),
                            (5000, (1, 1, 1, 0, 1)),
                            (5000, (1, 1, 0, 1, 1)),
                            (5000, (1, 0, 1, 1, 1)),
                            (5000, (1, 1, 1, 1, 0)),
                            (5000, (0, 1, 1, 1, 1)),
                            (50000, (0, 1, 1, 1, 1, 0)),
                            (99999999, (1, 1, 1, 1, 1))]

    def move_chess(self, x_pos, y_pos):
        self.list2.append((x_pos, y_pos))
        self.list3.append((x_pos, y_pos))
        if self.first:
            self.first = False
            return [8, 8]
        if self.strategy == 'minmax_search' or 'mms':
            return self.minmax_search()

    def minmax_search(self, ):
        self.cut_count = 0
        self.search_count = 0
        self.negamax(True, self.DEPTH, -99999999, 99999999)
        self.list1.append((self.next_point[0], self.next_point[1]))
        self.list3.append((self.next_point[0], self.next_point[1]))
        return self.next_point[0], self.next_point[1]

    def negamax(self, is_ai, depth, alpha, beta):
        # 游戏是否结束 | | 探索的递归深度是否到边界
        if depth == 0:
            return self.evaluation(is_ai)

        blank_list = list(set(self.list_all).difference(set(self.list3)))
        self.order(blank_list)  # 搜索顺序排序  提高剪枝效率
        # 遍历每一个候选步
        for next_step in blank_list:

            self.search_count += 1

            # 如果要评估的位置没有相邻的子， 则不去评估  减少计算
            if not self.has_neightnor(next_step):
                continue

            if is_ai:
                self.list1.append(next_step)
            else:
                self.list2.append(next_step)
            self.list3.append(next_step)

            value = -self.negamax(not is_ai, depth - 1, -beta, -alpha)
            if is_ai:
                self.list1.remove(next_step)
            else:
                self.list2.remove(next_step)
            self.list3.remove(next_step)

            if value > alpha:

                # print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
                # print(self.list3)
                if depth == self.DEPTH:
                    self.next_point[0] = next_step[0]
                    self.next_point[1] = next_step[1]
                # alpha + beta剪枝点
                if value >= beta:
                    self.cut_count += 1
                    return beta
                alpha = value

        return alpha

    #  离最后落子的邻居位置最有可能是最优点
    def order(self, blank_list):
        last_pt = self.list3[-1]
        for _ in blank_list:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                        blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                        blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))

    def has_neightnor(self, pt):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (pt[0] + i, pt[1] + j) in self.list3:
                    return True
        return False

    # 评估函数
    def evaluation(self, is_ai):
        # total_score = 0

        if is_ai:
            my_list = self.list1
            enemy_list = self.list2
        else:
            my_list = self.list2
            enemy_list = self.list1

        # 算自己的得分
        score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
        my_score = 0
        for pt in my_list:
            m = pt[0]
            n = pt[1]
            my_score += self.cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
            my_score += self.cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
            my_score += self.cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
            my_score += self.cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

        #  算敌人的得分， 并减去
        score_all_arr_enemy = []
        enemy_score = 0
        for pt in enemy_list:
            m = pt[0]
            n = pt[1]
            enemy_score += self.cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
            enemy_score += self.cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
            enemy_score += self.cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
            enemy_score += self.cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

        total_score = my_score - enemy_score * self.ratio * 0.1

        return total_score

    # 每个方向上的分值计算
    def cal_score(self, m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
        add_score = 0  # 加分项
        # 在一个方向上， 只取最大的得分项
        max_score_shape = (0, None)

        # 如果此方向上，该点已经有得分形状，不重复计算
        for item in score_all_arr:
            for pt in item[1]:
                if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                    return 0

        # 在落子点 左右方向上循环查找得分形状
        for offset in range(-5, 1):
            # offset = -2
            pos = []
            for i in range(0, 6):
                if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                    pos.append(2)
                elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                    pos.append(1)
                else:
                    pos.append(0)
            tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

            for (score, shape) in self.shape_score:
                if tmp_shap5 == shape or tmp_shap6 == shape:
                    if tmp_shap5 == (1, 1, 1, 1, 1):
                        pass
                    if score > max_score_shape[0]:
                        max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                                   (m + (1 + offset) * x_decrict, n + (1 + offset) * y_derice),
                                                   (m + (2 + offset) * x_decrict, n + (2 + offset) * y_derice),
                                                   (m + (3 + offset) * x_decrict, n + (3 + offset) * y_derice),
                                                   (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                           (x_decrict, y_derice))

        # 计算两个形状相交 如两个3活 相交 得分增加 一个子的除外
        if max_score_shape[1] is not None:
            for item in score_all_arr:
                for pt1 in item[1]:
                    for pt2 in max_score_shape[1]:
                        if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                            add_score += item[0] + max_score_shape[0]

            score_all_arr.append(max_score_shape)

        return add_score + max_score_shape[0]
