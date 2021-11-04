import math
import pygame
import sys
import numpy as np
import numba

size = np.array([1000, 500])

clock = pygame.time.Clock()

speed = 0.5

fast_mode = False


def get_object_from_file(filename):
    _vertex, _faces = [], []
    with open(filename) as f:
        m = 0
        for line in f:
            if line.startswith('v '):
                _vertex.append(
                    list(
                        rotate(0, -90, np.array([float(i) for i in line.split()[1:]]), np.array([0, 0, 0])
                               )
                    )
                )
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                _arr = [int(face_.split('/')[0]) - 1 for face_ in faces_]
                _faces.append(_arr)
                if m < len(_arr):
                    m = len(_arr)
    faces_2 = np.zeros([len(_faces), m])
    for i in range(len(_faces)):
        face = _faces[i]
        for j in range(m):
            if len(face) > j:
                faces_2[i][j] = face[j]
            else:
                faces_2[i][j] = -1
    return np.array(_vertex), faces_2


@numba.njit(fastmath=True)
def normalise(_arr, _size):
    new_arr = []
    a = True
    for i in range(len(_arr)):
        if not bool(_arr[i][2]):
            a = False
    if a:
        return [[0.0, 0.0]], False

    for i in range(len(_arr)):
        x, y, b = _arr[i]
        if not bool(b):
            new_arr.append([x, y])
        else:
            if not _arr[(i - 1) % len(_arr)][2]:
                x1, y1 = _arr[(i - 1) % len(_arr)][:2]
                x2, y2 = (x1 - _size[0] / 2 + x - _size[0] / 2) / 2, (y1 - _size[1] / 2 + y - _size[1] / 2) / 2
                new_arr.append([x2 * 1000 + _size[0] / 2, y2 * 1000 + _size[1] / 2])
            if not _arr[(i + 1) % len(_arr)][2]:
                x1, y1 = _arr[(i + 1) % len(_arr)][:2]
                x2, y2 = (x1 - _size[0] / 2 + x - _size[0] / 2) / 2, (y1 - _size[1] / 2 + y - _size[1] / 2) / 2
                new_arr.append([x2 * 1000 + _size[0] / 2, y2 * 1000 + _size[1] / 2])

    return new_arr, True


@numba.njit(fastmath=True)
def rotate(_x_angle, _y_angle,
           _pos: np.array([float, float, float]),
           center: np.array([float, float, float])) -> np.array([float, float, float]):
    _x_angle = math.radians(_x_angle)
    _y_angle = math.radians(_y_angle)

    _pos -= center

    r_x_y = math.sqrt(_pos[1] ** 2 + _pos[0] ** 2)
    _x_angle += math.atan2(_pos[1], _pos[0])
    _pos[0] = r_x_y * math.cos(_x_angle)
    _pos[1] = r_x_y * math.sin(_x_angle)

    _y_angle += math.atan2(_pos[2], _pos[1])
    r_y_z = math.sqrt(_pos[1] ** 2 + _pos[2] ** 2)
    _pos[1] = r_y_z * math.cos(_y_angle)
    _pos[2] = r_y_z * math.sin(_y_angle)

    _pos += center
    return _pos


@numba.njit(fastmath=True)
def get_pos_in_2d_plane(pos_player: np.array([float, float, float]), _x_angle, _y_angle,
                        _size, _vertex, _faces, _fast_mode):
    _x_angle = math.radians(_x_angle)
    _y_angle = math.radians(_y_angle)
    _arr2D = []
    for pos_object in _vertex:
        _x_angle2 = _x_angle
        _y_angle2 = _y_angle
        pos_object -= pos_player

        r_x_y = math.sqrt(pos_object[1] ** 2 + pos_object[0] ** 2)
        _x_angle2 += math.atan2(pos_object[1], pos_object[0])
        pos_object[0] = r_x_y * math.cos(_x_angle2)
        pos_object[1] = r_x_y * math.sin(_x_angle2)

        _y_angle2 += math.atan2(pos_object[2], pos_object[1])
        r_y_z = math.sqrt(pos_object[1] ** 2 + pos_object[2] ** 2)
        pos_object[1] = r_y_z * math.cos(_y_angle2)
        pos_object[2] = r_y_z * math.sin(_y_angle2)

        if (pos_object[1]) == 0:
            _arr2D.append([(pos_object[0]) * 10000 + _size[0] / 2,
                          (pos_object[2]) * 10000 + _size[1] / 2, False])

        xa = (pos_object[0]) / (max(abs(pos_object[1]), 0.01) / 4)
        ya = (pos_object[2]) / (max(abs(pos_object[1]), 0.01) / 4)

        _arr2D.append([_size[0] / 2 + xa * 100,
                      _size[1] / 2 + ya * 100,
                      pos_object[1] < 0])

    _arr = []
    for face in _faces:
        buffer = []
        for i in face:
            if i != -1:
                buffer.append(_arr2D[int(i)])
            else:
                break
        arr2, b = normalise(buffer, _size)
        if _fast_mode:
            if b and [0 <= x <= _size[0] and 0 <= y <= _size[1] for x, y in arr2].count(True):
                _arr.append(arr2)
        else:
            if b:
                _arr.append(arr2)

    return _arr


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
x_angle, y_angle = -90.1, -30.1

pygame.init()
screen = pygame.display.set_mode(size)

now_pos = [None, None]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()


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
    
    y_angle = max(-90, min(90, y_angle))
    x_angle = x_angle % 360

    arr = get_pos_in_2d_plane(pos_pl, x_angle, y_angle, size, vertex.copy(), faces, fast_mode)

    for pos in arr:
        pygame.draw.polygon(screen, [255, 255, 255], pos, 1)

    pygame.display.update()
    screen.fill((0, 0, 0))

    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
