from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import sys
from ctypes import *
import numpy as np
import math

size = [1000, 500]

player_pos = [0, 0, -60]
player_angle = [0, 0]
speed = 1

now_pos = [None, None]


def rotate(_x_angle, _y_angle):
    _x_angle = math.radians(_x_angle)
    _y_angle = math.radians(-_y_angle)
    _pos = [0, 0, speed]

    _y_angle += math.atan2(_pos[2], _pos[1])
    r_y_z = math.sqrt(_pos[1] ** 2 + _pos[2] ** 2)
    _pos[1] = r_y_z * math.cos(_y_angle)
    _pos[2] = r_y_z * math.sin(_y_angle)

    r_x_y = math.sqrt(_pos[2] ** 2 + _pos[0] ** 2)
    _x_angle += math.atan2(_pos[2], _pos[0])
    _pos[0] = r_x_y * math.cos(_x_angle)
    _pos[2] = r_x_y * math.sin(_x_angle)



    return _pos


def get_object_from_file(filename, types):
    _vertex, _faces = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                _vertex.append([float(i) for i in line.split()[1:]])
            elif line.startswith('f'):
                _faces.append([int(face_.split('/')[0]) - 1 for face_ in line.split()[1:]])
    _faces_2 = []
    if types == "GL_TRIANGLES":
        _faces_2 = []
        for _face in _faces:
            i = 1
            while i + 1 <= len(_face) - 1:
                _faces_2.append([_face[0], _face[i], _face[i + 1]])
                i += 1
    elif types == "GL_LINES":
        _faces_2 = []
        for _face in _faces:
            i = 0
            while i + 1 <= len(_face) - 1:
                _faces_2.append([_face[i], _face[i + 1]])
                i += 1
            _faces_2.append([_face[i], _face[0]])
    return _vertex, _faces_2


def init():
    pygame.init()

    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glOrtho(-1, 1, -1, 1, -1, 1)
    gluPerspective(45, 1, 0.1, 200)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glScalef(size[1] / size[0], 1, 1)

    vertexVBO = GLuint()
    indexEBO = GLuint()


    glGenBuffers(1, vertexVBO)
    glBindBuffer(GL_ARRAY_BUFFER, vertexVBO)
    glBufferData(GL_ARRAY_BUFFER, len(vertexes) * 4, (c_float * len(vertexes))(*vertexes),
                 GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glGenBuffers(1, indexEBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexes) * 4, (c_uint * len(indexes))(*indexes),
                 GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


    return screen, clock, vertexVBO, indexEBO


def event_update():
    global now_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        arr = rotate(player_angle[0] + 90, 0)
        player_pos[0] -= arr[0]
        player_pos[1] -= arr[1]
        player_pos[2] -= arr[2]
    if keys[pygame.K_d]:
        arr = rotate(player_angle[0] + 90, 0)
        player_pos[0] += arr[0]
        player_pos[1] += arr[1]
        player_pos[2] += arr[2]
    if keys[pygame.K_s]:
        arr = rotate(player_angle[0], player_angle[1])
        player_pos[0] -= arr[0]
        player_pos[1] -= arr[1]
        player_pos[2] -= arr[2]
    if keys[pygame.K_w]:
        arr = rotate(player_angle[0], player_angle[1])
        player_pos[0] += arr[0]
        player_pos[1] += arr[1]
        player_pos[2] += arr[2]
    if keys[pygame.K_e]:
        arr = rotate(player_angle[0], player_angle[1] - 90)
        player_pos[0] -= arr[0]
        player_pos[1] -= arr[1]
        player_pos[2] -= arr[2]
    if keys[pygame.K_q]:
        arr = rotate(player_angle[0], player_angle[1] - 90)
        player_pos[0] += arr[0]
        player_pos[1] += arr[1]
        player_pos[2] += arr[2]

    if pygame.mouse.get_pressed(3)[0]:
        if now_pos == [None, None]:
            now_pos = pygame.mouse.get_pos()
        else:
            player_angle[1] += (now_pos[1] - pygame.mouse.get_pos()[1]) * 0.2
            player_angle[0] += (now_pos[0] - pygame.mouse.get_pos()[0]) * 0.2
            now_pos = pygame.mouse.get_pos()
            player_angle[0] = player_angle[0] % 360
            player_angle[1] = min(max(player_angle[1], -90), 90)
    else:
        now_pos = [None, None]


def draw():
    glPushMatrix()

    glRotate(player_angle[1], 1, 0, 0)
    glRotate(player_angle[0], 0, 1, 0)
    glTranslate(*player_pos)

    glEnableClientState(GL_VERTEX_ARRAY)

    glBindBuffer(GL_ARRAY_BUFFER, vertexVBO)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexEBO)
    glDrawElements(GL_LINES, len(indexes), GL_UNSIGNED_INT, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    glDisableClientState(GL_VERTEX_ARRAY)

    glPopMatrix()


vertexes, indexes = get_object_from_file("resources/t_34_obj.obj", "GL_LINES")

vertexes = list(np.array(vertexes).reshape(len(vertexes) * len(vertexes[0])))
indexes = list(np.array(indexes).reshape(len(indexes) * len(indexes[0])))

screen, clock, vertexVBO, indexEBO = init()

while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    event_update()
    draw()
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.flip()
    clock.tick(60)
