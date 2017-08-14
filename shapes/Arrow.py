
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Arrow:
	matplotlib_obj = None
	def __init__(self, start, end, headWidth, headLength, lw, mplprops, figure):
		self.figure = figure
		self.mplprops = mplprops


		head_len = headLength*self.figure.UNITS_PER_PIXEL_x # 15 pixels

		head_width = headWidth*self.figure.UNITS_PER_PIXEL_y


		self.matplotlib_obj = self.figure.ax.arrow(
			start[0], start[1], end[0], end[1], lw=lw*self.figure.UNITS_PER_PIXEL_y,
			head_width=head_width, head_length=head_len,
			length_includes_head=True, clip_on=False, **self.mplprops
		)

	def __draw__(self, zorder=1):
		a = self.figure.ax.add_patch(self.matplotlib_obj)
		a.set(zorder=zorder)
