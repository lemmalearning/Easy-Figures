import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Text:
	matplotlib_obj = None
	def __init__(self, fig, ax, xy, text, color="black", fontsize=12, halignment='center', valignment='top', bbox={}, latex=True):
		if not isinstance(color, list):
			color = [color]
			xy = [xy]
			text = [text]
			halignment = [halignment]
			valignment = [valignment]
			bbox = [bbox]
			latex = [latex]

			self.fig = fig
			self.ax = ax
			self.xy = xy
			self.text = text
			self.color=color
			self.fontsize = fontsize
			self.halignment = halignment
			self.valignment = valignment
			self.bbox = bbox
			self.latex = latex

		for xy, text, color, valignment, halignment, bbox, latex in zip(self.xy, self.text, self.color, self.valignment, self.halignment, self.bbox, self.latex):
			self.ax.annotate("$"+text+"$" if latex else text, usetex=True, xytext=xy, xy=xy, fontsize=fontsize, horizontalalignment=halignment, verticalalignment=valignment, bbox=bbox, color=color)


	def __draw__(self, zorder=1):
		for xy, text, color, valignment, halignment, bbox, latex in zip(self.xy, self.text, self.color, self.valignment, self.halignment, self.bbox, self.latex):
			self.ax.annotate("$"+text+"$" if latex else text, usetex=self.latex, xytext=xy, xy=xy, fontsize=self.fontsize, horizontalalignment=halignment, verticalalignment=valignment, bbox=bbox, color=color, zorder=zorder)
