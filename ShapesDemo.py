import numpy as np
from random import randint, choice
import matplotlib
matplotlib.use('Svg')
import matplotlib.pyplot as plt
from matplotlib import patches
import figures

def main():
    f = figures.Figures()
    """
    # Triangle & Polygon
    # Given figure: Two triangles ABO and CDO in a ribbon shape, meeting at point O. AO = 6, BO = 4, CO = 10. NOTE: Figure not drawn to scale.
    # Q: Line segments AB and CD in the figure are parallel. What is the length of AD?

    tri = f.addTriangle_angle(angle=np.pi/6, xy=[0,0], rotation=np.pi/4)
    tri.labelVertices(['a', '\,', 'b'])

    poly = f.addPolygon(np.matrix([[-2, -2.2],
                                    [0, 0],
                                    [2,-1.8]
                                    ]))
    poly.labelVertices(['c','\,','d'])

    o = f.addText(xy=(0,-0.05), text="o", latex=True, fontsize=20)

    random = randint(1,15)
    random2 = randint(1,15)

    ao = f.addText(xy=(0.8,0.6), text="" + str(random) + "", latex=True, fontsize=20)
    bo = f.addText(xy=(-0.6,0.35), text="" + str(random2) + "", latex=True, fontsize=20)
    co = f.addText(xy=(-1.1, -0.8), text="" + str(random*2) + "", latex=True, fontsize=20)
    f.axisFormat(xyrange=[[-3,3], [-3,3]], arrows=False, grid=False)
    plt.axis('off')

    # Correct if ans == random2*2

    """
    # Circle & Ellipse
    # Given figure: An ellipse wrapping around a circle. NOTE: Figure not drawn to scale.
    # The ellipses major axis is given and the given length "d" is given. Find the area of the shaded region.

    # randomized

    d = randint(5,30)
    majorAxis = d+5

    ell = f.addEllipse(xy=(7,10), width=20, height=50, is_radius=1, fc='white')
    circ = f.addCircle(xy=(7,10), label="r", radius=10, fc='grey')
    b = f.addText(xy=(8.5, 28), text=str(d), latex=True, fontsize=20)

    plt.axis('off')
    plt.axis('scaled')

    # Correct if ans == np.pi*((majorAxis-d)^2)


    f.__writeFile__('/Users/chloesheen/test.svg')

    return None

if __name__ == "__main__":
    main()
