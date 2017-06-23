import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Polygon:
	matplotlib_obj = None
	def __init__(self, fig, ax, vertices, pixelSize=400, figure=None):
		self.vertices = np.matrix(vertices)
		self.fig = fig
		self.ax = ax
		# Define the polygon
		self.matplotlib_obj = plt.Polygon(vertices, fill=False, linewidth=2)
		self.pixelSize = pixelSize
		self.figure = figure
		# Create and add polygon

	def labelSides(self, labelList):
		self.sideLabels = labelList
		vertices_pairs = sorted(self.vertices.tolist(), key=lambda element: (element[0], element[1]))
		vertices_pairs=self.vertices.tolist() + [self.vertices.tolist()[0]]

		centroid = np.mean(self.vertices, axis=0)

		for i, vertex in enumerate(vertices_pairs[:-1]):
			x = (vertex[0] + vertices_pairs[i+1][0])/2
			y = (vertex[1] + vertices_pairs[i+1][1])/2
			d = np.matrix([x,y]) - centroid

			x = x+self.figure.UNITS_PER_PIXEL_x*5 if d[0,0] > 1 else x-self.figure.UNITS_PER_PIXEL_x*5
			y = y+self.figure.UNITS_PER_PIXEL_y*5 if d[0, 1] > 1 else y-self.figure.UNITS_PER_PIXEL_y*5

			hA = "right" if d[0,0] < 0 else "top"
			vA = "top" if d[0, 1] < 0 else "center"
			if d[0,0] > 0 and d[0, 1] > 0:
				x +=self.figure.UNITS_PER_PIXEL_x*5
				y +=self.figure.UNITS_PER_PIXEL_y*5
				vA = "right"

			self.figure.addText((x,y), self.sideLabels[i], fontsize=.0625*self.pixelSize, latex=True,
				halignment=hA,valignment=vA)

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

	def labelAngles(self, labelList):
		# Everything is the counter clockwise, and the first angle/vertex is the first lable, everything else is counter clockwise order
		# The side that's mentioned first is horizontal
		self.labels = labelList

		centroid = np.mean(self.vertices, axis=0)

		for i, label in enumerate(self.labels):
			d = self.vertices[i, :] - centroid
			v = self.vertices[i, :] - .1*np.linalg.norm(d)*d
			print label, d, v

			self.ax.text(v[0, 0], v[0, 1], '$'+label+'$', fontsize=8, \
				horizontalalignment=("left" if d[0,0] < 0 else "right"), \
				verticalalignment=("bottom" if d[0, 1] < 0 else "top") \
			)

	def __draw__(self, zorder=1):
		p = self.ax.add_patch(self.matplotlib_obj)
		p.set(zorder=zorder)
