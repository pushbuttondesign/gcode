"""

  boingy.py
  CamBam jscript - converted from boingy.vbs
  (c) 2010 Andy Payne (10Bulls)
  (c) 2007 Andy Payne (10Bulls)

  NOTE: For best effect, rotate the view before or during running this script.

"""

def main():
    doc.ClearAll()
    view.DrawingTree.ReloadTree()
    p = MakeHelix()
    doc.Add(p)
    boingit(p)



def MakeHelix():
    start = 0.0						# in radians
    finish = 30.0*Math.PI			# in radians
    steps = 500						# number of steps
    radius = 10.0
    startz = 20.0
    endz = 0.0

    x = 0.0
    y = 0.0
    z = startz

    th = start
    dt = (finish-start)/steps
    dz = (endz-startz)/steps

    # Get the drawing ready to draw	
    p = Polyline()

    # Play da loop
    for i in range(0,steps):
        z = z + dz
        th = th + dt
        x = radius * Math.Cos(th)
        y = radius * Math.Sin(th)

        p.Add(x,y,z)
	
    return p


def boingit( p ):
    th = 0.0
    for i in range(100):
        th += 20*Math.PI/100

        p.Transform.m[10] = 1 + Math.Sin(th)/5

        # Repaint the view
        view.RefreshView()

        # Slow things down so we can see
        app.Sleep(20)


main()
