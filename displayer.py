import tkinter

# Interface

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

    def drawPath(self, points):
        q=points[0]
        for p in points[1:]:
            self.w.create_line(q[0], q[1], p[0], p[1], fill="red")
            q=p

    def drawCurves(self, curves):
        for c in curves:
            points=c.sample(50)
            q=points[0]
            for p in points[1:]:
                self.w.create_line(q[0], q[1], p[0], p[1], fill="green")
                q=p
            
    def getSpace(self):
        return self.space
