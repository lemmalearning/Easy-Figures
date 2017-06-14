import shapes
import StringIO

class Figures():
	def __init__(self):
		self.fig, self.ax = plt.subplots()

		# Modify the plot view to scale, remove axis, and center our shape
		self.ax.autoscale_view()
		self.plt.axis('off')
		self.plt.axis('scaled')

		# Display or Save to file
		#plt.savefig('/Users/ajpersinger/test.svg')
		self.plt.show()

	def __export__():
		export_str = StringIO.StringIO()
		fig.savefig(export_str, format='svg')
		export_str.seek(0)  # rewind the data
		return export_str.buf  # this is svg data



	def addPolygon(vertices):
		polygon = shapes.Triangle(vertices, self.fig, self.ax)
		return polygon
