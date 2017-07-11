import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Line:
    matplotlib_obj = None
    def __init__(self, pointA, pointB, lw=2, mplprops={}, figure=None):
        print 'created'
        if not isinstance(lw, list):
            lw = [lw]
            pointA = [pointA]
            pointB = [pointB]
            self.matplotlib_obj = []

            self.pointA = pointA
            self.pointB = pointB
            self.lw = lw
            self.mplprops = mplprops
            self.figure = figure

    def __draw__(self, zorder=1):
        for pointA, pointB, lw in zip(self.pointA, self.pointB, self.lw):
            self.matplotlib_obj.append(matplotlib.lines.Line2D(pointA, pointB, lw, **self.mplprops))


        for obj in self.matplotlib_obj:
            obj.zorder=zorder
