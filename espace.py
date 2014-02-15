# Structures de donnees
import math

# Configuration 
class Robot:
    l=50.
    trailerWidth=30.
    trailerLength=60.
    steerWidth=20.
    steerLength=20.

    @staticmethod
    def kappa2theta(q):
        return q[0:3] + [math.atan(Robot.l * q[3])]
    
    @staticmethod
    def theta2kappa(r):
        return r[0:3] + [math.tan(r[3] - r[2]) / Robot.l]

##############################################################################

# Obstacle triangulaire
class Obstacle:
    
    def __init__(self,points):
        self.points=points
        a=points[0:2]
        b=points[2:4]
        c=points[4:6]
        self.u=u=[b[0]-a[0],b[1]-a[1]]
        self.v=v=[c[0]-a[0],c[1]-a[1]]
        self.dot00=u[0]**2 + u[1]**2
        self.dot01=u[0]*v[0]+u[1]*v[1]
        self.dot11=v[0]**2 + v[1]**2
        self.invDenom = 1 / (self.dot00 * self.dot11 - self.dot01 * self.dot01)

    def inside(self,x,y):
        x=x-self.points[0]
        y=y-self.points[1]
        # Le point est-il dans l'obstacle ?
        dot02=self.u[0]*x + self.u[1]*y
        dot12=self.v[0]*x + self.v[1]*y
        k = (self.dot11 * dot02 - self.dot01 * dot12) * self.invDenom
        j = (self.dot00 * dot12 - self.dot01 * dot02) * self.invDenom
        return (k >= 0 and j >= 0 and k + j <=1)

    def visible(self, Cx, Cy, Dx, Dy):
        # Calcule si C est visible depuis D
        Ax=self.points[4]
        Ay=self.points[5]
        for j in range(3):
            k=j*2
            Bx=Ax
            By=Ay
            Ax=self.points[k]
            Ay=self.points[k+1]
            d=(Bx-Ax)*(Dy-Cy)-(By-Ay)*(Dx-Cx)
            if d==0:
                continue
            r=((Ay-Cy)*(Dx-Cx)-(Ax-Cx)*(Dy-Cy))/d
            s=((Ay-Cy)*(Bx-Ax)-(Ax-Cx)*(By-Ay))/d
            if r>=0 and r<=1 and s>=0 and s<=1:
                return False
        return True

    def collision(self, r):
        x, y, t1 = r[0:3]
        v1 = rotate([Robot.trailerLength/2, Robot.trailerWidth/2], t1)
        v2 = rotate([Robot.trailerLength/2, -Robot.trailerWidth/2], t1)
        if self.inside(x+v1[0], y+v1[1]) or self.inside(x+v2[0], y+v2[1]) or\
           self.inside(x-v1[0], y-v1[1]) or self.inside(x-v2[0], y-v2[1]) or\
           not self.visible(x+v1[0], y+v1[1], x+v2[0], y+v2[1]) or\
           not self.visible(x+v2[0], y+v2[1], x-v2[0], y-v2[1]) or\
           not self.visible(x-v1[0], y-v1[1], x-v2[0], y-v2[1]) or\
           not self.visible(x+v1[0], y+v1[1], x-v1[0], y-v1[1]) or\
           self.inside(x,y):
            return True
        x2 = x + Robot.l*math.cos(t1)
        y2 = y + Robot.l*math.sin(t1)
        if self.inside(x2,y2):
            return True
        if len(r)>3:
            t2=r[3]
            v1 = rotate([Robot.steerLength/2, Robot.steerWidth/2], t2)
            v2 = rotate([Robot.steerLength/2, -Robot.steerWidth/2], t2)
            if self.inside(x2+v1[0], y2+v1[1]) or self.inside(x2+v2[0], y2+v2[1]) or\
               self.inside(x2-v1[0], y2-v1[1]) or self.inside(x2-v2[0], y2-v2[1]) or\
               not self.visible(x2+v1[0], y2+v1[1], x2+v2[0], y2+v2[1]) or\
               not self.visible(x2+v2[0], y2+v2[1], x2-v2[0], y2-v2[1]) or\
               not self.visible(x2-v1[0], y2-v1[1], x2-v2[0], y2-v2[1]) or\
               not self.visible(x2+v1[0], y2+v1[1], x2-v1[0], y2-v1[1]):
                return True
        return False


def rotate(v, theta):
    return [v[0]*math.cos(theta)-v[1]*math.sin(theta), v[1]*math.cos(theta)+v[0]*math.sin(theta)]

##############################################################################

# Espace d'obstacles
class Space:

    def __init__(self,width,height):
        self.width=width
        self.height=height
        brdH0=Obstacle([0,0,width,0,0,-10])
        brdH1=Obstacle([width,-10,width,0,0,-10])
        brdG0=Obstacle([0,0,0,height,-10,0])
        brdG1=Obstacle([-10,0,0,height,-10,height])
        brdB0=Obstacle([0,height,width,height,0,height+10])
        brdB1=Obstacle([width,height+10,width,height,0,height+10])
        brdD0=Obstacle([width,0,width,height,width+10,0])
        brdD1=Obstacle([width+10,0,width,height,width+10,height])
        self.obstacles=[brdH0,brdH1,brdG0,brdG1,brdB0,brdB1,brdD0,brdD1]
        self.qBegin=[100,100,3,0]
        self.qEnd=[400,100,5,0]
        
    def addObstacle(self,obs):
        self.obstacles+=[obs]

    def visible(self, x1, y1, x2, y2):
        for obs in self.obstacles:
            if not obs.visible(x1,y1,x2,y2):
                return False
        return True

    def isFree(self,x,y):
        for obs in self.obstacles:
            if obs.inside(x,y):
                return False
        return True
    
    def collision(self, r):
        for obs in self.obstacles:
            if obs.collision(r):
                return True
        return False

    def collisionAny(self, rs):
        for r in rs:
            if self.collision(r):
                return True
        return False

