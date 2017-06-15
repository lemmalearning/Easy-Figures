import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Ellipse:
	def __init__(self, fig, ax, xy=(0,0), w_diameter=None, h_diameter=None, w_radius=None, h_radius=None, w_label=None, h_label=None):
		if w_radius!=None:
			ellipse = patches.Ellipse(xy, width, height, angle=0.0, fill=False, linewidth=3)

			w_p = (xy[0]+w_radius, xy[1])
			h_p = (xy[0], xy[1]+h_radius)

			plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

			mid_w_radius = (xy[0]+w_p[0])/2.0
			mid_h_radius = (xy[0]+h_p[0])/2.0
			textobj = plt.text(mid_w_radius, xy[1]+100, "$"+label+"$", fontsize=25)
			textobj = plt.text(mid_h_radius+100, xy[1], "$"+label+"$", fontsize=25)

			bb = textobj.get_axes().get_window_extent()

			textobj.set_position((mid_x_radius-(bb.width/2.0), xy[1]+100))
			textobj.set_position((mid_y_radius-(bb.width/2.0), xy[1]+100))

		else:
			ellipse = patches.Ellipse(xy, width, height, angle=0.0, fill=False, linewidth=3)

			w_p1 = (xy[0]+w_radius, xy[1])
			w_p2 = (xy[0]-w_radius, xy[1])
			h_p1 = (xy[0], xy[1]+h_radius)
			h_p2 = (xy[0], xy[1]-h_radius)

			plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

			textobj = plt.text(xy[0], xy[1]+100, "$"+label+"$", fontsize=25)
			textobj = plt.text(xy[0]+100, xy[1], "$"+label+"$", fontsize=25)

			bb = textobj.get_axes().get_window_extent()

			textobj.set_position((xy[0]-(bb.width/2.0), xy[1]+100))
			#textobj.set_position((xy[0]-(bb.width/2.0), xy[1]+100))

		ax.add_patch(circle)
