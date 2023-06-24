"""Routines for creating various 3D meshes.

"""
from System import Math
from System import Array
from System.Collections.Generic import List
from CamBam.UI import CamBamUI
from CamBam.Geom import *
from CamBam.CAD import *

def ExtrudeSolid( shapeids, height, t ):
    """Creates solid meshes by extruding 2D shapes along the Z axis.

    Args:
        shapeids : an array of entity ids or a string containing a layer name.
        height (double) : the height to extrude along the positive Z axis.
        t (double) : tolerance used when expanding curves to faces.

    Example:
        import Solids
        # extrude all objects on Layer1, 10 drawing units.
        this.Entities.Add(Solids.ExtrudeSolid("Layer1",10.0,0.1))

    Returns:
        List[Entity] : A list of surface entities.
    
    """    
    shapes = ShapeList()
    shapes.ApplyTransformations = True

    if isinstance(shapeids,str):
        shapes.AddEntities(CamBamUI.MainUI.ActiveView.CADFile.Layers[shapeids].Entities)
    else:
        for id in shapeids:
            ent = CamBamUI.MainUI.ActiveView.CADFile.FindPrimitive(id)
            if ent == None:
                print str(id) + " not found"
                continue
            shapes.AddEntity(ent)
    regions = shapes.DetectRegions()

    ret = List[Entity]()

    for itm in regions:
        ss = CAD3DUtils.Extrude(itm.Shape,t,height,True,True)
        ret.Add(ss)
    
    return ret

def SurfaceOfRevolution( shapeids, steps, t, invertfaces=False ):
    """Creates solid meshes by rotating 2D shapes around the Y axis.

    Args:
        shapeids : an array of entity ids or a string containing a layer name.
        steps (int) : number of angular steps per revolution.
        t (double) : tolerance used when expanding curves to faces.
        invertfaces (bool) : if True, reverses the mesh face orientation.

    Example:
        import Solids
        # create a surface of revolution from all objects on Layer2.
        this.Entities.Add(Solids.SurfaceOfRevolution("Layer2",200,0.1,False))

    Returns:
        List[Entity] : A list of surface entities.
    
    """    
    shapes = ShapeList()
    shapes.ApplyTransformations = True

    if isinstance(shapeids,str):
        shapes.AddEntities(CamBamUI.MainUI.ActiveView.CADFile.Layers[shapeids].Entities)
    else:
        for id in shapeids:
            ent = CamBamUI.MainUI.ActiveView.CADFile.FindPrimitive(id)
            if ent == None:
                print str(id) + " not found"
                continue
            shapes.AddEntity(ent)
    regions = shapes.DetectRegions()

    ret = List[Entity]()

    for itm in regions:

        if itm.Shape.GetType() == Region().GetType():
            region = itm.Shape
            ss = RevolvePolyline(region.OuterCurve,steps,t)
            ret.Add(ss)
            for hole in region.HoleCurves:
                sshole = RevolvePolyline(hole,steps,t,invertfaces)
                ret.Add(sshole)
        else:
            ss = RevolvePolyline(itm.Shape,steps,t,invertfaces)
            ret.Add(ss)
    
    return ret

def RevolvePolyline( poly, steps, t, invertfaces ):
    """Creates solid meshes by rotating a polyline around the Y axis.

    Args:
        poly (Polyline) : a Polyline to rotate.
        steps (int) : number of angular steps per revolution.
        t (double) : tolerance used when expanding curves to faces.
        invertfaces (bool) : if True, reverses the mesh face orientation.

    Returns:
        Surface : A surface entity.
    
    """    

    # angle increment per step    
    dt = 2.0 * Math.PI / steps
    
    # create a copy of the polyline with arcs converted to line segments
    lpoly = poly.RemoveArcs(t)
    np = lpoly.Points.Count
    fp = np
    if (lpoly.Closed): fp += 1
    
    surf = Surface()
    surf.Points = Point3FArray(np * steps, True)
    faces = List[TriangleFace]((np - 1) * 2 * steps)
    
    sweep = 0.0
    f = 0
    
    for band in range(0,steps):
    
        mrot = Matrix4x4F.RotationY(sweep)
        
        for i in range (0,np):
        
            if (i < np or not lpoly.Closed):
                p = lpoly.Points[i].Point
                p = p * mrot
                surf.Points.Add(p)
                
            if (i < np-1):
                nextpoint = i + 1
            else:
                nextpoint = 0
            
            if (band < steps-1):    
                nextband = band+1
            else:
                # last band, so back to start band
                nextband = 0
                
            if (i < fp-1 and band < steps ):
                faces.Add(TriangleFace((np * band) + i, (np * band) + nextpoint, (np * nextband) + nextpoint ))
                faces.Add(TriangleFace((np * band) + i, (np * nextband) + nextpoint, (np * nextband) + i ))
        
        sweep += dt

    surf.Faces = faces.ToArray()            
    
    invert = lpoly.Direction == RotationDirection.CCW
    if invertfaces: invert = not invert
    
    if invert:
        surf.InvertFaces()
    
    return surf
            