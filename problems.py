import numpy as np
from random import randint
import matplotlib
matplotlib.use('Agg')
#import matplotlib.pyplot as plt
from matplotlib import patches
import figures
import time

def problem1(angle=(45*np.pi)/180, rotation=0, translation=(0,0), text=""): # Given a specific angle, generate a right triangle with one angle specified
	fig, ax = plt.subplots()

	# Define the angles and sides
	alpha = angle
	beta = np.pi/2
	gamma = ((np.pi-beta-alpha))

	A = 1
	B = np.sin(beta)/np.sin(alpha)
	C = np.sin(gamma)/np.sin(alpha)

	# Define the vertices
	vertex_A = [0, A]
	vertex_B = [0, 0]
	vertex_C = [C, 0]

	polygon = plt.Polygon([vertex_A, vertex_B, vertex_C], fill=False, linewidth=3)

	ax.text(1, 1, '$\\frac{1}{2}$', fontsize=15)

	# Perform the rotation if at all
	transformation = matplotlib.transforms.Affine2D().translate(translation[0], translation[1]).rotate(rotation) + ax.transData
	polygon.set_transform(transformation)

	# Create and add polygon
	ax.add_patch(polygon)


	# Modify the plot view to scale, remove axis, and center our shape
	ax.autoscale_view()
	plt.axis('off')
	plt.axis('scaled')

	print alpha, beta, gamma, A, B, C
	# Display or Save to file
	#plt.savefig('/Users/ajpersinger/test.svg')
	plt.show()


def problem2(vertices):
	fig, ax = plt.subplots()

	# Define the polygon
	polygon = plt.Polygon(vertices, fill=False, linewidth=3)

	#ax.text(1, 1, '$\\frac{1}{2}$', fontsize=15)

	# Create and add polygon
	ax.add_patch(polygon)

	# To calculate centroid, first calculate area:
	#	Mean of vertices
	vertix_mean = np.mean(vertices, axis=0)
	plt.plot([vertix_mean[0, 0]], [vertix_mean[0, 1]], marker='o', markersize=3, color="red")

	# Plot the vectors from centroid to vertices
	segs = vertices - vertix_mean
	for i in range(0, segs.shape[0]):
		plt.plot([vertix_mean[0, 0], vertices[i, 0]], [vertix_mean[0, 1], vertices[i, 1]])
		print [vertix_mean[0, 0], vertices[i, 0]], [vertix_mean[0, 1], vertices[i, 1]]
		t = plt.text(550, 450, r'$\alpha$', fontsize=20)
		bb = t.get_window_extent(renderer='SVG')
		width = bb.width
		height = bb.height
		#text.set_position((event.xdata, event.ydata))
		#x = (vertix_mean[0, 1] - vertices[i, 1])/(vertix_mean[0, 0] - vertices[i, 0])

	#t = plt.text(550, 450, r'$\alpha$', fontsize=20)
	#bb = t.get_window_extent(renderer=r)
	#width = bb.width
	#height = bb.height
	#text.set_position((event.xdata, event.ydata))


	# Modify the plot view to scale, remove axis, and center our shape
	ax.autoscale_view()
	plt.axis('off')
	plt.axis('scaled')

	# Display or Save to file
	#plt.savefig('/Users/ajpersinger/test.svg')
	plt.show()

def foo(vertices):
	fig, ax = plt.subplots()


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
	#for i in range(0, segs.shape[0]):
	#	ax.text(vertices[i, 0], vertices[i, 1], '$'+str(i)+'$', fontsize=15)



	# Modify the plot view to scale, remove axis, and center our shape
	ax.autoscale_view()
	plt.axis('off')
	plt.axis('scaled')
	plt.show()

def main():
	"""
	problem2(np.matrix([
		[550, 450],
		[455, 519],
		[491, 631],
		[609, 631],
		[645, 519]
	]))

	problem1()
	"""


	t = figures.Figures()
	polygon = t.addPolygon(np.matrix([
		[550, 450],
		[455, 519],
		[491, 631],
		[609, 631],
		[645, 519]
	]))
	polygon.labelVertices(['a', 'b', 'c', 'd', 'e'])
	t.__writeFile__('/Users/ajpersinger/test.svg')
	#t.__display__()

if __name__ == "__main__":
	main()

# find centroid, go in direction of vertex by 1.5*the font size and write there. I.e.
#plt.plot([vertix_mean[0, 0], vertices[i, 0]], [vertix_mean[0, 1], vertices[i, 1]])
#print [vertix_mean[0, 0], vertices[i, 0]], [vertix_mean[0, 1], vertices[i, 1]]
#t = plt.text(550, 450, r'$\alpha$', fontsize=20)
#bb = t.get_window_extent(renderer='SVG')
#width = bb.width
#height = bb.height
#text.set_position((event.xdata, event.ydata))
#x = (vertix_mean[0, 1] - vertices[i, 1])/(vertix_mean[0, 0] - vertices[i, 0])





# Everything is the counter clockwise, and the first angle/vertex is the first lable, everything else is counter clockwise order
# The side that's mentioned first is horizontal
