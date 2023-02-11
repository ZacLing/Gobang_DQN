import pygame
import sys
# 调用常用关键字常量
from pygame.locals import QUIT, KEYDOWN
import numpy as np
import pandas as pd
from environment import Env

chess = Env()

record = pd.read_csv('game_record/game_332.csv')
# 初始化pygame
pygame.init()
# 获取对显示系统的访问，并创建一个窗口screen
# 窗口大小为670x670
screen = pygame.display.set_mode((670, 670))
# 72 209 204
screen_color = [72, 209, 204]  # 设置画布颜色,[238,154,73]对应为棕黄色
line_color = [0, 0, 0]  # 设置线条颜色，[0,0,0]对应黑色

def draw_screen():
    screen.fill(screen_color)  # 清屏
    for i in range(27, 670, 44):
        # 先画竖线
        if i == 27 or i == 670 - 27:  # 边缘线稍微粗一些
            pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 4)
        else:
            pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 2)
        # 再画横线
        if i == 27 or i == 670 - 27:  # 边缘线稍微粗一些
            pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 4)
        else:
            pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 2)

    # 在棋盘中心画个小圆表示正中心位置
    pygame.draw.circle(screen, line_color, [27 + 44 * 7, 27 + 44 * 7], 8, 0)

    _, not_pos, player, _ = chess.observe()
    for index in range(len(not_pos)):
        if player[index] == 0:
            color = [255, 255, 255]
        else:
            color = [0, 0, 0]
        move_pos = (not_pos[index] * 44 + 27).tolist()
        pygame.draw.circle(screen, color, move_pos, 20, 0)


flag = False
tim = 0

over_pos = []  # 表示已经落子的位置
white_color = [255, 255, 255]  # 白棋颜色
black_color = [0, 0, 0]  # 黑棋颜色

game = True
i = 0
while True:
    # for i in range(len(record)):

    for event in pygame.event.get():  # 获取事件，如果鼠标点击右上角关闭按钮，关闭
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    draw_screen()

    now = record.iloc[i]
    chess.move(now['player'], now['move_x'], now['move_y'])

    pygame.time.delay(100)
    if i < len(record) - 1:
        i += 1
    pygame.display.update()