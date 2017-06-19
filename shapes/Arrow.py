
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Arrow:
	def __init__(self, xy, dxdy, color='black'):
		ax.arrow(xy[0], xy[1], dxdy[0], dxdy[1],, head_width=0.05, head_length=0.1, fc='k', ec='k')
