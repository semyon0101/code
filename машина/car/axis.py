from машина.more.p_a_v import *
import math

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
