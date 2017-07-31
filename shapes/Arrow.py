
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Arrow:
	matplotlib_obj = None
	def __init__(self, start, end, headWidth=1, lw=2, mplprops={}, figure=None):
		self.figure = figure
		self.lw = lw
		self.mplprops = mplprops
		self.matplotlib_obj = figure.ax.arrow(start[0], start[1], start[0]+end[0], start[1]+end[1], length_includes_head=True, head_width=headWidth, head_length=2*headWidth, lw=lw, **self.mplprops)

	def __draw__(self, zorder=1):
		a = self.figure.ax.add_patch(self.matplotlib_obj)
		a.set(zorder=zorder)
