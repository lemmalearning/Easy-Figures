import matplotlib.pyplot as plt
from .serial_utils import *

class Line:
	matplotlib_obj = None
	def __init__(self, pointA, pointB, lw, ls, color, clip, mplprops, figure):
		self.matplotlib_obj = None
		self.pointA = pointA
		self.pointB = pointB
		self.lw = lw
		self.ls = ls
		self.color = color
		self.mplprops = mplprops
		self.figure = figure
		self.clip = clip
		self.xyrange=self.figure.xyrange
		if 'solid_capstyle' not in self.mplprops:
			self.mplprops['solid_capstyle'] = 'butt'
		
		x = [self.pointA[0], self.pointB[0]]
		y = [self.pointA[1], self.pointB[1]]
		self.matplotlib_obj = plt.plot(x, y, ls=self.ls, linewidth=self.lw, color=self.color, **self.mplprops)[0]

	def __draw__(self, zorder=1):
		self.matplotlib_obj.set_clip_on(self.clip)
		self.matplotlib_obj.set_zorder(zorder)

	def serialize(self):
		return {
			"type": "Line",
			"start": [float(x) for x in self.pointA],
			"end": [float(x) for x in self.pointB],
			"lineWidth": self.figure.raw2px(self.lw),
			"edgeColor": convert_color(self.matplotlib_obj.get_color()),
			"lineStyle": self.matplotlib_obj.get_linestyle()

			# TODO: What about the clipping
		}
