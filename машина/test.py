import pygame
import sys

pygame.init()

size = [500, 500]
surf = pygame.Surface(size)


def in_trangal(point: list, t1: list, t2: list, t3: list):
    [xa, ya] = t1
    [xb, yb ] = t2
    [xc, yc] = t3
    [xd, yd] = point
    return (((xd - xa) * (yb - ya) - (yd - ya) * (xb - xa)) * ((xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)) >= 0) and\
    (((xd - xb) * (yc - yb) - (yd - yb) * (xc - xb)) * ((xa - xb) * (yc - yb) - (ya - yb) * (xc - xb)) >= 0) and\
    (((xd - xc) * (ya - yc) - (yd - yc) * (xa - xc)) * ((xb - xc) * (ya - yc) - (yb - yc) * (xa - xc)) >= 0)



point1 = [291, 274]
point2 = [187, 124]
point3 = [374, 99]
for x in range(size[0]):
    for y in range(size[1]):
        if in_trangal([x, y], point1, point2, point3):
            surf1 = pygame.Surface((1, 1))
            surf1.fill((255, 255, 255))
            surf.blit(surf1, [x, y])
print("end")
while True:
    screen = pygame.display.set_mode(size)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    screen.blit(surf, [0, 0])
    pygame.draw.circle(screen, (255, 0, 0), point1, 5)
    pygame.draw.circle(screen, (0, 255, 0), point2, 5)
    pygame.draw.circle(screen, (0, 0, 255), point3, 5)
    pygame.display.flip()
