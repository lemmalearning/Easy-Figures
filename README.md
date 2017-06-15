# README

### Purpose
The purpose of this library is to reduce the complexity of adding simple shapes
and creating function graphs using matplotlib.

### Structure
Shapes and functions are added to the `Figures` class which controls anything exported.
Using the `Figures` class you can either save to file or display it on the screen using various renderers.
The `Figures` lets you add shapes and modify the axes.

### Examples
##### Regular Polygon


    f = figures.Figures()
    poly = f.addPolygon(np.matrix([
	    [55, 45],
	    [45, 51],
	    [49, 63],
	    [60, 63],
	    [64, 51]
    ]))
    poly.labelVertices(['a','b','c','d','e'])
	f.__writeFile__('/Users/<USER>/polygon.png')

![Regular Polygon](images/polygon.png "Regular Polygon")

##### Circle


    f = figures.Figures()
    circ = f.addCircle(xy=(1, 2), label="r", radius=3)
	f.__writeFile__('/Users/<USER>/circle-r.png')

![Circle (Radius)](images/circle-r.png "Circle (Radius)")

---

	f = figures.Figures()
	circ = f.addCircle(xy=(1, 3), label="d", diameter=3)
	f.__writeFile__('/Users/<USER>/polygon.png')

![Circle (Diameter)](images/circle-d.png "Circle (Diameter)")

##### Axis


	f = figures.Figures()
	func = lambda x: x**2
	f.format_axis(xyrange=[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]], function=func)
	f.__writeFile__('/Users/<USER>/axis-f.png')

![Axis (with Function)](images/axis-f.png "Axis (with Function)")


---

	f = figures.Figures()
	f.format_axis(xyrange=[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]])
	f.__writeFile__('/Users/<USER>/axis.png')

![Axis](images/axis.png "Axis")



# License

* Licensed under the Apache License
* Please note: Any and all modifications to this code must also be licensed under Apache
