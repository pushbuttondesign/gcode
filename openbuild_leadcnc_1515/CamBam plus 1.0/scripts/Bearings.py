from System import Math
from System import Array
from System.Collections.Generic import List
from CamBam.UI import CamBamUI
from CamBam.Geom import *
from CamBam.CAD import *

class BallBearing:
    def __init__(self,code,inner,inner2,outer,outer2,thickness):
        self.code = code
        self.ID = inner
        self.OD = outer
        self.ID2 = inner2
        self.OD2 = outer2
        self.T = thickness

    def getFrontView(self):
        shapes = List[Entity]()
        shapes.Add(Circle(Point3F(0,0,0),self.ID/2.0))
        shapes.Add(Circle(Point3F(0,0,0),self.ID2/2.0))
        shapes.Add(Circle(Point3F(0,0,0),self.OD/2.0))
        shapes.Add(Circle(Point3F(0,0,0),self.OD2/2.0))
        shapes.Add(PointList(0,0))
        return shapes

    def getSideView(self):
        shapes = List[Entity]()
        shapes.Add(PolyRectangle(Point3F(-self.T,-self.ID/2.0,0),self.T,self.ID))
        shapes.Add(PolyRectangle(Point3F(-self.T,-self.ID2/2.0,0),self.T,self.ID2))
        shapes.Add(PolyRectangle(Point3F(-self.T,-self.OD/2.0,0),self.T,self.OD))
        shapes.Add(PolyRectangle(Point3F(-self.T,-self.OD2/2.0,0),self.T,self.OD2))
        points = PointList()
        points.Add(0,0)
        points.Add(-self.T,0)
        shapes.Add(points)
        return shapes

Bearing_6000 = BallBearing("6000",10.0,14.8,26.0,22.6,8.0)