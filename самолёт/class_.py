import pygame as pg

pg.init()


class Button:
    def __init__(self, rect, text, func, FONT=pg.font.SysFont("arial", 28),
                 COLOR_INACTIVE=(141, 182, 205, 255),
                 COLOR_ACTIVE=(28, 134, 238, 255)):
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
        _screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + self.border))
        pg.draw.rect(_screen, self.color,
                     pg.Rect(self.rect.x, self.rect.y + self.border, self.rect.size[0], self.rect.size[1]), 2)

        return _screen
