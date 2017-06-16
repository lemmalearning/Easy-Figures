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

	def format_axis(self, xyrange=None, arrows=False, ticks=[], grid=False, function=None):
		# Modify the plot view to scale, remove axis, and center our shape
		self.ax.autoscale_view()
		if xyrange == None:
			plt.axis('off')
		else:
			self.ax.set_xlim([xyrange[0][0],xyrange[0][1]])
			self.ax.set_ylim([xyrange[1][0],xyrange[1][1]])
			#plt.gca().set_aspect('equal', adjustable='box')
			plt.axis('equal')
			if function is not None:
				x = np.linspace(xyrange[0][0], xyrange[0][1], 100)
				y = function(x)
				plt.plot(x, y)

		plt.axis('scaled')



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

	def addEllipse(self, xy=(0,0), width=None, height=None, wlabel=None, hlabel=None, is_radius=None):
		ellipse = Ellipse.Ellipse(self.fig, self.ax, xy, width, height, wlabel, hlabel, is_radius)
		return ellipse
