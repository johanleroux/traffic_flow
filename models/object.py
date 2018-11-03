from math import fabs

from scipy.spatial import distance as dist


class Object:
    def __init__(self):
        self.id = 0
        self.name = None
        self.score = 0
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.hiddenFrames = 0
        self.dangerLevel = 0
        self.personLevel = None

    def startX(self):
        return int(self.x - self.w / 2)

    def endX(self):
        return int(self.x + self.w / 2)

    def startY(self):
        return int(self.y - self.h / 2)

    def endY(self):
        return int(self.y + self.h / 2)

    def distanceTo(self, other):
        return dist.euclidean([self.x, self.y], [other.x, other.y])

    def collides(self, other):
        if (self.startX() < other.endX() and self.endX() > other.startX()
                and self.startY() < other.endY()
                and self.endY() > other.startY()):
            return True
        return False
