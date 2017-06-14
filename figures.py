import shapes
import StringIO
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



	def addPolygon(self, vertices):
		self.polygon = shapes.Polygon(vertices, self.fig, self.ax)
		return polygon
