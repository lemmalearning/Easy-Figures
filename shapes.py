import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


class Circle:
	def __init__(self, radius=1, fill='transparent', center=(0, 0)):
		self.radius = radius
		self.background = background
		self.center = center

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
		self.labels = label_list
		for i, label in enumerate(self.labels):
			self.ax.text(self.vertices[i, 0], self.vertices[i, 1], '$'+label+'$', fontsize=15)
