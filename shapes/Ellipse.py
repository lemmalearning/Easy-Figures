import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Ellipse:
	matplotlib_obj = None
	def __init__(self, fig, ax, xy=(0,0), width=None, height=None, wlabel="", hlabel="", is_radius=True):
		if is_radius:
			ellipse = patches.Ellipse(xy, width, height, fill=False, linewidth=3)
			self.matplotlib_obj = ellipse
			if hlabel != "" and wlabel != "":
				w_p = (xy[0]+(width/2.0), xy[1])
				h_p = (xy[0], xy[1]+(height/2.0))

				plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
				plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

				width/=2
				height/=2

				mid_rwidth = (xy[0]+w_p[0])/2.0
				mid_rheight = (xy[1]+h_p[1])/2.0

				textwobj = ax.text(mid_rwidth, xy[1]*1.025, '$'+wlabel+'$', fontsize=25, horizontalalignment='center')
				texthobj = ax.text(xy[0]*1.025, mid_rheight, '$'+hlabel+'$', fontsize=25, verticalalignment='center')

		else:
			ellipse = patches.Ellipse(xy, width, height, fill=False, linewidth=3)
			self.matplotlib_obj = ellipse
			if hlabel != "" and wlabel != "":
				w_p1 = (xy[0]+(width/2.0), xy[1])
				w_p2 = (xy[0]-(width/2.0), xy[1])
				h_p1 = (xy[0], xy[1]+(height/2.0))
				h_p2 = (xy[0], xy[1]-(height/2.0))

				plt.plot([w_p2[0],w_p1[0]], [xy[1], xy[1]], linewidth=2, ls='dashed', color='black')
				plt.plot([xy[0],xy[0]], [h_p1[1], h_p2[1]], linewidth=2, ls='dashed', color='black')

				mid_rwidth = (xy[0]+w_p1[0])/2.0
				mid_rheight = (xy[1]+h_p1[1])/2.0

				textwobj = ax.text(mid_rwidth, xy[1]*1.025, '$'+wlabel+'$', fontsize=25, horizontalalignment='center')
				texthobj = ax.text(xy[0]*1.025, mid_rheight, '$'+hlabel+'$', fontsize=25, verticalalignment='center')


		ax.add_patch(ellipse)
