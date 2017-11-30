import matplotlib.colors
import six

def convert_color(c):
	if isinstance(c, six.string_types):
		c = matplotlib.colors.to_rgba(c)
		
	return "rgba(" + ", ".join([ str(int(255*x)) for x in c[0:3] ]) + ", " + str(c[-1]) + ")"