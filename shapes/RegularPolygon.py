import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class RegularPolygon:
    def __init__(self, xy, numVertices, radius=0, fill=False, orientation=0.0, mplprops={}, figure=None):
        self.xy = xy
        self.numVertices = numVertices
        self.radius = radius
        self.fill = fill
        self.orientation = orientation
        self.linewidth = 2
        self.mplprops = mplprops
        self.figure = figure

        # Define the polygon
        polygon = patches.RegularPolygon(xy, numVertices, radius, fill=False, linewidth=self.linewidth, **self.mplprops)
        self.matplotlib_obj = polygon

    def __draw__(self, zorder=1):
        p = self.figure.ax.add_patch(self.matplotlib_obj)
        p.set(zorder=zorder)
