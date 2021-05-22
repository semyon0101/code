import pygame
import sys
import math

pygame.init()
size = [800, 800]
font = pygame.font.Font(None, 36)

points = [(238, 112), (126, 46), (167, 195), (45, 168), (162, 298), (45, 320), (176, 391), (58, 454), (200, 475),
          (106, 531), (257, 499), (205, 588), (315, 508), (328, 604), (401, 508), (439, 613), (488, 494), (546, 603),
          (565, 433), (666, 521), (629, 391), (714, 449), (683, 334), (742, 358), (677, 269), (753, 286), (682, 209),
          (755, 199), (666, 159), (736, 116), (623, 121), (660, 45), (589, 99), (594, 27), (532, 95), (497, 8),
          (481, 87), (445, 7), (436, 83), (380, 2), (351, 81), (314, 2), (284, 87), (207, 3), (238, 112), (126, 46)]


def level():
    _surf = pygame.Surface(size)
    _surf.set_colorkey((0, 0, 0))
    last = []
    for f, s in zip(points[::2], points[1::2]):
        if len(last) >= 2:
            pygame.draw.polygon(_surf, (150, 150, 150), [*last, s, f])
        last = [f, s]
    return _surf


def get_obj_level():
    all_obj = []
    last = []
    for f, s in zip(points[::2], points[1::2]):
        if len(last) >= 2:
            all_obj.append(pygame.draw.polygon(pygame.Surface(size), (150, 150, 150), (last[0], last[1], s, f)))
        last = [f, s]
    return all_obj


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_arr(self):
        return [self.x, self.y]

    def __repr__(self):
        return f"{self.x}, {self.y}"


class Vector(Pos):
    pass


class Line:
    def __init__(self, pos: Pos):
        self.pos = pos
        self.angle = 0
        self.margin = [0, 0]
        self.start()

    def start(self):
        pass

    def get_len(self) -> float:
        end = False
        m = 0
        while not end:
            pass
        return m


class Axis:
    def __init__(self, point: Pos):
        self.point = point
        self.vector = Vector(0, 0)
        self.axis_angle = 0
        self.wheels_angle = 0

    def get_vector_by_meters(self, meters):
        angle = self.axis_angle + self.wheels_angle
        x = math.sin(math.radians(angle)) * meters
        y = math.cos(math.radians(angle)) * meters
        return Vector(x, y)

    def go_by_vector(self, vector: Vector):
        self.point.x += vector.x
        self.point.y -= vector.y

    def get_all_angle(self) -> float:
        return self.axis_angle + self.wheels_angle


class Car:
    def __init__(self):
        self.size = [30, 60]
        self.first_axis = Axis(Pos(310, 550))
        self.second_axis = Axis(Pos(340, 550))
        img = pygame.image.load("car.png")
        img = pygame.transform.rotate(img, 90)
        self.img = pygame.transform.scale(img, self.size)
        self.angle = 0
        self.now_speed = 0
        self.speed = 0.002
        self.max_speed = 0.5
        self.max_angle = 30
        self.end = False
        self.all_obj = get_obj_level()
        print(self.all_obj)
        self.update()

    def handle_event(self, _event):
        pass

    def update(self):
        angle = self.get_angel()
        self.angle = angle
        self.first_axis.axis_angle = angle
        self.second_axis.axis_angle = angle

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.first_axis.wheels_angle = -self.max_angle
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.first_axis.wheels_angle = self.max_angle
        else:
            self.first_axis.wheels_angle = 0

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.now_speed += self.speed

        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.now_speed -= self.speed

        self.now_speed *= 0.997

        if (keys[pygame.K_a] and not keys[pygame.K_d]) or (keys[pygame.K_d] and not keys[pygame.K_a]):
            self.now_speed *= 0.998

        if self.now_speed > self.max_speed:
            self.now_speed = self.max_speed
        elif self.now_speed < -self.max_speed * 0.5:
            self.now_speed = -self.max_speed * 0.5

        if self.now_speed > 0:
            i = 0.2
            for _ in range(int(self.now_speed // i)):
                vector1 = self.first_axis.get_vector_by_meters(i)
                self.first_axis.go_by_vector(vector1)
                vector2 = self.second_axis.get_vector_by_meters(i)
                self.second_axis.go_by_vector(vector2)

            vector1 = self.first_axis.get_vector_by_meters(self.now_speed % i)
            self.first_axis.go_by_vector(vector1)
            vector2 = self.second_axis.get_vector_by_meters(self.now_speed % i)
            self.second_axis.go_by_vector(vector2)
        else:
            i = -0.2
            for _ in range(int(self.now_speed // i)):
                vector1 = self.first_axis.get_vector_by_meters(i)
                self.first_axis.go_by_vector(vector1)
                vector2 = self.second_axis.get_vector_by_meters(i)
                self.second_axis.go_by_vector(vector2)

            vector1 = self.first_axis.get_vector_by_meters(self.now_speed % i)
            self.first_axis.go_by_vector(vector1)
            vector2 = self.second_axis.get_vector_by_meters(self.now_speed % i)
            self.second_axis.go_by_vector(vector2)

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

        a = False
        for obj in self.all_obj:
            _surf = self.img
            _surf = pygame.transform.rotate(_surf, -self.angle)
            rect = _surf.get_rect()
            rect.center = self.get_center().get_arr()
            if obj.colliderect(rect):
                a = True
        if not a:
            self.end = True
            print("234")

    def draw(self, screen):

        _surf = self.img
        _surf = pygame.transform.rotate(_surf, -self.angle)
        center = self.get_center()
        _screen.blit(_surf, _surf.get_rect(center=center.get_arr()))

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


car = Car()

level_surf = level()
while True:
    _screen = pygame.display.set_mode(size)
    _screen.fill((60, 160, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        car.handle_event(event)
    car.update()
    _screen.blit(level_surf, [0, 0])
    pygame.draw.line(_screen, (255, 255, 255), (329, 510), (329, 603), 40)
    _screen = car.draw(_screen)
    surf = font.render(str(int(round(car.now_speed, 3) * 400)), True, (0, 0, 0))
    _screen.blit(surf, [745, 10])

    pygame.display.flip()
