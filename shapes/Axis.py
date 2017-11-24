import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import math

class Axis:
	"""
	Creates an Axis object which contains ticks, spine arrows, and grids.

	__init__ - Creates the object and sets the various class variables
	Ticks - Creates the class variables required for drawing tick marks
	__draw__ - Draws the axis and tick marks according to class variables
	"""
	def __init__(self, hideAxis, arrows, color, lw, label, xlabel, ylabel, mplprops, figure):
		"""
		hideAxis=False - By default show the axis, but have an option to hide the spines
		xyrange=None - By default inherit the xyrange of the axis from the Figures definition, but take a custom one if a custom spine range is required
		arrows=True -
		color='black' -
		"""
		self.hideAxis 	= hideAxis
		self.arrows 	= arrows
		self.color 		= color
		self.label		= label
		if not self.label:
			figure.padding=0
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.lw			= lw if not self.hideAxis else 0
		self.mplprops 	= mplprops
		self.ticks 		= None

	def serialize(self):
		return {
			"showXAxis": (not self.hideAxis),
			"showYAxis": (not self.hideAxis),
			"showLabels": self.label,
			"showArrows": self.arrows
			# TODO: color, lw, label, xlabel, ylabel
		}

	def __draw__(self, zorder=1):
		# set the aspect ratio
		self.figure.ax.set_aspect(self.figure.aspectRatio)
		# Modify the plot view to scale, remove axis, and center our shape
		def adjust_spines(ax, spines):
			for loc, spine in ax.spines.items():
				if loc in spines:
					spine.set_position(('outward', 10))  # outward by 10 points
					spine.set_smart_bounds(True)
					#spine.set_color('k')
				else:
					spine.set_color('none')  # don't draw spine

			# turn off ticks where there is no spine
			if 'left' in spines:
				ax.yaxis.set_ticks_position('left')
			else:
				# no yaxis ticks
				ax.yaxis.set_ticks([])

			if 'bottom' in spines:
				ax.xaxis.set_ticks_position('bottom')
			else:
				# no xaxis ticks
				ax.xaxis.set_ticks([])

		self.figure.ax.set_xlim(left=self.figure.xyrange[0][0], right=self.figure.xyrange[0][1], **self.mplprops)
		self.figure.ax.set_ylim(bottom=self.figure.xyrange[1][0], top=self.figure.xyrange[1][1], **self.mplprops)

		self.figure.ax.spines['right'].set_color('none')
		self.figure.ax.spines['top'].set_color('none')

		if self.figure.xyrange[0][0] > 0:
			self.figure.ax.spines['left'].set_position(('data', self.figure.xyrange[0][0]))
		else:
			self.figure.ax.spines['left'].set_position(('data', 0))

		if self.figure.xyrange[1][0] > 0:
			self.figure.ax.spines['bottom'].set_position(('data', self.figure.xyrange[1][0]))
		else:
			self.figure.ax.spines['bottom'].set_position(('data', 0))


		[i.set_linewidth(self.lw) for i in self.figure.ax.spines.itervalues()]


		if self.arrows and not self.hideAxis:
			xmin, xmax = self.figure.ax.get_xlim()
			ymin, ymax = self.figure.ax.get_ylim()

			head_len_x = self.figure.px2unit(9, 'x')
			head_len_y = self.figure.px2unit(9, 'y')

			head_width_x = self.figure.px2unit(5, 'x')
			head_width_y = self.figure.px2unit(5, 'y')


			arrow_x = self.figure.addArrow(
				(xmin if xmin>0 else 0,ymin if ymin>0 else 0), (xmax+(self.figure.px2unit(5, 'x')), ymin if ymin>0 else 0),
				lw=self.lw, head_width=head_width_y, head_length=head_len_x, color=self.color, length_includes_head=True, clip_on=False,
				clip=False, add=False
			)
			arrow_x.__draw__(zorder=zorder)
			arrow_y = self.figure.addArrow(
				(xmin if xmin>0 else 0,ymin if ymin>0 else 0), (xmin if xmin>0 else 0, ymax+(self.figure.px2unit(5, 'y'))),
				lw=self.lw,	head_width=head_width_x, head_length=head_len_y, color=self.color, length_includes_head=True, clip_on=False,
				clip=False, add=False
			)
			arrow_y.__draw__(zorder=zorder)

			if self.label and not self.hideAxis:
				x_dim = self.figure.addText((xmax+self.figure.px2unit(25, 'x'), ymin if ymin > 0 else 0+self.figure.px2unit(25, 'y')), self.xlabel, latex=True,
					fontsize=15, valignment='top', halignment='right', add=False,
					bbox=dict(
						boxstyle='round', facecolor=self.figure.bgcolor,
						edgecolor='none', pad=0.03
					)
				)
				y_dim = self.figure.addText((xmin if xmin > 0 else 0+self.figure.px2unit(15, 'x'), ymax+(self.figure.px2unit(25, 'y'))), self.ylabel, latex=True,
					fontsize=15, valignment='top', halignment='center', add=False,
					bbox=dict(
						boxstyle='round', facecolor=self.figure.bgcolor,
						edgecolor='none', pad=0.03
					)
				)
				x_dim.__draw__(zorder=zorder)
				y_dim.__draw__(zorder=zorder)

		# Control color
		self.figure.ax.spines['bottom'].set_color(self.color)
		self.figure.ax.spines['left'].set_color(self.color)


		if self.hideAxis:
			self.figure.ax.spines['bottom'].set_color(self.figure._BG)
			self.figure.ax.spines['left'].set_color(self.figure._BG)
			xlabels = ["" for item in self.figure.ax.get_xticks()]
			ylabels = ["" for item in self.figure.ax.get_yticks()]
			self.figure.ax.set_yticklabels(ylabels)
			self.figure.ax.set_xticklabels(xlabels)
			plt.gca().xaxis.set_major_locator(plt.NullLocator())
			plt.gca().xaxis.set_minor_locator(plt.NullLocator())
			plt.gca().yaxis.set_major_locator(plt.NullLocator())
			plt.gca().yaxis.set_minor_locator(plt.NullLocator())

		for k, spine in self.figure.ax.spines.items():  # ax.spines is a dictionary
			spine.set_zorder(zorder)
