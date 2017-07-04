
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Arrow:
	matplotlib_obj = None
	def __init__(self, xy, dxdy, color='black', headWidth=0.1, width=0.35, lw=2, mplprops={}, figure=None):
		self.figure = figure
		self.lw = lw
		self.mplprops = mplprops
		self.matplotlib_obj = figure.ax.arrow(xy[0], xy[1], dxdy[0], dxdy[1], length_includes_head=True, width=width, head_width=headWidth, head_length=2*headWidth, lw=lw, fc=color, ec=color, **self.mplprops)

	def __draw__(self, zorder=1):
		a = self.figure.ax.add_patch(self.matplotlib_obj)
		a.set(zorder=zorder)
