import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Polygon:
	def __init__(self, vertices, fig, ax):
		self.vertices = vertices
		self.fig = fig
		self.ax = ax
		# Define the polygon
		polygon = plt.Polygon(vertices, fill=False, linewidth=3)
		# Create and add polygon
		ax.add_patch(polygon)

	def labelVertices(self, label_list):
		# Everything is the counter clockwise, and the first angle/vertex is the first lable, everything else is counter clockwise order
		# The side that's mentioned first is horizontal
		self.labels = label_list
		for i, label in enumerate(self.labels):
			self.ax.text(self.vertices[i, 0], self.vertices[i, 1], '$'+label+'$', fontsize=15)
