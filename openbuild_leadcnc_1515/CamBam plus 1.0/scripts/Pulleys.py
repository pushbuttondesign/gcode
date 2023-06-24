from System import Math
from System import Array
from System.Collections.Generic import List
from CamBam.UI import CamBamUI
from CamBam.Geom import *
from CamBam.CAD import *

class HTDPulley:
    def __init__(self,pitch,teeth):
        self.P = pitch
        self.N = teeth
        self.PD = pitch * teeth / Math.PI

    def getFrontView(self):
        shapes = List[Entity]()
        # teeth profile
        # TODO: handle other pitches
        if (self.P == 5.0):
            teeth_profile = self.getTeethProfile()
            if (teeth_profile):
                shapes.Add(teeth_profile)
        else:
            # pitch circle
            shapes.Add(Circle(Point3F(0,0,0),self.PD/2.0))
        # shapes.Add(Circle(Point3F(0,0,0),self.PD/2.0))
        return shapes

    def getPitchCircle(self):
        return Circle(Point3F(0,0,0),self.PD/2.0)

    def getOuterCircle(self):
        return Circle(Point3F(0,0,0),self.getOuterDiameter()/2.0)

    def getBeltCircle(self):
        t = 0.0
        if (self.P==3.0):
            t = 2.41-1.22
        elif (self.P==5.0):
            t = 3.81-2.08
        elif (self.P==8.0):
            t = 13.2-8.4
        if (t==0):
            return none
        
        return Circle(Point3F(0,0,0),self.getOuterDiameter()/2.0+t)


    def getSideView(self,W,hub,flange):
        shapes = List[Entity]()
        # body
        body_rect = PolyRectangle(Point3F(0,-self.PD/2.0,0),W,self.PD)
        shapes.Add(body_rect)
        #flanges
        if (flange):
            shapes.Add(PolyRectangle(Point3F(-1.0,-flange/2.0,0),1.0,flange))
            shapes.Add(PolyRectangle(Point3F(W,-flange/2.0,0),1.0,flange))
        if (hub):
            hx = -5.0
            if (flange):
                hx = hx - 1.0
            shapes.Add(PolyRectangle(Point3F(hx,-hub/2.0,0),5.0,hub))
        return shapes

    def getOuterDiameter(self):
        u = 0.0
        if (self.P==3.0):
            u = 0.381   # 0.015"
        elif (self.P==5.0):
            u = 0.5715  # 0.0225"
        elif (self.P==8.0):
            u = 0.6858  # 0.027"
        if (u==0):
            return none

        return self.PD - 2.0 * u
        
    
    def getTeethProfile(self):
        # TODO: handle other pitches
        # http://www.sdp-si.com/D265/HTML/D265T015.html
        # http://www.sdp-si.com/D265/PDF/D265T016.pdf
        # tooth_diam = 3.0
        tooth_diam = 3.1

        outer_dia = self.getOuterDiameter()

        profile = Polyline()

        tooth_profile = Polyline()

        # generate tooth profile

        a1 = Arc2F(Point2F(outer_dia/2.0-0.6,0),tooth_diam/2.0,-90.0,-180.0)

        th1 = Math.Asin((tooth_diam/2.0) / (outer_dia/2.0-0.6))
        th1 = th1 / Math.PI * 180.0

        # fillet_arc = 0.4 / (outer_dia/2.0)
        fillet_arc = 0.6 / (outer_dia/2.0)
        fillet_arc = fillet_arc / Math.PI * 180.0
        start = th1 + fillet_arc
        sweep = 360.0/self.N - 2.0*th1 - 2.0*fillet_arc
        a3 = Arc2F(Point2F(0,0),outer_dia/2.0,start,sweep)

        # aswp = 100.0  # better for small number of teeth
        aswp = 90.0     # better for larger number of teeth
        a2 = Arc2F( a1.P2, a3.P1, aswp )
        a0 = Arc2F( Point2F(a3.P1.X,-a3.P1.Y), a1.P1, aswp )

        tooth_profile.Add( a0, 0.00001 )
        tooth_profile.Add( a1, 0.00001 )
        tooth_profile.Add( a2, 0.00001 )
        tooth_profile.Add( a3, 0.00001 )

        pt = Array.CreateInstance(Polyline,self.N)

        # rotate and append profiles
        for i in range(0,self.N):
            th = float(i) / self.N * 2.0 * Math.PI
            px = tooth_profile.Clone()
            px.Transform.RotZ( th )
            pt[i] = px

        pret = Polyline.Join(pt, 0.00001 )

        for pulley in pret:
            if (pulley.Points.Count > 1):
                scale = 1.0/Unit.GetFactor(CamBamUI.MainUI.ActiveView.CADFile.DrawingUnits)
                if (scale != 1.0):
                    pulley.Transform.Scale(scale, scale, 1)
                if (pulley.ApplyTransformation()):
                    pulley.Transform = Matrix4x4F.Identity
                return pulley

    def getCenterDistance( self, other, beltlength):
        # estimate only
        return Math.Sqrt(Math.Pow((beltlength-(0.5*Math.PI*(self.PD+other.PD)))/2,2)-Math.Pow((0.5*self.PD-0.5*other.PD),2))
