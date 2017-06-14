import shapes
import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()

	def format_axis(self):
		# Modify the plot view to scale, remove axis, and center our shape
		self.ax.autoscale_view()
		plt.axis('off')
		plt.axis('scaled')


	def __export__(self):
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
		polygon = shapes.Polygon(vertices, self.fig, self.ax)
		return polygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label=None):
		circle = shapes.Circle(self.fig, self.ax, xy, diameter, radius, label)
		return circle

	def addEllipse(self, fig, ax, xy=(0,0), w_diameter=None, h_diameter=None, w_radius=None, h_radius=None, w_label=None, h_label=None):
		ellipse = shapes.Ellipse(fig, ax, xy, w_diameter, h_diameter, w_radius, h_radius, w_label, h_label)
		return ellipse
