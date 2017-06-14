import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class Circle:
	def __init__(self, fig, ax, xy=(0,0), diameter=None, radius=None, label=None):
		if radius!=None:
			circle = patches.Circle(xy, radius=radius, fill=False, linewidth=3)

			p = (xy[0]+radius, xy[1])

			plt.plot([xy[0],p[0]], [xy[1],p[1]], linewidth=2, ls='dashed', color='black')

			mid_radius = (xy[0]+p[0])/2.0
			textobj = plt.text(mid_radius, xy[1]+100, "$"+label+"$", fontsize=25)

			bb = textobj.get_axes().get_window_extent()

			textobj.set_position((mid_radius-(bb.width/2.0), xy[1]+100))

		else:
			circle = patches.Circle(xy, radius=diameter, fill=False, linewidth=3)

			p1 = (xy[0]-diameter, xy[1])
			p2 = (xy[0]+diameter, xy[1])

			plt.plot([p1[0],p2[0]], [p1[1],p2[1]], linewidth=2, ls='dashed', color='black')

			textobj = plt.text(xy[0], xy[1]+100, "$"+label+"$", fontsize=25)

			bb = textobj.get_axes().get_window_extent()

			textobj.set_position((xy[0]-(bb.width/2.0), xy[1]+100))

		ax.add_patch(circle)

class Ellipse:
	def __init__(self, fig, ax, xy=(0,0), w_diameter=None, h_diameter=None, w_radius=None, h_radius=None, w_label=None, h_label=None):
		if w_radius!=None:
			ellipse = patches.Ellipse(xy, width, height, angle=0.0, fill=False, linewidth=3)

			w_p = (xy[0]+w_radius, xy[1])
			h_p = (xy[0], xy[1]+h_radius)

			plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

			mid_w_radius = (xy[0]+w_p[0])/2.0
			mid_h_radius = (xy[0]+h_p[0])/2.0
			textobj = plt.text(mid_w_radius, xy[1]+100, "$"+label+"$", fontsize=25)
			textobj = plt.text(mid_h_radius+100, xy[1], "$"+label+"$", fontsize=25)

			bb = textobj.get_axes().get_window_extent()

			textobj.set_position((mid_x_radius-(bb.width/2.0), xy[1]+100))
			textobj.set_position((mid_y_radius-(bb.width/2.0), xy[1]+100))

		else:
			ellipse = patches.Ellipse(xy, width, height, angle=0.0, fill=False, linewidth=3)

			w_p1 = (xy[0]+w_radius, xy[1])
			w_p2 = (xy[0]-w_radius, xy[1])
			h_p1 = (xy[0], xy[1]+h_radius)
			h_p2 = (xy[0], xy[1]-h_radius)

			plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

			textobj = plt.text(xy[0], xy[1]+100, "$"+label+"$", fontsize=25)
			textobj = plt.text(xy[0]+100, xy[1], "$"+label+"$", fontsize=25)

			bb = textobj.get_axes().get_window_extent()

			textobj.set_position((xy[0]-(bb.width/2.0), xy[1]+100))
			#textobj.set_position((xy[0]-(bb.width/2.0), xy[1]+100))

		ax.add_patch(circle)

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
