import matplotlib
matplotlib.use('Svg') # Change renderer so it doesn't use the GUI
matplotlib.rcParams['font.family'] = 'cmr10' # Change font to Computer Modern (LaTeX font)
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [10,10]
from shapes import Polygon, Circle, Ellipse, Arrow, Axis, Point, Text, Function

import numpy as np
import StringIO
import math
import re
from sympy.utilities.lambdify import lambdify


class Figures:
	def __init__(self, xyrange=None, ratio=[10,10], width=400):
		self.fig, self.ax = plt.subplots()
		self.fig.set_dpi(72)
		self.tickInterval = 0
		self.tickLabelInterval = 1
		self.tight_fit = True
		self.padding = 0
		self.height = None
		self.xyrange = xyrange
		self.drawOrder = []
		self.width = 400

		self.setPixelSize(400, height='auto')
		#plt.figure(figsize=ratio)


	def __export__(self):
		export_str = StringIO.StringIO()
		self.__writeFile__(export_str, format='svg')
		export_str.seek(0)  # rewind the data
		s = export_str.buf  # this is svg data

		# Clipping height to the used area after rendering
		# https://stackoverflow.com/questions/22667224/matplotlib-get-text-bounding-box-independent-of-backend/22689498
		# https://stackoverflow.com/questions/28692981/matplotlib-get-resulting-bounding-box-of-bbox-inches-tight
		#print(self.ax.get_position().bounds) # This gives you percentage wise the xmin, ymin, width, height up to the very edge of the grid lines
		#print(self.fig.bbox)
		if self.height == 'auto':
		 	bb = self.ax.get_tightbbox(self.fig._cachedRenderer) #get_renderer()))

			minY = math.floor(bb.y0)
			maxY = math.ceil(bb.y1)

			s = re.sub(r'height="[0-9]+pt"', 'height="%dpt"' % (maxY - minY), s)

			viewBoxReg = r'viewBox="([0-9]+ [0-9]+ [0-9]+ [0-9]+)"';
			viewBox = [int(x) for x in re.search(viewBoxReg, s).group(1).split(' ')]
			viewBox[1] = viewBox[3] - maxY
			viewBox[3] = (maxY - minY)
			s = re.sub(viewBoxReg, 'viewBox="' + ' '.join([str(x) for x in viewBox]) + '"', s)

		return s

	def __writeFile__(self, fileLocation, **kwargs):
		self.fig.savefig(fileLocation, bbox_inches=('tight' if self.tight_fit else None), pad_inches=self.padding, **kwargs)

	def __display__(self):
		plt.show()

	def __draw_shapes__(self, order=None):
		for i, shape in enumerate(self.drawOrder if order is None else order):
			shape.__draw__(zorder=i)

	def addAxis(self, hideAxis=False, xyrange=None, grid=False, arrows=True, color='black', minorGrid=False):
		xyrange=self.xyrange if xyrange is None else xyrange
		axis = Axis.Axis(self.fig, self.ax, hideAxis, xyrange, grid, arrows, color, minorGrid)
		self.drawOrder.append(axis)
		return axis



	def setPixelSize(self, width=400, height=None, padding=0):
		"""Sets the pixel size of the figure.

			If only width is provided, then the figure will try to tight fit to that width
			If height is also specified, then the size is completely fixed to that size
		"""

		self.width = width

		# a point is 1/72in;  12pt = 16px
		px2in = lambda p: (p * 0.75 / 72.0)

		self.padding = px2in(padding)

		width_in = px2in(width)
		height_in = width_in

		if height == 'auto':
			self.height = height
			self.tight_fit = False
			self.fig.set_tight_layout({ "pad": self.padding })
			height_in = 2*width_in
		elif height != None:
			self.tight_fit = False
			self.fig.set_tight_layout({ "pad": self.padding })
			height_in = px2in(height)

		self.fig.set_size_inches((width_in, height_in))


	def addPoint(self, xys, texts, pointsize=6, fontsize=12, colors='black', latex=True):
		p = Point.Point(self.fig, self.ax, xys, texts, pointsize, fontsize, colors, latex)
		self.drawOrder.append(p)
		return p

	def addText(self, xy, text, color="black", fontsize=12, halignment='center', valignment='top', bbox={}, latex=True):
		t = Text.Text(self.fig, self.ax,xy, text, color="black", fontsize=12, halignment='center', valignment='top', bbox={}, latex=True)
		self.drawOrder.append(t)
		return t

	def addFunction(self, functions, xyranges=None, colors='black', linewidth=2, variable=None):
		xyranges= self.xyrange if xyranges == None else xyranges
		f = Function.Function(self.fig, self.ax, functions, xyranges, colors, linewidth, variable)
		self.drawOrder.append(f)
		return f


	def axisFormatTicks(self, tickLabelInterval=1, tickInterval=1, fontsize=12, origin=False, top=True):
		self.tickInterval = tickInterval
		self.tickLabelInterval = tickLabelInterval
		# Control ticks
		self.ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(tickLabelInterval))
		self.ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(tickLabelInterval))
		self.ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(tickInterval))
		self.ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(tickInterval))
		self.ax.tick_params(axis='both', which='major', labelsize=fontsize)


		if top:
			self.ax.xaxis.set_label_position('top')


		if origin:
			ylabels = [int(item) if int(item) is not 0 else "" for item in self.ax.get_yticks().tolist()]
			xlabels = [int(item) if int(item) is not 0 else "        (0,0)" for item in self.ax.get_xticks().tolist()]
			self.ax.set_yticklabels(ylabels)
			self.ax.set_xticklabels(xlabels)
		else:
			xlabels = [int(item) if int(item) is not 0 else "" for item in self.ax.get_xticks().tolist()]
			self.ax.set_xticklabels(xlabels)
			ylabels = [int(item) if int(item) is not 0 else "" for item in self.ax.get_yticks().tolist()]
			self.ax.set_yticklabels(ylabels)

			for label in self.ax.xaxis.get_ticklabels():
				label.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))
			for label in self.ax.yaxis.get_ticklabels():
				label.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.1))

	def addPolygon(self, vertices):
		polygon = Polygon.Polygon(vertices, self.fig, self.ax)
		self.drawOrder.append(polygon)
		return polygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label="", fc='none', ec='k'):
		circle = Circle.Circle(self.fig, self.ax, xy, diameter, radius, label, fc, ec)
		self.drawOrder.append(circle)
		return circle

	def addEllipse(self, xy=[0,0], r=(1,1), fc='none', ec='k', angle=0.0, lw=2):
		if isinstance(r, int):
			self.addCircle(xy=xy, radius=r, fc=fc, ec=ec)
		else:
			ellipse = Ellipse.Ellipse(self.fig, self.ax, xy, r, fc, ec, angle, lw)
			self.drawOrder.append(ellipse)
			return ellipse

	def addTriangle_angle(self, xy=(0,0), angle=(45*np.pi)/180, rotation=0, length=1):
		# Define the angles and sides
		alpha = angle
		beta = np.pi/2
		gamma = np.pi-beta-alpha

		A = length
		B = np.sin(beta)*length/np.sin(alpha)
		C = np.sin(gamma)*length/np.sin(alpha)

		# Define the vertices
		vertexA = [0+xy[0], A+xy[1], 1]
		vertexB = [xy[0], xy[1], 1]
		vertexC = [C+xy[0], 0+xy[1], 1]

		transformation = matplotlib.transforms.Affine2D().rotate_around(xy[0], xy[1], rotation) # + self.ax.transData
		polygon = Polygon.Polygon(np.delete((transformation * np.matrix([vertexA, vertexB, vertexC]).transpose()).transpose(), 2, axis=1), self.fig, self.ax)
		self.drawOrder.append(polygon)
		return polygon

	def addTriangle_side(self, xy=(0,0), a=0, b=0, c=0, rotation=0, length=1):
		# Angles
		return
		alpha = np.arccos((b**2+c**2-a**2) /(2.0*b*c))
		beta = np.arccos((-b**2+c**2+a**2) /(2.0*a*c))
		gamma = (np.pi)-alpha-beta

		# Points
		x = (c*np.tan(beta))/(np.tan(alpha)+np.tan(beta))
		y = x * np.tan(alpha)
		z = np.array([a,b,c])

		vertexA = [0,0]
		vertexB = [z[-1],0]
		vertexC = [x,y]

		triangle = Polygon.Polygon(np.delete((transformation * np.matrix([[0,0], [z[-1],0], [x,y]]).transpose()).transpose(), 2, axis=1), self.fig, self.ax)

		return triangle

	def addArrow(self, xy, dxdy, color='black', headWidth=0.1, width=0.35):
		arrow = Arrow.Arrow(self.ax, self.fig, xy, dxdy, color=color, headWidth=headWidth, width=width)
		self.drawOrder.append(arrow)
		return arrow
