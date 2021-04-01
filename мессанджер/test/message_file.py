import pygame


# from class_ import *


def start():
    pygame.init()

    class TextAria:
        def __init__(self, pos, width, FONT=pygame.font.Font(None, 34), margin_text=5, color_text=(255, 255, 255),
                     max_len=None):
            self.max_len = max_len
            self.color_text = color_text
            self.margin_text = margin_text
            self.FONT = FONT
            self.pos = pos
            self.width = width
            self.text = ""
            self.draw_blocks = []
            self.good_text = [""]
            self.wights_mark = []
            self.wights_mark_2 = []
            self.cursor = [0, 0]
            self.update_1()

        def update_1(self):
            pass

        def handle_event(self, _event):
            if _event.type == pygame.KEYDOWN:
                if _event.unicode == "\r" or _event.unicode == "\n":
                    self.text += "\n"
                    self.cursor[1] += 1
                    self.cursor[0] = 0
                elif _event.unicode != "":
                    self.text += _event.unicode
                    self.cursor[0] += 1

        def update(self):
            self.good_text = [""]
            self.wights_mark = []
            self.wights_mark_2 = []
            self.draw_blocks = []

            ar = []
            for STR in self.text.split("\n"):
                ar.append([STR])

            for i in range(len(ar)):
                for j in range(len(ar[i][0])):
                    if ar[i][0][j] != "":
                        ar[i].append(ar[i][0][j])
                ar[i].pop(0)
            for i in range(len(ar)):
                if i != 0:
                    self.good_text.append(f"")
                for j in range(len(ar[i])):
                    mark = "".join(ar[i][j])
                    width = self.FONT.render(self.good_text[-1] + mark, True, (0, 0, 0)).get_width()
                    if width >= self.width:
                        self.good_text.append(f"{mark}")
                    else:
                        self.good_text[-1] += mark

            if self.max_len and len(self.good_text) > self.max_len:
                self.text = self.text[:-1]
                self.good_text = self.good_text[:self.max_len]

            text = self.FONT.render("12", True, (0, 0, 0))

            for i in range(len(self.good_text)):
                y = self.pos[1] - (len(self.good_text) - 1 - i) * (text.get_height() + self.margin_text)
                self.wights_mark.append([(0, y)])
                for j in range(len(self.good_text[i])):
                    text_1 = self.good_text[i][:(j + 1)]

                    self.wights_mark[i].append((self.FONT.render(text_1, True, (0, 0, 0)).get_width(), y))
            col_mark = 0

            for i in range(len(self.text.split("\n"))):
                y = self.pos[1] - (len(self.good_text) - 1 - col_mark) * (text.get_height() + self.margin_text)

                self.wights_mark_2.append([(self.pos[0], y)])

                ar = [""]

                for j in range(len(self.text.split("\n")[i])):
                    mark = "".join(self.text.split("\n")[i][j])
                    width = self.FONT.render(ar[-1] + mark, True, (0, 0, 0)).get_width()
                    if width >= self.width:
                        ar.append(f"{mark}")
                        col_mark += 1
                    else:
                        ar[-1] += mark
                    x = self.FONT.render(ar[-1], True, (0, 0, 0)).get_width() + self.pos[0]
                    y = self.pos[1] - (len(self.good_text) - 1 - col_mark) * (text.get_height() + self.margin_text)

                    self.wights_mark_2[i].append((x, y))

                col_mark += 1

            if self.cursor[1] + 1 > len(self.text.split("\n")):
                self.cursor[1] = len(self.text.split("\n")) - 1
            if self.cursor[0] - 1 >= len(self.text.split("\n")[self.cursor[1]]) and self.text.split("\n")[
                self.cursor[1]]:
                self.cursor[0] = len(self.text.split("\n")) - 1

            for i in range(len(self.good_text)):
                y = self.pos[1] - (len(self.good_text) - 1 - i) * (text.get_height() + self.margin_text)
                self.draw_blocks.append((self.FONT.render(self.good_text[i], True, self.color_text), (self.pos[0], y)))

        def draw(self, _screen):
            text = self.FONT.render("12", True, (0, 0, 0))

            for block in self.draw_blocks:
                _screen.blit(block[0], (block[1][0], block[1][1]))
            surf = pygame.Surface((1, text.get_height()))
            surf.fill(self.color_text)
            _screen.blit(surf, self.wights_mark_2[self.cursor[1]][self.cursor[0]])

            return _screen

    pygame.display.set_caption("Мессанджер")
    screen = pygame.display.set_mode((500, 400))

    clock = pygame.time.Clock()

    text_aria = TextAria((100, 100), 300)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return True
            text_aria.handle_event(event)
        screen.fill((30, 30, 30))
        text_aria.update()

        screen = text_aria.draw(screen)
        pygame.display.flip()
        clock.tick(30)
