import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Text:
	matplotlib_obj = None
	def __init__(self, xy, text, color, fontsize, halignment, valignment, bbox, latex, pixel, mplprops, figure):
		if not isinstance(color, list):
			color = [color]
			xy = [xy]
			text = [text]
			halignment = [halignment]
			valignment = [valignment]
			bbox = [bbox]
			latex = [latex]
			pixel = [pixel]
			self.matplotlib_obj = []

			self.xy = xy
			self.text = text
			self.color = color
			self.fontsize = fontsize
			self.halignment = halignment
			self.valignment = valignment
			self.bbox = bbox
			self.latex = latex
			self.figure = figure
			self.mplprops = mplprops
			self.pixel = pixel


	def __draw__(self, zorder=1):
		for xy, text, color, valignment, halignment, bbox, latex, pixel in zip(self.xy, self.text, self.color, self.valignment, self.halignment, self.bbox, self.latex, self.pixel):
			obj = self.figure.ax.text(xy[0] if not pixel else xy[0] * self.figure.UNITS_PER_PIXEL_x,
			                          xy[1] if not pixel else xy[1] * self.figure.UNITS_PER_PIXEL_y,
			                          "$" + text + "$" if latex else text, fontsize=self.fontsize,
			                          horizontalalignment=halignment, verticalalignment=valignment, bbox=bbox,
			                          color=color, zorder=zorder, clip_on=False, **self.mplprops
			                          )
			obj.set_clip_on(False)
			self.matplotlib_obj.append(obj)

