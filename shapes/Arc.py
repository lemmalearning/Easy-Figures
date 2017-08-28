import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Arc:
	def __init__(self, xy, width, height, fc, ec, lw, angle, theta1, theta2, mplprops, figure):
		self.xy = xy
		self.width = width
		self.height = height
		self.angle = angle
		self.theta1 = theta1
		self.theta2 = theta2
		self.lw = lw
		self.mplprops = mplprops
		self.figure = figure
		arc = patches.Arc(xy, width, height, angle, theta1, theta2, fc=fc, ec=ec, lw=lw, **self.mplprops)
		self.matplotlib_obj = arc

	def __draw__(self, zorder=1):
		p = self.figure.ax.add_patch(self.matplotlib_obj)
		p.set(zorder=zorder)
