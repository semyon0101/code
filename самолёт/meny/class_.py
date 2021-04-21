import pygame as pg
import math
from datetime import datetime
from самолёт.config import *

pg.init()

pygame = pg


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


class Level:
    def __init__(self, _blocks: list, _enemies: list):
        self.blocks = _blocks
        self.enemies = _enemies
        self.m = 0
        self.max_hp = 100
        self.player = Player(self.max_hp)
        self.arial = pygame.font.SysFont("arial", 36)
        self.xp_model = {
            "Enemy_2": 20,
            "Enemy_1": 10,
        }
        self.lasers = []
        self.game_over = False
        self.win = False
        self.article = []
        self.end = False

    def handle_event(self, _event):
        for _some in self.article:
            click = _some.handle_event(_event)
            if click:
                return True

    def update(self):
        if not debug and not self.game_over and not self.win:
            _over = self.player.update(self.blocks, self.enemies, self.lasers, self.blocks, self.enemies, self.m)
            if _over:
                self.player.hp -= 25
            for _laser in self.lasers:
                _over = _laser.update(self.player, self.lasers, self.enemies, self.xp_model, self.m)
                if _over:
                    self.player.hp -= 10
                if -abs(self.player.hp) == self.player.hp:
                    self.game_over = True

            if self.m >= 360 and not self.enemies:
                self.win = True

            for _enemy in self.enemies:
                _enemy.update(self.blocks, self.player, self.lasers, self.enemies, self.m)

        if not debug and not self.game_over and not self.win:
            self.m += 2

    def draw(self, _screen, m_1):
        for _block in self.blocks:
            _screen = _block.draw(_screen, self.m + m_1)

        for _laser in self.lasers:
            _screen = _laser.draw(self.lasers, _screen)

        for _enemy in self.enemies:
            _screen = _enemy.draw(_screen, self.m + m_1)

        _screen = self.player.draw(_screen, m_1)

        for _some in self.article:
            _screen = _some.draw(_screen)

        if self.game_over:
            self.end = True
            _surf = self.arial.render("game over", True, (255, 90, 65))
            _screen.blit(_surf, (size[0] / 2 - _surf.get_rect()[2] / 2, size[1] / 2 - _surf.get_rect()[3] / 2))
        elif self.win:

            def func():
                return True

            _surf = self.arial.render("you win", True, (255, 90, 70))
            _screen.blit(_surf, (size[0] / 2 - _surf.get_rect()[2] / 2, size[1] / 2 - _surf.get_rect()[3] / 2))
            if not self.end:
                self.article.append(Button([size[0] / 2 - 60, size[1] / 2 + 30, 120, 30], "in menu", func,
                                           border_x_y=[20, -1]))

            self.end = True

        if not debug:
            pygame.draw.rect(_screen, (0, 0, 0), pygame.Rect([0, 0, 203, 53]))
            pygame.draw.rect(_screen, (100, 100, 100), pygame.Rect([0, 0, 203, 53]), 2)
            pygame.draw.rect(_screen,
                             [100 + (self.max_hp - max(self.player.hp, 0)) * (155 / self.max_hp),
                              255 - (self.max_hp - max(self.player.hp, 0)) * (155 / self.max_hp),
                              100], pygame.Rect([2, 2, 200 / self.max_hp * max(self.player.hp, 0), 50]))

            _surf = self.arial.render(str(max(self.player.hp, 0)) + " hp", True, (255, 255, 255))
            _screen.blit(_surf, [101.5 - _surf.get_rect()[2] / 2, 26.5 - _surf.get_rect()[3] / 2])

            _surf = self.arial.render(str(self.player.xp) + " xp", True, (255, 255, 255))
            _screen.blit(_surf, [450 - _surf.get_rect()[2], 10])


        else:
            pygame.draw.rect(_screen, (0, 0, 0), pygame.Rect([0, 0, 203, 53]))
            pygame.draw.rect(_screen, (100, 100, 100), pygame.Rect([0, 0, 203, 53]), 2)
            _surf = self.arial.render(str(m_1), True, (255, 255, 255))
            _screen.blit(_surf, [101.5 - _surf.get_rect()[2] / 2, 26.5 - _surf.get_rect()[3] / 2])

        return _screen

    def __str__(self):
        return f"Level({self.blocks}, {self.enemies})"

    def __repr__(self):
        return f"Level({self.blocks}, {self.enemies})"


class Button:
    def __init__(self, rect, text, func, FONT=pg.font.SysFont("arial", 28),
                 COLOR_INACTIVE=(141, 182, 205, 255),
                 COLOR_ACTIVE=(28, 134, 238, 255), border_x_y=None):
        self.border_x_y = border_x_y
        self.active = False
        self.rect = pg.Rect(rect)
        self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render(text, True, self.color)
        self.FONT = FONT
        self.text = text
        self.colors = [COLOR_INACTIVE, COLOR_ACTIVE]
        self.func = func
        self.border = 0

    def handle_event(self, _event):
        rect = self.rect.copy()
        rect.y += self.border
        if rect.collidepoint(pg.mouse.get_pos()):
            if _event.type == pg.MOUSEBUTTONDOWN:

                if _event.button == 1 or _event.button == 2 or _event.button == 3:
                    self.func()
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]

        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        pass

    def draw(self, _screen):
        pg.draw.rect(_screen, (50, 50, 50),
                     pg.Rect(self.rect.x, self.rect.y + self.border, self.rect.size[0] + 1, self.rect.size[1] + 1))
        if self.border_x_y:
            _screen.blit(self.txt_surface, (self.rect.x + self.border_x_y[0], self.rect.y + self.border_x_y[1]))
        else:
            _screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + self.border))
        pg.draw.rect(_screen, self.color,
                     pg.Rect(self.rect.x, self.rect.y + self.border, self.rect.size[0], self.rect.size[1]), 2)

        return _screen


class Enemy_2:
    def __init__(self, _pos: list):
        self.m_1 = 0
        self.speed = 1
        self.pos = _pos
        self.size = [30, 30]
        self.surf = pygame.Surface(self.size)
        self.draw_bool = False
        self.margin = [0, 0]

    def update(self, _blocks, _player, _lasers, _enemies, _m):
        if pygame.Rect(0, 0, size[0], size[1]).colliderect(
                pygame.Rect(self.pos[0], self.pos[1], self.pos[0] + self.size[0],
                            self.pos[1] + self.size[1])):
            self.draw_bool = True
        else:
            self.draw_bool = False

        if self.draw_bool:
            b, a = _player.pos[0] - self.pos[0], _player.pos[1] - self.pos[1]
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
        elif debug:
            _screen.blit(self.surf, (self.pos[0], self.pos[1] + _m))
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

    def update(self, _blocks, _player, _lasers, _enemies, _m):
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
                end_pos = [_player.pos[0] + _player.size[0] / 2, _player.pos[1] + _player.size[1] / 2]
                b, a = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
                rotate = math.degrees(math.atan2(b, a))
                _surf = pygame.Surface([10, 30])
                _surf.fill((255, 100, 100))
                _surf.set_colorkey((0, 0, 0))
                _surf = pygame.transform.rotate(_surf, rotate)
                _size_1 = _surf.get_rect().size
                _lasers.append(Laser([self.pos[0] + self.size[0] / 2 - _size_1[0] / 2,
                                      self.pos[1] + self.size[1] / 2 + _m - _size_1[1] / 2],
                                     [_player.pos[0] + _player.size[0] / 2, _player.pos[1] + _player.size[1] / 2],
                                     "enemy"))
                self.date = datetime.now()
        elif self.pos[1] + _m >= size[1]:
            for i in range(len(_enemies)):
                _enemy = _enemies[i]
                if _enemy == self:
                    _enemies.pop(i)
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
            for i in range(len(_enemies)):
                if _enemies[i] == self:
                    _enemies.pop(i)
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

    def update(self, player, lasers, enemies, xp_model, _m):
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

    def draw(self, lasers, _screen):

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
    def __init__(self, max_hp):
        self.pos = [size[0] / 2, size[0] / 2]
        self.size = [50, 50]
        self.surf = pygame.Surface(self.size)
        self.surf.fill((100, 255, 100))
        self.cooldown = 0.5
        self.date = datetime.now()
        self.hp = max_hp
        self.xp = 0

    def update(self, _blocks, _enemies, lasers, blocks, enemies, _m):
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
