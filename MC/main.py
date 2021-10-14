import math
import pygame
import sys
import numpy as np

size = [500, 500]
x_fov_d = 120
y_fov_d = size[1] / (size[0] / x_fov_d)

x_fov_r = math.radians(x_fov_d)
y_fov_r = math.radians(y_fov_d)


def rot(pos_object: [float, float, float], pos_player: [float, float, float], x_angle, y_angle):
    pos_object = pos_object.copy()
    pos_object[0] -= pos_player[0]
    pos_object[1] -= pos_player[1]
    pos_object[2] -= pos_player[2]

    if pos_object[0] == 0 and pos_object[1] == 0 and pos_object[2] == 0:
        return pos_player[0], pos_player[1], pos_player[2]

    angle = math.atan2(pos_object[1], pos_object[0])
    r_x_y = math.sqrt(pos_object[0] ** 2 + pos_object[1] ** 2)
    new_pos = [r_x_y * math.cos(math.radians(x_angle) + angle),
               r_x_y * math.sin(math.radians(x_angle) + angle),
               pos_object[2]]
    x_per = 0
    y_per = 1
    angle_2 = math.atan2(new_pos[2], math.sqrt(new_pos[0] ** 2 + new_pos[1] ** 2))
    if not (pos_object[0] == 0 and pos_object[1] == 0):
        x_per = new_pos[0] / (new_pos[0] + new_pos[1])
        y_per = new_pos[1] / (new_pos[0] + new_pos[1])

    r_x_y_z = math.sqrt(new_pos[0] ** 2 + new_pos[1] ** 2 + new_pos[2] ** 2)
    new_pos_1 = [
        math.sqrt(round(
            ((r_x_y_z * math.cos(math.radians(y_angle) + angle_2)) ** 2) * x_per, 12)),
        math.sqrt(round(
            ((r_x_y_z * math.cos(math.radians(y_angle) + angle_2)) ** 2) * y_per, 12)),
        r_x_y_z * math.sin(math.radians(y_angle) + angle_2)]
    return [new_pos_1[0] + pos_player[0], new_pos_1[1] + pos_player[1], new_pos_1[2] + pos_player[2]]


def rotate_test(x, y, z, pos):
    x = math.radians(x)
    y = math.radians(y)
    z = math.radians(z)
    M = np.array([
        np.array([
            math.cos(x) * math.cos(z) - math.sin(x) * math.cos(y) * math.sin(z),
            math.cos(x) * math.sin(z) + math.sin(x) * math.cos(y) * math.cos(z),
            math.sin(x) * math.sin(y)
        ]),
        np.array([
            -math.sin(x) * math.cos(z) - math.cos(x) * math.cos(y) * math.sin(z),
            -math.sin(x) * math.sin(z) + math.cos(x) * math.cos(y) * math.cos(z),
            math.cos(x) * math.sin(y)
        ]),
        np.array([
            math.sin(y) * math.sin(z),
            -math.sin(y) * math.cos(z),
            math.cos(y)
        ])
    ])
    return pos @ M


def rotate(x, y, z, pos, center):
    pos -= center
    pos = rotate_test(90, x, 0, pos)
    pos = rotate_test(-90, 0, 0, pos)
    pos = rotate_test(0, y, z, pos)
    pos += center
    return pos


def get_pos_in_2d_plane(pos_player: [float, float, float], pos_object: [float, float, float], x_angle, y_angle):
    # print(pos_object, pos_player, x_angle, y_angle)

    pos_object = list(rotate(x_angle, y_angle, 0, np.array(pos_object, np.float), np.array(pos_player, np.float)))
    # print(pos_object)
    x_r_angle = math.atan2(pos_object[0] - pos_player[0], pos_object[2] - pos_player[2])
    y_r_angle = math.atan2(pos_object[1] - pos_player[1], pos_object[2] - pos_player[2])

    if -x_fov_r / 2 <= x_r_angle <= x_fov_r / 2 and -y_fov_r / 2 <= y_r_angle <= y_fov_r / 2:
        x = size[0] / 2 + x_r_angle * (size[0] / x_fov_r)
        y = size[1] / 2 + y_r_angle * (size[1] / y_fov_r)
        return x, y
    return None


pygame.init()
screen = pygame.display.set_mode(size)
obj = [np.array([x, y, z]) for x in [0, 1] for y in [0, 1] for z in [0, 1]]

pos_pl = np.array([0, 0, 0])

x_angle, y_angle = 0, 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        #left = rotate(x_angle, y_angle, 0, np.array([0,-1,0]), np.array(pos_pl))
        pos_pl[0] -= 0.01
        print(pos_pl[0])
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
    if keys[pygame.K_RIGHT]:
        x_angle -= 0.1
    if keys[pygame.K_LEFT]:
        x_angle += 0.1
    if keys[pygame.K_UP]:
        y_angle -= 0.1
    if keys[pygame.K_DOWN]:
        y_angle += 0.1

    for pos_obj in obj:
        answer = get_pos_in_2d_plane(pos_pl, pos_obj, x_angle, y_angle)

        if not answer is None:
            pygame.draw.circle(screen, (255, 255, 255), answer, 3)


    pygame.display.update()
    screen.fill((0, 0, 0))
