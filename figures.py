import matplotlib
matplotlib.rcParams['font.family'] = 'cmr10' # Change font to Computer Modern (LaTeX font)
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.use('Svg') # Change renderer so it doesn't use the GUI
import matplotlib.pyplot as plt
from shapes import Polygon, Arc, Wedge, FancyArrowPatch, RegularPolygon, Circle, Ellipse, Arrow, Axis, Point, Text, Function, Line

import numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import math
import re
from sympy.utilities.lambdify import lambdify

from matplotlib.backends.backend_svg import FigureCanvas, RendererSVG

class Figures:
	def __init__(self, xyrange=None, ratio=[10,10], width=200, height=200, bgcolor='#f0feffff'):
		self.fig, self.ax = plt.subplots()
		#self.fig, self.ax = plt.subplots(figsize=(20, 10))
		self.fig.set_dpi(72)
		self.tickInterval = 0
		self.tickLabelInterval = 1
		self.tight_fit = True
		self.padding = 0
		self.height = None
		self.xyrange = xyrange
		self.drawOrder = []
		self.width = width
		self.height = height
		self.bgcolor = bgcolor
		self.ax.set_facecolor(bgcolor)
		self.fig.patch.set_facecolor(bgcolor)

		# TODO: Move to __export__
		if xyrange is not None:
			self.UNITS_PER_PIXEL_x = float(((0-self.xyrange[0][0]) + (self.xyrange[0][1])))/(self.width if not isinstance(self.width, str) else self.height)
			self.UNITS_PER_PIXEL_y = float(((0-self.xyrange[1][0]) + (self.xyrange[1][1])))/(self.width if not isinstance(self.width, str) else self.height)
			self.UNITS_PER_PT_x = self.UNITS_PER_PIXEL_x / 0.75
			self.UNITS_PER_PT_y = self.UNITS_PER_PIXEL_y / 0.75

		self.setPixelSize(width, height=height)
		#plt.figure(figsize=ratio)

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
		# print(self.ax.get_xlim())
		# print(self.ax.get_ylim())
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
    		if not any([isinstance(obj, Axis.Axis) for obj in self.drawOrder]):
    			self.addAxis(hideAxis=True)

    		for i, shape in enumerate(self.drawOrder if order is None else order):
    			shape.__draw__(zorder=i)

    	def addAxis(self, hideAxis=False, grid=False, arrows=True, color='black', lw=2, minorGrid=False, label=True, xlabel='x', ylabel='y', mplprops={}):
    		pixelSize = self.width
    		axis = Axis.Axis(hideAxis, grid, arrows, color, lw, minorGrid, label, xlabel, ylabel, mplprops, figure=self)
    		self.drawOrder.append(axis)

    		return axis

    	def setPixelSize(self, width=400, height=None, padding=0):
    		"""Sets the pixel size of the figure.

    			Warning: Do NOT call this outside of the constructor

    			If only width is provided, then the figure will try to tight fit to that width
    			If height is also specified, then the size is completely fixed to that size
    		"""

    		self.width = width

    		# a point is 1/72in;  12pt = 16px
    		px2in = lambda p: (p * 0.75 / 72.0)

    		self.padding = px2in(padding)

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

    	def addPoint(self, xys, texts='\ ', pointsize=6, fontsize=12, color='black', latex=True, mplprops={}):
    		p = Point.Point(xys, texts, pointsize, fontsize, color, latex, mplprops, figure=self)
    		self.drawOrder.append(p)
    		return p

        def addLine(self, pointA, pointB, lw=2, color='k', mplprops={}):
            l = Line.Line(pointA, pointB, lw, color, mplprops, figure=self)
            self.drawOrder.append(l)
            return l

        def addText(self, xy, text, color="black", fontsize=12, halignment='center', valignment='top', bbox={}, mplprops={}, latex=True, pixel=False):
            t = Text.Text(xy, text, color, fontsize, halignment, valignment, bbox, latex, pixel, mplprops, figure=self)
            self.drawOrder.append(t)
            return t

        def addFunction(self, functions, xyranges=None, color='black', lw=2, variable=None, mplprops={}):
            xyranges= self.xyrange if xyranges == None else xyranges
            f = Function.Function(functions, xyranges, color, lw, variable, mplprops, figure=self)
            self.drawOrder.append(f)
            return f

            """
        def addBox(self, xy, xlabel='x', ylabel='y', lw=2, mplprops={}):
            b = Box.Box(xy, xlabel, ylabel, lw, mplprops, figure=self)
            self.drawOrder.append(f)
            return b
            """

    	def addPolygon(self, vertices, lw=2, mplprops={}):
    		pixelSize=self.width
    		polygon = Polygon.Polygon(vertices, lw, mplprops, figure=self)
    		self.drawOrder.append(polygon)
    		return polygon

    	def addRegularPolygon(self, xy=(0,0), numVertices=0, radius=None, fill=False, lw=2, orientation=0.0, mplprops={}):
    		pixelSize=self.width
    		regpolygon = RegularPolygon.RegularPolygon(xy, numVertices, radius, fill, lw, orientation, mplprops, figure=self)
    		self.drawOrder.append(regpolygon)
    		return regpolygon

    	def addCircle(self, xy=(0,0), diameter=None, radius=None, label="", fc='none', ec='k', lw=2, mplprops={}):
    		pixelSize=self.width
    		circle = Circle.Circle(xy, diameter, radius, label, fc, ec, lw, mplprops, figure=self)
    		self.drawOrder.append(circle)
    		return circle

    	def addEllipse(self, xy=[0,0], r=(1,1), fc='none', ec='k', angle=0.0, lw=2, mplprops={}):
    		if isinstance(r, int):
    			self.addCircle(xy=xy, radius=r, fc=fc, ec=ec, lw=lw, mplprops=mplprops)
    		else:
    			pixelSize=self.width
    			ellipse = Ellipse.Ellipse(xy, r, fc, ec, angle, lw, mplprops, figure=self)
    			self.drawOrder.append(ellipse)
    			return ellipse

    	def addArc(self, xy=(0,0), width=0, height=0, lw=2, angle=0.0, theta1=0.0, theta2=360.0, mplprops={}):
    		pixelSize=self.width
    		arc = Arc.Arc(xy, width, height, lw, angle, theta1, theta2, mplprops=mplprops, figure=self)
    		self.drawOrder.append(arc)
    		return arc

    	def addWedge(self, xy=(0,0), r=0, theta1=0, theta2=0, width=None, mplprops={}):
    		pixelSize=self.width
    		wedge = Wedge.Wedge(xy, r, theta1, theta2, width=width, mplprops=mplprops, figure=self)
    		self.drawOrder.append(wedge)
    		return wedge

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
    			triangle = Polygon.Polygon(np.delete((transformation * np.matrix([vertexA, vertexB, vertexC]).transpose()).transpose(), 2, axis=1), lw, mplprops, figure=self)
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
    			triangle = Polygon.Polygon(np.delete((transformation * np.matrix([vertexA, vertexB, vertexC]).transpose()).transpose(), 2, axis=1), lw, mplprops, figure=self)
    			self.drawOrder.append(triangle)
    			return triangle

    	def addArrow(self, xy, dxdy, color, lw=2, headWidth=0.1, mplprops={}, **kwargs):
            if 'arrowstyle' in kwargs:
    			self.addFancyArrow(posA=[xy[0],xy[1]], posB=[xy[0]+dxdy[0],xy[1]+dxdy[1]], lw=lw, path=None, color=color, arrowstyle=kwargs['arrowstyle'], connectionstyle=kwargs['connectionstyle'], mutation_scale=lw*5, mplprops={})
            else:
    			arrow = Arrow.Arrow(xy, dxdy, lw=lw, mplprops=mplprops, color=color, headWidth=headWidth, figure=self)
    			self.drawOrder.append(arrow)
    			return arrow

    	def addFancyArrow(self, posA, posB, path=None, color='black', lw=2, arrowstyle=None, connectionstyle=None, mutation_scale=3, mplprops={}):
            fancyArrow = FancyArrowPatch.FancyArrowPatch(posA, posB, path, color, lw, arrowstyle=arrowstyle, connectionstyle=connectionstyle, mplprops=mplprops, mutation_scale=mutation_scale, figure=self)
            self.drawOrder.append(fancyArrow)
            return fancyArrow
