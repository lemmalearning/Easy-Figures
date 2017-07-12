import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Line:
    matplotlib_obj = None
    def __init__(self, pointA, pointB, lw=2, mplprops={}, figure=None):
        self.matplotlib_obj = None
        self.pointA = pointA
        self.pointB = pointB
        self.lw = lw
        self.mplprops = mplprops
        self.figure = figure

    def __draw__(self, zorder=1):
        x = [self.pointA[0], self.pointB[0]]
        y = [self.pointA[1], self.pointB[1]]
        self.matplotlib_obj = plt.plot(x, y, linewidth=self.lw, **self.mplprops)[0]
        self.matplotlib_obj.set_zorder(zorder)
