from tkinter import *
from tkinter import ttk
import math
from espace import *
import time

# Interface

class Displayer():
    
    def __init__(self, master, space):
        self.master = master
        self.canvas = Canvas(self.master, width=space.width, height=space.height)
        self.canvas.pack()
        self.space = space
        self.refreshAll()
        self.animPath=[]
        self.canvas.xview_moveto(self.canvas.canvasx(10))
        self.canvas.yview_moveto(self.canvas.canvasy(10))

    def drawObstacle(self,obs):
        self.canvas.create_polygon(obs.points, fill="blue")

    def refreshAll(self, configs=True):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0, 0, self.space.width, self.space.height, fill="white")
        for obs in self.space.obstacles:
            self.drawObstacle(obs)
        if configs:
            self.drawConfig(Robot.kappa2theta(self.space.qBegin))
            self.drawConfig(Robot.kappa2theta(self.space.qEnd))

    def drawGraph(self, graphe, color="grey"):
        points = graphe.points
        adj = graphe.adjacence
        for i in range(len(points)):
            Ax = points[i][0]
            Ay = points[i][1]
            for j in adj[i]:
                if j<=i:
                    continue
                self.canvas.create_line(Ax, Ay, points[j][0], points[j][1], fill=color)

    def drawPath(self, points, color="red"):
        q = points[0]
        for p in points[1:]:
            self.canvas.create_line(q[0], q[1], p[0], p[1], fill=color)
            q = p

    def drawCurves(self, curves, color="green"):
        for c in curves:
            points = c.sample(50)
            q = points[0]
            for p in points[1:]:
                self.canvas.create_line(q[0], q[1], p[0], p[1], fill=color)
                q = p
      
    def getSpace(self):
        return self.space
        
    def drawConfig(self, r, color="orange"):
        x, y, t1 = r[0:3]
        obj = []
        v1 = rotate([Robot.trailerLength/2, Robot.trailerWidth/2], t1)
        v2 = rotate([Robot.trailerLength/2, -Robot.trailerWidth/2], t1)
        obj += [self.canvas.create_polygon([x+v1[0], y+v1[1], x+v2[0], y+v2[1], x-v1[0], y-v1[1], x-v2[0], y-v2[1]], outline=color, fill="")]
        x2 = x + Robot.l*math.cos(t1)
        y2 = y + Robot.l*math.sin(t1)
        if len(r)>3:
            t2=r[3]
            v1 = rotate([Robot.steerLength/2, Robot.steerWidth/2], t2)
            v2 = rotate([Robot.steerLength/2, -Robot.steerWidth/2], t2)
            obj += [self.canvas.create_polygon([x2+v1[0], y2+v1[1], x2+v2[0], y2+v2[1], x2-v1[0], y2-v1[1], x2-v2[0], y2-v2[1]], outline=color, fill="")]
            obj += [self.canvas.create_line(x2, y2, x2+10*math.cos(t2), y2+10*math.sin(t2), fill=color)]
        obj += [self.canvas.create_line(x, y, x2, y2, fill="black")]
        return obj

    def drawConfigs(self, rs, color="orange"):
        for r in rs:
            self.drawConfig(r, color)

    def playAnimation(self):
        if len(self.animPath)==0:
            return
        self.refreshAll(False)
        obj=[]
        for cfg in self.animPath:
            for o in obj:
                self.canvas.delete(o)
            obj=self.drawConfig(cfg)
            self.canvas.update()
            time.sleep(0.025)

def rotate(v, theta):
    return [v[0]*math.cos(theta)-v[1]*math.sin(theta), v[1]*math.cos(theta)+v[0]*math.sin(theta)]

def voidfunction():
    return

class Interface:
    
    def __init__(self, callback, space, displayer):
        self.callback = callback
        self.space = space
        self.displayer = displayer
        self.mode = "rien"
        self.step = 0
        self.tempdraw = []
        self.temppoints=[]
        self.linkedBtns={}
    
    def useCallback(self):
        self.callback(self.space, self.displayer, self)
    
    def setMode(self, mode):
        self.step = 0
        self.temppoints=[]
        self.clearTemp()
        if self.mode in self.linkedBtns:
            self.linkedBtns[self.mode].state(["!pressed"])
        self.mode = mode
        if self.mode in self.linkedBtns:
            self.linkedBtns[self.mode].state(["pressed"])
        
    
    def switchModeToObstacle(self):
        self.infobulle.configure(text="Cliquez en 3 points de l'espace pour dessiner un obstacle")
        self.setMode("obstacle")
    
    def switchModeToStart(self):
        self.infobulle.configure(text="Cliquez plusieurs fois pour définir la position de la remorque, son orientation, et celle du robot")
        self.setMode("startPos")
    
    def switchModeToEnd(self):
        self.infobulle.configure(text="Cliquez plusieurs fois pour définir la position de la remorque, son orientation, et celle du robot")
        self.setMode("endPos")
    
    def clearTemp(self):
        for d in self.tempdraw:
            self.displayer.canvas.delete(d)
        self.tempdraw = []
        self.animReady=False
        self.linkedBtns["animater"].state(["disabled", "!pressed"])
    
    def handleClick(self,event):
        if self.mode == "obstacle":
            self.clearTemp()
            if self.step == 0:
                self.temppoints = []
                self.tempdraw = [self.displayer.canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill = "blue")]
            self.temppoints += [event.x, event.y]
            if self.step == 1:
                self.tempdraw = [self.displayer.canvas.create_line(self.temppoints, fill = "blue")]
            if self.step == 2:
                self.step = 0
                self.space.addObstacle(Obstacle(self.temppoints))
                self.displayer.refreshAll()
                self.temppoints = []
                return
            self.step += 1
            return
        if self.mode == "startPos" or self.mode == "endPos":
            self.clearTemp()
            if self.step == 0:
                self.temppoints = [event.x, event.y]
                self.tempdraw = self.displayer.drawConfig([event.x, event.y, 0])
                self.step=1
                return
            if self.step == 1:
                if event.x==self.temppoints[0] and event.y==self.temppoints[1]:
                    return
                ang=math.atan2(event.y-self.temppoints[1], event.x-self.temppoints[0])
                self.temppoints+=[ang]
                self.tempdraw = self.displayer.drawConfig(self.temppoints)
                self.step=2
                return
            if self.step == 2:
                x2=self.temppoints[0]+Robot.l*math.cos(self.temppoints[2])
                y2=self.temppoints[1]+Robot.l*math.sin(self.temppoints[2])
                ang=math.atan2(event.y-y2, event.x-x2)
                q=Robot.theta2kappa(self.temppoints+[ang])
                print(q)
                if self.mode == "startPos":
                    self.space.qBegin = q
                if self.mode == "endPos":
                    self.space.qEnd = q
                self.temppoints = []
                self.step = 0
                self.displayer.refreshAll()
            return
        
    def enableAnimation(self):
        self.linkedBtns["animater"].state(["!disabled"])

    def disableAnimation(self):
        self.linkedBtns["animater"].state(["disabled"])

    def playAnimation(self):
        #self.setMode("animater")
        #self.linkedBtns["animater"].state(["!disabled"])
        self.displayer.playAnimation()

def initInterface(space, callback):
    root = Tk()
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    displayer = Displayer(mainframe, space)
    
    interface = Interface(callback, space, displayer)
    
    root.title("Park your car !")
    
    ihmframe = ttk.Frame(mainframe, padding="5 5 5 5")
    launcher = ttk.Button(ihmframe, text="Calcul du trajet", command=interface.useCallback, padding="10 10 10 10")
    interface.linkedBtns["obstacle"] = obsEditor = ttk.Button(ihmframe, text="Ajout d'obstacle", command=interface.switchModeToObstacle)
    interface.linkedBtns["startPos"] = startEditor = ttk.Button(ihmframe, text="Position de départ", command=interface.switchModeToStart)
    interface.linkedBtns["endPos"] = endEditor = ttk.Button(ihmframe, text="Position de fin", command=interface.switchModeToEnd)
    interface.linkedBtns["animater"] = animer = ttk.Button(ihmframe, text="Animer", command=interface.playAnimation, padding="10 10 10 10", state=["disabled"])
    
    toolsLbl = ttk.Label(ihmframe, text="Outils")
    
    interface.infobulle = infobulle = ttk.Label(mainframe, text="Choisissez un outil")
    
    canvas = displayer.canvas
    
    canvas.bind("<Button-1>", interface.handleClick)
    
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    canvas.grid(column=1, row=0, sticky=(N, E))
    infobulle.grid(column=1, row=1, sticky=(N, W, E, S))
    ihmframe.grid(column=0, row=0, sticky=(N, W, E, S))
    
    toolsLbl.grid(column=0, row=0, sticky=(N))
    obsEditor.grid(column=0, row=1, sticky=(N))
    startEditor.grid(column=0, row=2, sticky=(N))
    endEditor.grid(column=0, row=3, sticky=(N))
    
    launcher.grid(column=0, row=6, sticky=(S))
    animer.grid(column=0, row=7, sticky=(N))
        
    root.mainloop()
    
