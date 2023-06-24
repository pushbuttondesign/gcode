// Tapered spiral generator

// Change these bits...

var radius_1 : double = 25;			// Start Radius
var radius_2 : double = 20;			// End Radius
var depth_increment : double = 1;	
var startz : double = 0;			
var endz : double = -50;

// Leave these bits...

var steps_per_loop : double = 10;
var x : double = 0;
var y : double = 0;
var z : double = startz;
var th : double = 0;
var dt : double = Math.PI*2.0/steps_per_loop;
var dz : double = depth_increment/steps_per_loop;
var bulge : double = Math.tan(dt/4.0);
var zheight : double = startz - endz;

var p : Polyline = new Polyline();

while( z > endz )
{
	var radius : double = radius_2 + (radius_1-radius_2) * (zheight - startz + z) / zheight;

	x = radius * Math.cos(th);
	y = radius * Math.sin(th);
	p.Add(x,y,z,bulge,1e-5);
	
	if (z - dz <= endz)
	{
		var z2go : double = z - endz;
        if (dz != 0)
        {
        	var th2go : double = (z2go / dz) * dt;
            x = radius_2 * Math.cos(th);
            y = radius_2 * Math.sin(th);
            th += th2go;

            p.Add(x, y, z, Math.tan(th2go/4.0), 1e-5);
		}
		break;
	}
	z -= dz;
	th += dt	
}

// move to center
p.Add(0,0,z);


doc.Add(p);


