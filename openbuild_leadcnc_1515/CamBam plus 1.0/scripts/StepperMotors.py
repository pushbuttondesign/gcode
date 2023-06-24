from System.Collections.Generic import List
from CamBam.Geom import *
from CamBam.CAD import *

class stepper_frame:
    def __init__(self,name,DD,a,b,c,d,e,g):
        self.name = name
        # width of frame square
        self.DD = DD
        # bolt hole distance
        self.a = a
        # shaft diameter
        self.b = b
        # shaft length
        self.c = c
        # pilot diameter
        self.d = d
        # pilot depth
        self.e = e
        # bolt hole size
        self.g = g
        

    def getFrontView(self):
        shapes = List[Entity]()
        
        # frame
        rect = PolyRectangle(Point3F(-self.DD/2.0,-self.DD/2.0,0),self.DD,self.DD)
        rect.CornerRadius = self.g / 2.0
        rect.Update()
        shapes.Add(rect)
        # shaft
        shapes.Add(Circle(Point3F(0,0,0),self.b/2.0))
        # pilot
        shapes.Add(Circle(Point3F(0,0,0),self.d/2.0))
        # bolt holes
        centers = PointList()
        centers.Add(self.a/2.0,self.a/2.0,0)
        centers.Add(-self.a/2.0,self.a/2.0,0)
        centers.Add(-self.a/2.0,-self.a/2.0,0)
        centers.Add(self.a/2.0,-self.a/2.0,0)
        shapes.Add(centers)
        
        for c in centers.Points:
            shapes.Add(Circle(c,self.g/2.0))
        
        return shapes        

    def getSideView(self,L):
        shapes = List[Entity]()
        
        # frame
        rect = PolyRectangle(Point3F(-L,-self.DD/2.0,0),L,self.DD)
        rect.Update()
        shapes.Add(rect)
        # shaft
        shaft_rect = PolyRectangle(Point3F(0,-self.b/2.0,0),self.c,self.b)
        shapes.Add(shaft_rect)
        # pilot
        pilot_rect = PolyRectangle(Point3F(0,-self.d/2.0,0),self.e,self.d)
        shapes.Add(pilot_rect)
        # bolt holes
        centers = PointList()
        centers.Add(0,self.a/2.0,0)
        centers.Add(0,-self.a/2.0,0)
        centers.Add(0,0,0)
        shapes.Add(centers)
        
        return shapes        


nema8 = stepper_frame("NEMA8",0.8*25.4,16.0,4.0,10.0,15.0,1.5,3.0)
nema11 = stepper_frame("NEMA11",1.1*25.4,23.0,5.0,15.0,22.0,2.0,4.0)
nema14 = stepper_frame("NEMA14",1.4*25.4,26.0,5.0,15.0,22.0,2.0,4.0)
nema17 = stepper_frame("NEMA17",1.7*25.4,31.0,5.0,24.0,22.0,2.0,2.845)
# NEMA23 6.35 or 10mm shaft
nema23 = stepper_frame("NEMA23",2.3*25.4,47.0,6.35,20.0,38.1,1.6,5.0)
nema34 = stepper_frame("NEMA34",3.4*25.4,69.6,14.0,38.0,73.0,1.6,6.5)
nema42 = stepper_frame("NEMA42",4.2*25.4,88.9,19.0,55.0,55.5,1.6,8.5)
        

