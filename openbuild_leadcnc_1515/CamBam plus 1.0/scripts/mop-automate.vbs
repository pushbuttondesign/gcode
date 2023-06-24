'
'	mop-automate.vbs
'
'	This python script demonstrates:	
'		. opening a CAD file (.dxf in this example)
'		. drawing some extra shapes into the drawing
'		. setting machining options
'		. Call asynchronous CAD functions such as
'			Edit -> Join and Edit -> Convert to polyline
'		. creating a machining operation from objects in a drawing layer
'		. setting machining operation properties
'		. saving a drawing and creating g-code
'
sub main

	' TO CHANGE...
	dim source_file = "C:\CamBam\cbfiles\aluskids.dxf"
	dim out_filename = "C:\dump\test.cb"

	' Open a source file
	' note: the second parameter '1' opens the file synchronously rather than in a worker thread
	CamBamUI.MainUI.OpenFile(source_file,1)

	' The 'doc' global variable is always the CADFile before any file opens,
	' so we create a new varialbe pointing to the newly opened active file...
	dim newdoc = view.CADFile
	
	' draw some shapes...
	dim poly = new Polyline()
	poly.Add(8,5,0)
	poly.Add(22,5,0)
	poly.Add(25,15,0)
	poly.Add(15,25,0)
	poly.Add(5,15,0)
	poly.Closed=True
	newdoc.Add(poly)
	
	dim circle = new Circle()
	circle.Center = new Point3F(-30,15,0)
	circle.Diameter=15
	newdoc.Add(circle)

	' set any machining options required...
	newdoc.MachiningOptions.PostProcessor = "Mach3-CutViewer"
	newdoc.MachiningOptions.FastPlungeHeight = 0.1

	' Select All...
	view.SelectAllVisibleGeometry()
	
	' Convert to polylines...
	PolylineUtils.PolyLinesConvert(view)
	' The gui operation runs in a worker process, so wait for the
	' thinking message to disapear...
	while not view.CurrentEditMode is nothing 
		app.Sleep(1)
	end while
	
	' Edit - Join
	PolylineUtils.JoinPolyLines(view,0.001)
	' wait for the thinking message to disapear...
	while not view.CurrentEditMode is nothing
		app.Sleep(1)
	end while

	' create a profile mop
	' Use all the drawing objects from the first layer...
	' dim profile = new MOPProfile(newdoc,newdoc.Layers(0).Entities)
	' Use all the drawing objects from the last layer...
	' dim profile = new MOPProfile(newdoc,newdoc.Layers(newdoc.Layers.Count-1).Entities)
	' Use all the drawing objects from a layer with a specific name...
	dim profile = new MOPProfile(newdoc,newdoc.Layers("LAYER_03").Entities)

	' Set the profile style property...
	profile.Style = "cutout"

	' Other properties are based on the generic CBValue class
	' Some examples of how these properties should be set...

	profile.ToolDiameter= profile.ToolDiameter.NewValue(0.8)
	profile.InsideOutside = profile.InsideOutside.NewValue(InsideOutsideOptions.Inside)

	' add the machine op to the drawing...
	CamBamUI.MainUI.InsertMOP(profile)

	' save the current drawing...
	newdoc.Save(out_filename)

	' create g-code output
	CAMUtils.GenerateGCodeOutput(view)

end sub
