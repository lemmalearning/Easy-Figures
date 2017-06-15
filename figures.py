import shapes
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np
from shapes import Polygon, Circle

class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()

	def format_axis(self):
		# Modify the plot view to scale, remove axis, and center our shape
		self.ax.autoscale_view()
		plt.axis('off')
		plt.axis('scaled')


	def __export__(self):
		import StringIO

		self.format_axis()
		export_str = StringIO.StringIO()
		self.fig.savefig(export_str, format='svg')
		export_str.seek(0)  # rewind the data
		return export_str.buf  # this is svg data

	def __writeFile__(self, file_location):
		self.format_axis()
		plt.savefig(file_location)

	def __display__(self):
		self.format_axis()
		plt.show()

	def addPolygon(self, vertices):
		polygon = Polygon.Polygon(vertices, self.fig, self.ax)
		return polygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label=None):
		circle = Circle.Circle(self.fig, self.ax, xy, diameter, radius, label)
		return circle
