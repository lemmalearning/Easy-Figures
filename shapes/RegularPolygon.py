import matplotlib.patches as patches


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

    def __draw__(self, zorder=1):
        p = self.figure.ax.add_patch(self.matplotlib_obj)
        p.set(zorder=zorder)
