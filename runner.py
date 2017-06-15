import numpy as np
from random import randint
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patches
import figures

def angle_builder(angle=(45*np.pi)/180, rotation=0, translation=(0,0), text=""): # Given a specific angle, generate a right triangle with one angle specified
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

def main():
	f = figures.Figures()
	#poly = f.addCircle(xy=(5,4),label="Q", diameter=1)
	circ = f.addCircle(xy=(4,3), label="r", radius=4)
	#ell = f.addEllipse(xy=(6,12), width=5, height=8, wlabel="r", hlabel="h")
    #ell2 = f.addEllipse(xy=(6,12), dwidth=5, dheight=8, wlabel="r", hlabel="h")
	f.format_axis(xyrange=[[-5,5],[-5,5]], arrows=False, ticks=[], grid=False, function=None)
	f.__writeFile__('/Users/ajpersinger/test.svg')

	return None

if __name__ == "__main__":
	main()
