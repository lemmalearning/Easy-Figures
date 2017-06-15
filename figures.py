import shapes
import matplotlib
matplotlib.use('Agg') # Change renderer so it doesn't use the GUI
matplotlib.rcParams['mathtext.fontset'] = 'cm' # Change font to Computer Modern (LaTeX font)
import matplotlib.pyplot as plt
import numpy as np
from shapes import Polygon, Circle, Ellipse

class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()

	def add_text(self, xy, text, color="black", fontsize=25):
		raise Exception('Not implemented yet')

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

	def format_axis(self, xyrange=None, arrows=False, ticks=[], grid=False):
		# TODO:
		    # Expose color of axis to user
			# Get rid of margins
			# Consecutive integers for ticks by default
			# Don't show numbers for all ticks

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

		#self.ax.autoscale_view()
		if xyrange == None:
			plt.axis('off')
			plt.axis('scaled')
		else:
			plt.gca().set_aspect('equal', adjustable='box')
			self.ax.set_xlim(left=xyrange[0][0], right=xyrange[0][1])
			self.ax.set_ylim(bottom=xyrange[1][0], top=xyrange[1][1])
			self.ax.spines['left'].set_position('center')
			self.ax.spines['right'].set_color('none')
			self.ax.spines['bottom'].set_position('center')
			self.ax.spines['top'].set_color('none')

		self.fig.tight_layout()

	def __export__(self):
		import StringIO

		export_str = StringIO.StringIO()
		self.fig.savefig(export_str, format='svg')
		export_str.seek(0)  # rewind the data
		return export_str.buf  # this is svg data

	def __writeFile__(self, file_location):
		plt.savefig(file_location)

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
