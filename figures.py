import matplotlib
matplotlib.use('Svg') # Change renderer so it doesn't use the GUI
matplotlib.rcParams['mathtext.fontset'] = 'cm' # Change font to Computer Modern (LaTeX font)
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [10,10]
from shapes import Polygon, Circle, Ellipse

import numpy as np
import StringIO

class Figures:
	def __init__(self):
		self.fig, self.ax = plt.subplots()
		self.tick_interval = .25
		self.tick_label_interval = 1
		self.tight_fit = True
		self.padding = 0

	def __export__(self):
		export_str = StringIO.StringIO()
		self.__writeFile__(export_str, format='svg')
		export_str.seek(0)  # rewind the data
		return export_str.buf  # this is svg data

	def __writeFile__(self, file_location, **kwargs):
		self.fig.savefig(file_location, bbox_inches=('tight' if self.tight_fit else None), pad_inches=self.padding, **kwargs)

	def __display__(self):
		plt.show()

	def format_axis(self, xyrange=None, grid=False, arrows=True, color='black'):
		# Modify the plot view to scale, remove axis, and center our shape

		color_dict = {
			"blue": 'b',
			"green": 'g',
			"red": 'r',
			"cyan": 'c',
			"magenta": 'm',
			"yellow": 'y',
			"black": 'k',
			"white": 'w'
		}

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
			self.ax.set_xlim(left=xyrange[0][0], right=xyrange[0][1])
			self.ax.set_ylim(bottom=xyrange[1][0], top=xyrange[1][1])

			self.ax.spines['right'].set_color('none')
			self.ax.spines['top'].set_color('none')

			self.ax.spines['left'].set_position(('data', 0))
			self.ax.spines['bottom'].set_position(('data', 0))

		if grid:
			self.ax.grid(color='k', linestyle='dashed', linewidth=.5, alpha=0.5)

		if arrows:
			xmin, xmax = self.ax.get_xlim()
			ymin, ymax = self.ax.get_ylim()

			self.ax.arrow(xmin, 0, xmax-xmin, 0., lw = 1,
			         head_width=self.tick_interval/3, head_length=self.tick_interval/3,
			         length_includes_head=True, clip_on=False,color=color_dict[color])

			self.ax.arrow(0, ymin, 0., ymax-ymin, lw = 1,
			         head_width=self.tick_interval/3, head_length=self.tick_interval/3,
					 length_includes_head=True, clip_on=False,color=color_dict[color])


		# Control color
		self.ax.spines['bottom'].set_color(color_dict[color])
		self.ax.spines['left'].set_color(color_dict[color])



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

		if height != None:
			self.tight_fit = False
			self.fig.set_tight_layout({ "pad": self.padding })
			height_in = px2in(height)

		self.fig.set_size_inches((width_in, height_in))


	def addPoint(self, xys, texts, pointsize=6, fontsize=12, colors='black'):
		color_dict = {
			"blue": 'b',
			"green": 'g',
			"red": 'r',
			"cyan": 'c',
			"magenta": 'm',
			"yellow": 'y',
			"black": 'k',
			"white": 'w'
		}
		if not isinstance(colors, list):
			colors = [colors]
			xys = [xys]
			texts = [texts]

		for xy, text, color in zip(xys, texts, colors):
			plt.plot(xy[0], xy[1], 'o{}'.format(color_dict[color]), ms=pointsize)
			self.ax.annotate(text, xytext=xy, xy=xy, fontsize=fontsize, horizontalalignment='center', textcoords='offset points')


	def addText(self, xy, text, color="black", fontsize=12, alignment='center'):
		color_dict = {
			"blue": 'b',
			"green": 'g',
			"red": 'r',
			"cyan": 'c',
			"magenta": 'm',
			"yellow": 'y',
			"black": 'k',
			"white": 'w'
		}
		if not isinstance(color, list):
			color = [color]
			xy = [xy]
			text = [text]
			alignment = [alignment]

		for xy, text, color, alignment in zip(xy, text, color, alignment):
			self.ax.annotate(text, xytext=xy, xy=xy, fontsize=fontsize, horizontalalignment=alignment)

	def addFunction(self, functions, xyranges, colors='black', linewidth=2):
		color_dict = {
			"blue": 'b',
			"green": 'g',
			"red": 'r',
			"cyan": 'c',
			"magenta": 'm',
			"yellow": 'y',
			"black": 'k',
			"white": 'w'
		}

		if not isinstance(functions, list):
			functions = [functions]
			xyranges = [xyranges]
			colors = [colors]

		for function, xyrange, color in zip(functions, xyranges, colors):
			x = np.linspace(xyrange[0][0], xyrange[0][1], 1000)
			y = function(x)
			self.ax.plot(x, y, color_dict[color])


	def addTicks(self, tick_label_interval=1, tick_interval=1, fontsize=12):
		self.tick_interval = tick_interval
		self.tick_label_interval = tick_label_interval
		# Control ticks
		self.ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(tick_label_interval))
		self.ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(tick_label_interval))
		self.ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(tick_interval))
		self.ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(tick_interval))
		self.ax.tick_params(axis='both', which='major', labelsize=fontsize)
		#self.ax.tick_params(axis='both', which='minor', labelsize=8)

	def addPolygon(self, vertices):
		polygon = Polygon.Polygon(vertices, self.fig, self.ax)
		return polygon

	def addCircle(self, xy=(0,0), diameter=None, radius=None, label=None):
		circle = Circle.Circle(self.fig, self.ax, xy, diameter, radius, label)
		return circle

	def addEllipse(self, xy=(0,0), width=None, height=None, wlabel=None, hlabel=None, is_radius=True):
		ellipse = Ellipse.Ellipse(self.fig, self.ax, xy, width, height, wlabel, hlabel, is_radius)
		return ellipse

	def addTriangle_angle(self, xy=(0,0), angle=(45*np.pi)/180, rotation=0):
		# Define the angles and sides
		alpha = angle
		beta = np.pi/2
		gamma = ((np.pi-beta-alpha))

		A = 1
		B = np.sin(beta)/np.sin(alpha)
		C = np.sin(gamma)/np.sin(alpha)

		# Define the vertices
		vertex_A = [0+xy[0], A+xy[1]]
		vertex_B = xy
		vertex_C = [C+xy[0], 0+xy[1]]

		polygon = Polygon.Polygon([vertex_A, vertex_B, vertex_C], self.fig, self.ax)

		# Perform the rotation if at all
		transformation = matplotlib.transforms.Affine2D().rotate(rotation) + self.ax.transData
		polygon.matplotlib_obj.set_transform(transformation)

		# Create and add polygon
		#self.ax.add_patch(polygon)

		return polygon

	def addTriangle_side(self):
		raise Exception('Not implemented yet!')
