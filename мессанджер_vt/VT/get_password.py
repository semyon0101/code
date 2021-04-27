import pygame
from class_ import *
import connected_user.user as db

def start():
    pygame.init()
    pygame.display.set_caption("Вход в VT")
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()
    input_box1 = InputBox((100, 120, 0, 32), max_length=15, hidden_text="логин", copy=False)
    input_box2 = InputBox((100, 205, 0, 32), max_length=15, hidden_text="пароль", copy=False)
    input_box1.text = db.db.get_text()[0][0]
    input_box2.text = db.db.get_text()[0][1]

    button = Button((200, 290, 71, 34), "войти")
    text1 = Text((140, 160), 220,
                 "У логин минимальная длина 3 знака. Максимальная длина 15 знаков.")
    text2 = Text((140, 245), 220,
                 "У пароля минимальная длина 3 знака. Максимальная длина 15 знаков.")
    overflow = OverFlow((0, 0, 500, 500))
    overflow.add(button, text1, text2, input_box1, input_box2)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return None
            if overflow.handle_event(event) and len(input_box1.text)>=3 and len(input_box2.text)>=3:
                return input_box1.text, input_box2.text
        overflow.update()
        screen.fill((0, 0, 0))

        screen = overflow.draw(screen)
        pygame.display.flip()
        clock.tick(30)

