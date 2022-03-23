import numpy as np
import pygame
import random as rd

pygame.init()


def spawn():
    i = rd.randint(0, 14)
    j = rd.randint(0, 14)
    while field[i, j] != 0:
        i = rd.randint(0, 14)
        j = rd.randint(0, 14)
    field[i, j] = -1


def index(a):
    for i in range(15):
        for j in range(15):
            if field[i, j] == a:
                return i, j


# возвращает расположение второй точки относительно первой, если они соседние
def direct(x1, y1, x2, y2):
    if x1 == x2 + 1:
        return 0
    elif x1 == x2 - 1:
        return 2
    elif y1 == y2 + 1:
        return 1
    else:
        return 3


# возвращает точки в порядке возрастания
def body_direction(a, b):  # a - i, b -j | возвращает точки в порядке возрастания
    # 0 - лево, 1 - вверх, 2 - право, 3 - низ
    value = field[a, b]
    n, m = -1, -1
    if value == 1:
        x2, y2 = index(2)
        m = direct(a, b, x2, y2)
    elif value == lengh:
        x2, y2 = index(value - 1)
        m = direct(a, b, x2, y2)
    elif 1 < value < lengh:
        x1, y1 = index(value + 1)
        x2, y2 = index(value - 1)
        n = direct(a, b, x1, y1)
        m = direct(a, b, x2, y2)
    if n > m:
        return m, n
    else:
        return n, m


def draw_body():
    for i in range(15):
        for j in range(15):
            if (i + j) % 2 == 0:
                gs.blit(lcell, (cell * i, cell * j))
            else:
                gs.blit(dcell, (cell * i, cell * j))
            if field[i, j] > 0:
                x, y = body_direction(i, j)
                if field[i, j] == 1:  # если это голова
                    if y == 0:
                        gs.blit(head_0, (i * cell, j * cell))
                    elif y == 1:
                        gs.blit(head_1, (i * cell, j * cell))
                    elif y == 2:
                        gs.blit(head_2, (i * cell, j * cell))
                    elif y == 3:
                        gs.blit(head_3, (i * cell, j * cell))
                elif field[i, j] == lengh:  # если это хвост
                    if y == 0:
                        gs.blit(tail_0, (i * cell, j * cell))
                    elif y == 1:
                        gs.blit(tail_1, (i * cell, j * cell))
                    elif y == 2:
                        gs.blit(tail_2, (i * cell, j * cell))
                    elif y == 3:
                        gs.blit(tail_3, (i * cell, j * cell))
                else:
                    if (x == 0) and (y == 2):
                        gs.blit(body_02, (i * cell, j * cell))
                    elif (x == 1) and (y == 3):
                        gs.blit(body_13, (i * cell, j * cell))
                    elif (x == 0) and (y == 1):
                        gs.blit(body_01, (i * cell, j * cell))
                    elif (x == 0) and (y == 3):
                        gs.blit(body_03, (i * cell, j * cell))
                    elif (x == 1) and (y == 2):
                        gs.blit(body_12, (i * cell, j * cell))
                    elif (x == 2) and (y == 3):
                        gs.blit(body_23, (i * cell, j * cell))
            if field[i, j] == -1:
                gs.blit(dot, (i * cell, j * cell))


def can_move():
    a, b = index(1)
    if (direction == 0) and (a - 1 >= 0):
        if field[a - 1, b] <= 0:
            return True
        else:
            return False
    elif (direction == 2) and (a + 1 <= 14):
        if field[a + 1, b] <= 0:
            return True
        else:
            return False
    elif (direction == 1) and (b - 1 >= 0):
        if field[a, b - 1] <= 0:
            return True
        else:
            return False
    elif (direction == 3) and (b + 1 <= 14):
        if field[a, b + 1] <= 0:
            return True
        else:
            return False


def is_eat():
    a, b = index(1)
    if (direction == 0) and (a - 1 >= 0):
        if field[a - 1, b] == -1:
            return True
        else:
            return False
    elif (direction == 2) and (a + 1 <= 14):
        if field[a + 1, b] == -1:
            return True
        else:
            return False
    elif (direction == 1) and (b - 1 >= 0):
        if field[a, b - 1] == -1:
            return True
        else:
            return False
    elif (direction == 3) and (b + 1 <= 14):
        if field[a, b + 1] == -1:
            return True
        else:
            return False


# движение
# True - eat
def move(bool):
    a, b = index(1)
    if direction == 0:
        a -= 1
    elif direction == 2:
        a += 1
    elif direction == 1:
        b -= 1
    elif direction == 3:
        b += 1
    if can_move():
        for i in range(15):
            for j in range(15):
                if field[i, j] > 0:
                    field[i, j] += 1
        field[a, b] = 1
        if not bool:
            a, b = index(lengh + 1)
            field[a, b] = 0


FPS = 5
lgreen = (153, 255, 102)
green = (102, 204, 0)
dgreen = (51, 102, 0)
white = (255, 255, 255)
black = (0, 0, 0)
crem = (245, 245, 220)
cell = 25  # толщина змеи - 7
xg = 17 * cell
yg = 18 * cell
sc = pygame.display.set_mode((xg, yg))
sc.fill(dgreen)
pygame.display.set_caption("Змейка")
gs = pygame.Surface((15 * cell, 15 * cell))
lcell = pygame.Surface((cell, cell))
lcell.fill(lgreen)
dcell = pygame.Surface((cell, cell))
dcell.fill(green)
clock = pygame.time.Clock()

file = open('h_score.txt', 'r')
h_score = int(file.read())
file.close()
font = pygame.font.SysFont('arial', 23)
text_h_sc = font.render('High score: ' + str(h_score), True, crem)
h_sc_rect = text_h_sc.get_rect(bottomright=(xg - cell, yg - cell / 2))
sc.blit(text_h_sc, h_sc_rect)
score = 0
text_sc = font.render('Score: ' + str(score), True, crem, dgreen)
sc_rect = text_sc.get_rect(bottomleft=(cell, yg - cell / 2))
sc.blit(text_sc, sc_rect)
next_sc = 100
lengh = 3
field = np.zeros([15, 15])  # [по x, по y]
field[7, 5] = 1
field[7, 4] = 2
field[7, 3] = 3
field[1, 1] = -1
direction = 3

# 0 - лево, 1 - вверх, 2 - право, 3 - низ
head_3 = pygame.image.load("pic/head.bmp").convert()
head_3.set_colorkey(white)
head_0 = pygame.transform.rotate(head_3, -90)
head_1 = pygame.transform.rotate(head_0, -90)
head_2 = pygame.transform.rotate(head_1, -90)

tail_1 = pygame.image.load("pic/tail.bmp").convert()
tail_1.set_colorkey(white)
tail_2 = pygame.transform.rotate(tail_1, -90)
tail_3 = pygame.transform.rotate(tail_2, -90)
tail_0 = pygame.transform.rotate(tail_3, -90)

body_13 = pygame.image.load("pic/body.bmp").convert()
body_13.set_colorkey(white)
body_02 = pygame.transform.rotate(body_13, -90)
body_23 = pygame.image.load("pic/bodyturn.bmp").convert()
body_23.set_colorkey(white)
body_03 = pygame.transform.rotate(body_23, -90)
body_01 = pygame.transform.rotate(body_03, -90)
body_12 = pygame.transform.rotate(body_01, -90)

dot = pygame.image.load("pic/dot.bmp").convert()
dot.set_colorkey(white)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w) and (direction != 3):
                direction = 1
            elif (event.key == pygame.K_s) and (direction != 1):
                direction = 3
            elif (event.key == pygame.K_d) and (direction != 0):
                direction = 2
            elif (event.key == pygame.K_a) and (direction != 2):
                direction = 0
    if not can_move():
        if h_score < score:
            file1 = open('h_score.txt', 'w')
            file1.write(str(score))
            file1.close()
        exit()
    if is_eat():
        score += next_sc
        next_sc += 20
        text_sc = font.render('Score: ' + str(score), True, crem, dgreen)
        sc_rect = text_sc.get_rect(bottomleft=(cell, yg - cell / 2))
        sc.blit(text_sc, sc_rect)
        lengh += 1
        spawn()
    move(is_eat())
    draw_body()
    sc.blit(gs, (cell, cell))
    pygame.display.update()
    clock.tick(FPS)
