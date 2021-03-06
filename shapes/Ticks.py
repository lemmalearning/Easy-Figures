import matplotlib.pyplot as plt
import math
import numpy as np

class Ticks:
	"""
	Creates an Axis object which contains ticks, spine arrows, and grids.

	__init__ - Creates the object and sets the various class variables
	Ticks - Creates the class variables required for drawing tick marks
	__draw__ - Draws the axis and tick marks according to class variables
	"""

	def __init__(self, grid, minorGrid, ticks, xticks, yticks, minorticks, xminorticks, yminorticks, fontsize, boxOrigin, origin, top, customLabels, figure):
		self.grid = grid
		self.minorGrid = minorGrid
		self.minorticks = minorticks
		self.xminorticks = xminorticks
		self.yminorticks = yminorticks
		self.xticks = xticks
		self.yticks = yticks
		self.ticks = ticks

		x_isdict = isinstance(customLabels, list) and customLabels != [] and isinstance(customLabels[0], dict)
		if x_isdict:
			x_0 =  len(set(['0', 0, 0.0, '0.0']).intersection(customLabels[0].keys())) > 0 # 0 in the x axis exists
		else:
			x_0 = False

		y_isdict = isinstance(customLabels, list) and customLabels != [] and isinstance(customLabels[1], dict)
		if y_isdict:
			y_0 = len(set(['0', 0, 0.0, '0.0']).intersection(customLabels[1].keys())) > 0  # 0 in the y axis exists
		else:
			y_0 = False

		if boxOrigin == True:
			self.boxOrigin = True
		elif (x_0 or y_0) and not boxOrigin:
			self.boxOrigin = [x_0, y_0]
		else:
			self.boxOrigin = boxOrigin


		self.customLabels = customLabels

		if self.ticks:
			self.xticks = self.yticks = self.ticks
		if self.minorticks:
			self.xminorticks = self.yminorticks = self.minorticks

		if not self.minorticks and self.ticks:
			self.minorticks = self.xminorticks = self.yminorticks = self.ticks/2.0

		self.fontsize = fontsize
		self.origin = origin
		self.top = top
		self.figure = figure

	def serialize(self):
		# The customLabels will be of the form [ { xValue: 'xLabel', ...}, { .. same for y ... } ]


		# The 0.001 is so that it includes the ending as well
		major_x = []
		major_y = []
		if self.xticks:
			major_x = np.arange(
				math.ceil(self.figure.xyrange[0][0] / self.xticks) * self.xticks,
				self.figure.xyrange[0][1] + 0.001,
				self.xticks
			)
		if self.yticks:
			major_y = np.arange(
				math.ceil(self.figure.xyrange[1][0] / self.yticks) * self.yticks,
				self.figure.xyrange[1][1] + 0.001,
				self.yticks
			)

		minor_x = []
		minor_y = []
		if self.xminorticks:
			minor_x = np.arange(
				math.ceil(self.figure.xyrange[0][0] / self.xminorticks) * self.xminorticks,
				self.figure.xyrange[0][1] + 0.001,
				self.xminorticks
			)
		if self.yminorticks:
			minor_y = np.arange(
				math.ceil(self.figure.xyrange[1][0] / self.yminorticks) * self.yminorticks,
				self.figure.xyrange[1][1] + 0.001,
				self.yminorticks
			)


		xticks = [ { "value": v, "label": str(v).rstrip('0').rstrip('.') if (v != 0 or self.origin) else None, "type": "major", "line": self.grid } for v in major_x ]
		yticks = [ { "value": v, "label": str(v).rstrip('0').rstrip('.') if v != 0 else None, "type": "major", "line": self.grid } for v in major_y ]

		for v in minor_x:
			if v in major_x:
				continue

			xticks.append({ "value": v, "label": None, "type": "minor", "line": self.minorGrid })

		for v in minor_y:
			if v in major_y:
				continue

			yticks.append({ "value": v, "label": None, "type": "minor", "line": self.minorGrid })


		customLabels = self.customLabels
		if customLabels != None:
			if customLabels[0]:
				for i in range(0, len(xticks)):
					v = xticks[i]["value"]
					xticks[i]["label"] = customLabels[0][v] if v in self.customLabels[0] else None

			if customLabels[1]:
				for i in range(0, len(yticks)):
					v = yticks[i]["value"]
					yticks[i]["label"] = customLabels[1][v] if v in self.customLabels[1] else None


		return {
			# TODO: This assumes that a floating point tick interval was given
			"xticks": xticks,
			"yticks": yticks,
			"showOrigin": self.origin
		}

	def check_MAXTICK(self):
		"""
		Checks the tick amounts to ensure they aren't generating greater than MAXTICKS
		:return: NONE
		"""
		MAXTICKS = 10000 # Matplotlib specified

		if self.ticks and (self.figure.abs_range_x / self.ticks > MAXTICKS or self.figure.abs_range_y / self.ticks > MAXTICKS):
			raise Exception("Tick count too high")
		if self.minorticks and (self.figure.abs_range_x / self.minorticks > MAXTICKS or self.figure.abs_range_y / self.minorticks > MAXTICKS):
			raise Exception("Tick count too high")
		if self.xticks and self.figure.abs_range_x / self.xticks > MAXTICKS:
			raise Exception("Tick count too high")
		if self.xminorticks and self.figure.abs_range_x / self.xminorticks > MAXTICKS:
			raise Exception("Tick count too high")
		if self.yticks and self.figure.abs_range_y / self.yticks > MAXTICKS:
			raise Exception("Tick count too high")
		if self.yminorticks and self.figure.abs_range_y / self.yminorticks > MAXTICKS:
			raise Exception("Tick count too high")

	def __draw__(self, zorder=1, box=False):
		# Parse the grid color:
		gridColor = self.figure.GRID[:-2]
		gridAlpha = int(self.figure.GRID[-2:], 16) / 256.0
		if self.grid is not False:
			self.figure.ax.grid(which='major', color=gridColor if self.grid == True else self.grid,
			                    linestyle='dashed', linewidth=.5, alpha=gridAlpha)
		if self.minorGrid is not False:
			self.figure.ax.grid(which='minor', color=gridColor if self.minorGrid == True else self.minorGrid,
			                    linestyle='dashed', linewidth=.3, alpha=gridAlpha)

		####### DRAW LABELS #######
		if isinstance(self.ticks, int) and isinstance(self.minorticks, int) and self.ticks > self.minorticks:
			self.minorGrid = True


		self.check_MAXTICK() # check to make sure there aren't too many ticks

		plt.gca().xaxis.set_major_locator(plt.MultipleLocator(self.xticks) if self.xticks is not False else plt.NullLocator())
		plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(self.xminorticks) if self.xminorticks is not False else plt.NullLocator())
		plt.gca().yaxis.set_major_locator(plt.MultipleLocator(self.yticks) if self.yticks is not False else plt.NullLocator())
		plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(self.yminorticks) if self.yminorticks is not False else plt.NullLocator())



		self.figure.ax.tick_params(axis='both', which='major', labelsize=self.fontsize)

		ylabels = []
		for item in self.figure.ax.get_yticks():
			if float(item) == 0 and not self.boxOrigin==True and not (isinstance(self.boxOrigin, list) and self.boxOrigin[1]):
				ylabels.append("")
			elif math.floor(float(item)) == float(item):  # it's an int
				ylabels.append(int(item))
			else:
				ylabels.append(float(item))

		xlabels = []
		for item in self.figure.ax.get_xticks():
			if float(item) == 0 and not self.boxOrigin==True and not (isinstance(self.boxOrigin, list) and self.boxOrigin[0]):
				xlabels.append("        (0,0)" if self.origin else "")
			elif math.floor(float(item)) == float(item):  # it's an int
				xlabels.append(int(item))
			else:
				xlabels.append(float(item))

		if self.customLabels and (self.customLabels[0] or self.customLabels[0] == {}):
			for i,label in enumerate(xlabels):
				if label == '':
					continue
				key = None
				if int(label) in self.customLabels[0]:
					key = int(label)
				if float(label) in self.customLabels[0]:
					key = float(label)
				if str(label) in self.customLabels[0]:
					key = str(label)

				if key != None:
					if self.customLabels[0][key] == 'auto':
						continue
					else:
						xlabels[i] = self.customLabels[0][key]
				else:
					xlabels[i] = ''
		if self.customLabels and (self.customLabels[1] or self.customLabels[1] == {}):
			for i, label in enumerate(ylabels):
				if label == '':
					continue
				key = None
				if int(label) in self.customLabels[1]:
					key = int(label)
				if float(label) in self.customLabels[1]:
					key = float(label)
				if str(label) in self.customLabels[1]:
					key = str(label)

				if key != None:
					if self.customLabels[1][key] == 'auto':
						continue
					else:
						ylabels[i] = self.customLabels[1][key]
				else:
					ylabels[i] = ''
		else:
			xlabels=xlabels[:-1]
			ylabels=ylabels[:-1]


		self.figure.ax.set_yticklabels([str(label).replace("-", "$-$") for label in ylabels])
		self.figure.ax.set_xticklabels([str(label).replace("-", "$-$") for label in xlabels])

		for label in self.figure.ax.xaxis.get_ticklabels():
			label.set_bbox(dict(boxstyle='round', facecolor=self.figure.bgcolor, edgecolor='none', pad=0.1))
			if '$' not in label.get_text() and not box:
				label.set_horizontalalignment('left')

		for label in self.figure.ax.yaxis.get_ticklabels():
			label.set_bbox(dict(boxstyle='round', facecolor=self.figure.bgcolor, edgecolor='none', pad=0.1))
			if '$' not in label.get_text() and not box:
				label.set_verticalalignment('bottom')

		if self.top:
			self.figure.ax.xaxis.set_label_position('top')
