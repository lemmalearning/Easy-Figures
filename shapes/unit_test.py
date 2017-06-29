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
	# AXIS #
	def axis(f):
		axis = f.addAxis(hideAxis=False, grid=True, arrows=True, color='black', minorGrid='red')
		axis.Ticks(tickLabelInterval=2, tickInterval=1, fontsize=12, origin=True, top=True)

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

	#triangle(f)
	#function(f)
	#circle(f)
	#ellipse(f)
	#polygon(f)
	axis(f)
	#point(f)
	#text(f)
	#arrow(f)
	print "correct file?"
	f.__draw_shapes__()
	s = f.__export__()
	f = open('images/test.svg', "w+")
	f.write(s)
	f.flush()
	f.close()



if __name__ == "__main__":
	unit_test()
