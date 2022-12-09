import numpy as np
import pygame

n = 50
cells = np.random.randint(0, 1, (n, n))
WIDTH = 1000  # ширина экрана
HEIGHT = 600  # высота экрана
GRID_SIZE = n  # Ширина и высота игрового поля
SQUARE_SIZE = int(HEIGHT / n)  # Размер одной клетки на поле

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], flags=pygame.RESIZABLE)
pygame.display.set_caption('Game Life')
# Run until the user asks to quit
running = True
to_start = False
font = pygame.font.SysFont('Arial', 30)
objects = []


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        objects.append(self)
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def next_generation():
    cells_new = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            if cells[i, j]:
                if i > 0 and j > 0:
                    cells_new[i - 1, j - 1] += 1
                if i > 0:
                    cells_new[i - 1, j] += 1
                if i > 0 and j < n - 1:
                    cells_new[i - 1, j + 1] += 1
                if j > 0:
                    cells_new[i, j - 1] += 1
                if j < n - 1:
                    cells_new[i, j + 1] += 1
                if i < n - 1 and j > 0:
                    cells_new[i + 1, j - 1] += 1
                if i < n - 1:
                    cells_new[i + 1, j] += 1
                if i < n - 1 and j < n - 1:
                    cells_new[i + 1, j + 1] += 1
    for i in range(0, n):
        for j in range(0, n):
            if cells[i, j]:
                if cells_new[i, j] == 2 or cells_new[i, j] == 3:
                    cells_new[i, j] = 1
                else:
                    cells_new[i, j] = 0
            else:
                if cells_new[i, j] == 3:
                    cells_new[i, j] = 1
                else:
                    cells_new[i, j] = 0
    return cells_new


def start():
    global to_start
    to_start = True


def pause():
    global to_start
    to_start = False


def restart():
    global cells
    cells = np.random.randint(0, 2, (n, n))


def end():
    pygame.quit()


Button(SQUARE_SIZE * n + 50, 30, 400, 50, 'Старт', start)
Button(SQUARE_SIZE * n + 50, 100, 400, 50, 'Пауза', pause)
Button(SQUARE_SIZE * n + 50, 170, 400, 50, 'Перезапуск', restart)
Button(SQUARE_SIZE * n + 50, 240, 400, 50, 'Конец', end)

while running:
    cellsRect = pygame.Rect(0, 0, SQUARE_SIZE * n, SQUARE_SIZE * n)
    cellsSurface = pygame.Surface((SQUARE_SIZE * n, SQUARE_SIZE * n))
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        mousePos = pygame.mouse.get_pos()
        if cellsRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                cells[int(mousePos[1] // SQUARE_SIZE), int(mousePos[0] // SQUARE_SIZE)] = \
                    not cells[int(mousePos[1] // SQUARE_SIZE), int(mousePos[0] // SQUARE_SIZE)]


    screen.fill((255, 255, 255))


    if to_start:
        cells = next_generation()

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if cells[j, i]:
                pygame.draw.rect(screen, (0, 0, 0), (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),1)

    for object in objects:
        object.process()
    pygame.display.flip()


pygame.quit()