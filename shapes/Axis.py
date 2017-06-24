import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import Text

class Axis:
	"""
	Creates an Axis object which contains ticks, spine arrows, and grids.

	__init__ - Creates the object and sets the various class variables
	Ticks - Creates the class variables required for drawing tick marks
	__draw__ - Draws the axis and tick marks according to class variables
	"""
	def __init__(self, hideAxis=False, grid=False, arrows=True, color='black', minorGrid=False, label=True, figure=None):
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
		self.figure    = figure

	def Ticks(self, tickLabelInterval=1, tickInterval=1, fontsize=12, origin=False, top=True):
		self.tickInterval = tickInterval
		self.tickLabelInterval = tickLabelInterval
		self.fontsize = fontsize
		self.origin = origin
		self.top = top

	def __draw__(self, zorder=1):
		# Modify the plot view to scale, remove axis, and center our shape
		def adjust_spines(ax, spines):
		    for loc, spine in ax.spines.items():
		        if loc in spines:
		            spine.set_position(('outward', 10))  # outward by 10 points
		            spine.set_smart_bounds(True)
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
			plt.gca().set_aspect('equal', adjustable='box')

			self.figure.ax.set_xlim(left=self.figure.xyrange[0][0]+.1 if self.figure.xyrange[0][0]!=0 else self.figure.xyrange[0][0], right=self.figure.xyrange[0][1]-.1)
			self.figure.ax.set_ylim(bottom=self.figure.xyrange[1][0]+.1 if self.figure.xyrange[0][0]!=0 else self.figure.xyrange[1][0], top=self.figure.xyrange[1][1]-.1)

			self.figure.ax.spines['right'].set_color('none')
			self.figure.ax.spines['top'].set_color('none')

			self.figure.ax.spines['left'].set_position(('data', 0))
			self.figure.ax.spines['bottom'].set_position(('data', 0))

		if self.hideAxis:
			plt.axis('off')
			return


		if self.grid is not False:
			self.figure.ax.grid(which='major', color='k' if self.grid == True else self.grid, linestyle='dashed', linewidth=.5, alpha=0.5)
			if self.minorGrid is not False:
				self.figure.ax.grid(which='minor', color='k' if self.minorGrid == True else self.minorGrid, linestyle='dashed', linewidth=.3, alpha=0.25)


		if self.arrows:
			#xyrange/pixelrange = unitsperpixel * pixels = units
			UNITS_PER_PIXEL_x = ((0-self.figure.xyrange[0][0]) + (self.figure.xyrange[0][1]))/self.pixelSize
			UNITS_PER_PIXEL_y = ((0-self.figure.xyrange[1][0]) + (self.figure.xyrange[1][1]))/self.pixelSize

			xmin, xmax = self.ax.get_xlim()
			ymin, ymax = self.ax.get_ylim()

			self.figure.ax.arrow(xmin, 0, xmax-xmin, 0., lw = 1,
			         head_width=UNITS_PER_PIXEL_x*.05/1.6, head_length=UNITS_PER_PIXEL_x*5,
			         length_includes_head=True, clip_on=False,color=self.color)

			self.figure.ax.arrow(0, ymin, 0., ymax-ymin, lw = 1,
			         head_width=UNITS_PER_PIXEL_y*.05/1.6, head_length=UNITS_PER_PIXEL_y*5,
					 length_includes_head=True, clip_on=False,color=self.color)

		# Control color
		self.figure.ax.spines['bottom'].set_color(self.color)
		self.figure.ax.spines['left'].set_color(self.color)

		if self.label:
			#size conversion: Should be 12 for every 400 pixels, or .003 per pixel
			Text.Text(self.figure.fig, self.figure.ax, ((self.figure.xyrange[0][1])-0.09, -0.09),'x', latex=True, fontsize=.03*self.figure.width).__draw__()
			Text.Text(self.figure.fig, self.figure.ax, (-0.3, (self.figure.xyrange[1][1])-0.1), 'y', latex=True, fontsize=.03*self.figure.width).__draw__()

		####### DRAW LABELS #######
		# Control ticks
		self.figure.ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(self.tickLabelInterval))
		self.figure.ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(self.tickLabelInterval))
		self.figure.ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(self.tickInterval))
		self.figure.ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(self.tickInterval))
		self.figure.ax.tick_params(axis='both', which='major', labelsize=self.fontsize)


		if self.top:
			self.figure.ax.xaxis.set_label_position('top')

		if self.origin:
			ylabels = [int(item) if int(item) is not 0 else "" for item in self.ax.get_yticks().tolist()]
			xlabels = [int(item) if int(item) is not 0 else "        (0,0)" for item in self.ax.get_xticks().tolist()]
			self.figure.ax.set_yticklabels(ylabels)
			self.figure.ax.set_xticklabels(xlabels)
		else:
			xlabels = [int(item) if int(item) is not 0 else "" for item in self.ax.get_xticks().tolist()]
			ylabels = [int(item) if int(item) is not 0 else "" for item in self.ax.get_yticks().tolist()]
			self.figure.ax.set_yticklabels(ylabels)
			self.figure.ax.set_xticklabels(xlabels)

			for label in self.figure.ax.xaxis.get_ticklabels():
				label.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))
			for label in self.figure.ax.yaxis.get_ticklabels():
				label.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))
		####### END DRAW LABELS #######

		self.figure.ax.xaxis.set_zorder(zorder)
		self.figure.ax.yaxis.set_zorder(zorder)
