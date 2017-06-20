import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Ellipse:
	def __init__(self, fig, ax, xy=(0,0), r=(1,1), fc=None, ec=None, angle=0.0):
		self.r = r
		self.angle=angle
		self.xy = xy
		semimajor = r[0]
		semiminor = r[1]
		self.fig = fig
		self.ax = ax
		semimajor = semimajor*2.0
		semiminor = semiminor*2.0

		ellipse = patches.Ellipse(xy, semimajor, semiminor, linewidth=3, fc=fc, ec=ec, angle=angle)

		ax.add_patch(ellipse)

	def ellipseLabels(self, xlabel=None, ylabel=None, isRadius=True):
		semimajor = self.r[0]
		semiminor = self.r[1]
		if isRadius:
			w_p = [self.xy[0]+semimajor, self.xy[1]]
			h_p = [self.xy[0], self.xy[1]+semiminor]

			p1 = w_p[0] - self.xy[0]
			q1 = w_p[1] - self.xy[1]

			p2 = p1*np.cos(self.angle) - q1*np.sin(self.angle)
			q2 = p1*np.sin(self.angle) + q1*np.cos(self.angle)

			w_p[0] = p2 + self.xy[0]
			w_p[1] = q2 + self.xy[1]

			plt.plot([self.xy[0],w_p[0]], [self.xy[1],w_p[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([self.xy[0],h_p[0]], [self.xy[1],h_p[1]], linewidth=2, ls='dashed', color='black')

			semimajor/=2
			semiminor/=2

			midMajor = (self.xy[0]+w_p[0])/2.0
			midMinor = (self.xy[1]+h_p[1])/2.0

			textxobj = self.ax.text(midMajor, self.xy[1]*1.025, '$'+xlabel+'$', fontsize=25)
			textyobj = self.ax.text(self.xy[0]*1.025, midMinor, '$'+ylabel+'$', fontsize=25)

			# Find out the pixel measurements of the text's bounding box
			renderer = FigureCanvasAgg(self.fig).get_renderer()
			xbbox = textxobj.get_window_extent(renderer)
			ybbox = textyobj.get_window_extent(renderer)
			# Find out what one horizontal and vertical unit is in pixel
			conversionMatrix = self.ax.transData.transform([(0,1),(1,0)])-self.ax.transData.transform((0,0))
			# Multiply the width in pixels by 1/width-conversion
			xwidth = (xbbox.bounds[2]*(1/conversionMatrix[1,0]))/2
			yheight = (25*(1/conversionMatrix[1,0]))/2
			# Left shift it
			textxobj.set_position((midMajor-xwidth, (self.xy[1]+0.2)))
			textyobj.set_position(((self.xy[0]+0.2), midMinor-yheight))

		else:
			w_p1 = (self.xy[0]+semimajor, self.xy[1])
			w_p2 = (self.xy[0]-semimajor, self.xy[1])
			h_p1 = (self.xy[0], self.xy[1]+semiminor)
			h_p2 = (self.xy[0], self.xy[1]-semiminor)

			plt.plot([w_p2[0],w_p1[0]], [self.xy[1], self.xy[1]], linewidth=2, ls='dashed', color='black')
			plt.plot([self.xy[0],self.xy[0]], [h_p1[1], h_p2[1]], linewidth=2, ls='dashed', color='black')

			midMajor = (self.xy[0]+w_p1[0])/2.0
			midMinor = (self.xy[1]+h_p1[1])/2.0

			textxobj = self.ax.text(midMajor, self.xy[1]*1.025, '$'+xlabel+'$', fontsize=25)
			textyobj = self.ax.text(self.xy[0]*1.025, midMinor, '$'+ylabel+'$', fontsize=25)

			# Find out the pixel measurements of the text's bounding box
			renderer = FigureCanvasAgg(self.fig).get_renderer()
			xbbox = textxobj.get_window_extent(renderer)
			ybbox = textyobj.get_window_extent(renderer)
			# Find out what one horizontal and vertical unit is in pixel
			conversionMatrix = self.ax.transData.transform([(0,1),(1,0)])-self.ax.transData.transform((0,0))
			# Multiply the width in pixels by 1/width-conversion
			xwidth = (xbbox.bounds[2]*(1/conversionMatrix[1,0]))/2
			yheight = (25*(1/conversionMatrix[1,0]))/2
			# Left shift it
			textxobj.set_position((midMajor-xwidth, (self.xy[1]+0.2)))
			textyobj.set_position((self.xy[0]+0.2, midMinor-yheight))
