import pygame as pg
import math
from datetime import datetime
from самолёт.config import *
import os

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
    def __init__(self, _blocks: list, _enemies: list, m_end):
        self.m_end = m_end
        self.start_blocks = str(_blocks)
        self.start_enemies = str(_enemies)
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

    def reload(self):
        self.blocks = eval(self.start_blocks)
        self.enemies = eval(self.start_enemies)
        self.m = 0
        self.player = Player(self.max_hp)
        self.lasers = []
        self.game_over = False
        self.win = False
        self.article = []
        self.end = False

    def handle_event(self, _event):
        click = None
        for _some in self.article:

            click_1 = _some.handle_event(_event)
            if click_1:
                click = click_1
        return click

    def update(self):
        if not debug and not self.game_over and not self.win:
            _over = self.player.update(self.blocks, self.enemies, self.lasers, self.blocks, self.enemies, self.m)
            if _over:
                self.player.hp -= 25
            for _laser in self.lasers:
                _over = _laser.update(self.player, self.lasers, self.enemies, self.xp_model, self.m)
                if _over:
                    self.player.hp -= 10

            if -abs(self.player.hp) == self.player.hp or self.player.hp == 0:
                self.game_over = True

            if self.m >= self.m_end and not self.enemies:
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

            _surf = self.arial.render("game over", True, (255, 90, 65))
            _screen.blit(_surf, (size[0] / 2 - _surf.get_rect()[2] / 2, size[1] / 2 - _surf.get_rect()[3] / 2))
            if not self.end:
                self.article.append(Button([size[0] / 2 - 60, size[1] / 2 + 30, 120, 30], "menu", "go to menu",
                                           border_x_y=[30, -1]))
                self.article.append(Button([size[0] / 2 - 60, size[1] / 2 + 70, 120, 30], "restart", "restart",
                                           border_x_y=[25, -1]))
            self.end = True
        elif self.win:

            _surf = self.arial.render("you win", True, (255, 90, 70))
            _screen.blit(_surf, (size[0] / 2 - _surf.get_rect()[2] / 2, size[1] / 2 - _surf.get_rect()[3] / 2))
            if not self.end:
                self.article.append(Button([size[0] / 2 - 60, size[1] / 2 + 30, 120, 30], "menu", "go to menu, you win",
                                           border_x_y=[30, -1]))
                self.article.append(Button([size[0] / 2 - 60, size[1] / 2 + 70, 120, 30], "next level", "next level",
                                           border_x_y=[10, -1]))

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
            # (255,255,255)   (0,0,0)
            _surf = self.arial.render(str(self.player.xp) + " xp", True, (0, 0, 0))
            _screen.blit(_surf, [size[0] - 50 - _surf.get_rect()[2], 10])
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
    def __init__(self, rect, text, name, FONT=pg.font.SysFont("arial", 28),
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
        self.name = name
        self.border = 0

    def handle_event(self, _event):
        rect = self.rect.copy()
        rect.y += self.border
        if rect.collidepoint(pg.mouse.get_pos()):
            if _event.type == pg.MOUSEBUTTONDOWN:

                if _event.button == 1 or _event.button == 2 or _event.button == 3:
                    return self.name
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
        self.size = [50, 50]
        self.gif = GIF("img/enemy/enemy_1")
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
                _surf = pygame.Surface([20, 20])
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
        surf = self.gif.draw()
        _screen.blit(surf, (self.pos[0], self.pos[1] + _m))
        return _screen

    def __str__(self):
        return f"Enemy_1({self.pos})"

    def __repr__(self):
        return f"Enemy_1({self.pos})"


class Laser:
    def __init__(self, start_pos: list, end_pos: list, made_by: str):

        self.made_by = made_by
        self.end_pos = end_pos
        self.start_pos = start_pos
        self.pos = start_pos
        self.speed = 4
        self.size = [20, 20]
        self.margin = [0, 0]
        self.rotate = 0
        if made_by == "player":
            self.img = pygame.image.load("img/armory/player/1.png")
        else:
            self.img = pygame.image.load("img/armory/enemy/1.png")
        self.img = pygame.transform.scale(self.img, self.size)
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

        _surf = self.img
        _surf = pygame.transform.rotate(_surf, self.rotate)
        self.img = _surf

    def update(self, player, lasers, enemies, xp_model, _m):
        x, y = self.margin

        self.pos = [self.pos[0] + x, self.pos[1] + y]
        if collide(pygame.Rect(*player.pos, *player.size),
                   pygame.Rect(*self.pos, *self.img.get_rect().size)) and self.made_by != "player":
            for _i in range(len(lasers)):
                if lasers[_i] == self:
                    lasers.pop(_i)
                    break
            return True
        for i in range(len(enemies)):

            if self.made_by == "player" and collide(
                    pygame.Rect(enemies[i].pos[0], enemies[i].pos[1] + _m + enemies[i].m_1, *enemies[i].size),
                    pygame.Rect(*self.pos, *self.img.get_rect().size)):
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
                pygame.Rect(*self.pos, self.pos[0] + self.img.get_rect()[2], self.pos[1] + self.img.get_rect()[3])):
            for i in range(len(lasers)):
                if lasers[i] == self:
                    lasers.pop(i)
                    break

        rect = self.img.get_rect()
        rect.center = [self.pos[0] + rect.size[0] / 2, self.pos[1] + rect.size[1] / 2]
        _screen.blit(self.img, rect)
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
        self.cooldown = 0.5
        self.date = datetime.now()
        self.hp = max_hp
        self.xp = 0
        self.gif = GIF("img/player/skin2")

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
            start_pos = [self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2]
            end_pos = list(mouse_pos)
            b, a = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
            rotate = math.degrees(math.atan2(b, a))
            _surf = pygame.Surface([20, 20])
            _surf.fill((255, 100, 100))
            _surf.set_colorkey((0, 0, 0))
            _surf = pygame.transform.rotate(_surf, rotate)
            _size_1 = _surf.get_rect().size

            lasers.append(Laser([start_pos[0] - _size_1[0] / 2, start_pos[1] - _size_1[1] / 2], end_pos, "player"))
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
        surf = self.gif.draw()
        _screen.blit(surf, (self.pos[0], self.pos[1] + _m))
        return _screen


class GIF:
    def __init__(self, path: str):
        self.cooldown = 0.04
        self.date = datetime.now()
        self.pitchers = []
        for name in os.listdir(path):
            png = pygame.image.load(path + "/" + name)
            self.pitchers.append(png)
        self.i = 0

    def draw(self):
        time = int(str(datetime.now() - self.date)[0:1]) * 3600 + \
               int(str(datetime.now() - self.date)[2:4]) * 60 + \
               int(str(datetime.now() - self.date)[5:7]) + \
               int(str(datetime.now() - self.date)[8:]) * 0.000001
        if time > self.cooldown:
            self.date = datetime.now()
            if self.i + 1 > len(self.pitchers) - 1:
                self.i = 0
            else:
                self.i += 1

        return self.pitchers[self.i]
