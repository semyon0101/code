import pygame
from class_ import *


# import connected_user.user as user

def start():
    pygame.init()
    pygame.display.set_caption("Вход")
    screen = pygame.display.set_mode((500, 400))

    clock = pygame.time.Clock()
    input_box1 = InputBox((100, 120, 0, 32), max_length=15, hidden_text="логин")
    input_box2 = InputBox((100, 205, 0, 32), max_length=15, hidden_text="пароль", copy=False, special_symbol=False)

    def a():
        print(input_box1.text, input_box2.text)
        # user.user(nike=input_box1.text,password=input_box2.text,command="")

    button = Button((200, 290, 71, 34), "войти", a)
    text1 = Text((140, 160), 220,
                 "У логин минимальная длина 3 знака. Максимальная длина 15 знаков.")
    text2 = Text((140, 245), 220,
                 "Пароль не может иметь пробелов и спец символов. Минимальная длина 3 знака. Максимальная длина 15 знаков.")
    overflow = OverFlow((0, 0, 500, 500))
    overflow.add(button, text1, text2, input_box1, input_box2)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return True
            overflow.handle_event(event)
        overflow.update()
        screen.fill((30, 30, 30))

        screen = overflow.draw(screen)
        pygame.display.flip()
        clock.tick(30)
