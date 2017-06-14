import shapes
import StringIO
import matplotlib.pyplot as plt
import numpy as np


class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()

		'''
		self.addPolygon(np.matrix([
			[550, 450],
			[455, 519],
			[491, 631],
			[609, 631],
			[645, 519]
		]))
		'''

		# Modify the plot view to scale, remove axis, and center our shape



	def __export__(self):
		export_str = StringIO.StringIO()
		fig.savefig(export_str, format='svg')
		export_str.seek(0)  # rewind the data
		return export_str.buf  # this is svg data

	def __writeFile__(self, file_location):
		self.ax.autoscale_view()
		plt.axis('off')
		plt.axis('scaled')
		plt.savefig(file_location)



	def addPolygon(self, vertices):
		print 1
		self.polygon = shapes.Polygon(vertices, self.fig, self.ax)
		#return polygon
