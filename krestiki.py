import pygame
import copy
import tkinter
import os.path
clock = pygame.time.Clock()

pygame.init() #ПАЙГЕЙМ ШОБ ТЫ ЗДОХ
size = 600, 400
scr = pygame.display.set_mode(size)
pygame.display.set_caption("Нолики-квадратики")
#print(os.path.exists('data/fonts/times.ttf'))
font = pygame.font.SysFont('TIMES', 20)
text1 = font.render("Правила просты:",True,(255, 0, 0))
text2 = font.render("Побеждает тот, кто",True,(255, 0, 0))
text3 = font.render("первым заполнит 4 клетки",True,(255, 0, 0))
text4 = font.render("в ряд (и по диагонали)",True,(255, 0, 0))
text5 = font.render("Никто не выиграл! ☺",True,(255, 0, 0))
kolvo = 0
zerowin = True #если тру - победили нули, другое - квадраты

class Board:
    # создание поля
    #kolvo = 0
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        global kolvo
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1:
                    pygame.draw.circle(scr, (100, 100, 100), (j * self.cell_size + self.left + 30, i * self.cell_size + self.top + 30), 28, 5)
                    #kolvo += 1
                elif self.board[i][j] == 2:
                    #crest
                    pygame.draw.rect(scr, (200, 200, 200), (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size))
                    #kolvo += 1
                else:
                    pygame.draw.rect(scr, (0, 0, 0), (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(scr, (255, 255, 255), (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size),1)

    def get_click(self,pos):
        cell = self.get_cell(pos)
        if cell:
            return self.on_click(cell)
        return False

    def get_cell(self,pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return x,y
#est or not
    def on_click(self, cell):
        if self.board[cell[1]][cell[0]] == 0:
            self.board[cell[1]][cell[0]] = self.board[cell[1]][cell[0]] + kolvo % 2 + 1
            return True
        else:
            return False

    def check_win(self):
        self.board_check = [[[[0,0,0],[0,0,0]]] * self.width for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                w = self.board[i][j] - 1
                if self.board[i][j] == 0:
                    continue
                if i == 0 and j == 0:
                    continue
                if i != 0 and j == 0:
                    if self.board[i][j] == self.board[i-1][j]:
                        self.board_check[i][j][w][0] = self.board_check[i-1][j][w][0]+1
                if i == 0 and j != 0:
                    if self.board[i][j] == self.board[i][j-1]:
                        self.board_check[i][j][w][2] = self.board_check[i][j-1][w][2]+1
                if i != 0 and j != 0:
                    if self.board[i][j] == self.board[i-1][j]:
                        self.board_check[i][j][w][0] = self.board_check[i-1][j][w][0]+1
                    if self.board[i][j] == self.board[i][j-1]:
                        self.board_check[i][j][w][2] = self.board_check[i][j-1][w][2]+1
                    if self.board[i][j] == self.board[i-1][j-1]:
                        self.board_check[i][j][w][1] = self.board_check[i-1][j-1][w][1]+1
                if self.board_check[i][j][w][0] == 3:
                    str = ''
                    if self.board[i][j] == 1:
                        str = 'Нолик'
                    elif self.board[i][j] == 2:
                        str = 'Крестик'
                    return True,str
                if self.board_check[i][j][w][1] == 3:
                    str = ''
                    if self.board[i][j] == 1:
                        str = 'Нолик'
                    elif self.board[i][j] == 2:
                        str = 'Крестик'
                    return True,str
                if self.board_check[i][j][w][2] == 3:
                    str = ''
                    if self.board[i][j] == 1:
                        str = 'Нолик'
                    elif self.board[i][j] == 2:
                        str = 'Крестик'
                    return True,str
        return False,None

class Life(Board):
    def __init__(self, w, h, l, t, size):
        super().__init__(w, h)
        super().set_view(l, t, size)


b = Life(5, 5, 10, 10, 60)
time = False
running = True
vol = 10
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #окончание игры и победитель
            scr.fill((50,50,50)) #ТОЛЬКО ОНО БЛИН НЕ РАБОТАЕТ
            if zerowin == True:
                winner = 'Нолики'#ЭТА ХРЕНЬ НЕ ВЫВОДИТСЯ
                scr.blit(text4, [100,10])
            else:
                winner = 'Квадратики' #КАК МЫ БЛИН ОПРЕДЕЛИМ КТО ПОБЕДИТЕЛЬ
                scr.blit(text4, [100,10]) #ЕСЛИ МЫ НЕ ЗНАЕМ ГДЕ НУЛИ А ГДЕ ЭТИ ТУПЫЕ КВАДРАТИКИ
            pygame.time.delay(1000)
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if b.get_click(event.pos):
                t,s = b.check_win()
                if t:
                    if s == 'Нолик':
                        zerowin = True
                    else:
                        zerowin = False
                    if zerowin == True:
                        winner = 'Нолики'
                        text5 = font.render("Нолики выиграли!",True,(245,44,44))
                    else:
                        winner = 'Квадратики'
                        text5 = font.render("Квадратики выиграли!",True,(245,44,44))
                    running = False
                kolvo += 1
    scr.fill((255, 255, 255))
    scr.blit(text1, [325,50])
    scr.blit(text2, [325,80])
    scr.blit(text3, [325,110])
    scr.blit(text4, [325,140])
    b.render()
    if time:
        b.next_move()
    pygame.display.flip()
    clock.tick(vol)

scr.fill((0,0,0))
scr.blit(text5, [225,170])
pygame.display.flip()
pygame.time.delay(2000)
pygame.quit()
