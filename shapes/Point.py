import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Point:
	matplotlib_obj = None
	def __init__(self, xys, texts, pointsize, style, fontsize, color, latex, mplprops, figure):
		if not isinstance(color, list):
			color = [color]
			xys = [xys]
			texts = [texts]
			style=[style]

		self.xys = xys
		self.color = color
		self.texts = texts
		self.pointsize = pointsize
		self.fontsize = fontsize
		self.latex = latex
		self.style=style
		self.figure = figure
		self.mplprops = mplprops

	def __draw__(self, zorder=1):
		for xy, text, color, style in zip(self.xys, self.texts, self.color, self.style):
			plt.plot(xy[0], xy[1], style, color=color, ms=self.pointsize, zorder=zorder)
			self.figure.addText(xy, text, latex=self.latex, color='black',
			                    fontsize=self.fontsize, offset=[self.pointsize+5, self.pointsize+5]
			                    )
