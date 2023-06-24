' elipse.vbs
'
' Generates an elipse polyline
'
' Author: Andy Payne [10bulls] 26 May 2006
'
sub main
	
	' Set a to the width of the elipse
	dim a as single = 35
	' Set b to the height of the elipse
	dim b as single = 30
	' Set steps to the number of line segments to use to approcximate the elipse
	' larger number will be smoother but slower.
	dim steps as single = 100
	
	
	dim t as single
	dim s as single
	dim poly as polyline =new Polyline()
    dim x as single
	dim y as single
	
	for s = 0 to steps-1 

		t = 2 * pi * s / steps
		x = a * Math.Cos(t)
		y = b * Math.Sin(t)
		poly.Add(x,y,0)

	next s

	poly.closed=true

	doc.Add(poly)

end sub
