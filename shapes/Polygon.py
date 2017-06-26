import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import itertools

from matplotlib.patches import Arc


class Polygon:
	matplotlib_obj = None
	def __init__(self, vertices, props={}, figure=None):
		self.vertices = np.matrix(vertices)
		self.linewidth = 2
		self.props = props

		# Define the polygon
		self.matplotlib_obj = plt.Polygon(vertices, fill=False, linewidth=self.linewidth, **self.props)
		self.figure = figure


	def labelOppositeSides(self, labelList, **kwargs):
		# Number of sides - 1/2  + current index mod number of sides = new index
		numSides = len(self.vertices.tolist())
		const = (numSides-1)/2
		newLabels = range(numSides)
		for i, label in enumerate(labelList):
			idx = (const + i) % numSides
			newLabels[idx] = label
		self.labelSides(newLabels, **kwargs)

	def labelSides(self, labelList, fontsize=15, padding=1):
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

			# Get d as the perpendicular vector at the midpoint
			ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
			d = np.matrix([ac[0,1], -ac[0,0]])

			# Padding is "amount to clear line width" + "a constant # of points"
			p = (self.linewidth*self.figure.UNITS_PER_PT_x / 2) + (padding*2*self.figure.UNITS_PER_PT_x)
			v = midpoint_vertices[i, :] + p*d


			txt = self.figure.ax.text(0, 0, '$'+label+'$', fontsize=fontsize)
			txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))

			v, w, h, wp, hp = self.alignTextAlongVector(txt, v, d, i, debug=False)

			txt.set_position((v[0,0], v[0,1]))

	def bisector(self, i):
		"""For a vertex, get the vector of the angle bisector (pointing inwards)"""
		ab = self.vertices[i-1, :] - self.vertices[i, :]
		ab = ab / np.linalg.norm(ab)
		ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
		ac = ac / np.linalg.norm(ac)
		bisec = (ab + ac) / 2.0 # This points inward
		bisec = bisec / np.linalg.norm(bisec)
		return bisec

	def labelVertices(self, labelList, inner=False, fontsize=15, factorPadding=1, arcs=None):
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

			txt = self.figure.ax.text(0, 0, '$'+label+'$', fontsize=fontsize)
			txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))

			v = np.copy(self.vertices[i, :])

			v, w, h, wp, hp = self.alignTextAlongVector(txt, v, d, i, debug=False)

			# compute necessary padding to clear the polygon
			if inner:
				line_units = self.linewidth * self.figure.UNITS_PER_PT_x
				# Based on the right triangle formed by the angle bisector and a perpendicular line dropped to one side of the polygon
				# The length of that perpendicular line must be long enough to fix half of the text
				p = (hp + (line_units / 2)) / np.tan(angle / 2.0)
			else:
				p = 3 * self.figure.UNITS_PER_PT_x


			# Adding arcs for angle labels
			if inner and arcs is not None:
				if isinstance(arcs[i], int):
					for k in range(arcs[i]):
						r_x = self.figure.UNITS_PER_PT_x * 8
						r_y = self.figure.UNITS_PER_PT_y * 8

						# these are just the vectors along the adjacent sides
						ab = self.vertices[i-1, :] - self.vertices[i, :]
						ab = ab / np.linalg.norm(ab)
						ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
						ac = ac / np.linalg.norm(ac)


						theta1 = np.arctan2(ac[0,1], ac[0, 0]) * 180.0 / np.pi
						theta2 = np.arctan2(ab[0,1], ab[0, 0]) * 180.0 / np.pi

						r_x = (2*r_x + k*10*self.figure.UNITS_PER_PIXEL_x)/2
						r_y = (2*r_y + k*10*self.figure.UNITS_PER_PIXEL_y)/2

						#self.figure.ax.add_patch(Arc((self.vertices[i,0] + k*5*self.figure.UNITS_PER_PIXEL_x, self.vertices[i,1] + k*5*self.figure.UNITS_PER_PIXEL_y), 2*r, 2*r, theta1=theta1, theta2=theta2, edgecolor='k', linewidth=1))
						self.figure.ax.add_patch(Arc((self.vertices[i,0], self.vertices[i,1]), 2*r_x, 2*r_y, theta1=theta1, theta2=theta2, edgecolor='k', linewidth=1))

						pmin = r_x + 4*self.figure.UNITS_PER_PT_x
						if p < pmin:
							p = pmin
				elif arcs[i].upper() == 'SQUARE' or isinstance(arcs[i], str) or arcs[i] < 0:
					# these are just the vectors along the adjacent sides
					"""ab = self.vertices[i-1, :] - self.vertices[i, :]
					ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]"""
					ab = self.vertices[i-1, :] - self.vertices[i, :]
					ab = (ab / np.linalg.norm(ab))*(6*self.figure.UNITS_PER_PT_x)
					ac = self.vertices[(i+1) % self.vertices.shape[0], :] - self.vertices[i, :]
					ac = (ac / np.linalg.norm(ac))*(6*self.figure.UNITS_PER_PT_x)
					aa = [2*np.mean([ac, ab], axis=0)[0].tolist()[0], 2*np.mean([ac, ab], axis=0)[0].tolist()[0]]

					verts = [self.vertices[i, :].tolist()[0], ab.tolist()[0], aa, ac.tolist()[0]]
					cent = np.mean(verts, axis=0)
					verts.sort(key=lambda p: np.arctan2(p[1]-cent[1],p[0]-cent[0]))
					self.figure.addPolygon(verts, props={'lw':1})

			if inner:
				v = v + p*d*factorPadding
			else:
				v = v + p*d# apply the padding
			txt.set_position((v[0,0], v[0,1]))

	def alignTextAlongVector(self, txt, v, d, i, debug=False):
		"""
			Returns:
				(new v position, cartesian width, cartesian height, vector aligned width, vector aligned height)
		"""
		# Measure the size of the text box. We correct for the descent such that the anchor point of the text is at the very bottom left corner of the text rather than at the left baseline
		w, h, descent = self.figure.measureText(txt, True)
		v[0, 1] += descent
		h += descent

		# Compute span perpendicular to direction
		dp = np.matrix([[ d[0, 1], -d[0, 0] ]])
		c = np.matrix([[ w / 2.0, h / 2.0 ]])
		hp = 0 # This is the height of the text perpendicular to the direction vector
		for ii, jj in itertools.product([0,1], [0,1]):
			hij = abs(np.inner(np.matrix([[ ii*w, jj*h ]]) - c, dp))
			hp = max(hij, hp)


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

		# Debug information
		if debug:
			ov = self.vertices[i,:]
			dv = d*10.0
			self.figure.addArrow([ ov[0,0], ov[0,1] ], [ dv[0,0], dv[0,1] ], width=0.002, color='grey')
			self.figure.addPoint([vx, vy - descent], r'\;', color='blue', pointsize=2)
			self.figure.addPoint([vx + w, vy - descent + h], r'\;', color='blue', pointsize=2)
			self.figure.addPoint([vx + (w / 2.0), vy - descent + (h / 2.0)], r'\;', color='red', pointsize=2)

		return np.matrix([[vx, vy]]), w, h, 0, hp




	def labelAngles(self, labelList, **kwargs):
		self.labelVertices(labelList, True, **kwargs)

	def __draw__(self, zorder=1):
		p = self.figure.ax.add_patch(self.matplotlib_obj)
		p.set(zorder=zorder)
