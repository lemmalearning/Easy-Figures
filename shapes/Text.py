class Text:
	matplotlib_obj = None
	def __init__(self, xy, text, color, fontsize, offset, halignment, valignment, bbox, latex, pixel, mplprops, figure):
		if not isinstance(color, list):
			offset = [offset]
			color = [color]
			xy = [xy]
			text = [text]
			halignment = [halignment]
			valignment = [valignment]
			bbox = [bbox]
			latex = [latex]
			pixel = [pixel]
			self.matplotlib_obj = []

			self.xy = xy
			self.text = text
			self.color = color
			self.fontsize = fontsize
			self.halignment = halignment
			self.valignment = valignment
			self.bbox = bbox
			self.latex = latex
			self.figure = figure
			self.mplprops = mplprops
			self.pixel = pixel
			self.offset = offset


	def __draw__(self, zorder=1):
		for xy, text, color, offset, valignment, halignment, bbox, latex, pixel in zip(self.xy, self.text, self.color, self.offset, self.valignment, self.halignment, self.bbox, self.latex, self.pixel):
			if pixel:
				x=self.figure.px2unit(xy[0], 'x')+self.figure.px2unit(offset[0], 'x')
				y=self.figure.px2unit(xy[0], 'y')+self.figure.px2unit(offset[1], 'y')
			else:
				x=xy[0]+self.figure.px2unit(offset[0], 'x')
				y=xy[1]+self.figure.px2unit(offset[1], 'y')
			obj = self.figure.ax.text(x,y,
			                          "$" + text + "$" if latex else text, fontsize=self.fontsize,
			                          horizontalalignment=halignment, verticalalignment=valignment, bbox=bbox,
			                          color=color, zorder=zorder, clip_on=False, **self.mplprops
			                          )
			obj.set_clip_on(False)
			self.matplotlib_obj.append(obj)

