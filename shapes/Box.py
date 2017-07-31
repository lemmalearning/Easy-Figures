import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Box:
	matplotlib_obj = None
	def __init__(self, x, y, xlabel='x', ylabel='y', title=None, lw=2, mplprops={}, figure=None):
		self.x          = x
		self.y			= y
		#self.data 		= data
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.title 		= title
		self.lw	        = lw
		self.mplprops   = mplprops

	def __draw__(self, zorder=1):
		for x, y, xlabel, ylabel, title in zip(self.x, self.y, self.xlabel, self.ylabel, self.title):
			plt.axis('on')
			plt.axis([self.x[0], self.x[1], self.y[0], self.y[1]])
			plt.title(self.title)
			plt.xlabel(self.xlabel)
			plt.ylabel(self.ylabel)
			#plt.plot(self.data)
			"""

			objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
			y_pos = np.arange(len(objects)) #left: sequence of scalars
			performance = [10,8,6,4,2,1]  #height

			plt.bar(y_pos, performance, align='center', alpha=0.2) #drawing the bars
			plt.xticks(y_pos, objects)  #tick labels

			#bar(left, height, width=0.8, bottom=None, hold=None, data=None, **kwargs)
			"""
