import pygame
import pyperclip

# from class_ import *


def start():
    pygame.init()

    class TextAria:
        def __init__(self, pos, width, FONT=pygame.font.Font(None, 34), margin_text=5, color_text=(255, 255, 255)):
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
            self.old_click = [False, pygame.mouse.get_pos()]
            self.outline = {}
            self.update()

        def handle_event(self, _event):
            if _event.type == pygame.KEYDOWN:
                keys_1 = list(self.outline.keys())
                keys = pygame.key.get_pressed()
                stop = False
                if len(keys_1) >= 2 and _event.unicode != "" and not (_event.key == pygame.K_c and keys[pygame.K_LCTRL]):
                    arr_text_1 = self.text.split("\n")
                    if keys_1[0][1] == keys_1[1][1]:
                        text_1_1 = arr_text_1[keys_1[0][1]][:keys_1[0][0]]
                        text_2_1 = arr_text_1[keys_1[0][1]][keys_1[1][0]:]
                        arr_text_1[keys_1[0][1]] = text_1_1+text_2_1
                        self.text = "\n".join(arr_text_1)
                        self.cursor = [keys_1[0][0], keys_1[0][1]]
                    else:
                        text_1_1 = arr_text_1[keys_1[0][1]][:keys_1[0][0]]
                        text_2_1 = arr_text_1[keys_1[1][1]:]
                        text_2_1[0] = text_2_1[0][keys_1[1][0]:]
                        text_2_1 = "\n".join(text_2_1)
                        arr_text_1[keys_1[0][1]] = text_1_1+text_2_1
                        arr_text_1=arr_text_1[:keys_1[0][1]+1]
                        self.text = "\n".join(arr_text_1)
                        self.cursor = [keys_1[0][0], keys_1[0][1]]
                    stop = True

                if _event.unicode == "\r" or _event.unicode == "\n":
                    arr_text = self.text.split("\n")
                    text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                    text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                    arr_text[self.cursor[1]] = text_1 + "\n" + text_2
                    self.text = "\n".join(arr_text)
                    self.cursor[1] += 1
                    self.cursor[0] = 0
                    self.outline = {}
                elif _event.unicode == "\t":
                    arr_text = self.text.split("\n")
                    text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                    text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                    arr_text[self.cursor[1]] = text_1 + "    " + text_2
                    self.text = "\n".join(arr_text)
                    self.cursor[0] += 4
                    self.outline = {}
                elif _event.key == pygame.K_c and keys[pygame.K_LCTRL]:
                    arr_text = self.text.split("\n")
                    if keys_1[0][1] == keys_1[1][1]:
                        text_1 = arr_text[keys_1[0][1]][keys_1[0][0]:keys_1[1][0]]
                        pyperclip.copy(text_1)
                    else:
                        text_1 = arr_text[keys_1[0][1]][keys_1[0][0]:]
                        text_2 = arr_text[keys_1[0][1]+1:keys_1[1][1]+1]
                        if text_2:
                            text_2[-1] = text_2[-1][:keys_1[1][0]]
                        pyperclip.copy("\n".join([text_1]+text_2).replace("\n", "\r\n"))
                elif _event.key == pygame.K_v and keys[pygame.K_LCTRL]:
                    paste = pyperclip.paste().replace("\r\n", "\n")
                    arr_text = self.text.split("\n")
                    text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                    text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                    arr_text[self.cursor[1]] = text_1 + paste + text_2
                    self.text = "\n".join(arr_text)
                    self.cursor[1] += len(paste.split("\n"))-1
                    self.cursor[0] += len(paste.split("\n")[-1])
                    self.outline = {}
                elif _event.key == pygame.K_BACKSPACE:
                    if not stop:
                        arr_text = self.text.split("\n")
                        text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                        text_2 = arr_text[self.cursor[1]][self.cursor[0]:]

                        if text_1 == "" and self.cursor[1] != 0:
                            arr_text_1 = arr_text[:self.cursor[1]-1]
                            arr_text_1.append(arr_text[self.cursor[1]-1]+arr_text[self.cursor[1]])
                            arr_text_1 += arr_text[self.cursor[1]+1:]
                            arr_text = arr_text_1

                            self.cursor[1] -= 1
                            self.cursor[0] = len(arr_text[self.cursor[1]])
                        else:
                            arr_text[self.cursor[1]] = text_1[:-1] + text_2
                            self.cursor[0] -= 1

                        self.text = "\n".join(arr_text)
                    self.outline = {}
                elif _event.key == pygame.K_DELETE:
                    if not stop:
                        arr_text = self.text.split("\n")
                        text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                        text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                        if text_2 == "" and self.cursor[1]+1<len(arr_text):
                            arr_text_1 = arr_text[:self.cursor[1]]
                            arr_text_1.append(arr_text[self.cursor[1]] + arr_text[self.cursor[1]+1])
                            arr_text_1 += arr_text[self.cursor[1] + 2:]
                            arr_text = arr_text_1
                        else:
                            arr_text[self.cursor[1]] = text_1 + text_2[1:]

                        self.text = "\n".join(arr_text)
                    self.outline = {}
                elif _event.key == pygame.K_LEFT:
                    self.cursor[0] -= 1
                    if self.cursor[0] < 0 <= self.cursor[1] - 1:
                        self.cursor[1] -= 1
                        self.cursor[0] = len(self.text.split("\n")[self.cursor[1]])
                    self.outline = {}
                elif _event.key == pygame.K_RIGHT:
                    self.cursor[0] += 1
                    if self.cursor[0] > len(self.text.split("\n")[self.cursor[1]]) and \
                            self.cursor[1] + 1 < len(self.text.split("\n")):
                        self.cursor[1] += 1
                        self.cursor[0] = 0
                    self.outline = {}
                elif _event.unicode != "":
                    arr_text = self.text.split("\n")
                    text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                    text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                    arr_text[self.cursor[1]] = text_1 + _event.unicode + text_2
                    self.text = "\n".join(arr_text)
                    self.cursor[0] += 1
                    self.outline = {}

                if self.cursor[0] < 0:
                    self.cursor[0] = 0
                if self.cursor[1] < 0:
                    self.cursor[1] = 0
                if self.cursor[0] > len(self.text.split("\n")[self.cursor[1]]):
                    self.cursor[0] = len(self.text.split("\n")[self.cursor[1]])
                if self.cursor[1] > len(self.text.split("\n")):
                    self.cursor[1] = len(self.text.split("\n"))
            elif _event.type == pygame.MOUSEBUTTONDOWN:
                self.outline = {}
                if _event.button == 1:
                    height = self.FONT.render("12", True, (0, 0, 0)).get_height() + self.margin_text
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(len(self.wights_mark_2)):
                        for j in range(len(self.wights_mark_2[i])):
                            margin_1 = 0
                            margin_2 = 0
                            if j != 0:
                                margin_1 = max((self.wights_mark_2[i][j][0] - self.wights_mark_2[i][j - 1][0]) / 2, 0)
                            if j != len(self.wights_mark_2[i]) - 1:
                                margin_2 = max((self.wights_mark_2[i][j + 1][0] - self.wights_mark_2[i][j][0]) / 2, 0)

                            rect = pygame.Rect(self.wights_mark_2[i][j][0] - margin_1,
                                               self.wights_mark_2[i][j][1],
                                               margin_1 + margin_2 + 1,
                                               height)

                            if rect.collidepoint(*mouse_pos):
                                self.cursor = [j, i]

                            if j != 0 and j != len(self.wights_mark_2[i]) - 1 and \
                                    self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j - 1][1]:
                                y = self.wights_mark_2[i][j][1]
                                x = 100
                                margin = (self.wights_mark_2[i][j][0] - x) / 2
                                rect_1 = pygame.Rect(x, y, margin + 1, height)
                                rect_2 = pygame.Rect(self.wights_mark_2[i][j][0] - margin,
                                                     self.wights_mark_2[i][j + 1][1],
                                                     margin + 1, height)
                                if rect_1.collidepoint(*mouse_pos):
                                    self.cursor = [j - 1, i]

                                if rect_2.collidepoint(*mouse_pos):
                                    self.cursor = [j, i]

                            if j == len(self.wights_mark_2[i]) - 1 or \
                                    self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j + 1][1]:
                                if self.wights_mark_2[i][j][1] <= mouse_pos[1] <= self.wights_mark_2[i][j][1] + \
                                        height and self.wights_mark_2[i][j][0] <= mouse_pos[0]:
                                    self.cursor = [j, i]

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

            if pygame.mouse.get_pressed(num_buttons=3)[0] and pygame.mouse.get_focused():
                if self.old_click[0]:
                    self.outline = {}
                    height = self.FONT.render("12", True, (0, 0, 0)).get_height() + self.margin_text
                    for n in [1, 2]:
                        pos = ()
                        if n == 1:
                            pos = pygame.mouse.get_pos()
                        if n == 2:
                            pos = self.old_click[1]

                        stop = False
                        if pos[1] < self.wights_mark_2[0][0][1]:
                            self.outline[(0, 0)] = True
                            continue
                        max_i = len(self.wights_mark_2) - 1
                        max_j = len(self.wights_mark_2[max_i]) - 1
                        if pos[1] > self.wights_mark_2[max_i][max_j][1] + height:
                            self.outline[(max_j, max_i)] = True
                            continue
                        for i in range(len(self.wights_mark_2)):
                            if stop:
                                break
                            for j in range(len(self.wights_mark_2[i])):
                                margin_1 = 0
                                margin_2 = 0
                                if j != 0:
                                    margin_1 = max((self.wights_mark_2[i][j][0] - self.wights_mark_2[i][j - 1][0]) / 2,
                                                   0)
                                if j != len(self.wights_mark_2[i]) - 1:
                                    margin_2 = max((self.wights_mark_2[i][j + 1][0] - self.wights_mark_2[i][j][0]) / 2,
                                                   0)

                                rect = pygame.Rect(self.wights_mark_2[i][j][0] - margin_1,
                                                   self.wights_mark_2[i][j][1],
                                                   margin_1 + margin_2 + 1,
                                                   height)

                                if rect.collidepoint(*pos):
                                    self.outline[(j, i)] = True
                                    stop = True
                                    break

                                if j != 0 and j != len(self.wights_mark_2[i]) - 1 and \
                                        self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j - 1][1]:
                                    y = self.wights_mark_2[i][j][1]
                                    x = 100
                                    margin = (self.wights_mark_2[i][j][0] - x) / 2
                                    rect_1 = pygame.Rect(x, y, margin + 1, height)
                                    rect_2 = pygame.Rect(self.wights_mark_2[i][j][0] - margin,
                                                         self.wights_mark_2[i][j + 1][1],
                                                         margin + 1, height)
                                    if rect_1.collidepoint(*pos):
                                        self.outline[(j - 1, i)] = True
                                        stop = True
                                        break

                                    if rect_2.collidepoint(*pos):
                                        self.outline[(j, i)] = True
                                        stop = True
                                        break

                                if j == len(self.wights_mark_2[i]) - 1 or \
                                        self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j + 1][1]:
                                    if self.wights_mark_2[i][j][1] <= pos[1] <= self.wights_mark_2[i][j][1] + \
                                            height and self.wights_mark_2[i][j][0] <= pos[0]:
                                        self.outline[(j, i)] = True
                                        stop = True
                                        break

                                if j == 0 or self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j - 1][1]:
                                    if self.wights_mark_2[i][j][1] <= pos[1] <= self.wights_mark_2[i][j][1] + \
                                            height and self.wights_mark_2[i][j][0] >= pos[0]:
                                        self.outline[(max(j - 1, 0), i)] = True
                                        stop = True
                                        break
                    keys = list(self.outline.keys())
                    if len(keys) > 1 and (
                            keys[0][1] > keys[1][1] or (keys[0][0] > keys[1][0] and keys[0][1] >= keys[1][1])):
                        self.outline = {keys[1]: True, keys[0]: True}
                self.old_click[0] = True
            else:
                self.old_click = [False, pygame.mouse.get_pos()]

        def draw(self, _screen):
            text = self.FONT.render("12", True, (0, 0, 0))

            for block in self.draw_blocks:
                _screen.blit(block[0], (block[1][0], block[1][1]))
            surf = pygame.Surface((1, text.get_height()))
            surf.fill(self.color_text)
            _screen.blit(surf, self.wights_mark_2[self.cursor[1]][self.cursor[0]])

            keys = list(self.outline.keys())
            if len(keys) > 1:
                extreme_angles = [self.wights_mark_2[keys[0][1]][keys[0][0]],
                                  self.wights_mark_2[keys[1][1]][keys[1][0]]]
                if extreme_angles[0][1] == extreme_angles[1][1]:
                    blue_surf = pygame.Surface((extreme_angles[1][0] - extreme_angles[0][0], text.get_height()))
                    blue_surf.set_colorkey((0, 0, 0))
                    blue_surf.fill((0, 0, 255))
                    blue_surf.set_alpha(100)
                    _screen.blit(blue_surf, extreme_angles[0])
                else:
                    start_pos = ()
                    draw = False
                    for i in range(len(self.wights_mark_2)):
                        for j in range(len(self.wights_mark_2[i])):
                            if (j, i) == keys[0]:
                                draw = True
                                start_pos = (j, i)
                            if (j, i) == keys[1]:
                                draw = False
                                blue_surf = pygame.Surface(
                                    (extreme_angles[1][0] - 100, text.get_height()))
                                blue_surf.set_colorkey((0, 0, 0))
                                blue_surf.fill((0, 0, 255))
                                blue_surf.set_alpha(100)
                                _screen.blit(blue_surf, [100, extreme_angles[1][1]])

                            if draw:
                                start_cell = self.wights_mark_2[start_pos[1]][start_pos[0]]
                                now_cell = self.wights_mark_2[i][j]
                                next_cell = now_cell
                                new_line = False
                                if j + 1 >= len(self.wights_mark_2[i]):
                                    new_line = True
                                else:
                                    next_cell = self.wights_mark_2[i][j + 1]

                                if new_line or start_cell[1] != next_cell[1]:
                                    if extreme_angles[0][1] != now_cell[1]:
                                        blue_surf = pygame.Surface(
                                            (now_cell[0] - 100, text.get_height()))
                                        blue_surf.set_colorkey((0, 0, 0))
                                        blue_surf.fill((0, 0, 255))
                                        blue_surf.set_alpha(100)
                                        _screen.blit(blue_surf, [100, start_cell[1]])
                                    else:
                                        blue_surf = pygame.Surface(
                                            (now_cell[0] - start_cell[0], text.get_height()))
                                        blue_surf.set_colorkey((0, 0, 0))
                                        blue_surf.fill((0, 0, 255))
                                        blue_surf.set_alpha(100)
                                        _screen.blit(blue_surf, start_cell)

                                    if not new_line:
                                        start_pos = (j + 1, i)

            return _screen

    pygame.display.set_caption("Мессанджер")
    screen = pygame.display.set_mode((500, 400))

    clock = pygame.time.Clock()

    text_aria = TextAria((100, 350), 300)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            text_aria.handle_event(event)
        screen.fill((30, 30, 30))
        text_aria.update()

        screen = text_aria.draw(screen)
        pygame.display.flip()
        clock.tick(30)
