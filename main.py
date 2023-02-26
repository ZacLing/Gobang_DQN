import pygame
import sys
from pygame.locals import QUIT, KEYDOWN
import numpy as np
from environment import Env
from AgentPlayer import AgentPlayer

chess = Env()
# auto_player = AutoPlayer()
auto_player = AgentPlayer(strategy='mms', ratio=0.5)
# 初始化pygame
pygame.init()
# 获取对显示系统的访问，并创建一个窗口screen
# 窗口大小为670x670
screen = pygame.display.set_mode((670, 670))
# 72 209 204
screen_color = [72, 209, 204]  # 设置画布颜色,[238,154,73]对应为棕黄色
line_color = [0, 0, 0]  # 设置线条颜色，[0,0,0]对应黑色

mp_0 = np.zeros([15, 15], dtype=int)
mp_1 = np.zeros([15, 15], dtype=int)

def find_pos(x, y):  # 找到显示的可以落子的位置
    for i in range(27, 670, 44):
        for j in range(27, 670, 44):
            L1 = i - 22
            L2 = i + 22
            R1 = j - 22
            R2 = j + 22
            if x >= L1 and x <= L2 and y >= R1 and y <= R2:
                return i, j
    return x, y

def check_over_pos(x, y, over_pos):  # 检查当前的位置是否已经落子
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return False
    return True  # 表示没有落子

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

while game:  # 不断训练刷新画布

    for event in pygame.event.get():  # 获取事件，如果鼠标点击右上角关闭按钮，关闭
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    draw_screen()

    # 获取鼠标坐标信息
    x, y = pygame.mouse.get_pos()

    x, y = find_pos(x, y)
    if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再显示
        pygame.draw.rect(screen, [0, 229, 238], [x - 22, y - 22, 44, 44], 2, 1)

    keys_pressed = pygame.mouse.get_pressed()  # 获取鼠标按键信息
    # 鼠标左键表示落子,tim用来延时的，因为每次循环时间间隔很断，容易导致明明只按了一次左键，却被多次获取，认为我按了多次
    if keys_pressed[0] and tim == 0:
        flag = True
        if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再落子
            if len(over_pos) % 2 == 0:  # 黑子
                over_pos.append([[x, y], black_color])
                x_pos = int((x - 27) / 44)
                y_pos = int((y - 27) / 44)
                state = chess.move(0, x_pos, y_pos)
                if state == True:
                    continue
                chess_map, _, _, is_pos = chess.observe()
                p = auto_player.move_chess(x_pos, y_pos)
                state = chess.move(1, p[0], p[1])
                if state == True:
                    continue
                over_pos.append([[p[0], p[1]], white_color])

            '''
            else:
                over_pos.append([[x, y], white_color])
                chess.move(0, int((x - 27) / 44), int((y - 27) / 44))
                '''

    # 鼠标左键延时作用
    if flag:
        tim += 1
    if tim % 50 == 0:  # 延时200ms
        flag = False
        tim = 0

    pygame.display.update()  # 刷新显示
