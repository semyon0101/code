import math
import pygame
import sys

size = [500, 500]
x_fov_d = 120
y_fov_d = size[1] / (size[0] / x_fov_d)

x_fov_r = math.radians(x_fov_d)
y_fov_r = math.radians(y_fov_d)


def get_pos_in_2d_plane(pos_player: [float, float, float], pos_object: [float, float, float]):
    x_r_angle = math.atan2(pos_object[0] - pos_player[0], pos_object[2] - pos_player[2])
    y_r_angle = math.atan2(pos_object[1] - pos_player[1], pos_object[2] - pos_player[2])
    if pos_object==[1,1,1]:
        print(math.degrees(x_r_angle))
        print(pos_object)
    if -x_fov_r/2 <= x_r_angle <= x_fov_r/2 and -y_fov_r/2 <= y_r_angle <= y_fov_r/2:
        x = size[0] / 2 + x_r_angle * (size[0] / x_fov_r)
        y = size[1] / 2 + y_r_angle * (size[1] / y_fov_r)
        return x, y
    return None


pygame.init()
screen = pygame.display.set_mode(size)
obj = [[x, y, z] for x in [0, 1] for y in [0, 1] for z in [0, 1]]

pos_pl = [0, 0, 0]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        pos_pl[0] -= 0.01
    if keys[pygame.K_d]:
        pos_pl[0] += 0.01
    if keys[pygame.K_s]:
        pos_pl[2] -= 0.01
    if keys[pygame.K_w]:
        pos_pl[2] += 0.01
    if keys[pygame.K_e]:
        pos_pl[1] -= 0.01
    if keys[pygame.K_q]:
        pos_pl[1] += 0.01


    for pos_obj in obj:
        answer = get_pos_in_2d_plane(pos_pl, pos_obj)
        if not answer is None:
            pygame.draw.circle(screen, (255, 255, 255), answer, 3)
            if pos_obj==[1,1,1]:
                pygame.draw.circle(screen, (255, 0, 0), answer, 3)

    pygame.display.update()
    screen.fill((0, 0, 0))
