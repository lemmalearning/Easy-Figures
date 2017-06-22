import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Ellipse:
	def __init__(self, fig, ax, xy=[0,0], r=(1,1), fc=None, ec='none', angle=0.0, lw=2):
		self.r = r
		self.angle=angle
		self.lw=lw
		self.xy = xy
		semimajor = r[0]
		semiminor = r[1]
		self.fig = fig
		self.ax = ax
		semimajor = semimajor*2.0
		semiminor = semiminor*2.0

		ellipse = patches.Ellipse(xy, semimajor, semiminor, linewidth=3, fc=fc, ec=ec, angle=angle, lw=lw)
		self.matplotlib_obj = ellipse

	def ellipseLabels(self, xlabel=None, ylabel=None, isRadius=True):
		semimajor = self.r[0]
		semiminor = self.r[1]

		if isRadius:
			temp_x = self.xy[0]
			temp_y = self.xy[1]

			self.xy[0]-=self.xy[0]
			self.xy[1]-=self.xy[1]

			w_p = [self.xy[0]+semimajor, self.xy[1]]
			h_p = [self.xy[0], self.xy[1]+semiminor]

			p = (w_p[0]*np.cos(self.angle*(np.pi/180))) - (w_p[1]*np.sin(self.angle*(np.pi/180)))
			q = (w_p[1]*np.cos(self.angle*(np.pi/180))) + (w_p[0]*np.sin(self.angle*(np.pi/180)))

			r = (h_p[0]*np.cos(self.angle*(np.pi/180))) - (h_p[1]*np.sin(self.angle*(np.pi/180)))
			s = (h_p[1]*np.cos(self.angle*(np.pi/180))) + (h_p[0]*np.sin(self.angle*(np.pi/180)))

			plt.plot([self.xy[0]+temp_x,p+temp_x], [self.xy[1]+temp_y,q+temp_y], linewidth=2, ls='dashed', color='black')
			plt.plot([self.xy[0]+temp_x,r+temp_x], [self.xy[1]+temp_y,s+temp_y], linewidth=2, ls='dashed', color='black')

			self.xy[0] = temp_x + self.xy[0]
			self.xy[1] = temp_y + self.xy[1]

			semimajor/=2
			semiminor/=2

			midMajor = (self.xy[0]+(p+temp_x))/2.0
			midMinor = (self.xy[1]+(s+temp_y))/2.0

			textzobj = self.ax.text(midMajor, ((self.xy[1]+q+temp_y)/2.0)*1.15, '$'+xlabel+'$', fontsize=25, usetex=True)
			textqobj = self.ax.text(((self.xy[0]+r+temp_x)/2.0)*1.15, midMinor, '$'+ylabel+'$', fontsize=25, usetex=True)

			"""
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
			"""
		else:
			temp_x = self.xy[0]
			temp_y = self.xy[1]

			self.xy[0]-=self.xy[0]
			self.xy[1]-=self.xy[1]

			w_p1 = (self.xy[0]+semimajor, self.xy[1])
			w_p2 = (self.xy[0]-semimajor, self.xy[1])
			h_p1 = (self.xy[0], self.xy[1]+semiminor)
			h_p2 = (self.xy[0], self.xy[1]-semiminor)

			p = (w_p1[0]*np.cos(self.angle*(np.pi/180))) - (w_p1[1]*np.sin(self.angle*(np.pi/180)))
			q = (w_p1[1]*np.cos(self.angle*(np.pi/180))) + (w_p1[0]*np.sin(self.angle*(np.pi/180)))

			r = (h_p1[0]*np.cos(self.angle*(np.pi/180))) - (h_p1[1]*np.sin(self.angle*(np.pi/180)))
			s = (h_p1[1]*np.cos(self.angle*(np.pi/180))) + (h_p1[0]*np.sin(self.angle*(np.pi/180)))

			t = (w_p2[0]*np.cos(self.angle*(np.pi/180))) - (w_p2[1]*np.sin(self.angle*(np.pi/180)))
			u = (w_p2[1]*np.cos(self.angle*(np.pi/180))) + (w_p2[0]*np.sin(self.angle*(np.pi/180)))

			v = (h_p2[0]*np.cos(self.angle*(np.pi/180))) - (h_p2[1]*np.sin(self.angle*(np.pi/180)))
			w = (h_p2[1]*np.cos(self.angle*(np.pi/180))) + (h_p2[0]*np.sin(self.angle*(np.pi/180)))

			plt.plot([p+temp_x, t+temp_x], [q+temp_y, u+temp_y], lw=2, ls='dashed', color='black')
			plt.plot([r+temp_x, v+temp_x], [s+temp_y, w+temp_y], lw=2, ls='dashed', color='black')

			self.xy[0] = temp_x + self.xy[0]
			self.xy[1] = temp_y + self.xy[1]

			semimajor/=2
			semiminor/=2

			midMajor = (self.xy[0]+(p+temp_x))/2.0
			midMinor = (self.xy[1]+(s+temp_y))/2.0

			textzobj = self.ax.text(midMajor, ((self.xy[1]+q+temp_y)/2.0)*1.15, '$'+xlabel+'$', fontsize=25, usetex=True)
			textqobj = self.ax.text(((self.xy[0]+r+temp_x)/2.0)*1.15, midMinor, '$'+ylabel+'$', fontsize=25, usetex=True)


			"""
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
			"""

	def __draw__(self, zorder=1):
		e = self.ax.add_patch(self.matplotlib_obj)
		e.set(zorder=zorder)
