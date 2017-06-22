import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Polygon:
	matplotlib_obj = None
	def __init__(self, vertices, fig, ax):
		self.vertices = np.matrix(vertices)
		self.fig = fig
		self.ax = ax
		# Define the polygon
		self.matplotlib_obj = plt.Polygon(vertices, fill=False, linewidth=2)
		# Create and add polygon

	def labelVertices(self, labelList):
		# Everything is the counter clockwise, and the first angle/vertex is the first lable, everything else is counter clockwise order
		# The side that's mentioned first is horizontal
		self.labels = labelList

		centroid = np.mean(self.vertices, axis=0)

		for i, label in enumerate(self.labels):
			d = self.vertices[i, :] - centroid
			v = self.vertices[i, :] + 0.001*np.linalg.norm(d)*d

			self.ax.text(v[0, 0], v[0, 1], '$'+label+'$', fontsize=20, \
				horizontalalignment=("right" if d[0,0] < 0 else "left"), \
				verticalalignment=("top" if d[0, 1] < 0 else "bottom") \
			)

	def __draw__(self, zorder=1):
		p = self.ax.add_patch(self.matplotlib_obj)
		p.set(zorder=zorder)
