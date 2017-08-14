import figures, os, sys
import numpy as np
from sympy import sin

def unit_test():
	# TRIANGLE #
	def triangle(f):
		t = f.addTriangle(isSide=False, angle=np.pi/6, xy=[-3,6], rotation=0/np.pi, length=4)
		t.labelAngles([r'\alpha', r'\beta', r'\gamma'])
		t.labelOppositeSides(['A', 'B', 'C'])
		t.labelVertices(['a', 'b', 'c'])

	# FUNCTION #
	def function(f):
		func = lambda x: np.sin(x)
		func2 = lambda x: x**2

		f.addFunction(
			func,
			[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]],
			color="green",
			lw=2
		)

		f.addFunction(
			func2,
			[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]],
			color="orange",
			lw=2
		)

	# CIRCLE #
	def circle(f):
		circ = f.addCircle(xy=(7,10), label="r", radius=10, fc='#f4ab7a', lw=5)

	# ELLIPSE #
	def ellipse(f):
		ell = f.addEllipse(xy=[7,10], r=(9,12), angle=20.0)
		ell.ellipseLabels(xlabel='x', ylabel='y', isRadius=False)
		ell2 = f.addEllipse(xy=[-12,8], r=(4,8), angle=190.0, fc='yellow')
		ell3 = f.addEllipse(xy=[10,-8], r=(8,3), angle=45.0, lw=5.0, fc='pink')
		ell4 = f.addEllipse(xy=[-13,-7], r=(5,6), angle=270.0, fc='green', lw=1)

	# POLYGON #
	def polygon(f):
		poly = f.addPolygon(
			[
				[8.5, 2.5],
				[1.5, 6.1],
				[7.2, 12.3],
				[12.0, 12.3],
				[15.4, 6.1]
			],
			lw=3
		)
		poly.labelVertices(['a', 'b', 'c', 'd', 'e'])
		poly.labelAngles([r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon'])

	# REGULAR POLYGON #
	def regpoly(f):
		f.addRegularPolygon(xy=(-4,-3), numVertices=3, radius=7, mplprops={'ec':'k', 'color':'orange'})
		f.addRegularPolygon((3,0), 4, radius=3, orientation=np.pi/2, lw=1, mplprops={'color':'green'})
		f.addRegularPolygon((6,-6), 5, radius=3, lw=3, mplprops={'ls':'dashed'})

	# AXIS #
	def axis(f):
		axis = f.addAxis(arrows=True, grid=True, minorGrid='green', xlabel='x', ylabel='y')
		axis.Ticks(fontsize=12, origin=False, top=True, xticks=5, yticks=6, xminorticks=2, yminorticks=1)

	# POINT #
	def point(f):
		f.addPoint((2,3), texts='A', color='k', pointsize=4)
		f.addPoint([(2,-2), (4,-4), (6,-6)], texts=['C','D','E'], color=['red', 'blue', 'green'], pointsize=7)

	# TEXT #
	def text(f):
		f.addText((-4,-2), "With\ cool\ effects", bbox=dict(boxstyle="rarrow,pad=0.3", ec="b", lw=2), color='blue')
		f.addText((2,4), r"Rendered\ as\  TeX\ ->\ \int_{a}^{b} x^2 dx")
		f.addText((0,1), "Or plain text!", latex=False, color='green', fontsize=18)

	# ARROW #
	def arrow(f):
		"""
		axis = f.addAxis(arrows=True, grid=True, minorGrid='green', xlabel='x', ylabel='y')
		axis.Ticks(fontsize=12, origin=False, top=True, xticks=5, yticks=6, xminorticks=2, yminorticks=1)
		f.addArrow([0,0], [1,1], color='k', headWidth=0.05, width=0.005, lw=1)
		"""
		axis = f.addAxis(arrows=True, grid=True, minorGrid='green', xlabel='x', ylabel='y')
		f.addArrow([4,2], [8,60])
		"""
		f2.addArrow([0,0.2], [1,0.2+1], color='k', headWidth=0.05, width=0.005, lw=1)
		f2.addArrow([1.08,1.15], [1.08-1,1.15-1], color='k', headWidth=0.05, width=0.005, lw=1)

		f2.addArrow((-0.4,0.45), (-0.4+0.35, 0.45-0.25), color='k', lw=0.5,  arrowstyle='->', connectionstyle='arc3, rad=2')
		"""
	# WEDGE #
	def wedge(f):
		for x in range(0,8):
			 f.addWedge((0,0), r=10, theta1=32*x, theta2=(32*x)+32, mplprops={'color':'#a39c92', 'ec':'#f0feffff', 'lw':1})
		f.addWedge((0.2,-0.8), r=10, theta1=259, theta2=291, mplprops={'color':'orange', 'ec':'w', 'lw':1})
		f.addWedge((0,0), r=10, theta1=296, theta2=328, mplprops={'color':'#a39c92', 'ec':'w', 'lw':1})
		f.addWedge((0,0), r=10, theta1=328, theta2=360, mplprops={'color':'#a39c92', 'ec':'w', 'lw':1})

	# LINE #
	def line(f):
		f.addLine([5,10], [5,5], mplprops={'ls':'dotted'})


	# BOX #
	def box(f):
		f.addBox((0,0.3), (0,500), xlabel='Time (s)', ylabel='Velocity (m/s)', title='Velocity vs Time')

	# WRITE #
	def write(f, a=""):
		f.__draw_shapes__()
		s = f.__export__()
		f = open('images/{}test.svg'.format(a), "w+")
		f.write(s)
		f.flush()
		f.close()


	def test(func, funcName, silent=False):
		import os
		f = figures.Figures([[0, 10],[0, 100]], width=800, height=800)
		func(f)
		write(f, a=funcName)
		if not silent: os.system('open {}'.format('images/{}test.svg'.format(funcName)))

	list_funs = [
		triangle,
		function,
		circle,
		ellipse,
		polygon,
		regpoly,
		point,
		text,
		arrow,
		wedge,
		line,
		box,
		axis,
	]

	if sys.argv[1] == 'all' or len(sys.argv) == 1:
		for func in list_funs:
			test(func, func.__name__)
	elif sys.argv[1] == 'silent':
		for func in sys.argv[2:]:
			test(locals()[func], func, silent=True)
	else:
		for func in sys.argv[1:]:
			test(locals()[func], func)

if __name__ == "__main__":
	unit_test()
