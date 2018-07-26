import matplotlib.patches as patches
import numpy as np
from .serial_utils import *

class RegularPolygon:
	def __init__(self, xy, numVertices, radius, fill, fc, ec, lw, orientation, mplprops, figure):
		self.xy = xy
		self.numVertices = numVertices
		self.radius = radius
		self.fill = fill
		self.orientation = orientation
		self.lw = lw
		self.mplprops = mplprops
		self.figure = figure

		# Define the polygon
		polygon = patches.RegularPolygon(xy, numVertices, radius, fc=fc, ec=ec, fill=False, lw=lw, **self.mplprops)
		self.matplotlib_obj = polygon
		self.patch = self.figure.ax.add_patch(self.matplotlib_obj)

	def __draw__(self, zorder=1):
		self.patch.set(zorder=zorder)

	def serialize(self):		
		verts = self.radius * self.matplotlib_obj.get_path().vertices
		for i in range(0, verts.shape[0]):
			verts[i, :] += np.array(self.xy)
		
		return {
			"type": "Polygon",
			# TODO: This may need to be transformed by the orientation?
			"points": [ [ verts.item(i, 0), verts.item(i, 1) ]  for i in range(0, verts.shape[0]) ],
			"edgeColor": convert_color(self.matplotlib_obj.get_edgecolor()),
			"faceColor": convert_color(self.matplotlib_obj.get_facecolor()),
			"lineWidth": self.figure.raw2px(self.matplotlib_obj.get_linewidth()),
			"lineStyle": self.matplotlib_obj.get_linestyle()
		}
