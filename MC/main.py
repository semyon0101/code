import math
import pygame
import sys
import numpy as np
import numba
from datetime import datetime

size = [1000, 500]
x_fov_d = 180
y_fov_d = size[1] / (size[0] / x_fov_d)
if_display_is_circled = True

x_fov_r = math.radians(x_fov_d)
y_fov_r = math.radians(y_fov_d)

clock = pygame.time.Clock()

speed = 0.5


def get_object_from_file(filename):
    vertex, faces = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                vertex.append(
                    list(
                        rotate(0, -90, np.array([float(i) for i in line.split()[1:]]), np.array([0, 0, 0])
                               )
                    )
                )
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
    return vertex, faces


@numba.njit(fastmath=True)
def get_plane_pos_by_circled_pos2(x_ang, y_ang):
    x = x_ang/math.pi*2
    if math.cos(x_ang) > math.cos(y_ang):
        x = math.sin(x_ang)
    y = y_ang/math.pi*2
    if math.cos(y_ang) > math.cos(x_ang):
        y = math.sin(y_ang)
    return x, y


@numba.njit(fastmath=True)
def get_plane_pos_by_circled_pos1(x, y):
    if x == 0 or y == 0:
        return x, y
    r1 = min(math.sqrt(1 + (1 / x * y) ** 2), math.sqrt(1 + (1 / y * x) ** 2))
    r2 = math.sqrt(x ** 2 + y ** 2)
    new_x, new_y = x * (r1 / r2) * r2, y * (r1 / r2) * r2
    return new_x, new_y


@numba.njit(fastmath=True)
def get_plane_pos_by_circled_pos(x_ang, y_ang):
    x_ang *= 70 / 90
    y_ang *= 70 / 90
    x, y = math.sin(x_ang) * math.cos(y_ang), math.sin(y_ang) * math.cos(x_ang)
    if x == 0 or y == 0:
        return x, y
    return x / math.cos(x_ang) * math.cos(y_ang), y / math.cos(y_ang) * math.cos(x_ang)


@numba.njit(fastmath=True)
def matmul(A, B):
    C = np.array([0.0, 0.0, 0.0])
    for i in range(3):
        for j in range(3):
            C[i] += B[j][i] * A[j]
    return C


@numba.njit(fastmath=True)
def get_m(x: float, y: float):
    x = math.radians(x)
    y = math.radians(y)
    return np.array([
        [
            math.cos(x),
            math.sin(x) * math.cos(y),
            math.sin(x) * math.sin(y)
        ],
        [
            -math.sin(x),
            math.cos(x) * math.cos(y),
            math.cos(x) * math.sin(y)
        ],
        [
            0,
            -math.sin(y),
            math.cos(y)
        ]
    ])


@numba.njit(fastmath=True)
def rotate(x, y,
           pos: np.array([float, float, float]),
           center: np.array([float, float, float])) -> np.array([float, float, float]):
    pos -= center
    pos = matmul(pos, get_m(x, y))
    pos += center
    return pos


@numba.njit(fastmath=True)
def get_pos_in_2d_plane(pos_player: np.array([float, float, float]),
                        pos_object: np.array([float, float, float]),
                        x_angle, y_angle, size, x_fov_r, y_fov_r, if_display_is_circled):
    pos_object = rotate(x_angle, y_angle, pos_object, pos_player)
    x_r_angle = math.atan2(pos_object[0] - pos_player[0], pos_object[1] - pos_player[1])
    y_r_angle = math.atan2(pos_object[2] - pos_player[2],
                           math.sqrt(
                               (pos_object[1] - pos_player[1]) ** 2
                           ))
    if if_display_is_circled:
        x, y = get_plane_pos_by_circled_pos2(x_r_angle, y_r_angle)
        x = size[0] / 2 + x * math.pi / 2 * (size[0] / x_fov_r)
        y = size[1] / 2 + y * math.pi / 2 * (size[1] / y_fov_r)
    else:
        if math.radians(-90) <= x_r_angle <= math.radians(90) and \
                math.radians(-90) <= y_r_angle <= math.radians(90):
            xa = math.sin(x_r_angle) * math.cos(y_r_angle)
            ya = math.sin(y_r_angle) * math.cos(x_r_angle)
            x, y = get_plane_pos_by_circled_pos(x_r_angle, y_r_angle)
            print(xa, ya, x, y)
            x = size[0] / 2 + x * (size[0] / x_fov_r)
            y = size[1] / 2 + y * (size[1] / y_fov_r)
        else:
            x = size[0] / 2 + x_r_angle * (size[0] / x_fov_r)
            y = size[1] / 2 + y_r_angle * (size[1] / y_fov_r)

    return x, y
    # if -x_fov_r / 2 <= x_r_angle <= x_fov_r / 2 and -y_fov_r / 2 <= y_r_angle <= y_fov_r / 2:
    #     x = size[0] / 2 + x_r_angle * (size[0] / x_fov_r)
    #     y = size[1] / 2 + y_r_angle * (size[1] / y_fov_r)
    #     return x, y
    # return None


pygame.init()
screen = pygame.display.set_mode(size)
# obj = [np.array([x, y, z], np.float) for x in [0, 1] for y in [0, 1] for z in [0, 1]]

# vertex, faces = get_object_from_file('resources/t_34_obj.obj')
# vertex, faces=[[0,1,0]], [[0,0]]
pos_pl = np.array([-1, -5, 0], np.float)
vertex = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1],
    [-1, -1, -1],
    [-1, 1, -1],
    [-3, 1, -1],
    [-3, -1, -1],
    [-1, -1, 1],
    [-1, 1, 1],
    [-3, -1, 1],
    [-3, 1, 1]
]
faces = [
    [0, 1],
    [0, 3],
    [0, 4],
    [2, 1],
    [2, 3],
    [2, 7],
    [6, 3],
    [6, 4],
    [6, 7],
    [5, 1],
    [5, 4],
    [5, 7],
    [0 + 8, 1 + 8],
    [0 + 8, 3 + 8],
    [0 + 8, 4 + 8],
    [2 + 8, 1 + 8],
    [2 + 8, 3 + 8],
    [2 + 8, 7 + 8],
    [6 + 8, 3 + 8],
    [6 + 8, 4 + 8],
    [6 + 8, 7 + 8],
    [5 + 8, 1 + 8],
    [5 + 8, 4 + 8],
    [5 + 8, 7 + 8]
]
x_angle, y_angle = 0, 0
now_pos = [None, None]
while True:
    # print(x_angle, y_angle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    y_angle = max(-90, min(90, y_angle))
    x_angle = x_angle % 360
    if keys[pygame.K_a]:
        left = rotate(
            -x_angle, 0,
            np.array([-speed, 0, 0], np.float), np.array([0, 0, 0], np.float))
        pos_pl += left
    if keys[pygame.K_d]:
        right = rotate(
            -x_angle, 0,
            np.array([speed, 0, 0], np.float), np.array([0, 0, 0], np.float))
        pos_pl += right
    if keys[pygame.K_s]:
        back = rotate(
            0, -y_angle,
            np.array([0, -speed, 0], np.float), np.array([0, 0, 0], np.float))
        back = rotate(
            -x_angle, 0,
            back, np.array([0, 0, 0], np.float))
        pos_pl += back
    if keys[pygame.K_w]:
        forward = rotate(
            0, -y_angle,
            np.array([0, speed, 0], np.float), np.array([0, 0, 0], np.float))
        forward = rotate(
            -x_angle, 0,
            forward, np.array([0, 0, 0], np.float))
        pos_pl += forward
    if keys[pygame.K_e]:
        down = rotate(
            0, -y_angle,
            np.array([0, 0, speed], np.float), np.array([0, 0, 0], np.float))
        down = rotate(
            -x_angle, 0,
            down, np.array([0, 0, 0], np.float))
        pos_pl += down
    if keys[pygame.K_q]:
        up = rotate(
            0, -y_angle,
            np.array([0, 0, -speed], np.float), np.array([0, 0, 0], np.float))
        up = rotate(
            -x_angle, 0,
            up, np.array([0, 0, 0], np.float))
        pos_pl += up

    if pygame.mouse.get_pressed(3)[0]:
        if now_pos == [None, None]:
            now_pos = pygame.mouse.get_pos()
        else:
            x_angle += (now_pos[0] - pygame.mouse.get_pos()[0]) * 0.2
            y_angle -= (now_pos[1] - pygame.mouse.get_pos()[1]) * 0.2
            now_pos = pygame.mouse.get_pos()
    else:
        now_pos = [None, None]

    arr2D = []
    for pos_obj in vertex:
        answer = get_pos_in_2d_plane(np.array(pos_pl, np.float),
                                     np.array(pos_obj, np.float),
                                     x_angle, y_angle, np.array(size),
                                     x_fov_r, y_fov_r, if_display_is_circled)
        arr2D.append(answer)
    for face in faces:
        pygame.draw.polygon(screen, [255, 255, 255], [arr2D[i] for i in face], 1)

    pygame.display.update()
    screen.fill((0, 0, 0))

    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
