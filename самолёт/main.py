from class_ import *
import pygame
import math
from datetime import datetime

pygame.init()
pygame.display.set_caption("самолёт")

clock = pygame.time.Clock()

debug = False

m = 0
m_1 = 0
max_hp = 100
arial = pygame.font.SysFont("arial", 36)
xp_model = {
    "Enemy_2": 20,
    "Enemy_1": 10,
}

size = [500, 400]


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


class Enemy_2:
    def __init__(self, _pos: list):
        self.m_1 = 0
        self.speed = 1
        self.pos = _pos
        self.size = [30, 30]
        self.surf = pygame.Surface(self.size)
        self.draw_bool = False
        self.margin = [0, 0]

    def update(self, _blocks, _m):
        if pygame.Rect(0, 0, size[0], size[1]).colliderect(
                pygame.Rect(self.pos[0], self.pos[1], self.pos[0] + self.size[0],
                            self.pos[1] + self.size[1])):
            self.draw_bool = True
        else:
            self.draw_bool = False

        if self.draw_bool:
            b, a = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
            if int(b) != 0:
                angle_in_rad = math.atan(a / b)
                x = -math.cos(angle_in_rad) * self.speed
                y = -math.sin(angle_in_rad) * self.speed
                if abs(b) == b:
                    x = -x
                    y = -y
                self.margin = [x, y]
            else:
                self.margin = [0, 1 * self.speed * abs(a) / a]

        self.pos = [self.pos[0] + self.margin[0], self.pos[1] + self.margin[1]]

        self.m_1 = -_m

    def draw(self, _screen, _m):
        if self.draw_bool:
            _screen.blit(self.surf, (self.pos[0], self.pos[1]))
        return _screen

    def __str__(self):
        return f"Enemy_2({self.pos})"

    def __repr__(self):
        return f"Enemy_2({self.pos})"


class Enemy_1:
    def __init__(self, _pos: list):
        self.m_1 = 0
        self.pos = _pos
        self.size = [30, 50]
        self.surf = pygame.Surface(self.size)
        self.cooldown = 0.5
        self.date = datetime.now()

    def update(self, _blocks, _m):
        _m = self.m_1 + _m

        if pygame.Rect(0, 0, size[0], size[1]).colliderect(
                pygame.Rect(self.pos[0], self.pos[1] + _m, self.pos[0] + self.size[0],
                            self.pos[1] + _m + self.size[1])):
            time = int(str(datetime.now() - self.date)[0:1]) * 3600 + \
                   int(str(datetime.now() - self.date)[2:4]) * 60 + \
                   int(str(datetime.now() - self.date)[5:7]) + \
                   int(str(datetime.now() - self.date)[8:]) * 0.000001

            if time > self.cooldown:
                start_pos = [self.pos[0] + self.size[0] / 2, self.pos[1] + _m + self.size[1] / 2]
                end_pos = [player.pos[0] + player.size[0] / 2, player.pos[1] + player.size[1] / 2]
                b, a = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
                rotate = math.degrees(math.atan2(b, a))
                _surf = pygame.Surface([10, 30])
                _surf.fill((255, 100, 100))
                _surf.set_colorkey((0, 0, 0))
                _surf = pygame.transform.rotate(_surf, rotate)
                _size_1 = _surf.get_rect().size
                lasers.append(Laser([self.pos[0] + self.size[0] / 2 - _size_1[0] / 2,
                                     self.pos[1] + self.size[1] / 2 + _m - _size_1[1] / 2],
                                    [player.pos[0] + player.size[0] / 2, player.pos[1] + player.size[1] / 2], "enemy"))
                self.date = datetime.now()
        elif self.pos[1] + _m >= size[1]:
            for i in range(len(enemies)):
                _enemy = enemies[i]
                if _enemy == self:
                    enemies.pop(i)
                    return
        self.m_1 -= 1

        crash = False
        for _block in _blocks:
            rect_1 = pygame.Rect(_block.pos[0] + 1, _block.pos[1] + _m + 1,
                                 _block.size[0] - 1, _block.size[1] - 1)

            rect_2 = pygame.Rect(*self.pos, *self.size)
            if collide(rect_1, rect_2):
                crash = True
        if crash:
            for i in range(len(enemies)):
                if enemies[i] == self:
                    enemies.pop(i)
                    return

    def draw(self, _screen, _m):
        _m = self.m_1 + _m
        _screen.blit(self.surf, (self.pos[0], self.pos[1] + _m))
        return _screen

    def __str__(self):
        return f"Enemy_1({self.pos})"

    def __repr__(self):
        return f"Enemy_1({self.pos})"


class Laser:
    def __init__(self, start_pos: list, end_pos: list, made_by: str, color=(255, 100, 100)):
        self.color = color
        self.made_by = made_by
        self.end_pos = end_pos
        self.start_pos = start_pos
        self.pos = start_pos
        self.speed = 4
        self.size = [10, 30]
        self.margin = [0, 0]
        self.rotate = 0
        self.surf = pygame.Surface((0, 0))
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

        _surf = pygame.Surface(self.size)
        _surf.fill(self.color)
        _surf.set_colorkey((0, 0, 0))
        _surf = pygame.transform.rotate(_surf, self.rotate)
        self.surf = _surf

    def update(self, _m):
        x, y = self.margin

        self.pos = [self.pos[0] + x, self.pos[1] + y]
        if collide(pygame.Rect(*player.pos, *player.size),
                   pygame.Rect(*self.pos, *self.surf.get_rect().size)) and self.made_by != "player":
            for _i in range(len(lasers)):
                if lasers[_i] == self:
                    lasers.pop(_i)
                    break
            return True
        for i in range(len(enemies)):

            if self.made_by == "player" and collide(
                    pygame.Rect(enemies[i].pos[0], enemies[i].pos[1] + _m + enemies[i].m_1, *enemies[i].size),
                    pygame.Rect(*self.pos, *self.surf.get_rect().size)):
                name = str(enemies[i])
                for key in list(xp_model.keys()):
                    if name.startswith(key):
                        player.xp += xp_model[key]
                        break
                enemies.pop(i)
                for _i in range(len(lasers)):
                    if lasers[_i] == self:
                        lasers.pop(_i)
                        return

    def draw(self, _screen):

        if not pygame.Rect(0, 0, size[0], size[1]).colliderect(
                pygame.Rect(*self.pos, self.pos[0] + self.surf.get_rect()[2], self.pos[1] + self.surf.get_rect()[3])):
            for i in range(len(lasers)):
                if lasers[i] == self:
                    lasers.pop(i)
                    break

        rect = self.surf.get_rect()
        rect.center = [self.pos[0] + rect.size[0] / 2, self.pos[1] + rect.size[1] / 2]
        _screen.blit(self.surf, rect)
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
        self.hp = max_hp
        self.xp = 0

    def update(self, _blocks, _enemies, _m):
        _keys = pygame.key.get_pressed()
        if _keys[pygame.K_a] and self.pos[0] > 0:
            self.pos[0] -= 3
        if _keys[pygame.K_d] and self.pos[0] + self.size[0] < size[0]:
            self.pos[0] += 3
        if _keys[pygame.K_w] and self.pos[1] > 0:
            self.pos[1] -= 3
        if _keys[pygame.K_s] and self.pos[1] + self.size[1] < size[1]:
            self.pos[1] += 3

        click = pygame.mouse.get_pressed(num_buttons=3)[0]
        mouse_pos = pygame.mouse.get_pos()
        time = int(str(datetime.now() - self.date)[0:1]) * 3600 + \
               int(str(datetime.now() - self.date)[2:4]) * 60 + \
               int(str(datetime.now() - self.date)[5:7]) + \
               int(str(datetime.now() - self.date)[8:]) * 0.000001

        if click and time > self.cooldown:
            lasers.append(Laser([self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2],
                                list(mouse_pos), "player", color=[100, 100, 255]))
            self.date = datetime.now()

        _game_over = False
        for i in range(len(_blocks)):
            _block = _blocks[i]
            rect_1 = pygame.Rect(_block.pos[0] + 1, _block.pos[1] + _m + 1,
                                 _block.size[0] - 1, _block.size[1] - 1)

            rect_2 = pygame.Rect(*self.pos, *self.size)
            if collide(rect_1, rect_2):
                _game_over = True
                blocks.pop(i)
                break

        for i in range(len(_enemies)):
            _enemy = _enemies[i]
            rect_1 = pygame.Rect(_enemy.pos[0] + 1, _enemy.pos[1] + _m + _enemy.m_1 + 1,
                                 _enemy.size[0] - 1, _enemy.size[1] - 1)

            rect_2 = pygame.Rect(*self.pos, *self.size)
            if collide(rect_1, rect_2):
                _game_over = True
                enemies.pop(i)
                break

        return _game_over

    def draw(self, _screen, _m):
        _screen.blit(self.surf, (self.pos[0], self.pos[1] + _m))
        return _screen


player = Player()
blocks = [Block([300, 150]), Block([300, 50])]
enemies = [Enemy_1([150, 150]), Enemy_2([200, 200])]

lasers = []
done = False
game_over = False
win = False
samsung = []
while not done:
    screen = pygame.display.set_mode(size)
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if debug:
                print("blocks = " + str(blocks))
                print("enemies = " + str(enemies))
            done = True
        if debug:
            if event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                if event.button == 4:
                    m_1 += 30
                elif event.button == 5:
                    m_1 -= 30
                elif event.button == 1 and keys[pygame.K_1]:
                    pos = pygame.mouse.get_pos()
                    size_1 = Block([0, 0]).size
                    blocks.append(Block([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))
                elif event.button == 1 and keys[pygame.K_2]:
                    pos = pygame.mouse.get_pos()
                    size_1 = Enemy_1([0, 0]).size
                    enemies.append(Enemy_1([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))
                elif event.button == 1 and keys[pygame.K_3]:
                    pos = pygame.mouse.get_pos()
                    size_1 = Enemy_2([0, 0]).size
                    enemies.append(Enemy_2([pos[0] - size_1[0] / 2, pos[1] - size_1[1] / 2 - m_1]))
        else:
            for same in samsung:
                same.handle_event(event)

    if not debug and not game_over and not win:
        over = player.update(blocks, enemies, m)
        if over:
            player.hp -= 25
        for laser in lasers:
            over = laser.update(m)
            if over:
                player.hp -= 10
            if -abs(player.hp) == player.hp:
                game_over = True

        if m >= 360 and not enemies:
            win = True

        for enemy in enemies:
            enemy.update(blocks, m)

    for block in blocks:
        screen = block.draw(screen, m + m_1)

    for laser in lasers:
        screen = laser.draw(screen)

    for enemy in enemies:
        screen = enemy.draw(screen, m + m_1)

    screen = player.draw(screen, m_1)

    for same in samsung:
        screen = same.draw(screen)

    if game_over:
        surf = arial.render("game over", True, (255, 90, 70))
        screen.blit(surf, (size[0] / 2 - surf.get_rect()[2] / 2, size[1] / 2 - surf.get_rect()[3] / 2))
    elif win:
        def func():
            pass
        surf = arial.render("you win", True, (255, 90, 70))
        screen.blit(surf, (size[0] / 2 - surf.get_rect()[2] / 2, size[1] / 2 - surf.get_rect()[3] / 2))

        samsung.append(Button([size[0] / 2 - 50, size[1] / 2 + 30, 100, 30], "in menu", func))


    if not debug:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect([0, 0, 203, 53]))
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect([0, 0, 203, 53]), 2)
        pygame.draw.rect(screen,
                         [100 + (max_hp - max(player.hp, 0)) * (155 / max_hp),
                          255 - (max_hp - max(player.hp, 0)) * (155 / max_hp),
                          100], pygame.Rect([2, 2, 200 / max_hp * max(player.hp, 0), 50]))

        surf = arial.render(str(max(player.hp, 0))+" hp", True, (255, 255, 255))
        screen.blit(surf, [101.5 - surf.get_rect()[2] / 2, 26.5 - surf.get_rect()[3] / 2])

        surf = arial.render(str(player.xp)+" xp", True, (255, 255, 255))
        screen.blit(surf, [450 - surf.get_rect()[2], 10])


    else:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect([0, 0, 203, 53]))
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect([0, 0, 203, 53]), 2)
        surf = arial.render(str(m_1), True, (255, 255, 255))
        screen.blit(surf, [101.5 - surf.get_rect()[2] / 2, 26.5 - surf.get_rect()[3] / 2])

    if not debug and not game_over and not win:
        m += 2

    pygame.display.flip()
    clock.tick(30)
