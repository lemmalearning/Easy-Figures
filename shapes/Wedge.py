import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Wedge:
    def __init__(self, xy, r, theta1=0, theta2=0, width=None, mplprops={}, figure=None):
        self.xy = xy
        self.r = r
        self.theta1 = theta1
        self.theta2 = theta2
        self.mplprops = mplprops
        self.figure = figure
        self.width = width

        wedge = patches.Wedge(xy, r, theta1, theta2, width, **self.mplprops)
        self.matplotlib_obj = wedge

    def __draw__(self, zorder=1):
        p = self.figure.ax.add_patch(self.matplotlib_obj)
        p.set(zorder=zorder)
