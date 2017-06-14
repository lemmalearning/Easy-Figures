import matplotlib.pyplot as plt
import numpy as np


class Circle:
	def __init__(self, radius=1, fill='transparent', center=(0, 0)):
		self.radius = radius
		self.background = background
		self.center = center

class Polygon:
	def __init__(self, vertices, fig, ax):
		print 2
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

			
