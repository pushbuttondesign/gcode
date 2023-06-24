//////////////////////////////////////////////////////////////////////////////
//
// boingy.js
// CamBam jscript - converted from boingy.vbs
// (c) 2010 Andy Payne (10Bulls)
// (c) 2007 Andy Payne (10Bulls)
//
//   NOTE: For best effect, rotate the view before or during running this script.

function main()
{
	var p : Polyline = MakeHelix();
	doc.Add(p);
	boingit(p);
}


function boingit( p : Polyline )
{
	var th : double = 0;
	for(var i : int = 0; i < 100; i++)
	{
		th += 20*Math.PI/100;

		p.Transform.m(10) = 1 + Math.sin(th)/5;

		// Repain the view
		view.RefreshView();

		// Slow things down so we can see
		app.Sleep(20);
	}
}


function  MakeHelix() : Polyline
{
	var start : double	= 0;		// in radians
	var finish : double = 30*Math.PI;	// in radians
	var steps : double	= 500;		// number of steps
	var radius : double = 10;
	var startz : double = 20;
	var endz : double   = 0;

	var x : double = 0;
	var y : double = 0;
	var z : double = startz;

	var th : double = start;
	var dt : double = (finish-start)/steps;
	var dz : double = (endz-startz)/steps;

	// Get the drawing ready to draw	
	var p : Polyline = new Polyline();

	// Play da loop
	for (var i : int = 0 ; i <= steps; i++)
	{
		z = z + dz;
		th = th + dt;
		x = radius * Math.cos(th);
		y = radius * Math.sin(th);

		p.Add(x,y,z);
	}

	return p;
}

main();
