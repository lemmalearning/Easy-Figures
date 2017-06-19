import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Ellipse:
	def __init__(self, fig, ax, xy=(0,0), width=None, height=None, wlabel=None, hlabel=None, is_radius=True, fc=None):
		if is_radius:
			ellipse = patches.Ellipse(xy, width, height, linewidth=3, fc=fc)

			w_p = (xy[0]+(width/2.0), xy[1])
			h_p = (xy[0], xy[1]+(height/2.0))

			plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

			width/=2
			height/=2

			mid_rwidth = (xy[0]+w_p[0])/2.0
			mid_rheight = (xy[1]+h_p[1])/2.0
			if wlabel!=None or hlabel!=None:
				textwobj = ax.text(mid_rwidth, xy[1]*1.025, '$'+wlabel+'$', fontsize=25)
				texthobj = ax.text(xy[0]*1.025, mid_rheight, '$'+hlabel+'$', fontsize=25)

				# Find out the pixel measurements of the text's bounding box
				renderer = FigureCanvasAgg(fig).get_renderer()
				wbbox = textwobj.get_window_extent(renderer)
				hbbox = texthobj.get_window_extent(renderer)
				# Find out what one horizontal and vertical unit is in pixel
				conversion_matrix = ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0))
				# Multiply the width in pixels by 1/width-conversion
				wwidth = (wbbox.bounds[2]*(1/conversion_matrix[1,0]))/2
				hheight = (25*(1/conversion_matrix[1,0]))/2
				# Left shift it
				textwobj.set_position((mid_rwidth-wwidth, (xy[1]+0.2)))
				texthobj.set_position(((xy[0]+0.2), mid_rheight-hheight))

		else:
			ellipse = patches.Ellipse(xy, width, height, linewidth=3, fc=fc)

			w_p1 = (xy[0]+(width/2.0), xy[1])
			w_p2 = (xy[0]-(width/2.0), xy[1])
			h_p1 = (xy[0], xy[1]+(height/2.0))
			h_p2 = (xy[0], xy[1]-(height/2.0))

			plt.plot([w_p2[0],w_p1[0]], [xy[1], xy[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([xy[0],xy[0]], [h_p1[1], h_p2[1]], linewidth=2, ls='dashed', color='black')

			mid_rwidth = (xy[0]+w_p1[0])/2.0
			mid_rheight = (xy[1]+h_p1[1])/2.0

			if wlabel!=None:
				textwobj = ax.text(mid_rwidth, xy[1]*1.025, '$'+wlabel+'$', fontsize=25)
				texthobj = ax.text(xy[0]*1.025, mid_rheight, '$'+hlabel+'$', fontsize=25)

				# Find out the pixel measurements of the text's bounding box
				renderer = FigureCanvasAgg(fig).get_renderer()
				wbbox = textwobj.get_window_extent(renderer)
				hbbox = texthobj.get_window_extent(renderer)
				# Find out what one horizontal and vertical unit is in pixel
				conversion_matrix = ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0))
				# Multiply the width in pixels by 1/width-conversion
				wwidth = (wbbox.bounds[2]*(1/conversion_matrix[1,0]))/2
				hheight = (25*(1/conversion_matrix[1,0]))/2
				# Left shift it
				textwobj.set_position((mid_rwidth-wwidth, (xy[1]+0.2)))
				texthobj.set_position((xy[0]+0.2, mid_rheight-hheight))

		ax.add_patch(ellipse)
