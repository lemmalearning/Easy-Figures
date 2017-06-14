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

class Polygon:
	def __init__(self, vertices, fig, ax):
		# Define the polygon
		polygon = plt.Polygon(vertices, fill=False, linewidth=3)


		# Create and add polygon
		ax.add_patch(polygon)

		# To calculate centroid, first calculate area:
		#	Mean of vertices
		vertix_mean = np.mean(vertices, axis=0)
		plt.plot([vertix_mean[0, 0]], [vertix_mean[0, 1]], marker='o', markersize=3, color="red")

		# Plot the vectors from centroid to vertices
		segs = vertices - vertix_mean
		for i in range(0, segs.shape[0]):
			ax.text(vertices[i, 0], vertices[i, 1], '$'+str(i)+'$', fontsize=15)
