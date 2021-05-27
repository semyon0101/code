from машина.more.p_a_v import *
from машина.more.config import *
import math
import numba
import numpy as np


class Line:
    def __init__(self, angle, max_length_in_car):
        self.angle = angle
        self.m_l_c = max_length_in_car
        self.pos = Pos(0, 0)

    def get_length(self, center: Pos, car_angle):
        margin = get_margin(-car_angle + self.angle)

        m = get_m(np.array(center.get_arr()), margin, np.array(points))

        self.pos = Pos(center.x + margin[0] * m, center.y + margin[1] * m)

        return m, self.m_l_c >= m


@numba.jit(nopython=True, parallel=True)
def get_m(center: np.array, margin: np.array, _points: np.array):
    m = 0.0
    while m < 600:
        point = np.array([center[0] + margin[0] * m, center[1] + margin[1] * m])
        if not in_all_quadrilaterals(point, _points):
            break
        m += 5
    return m




@numba.jit(nopython=True)
def in_all_quadrilaterals(point: np.array, _points: np.array):
    b = 0
    for i in range(int(len(_points) / 2)):
        if i >= 1:
            t1 = _points[i * 2]
            t2 = _points[i * 2 + 1]
            t3 = _points[i * 2 - 2]
            t4 = _points[i * 2 - 1]
            if in_quadrilateral(point, t1, t2, t3, t4):
                b += 1
                break
    return bool(b)


@numba.jit(nopython=True)
def get_margin(angle):
    return np.array([math.sin(math.radians(angle)), math.cos(math.radians(angle))])


@numba.jit(nopython=True)
def in_quadrilateral(point: np.array, t1: np.array, t2: np.array, t3: np.array, t4: np.array):
    return in_triangle(point, t1, t2, t3) or in_triangle(point, t2, t3, t4)


@numba.jit(nopython=True)
def in_triangle(point: np.array, t1: np.array, t2: np.array, t3: np.array):
    [xa, ya] = t1
    [xb, yb] = t2
    [xc, yc] = t3
    [xd, yd] = point
    return (((xd - xa) * (yb - ya) - (yd - ya) * (xb - xa)) * ((xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)) >= 0) and \
           (((xd - xb) * (yc - yb) - (yd - yb) * (xc - xb)) * ((xa - xb) * (yc - yb) - (ya - yb) * (xc - xb)) >= 0) and \
           (((xd - xc) * (ya - yc) - (yd - yc) * (xa - xc)) * ((xb - xc) * (ya - yc) - (yb - yc) * (xa - xc)) >= 0)
