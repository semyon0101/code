import pygame
import math
from datetime import datetime

pygame.init()
pygame.display.set_caption("самолёт")

clock = pygame.time.Clock()

debug = False

m = 0
m_1 = 0
arial = pygame.font.SysFont("arial", 36)

size = [500, 400]


class Laser:
    def __init__(self, start_pos: list, end_pos: list):
        self.end_pos = end_pos
        self.start_pos = start_pos
        self.pos = start_pos
        self.speed = 2
        self.size = [10, 30]
        self.margin = [0, 0]
        self.rotate = 0
        self.update_1()

    def update_1(self):
        b, a = self.end_pos[0] - self.pos[0], self.end_pos[1] - self.pos[1]
        if int(b) != 0:
            angle_in_rad = math.atan(a / b)
            self.rotate = math.degrees(math.atan2(b, a))
            x = -math.cos(angle_in_rad) * self.speed
            y = -math.sin(angle_in_rad) * self.speed
            if abs(b) == b:
                x = -x
                y = -y
            self.margin = [x, y]
        else:
            self.margin = [0, 1 * self.speed * abs(a) / a]

    def update(self):
        x, y = self.margin

        self.pos = [self.pos[0] + x, self.pos[1] + y]

    def draw(self, _screen):
        surf = pygame.Surface(self.size)
        surf.fill((255, 100, 100))
        surf.set_colorkey((0, 0, 0))
        l = len(lasers)
        if not pygame.Rect(0, 0, size[0], size[1]).colliderect(
                pygame.Rect(*self.pos, self.pos[0] + surf.get_rect()[2], self.pos[1] + surf.get_rect()[3])):
            for i in range(len(lasers)):
                i = l - 1 - i
                if lasers[i] == self:
                    lasers.pop(i)
        surf = pygame.transform.rotate(surf, self.rotate)
        rect = surf.get_rect()
        rect.center = self.pos
        _screen.blit(surf, rect)
        return _screen


class Block:
    def __init__(self, _pos: list):
        self.surf = pygame.Surface((50, 50))
        self.pos = _pos
        self.size = [50, 50]

    def draw(self, _screen, _m):
        _screen.blit(self.surf, (self.pos[0], self.pos[1] + _m))
        return _screen

    def __str__(self):
        return f"Block({self.pos})"

    def __repr__(self):
        return f"Block({self.pos})"


class Player:
    def __init__(self):
        self.pos = [size[0] / 2, size[0] / 2]
        self.size = [50, 50]
        self.surf = pygame.Surface(self.size)
        self.surf.fill((100, 255, 100))
        self.cooldown = 0.5
        self.date = datetime.now()

    def update(self, _blocks, _m):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.pos[0] > 0:
            self.pos[0] -= 3
        if keys[pygame.K_d] and self.pos[0] + self.size[0] < size[0]:
            self.pos[0] += 3
        if keys[pygame.K_w] and self.pos[1] > 0:
            self.pos[1] -= 3
        if keys[pygame.K_s] and self.pos[1] + self.size[1] < size[1]:
            self.pos[1] += 3

        click = pygame.mouse.get_pressed(num_buttons=3)[0]
        mouse_pos = pygame.mouse.get_pos()
        time = int(str(datetime.now() - self.date)[0:1]) * 3600 + \
               int(str(datetime.now() - self.date)[2:4]) * 60 + \
               int(str(datetime.now() - self.date)[5:7]) + \
               int(str(datetime.now() - self.date)[8:]) * 0.000001

        if click and time > self.cooldown:
            lasers.append(Laser([self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2],
                                list(mouse_pos)))
            self.date = datetime.now()

        def collide(rect1: pygame.Rect, rect2: pygame.Rect):
            a = False
            if (rect1[0] <= rect2[0] <= rect1[0] + rect1[2] or
                rect1[0] <= rect2[0] + rect2[2] <= rect1[0] + rect1[2] or
                (rect2[0] <= rect1[0] and rect2[0] + rect2[2] >= rect1[0] + rect1[2])) and \
                    (rect1[1] <= rect2[1] <= rect1[1] + rect1[3] or
                     rect1[1] <= rect2[1] + rect2[3] <= rect1[1] + rect1[3] or
                     (rect2[1] <= rect1[1] and rect2[1] + rect2[3] >= rect1[1] + rect1[3])):
                a = True
            return a

        _game_over = False
        for _block in _blocks:
            rect_1 = pygame.Rect(_block.pos[0] + 1, _block.pos[1] + _m + 1,
                                 _block.size[0] - 1, _block.size[1] - 1)

            rect_2 = pygame.Rect(*self.pos, *self.size)
            if collide(rect_1, rect_2):
                _game_over = True

        return _game_over

    def draw(self, _screen, _m):
        _screen.blit(self.surf, (self.pos[0], self.pos[1] + _m))
        return _screen


player = Player()
blocks = [Block([300, 150]), Block([300, 50])]

lasers = []
done = False
game_over = False
while not done:
    screen = pygame.display.set_mode(size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if debug:
                print(blocks)
            done = True
        if debug:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    m_1 += 30
                elif event.button == 5:
                    m_1 -= 30
                elif event.button == 1:
                    pos = pygame.mouse.get_pos()
                    size_1 = blocks[0].size
                    blocks.append(Block([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))

    screen.fill((30, 30, 30))

    if not debug and not game_over:
        game_over = player.update(blocks, m + m_1)
        for laser in lasers:
            laser.update()

    for block in blocks:
        screen = block.draw(screen, m + m_1)

    for laser in lasers:
        screen = laser.draw(screen)
    screen = player.draw(screen, m_1)
    if game_over:
        surf = arial.render("game over", 1, (255, 90, 70))
        screen.blit(surf, (size[0] / 2-surf.get_rect()[2]/2, size[1] / 2-surf.get_rect()[3]/2))

    if not debug and not game_over:
        m += 2
    pygame.display.flip()
    clock.tick(30)
