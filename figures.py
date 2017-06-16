import shapes
import matplotlib
matplotlib.use('Agg') # Change renderer so it doesn't use the GUI
matplotlib.rcParams['mathtext.fontset'] = 'cm' # Change font to Computer Modern (LaTeX font)
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [10,10]
import numpy as np
from shapes import Polygon, Circle, Ellipse

class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()

	def add_text(self, xy, text, color="black", fontsize=25, alignment='center'):
		raise Exception('Not implemented yet!')

	def add_function(self, functions, xyranges, colors='black', linewidth=2):
		color_dict = {
			"blue": 'b',
			"green": 'g',
			"red": 'r',
			"cyan": 'c',
			"magenta": 'm',
			"yellow": 'y',
			"black": 'k',
			"white": 'w'
		}

		if not isinstance(functions, list):
			functions = [functions]
			xyranges = [xyranges]
			colors = [colors]

		for function, xyrange, color in zip(functions, xyranges, colors):
			x = np.linspace(xyrange[0][0], xyrange[0][1], 100)
			y = function(x)
			self.ax.plot(x, y, color_dict[color])

	def format_axis(self, xyrange=None, arrows=False, tick_label_interval=1, tick_interval=1, grid=False, arrow=True, color='black'):
		# TODO:
		    # Expose color of axis to user
			# Get rid of margins
			# Consecutive integers for ticks by default
			# Don't show numbers for all ticks

		# Modify the plot view to scale, remove axis, and center our shape

		color_dict = {
			"blue": 'b',
			"green": 'g',
			"red": 'r',
			"cyan": 'c',
			"magenta": 'm',
			"yellow": 'y',
			"black": 'k',
			"white": 'w'
		}

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

		if xyrange == None:
			plt.axis('off')
			plt.axis('scaled')
		else:
			plt.gca().set_aspect('equal', adjustable='box')
			self.ax.set_xlim(left=xyrange[0][0], right=xyrange[0][1])
			self.ax.set_ylim(bottom=xyrange[1][0], top=xyrange[1][1])

			self.ax.spines['right'].set_color('none')
			self.ax.spines['top'].set_color('none')

			self.ax.spines['left'].set_position(('data', 0))
			self.ax.spines['bottom'].set_position(('data', 0))

		if grid:
			self.ax.grid(color='k', linestyle='dashed', linewidth=.5, alpha=0.5)

		if arrow:
			# https://3diagramsperpage.wordpress.com/2014/05/25/arrowheads-for-axis-in-matplotlib/
			xmin, xmax = self.ax.get_xlim()
			ymin, ymax = self.ax.get_ylim()
			# get width and height of axes object to compute
			# matching arrowhead length and width
			dps = self.fig.dpi_scale_trans.inverted()
			bbox = self.ax.get_window_extent().transformed(dps)
			width, height = bbox.width, bbox.height

			# manual arrowhead width and length
			hw = 1./20.*(ymax-ymin)
			hl = 1./20.*(xmax-xmin)
			lw = 1. # axis line width

			# compute matching arrowhead length and width
			yhw = hw/(ymax-ymin)*(xmax-xmin)* height/width
			yhl = hl/(xmax-xmin)*(ymax-ymin)* width/height

			# draw x and y axis
			self.ax.arrow(xmin, 0, xmax-xmin, 0., lw = lw,
			         head_width=tick_interval, head_length=tick_interval,
			         length_includes_head=True, clip_on=False,color=color_dict[color])

			self.ax.arrow(0, ymin, 0., ymax-ymin, lw = lw,
			         head_width=tick_interval, head_length=tick_interval,
					 length_includes_head=True, clip_on=False,color=color_dict[color])
		# Control ticks
		self.ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(tick_label_interval))
		self.ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(tick_label_interval))
		self.ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(tick_interval))
		self.ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(tick_interval))

		# Control color
		self.ax.spines['bottom'].set_color(color_dict[color])
		self.ax.spines['left'].set_color(color_dict[color])

		self.fig.tight_layout()

	def __export__(self):
		import StringIO

		export_str = StringIO.StringIO()
		self.fig.savefig(export_str, format='svg', bbox_inches='tight')
		export_str.seek(0)  # rewind the data
		return export_str.buf  # this is svg data

	def __writeFile__(self, file_location):
		plt.savefig(file_location, bbox_inches='tight')

	def __display__(self):
		plt.show()

	def addPolygon(self, vertices):
		polygon = Polygon.Polygon(vertices, self.fig, self.ax)
		return polygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label=None):
		circle = Circle.Circle(self.fig, self.ax, xy, diameter, radius, label)
		return circle

	def addEllipse(self, xy=(0,0), width=None, height=None, wlabel=None, hlabel=None, dwidth=None, dheight=None):
		ellipse = Ellipse.Ellipse(self.fig, self.ax, xy, width, height, wlabel, hlabel, dwidth, dheight)
		return ellipse
