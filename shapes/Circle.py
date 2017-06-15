import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Circle:
	def __init__(self, fig, ax, xy=(0,0), diameter=None, radius=None, label="a"):
		if radius!=None:
			circle = patches.Circle(xy, radius=radius, fill=False, linewidth=3)

			p = (xy[0]+radius, xy[1])
			plt.plot([xy[0],p[0]], [xy[1],p[1]], linewidth=2, ls='dashed', color='black')

			mid_radius = (xy[0]+p[0])/2.0
			textobj = ax.text(mid_radius, xy[1]*1.015, '$'+label+'$', fontsize=25)

			# Find out the pixel measurements of the text's bounding box
			renderer = FigureCanvasAgg(fig).get_renderer()
			bbox = textobj.get_window_extent(renderer)
			# Find out what one horizontal and vertical unit is in pixel
			conversion_matrix = ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0))
			# Multiply the width in pixels by 1/width-conversion
			width = (bbox.bounds[2]*(1/conversion_matrix[1,0]))/2
			# Left shift it
			textobj.set_position((mid_radius-width, xy[1]*1.015))

		else:
			circle = patches.Circle(xy, radius=diameter, fill=False, linewidth=3)

			p1 = (xy[0]-diameter, xy[1])
			p2 = (xy[0]+diameter, xy[1])
			plt.plot([p1[0],p2[0]], [p1[1],p2[1]], linewidth=2, ls='dashed', color='black')

			textobj = ax.text(xy[0], xy[1]*1.015, '$'+label+'$', fontsize=25)

			# Find out the pixel measurements of the text's bounding box
			renderer = FigureCanvasAgg(fig).get_renderer()
			bbox = textobj.get_window_extent(renderer)
			# Find out what one horizontal and vertical unit is in pixel
			conversion_matrix = ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0))
			# Multiply the width in pixels by 1/width-conversion
			width = (bbox.bounds[2]*(1/conversion_matrix[1,0]))/2
			# Left shift it
			textobj.set_position((xy[0], xy[1]*1.015))

		ax.add_patch(circle)
