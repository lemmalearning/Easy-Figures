import figures, os, sys
import numpy as np


def unit_test():
	# TRIANGLE #
	def triangle(f):
		t = f.addTriangle(isSide=False, angle=np.pi/6, xy=[-3,6], rotation=0/np.pi, length=4)
		t.labelAngles([r'\alpha', r'\beta', r'\gamma'])
		t.labelOppositeSides(['A', 'B', 'C'])
		t.labelVertices(['a', 'b', 'c'])

	# FUNCTION #
	def function(f):
		func = lambda x: np.np.sin(x)
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
				[2, 3],
				[9, 3],
				[2, 10]
			],
			lw=3
		)
		poly.labelVertices(['a', 'd', 'e'])
		poly.labelAngles([r'\alpha',r'\delta', r'\epsilon'], arcs=['sq2uare', 2, 1])

	# REGULAR POLYGON #
	def regpoly(f):
		f.addRegularPolygon(xy=(-4,-3), numVertices=3, radius=7, mplprops={'ec':'k', 'color':'orange'})
		f.addRegularPolygon((3,0), 4, radius=3, orientation=np.pi/2, lw=1, mplprops={'color':'green'})
		f.addRegularPolygon((6,-6), 5, radius=3, lw=3, mplprops={'ls':'dashed'})

	# AXIS #
	def axis(f):
		axis = f.addAxis(hideAxis=False, minorGrid=True, arrows=True, color='black', lw=2)
		#axis.Ticks(xticks=5, yticks=5, xminorticks=2, yminorticks=2, fontsize=12, origin=False, top=True)
		axis.Ticks(ticks=False)

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
		#arrow = f.addArrow((0,0), (5, 5), color='r', lw=1)
		#farrow = f.addArrow((0,0), (5, 5), color='b', lw=1, arrowstyle='|-|', connectionstyle='arc')
		r=2
		bbox = f.addRectangle_rounded([-2, -4], [5, 6], ec='green', r=r)

		#bbox = f.addRectangle_rounded([-2, -4], [5, 6], fc='red', ec='green', r=0)
		axis = f.addAxis(hideAxis=False, grid=True, minorGrid=True, arrows=True, color='black', lw=2)
		axis.Ticks(ticks=1, minorticks=.5)


	def arc(f):
		axis = f.addAxis(hideAxis=False, minorGrid=True, arrows=True, color='black', lw=2)
		arc = f.addArc(xy=(0,0), width=5, height=5,lw=2, theta1=0.0, theta2=180.0)

	# WEDGE #
	def wedge(f):
		for x in range(0,8):
			 f.addWedge((0,0), r=10, theta1=32*x, theta2=(32*x)+32, mplprops={'color':'#a39c92', 'ec':'#f0feffff', 'lw':1})
		f.addWedge((0.2,-0.8), r=10, theta1=259, theta2=291, mplprops={'color':'orange', 'ec':'w', 'lw':1})
		f.addWedge((0,0), r=10, theta1=296, theta2=328, mplprops={'color':'#a39c92', 'ec':'w', 'lw':1})
		f.addWedge((0,0), r=10, theta1=328, theta2=360, mplprops={'color':'#a39c92', 'ec':'w', 'lw':1})

	# LINE #
	def line(f):
		axis = f.addAxis(hideAxis=False, grid=True, minorGrid=True, arrows=True, color='black', lw=2)
		axis.Ticks(ticks=4, yminorticks=2, xminorticks=4)
		f.addPolygon(([ 0, 0 ], [ 0, 5 ], [5, 0]), mplprops={'color':'red', 'ec':None})
		f.addLine([5,10], [5,5], lw=5, mplprops={})


	# BOX #
	def box(f):
		f.addBox((0,0.3), (0,500), xlabel='Time (s)', ylabel='Velocity (m/s)', title='Velocity vs Time')

	def zigzag(f):
		axis = f.addAxis(hideAxis=False, grid=True, minorGrid=True, arrows=True, color='black', lw=2)
		axis.Ticks(ticks=5, minorticks=2.5)
		points = [
			[0,0],
			[2,2],
			[1,3],
			[5,5]
		]
		lines = f.addZigzag(points, lw=2, color='b', mplprops={'ls':'dashed'})

	def asdf(f):
		alpha = pi/3
		r = 2
		W = 5
		fig = figures.Figures([[-W, W],[-W, W]], width=300, height=300)
		axis = fig.addAxis(hideAxis=False, grid=True, minorGrid=True, arrows=True, color='black', lw=2)
		axis.Ticks(ticks=2, minorticks=1)

		fig.addCircle(xy=[0,0], radius=r, lw=1)
		fig.addArc(xy=(0,0), width=2*r, height=2*r, lw=3, theta1=0.0, theta2=90.0)
		fig.addLine([-2, 2], [0, 2], lw=3)

	# WRITE #
	def write(f, a=""):
		f.__draw_shapes__()
		s = f.__export__()
		f = open('images/{}test.svg'.format(a), "w+")
		f.write(s.encode('ascii', 'ignore'))
		f.flush()
		f.close()


	def test(func, funcName, silent=False):
		import os
		#f = figures.Figures([[-10, 10],[-10, 10]], width=800, height=800)
		f = figures.Figures([[-10,10 ], [ -10,10 ]], padding=100, width=800, height=800, aspectRatio=1)
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
	elif 'silent' in sys.argv:
		for func in sys.argv[2:]:
			test(locals()[func], func, silent=True)
	else:
		for func in sys.argv[1:]:
			test(locals()[func], func)

if __name__ == "__main__":
	unit_test()
