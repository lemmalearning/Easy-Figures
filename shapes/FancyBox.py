import matplotlib.patches as patches
import matplotlib.transforms as mtransforms

class FancyBox:
	matplotlib_obj = None
	def __init__(self, ll_point, ur_point, fc, ec, boxstyle, mplprops, figure):
		#ll_point - lower left Point
		#ur_point - upper right Point
		"""
		Box style:
				class 			Name 			Attrs
				----------------------------------------
				Circle		|	circle		|	pad=0.3
				DArrow		|	darrow		|	pad=0.3
				LArrow		|	larrow		|	pad=0.3
				RArrow		|	rarrow		|	pad=0.3
				Round		|	round		|	pad=0.3,rounding_size=None
				Round4		|	round4		|	pad=0.3,rounding_size=None
				Roundtooth	|	roundtooth	|	pad=0.3,tooth_size=None
				Sawtooth	|	sawtooth	|	pad=0.3,tooth_size=None
				Square		|	square		|	pad=0.3
		"""
		self.figure = figure
		bb = mtransforms.Bbox([ll_point, ur_point])
		self.matplotlib_obj = patches.FancyBboxPatch(
								(bb.xmin, bb.ymin),
								abs(bb.width), abs(bb.height),
                            	boxstyle=boxstyle, fc=fc, ec=ec,
								**mplprops
							)
		self.patch = self.figure.ax.add_patch(self.matplotlib_obj)

	def __draw__(self, zorder=1):
		self.patch.set(zorder=zorder)
