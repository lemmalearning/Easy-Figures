import matplotlib
import figures
import numpy as np
from random import randint
from sympy import sin
import matplotlib.pyplot as plt

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
		f.addRegularPolygon((7,0), 4, radius=3, orientation=np.pi/2, mplprops={'color':'green'})
		f.addRegularPolygon((6,-6), 5, radius=3, mplprops={'ls':'dashed'})

	# AXIS #
	def axis(f):
		#plt.axis('equal')

		axis = f.addAxis(hideAxis=False, grid=True, arrows=True, color='black', lw=2, minorGrid='red', xlabel='hi', ylabel='bye')
		#axis.Ticks(tickLabelInterval=1, tickInterval=0.5, fontsize=12, origin=False, top=True)
		axis.Ticks(xtickLabelInterval=25, ytickLabelInterval=10, tickInterval=5, fontsize=12, origin=False, top=True)


		"""
		t = np.arange(0.0, 1.0 + 0.01, 0.01)

		f.plot(t, s, '-', lw=2)

		f.grid(True)

		f.axes().set_aspect('equal', 'datalim')


		plt.show()
		"""
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
		dxdy1 = (randint_except(-1,8, 0), randint_except(-4,2, 0))
		dxdy2 = (randint_except(-8,2, 0), randint_except(-1, 5, 0))

		f.addArrow((0,0), dxdy1, color='blue', width=0.035, lw=10)
		f.addArrow((0,0), dxdy2, color='blue', width=0.035)
		"""
		f.addFancyArrow(posA=(-8,-7), posB=(-4, 3), lw=1, arrowstyle='|-|', connectionstyle='bar', mplprops={'mutation_scale':3})
		f.addFancyArrow(posA=(8,-8), posB=(-8, 10), arrowstyle='<->', connectionstyle='bar', mplprops={'mutation_scale':10})
		f.addFancyArrow(posA=(-8,-8), posB=(8, -9), lw=1, arrowstyle='<|-|>', connectionstyle='arc', mplprops={'mutation_scale':10, 'ls':'dotted'})
		f.addFancyArrow(posA=(10,8), posB=(4, 4), arrowstyle='fancy', connectionstyle='bar', mplprops={'mutation_scale':15, 'color':'black'})
		f.addFancyArrow(posA=(8,8), posB=(3, 4), lw=1, arrowstyle='fancy', connectionstyle='bar', mplprops={'mutation_scale':15, 'color':'white', 'ec':'black'})

	# WEDGE #
	def wedge(f):
		f.addWedge((0,0), r=10, theta1=0, theta2=32, mplprops={'color':'#a39c92', 'lw':1, 'ec':'w'})
		f.addWedge((0,0), r=10, theta1=32, theta2=64, mplprops={'color':'#d3c7b6', 'lw':1, 'ec':'w'})
		f.addWedge((0,0), r=10, theta1=64, theta2=96, mplprops={'color':'#a39c92', 'lw':1, 'ec':'w'})
 		f.addWedge((0,0), r=10, theta1=96, theta2=128, mplprops={'color':'#d3c7b6', 'lw':1, 'ec':'w'})
 		f.addWedge((0,0), r=10, theta1=128, theta2=160, mplprops={'color':'#a39c92','lw':1, 'ec':'w'})
		f.addWedge((0,0), r=10, theta1=160, theta2=192, mplprops={'color':'#d3c7b6', 'lw':1, 'ec':'w'})
		f.addWedge((0,0), r=10, theta1=192, theta2=224, mplprops={'color':'#a39c92', 'lw':1, 'ec':'w'})
		f.addWedge((0,0), r=10, theta1=224, theta2=256, mplprops={'color':'#d3c7b6', 'lw':1, 'ec':'w'})
		f.addWedge((0.2,-0.8), r=10, theta1=259, theta2=360, width=2, mplprops={'color':'orange', 'lw':1, 'ec':'w'})
		f.addWedge((0.2,-0.8), r=7, theta1=296, theta2=360, width=1, mplprops={'color':'red', 'lw':1, 'ec':'w'})
		f.addWedge((0.2,-0.8), r=5, theta1=328, theta2=360, width=1, mplprops={'color':'green', 'lw':1, 'ec':'w'})

	# LINE #
	def line(f):
		f.addLine([2,4], [6,8], lw=2, mplprops={'color':'r'})
		#f.addLine([0.02,0.02], [0.06,0.05], lw=2, mplprops={'color':'r'})


	# WRITE #
	def write(f):
		f.__draw_shapes__()
		s = f.__export__()
		f = open('images/test.svg', "w+")
		f.write(s)
		f.flush()
		f.close()

	# INIT #
	#f = figures.Figures([[-1.8,1.8],[-1.8,1.4]], height='auto', bgcolor='w')
	#f = figures.Figures([[-0.06,0.06],[-0.06, 0.06]], height='auto', bgcolor='w')
	f = figures.Figures([[-30,100],[-60,100]], height=400, bgcolor='w')

	#triangle(f)
	#function(f)
	#circle(f)
	#ellipse(f)
	#polygon(f)
	#regpoly(f)
	#point(f)
	#text(f)
	#arrow(f)
	#wedge(f)
	line(f)
	axis(f)

	write(f)

if __name__ == "__main__":
	unit_test()
