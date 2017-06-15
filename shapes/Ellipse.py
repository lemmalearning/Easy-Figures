import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Ellipse:
    def __init__(self, fig, ax, xy=(0,0), width=None, height=None, wlabel=None, hlabel=None, dwidth=None, dheight=None):
        if width!=None:
            #0300, label 0300
            ellipse = patches.Ellipse(xy, width, height, fill=False, linewidth=3)

            #xy=(6,12), width=5, height=8, wlabel="r", hlabel="h")
            w_p = (xy[0]+(width/2.0), xy[1])  #(8.5, 12)
            h_p = (xy[0], xy[1]+(height/2.0)) #(6, 16)

            plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
            plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

            mid_rwidth = (xy[0]+w_p[0])/2.0  #8.5+6 /2 = 7.25
            mid_rheight = (xy[0]+h_p[1])/2.0 #22 / 2 = 11.0

            textwobj = ax.text(mid_rwidth, xy[1]*1.015, '$'+wlabel+'$', fontsize=25)
            texthobj = ax.text(xy[0]*1.015, mid_rheight, '$'+hlabel+'$', fontsize=25)

            # Find out the pixel measurements of the text's bounding box
            renderer = FigureCanvasAgg(fig).get_renderer()
            wbbox = textwobj.get_window_extent(renderer)
            hbbox = texthobj.get_window_extent(renderer)

            # Find out what one horizontal and vertical unit is in pixel
            conversion_matrix = ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0))
            # Multiply the width in pixels by 1/width-conversion
            wwidth = (wbbox.bounds[2]*(1/conversion_matrix[1,0]))/2
            hwidth = (hbbox.bounds[2]*(1/conversion_matrix[1,0]))/2
            # Left shift it
            textwobj.set_position((mid_rwidth-wwidth, xy[1]*1.015))
            texthobj.set_position((xy[0]*1.015, mid_rheight+hwidth))

        else:
            #cross, label 0300
            ellipse = patches.Ellipse(xy, width, height, angle=0.0, fill=False, linewidth=3)

            w_p1 = (xy[0]+rwidth, xy[1])
            w_p2 = (xy[0]-rwidth, xy[1])
            h_p1 = (xy[0], xy[1]+rheight)
            h_p2 = (xy[0], xy[1]-rheight)

            plt.plot([xy[0],w_p[0]], [xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
            plt.plot([xy[0],h_p[0]], [xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

            mid_dwidth = (xy[0]+w_p[0])/2.0
            mid_dheight = (xy[0]+h_p[0])/2.0

            textwobj = ax.text(mid_dwidth, xy[1]*1.015, '$'+wlabel+'$', fontsize=25)
            texthobj = ax.text(mid_dheight, xy[1], "$"+hlabel+"$", fontsize=25)

            # Find out the pixel measurements of the text's bounding box
            renderer = FigureCanvasAgg(fig).get_renderer()
            bbox = textobj.get_window_extent(renderer)
            # Find out what one horizontal and vertical unit is in pixel
            conversion_matrix = ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0))
            # Multiply the width in pixels by 1/width-conversion
            width = (bbox.bounds[2]*(1/conversion_matrix[1,0]))/2
            # Left shift it
            textwobj.set_position((mid_dwidth-width, xy[1]*1.015))
            texthobj.set_position((mid_dheight-width, xy[1]))

        ax.add_patch(ellipse)
