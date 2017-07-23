"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Box:
	def __init__(self, xy, xlabel='x', ylabel='y',  lw=2, mplprops={}, figure=None):
        self.xy         = xy
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.lw	        = lw
		self.mplprops   = mplprops

	def __draw__(self, zorder=1):
		for xy, xlabel, ylabel, figure, lw in zip(self.xy, self.xlabel, self.ylabel, self.lw):
			plt.plot(xy[0], xy[1], xlabel=xlabel, ylabel=ylabel, lw=lw, zorder=zorder, **self.mplprops)
"""
            """
            if type is 'bar':

            if type is 'scatter':
                plt.scatter(x, y, s=area, c=colors, alpha=0.5)

            if type is ''
            """

"""

N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radii

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()

"""
"""
dashes = [10, 5, 100, 5]

fig, ax = plt.subplots()
line1, = ax.plot(x, np.sin(x), '--', linewidth=2,
                 label='Dashes set retroactively')
line1.set_dashes(dashes)

line2, = ax.plot(x, -1 * np.sin(x), dashes=[30, 5, 10, 5],
                 label='Dashes set proactively')

ax.legend(loc='lower right')
plt.show()
"""
