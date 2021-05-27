from машина.car.axis import *
from машина.line.line import *
from машина.more.p_a_v import *
import pygame
import numba
import numpy as np

pygame.init()


class Car:
    def __init__(self):
        self.size = [20, 40]
        self.first_axis = Axis(Pos(310, 550))
        self.second_axis = Axis(Pos(340, 550))
        img = pygame.image.load("car/car.png")
        img = pygame.transform.rotate(img, 90)
        self.img = pygame.transform.scale(img, self.size)
        self.angle = 0
        self.now_speed = 0
        self.speed = 0.011
        self.max_speed = 1.5
        self.max_angle = 30
        self.end = False
        self.lines = [Line(-90, 10), Line(-27, 22), Line(0, 20), Line(27, 22),
                      Line(90, 10), Line(153, 22), Line(180, 20), Line(-153, 22)]
        self.fitnessAI = 30
        self.i = 1

    def update(self):

        angle = self.get_angel()
        self.angle = angle
        self.first_axis.axis_angle = angle
        self.second_axis.axis_angle = angle
        self.fitnessAI -= 0.1

        self.keys_update()

        self.going()

        self.remake_axis()

        self.new_circle()

        center = self.get_center()
        for line in self.lines:
            m, b = line.get_length(center, self.angle)
            if b:
                print("end")

    def draw(self, screen):

        _surf = self.img
        _surf = pygame.transform.rotate(_surf, -self.angle)
        center = self.get_center()
        screen.blit(_surf, _surf.get_rect(center=center.get_arr()))

        draw = False
        if draw:
            for line in self.lines:
                pygame.draw.line(screen, (0, 0, 0), center.get_arr(), line.pos.get_arr())

        return screen

    def get_center(self) -> Pos:
        return Pos((self.first_axis.point.x + self.second_axis.point.x) / 2,
                   (self.first_axis.point.y + self.second_axis.point.y) / 2)

    def get_angel(self) -> float:
        center = self.get_center()
        point_3 = Pos(center.x, center.y - 15)
        a = math.sqrt((point_3.x - self.second_axis.point.x) ** 2 + (point_3.y - self.second_axis.point.y) ** 2)
        b = math.sqrt((point_3.x - self.first_axis.point.x) ** 2 + (point_3.y - self.first_axis.point.y) ** 2)
        angle = 180 - math.degrees(math.atan2(a, b)) * 2

        if self.first_axis.point.x < center.x:
            angle *= -1
        return angle

    def keys_update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.first_axis.wheels_angle = -self.max_angle
            self.fitnessAI -= 0.03
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.first_axis.wheels_angle = self.max_angle
            self.fitnessAI -= 0.03
        else:
            self.first_axis.wheels_angle = 0

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.now_speed += self.speed

        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.now_speed -= self.speed
        if self.now_speed != 0:
            sp = (abs(self.now_speed) / self.now_speed) * self.speed * 0.5
            if abs(self.now_speed) < abs(sp):
                self.now_speed = 0
            else:
                self.now_speed -= sp

        if (keys[pygame.K_a] and not keys[pygame.K_d]) or (keys[pygame.K_d] and not keys[pygame.K_a]):
            self.now_speed *= 0.995

    def going(self):
        if self.now_speed > self.max_speed:
            self.now_speed = self.max_speed
        elif self.now_speed < -self.max_speed * 0.5:
            self.now_speed = -self.max_speed * 0.5
        i = 0.2
        if self.now_speed <= 0:
            i = -0.2

        if self.now_speed > 0:
            self.fitnessAI += 0.1
        elif self.fitnessAI < 0:
            self.fitnessAI += 0.05

        for _ in range(int(self.now_speed // i)):
            vector1 = self.first_axis.get_vector_by_meters(i)
            self.first_axis.go_by_vector(vector1)
            vector2 = self.second_axis.get_vector_by_meters(i)
            self.second_axis.go_by_vector(vector2)

        vector1 = self.first_axis.get_vector_by_meters(self.now_speed % i)
        self.first_axis.go_by_vector(vector1)
        vector2 = self.second_axis.get_vector_by_meters(self.now_speed % i)
        self.second_axis.go_by_vector(vector2)

    def remake_axis(self):
        angle = self.get_angel()
        self.angle = angle
        center = self.get_center()
        point_3 = Pos(center.x, center.y - 15)
        angle2 = (180 - angle) / 2
        angle3 = angle / 2
        a2 = math.sin(math.radians(angle3)) * 30
        b2 = math.sin(math.radians(angle2)) * 30
        pos1 = Pos(math.sin(math.radians(angle2)) * a2, math.cos(math.radians(angle2)) * a2)
        pos2 = Pos(math.sin(math.radians(angle3)) * b2, math.cos(math.radians(angle3)) * b2)
        if self.first_axis.point.x < self.second_axis.point.x:
            if angle > 0:
                pos1.x *= -1
            if angle < 0:
                pos2.x *= -1
        else:
            if angle < 0:
                pos1.x *= -1
            if angle > 0:
                pos2.x *= -1
        self.first_axis.point.x = point_3.x + pos1.x
        self.first_axis.point.y = point_3.y + pos1.y
        self.second_axis.point.x = point_3.x + pos2.x
        self.second_axis.point.y = point_3.y + pos2.y

    def new_circle(self):
        for point in self.get_last_point():
            if in_quadrilaterals2(np.array(point.get_arr()), np.array(checkpoint[self.i])):
                self.i += 1

                if self.i > len(checkpoint) - 1:
                    self.i = 0
                elif self.i == 1:
                    self.fitnessAI += 10

                self.fitnessAI += 1
                break

    def get_last_point(self) -> tuple[Pos, Pos, Pos, Pos]:
        margin = Vector(math.sin(math.radians(self.angle + 90)) * 10, math.cos(math.radians(self.angle + 90)) * 10)
        t1 = Pos(self.first_axis.point.x - margin.x, self.first_axis.point.y - margin.y)
        t2 = Pos(self.first_axis.point.x + margin.x, self.first_axis.point.y + margin.y)
        t3 = Pos(self.second_axis.point.x - margin.x, self.second_axis.point.y - margin.y)
        t4 = Pos(self.second_axis.point.x + margin.x, self.second_axis.point.y + margin.y)
        return t1, t2, t3, t4


@numba.jit(nopython=True)
def in_quadrilaterals2(point: np.array, checkpoint_i: np.array):
    return in_quadrilateral(point, checkpoint_i[0], checkpoint_i[1], checkpoint_i[2], checkpoint_i[3])
