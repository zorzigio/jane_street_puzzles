from shapely.geometry import Point, Polygon, LineString
from shapely import affinity
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import math


class Pentagon:
    SIDE_LENGTH = 1
    ANGLE_INTERNAL = 2 * math.pi - math.pi * 2 / 5
    R = (SIDE_LENGTH / 2) / math.sin(math.pi / 5)
    r = (SIDE_LENGTH / 2) / math.tan(math.pi / 5)

    def __init__(
        self,
        p1: Point,
        p2: Point,
    ) -> None:
        """
        Create a pentagon with side length 1 given one side defined by p1 and p2.
        The pentagon is created by going from p1 to p2 and closing clockwise
        """
        self.p1 = p1
        self.p2 = p2
        # Calculate the side length
        side_length = p1.distance(p2)
        if side_length != self.SIDE_LENGTH:
            raise ValueError("Side length is not 1")

        # Calculate the angle between p1 and p2
        angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
        # compute the center of the line
        center_line_point = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        # center of the pentagon
        self.center_point = Point(center_line_point.x + math.sin(angle) * self.r, center_line_point.y - math.cos(angle) * self.r)
        # this is the radius of the circle that inscribes the pentagon
        self.line_R = LineString([self.center_point, p2])
        # get points of pentagon
        rotated = affinity.rotate(self.line_R, -72, origin=self.center_point)  # type: ignore
        self.p3 = Point(rotated.coords[1])
        rotated = affinity.rotate(self.line_R, -144, origin=self.center_point)  # type: ignore
        self.p4 = Point(rotated.coords[1])
        rotated = affinity.rotate(self.line_R, -216, origin=self.center_point)  # type: ignore
        self.p5 = Point(rotated.coords[1])
        # create polygon
        self.poly = Polygon([self.p1, self.p2, self.p3, self.p4, self.p5])
        self.p: tuple[Point, Point, Point, Point, Point] = (self.p1, self.p2, self.p3, self.p4, self.p5)

    def side(self, n: int) -> LineString:
        return LineString([self.p[n-1], self.p[(n)]])

    def R_line(self, n: int) -> LineString:
        return LineString([self.center_point, self.p[(n-1)]])

    def plot(self, ax: plt.Axes) -> None:
        patch = PolygonPatch(self.poly, fc='#999999', ec='#000000', alpha=0.5, zorder=2)
        ax.add_patch(patch)
        plt.plot(*self.side(1).xy)
        plt.plot(*self.R_line(1).xy)
        plt.plot(self.center_point.x, self.center_point.y, 'ro')
