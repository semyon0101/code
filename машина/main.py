import pygame
import sys
import math

pygame.init()
size = [800, 800]


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_arr(self):
        return [self.x, self.y]


class Vector(Pos):
    pass


class Car:
    def __init__(self):
        self.size = [15, 40]
        self.first_point = Pos(435, 407.5)
        self.second_point = Pos(405, 407.5)

        self.angle = 0
        self.wheels_angle = 0
        self.first_vector = Vector(0, 0)
        self.second_vector = Vector(0, 0)
        self.speed = 0.1
        self.max_speed = 1
        self.update()

    def handle_event(self, _event):
        pass

    def update(self):
        if self.first_vector.x > self.max_speed: self.first_vector.x = self.max_speed
        if self.first_vector.y > self.max_speed: self.first_vector.y = self.max_speed
        if self.second_vector.x > self.max_speed: self.second_vector.x = self.max_speed
        if self.second_vector.y > self.max_speed: self.second_vector.y = self.max_speed
        if self.first_vector.x < -self.max_speed: self.first_vector.x = self.max_speed
        if self.first_vector.y < -self.max_speed: self.first_vector.y = self.max_speed
        if self.second_vector.x < -self.max_speed: self.second_vector.x = self.max_speed
        if self.second_vector.y < -self.max_speed: self.second_vector.y = self.max_speed
        self.first_point.x += self.first_vector.x
        self.first_point.y += self.first_vector.y
        self.second_point.x += self.second_vector.x
        self.second_point.y += self.second_vector.y
        self.first_vector.x *= 0.8
        self.first_vector.y *= 0.8
        self.second_vector.x *= 0.8
        self.second_vector.y *= 0.8

        center = Pos((self.first_point.x + self.second_point.x) / 2, (self.first_point.y + self.second_point.y) / 2)
        point_3 = Pos(center.x, center.y - 15)
        a = math.sqrt((point_3.x - self.second_point.x) ** 2 + (point_3.y - self.second_point.y) ** 2)
        b = math.sqrt((point_3.x - self.first_point.x) ** 2 + (point_3.y - self.first_point.y) ** 2)
        angle = 180 - math.degrees(math.atan2(a, b)) * 2

        if self.first_point.x < center.x:
            angle *= -1

        self.angle = angle

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            center = Pos((self.first_point.x + self.second_point.x) / 2,
                         (self.first_point.y + self.second_point.y) / 2)

            point_3 = Pos(center.x, center.y - 15)
            a = math.sqrt((point_3.x - self.second_point.x) ** 2 + (point_3.y - self.second_point.y) ** 2)
            b = math.sqrt((point_3.x - self.first_point.x) ** 2 + (point_3.y - self.first_point.y) ** 2)

            angle_in_rad = math.radians(180 - math.degrees(math.atan2(a, b)) * 2)
            x = -math.sin(angle_in_rad) * self.speed
            y = -math.cos(angle_in_rad) * self.speed
            if point_3.x > self.second_point.x:
                x = -x
                y = -y
            self.first_vector.x += x
            self.first_vector.y += y
            self.second_vector.x += x
            self.second_vector.y += y
        if keys[pygame.K_s]:
            center = Pos((self.first_point.x + self.second_point.x) / 2,
                         (self.first_point.y + self.second_point.y) / 2)

            point_3 = Pos(center.x, center.y - 15)
            a = math.sqrt((point_3.x - self.second_point.x) ** 2 + (point_3.y - self.second_point.y) ** 2)
            b = math.sqrt((point_3.x - self.first_point.x) ** 2 + (point_3.y - self.first_point.y) ** 2)

            angle_in_rad = math.radians(180 - math.degrees(math.atan2(a, b)) * 2)
            x = -math.sin(angle_in_rad) * self.speed
            y = -math.cos(angle_in_rad) * self.speed
            if center.x > self.second_point.x:
                x = -x
                y = -y
            self.first_vector.x -= x
            self.first_vector.y -= y
            self.second_vector.x -= x
            self.second_vector.y -= y

        angle2 = (180 - angle) / 2
        angle3 = angle / 2
        a2 = math.sin(math.radians(angle3)) * 30
        b2 = math.sin(math.radians(angle2)) * 30
        pos1 = Pos(math.sin(math.radians(angle2)) * a2, math.cos(math.radians(angle2)) * a2)
        pos2 = Pos(math.sin(math.radians(angle3)) * b2, math.cos(math.radians(angle3)) * b2)
        if center.x > self.first_point.x:
            pos1.x *= -1
        if center.x > self.second_point.x:
            pos2.x *= -1
        self.first_point.x = point_3.x + pos1.x
        self.first_point.y = point_3.y + pos1.y
        self.second_point.x = point_3.x + pos2.x
        self.second_point.y = point_3.y + pos2.y

    def draw(self, screen):

        surf = pygame.Surface(self.size)
        surf.fill((255, 255, 255))
        surf.set_colorkey((0, 0, 0))
        center = Pos((self.first_point.x + self.second_point.x) / 2, (self.first_point.y + self.second_point.y) / 2)

        surf = pygame.transform.rotate(surf, self.angle)
        _screen.blit(surf, surf.get_rect(center=center.get_arr()))

        surf1 = pygame.Surface((3, 3))
        _screen.blit(surf1, [self.first_point.x - 1, self.first_point.y - 1])
        return screen


car = Car()

while True:
    _screen = pygame.display.set_mode(size)
    _screen.fill((60, 160, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        car.handle_event(event)
    car.update()
    _screen = car.draw(_screen)
    pygame.display.flip()
