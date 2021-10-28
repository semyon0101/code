import math
import pygame
import sys
import numpy as np
import numba

size = [1000, 500]

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
        return (pos_object[0] - pos_player[0]) * 1000 + size[0] / 2, \
               (pos_object[2] - pos_player[2]) * 1000 + size[1] / 2, False
    if pos_object[1] - pos_player[1] < 0:
        return (pos_object[0] - pos_player[0]) * 1000*max((-pos_object[1] + pos_player[1]) / 4, 1) + size[0] / 2, \
               (pos_object[2] - pos_player[2]) * 1000*max((-pos_object[1] + pos_player[1]) / 4, 1) + size[1] / 2, True

    xa = (pos_object[0] - pos_player[0]) / max((pos_object[1] - pos_player[1]) / 4, 0.1)
    ya = (pos_object[2] - pos_player[2]) / max((pos_object[1] - pos_player[1]) / 4, 0.1)

    x = size[0] / 2 + xa * 100
    y = size[1] / 2 + ya * 100
    return x, y, False


pygame.init()
screen = pygame.display.set_mode(size)
# obj = [np.array([x, y, z], np.float_) for x in [0, 1] for y in [0, 1] for z in [0, 1]]

vertex, faces = get_object_from_file('resources/t_34_obj.obj')
pos_pl = np.array([-1, -5, 0], np.float_)
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
        answer = get_pos_in_2d_plane(np.array(pos_pl, np.float_),
                                     np.array(pos_obj, np.float_),
                                     x_angle, y_angle, np.array(size))

        arr2D.append(answer)

    for face in faces:
        arr = [arr2D[i] for i in face]
        a = True
        for i in range(len(arr)):
            if not arr[i][2]:
                a = False
            arr[i] = arr[i][:2]
        if a:
            continue

        pygame.draw.polygon(screen, [255, 255, 255], arr, 1)

    pygame.display.update()
    screen.fill((0, 0, 0))

    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
