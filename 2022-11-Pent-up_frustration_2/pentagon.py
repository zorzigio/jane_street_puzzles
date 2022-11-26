from shapely.geometry import Point, Polygon, LineString
from shapely import affinity
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import math


class LineStringPlus(LineString):
    @property
    def points(self) -> tuple[Point, Point]:
        return (Point(self.coords[0]), Point(self.coords[1]))


class Pentagon:
    SIDE_LENGTH = 1
    ANGLE_INTERNAL = 2 * math.pi - math.pi * 2 / 5
    R = (SIDE_LENGTH / 2) / math.sin(math.pi / 5)
    r = (SIDE_LENGTH / 2) / math.tan(math.pi / 5)
    COLLISION_DISTANCE = 1e-6

    def __init__(
        self,
        p1: Point,
        p2: Point,
        label: str | None = None,
    ) -> None:
        """
        Create a pentagon with side length 1 given one side defined by p1 and p2.
        The pentagon is created by going from p1 to p2 and closing clockwise
        """
        self.p1 = p1
        self.p2 = p2
        self.label = label

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

    def side(self, n: int) -> LineStringPlus:
        return LineStringPlus([self.p[n-1], self.p[(n)]])

    def R_line(self, n: int) -> LineStringPlus:
        return LineStringPlus([self.center_point, self.p[(n-1)]])

    def get_pentagon_on_side(self, n: int, label: str | None = None) -> "Pentagon":
        return Pentagon(self.p[n % 5], self.p[n-1], label=label)

    def plot(self, ax: plt.Axes) -> None:
        patch = PolygonPatch(self.poly, fc='#999999', ec='#000000', alpha=0.5, zorder=2)
        ax.add_patch(patch)
        plt.plot(*self.side(1).xy)
        plt.plot(*self.R_line(1).xy)
        plt.plot(self.center_point.x, self.center_point.y, 'ro')
        if self.label is not None:
            plt.text(self.center_point.x, self.center_point.y, self.label)


class Pentagons:

    def __init__(self) -> None:
        self.pentagons: list[Pentagon] = []
        self.distance: float = float("inf")
        self.has_collisions: bool = False
        "Starts with 2 pentagons"
        p1 = Point(0, 1)
        p2 = Point(0, 0)
        P1 = Pentagon(p1, p2, label="P1")
        self.pentagons.append(P1)
        P2 = P1.get_pentagon_on_side(1, label="P2")
        self.pentagons.append(P2)
        self.sequence: list[int] = []

    @ classmethod
    def from_sequence(cls, sequence: list[int]) -> "Pentagons":
        pents = cls()
        for n in sequence:
            pents.add(n)
            if pents.has_collisions:
                break
        return pents

    def add(self, n: int) -> None:
        P = self.pentagons[-1].get_pentagon_on_side(n, label=f"P{len(self)+1}")
        # print(f"Adding pentagon {P.label} on side {n}")
        self.pentagons.append(P)
        self.sequence.append(n)
        self.has_collisions = self.check_for_collisions()
        if not self.has_collisions:
            self.distance = self._compute_min_distance()

    def plot(self) -> None:
        fig = plt.figure(1, figsize=(5, 5), dpi=90)
        ax = fig.add_subplot(111)
        for P in self:
            P.plot(ax)
        extent = 10
        ax.set_xlim(-extent, extent)
        ax.set_ylim(-extent, extent)
        ax.set_aspect(1)
        plt.title(f"Distance: {self.distance:.7f}")
        plt.show()

    def __len__(self) -> int:
        return len(self.pentagons)

    def __getitem__(self, i: int) -> Pentagon:
        return self.pentagons[i]

    def _compute_min_distance(self) -> float:
        if len(self) <= 3:
            return float("inf")
        last_pentagon = self[-1]
        min_distance = self.distance
        for pentagon in self.pentagons[0:-3]:
            distance = pentagon.poly.distance(last_pentagon.poly)
            if distance < min_distance:
                min_distance = distance
        if min_distance < Pentagon.COLLISION_DISTANCE:
            self.has_collisions = True
        return min_distance

    def check_for_collisions(self) -> bool:
        if self.has_collisions:
            return True
        if len(self) <= 2:
            return False
        last_pentagon = self[-1]
        for pentagon in self.pentagons[:-2]:
            intersection = pentagon.poly.intersection(last_pentagon.poly)
            if intersection.area > 0:
                return True

        return False
