import matplotlib.patches as patches

class FancyArrowPatch:
	def __init__(self, posA, posB, path, color, lw, arrowstyle, connectionstyle, mutation_scale, mplprops, figure):
		self.posA = posA
		self.posB = posB
		self.path = path
		self.lw = lw
		self.arrowstyle = arrowstyle
		self.connectionstyle = connectionstyle
		self.mutation_scale = mutation_scale
		self.mplprops = mplprops
		self.figure = figure
		self.color = color

		fancyArrow = patches.FancyArrowPatch(posA, posB, path, arrowstyle, connectionstyle, color=self.color, mutation_scale = self.mutation_scale, lw=lw, **self.mplprops)
		self.matplotlib_obj = fancyArrow
		self.patch = self.figure.ax.add_patch(self.matplotlib_obj)

	def __draw__(self, zorder=1):
		self.patch.set(zorder=zorder)

	def serialize(self):
		# NOTE: We will not try to serialize this
		pass
