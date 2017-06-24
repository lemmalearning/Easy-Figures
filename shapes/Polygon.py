import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Polygon:
	matplotlib_obj = None
	def __init__(self, vertices, figure=None):
		self.vertices = np.matrix(vertices)
		# Define the polygon
		self.matplotlib_obj = plt.Polygon(vertices, fill=False, linewidth=2)
		self.figure = figure
		# Create and add polygon


	def labelOppositeSides(self, labelList):
		# Number of sides - 1/2  + current index mod number of sides = new index
		numSides = len(self.vertices.tolist())
		const = (numSides-1)/2
		newLabels = range(numSides)
		for i, label in enumerate(labelList):
			idx = (const + i) % numSides
			newLabels[idx] = label
		self.labelSides(newLabels)

	def labelSides(self, labelList):

		self.sideLabels = labelList
		vertices_pairs = sorted(self.vertices.tolist(), key=lambda element: (element[0], element[1]))
		vertices_pairs=self.vertices.tolist() + [self.vertices.tolist()[0]]
		midpoint_vertices=[]
		for i, vertex in enumerate(vertices_pairs[:-1]):
			x = (vertex[0] + vertices_pairs[i+1][0])/2
			y = (vertex[1] + vertices_pairs[i+1][1])/2
			midpoint_vertices.append([x,y])
		midpoint_vertices = np.matrix(midpoint_vertices)

		centroid = np.mean(midpoint_vertices, axis=0)

		for i, label in enumerate(labelList):
			ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
			d = np.matrix([ac[0,1], -ac[0,0]])
			# TODO: We need to figure out a better amount of padding to use
			p = 0.1
			v = midpoint_vertices[i, :] + p*d

			dx, dy = d[0, 0], d[0, 1]
			vx, vy = v[0, 0], v[0, 1]

			txt = self.figure.ax.text(0, 0, '$'+label+'$', fontsize=.03*self.figure.width)
			txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))

			w, h = self.figure.measureText(txt, True)

			# Next we essentially adjust the text to be anchored on a point anchored along the direction line that divides the rectangle into two equal length areas
			# Center text on the direction line : this assumes that the text is usually anchored on the bottom left point
			if abs(dy) > abs(dx): # run greater than rise : intersects top and bottom lines of rectangle
				vx -= w / 2.0
				delx = ((dx / dy) * h) / 2.0
				if dy < 0:
					vx -= delx
					vy -= h
				else:
					vx += delx
			else:
				vy -= h / 2.0
				dely = ((dy / dx) * w) / 2.0
				if dx < 0:
					vy -= dely
					vx -= w
				else:
					vy += dely

			txt.set_position((vx, vy))

	def bisector(self, i):
		"""For a vertex, get the vector of the angle bisector (pointing inwards)"""
		ab = self.vertices[i-1, :] - self.vertices[i, :]
		ab = ab / np.linalg.norm(ab)
		ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
		ac = ac / np.linalg.norm(ac)
		bisec = (ab + ac) / 2.0 # This points inward
		bisec = bisec / np.linalg.norm(bisec)
		return bisec

	def labelVertices(self, labelList, inner=False):
		# Everything is the counter clockwise, and the first angle/vertex is the first lable, everything else is counter clockwise order
		# The side that's mentioned first is horizontal
		if inner:
			self.angleLabels = labelList
		else:
			self.verticesLabels = labelList

		for i, label in enumerate(labelList):
			a = (self.vertices[i-1, :] - self.vertices[i, :])
			b = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
			dotted = b.dot(a.transpose())[0,0]
			magnitude = np.hypot(a[0, 0], a[0, 1]) * np.hypot(b[0, 0], b[0, 1])
			angle = np.arccos(float(dotted)/magnitude)

			d = self.bisector(i)
			if not inner:
				d = -d

			txt = self.figure.ax.text(0, 0, '$'+label+'$', fontsize=.025*self.figure.width if not inner else .015*self.figure.width)
			txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))

			w, h = self.figure.measureText(txt, True)
			# TODO: We need to figure out a better amount of padding to use
			p = 0.6*2.65*h/np.sin(angle) if inner else 0.1
			# small triangles .25?
			v = self.vertices[i, :] + p*d

			dx, dy = d[0, 0], d[0, 1]
			vx, vy = v[0, 0], v[0, 1]

			# Next we essentially adjust the text to be anchored on a point anchored along the direction line that divides the rectangle into two equal length areas
			# Center text on the direction line : this assumes that the text is usually anchored on the bottom left point
			if abs(dy) > abs(dx): # run greater than rise : intersects top and bottom lines of rectangle
				vx -= w / 2.0
				delx = ((dx / dy) * h) / 2.0
				if dy < 0:
					vx -= delx
					vy -= h
				else:
					vx += delx
			else:
				vy -= h / 2.0
				dely = ((dy / dx) * w) / 2.0
				if dx < 0:
					vy -= dely
					vx -= w
				else:
					vy += dely

			txt.set_position((vx, vy))

	def labelAngles(self, labelList):
		self.labelVertices(labelList, True)

	def __draw__(self, zorder=1):
		p = self.figure.ax.add_patch(self.matplotlib_obj)
		p.set(zorder=zorder)
