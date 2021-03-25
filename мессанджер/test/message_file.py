import pygame


# from class_ import *


def start():
    pygame.init()



    pygame.display.set_caption("Мессанджер")
    screen = pygame.display.set_mode((500, 400))

    clock = pygame.time.Clock()

    text_aria = TextAria((100, 400), 300)

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
