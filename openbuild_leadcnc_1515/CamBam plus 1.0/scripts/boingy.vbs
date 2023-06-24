'//////////////////////////////////////////////////////////////////////////////
'
' boingy.vbs
' CamBam vbscript
' (c) 2007 Andy Payne (10Bulls)
'
'   NOTE: For best effect, rotate the view before or during running this script.
'
sub main
	dim p as polyline =	MakeHelix()
	doc.add(p)
	boingit(p)
end sub


sub boingit( p as polyline )
	dim th as single = 0
	for i as short = 0 to 100

		th = th + 20*pi/100

		p.Transform.m(10) = 1 + math.sin(th)/5

		'// Repain the view
		view.RefreshView()

		'// Slow things down so we can see
		app.Sleep(20)

	next i
end sub


function  MakeHelix as polyline
	dim start as single	= 0			' in radians
	dim finish as single = 30*pi		' in radians
	dim steps as single	= 500		' number of steps
	dim radius as single = 10
	dim startz as single = 20
	dim endz as single   = 0

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
		z = z + dz
		th = th + dt
		x = radius * math.cos(th)
		y = radius * math.sin(th)

		p.Add(x,y,z)
	next i

	MakeHelix = p
		
end function
