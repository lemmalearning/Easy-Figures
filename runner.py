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
	t = figures.Figures()
	#poly = t.addCircle(xy=(5,4),label="Q", diameter=1)
    #circ = t.addCircle(xy=(7,10), label="r", radius=4)
	#ellr = t.addEllipse(xy=(10,12), width=50, height=70, wlabel="r", hlabel="h") #hlabel ok
	ellr1 = t.addEllipse(xy=(60030,59004), width=57, height=24, wlabel="r", hlabel="h", is_radius=0) 

	t.format_axis()
	t.__writeFile__('/Users/chloesheen/test.svg')

	return None

if __name__ == "__main__":
	main()
