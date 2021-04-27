import pygame
import connected_user.user as db
from class_ import *


def start():
    pygame.init()

    pygame.display.set_caption("VT")
    screen = pygame.display.set_mode((1000, 800))

    clock = pygame.time.Clock()

    text_aria = TextAria((100, 750), 800)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            text = text_aria.handle_event(event)
            if text:
                answer = db.user(command=f"spend_message: 0, {text}")
                if answer != b"message is open":
                    print(answer)
                else:
                    text_aria.text = ""
                    text_aria.draw_blocks = []
                    text_aria.good_text = [""]
                    text_aria.wights_mark = []
                    text_aria.wights_mark_2 = []
                    text_aria.cursor = [0, 0]
                    text_aria.old_click = [False, pg.mouse.get_pos()]
                    text_aria.outline = {}
                    text_aria.update()
                    print(db.user(command="open_server: 0"))
        screen.fill((30, 30, 30))
        text_aria.update()

        screen = text_aria.draw(screen)
        pygame.display.flip()
        clock.tick(30)
