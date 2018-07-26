import matplotlib.patches as patches
import math

class Arc:
	def __init__(self, xy, width, height, fc, ec, lw, angle, theta1, theta2, mplprops, figure):
		self.xy = xy
		self.width = width
		self.height = height
		self.angle = angle
		self.theta1 = theta1
		self.theta2 = theta2
		self.lw = lw
		self.mplprops = mplprops
		self.figure = figure
		arc = patches.Arc(xy, width, height, angle, theta1, theta2, fc=fc, ec=ec, lw=lw, **self.mplprops)
		self.matplotlib_obj = arc
		self.patch = self.figure.ax.add_patch(self.matplotlib_obj)

	def __draw__(self, zorder=1):
		self.patch.set(zorder=zorder)

	def serialize(self):
		return {
			"type": "Arc",
			"center": [ float(x) for x in self.xy ],
			"radius": self.width / 2.0, #[ self.width / 2.0, self.height / 2.0 ],
			"theta1": float(self.theta1) * (math.pi / 180.0),
			"theta2": float(self.theta2) * (math.pi / 180.0),
			"lineWidth": self.figure.raw2px(self.matplotlib_obj.get_linewidth())
			# TODO:


		}
