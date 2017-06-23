import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Function:
	matplotlib_obj = None
	def __init__(self, fig, ax, functions, xyranges=None, color='black', linewidth=2, variable=None):
		if not isinstance(functions, list):
			functions = [functions]

		if not isinstance(color, list):
			xyranges = [xyranges] * len(functions)
			color = [color] * len(functions)

		if variable is not None:
			if not isinstance(variable, list):
				variable = [variable] * len(functions)
			function_lam = [lambdify(v, f, "numpy") for f, v in zip(functions, variable)]

		self.functions = functions
		self.function_lam = function_lam if variable is not None else None
		self.xyranges = xyranges
		self.color = color
		self.variable = variable



	def __draw__(self, zorder=1):
		for function, xyrange, color in zip(self.function_lam if self.variable is not None else self.functions, self.xyranges, self.color):
			x = np.linspace(xyrange[0][0], xyrange[0][1], 350)
			y = function(x)
			plt.plot(x, y, color, zorder=zorder)
