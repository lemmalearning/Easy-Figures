import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

#f.addFancyArrow(posA=(-5,2.5), posB=(3,2.5), arrowstyle='|-|', connectionstyle='bar', mplprops={'mutation_scale':5})
#f.addFancyArrow(posA=(6, 0), posB=(6, 3), arrowstyle='<->', connectionstyle='bar', mplprops={'mutation_scale':7})

class FancyArrowPatch:
    def __init__(self, posA=None, posB=None, path=None, color='k', lw=1, arrowstyle='simple', connectionstyle='bar', mutation_scale=3, mplprops={}, figure=None):
        self.posA = posA
        self.posB = posB
        self.path = path
        self.lw = lw
        self.color = color
        self.arrowstyle = arrowstyle
        self.connectionstyle = connectionstyle
        self.mutation_scale = mutation_scale
        self.mplprops = mplprops
        self.figure = figure

        fancyArrow = patches.FancyArrowPatch(posA, posB, path, arrowstyle, connectionstyle, mutation_scale = self.mutation_scale, color=self.color, lw=lw, **self.mplprops)
        self.matplotlib_obj = fancyArrow

    def __draw__(self, zorder=1):
        p = self.figure.ax.add_patch(self.matplotlib_obj)
        p.set(zorder=zorder)
