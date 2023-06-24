# elipse.py
#
# Generates an elipse polyline
#
# Author: Andy Payne [10bulls] 26 May 2006
# Converted to Python 23 March 2012
#
	
# Set a to the width of the elipse
a = 60.0

# Set b to the height of the elipse
b = 35.0

# Set steps to the number of line segments to use to approcximate the elipse
# larger number will be smoother but slower.
steps = 100

poly = Polyline()

for s in range(0, steps-1):
	t = 2 * Math.PI * s / steps
	x = a * Math.Cos(t)
	y = b * Math.Sin(t)
	poly.Add(x,y,0)

poly.Closed=1

doc.Add(poly)

