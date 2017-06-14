import matplotlib.pyplot as plt

plt.axes()

circle = plt.Circle((0, 0), radius=0.75, fc='y')
plt.gca().add_patch(circle)
plt.axis('off')
plt.axis('scaled')

#plt.show()
plt.figure().savefig('/Users/ajpersinger/test.png', transparent=True)


class Circle():
	def __init__(radius=1, fill='transparent', center=(0, 0)):
		self.radius = radius
		self.background = background
		self.center = center

class Polygon():
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
			ax.text(vertices[i, 0], vertices[i, 1], '$'+i+'$', fontsize=15)
			#plt.plot([vertix_mean[0, 0], vertices[i, 0]], [vertix_mean[0, 1], vertices[i, 1]])
			#print [vertix_mean[0, 0], vertices[i, 0]], [vertix_mean[0, 1], vertices[i, 1]]
			#t = plt.text(550, 450, r'$\alpha$', fontsize=20)
			#bb = t.get_window_extent(renderer='SVG')
			#width = bb.width
			#height = bb.height
			#text.set_position((event.xdata, event.ydata))
			#x = (vertix_mean[0, 1] - vertices[i, 1])/(vertix_mean[0, 0] - vertices[i, 0])
