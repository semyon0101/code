import pygame
from самолёт.config import *
from самолёт.meny.class_ import *
import самолёт.meny.levels.levels as levels
def f(overflow, max_open_lvl):
    size_button = [50, 50]
    max_i = 0
    j = 0
    for i in range(len(levels.get_all_levels())):
        i1 = i
        if not max_i and 10 + (10 + size_button[0]) * (i + 1) > size[0]:
            max_i = i
        if max_i:
            j = i // max_i
            i1 = i % max_i
        if i <= max_open_lvl:
            btn = Button(pygame.Rect([10 + (10 + size_button[0]) * i1, 10 + (10 + size_button[0]) * j, *size_button]),
                         str(i + 1), i + 1)
        else:
            btn = Button(pygame.Rect([10 + (10 + size_button[0]) * i1, 10 + (10 + size_button[0]) * j, *size_button]),
                         str(i + 1), False, COLOR_ACTIVE=(190, 100,100), COLOR_INACTIVE=(130, 100, 100))
        overflow.add(btn)
    return overflow

def start():
    pygame.init()
    pygame.display.set_caption("meny")
    overflow = OverFlow(pygame.Rect([0, 0, *size]))
    max_open_lvl = 0
    player_xp = 0

    overflow = f(overflow, max_open_lvl)
    clock = pygame.time.Clock()
    stop = False
    i = None
    while not stop:
        _screen = pygame.display.set_mode(size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            i = overflow.handle_event(event)

        overflow.update()

        _screen = overflow.draw(_screen)
        pygame.display.flip()
        clock.tick(30)
        if i:
            m = int(i) - 1
            while True:
                answer = levels.start_level(m, player_xp)

                if answer[0] == "next level":
                    m += 1
                    max_open_lvl +=1
                    overflow = f(overflow, max_open_lvl)
                elif answer[0] == "go to menu":
                    break
                elif answer[0] == "restart":
                    continue
                elif answer[0] == "go to menu, you win":
                    max_open_lvl += 1
                    overflow = f(overflow, max_open_lvl)
                    break
                else:
                    pygame.quit()
                    return
                player_xp += answer[1]
                pygame.init()
