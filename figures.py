import matplotlib
 # Change font to Computer Modern (LaTeX font)
matplotlib.rcParams['font.family'] = 'cmr10'; matplotlib.rcParams['mathtext.fontset'] = 'cm'
#matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams["font.size"] = 72
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
from six import string_types

px2in = lambda p: (p * 0.75 / 72.0)

class Figures:
	"""
		Object to hold multiple shapes and objects.
	"""

	head_len = 14.0
	head_width = 5.0
	def _BG_COLOR():
		return "#f0feffff"
	_BG = _BG_COLOR()
	BG = _BG_COLOR()

	def __init__(self, xyrange=None, aspectRatio=None, width=300, height=300, bgcolor='#f0feffff', padding=20, xPad=None, yPad=None):
		"""
			__init__ function for Figures class.
			Args:
				xyrange (Optional[List[List(float), List(float)]]): The x and y minimum and maximum represnted by
					[[xmin, xmax], [ymin, ymax]]. Default is None
				width (Optional[int]): The width of the image in pixels. Default is 200 px.
				height (Optional[int]): The height of the image in pixels. Default is 200 px.
				bgcolor (Optional[str]): The color of the background (matplotlib string, or hex). Default is '#f0feffff'
				padding (Optional[int]): Padding in pixels around the image. Default is 50 px
		"""

		if xyrange == None:
			raise ValueError('xyrange must be specified explictly for figures')

		unconstrained = 0
		if isinstance(height, string_types):
			height = height.lower()
			if height == 'auto':
				unconstrained += 1
			else:
				raise ValueError('Unknown value for height: ' + height)
		if isinstance(width, string_types):
			width = width.lower()
			if width == 'auto':
				unconstrained += 1
			else:
				raise ValueError('Unknown value for width: ' + width)

		if unconstrained > 1:
			raise ValueError('Underconstrained dimensions of figure')

		if width == 'auto':
			aspectRatio_temp = 1 if not aspectRatio else aspectRatio
			width_temp = height * 1.0/float(aspectRatio_temp)
		else:
			width_temp = width
		if height == 'auto':
			aspectRatio_temp = 1 if not aspectRatio else aspectRatio
			height_temp = width * float(aspectRatio_temp)
		else:
			height_temp = height

		self.xPad = xPad if xPad != None else padding
		self.yPad = yPad if yPad != None else padding
		self.abs_range_x = xyrange[0][1]- xyrange[0][0]
		self.abs_range_y = xyrange[1][1]- xyrange[1][0]
		self.fig, self.ax = plt.subplots()
		self.fig.set_dpi(72)
		self.tickLabelInterval = 1
		self.padding = padding
		self.true_pad = (0.75 * self.padding)/10.0
		self.tight_fit = True
		if width!='auto' and height!='auto':
			self.aspectRatio=(float(height_temp-2*self.true_pad)/(width_temp-2*self.true_pad)) / (float(self.abs_range_y)/self.abs_range_x) if not aspectRatio else aspectRatio
		elif width=='auto' or height=='auto':
			self.aspectRatio = 1 if not aspectRatio else (float(height_temp-2*self.true_pad)/(width_temp-2*self.true_pad)) / (float(self.abs_range_y)/self.abs_range_x)
		self.xyrange = xyrange
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
		num, den = Fraction(str(self.aspectRatio)).numerator, Fraction(str(self.aspectRatio)).denominator
		val = self.width
		if self.width == 'auto':
			val = self.height
			num, den = (den, num)

		# if aspect > 1, multiply width
		self.UNITS_PER_PIXEL_x = self.abs_range_x / float(width_temp-2*self.true_pad)
		self.UNITS_PER_PIXEL_y = self.abs_range_y / float(height_temp-2*self.true_pad)
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
		true_pad = (0.75 * self.padding)/12.0

		self.fig.tight_layout(pad=px2in(self.padding))

		# post draw
		# do all drawing that depends on unit metrics
		# TODO

		# Do the actual drawing onto the svg
		#1inch = 72 pts
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

		if self.width == 'auto':
			bb = self.ax.get_tightbbox(self.fig._cachedRenderer) #get_renderer()))

			minX = math.floor(bb.x0)
			maxX = math.ceil(bb.x1)

			s = re.sub(r'width="[0-9]+pt"', 'width="%dpt"' % (maxX - minX), s)

			viewBoxReg = r'viewBox="([0-9]+ [0-9]+ [0-9]+ [0-9]+)"';
			viewBox = [int(x) for x in re.search(viewBoxReg, s).group(1).split(' ')]
			viewBox[0] = viewBox[2] - maxX
			viewBox[2] = (maxX - minX)
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
		local_order = self.drawOrder if order is None else order
		if not any([isinstance(obj, Axis.Axis) for obj in local_order]) and not any([isinstance(obj, Box.Box) for obj in local_order]):
			axis = self.addAxis(hideAxis=True, label=False, arrows=False, grid=False, minorGrid=False, lw=0)

		for i, shape in enumerate(local_order):
			shape.__draw__(zorder=i*10+1)

	def setPixelSize(self, width, height):
		"""Sets the pixel size of the figure.

			Warning: Do NOT call this outside of the constructor

			If only width is provided, then the figure will try to tight fit to that width
			If height is also specified, then the size is completely fixed to that size
		"""

		self.width = width

		# a point is 1/72in;  12pt = 16px


		height_in = None
		width_in = None

		if not isinstance(width, string_types):
			width_in = px2in(width)
		if not isinstance(height, string_types):
			height_in = px2in(height)

		if height == 'auto':
			self.tight_fit = False
			#self.fig.set_tight_layout({ "pad": 1.08 })
			height_in = 2*width_in
		elif width == 'auto':
			self.tight_fit = False
			#self.fig.set_tight_layout({ "pad": 1.08 })
			width_in = 2*height_in
		elif height != None:
			self.tight_fit = False
			#self.fig.set_tight_layout({ "pad": self.padding })

		self.fig.set_size_inches((width_in, height_in))


	############################################################################
	#							SHAPE DEFINITIONS
	############################################################################


	def addAxis(self, hideAxis=False, grid=True, arrows=True, color='black', lw=1, minorGrid=False, label=True, xlabel='x', ylabel='y', mplprops={}):
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

	def addLine(self, pointA, pointB, lw=2, color='k', clip=True, add=True, mplprops={}):
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
		l = Line.Line(pointA, pointB, lw, color, clip, mplprops, self)
		if add: self.drawOrder.append(l)
		return l

	def addText(self, xy, text, color="black", fontsize=12, halignment='center', valignment='center', bbox={}, mplprops={}, latex=True, pixel=False, add=True):
		t = Text.Text(xy, text, color, fontsize, halignment, valignment, bbox, latex, pixel, mplprops, self)
		if add: self.drawOrder.append(t)
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

	def addPolygon(self, vertices, lw=2, fc='None', color='k', clip=True, add=True, mplprops={}):
		pixelSize=self.width
		polygon = Polygon.Polygon(vertices, lw, True if fc!='None' else False, fc, color, clip, mplprops, self)
		if add: self.drawOrder.append(polygon)
		return polygon

	def addRegularPolygon(self, xy=(0,0), numVertices=0, radius=None, fc='None', color='k', lw=2, orientation=0.0, mplprops={}):
		pixelSize=self.width
		regpolygon = RegularPolygon.RegularPolygon(xy, numVertices, radius, True if fc!='None' else False, fc, color, lw, orientation, mplprops, self)
		self.drawOrder.append(regpolygon)
		return regpolygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label="", fc='none', color='k', lw=2, mplprops={}):
		pixelSize=self.width
		circle = Circle.Circle(xy, diameter, radius, label, fc, color, lw, mplprops, self)
		self.drawOrder.append(circle)
		return circle

	def addEllipse(self, xy=[0,0], r=(1,1), fc='none', color='k', angle=0.0, lw=2, mplprops={}):
		if isinstance(r, int):
			self.addCircle(xy=xy, radius=r, fc=fc, ec=ec, lw=lw, mplprops=mplprops)
		else:
			pixelSize=self.width
			ellipse = Ellipse.Ellipse(xy, r, fc, color, angle, lw, mplprops, self)
			self.drawOrder.append(ellipse)
			return ellipse

	def addArc(self, xy=(0,0), width=0, height=0, fc='None', color='k', lw=2, angle=0.0, theta1=0.0, theta2=360.0, mplprops={}):
		theta1=math.radians(theta1)
		theta2=math.radians(theta2)
		pixelSize=self.width
		arc = Arc.Arc(xy, width, height, fc, color, lw, angle, theta1, theta2, mplprops, self)
		self.drawOrder.append(arc)
		return arc

	def addWedge(self, xy=(0,0), r=0, theta1=0, theta2=0, fc='None', color='k', width=None, mplprops={}):
		theta1=math.radians(theta1)
		theta2=math.radians(theta2)
		pixelSize=self.width
		wedge = Wedge.Wedge(xy, r, theta1, theta2, fc, color, width, mplprops, self)
		self.drawOrder.append(wedge)
		return wedge

	def addArrow(self, start, end, lw=25, color='k', headWidth=30, headLength=70, mplprops={}, clip=True, add=True, **kwargs):
		if 'arrowstyle' in kwargs:
			self.addFancyArrow(
				posA=start, posB=end, color=color, lw=lw, path=None, arrowstyle=kwargs['arrowstyle'],
				connectionstyle=kwargs['connectionstyle'],mutation_scale=lw*5,mplprops=mplprops
			)

		else:
			return Arrow.Arrow(start, end, color, headWidth, headLength, lw, mplprops, clip, add, self)

	def addFancyArrow(self, posA, posB, path=None, color='k', lw=2, arrowstyle=None, connectionstyle='bar', mutation_scale=3, mplprops={}):
		fancyArrow = FancyArrowPatch.FancyArrowPatch(posA, posB, path, color, lw, arrowstyle, connectionstyle, mutation_scale, mplprops, self)
		self.drawOrder.append(fancyArrow)
		return fancyArrow

	def addRectangle(self, ll_point, ur_point, r=0, fc='None', ec='black', mplprops={}):
		if r!=0:
			return self.addRectangle_rounded(ll_point, ur_point, r=r, fc=fc, ec=ec, mplprops=mplprops)
		FancyBBox = FancyBox.FancyBox(ll_point, ur_point, fc, ec, "square,pad=0", mplprops, self)
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

	def addZigzag(self, points, lw=2, color='k', mplprops={}):
		lines = []
		for i, point in enumerate(points):
			if i == len(points)-1:
				break

			lines.append(self.addLine(point, points[i+1], lw=lw, color=color, mplprops=mplprops))
		return lines

	def addRectangle_rounded(self, ll_point, ur_point, r=0, fc='None', ec='black', mplprops={}):

		self.addLine([ll_point[0]+r, ll_point[1]], [ur_point[0]-r, ll_point[1]], color=ec)
		self.addLine([ll_point[0], ll_point[1]+r], [ll_point[0], ur_point[1]-r], color=ec)
		self.addLine([ll_point[0]+r, ur_point[1]], [ur_point[0]-r, ur_point[1]], color=ec)
		self.addLine([ur_point[0], ll_point[1]+r], [ur_point[0], ur_point[1]-r], color=ec)

		if r != 0:
			self.addArc(xy=[ll_point[0]+r,ll_point[1]+r], width=2*r, height=2*r, theta1=180, theta2=270, mplprops={'color': ec})
			self.addArc(xy=[ur_point[0]-r, ll_point[1]+r], width=2*r, height=2*r, theta1=-90, theta2=0, mplprops={'color': ec})
			self.addArc(xy=[ur_point[0]-r, ur_point[1]-r], width=2*r, height=2*r, theta1=0, theta2=90, mplprops={'color': ec})
			self.addArc(xy=[ll_point[0]+r, ur_point[1]-r], width=2*r, height=2*r, theta1=90, theta2=180, mplprops={'color': ec})

		#Coloring:
		ul_point = [ll_point[0], ur_point[1]]
		lr_point = [ur_point[0], ll_point[1]]
		self.addCircle(xy=[ll_point[0]+r, ll_point[1]+r], fc=fc, radius=r, lw=0)
		self.addCircle(xy=[ur_point[0]-r, ll_point[1]+r], fc=fc, radius=r, lw=0)
		self.addCircle(xy=[ll_point[0]+r, ur_point[1]-r], fc=fc, radius=r, lw=0)
		self.addCircle(xy=[ur_point[0]-r, ur_point[1]-r], fc=fc, radius=r, lw=0)
		self.addRectangle([ll_point[0]+r, ll_point[1]], [ur_point[0]-r, ur_point[1]], fc=fc, ec='none')
		self.addRectangle([ll_point[0], ll_point[1]+r], [ur_point[0], ur_point[1]-r], fc=fc, ec='none')

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
