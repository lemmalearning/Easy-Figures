import matplotlib.pyplot as plt
import numpy as np
from sympy.utilities.lambdify import lambdify
from sympy.printing.jscode import jscode
from sympy import Expr

class Function:
	matplotlib_obj = None
	def __init__(self, functions, xyranges, color, lw, variable, mplprops, figure):
		if not isinstance(functions, list):
			functions = [functions]
			lw = [lw] * len(functions)
			xyranges = list([xyranges]) * len(functions)
			color = [color] * len(functions)
		elif isinstance(functions, list):
			lw = [lw] * len(functions)
			xyranges = list([xyranges]) * len(functions)
			color = [color] * len(functions)

		# For sympy functions, if the variable is not included, pick the first one
		if variable is None and len(functions) > 0 and isinstance(functions[0], Expr):
			variable = [ (list(e.free_symbols)[0] if len(e.free_symbols) > 0 else None) for e in functions ]
			
		if variable is not None:
			if not isinstance(variable, list):
				variable = [variable] * len(functions)
			function_lam = [lambdify(v, f, "numpy") if v != None else np.vectorize(lambdify("x", f, "numpy")) for f, v in zip(functions, variable)]
			

		self.functions = functions
		self.function_lam = function_lam if variable is not None else None
		self.xyranges = xyranges
		self.color = color
		self.lw = lw
		self.variable = variable
		self.mplprops = mplprops
		self.figure = figure

	def __draw__(self, zorder=1):
		for function, xyrange, color, lw in zip(self.function_lam if self.variable is not None else self.functions, self.xyranges, self.color, self.lw):
			if xyrange == None:
				xyrange = self.figure.xyranges

			x = np.linspace(xyrange[0][0], xyrange[0][1], 350)
			y = function(x)
			plt.plot(x, y, color, lw=lw, zorder=zorder, **self.mplprops)

	def serialize(self):
		arr = []
		for i in range(0, len(self.functions)):
			f = self.functions[i]
			if not isinstance(f, Expr):
				raise Exception("Must only use sympy expressions when serializing")

			arr.append({
				"type": "Function",
				"lineWidth": self.figure.raw2px(self.lw[i]), # TODO: We need to convert from pt to px
				"edgeColor": self.color[i],
				"lineStyle": self.mplprops["ls"] if self.mplprops != None and "ls" in self.mplprops else None,
				"value": jscode(f),
				"variable": str(self.variable[i]) if self.variable[i] != None else None,
				"domain": self.xyranges[i][0] if self.xyranges[i] else None
			})

		return arr
