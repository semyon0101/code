import math
import pygame
import sys
import numpy as np
import numba

size = np.array([1500, 1000])

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
    return np.array(vertex), faces


def normalise(_arr, size):
    new_arr = []
    a = True
    for i in range(len(_arr)):
        if not _arr[i][2]:
            a = False
    if a:
        return None

    for i in range(len(_arr)):
        x, y, b = _arr[i]
        if not b:
            new_arr.append([x, y])
        else:
            if not _arr[(i - 1) % len(_arr)][2]:
                x1, y1 = _arr[(i - 1) % len(_arr)][:2]
                x2, y2 = (x1 - size[0] / 2 + x - size[0] / 2) / 2, (y1 - size[1] / 2 + y - size[1] / 2) / 2
                new_arr.append([x2 * 1000 + size[0] / 2, y2 * 1000 + size[1] / 2])
            if not _arr[(i + 1) % len(_arr)][2]:
                x1, y1 = _arr[(i + 1) % len(_arr)][:2]
                x2, y2 = (x1 - size[0] / 2 + x - size[0] / 2) / 2, (y1 - size[1] / 2 + y - size[1] / 2) / 2
                new_arr.append([x2 * 1000 + size[0] / 2, y2 * 1000 + size[1] / 2])

    return new_arr


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
                        x_angle, y_angle, size):
    pos_object = rotate(x_angle, y_angle, pos_object, pos_player)
    if (pos_object[1] - pos_player[1]) == 0:
        return (pos_object[0] - pos_player[0]) * 10000 + size[0] / 2, \
               (pos_object[2] - pos_player[2]) * 10000 + size[1] / 2, False

    xa = (pos_object[0] - pos_player[0]) / (max(abs(pos_object[1] - pos_player[1]), 0.01) / 4)
    ya = (pos_object[2] - pos_player[2]) / (max(abs(pos_object[1] - pos_player[1]), 0.01) / 4)

    x = size[0] / 2 + xa * 100
    y = size[1] / 2 + ya * 100
    return x, y, pos_object[1] - pos_player[1] < 0


pygame.init()
screen = pygame.display.set_mode(size)

vertex, faces = get_object_from_file('resources/t_34_obj.obj')
pos_pl = np.array([0.5, 0.5, -0.35], np.float_)
# vertex = [
#     [1, -1, -1],
#     [1, 1, -1],
#     [-1, 1, -1],
#     [-1, -1, -1],
#     [1, -1, 1],
#     [1, 1, 1],
#     [-1, -1, 1],
#     [-1, 1, 1],
#     [-1, -1, -1],
#     [-1, 1, -1],
#     [-3, 1, -1],
#     [-3, -1, -1],
#     [-1, -1, 1],
#     [-1, 1, 1],
#     [-3, -1, 1],
#     [-3, 1, 1]
# ]
# faces = [
#     [0, 1],
#     [0, 3],
#     [0, 4],
#     [2, 1],
#     [2, 3],
#     [2, 7],
#     [6, 3],
#     [6, 4],
#     [6, 7],
#     [5, 1],
#     [5, 4],
#     [5, 7],
#     [0 + 8, 1 + 8],
#     [0 + 8, 3 + 8],
#     [0 + 8, 4 + 8],
#     [2 + 8, 1 + 8],
#     [2 + 8, 3 + 8],
#     [2 + 8, 7 + 8],
#     [6 + 8, 3 + 8],
#     [6 + 8, 4 + 8],
#     [6 + 8, 7 + 8],
#     [5 + 8, 1 + 8],
#     [5 + 8, 4 + 8],
#     [5 + 8, 7 + 8]
# ]
# vertex = [
#     [0, 0, 0],
#     [0, 1, 0],
#     [1, 1, 0],
#     [1, 0, 0],
# ]
# faces = [
#     [0, 1, 2, 3]
# ]
# faces = [
#     [0, 1],
#     [1, 2],
#     [2, 3],
#     [3, 0]
# ]
x_angle, y_angle = -90, -30
now_pos = [None, None]
while True:
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
            np.array([-speed, 0, 0], np.float_), np.array([0, 0, 0], np.float_))
        pos_pl += left
    if keys[pygame.K_d]:
        right = rotate(
            -x_angle, 0,
            np.array([speed, 0, 0], np.float_), np.array([0, 0, 0], np.float_))
        pos_pl += right
    if keys[pygame.K_s]:
        back = rotate(
            0, -y_angle,
            np.array([0, -speed, 0], np.float_), np.array([0, 0, 0], np.float_))
        back = rotate(
            -x_angle, 0,
            back, np.array([0, 0, 0], np.float_))
        pos_pl += back
    if keys[pygame.K_w]:
        forward = rotate(
            0, -y_angle,
            np.array([0, speed, 0], np.float_), np.array([0, 0, 0], np.float_))
        forward = rotate(
            -x_angle, 0,
            forward, np.array([0, 0, 0], np.float_))
        pos_pl += forward
    if keys[pygame.K_e]:
        down = rotate(
            0, -y_angle,
            np.array([0, 0, speed], np.float_), np.array([0, 0, 0], np.float_))
        down = rotate(
            -x_angle, 0,
            down, np.array([0, 0, 0], np.float_))
        pos_pl += down
    if keys[pygame.K_q]:
        up = rotate(
            0, -y_angle,
            np.array([0, 0, -speed], np.float_), np.array([0, 0, 0], np.float_))
        up = rotate(
            -x_angle, 0,
            up, np.array([0, 0, 0], np.float_))
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
        arr2D.append(
            get_pos_in_2d_plane(pos_pl,
                                pos_obj.copy(),
                                x_angle, y_angle, size)
        )

    for face in faces:
        answer = normalise([arr2D[i] for i in face], size)
        if answer:
            pygame.draw.polygon(screen, [255, 255, 255], answer, 1)

    pygame.display.update()
    screen.fill((0, 0, 0))

    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
