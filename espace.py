
from tkinter import *

# Structures de données et fonction d'interface

class Obstacle:
    # Obstacle triangulaire
    
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
        # Le point est-il dans l'obstacle ?
        dot02=self.u[0]*x + self.u[1]*y
        dot12=self.v[0]*x + self.v[1]*y
        k = (self.dot11 * dot02 - self.dot01 * dot12) * self.invDenom
        j = (self.dot00 * dot12 - self.dot01 * dot02) * self.invDenom
        return (k >= 0 and j >= 0 and k + j <=1)

    def visible(self,Cx,Cy,Dx,Dy):
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

class Space:
    # Espace d'obstacles

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
        
    def addObstacle(self,obs):
        self.obstacles+=[obs]

    def visible(self,x1,y1,x2,y2):
        for obs in self.obstacles:
            if not obs.visible(x1,y1,x2,y2):
                return False
        return True

    def isFree(self,x,y):
        for obs in self.obstacles:
            if obs.inside(x,y):
                return False
        return True
    

class Displayer():
    
    def __init__(self, master, space):
        self.master=master
        self.w=Canvas(self.master,width=space.width,height=space.height)
        self.w.pack()
        self.space=space
        self.refreshAll()
        self.w.xview_moveto(self.w.canvasx(10))
        self.w.yview_moveto(self.w.canvasy(10))

    def drawObstacle(self,obs):
        self.w.create_polygon(obs.points,fill="blue")

    def refreshAll(self):
        self.w.delete(ALL)
        self.w.create_rectangle(0,0,self.space.width,self.space.height,fill="white")
        for obs in self.space.obstacles:
            self.drawObstacle(obs)

    def drawGraph(self,graphe):
        points=graphe.points
        adj=graphe.adjacence
        print(adj)
        for i in range(len(points)):
            Ax=points[i][0]
            Ay=points[i][1]
            for j in adj[i]:
                if j<=i:
                    continue
                self.w.create_line(Ax,Ay,points[j][0],points[j][1],fill="black")
        self.w.create_oval(points[0][0]-2,points[0][1]-2,points[0][0]+2,points[0][1]+2,fill="red")
        self.w.create_oval(points[1][0]-2,points[1][1]-2,points[1][0]+2,points[1][1]+2,fill="red")
