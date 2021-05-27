from машина.car.car import *
from машина.more.config import *
import pygame
import sys

pygame.init()

clock = pygame.time.Clock()

cars = [Car() for _ in range(50)]

level_surf = level()
while True:
    pygame.display.set_caption(str(clock.get_fps()))
    _screen = pygame.display.set_mode(size)
    _screen.fill((60, 160, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    for car in cars:
        car.update()
    _screen.blit(level_surf, [0, 0])
    pygame.draw.rect(_screen, (255, 255, 255), [300, 505, 50, 95])

    for car in cars:
        _screen = car.draw(_screen)

    draw = True
    if draw:
        surf = font.render(str(int(cars[0].fitnessAI)), True, (0, 0, 0))
        _screen.blit(surf, [745, 10])

    pygame.display.flip()
    clock.tick(120)
