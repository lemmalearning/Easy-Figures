
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Arrow:
	matplotlib_obj = None
	def __init__(self, ax, fig, xy, dxdy, color='black', head_width=0.15, width=0.015):
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
		self.matplotlib_obj = ax.arrow(xy[0], xy[1], dxdy[0], dxdy[1], length_includes_head=True, width=width, head_width=head_width, head_length=2*head_width, fc=color_dict[color], ec=color_dict[color])
