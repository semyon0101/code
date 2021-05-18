import pygame as pg

pg.init()


class Button:
    def __init__(self, rect, text, name, FONT=pg.font.SysFont("arial", 28),
                 COLOR_INACTIVE=(141, 182, 205, 255),
                 COLOR_ACTIVE=(28, 134, 238, 255), border_x_y=None):
        self.border_x_y = border_x_y
        self.active_1 = False
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
        if rect.collidepoint(pg.mouse.get_pos()) and self.active_1:
            if _event.type == pg.MOUSEBUTTONDOWN:

                if _event.button == 1 or _event.button == 2 or _event.button == 3:
                    return self.name
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]

        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        if not self.active_1:
            self.color = self.colors[0]
            self.txt_surface = self.FONT.render(self.text, True, self.color)

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


class OverFlow:
    def __init__(self, rect, target=50, color=None):
        self.target = target
        self.color = color
        self.rect = pg.Rect(rect)
        self.dote = []
        self.border = 0
        self.all_width = 0
        self.active = False
        self.old_pos_y = 0

    def update_1(self):
        for child in self.dote:
            self.all_width = max(self.all_width, child.rect.size[1] + child.rect.y)

    def add(self, *children):
        for child in children:
            self.dote.append(child)
        self.update_1()

    def handle_event(self, _event):
        if _event.type == pg.MOUSEBUTTONDOWN and self.all_width > self.rect.y + self.rect.size[1]:
            if _event.button == 4:
                self.border -= self.target
            elif _event.button == 5:
                self.border += self.target
        # rect = pg.Rect(0, 0, 0, 0)
        # if self.all_width > self.rect.y + self.rect.size[1]:
        #     rect = pg.Rect(self.rect.x + self.rect.size[0] - 10,
        #                    (self.border / self.all_width) * self.rect.size[1],
        #                    10, self.rect.size[1] ** 2 / self.all_width)
        d = False
        for child in self.dote:
            if self.active:
                child.active_1 = False
            else:
                child.active_1 = True
            a = child.handle_event(_event)
            if not a is None:
                d = a

        if d:
            return d

    def update(self):
        if self.all_width > self.rect.y + self.rect.size[1]:
            rect = pg.Rect(self.rect.x + self.rect.size[0] - 10,
                           (self.border / self.all_width) * self.rect.size[1],
                           10, self.rect.size[1] ** 2 / self.all_width)

            if rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed(num_buttons=3)[0]:
                self.active = True
            elif not pg.mouse.get_pressed(num_buttons=3)[0]:
                self.active = False
                self.old_pos_y = pg.mouse.get_pos()[1] - rect.y

            if self.active:
                self.border = (pg.mouse.get_pos()[1] - self.old_pos_y) * (self.all_width / self.rect.size[1])
            else:
                self.old_pos_y = pg.mouse.get_pos()[1] - rect.y
            if self.border < 0:
                self.border = 0
            elif self.border > self.all_width - self.rect.size[1]:
                self.border = self.all_width - self.rect.size[1]

        for child in self.dote:
            child.update()
            if self.all_width > self.rect.y + self.rect.size[1]:
                child.border = -self.border

    def draw(self, _screen):
        surf = pg.Surface((self.rect.size[0], self.rect.size[1]))
        if self.color:
            surf.fill(self.color)
        else:
            surf.set_colorkey((0, 0, 0))

        for child in self.dote:
            surf = child.draw(surf)
        _screen.blit(surf, (self.rect.x, self.rect.y))
        if self.all_width > self.rect.y + self.rect.size[1]:
            pg.draw.rect(_screen, (100, 100, 100),
                         pg.Rect(self.rect.x + self.rect.size[0] - 10,
                                 (self.border / self.all_width) * self.rect.size[1],
                                 10, self.rect.size[1] ** 2 / self.all_width))
        return _screen
