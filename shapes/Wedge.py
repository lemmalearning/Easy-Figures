import matplotlib.patches as patches
import math

class Wedge:
	def __init__(self, xy, r, theta1, theta2, fc, ec, width, lw, mplprops, figure):
		self.xy = xy
		self.r = r
		self.theta1 = theta1
		self.theta2 = theta2
		self.mplprops = mplprops
		self.figure = figure
		self.width = width
		self.maple = "12"

		wedge = patches.Wedge(xy, r, theta1, theta2, width, fc=fc, ec=ec, lw=lw, **self.mplprops)
		self.matplotlib_obj = wedge
		self.patch = self.figure.ax.add_patch(self.matplotlib_obj)

	def __draw__(self, zorder=1):
		self.patch.set(zorder=zorder)
	
	def serialize(self):
		def convert_color(c):
			return "rgba(" + ", ".join([ str(int(255*x)) for x in c[0:3] ]) + ", " + str(c[-1]) + ")"
		
		return {
			"type": "Wedge",
			"theta1": self.theta1 * (math.pi / 180.0),
			"theta2": self.theta2 * (math.pi / 180.0),
			"radius": self.r,
			"center": self.xy,
			"edgeColor": convert_color(self.matplotlib_obj.get_edgecolor()),
			"faceColor": convert_color(self.matplotlib_obj.get_facecolor()),
			"lineWidth": self.figure.raw2px(self.matplotlib_obj.get_linewidth())
		}
