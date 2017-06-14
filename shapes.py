import matplotlib.pyplot as plt

plt.axes()

circle = plt.Circle((0, 0), radius=0.75, fc='y')
plt.gca().add_patch(circle)
plt.axis('off')
plt.axis('scaled')

#plt.show()
plt.figure().savefig('/Users/ajpersinger/test.png', transparent=True)


class Circle():
	def __init__(radius=1, fill='transparent', center=(0, 0)):
		self.radius = radius
		self.background = background
		self.center = center
