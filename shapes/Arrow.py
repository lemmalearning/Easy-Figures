import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Arrow:
	matplotlib_obj = None
	def __init__(self, start, end, color, headWidth, headLength, lw, mplprops, clip, add, figure):
		# x0,y0 start
		# x1,y1 end
		# xt,yt headlength point
		# d distance
		# dt headlength
		# k slope
		# l -1/k
		# l0 point 1
		# l1 point 2
		# Everything until otherwise mentioned is in pixels
		self.figure=figure
		if isinstance(start, list) or isinstance(start, tuple):
			start = np.matrix(start)
		if isinstance(end, list) or isinstance(end, tuple):
			end = np.matrix(end)

		start = self.figure.unit2px_c(start)
		end = self.figure.unit2px_c(end)
		v = end-start
		d = np.linalg.norm(v)
		head_len = self.figure.head_len
		head_width = self.figure.head_width
		t = head_len/d
		p_t = t*start + (1-t)*end
		v_norm = math.sqrt(v[0,0]**2+v[0,1]**2)
		l_1 = p_t + np.matrix([-v[0, 1], +v[0, 0]])/v_norm*head_width
		l_2 = p_t + np.matrix([+v[0, 1], -v[0, 0]])/v_norm*head_width
		p_t0 = (t-0.01)*start + (1.01-t)*end # One pixel into the triangle to avoid any pixel breaks
		self.head = self.figure.addPolygon([self.figure.px2unit_c(l_1).tolist()[0], self.figure.px2unit_c(end).tolist()[0], self.figure.px2unit_c(l_2).tolist()[0]], lw=0, fc=color, add=add, clip=clip)
		self.line = self.figure.addLine(self.figure.px2unit_c(start).tolist()[0], self.figure.px2unit_c(p_t0).tolist()[0], lw=lw, color=color, add=add, clip=clip)

	def __draw__(self, zorder=1):
		self.line.__draw__(zorder=zorder)
		self.head.__draw__(zorder=zorder)
