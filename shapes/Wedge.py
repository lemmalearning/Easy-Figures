import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Wedge:
    def __init__(self, xy, radius, theta1=0.0, theta2=360.0, props={}, figure=None):
        self.xy = xy
        self.radius = radius
        self.theta1 = theta1
        self.theta2 = theta2
        self.props = props
        self.figure = figure

        wedge = patches.Wedge(xy, radius, theta1, theta2, **self.props)
        self.matplotlib_obj = wedge

    def __draw__(self, zorder=1):
        p = self.figure.ax.add_patch(self.matplotlib_obj)
        p.set(zorder=zorder)
