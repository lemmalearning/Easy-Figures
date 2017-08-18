import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
class Axis:
	"""
	Creates an Axis object which contains ticks, spine arrows, and grids.

	__init__ - Creates the object and sets the various class variables
	Ticks - Creates the class variables required for drawing tick marks
	__draw__ - Draws the axis and tick marks according to class variables
	"""
	def __init__(self, hideAxis, grid, arrows, color, lw, minorGrid, label, xlabel, ylabel, mplprops, figure):
		"""
		fig - fig object from matplotlib
		ax - ax object from matplotlib
		hideAxis=False - By default show the axis, but have an option to hide the spines
		xyrange=None - By default inherit the xyrange of the axis from the Figures definition, but take a custom one if a custom spine range is required
		grid=False - By default do not show the grid,
		arrows=True -
		color='black' -
		minorGrid=False -
		"""
		self.hideAxis 	= hideAxis
		self.grid 		= grid
		self.arrows 	= arrows
		self.color 		= color
		self.minorGrid 	= minorGrid
		self.label		= label
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.lw			= lw
		self.mplprops 	= mplprops
		self.ticks 		= None
		self.tickRan	= False

	def Ticks(self, ticks=False, xticks=None, yticks=None, minorticks=False, xminorticks=None, yminorticks=None, fontsize=12, origin=False, top=True):
		self.minorticks = minorticks
		self.xminorticks = xminorticks
		self.yminorticks = yminorticks
		self.xticks = xticks
		self.yticks = yticks
		self.ticks = ticks

		if self.ticks is not None:
			self.xticks = self.yticks = self.ticks
		if self.minorticks is not None:
			self.xminorticks = self.yminorticks = self.minorticks

		if self.minorticks is None and self.ticks is not False:
			self.minorticks = self.xminorticks = self.yminorticks = self.ticks/2.0

		self.fontsize = fontsize
		self.origin = origin
		self.top = top
		self.tickRan = True

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

		if self.figure.xyrange is None:
			plt.axis('off')
			plt.axis('scaled')

		else:
			plt.autoscale(enable=True, axis='y', tight=None)

			self.figure.ax.set_xlim(left=self.figure.xyrange[0][0]+.1 if self.figure.xyrange[0][0]!=0 else self.figure.xyrange[0][0], right=self.figure.xyrange[0][1]-.1, **self.mplprops)
			self.figure.ax.set_ylim(bottom=self.figure.xyrange[1][0]+.1 if self.figure.xyrange[0][0]!=0 else self.figure.xyrange[1][0], top=self.figure.xyrange[1][1]-.1, **self.mplprops)

			self.figure.ax.spines['right'].set_color('none')
			self.figure.ax.spines['top'].set_color('none')

			self.figure.ax.spines['left'].set_position(('data', 0))
			self.figure.ax.spines['bottom'].set_position(('data', 0))



		[i.set_linewidth(self.lw) for i in self.figure.ax.spines.itervalues()]

		if self.hideAxis:
			plt.axis('off')
			return

		if self.arrows:
			xmin, xmax = self.figure.ax.get_xlim()
			ymin, ymax = self.figure.ax.get_ylim()

			head_len_x = 9*self.figure.UNITS_PER_PIXEL_x # 15 pixels
			head_len_y = 9*self.figure.UNITS_PER_PIXEL_y # 15 pixels

			head_width_x = 5*self.figure.UNITS_PER_PIXEL_y
			head_width_y = 5*self.figure.UNITS_PER_PIXEL_x
			#print xmin, xmax, ymin, ymax

			self.figure.ax.arrow(
				0,0, xmax+(self.figure.px2unit(5, 'x')), 0, lw=self.lw,
				head_width=head_width_x, head_length=head_len_x, color=self.color,
				length_includes_head=True, clip_on=False
			)
			self.figure.ax.arrow(
				0,0, 0, ymax+(self.figure.px2unit(5, 'x')), lw=self.lw,
				head_width=head_width_y, head_length=head_len_y, color=self.color,
				length_includes_head=True, clip_on=False
			)

			if self.label:
				x_dim = self.figure.addText((xmax+self.figure.px2unit(10, 'x'), 25*self.figure.UNITS_PER_PIXEL_y), self.xlabel, latex=True,
					fontsize=15, valignment='top', halignment='right',
					bbox=dict(
						boxstyle='round', facecolor=self.figure.bgcolor,
						edgecolor='none', pad=0.03
					)
				)
				y_dim = self.figure.addText((15*self.figure.UNITS_PER_PIXEL_x, ymax+(self.figure.UNITS_PER_PIXEL_y*5)), self.ylabel, latex=True,
					fontsize=15, valignment='top', halignment='center',
					bbox=dict(
						boxstyle='round', facecolor=self.figure.bgcolor,
						edgecolor='none', pad=0.03
					)
				)
				x_dim.__draw__()
				y_dim.__draw__()

		# Control color
		self.figure.ax.spines['bottom'].set_color(self.color)
		self.figure.ax.spines['left'].set_color(self.color)

		####### DRAW LABELS #######
		# Control ticks

		if self.tickRan == False:
			self.ticks = self.xticks = self.yticks = 1
			self.minorticks = self.xminorticks = self.yminorticks = 1
			self.origin=False
			self.top=True
			self.fontsize=12
		if isinstance(self.ticks, int) and isinstance(self.minorticks, int) and self.ticks > self.minorticks:
			self.minorGrid = True

		tick_props = [self.ticks, self.xticks, self.yticks, self.minorticks, self.xminorticks, self.yminorticks]
		plt.gca().xaxis.set_major_locator(plt.MultipleLocator(self.xticks) if self.xticks is not False else plt.NullLocator())
		plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(self.xminorticks) if self.xminorticks is not False else plt.NullLocator())
		plt.gca().yaxis.set_major_locator(plt.MultipleLocator(self.yticks) if self.yticks is not False else plt.NullLocator())
		plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(self.yminorticks) if self.yminorticks is not False else plt.NullLocator())

		self.figure.ax.tick_params(axis='both', which='major', labelsize=self.fontsize)

		if any([True for tick in tick_props if tick!=False]):
			if self.origin:
				ylabels = [int(item) if int(item) is not 0 else "" for item in self.figure.ax.get_yticks().tolist()]
				xlabels = [int(item) if int(item) is not 0 else "        (0,0)" for item in self.figure.ax.get_xticks().tolist()]
				self.figure.ax.set_yticklabels(ylabels)
				self.figure.ax.set_xticklabels(xlabels)
			else:
				xlabels = [int(item) if int(item) is not 0 else "" for item in self.figure.ax.get_xticks().tolist()]
				ylabels = [int(item) if int(item) is not 0 else "" for item in self.figure.ax.get_yticks().tolist()]

			self.figure.ax.set_yticklabels(ylabels)
			self.figure.ax.set_xticklabels(xlabels)

			for label in self.figure.ax.xaxis.get_ticklabels():
				label.set_bbox(dict(boxstyle='round', facecolor=self.figure.bgcolor, edgecolor='none', pad=0.1))

			for label in self.figure.ax.yaxis.get_ticklabels():
				label.set_bbox(dict(boxstyle='round', facecolor=self.figure.bgcolor, edgecolor='none', pad=0.1))

		if self.top:
			self.figure.ax.xaxis.set_label_position('top')

		if self.grid is not False:
			self.figure.ax.grid(which='major', color='k' if self.grid == True else self.grid, linestyle='dashed', linewidth=.5, alpha=0.5)
		if self.minorGrid is not False:
			self.figure.ax.grid(which='minor', color='k' if self.minorGrid == True else self.minorGrid, linestyle='dashed', linewidth=.3, alpha=0.25)


		####### END DRAW LABELS #######

		self.figure.ax.xaxis.set_zorder(zorder)
		self.figure.ax.yaxis.set_zorder(zorder)
