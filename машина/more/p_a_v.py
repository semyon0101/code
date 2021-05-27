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
