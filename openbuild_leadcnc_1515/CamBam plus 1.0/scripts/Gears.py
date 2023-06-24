from System import Math
from System import Array
from System.Collections.Generic import List
from CamBam.UI import CamBamUI
from CamBam.Geom import *
from CamBam.CAD import *

# pitch = diametral pitch (or normal module)
# teeth = number of teeth
# pressureangle = pressure angle (degrees) 20 deg most common, 14.5 sometimes used
# internal = True if an internal (ring) gear, otherwise False

class InvoluteGear:
    def __init__(self,pitch,teeth,pressureangle,internal):
        self.P = pitch
        self.N = teeth
        self.PA = pressureangle
        self.Internal = internal
        
        # pitchdiameter
        if self.P > 0:
            self.D = self.N / self.P
        # pitch radius
        self.R = self.D / 2
        # base circle diameter
        self.DB = self.D * Math.Cos(self.PA * Math.PI / 180.0)
        # base circle radius
        self.RB = self.DB / 2.0
        # addendum
        # NOTE: should we apply clearance to addendum for internal gears?
        self.a = 1.0 / self.P
        # dedendum
        # NOTE: using clearance factor of 0.157 (ie clearance distance = 0.157 / Pd
        if (self.Internal):
            self.d = (1.0 - 0.157) / self.P
        else:
            self.d = (1.0 + 0.157) / self.P
        # outside diameter
        self.OD = self.D + (self.a * 2.0)
        # outside radius
        self.RO = self.R + self.a
        # root diameter
        self.DR = self.D - (self.d * 2)
        # root radius
        self.RR = self.R - self.d
        # circumference of base circle
        self.CB = Math.PI * self.DB
        # base circle ratio (not sure where 20.0 comes from)
        self.FCB = self.RB / 20.0
        # number of times that FCB can be divided into CB
        self.NCB = self.CB / self.FCB
        # 360 degrees divided by NCB
        self.ACB = 360.0 / self.NCB
        # gear tooth spacing
        self.GT = 360.0 / float(self.N)

    def getFrontView(self):
        shapes = List[Entity]()
        # teeth profile
        teeth_profile = self.getTeethProfile()
        if (teeth_profile):
            shapes.Add(teeth_profile)
        else:
            # pitch circle
            shapes.Add(Circle(Point3F(0,0,0),self.D/2.0))
        return shapes

        
    def getPitchCircle(self):
        return Circle(Point3F(0,0,0),self.D/2.0)

    def getOuterCircle(self):
        return Circle(Point3F(0,0,0),self.OD/2.0)

    def getSideView(self,W,hub,flange):
        shapes = List[Entity]()
        # body
        body_rect = PolyRectangle(Point3F(0,-self.OD/2.0,0),W,self.OD)
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

        
    def getTeethProfile(self):
        INVOLUTE_SEGMENTS = 20
        
        # output outside diameter
        outsidediameter = self.OD
        # output maximum endmill diameter
        maxendmilldiameter = (self.DR * Math.PI) / (2.0 * float(self.N))

        # calculate line endpoints
        endpoints = Array.CreateInstance(Point2F,INVOLUTE_SEGMENTS)
        
        angle = 0.0
        for line in range(0,INVOLUTE_SEGMENTS):
            # endpoints[line].X = Math.Sin(angle * Math.PI / 180.0) * self.RB
            # endpoints[line].Y = Math.Cos(angle * Math.PI / 180.0) * self.RB
            endpoints[line] = Point2F(Math.Sin(angle * Math.PI / 180.0) * self.RB, Math.Cos(angle * Math.PI / 180.0) * self.RB )
            angle += self.ACB

        # calculate involute points
        involutepoints = Array.CreateInstance(Point2F,INVOLUTE_SEGMENTS)
        
        angle = 0.0
        for line in range(0,INVOLUTE_SEGMENTS):
            linelength = float(INVOLUTE_SEGMENTS - 1 - line) * self.FCB
            # involutepoints[line].X = endpoints[line].X + Math.Cos(angle * Math.PI / 180.0) * linelength
            # involutepoints[line].Y = endpoints[line].Y - Math.Sin(angle * Math.PI / 180.0) * linelength
            involutepoints[line] = Point2F(endpoints[line].X + Math.Cos(angle * Math.PI / 180.0) * linelength, endpoints[line].Y - Math.Sin(angle * Math.PI / 180.0) * linelength )
            angle += self.ACB

        # construct involute curve
        involute = Polyline()
        for line in range(0,INVOLUTE_SEGMENTS):
            involute.Add(Point3F(involutepoints[line].X, involutepoints[line].Y, 0))

        # extend involute to center of gear
        involute.Add(Point3F(0, 0, 0))

        # create outside diameter circle as polyline
        do_circle_poly = Circle(0, 0, self.RO).ToPolyline()

        # create root diameter circle as polyline
        dr_circle_poly = Circle(0, 0, self.RR).ToPolyline()

        # create pitch diameter circle as polyline
        d_circle_poly = Circle(0, 0, self.R).ToPolyline()
        
        # find intersection of outside diameter circle and involute curve
        involute_end = Polyline.PolylineIntersections(involute, do_circle_poly, 0.000001)
        if (involute_end.Length == 0):
            print "Involute Gear Generator has failed. Please report the parameters used to us for testing (error code: 1)."
            return None

        # split involute curve at intersection - keep bottom part
        involute2 = involute.SplitAtPoint(involute_end[0], 0.000001)[1]

        # find intersection of root diameter circle and involute curve
        involute_end2 = Polyline.PolylineIntersections(involute2, dr_circle_poly, 0.000001)
        if (involute_end2.Length == 0):
            print "Involute Gear Generator has failed. Please report the parameters used to us for testing (error code: 1)."
            return None

        # split involute curve at intersection - keep top part
        involute_curve_r = involute2.SplitAtPoint(involute_end2[0], 0.000001)[0]

        # find intersection of pitch diameter circle and involute curve
        pitch_involute = Polyline.PolylineIntersections(involute_curve_r, d_circle_poly, 0.000001)
        if (pitch_involute.Length == 0):
            print "Involute Gear Generator has failed. Please report the parameters used to us for testing (error code: 1)."
            return None
            
        # calculate angle to intersection in degrees
        pitch_involute_theta = Math.Acos(pitch_involute[0].Y / self.R) * 180.0 / Math.PI

        # calculate angle for "mirror line"
        mirror_theta = pitch_involute_theta - (self.GT / 4.0)

        # create a polyline for the left side of the tooth
        involute_curve_l = Polyline()

        # mirror using "mirror line"
        self.radialMirror(involute_curve_r, involute_curve_l, mirror_theta)

        tooth_profile = Polyline()
        
        self.getToothProfile(involute_curve_l, involute_curve_r, tooth_profile, self.RO, self.RR, self.GT)

        # generate gear
        teeth = Array.CreateInstance(Polyline,self.N)
        
        angle = 0.0
        for t in range(0,self.N):
            pl = tooth_profile.Clone()
            pl.Transform.RotZ(angle)
            teeth[t] = pl

            angle += self.GT * Math.PI / 180.0
        
        involutegear = Polyline.Join(teeth, 0.00001)

        for gearpart in involutegear:
            if (gearpart.Points.Count > 1):
                scale = 1.0/Unit.GetFactor(CamBamUI.MainUI.ActiveView.CADFile.DrawingUnits)
                if (scale != 1.0):
                    gearpart.Transform.Scale(scale, scale, 1)
                if (gearpart.ApplyTransformation()):
                    gearpart.Transform = Matrix4x4F.Identity
                return gearpart
                
                
    def radialMirror(self, original, mirrorcopy, degangle ):
        originalpoints = original.Points
        # loop through points
        for p in range(0, originalpoints.Count):
            # get point
            point = originalpoints[p].Point
            # get distance of point from center of circle
            distance = Math.Sqrt((point.X * point.X) + (point.Y * point.Y))
            # get angle of point in degrees
            theta = Math.Acos(point.Y / distance) * 180.0 / Math.PI
            # calculate new angle around mirror line
            theta = degangle - (theta - degangle)
            # calculate mirrored point location
            # point.X = Math.Sin(theta * Math.PI / 180.0) * distance
            # point.Y = Math.Cos(theta * Math.PI / 180.0) * distance
            # add to mirror copy
            # mirrorcopy.Add(point)
            mirrorcopy.Add(Point3F(Math.Sin(theta * Math.PI / 180.0) * distance, Math.Cos(theta * Math.PI / 180.0) * distance, 0 ))

    def getToothProfile(self,involute_l,involute_r,tooth,outsideradius,rootradius,toothspacing):
        # get lists of points for sides
        points_l = involute_l.Points
        points_r = involute_r.Points
        
        # add left side of tooth
        for p in range(points_l.Count - 1,-1,-1):
            tooth.Add(points_l[p].Point)

        # construct arc for end of tooth and add it
        toparc = Arc2F(Point2F(0, 0), Point2F(points_l[0].Point.X, points_l[0].Point.Y),  
                                      Point2F(points_r[0].Point.X, points_r[0].Point.Y), 
                                      RotationDirection.CW )
        tooth.Add(toparc, 0.000001)

        # add right side of tooth
        for p in range (0, points_r.Count):
            tooth.Add(points_r[p].Point)
        
        
        # get angle for last point on left size of tooth
        theta = Math.Acos(points_l[points_l.Count - 1].Point.Y / rootradius) * 180.0 / Math.PI
        # add to get start of next tooth
        theta += toothspacing

        # calculate new point
        nexttoothpoint = Point2F()
        #nexttoothpoint.X = Math.Sin(theta * Math.PI / 180.0) * rootradius
        #nexttoothpoint.Y = Math.Cos(theta * Math.PI / 180.0) * rootradius
        nexttoothpoint = Point2F(Math.Sin(theta * Math.PI / 180.0) * rootradius,Math.Cos(theta * Math.PI / 180.0) * rootradius)

        # construct arc for right side of profile and add it
        bottomarc = Arc2F(Point2F(0, 0), Point2F(points_r[points_r.Count - 1].Point.X, points_r[points_r.Count - 1].Point.Y), 
                                    nexttoothpoint, 
                                    RotationDirection.CW )
        tooth.Add(bottomarc, 0.000001)


class PlanetaryGear:
    def __init__(self,pitch,sunteeth,planetteeth,numplanets):
        self.Pitch = pitch
        self.SunTeeth = sunteeth
        self.PlanetTeeth = planetteeth
        self.NumPlanets = numplanets
        self.RingTeeth = 2*self.PlanetTeeth + self.SunTeeth
        # num ring teeth + num sun teeth must be evenly divisible by number of planets
        self.IsValid = ((self.RingTeeth + self.SunTeeth) % self.NumPlanets) == 0
        # number of turns of carrier for each turn of sun when ring is fixed
        self.CarrierRatio = self.SunTeeth / (self.SunTeeth + self.RingTeeth)
        # number of turns of ring for each turn of sun when carrier is fixed
        self.RingRatio = self.SunTeeth / self.RingTeeth
    