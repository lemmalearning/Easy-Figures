import figures
import numpy as np
from random import randint
from sympy import sin

def randint_except(a, b, c):
	if not isinstance(c, list) and not isinstance(c, tuple):
		return randint_except(a, b, [c])

	if not c:
		return randint(a, b)

	x = c[0];
	while x in c:
		x = randint(a, b)

	return x

def unit_test():
	# TRIANGLE #
	def triangle(f):
		t = f.addTriangle(isSide=False, angle=np.pi/6, xy=[-3,6], rotation=0/np.pi, length=3)
		t.labelAngles([r'\alpha', r'\beta', r'\gamma'])
		t.labelOppositeSides(['A', 'B', 'C'])
		t.labelVertices(['a', 'b', 'c'])

	# FUNCTION #
	def function(f):
		func = lambda x: np.sin(x)
		f.addFunction(
			func,
			[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]],
			color="blue",
			lw=10
			#mplprops={'lw':10}
		)

	# CIRCLE #
	def circle(f):
		circ = f.addCircle(xy=(7,10), label="r", radius=10, fc='grey', lw=5)
		# OR #
		#circ = f.addEllipse(xy=(7,10), label="r", r=10, fc='grey')

	# ELLIPSE #
	def ellipse(f):
		ell = f.addEllipse(xy=[9,12], r=(9,12), angle=30.0, fc='red', ec='w', lw=10)
		ell.ellipseLabels(xlabel='x', ylabel='y', isRadius=False)
		ell2 = f.addEllipse(xy=[-12,8], r=(4,8), angle=190.0, fc='yellow')
		ell3 = f.addEllipse(xy=[10,-8], r=(8,3), angle=45.0, lw=5.0, fc='pink')
		ell4 = f.addEllipse(xy=[-13,-7], r=(5,6), angle=270.0, fc='green', lw=1)

	# POLYGON #
	def polygon(f):
		poly = f.addPolygon(
			[
				[5.5, 4.5],
				[4.5, 5.1],
				[4.9, 6.3],
				[6.0, 6.3],
				[6.4, 5.1]
			],
			lw=10
		)
		poly.labelVertices(['a', 'b', 'c', 'd', 'e'])
		poly.labelOppositeSides(['A', 'B', 'C', 'D', 'E'])
		poly.labelAngles([r'\alpha', r'\beta', r'\gamma', r'\delta', r'\epsilon'])


	# AXIS #
	def axis(f):
		axis = f.addAxis(hideAxis=False, grid=True, arrows=True, color='black', lw=4, minorGrid='red')
		axis.Ticks(tickLabelInterval=2, tickInterval=1, fontsize=12, origin=False, top=True)

	# POINT #
	def point(f):
		#f.addPoint([(2,3), (4, 3), (6,3)], ['A', 'B', 'C'], color=['red', 'blue', 'green'], pointsize=14)
		f.addPoint((4,3), color='black')

	# TEXT #
	def text(f):
		f.addText((-5,-4), "With\ cool\ effects", bbox=dict(boxstyle="rarrow,pad=0.3", fc="cyan", ec="b", lw=2), color='red')
		f.addText((-0,4), r"Rendered\ as\  TeX\ ->\ \int_{a}^{b} x^2 dx", bbox=dict(boxstyle="circle,pad=0.3", fc="orange", ec="yellow", lw=2), color='blue')
		f.addText((-5,9), "Or plain text!", latex=False, color='green', fontsize=20)

	# ARROW #
	def arrow(f):
		dxdy1 = (randint_except(-1,8, 0), randint_except(-4,2, 0))
		dxdy2 = (randint_except(-8,2, 0), randint_except(-1, 5, 0))

		f.addArrow((0,0), dxdy1, color='blue', width=0.035, lw=10)
		f.addArrow((0,0), dxdy2, color='blue', width=0.035)

	# WRITE #
	def write(f):
		f.__draw_shapes__()
		s = f.__export__()
		f = open('images/test.svg', "w+")
		f.write(s)
		f.flush()
		f.close()

	# INIT #
	f = figures.Figures([[-10,10],[-10, 10]])

	triangle(f)
	function(f)
	circle(f)
	ellipse(f)
	polygon(f)
	axis(f)
	point(f)
	text(f)
	arrow(f)
	write(f)

if __name__ == "__main__":
	unit_test()
