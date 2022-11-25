from shapely.geometry import Point
import matplotlib.pyplot as plt
from pentagon import Pentagon

if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(0, 1)
    P1 = Pentagon(p1, p2)
    P2 = Pentagon(p2, p1)

    # plot
    fig = plt.figure(1, figsize=(5, 5), dpi=90)
    ax = fig.add_subplot(111)
    P1.plot(ax)
    P2.plot(ax)
    extent = 10
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect(1)
    plt.show()
