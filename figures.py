import matplotlib
matplotlib.use('Svg') # Change renderer so it doesn't use the GUI
matplotlib.rcParams['font.family'] = 'cmr10' # Change font to Computer Modern (LaTeX font)
import matplotlib.pyplot as plt
#plt.rcParams.update({'text.usetex': True})
plt.rcParams["figure.figsize"] = [10,10]
#matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.sans-serif'] = ['cm']
from shapes import Polygon, Circle, Ellipse, Arrow

import numpy as np
import StringIO
import math
import re
from sympy.utilities.lambdify import lambdify


class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()
		self.fig.set_dpi(72)
		self.tickInterval = 0
		self.tickLabelInterval = 1
		self.tight_fit = True
		self.padding = 0
		self.height = None

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

	def axisFormat(self, hideAxis=False, xyrange=None, grid=False, arrows=True, color='black', minorGrid=False):
		self.xyrange = xyrange
		# Modify the plot view to scale, remove axis, and center our shape
		def adjust_spines(ax, spines):
		    for loc, spine in ax.spines.items():
		        if loc in spines:
		            spine.set_position(('outward', 10))  # outward by 10 points
		            spine.set_smart_bounds(True)
		        else:
		            spine.set_color('none')  # don't draw spine

		    # turn off ticks where there is no spine
		    if 'left' in spines:
		        ax.yaxis.set_ticks_position('left')
		    else:
		        # no yaxis ticks
		        ax.yaxis.set_ticks([])

		    if 'bottom' in spines:
		        ax.xaxis.set_ticks_position('bottom')
		    else:
		        # no xaxis ticks
		        ax.xaxis.set_ticks([])

		if xyrange == None:
			plt.axis('off')
			plt.axis('scaled')
		else:
			plt.gca().set_aspect('equal', adjustable='box')
			self.ax.set_xlim(left=xyrange[0][0]+.1, right=xyrange[0][1]-.1)
			self.ax.set_ylim(bottom=xyrange[1][0]+.1, top=xyrange[1][1]-.1)

			self.ax.spines['right'].set_color('none')
			self.ax.spines['top'].set_color('none')

			self.ax.spines['left'].set_position(('data', 0))
			self.ax.spines['bottom'].set_position(('data', 0))

		if hideAxis:
			plt.axis('off')
			return

		if grid is not False:
			self.ax.grid(which='major', color='k' if grid == True else grid, linestyle='dashed', linewidth=.5, alpha=0.5)
			if minorGrid is not False:
				self.ax.grid(which='minor', color='k' if minorGrid == True else minorGrid, linestyle='dashed', linewidth=.3, alpha=0.25)

		if arrows:
			xmin, xmax = self.ax.get_xlim()
			ymin, ymax = self.ax.get_ylim()

			self.ax.arrow(xmin, 0, xmax-xmin, 0., lw = 1,
			         head_width=0.1875, head_length=.3,
			         length_includes_head=True, clip_on=False,color=color)

			self.ax.arrow(0, ymin, 0., ymax-ymin, lw = 1,
			         head_width=.1875, head_length=.3,
					 length_includes_head=True, clip_on=False,color=color)


		# Control color
		self.ax.spines['bottom'].set_color(color)
		self.ax.spines['left'].set_color(color)



	def setPixelSize(self, width=400, height=None, padding=0):
		"""Sets the pixel size of the figure.

			If only width is provided, then the figure will try to tight fit to that width
			If height is also specified, then the size is completely fixed to that size
		"""

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
		if not isinstance(colors, list):
			colors = [colors]
			xys = [xys]
			texts = [texts]

		for xy, text, color in zip(xys, texts, colors):
			plt.plot(xy[0], xy[1], 'o{}'.format(color), ms=pointsize)
			self.ax.annotate("$"+text+"$" if latex else text, xytext=xy, xy=xy, fontsize=fontsize, horizontalalignment='center', textcoords='offset points')

	def addText(self, xy, text, color="black", fontsize=12, halignment='center', valignment='top', bbox={}, latex=True):
		if not isinstance(color, list):
			color = [color]
			xy = [xy]
			text = [text]
			halignment = [halignment]
			valignment = [valignment]
			bbox = [bbox]
			latex = [latex]

		for xy, text, color, valignment, halignment, bbox, latex in zip(xy, text, color, valignment, halignment, bbox, latex):
			self.ax.annotate("$"+text+"$" if latex else text, xytext=xy, xy=xy, fontsize=fontsize, horizontalalignment=halignment, verticalalignment=valignment, bbox=bbox, color=color)

	def addFunction(self, functions, xyranges=None, colors='black', linewidth=2, variable=None):
		if xyranges is None:
			xyranges = self.xyrange
		if not isinstance(functions, list):
			functions = [functions]

		if not isinstance(colors, list):
			xyranges = [xyranges] * len(functions)
			colors = [colors] * len(functions)

		if variable is not None:
			if not isinstance(variable, list):
				variable = [variable] * len(functions)
			function_lam = [lambdify(v, f, "numpy") for f, v in zip(functions, variable)]

		for function, xyrange, color in zip(function_lam, xyranges, colors):
			x = np.linspace(xyrange[0][0], xyrange[0][1], 350)
			y = function(x)
			self.ax.plot(x, y, color)


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
		return polygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label="", fc='w', ec='k'):
		circle = Circle.Circle(self.fig, self.ax, xy, diameter, radius, label, fc, ec)
		return circle

	def addEllipse(self, xy=(0,0), r=(1,1), fc='w', ec='k', angle=0.0, lw=2):
		if isinstance(r, int):
			self.addCircle(xy=xy, radius=r, fc=fc, ec=ec)
		else:
			ellipse = Ellipse.Ellipse(self.fig, self.ax, xy, r, fc, ec, angle, lw)
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

		return polygon

	def addTriangle_side(self, xy=(0,0), p1=(0,0), p2=(0,0), rotation=0):

		polygon = Polygon.Polygon([vtx1, vtx2, vtx3], self.fig, self.ax)

		return polygon
		#raise Exception('Not implemented yet!')

	def addArrow(self, xy, dxdy, color='black', headWidth=0.1, width=0.35):
		return Arrow.Arrow(self.ax, self.fig, xy, dxdy, color=color, headWidth=headWidth, width=width)
