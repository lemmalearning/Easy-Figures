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
	f.format_axis(xyrange=[[-10,10], [-10,10]], grid=True, tick_interval=.25, tick_label_interval=1, color='blue')
	f.__writeFile__('/Users/<USER>/axis.png')

![Axis](images/axis.png "Axis")

##### Functions


	f = figures.Figures()
	func = lambda x: x**2
	f.add_function(func, [[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]], colors="blue")
	f.format_axis(xyrange=[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]])
	f.__writeFile__('/Users/<USER>/axis-f.png')

![Function](images/func.png "Function")


---
	f = figures.Figures()
	func1 = lambda x: x**2
	func2 = lambda x: x**3
	f.add_function([func1, func2], [[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]],[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]]], colors=["blue", "green"])
	f.format_axis(xyrange=[[-3*np.pi,3*np.pi],[-3*np.pi,3*np.pi]])
	f.__writeFile__('/Users/<USER>/func-multi.png')

![Function (Multiple)](images/func-multi.png "Function (Multiple)")



# License

* Licensed under the Apache License
* Please note: Any and all modifications to this code must also be licensed under Apache
