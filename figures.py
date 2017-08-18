import matplotlib
 # Change font to Computer Modern (LaTeX font)
matplotlib.rcParams['font.family'] = 'cmr10'; matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['axes.unicode_minus'] = False
 # Change renderer so it doesn't use the GUI
matplotlib.use('Svg')

import matplotlib.pyplot as plt
from shapes import Polygon, Arc, Wedge, FancyArrowPatch, RegularPolygon, Circle, Ellipse, Arrow, Axis, Point, Text, Function, Line, Box, FancyBox
import numpy as np
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO
import math
import re
from sympy.utilities.lambdify import lambdify
from matplotlib.backends.backend_svg import FigureCanvas, RendererSVG
from fractions import Fraction

class Figures:
	"""
		Object to hold multiple shapes and objects.
	"""

	head_len = 14.0
	head_width = 5.0
	def __init__(self, xyrange=[[-10,10],[-10,10]], aspectRatio=1, width=300, height=300, bgcolor='#f0feffff', padding=50):
		"""
			__init__ function for Figures class.
			Args:
				xyrange (Optional[List[List(float), List(float)]]): The x and y minimum and maximum represnted by
					[[xmin, xmax], [ymin, ymax]]. Default is None
				width (Optional[int]): The width of the image in pixels. Default is 200 px.
				height (Optional[int]): The heigt of the image in pixels. Default is 200 px.
				bgcolor (Optional[str]): The color of the background (matplotlib string, or hex). Default is '#f0feffff'
				padding (Optional[int]): Padding in pixels around the image. Default is 50 px
		"""
		self.fig, self.ax = plt.subplots()
		self.fig.set_dpi(72)
		self.tickLabelInterval = 1
		self.tight_fit = True
		self.padding = padding
		self.xyrange = xyrange
		self.aspectRatio = aspectRatio
		self.drawOrder = []
		self.width = width
		self.height = height
		self.bgcolor = bgcolor
		self.ax.set_facecolor(bgcolor)
		self.fig.patch.set_facecolor(bgcolor)




		"""
		aspect ratio is length of y unit by x unit in pixels
		aspect ratio is one by default, if 'auto' then do what you were doing where image fills box. If it's one and the width/height != 1 then the x or y needs to be shorter than the actual image
		"""

		# TODO: Move to __export__
		num, den = Fraction(aspectRatio).numerator, Fraction(aspectRatio).denominator
		self.UNITS_PER_PIXEL_x = num * ((0.0-self.xyrange[0][0]) + self.xyrange[0][1]) / (self.width-20.0)
		self.UNITS_PER_PIXEL_y = den * ((0.0-self.xyrange[1][0]) + self.xyrange[1][1]) / (self.width-20.0)
		self.UNITS_PER_PT_x = self.UNITS_PER_PIXEL_x / 0.75
		self.UNITS_PER_PT_y = self.UNITS_PER_PIXEL_y / 0.75

		self.setPixelSize(width, height)

		self.__init_canvas__()

	def __init_canvas__(self):
		# Adapted from https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/backend_svg.py : print_svg
		self.canvas = FigureCanvas(self.fig)
		self.export_str = StringIO()

		self.fig.set_dpi(72.0)
		width, height = self.fig.get_size_inches()
		w, h = width*72, height*72

		self.renderer = RendererSVG(w, h, self.export_str, None, 72)

	def __export__(self):

		self.fig._cachedRenderer = self.renderer

		# draw
		self.__draw_shapes__()

		# We will perform the tight layout ourselves
		self.fig.set_tight_layout(False)
		self.fig.tight_layout(pad=self.padding) # TODO: Give the author control other padding on all sides

		# compute pixel/pt/unit conversations based on axis limits and known padding
		# TODO

		# post draw
		# do all drawing that depends on unit metrics
		# TODO

		# Do the actual drawing onto the svg
		# Adapted from https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/backend_svg.py : print_svg
		self.fig.draw(self.renderer)
		self.renderer.finalize()

		#self.__writeFile__(self.export_str, format='svg')
		self.export_str.seek(0)  # rewind the data
		s = self.export_str.buf  # this is svg data

		# Clipping height to the used area after rendering
		# https://stackoverflow.com/questions/22667224/matplotlib-get-text-bounding-box-independent-of-backend/22689498
		# https://stackoverflow.com/questions/28692981/matplotlib-get-resulting-bounding-box-of-bbox-inches-tight
		#print(self.ax.get_position().bounds) # This gives you percentage wise the xmin, ymin, width, height up to the very edge of the grid lines
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
		s = self.__export__()
		f = open(fileLocation, "w+")
		f.write(s)
		f.flush()
		f.close()

	def __display__(self):
		plt.show()

	def measureText(self, text, units=False):
		"""Given a matplotlib Text object, returns a tuple of its width and height (in pts)"""

		prop = text._fontproperties
		width, height, descent, svg_elements, used_chars = self.renderer.mathtext_parser.parse(text.get_text(), 72, prop)

		if units:
			width *= self.UNITS_PER_PT_x
			height *= self.UNITS_PER_PT_y
			descent *= self.UNITS_PER_PT_y

		return (width, height, descent)

	def __draw_shapes__(self, order=None):
		if not any([isinstance(obj, Axis.Axis) for obj in self.drawOrder]) and not any([isinstance(obj, Box.Box) for obj in self.drawOrder]):
			self.addAxis(hideAxis=True)

		for i, shape in enumerate(self.drawOrder if order is None else order):
			shape.__draw__(zorder=i)

	def setPixelSize(self, height, width):
		"""Sets the pixel size of the figure.

			Warning: Do NOT call this outside of the constructor

			If only width is provided, then the figure will try to tight fit to that width
			If height is also specified, then the size is completely fixed to that size
		"""

		self.width = width

		# a point is 1/72in;  12pt = 16px
		px2in = lambda p: (p * 0.75 / 72.0)

		self.padding = px2in(self.padding)

		if isinstance(width, str):
			height_in = px2in(height)
			width_in = height_in
		else:
			width_in = px2in(width)
			height_in = width_in

		if height == 'auto':
			self.height = height
			self.tight_fit = False
			#self.fig.set_tight_layout({ "pad": 1.08 })
			height_in = 2*width_in
		elif width == 'auto':
			self.width = height
			self.tight_fit = False
			#self.fig.set_tight_layout({ "pad": 1.08 })
			height_in = 2*height_in
		elif height != None:
			self.tight_fit = False
			#self.fig.set_tight_layout({ "pad": self.padding })
			height_in = px2in(height)

		self.fig.set_size_inches((width_in, height_in))


	############################################################################
	#							SHAPE DEFINITIONS
	############################################################################


	def addAxis(self, hideAxis=False, grid=True, arrows=True, color='black', lw=1.5, minorGrid=True, label=True, xlabel='x', ylabel='y', mplprops={}):
		"""
			addAxis - Adds the axis 'shape' to the Figures.
			Args:
				hideAxis (Optional[bool]): Whether or not to hide the axis; takes either True which sets it to the color of the axis, or a color which defines it as its own color. Default is False.
				grid (Optional[bool]): Whether or not to display grids on major ticks. Default is False.
				arrows (Optional[bool]): Whether or not to display dimension arrows. Default is True.
				color (Optional[str]): Color of the axis. Default is 'black'.
				lw (Optional[float]): Lineweight of the axis. Default is 1.5.
				minorGrid (Optional[bool]): Whether or not to display axis on minor ticks; takes either True which sets it to the color of the axis, or a color which defines it as its own color. Default is False.
				label (Optional[bool]): Whether or not to label the dimensions. Default is True.
				xlabel (Optional[str]): Label for the x-dimension. Default is 'x'.
				ylabel (Optional[str]): Label for the y-dimension. Default is 'y'.
				mplprops (Optional[dict]): Dictionary to pass directly to the matplotlib object. Default is {}.
			Returns:
				Axis.Axis object
		"""
		pixelSize = self.width
		axis = Axis.Axis(hideAxis, grid, arrows, color, lw, minorGrid, label, xlabel, ylabel, mplprops, self)
		self.drawOrder.append(axis)
		return axis

	def addPoint(self, xys, texts='\ ', pointsize=6, fontsize=12, color='black', latex=True, mplprops={}):
		"""
			addPoint - Adds a point 'shape' to the Figures.
			Args:
				xys (List[float]): Whether or not to hide the axis; takes either True which sets it to the color of the axis, or a color which defines it as its own color. Default is False.
				texts (Optional[str]): Text to display at point. Default is '\ '
				pointsize (Optional[float]): Size of the point. Default is 6
				fontsize (Optional[float]): Fontsize. Default is 12.
				color (Optional[str]):  Color of the axis. Default is 'black'.
				latex (Optional[bool]): Whether or not to use LaTeX to render text. Default is True.
				mplprops (Optional[dict]): Dictionary to pass directly to the matplotlib object. Default is {}.
			Returns:
				Point.Point object
		"""
		p = Point.Point(xys, texts, pointsize, fontsize, color, latex, mplprops, self)
		self.drawOrder.append(p)
		return p

	def addLine(self, pointA, pointB, lw=2, color='k', mplprops={}):
		"""
			addLine - Adds a line 'shape' to the Figures.
			Args:
				pointA (List[float]): List or tuple, in x,y, of the first point.
				pointB (List[float]): List or tuple, in x,y, of the second point.
				lw (Optional[float]): Line width of the line. Default is 2.
				color (Optional[str]): Color of the line. Default is 'k'
				mplprops (Optional[dict]): Dictionary to pass directly to the matplotlib object. Default is {}.
			Returns:
				Line.Line object
		"""
		l = Line.Line(pointA, pointB, lw, color, mplprops, self)
		self.drawOrder.append(l)
		return l

	def addText(self, xy, text, color="black", fontsize=12, halignment='center', valignment='center', bbox={}, mplprops={}, latex=True, pixel=False):
		t = Text.Text(xy, text, color, fontsize, halignment, valignment, bbox, latex, pixel, mplprops, self)
		self.drawOrder.append(t)
		return t

	def addFunction(self, functions, xyranges=None, color='black', lw=2, variable=None, mplprops={}):
		xyranges= self.xyrange if xyranges == None else xyranges
		f = Function.Function(functions, xyranges, color, lw, variable, mplprops, self)
		self.drawOrder.append(f)
		return f

	def addBox(self, x, y, xlabel='  ', ylabel='  ', title="  ", lw=2, mplprops={}):
		pixelSize=self.width
		b = Box.Box(x, y, xlabel, ylabel, title, lw, mplprops, self)
		self.drawOrder.append(b)
		return b

	def addPolygon(self, vertices, lw=2, mplprops={}):
		pixelSize=self.width
		polygon = Polygon.Polygon(vertices, lw, True if 'color' in mplprops else False, mplprops, self)
		self.drawOrder.append(polygon)
		return polygon

	def addRegularPolygon(self, xy=(0,0), numVertices=0, radius=None, fill=False, lw=2, orientation=0.0, mplprops={}):
		pixelSize=self.width
		regpolygon = RegularPolygon.RegularPolygon(xy, numVertices, radius, fill, lw, orientation, mplprops, self)
		self.drawOrder.append(regpolygon)
		return regpolygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label="", fc='none', ec='k', lw=2, mplprops={}):
		pixelSize=self.width
		circle = Circle.Circle(xy, diameter, radius, label, fc, ec, lw, mplprops, self)
		self.drawOrder.append(circle)
		return circle

	def addEllipse(self, xy=[0,0], r=(1,1), fc='none', ec='k', angle=0.0, lw=2, mplprops={}):
		if isinstance(r, int):
			self.addCircle(xy=xy, radius=r, fc=fc, ec=ec, lw=lw, mplprops=mplprops)
		else:
			pixelSize=self.width
			ellipse = Ellipse.Ellipse(xy, r, fc, ec, angle, lw, mplprops, self)
			self.drawOrder.append(ellipse)
			return ellipse

	def addArc(self, xy=(0,0), width=0, height=0, lw=2, angle=0.0, theta1=0.0, theta2=360.0, mplprops={}):
		pixelSize=self.width
		arc = Arc.Arc(xy, width, height, lw, angle, theta1, theta2, mplprops, self)
		self.drawOrder.append(arc)
		return arc

	def addWedge(self, xy=(0,0), r=0, theta1=0, theta2=0, width=None, mplprops={}):
		pixelSize=self.width
		wedge = Wedge.Wedge(xy, r, theta1, theta2, width, mplprops, self)
		self.drawOrder.append(wedge)
		return wedge

	def addArrow(self, start, end, lw=25, color='k', headWidth=30, headLength=70, mplprops={}, **kwargs):
		if 'arrowstyle' in kwargs:
			self.addFancyArrow(
				posA=start, posB=end, color=color, lw=lw, path=None, arrowstyle=kwargs['arrowstyle'],
				connectionstyle=kwargs['connectionstyle'],mutation_scale=lw*5,mplprops=mplprops
			)

		else:
			return Arrow.Arrow(start, end, color, headWidth, headLength, lw, mplprops, self)

	def addFancyArrow(self, posA, posB, path=None, color='k', lw=2, arrowstyle=None, connectionstyle='bar', mutation_scale=3, mplprops={}):
		fancyArrow = FancyArrowPatch.FancyArrowPatch(posA, posB, path, color, lw, arrowstyle, connectionstyle, mutation_scale, mplprops, self)
		self.drawOrder.append(fancyArrow)
		return fancyArrow
	def addFancyBox(self, ll_point, ur_point, boxstyle="square,pad=0.", mplprops={}):
		FancyBBox = FancyBox.FancyBox(ll_point, ur_point, boxstyle, mplprops, self)
		self.drawOrder.append(FancyBBox)
		return FancyBBox

	############################################################################
	#							HELPER DEFINITIONS
	############################################################################

	def unit2px(self, i, dim):
		"""
			Converts units to pixel
			Args:
				i (int): Number of pixels
				dim (str): dimension
			Returns:
				(float) number of units

		"""
		return (1.0/self.UNITS_PER_PIXEL_x)*i if dim=='x' else (1.0/self.UNITS_PER_PIXEL_y)*i

	def px2unit(self, i, dim):
		"""
			Converts units to pixel
			Args:
				i (int): Number of pixels
				dim (str): dimension
			Returns:
				(float) number of units

		"""
		return self.UNITS_PER_PIXEL_x*i if dim=='x' else self.UNITS_PER_PIXEL_y*i

	def px2unit_c(self, p):
		"""
			Converts units to pixel
			Args:
				p (Tuple[float]): x and y coord in units
			Returns:
				(Tuple[float]) x and y coorfd in pixels

		"""
		return np.matrix([p[0,0]*self.UNITS_PER_PIXEL_x, p[0,1]*self.UNITS_PER_PIXEL_y])

	def unit2px_c(self, p):
		"""
			Converts pixels to units
			Args:
				p (Tuple[float]): x and y coord in pixel
			Returns:
				(Tuple[float]) x and y coorfd in units

		"""
		return np.matrix([p[0,0]*(1.0/self.UNITS_PER_PIXEL_x), p[0,1]*(1.0/self.UNITS_PER_PIXEL_y)])


	def addTriangle(self, xy=(0,0), a=0, b=0, c=0, isSide=True, angle=0.0, rotation=0.0, length=1, lw=2, mplprops={}):
		if isSide:
			alpha = np.arccos((b**2+c**2-a**2) /(2.0*b*c))
			beta = np.arccos((-b**2+c**2+a**2) /(2.0*a*c))
			gamma = (np.pi)-alpha-beta

			# Points
			x = (c*np.tan(beta))/(np.tan(alpha)+np.tan(beta))
			y = x * np.tan(alpha)
			z = np.array([a,b,c])

			vertexA = [0+xy[0],0,1]
			vertexB = [z[-1],0+xy[0],1]
			vertexC = [x,y,1]

			transformation = matplotlib.transforms.Affine2D().rotate_around(xy[0], xy[1], rotation)
			triangle = Polygon.Polygon(np.delete((transformation * np.matrix([vertexA, vertexB, vertexC]).transpose()).transpose(), 2, axis=1), lw, None, mplprops, figure=self)
			self.drawOrder.append(triangle)
			return triangle

		else:
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
			triangle = Polygon.Polygon(np.delete((transformation * np.matrix([vertexA, vertexB, vertexC]).transpose()).transpose(), 2, axis=1), lw, None, mplprops, figure=self)
			self.drawOrder.append(triangle)
			return triangle
