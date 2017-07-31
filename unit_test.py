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
		axis = f.addAxis(hideAxis=False, grid=True, arrows=True, color='black', lw=2, minorGrid='red')
		#axis.Ticks(ticks=2, tickInterval=3, fontsize=12, origin=False, top=True)
		axis.Ticks(xticks=1, yticks=1, tickInterval=1, fontsize=12, origin=False, top=True)

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
		#f.addFancyArrow(posA=(-8,-7), posB=(-4, 3), lw=1, arrowstyle='|-|', connectionstyle='bar', mplprops={'mutation_scale':3})
		#f.addFancyArrow(posA=(8,-8), posB=(80, 10), arrowstyle='<->', connectionstyle='bar', mplprops={'mutation_scale':10})
		#f.addFancyArrow(posA=(-8,-8), posB=(8, -9), lw=1, arrowstyle='<|-|>', connectionstyle='arc', mplprops={'mutation_scale':10, 'ls':'dotted'})
		#f.addFancyArrow(posA=(10,8), posB=(4, 4), arrowstyle='fancy', connectionstyle='bar', mplprops={'color':'black'})

		#f.addArrow((10,3), (10,8), lw=2, arrowstyle='<->', connectionstyle='bar', mplprops={'color':'red'})
		#f.addArrow((10,3), (-5,0), lw=2, arrowstyle='<->', connectionstyle='bar', mplprops={'color':'red'})

		#f.addArrow((10,3), (5+2,3+2), lw=2, arrowstyle='<->', connectionstyle='bar', mplprops={'color':'red'})
		#f.addArrow((-10,3), (-5,3), lw=2, arrowstyle='<->', connectionstyle='bar', mplprops={'color':'red'})

		#f.addArrow((0,0), (13, 13), lw=3, arrowstyle='fancy', connectionstyle='bar', mplprops={'color':'red'})
		#f.addArrow((0,0), (10, 10), lw=2, arrowstyle='simple', mplprops={'color':'red'})

		#f.addArrow([-0.06,0.06], [-0.06+1,0.06+1], color='k', headWidth=0.05, width=0.005, lw=1)
		#f.addArrow((-0.06,0.06), (1,1), color='red', headWidth=0.05, width=0.005, lw=1)
		#f.addArrow((1,1), (6,6), color='k', headWidth=0.05, width=0.005, lw=1)

		f.addArrow([0,0], [1,1], color='k', headWidth=0.05, width=0.005, lw=1)
		f.addArrow([-0.06,0.06], [-0.06+1,0.06+1], color='k', headWidth=0.05, width=0.005, lw=1)
		f.addArrow([0.1,-0.1], [0.1+2,-0.1+2], color='k', headWidth=0.05, width=0.005, lw=1)

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
		f.addLine([5,10], [5,5], mplprops={'ls':'dotted'})
		#f.addLine([0.02,0.02], [0.06,0.05], lw=2, mplprops={'color':'r'})


	# BOX #
	def box(f):
		f.addBox((0,20), (0,20), xlabel='hello', ylabel='yellow', title='This is the title', mplprops={'color':'k'})
		#f.addBox((0,20), (0,20))


	# WRITE #
	def write(f):
		f.__draw_shapes__()
		s = f.__export__()
		f = open('images/test.svg', "w+")
		f.write(s)
		f.flush()
		f.close()

	# INIT #
	#f = figures.Figures([[-0.06,0.06],[-0.06, 0.06]], height='auto', bgcolor='w')
	#f = figures.Figures([[-10,10],[-10,10]], height=400, width=400, bgcolor='w')
	#f = figures.Figures([[-15,15],[-15,15]], height=600, width=600, bgcolor='w')
	f = figures.Figures([[-.5,2.6], [-.5, 2.6]], width=200, height=200)

	#f = figures.Figures([[-7, 5],[-4, 4]], width=400, height=300)

	#triangle(f)
	#function(f)
	#circle(f)
	#ellipse(f)
	#polygon(f)
	#regpoly(f)
	#point(f)
	#text(f)
	arrow(f)
	#wedge(f)
	#line(f)
	#box(f)
	axis(f)
	write(f)

if __name__ == "__main__":
	unit_test()
