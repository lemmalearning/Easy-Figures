import matplotlib
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
		# OR #
		#circ = f.addEllipse(xy=(7,10), label="r", r=10, fc='grey')

	# ELLIPSE #
	def ellipse(f):
		ell = f.addEllipse(xy=[7,10], r=(9,12), angle=20.0)
		ell.ellipseLabels(xlabel='x', ylabel='y', isRadius=False)
		#ell2 = f.addEllipse(xy=[-12,8], r=(4,8), angle=190.0, fc='yellow')
		#ell3 = f.addEllipse(xy=[10,-8], r=(8,3), angle=45.0, lw=5.0, fc='pink')
		#ell4 = f.addEllipse(xy=[-13,-7], r=(5,6), angle=270.0, fc='green', lw=1)

	# POLYGON #
	def polygon(f):
		"""
		poly = f.addPolygon(
			[
				[5.5, 4.5],
				[4.5, 5.1],
				[4.9, 6.3],
				[6.0, 6.3],
				[6.4, 5.1]
			],
			lw=3
		)
		"""
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


	# AXIS #
	def axis(f):
		axis = f.addAxis(hideAxis=False, grid=True, arrows=True, color='black', lw=1, minorGrid='red')
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

	# WEDGE #
	def wedge(f):
		#f.addWedge((0,0), r=5, theta1=60, theta2=90)

		f.addWedge((0,0), r=5, theta1=60, theta2=90, mplprops={'color':'orange', 'ec':'k'})
		f.addWedge((-2,0), r=3, theta1=120, theta2=190)
		f.addWedge((-2,0), r=8, theta1=270, theta2=360)

	# WRITE #
	def write(f):
		f.__draw_shapes__()
		s = f.__export__()
		f = open('images/test.svg', "w+")
		f.write(s)
		f.flush()
		f.close()

	# INIT #
	f = figures.Figures([[-7,7],[-12,12]], bgcolor='w')

	triangle(f)
	###function(f)
	###circle(f)
	###ellipse(f)
	###polygon(f)
	#point(f)
	#text(f)
	#arrow(f)
	#wedge = f.addWedge(xy=(1,1), radius=5, theta1=0, theta2=300, mplprops={'width':None})
	#wedge(f)
	#line = f.addLine([2,4], [6,8], lw=2, mplprops={'color':'r'})

	#matplotlib.lines.Line2D([0,0], [5,5])

	###axis(f)

	write(f)

if __name__ == "__main__":
	unit_test()
