'//////////////////////////////////////////////////////////////////////////////
'
' spiral-fan.vbs 
' CamBam vbscript
' (c) 2007 Andy Payne (10Bulls)
'
sub main

	dim startz as single = 0
	dim depth as single = -2
	dim steps as single = 200
	dim arms = 5
	dim tail = -0.7*pi/arms
	dim th as single
	dim minrad = 6
	dim maxrad = 15
	dim radsteps = 12
	dim drad = (maxrad-minrad)/radsteps

	doc.ActiveLayer.Entities.Clear()

	th = pi/arms

	for i as integer = 1 to arms
		for rr as integer = 1 to radsteps

			MakeSpiral( th, th+tail-rr*pi/50, steps, minrad + rr * drad, startz, depth )

		next rr

		th = th + 2 * pi/arms
	
	next i

end sub

'//////////////////////////////////////////////////////////////////////////////
'
'   MakeSpiral
'
'   Parameters
'        start :    start angle in radians
'        finish :   finish angle in radians
'        steps :    number of steps in the resulting polyline (bigger is smoother but slower)
'        radius :   the radius of the spiral
'        startz :   the z value at the top of the spiral
'        endz :     the z value at the end of the spiral
'
sub MakeSpiral( start as single, finish as single, steps as single, radius as single, startz as single, endz as single )

	dim x as single = 0
	dim y as single = 0
	dim z as single = startz

	dim th as single = start
	dim dt as single = (finish-start)/steps
	dim dz as single = (endz-startz)/steps

	'// Get the drawing ready to draw	
	dim p as Polyline = new Polyline

	'// Play da loop
	for i as short = 0 to steps
		x = radius * math.cos(th)
		y = radius * math.sin(th)
		p.Add(x,y,z)
		th = th + dt
		z = z + dz
	next i
		
	'// add the polyline to the current drawing
	doc.Add(p)

end sub
