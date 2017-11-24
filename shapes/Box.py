import matplotlib.pyplot as plt

class Box:
	matplotlib_obj = None
	def __init__(self, xlabel, ylabel, title, lw, fontsize, mplprops, figure):
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.title 		= title
		self.lw	        = lw
		self.mplprops   = mplprops
		self.fontsize = fontsize

	def __draw__(self, zorder=None):
		plt.axis('on')
		plt.axis([self.figure.xyrange[0][0], self.figure.xyrange[0][1], self.figure.xyrange[1][0], self.figure.xyrange[1][1]])
		plt.tick_params(labelsize=self.fontsize/2.0)
		plt.xlabel(self.xlabel, fontsize=self.fontsize)
		plt.ylabel(self.ylabel, fontsize=self.fontsize)
		plt.title(self.title, fontsize=self.fontsize)


	def serialize(self):
		# TODO: These are just modifiers on the axes?
		pass
