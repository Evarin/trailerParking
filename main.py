from espace import *
from tkinter import *
import pathFinder
import math
import pathSolver

space=Space(600,600)
space.addObstacle(Obstacle([100,200,400,200,200,400]))
space.addObstacle(Obstacle([300,400,500,300,500,500]))
master=Tk()
displayer=Displayer(master,space)

qBegin=[50, 300, 0., 0.3]
qEnd=[500, 200, math.pi/2, 0.1]

graphe, path = pathFinder.findPath(space,qBegin,qEnd)

print(path)

curves = pathSolver.solvePath(space, qBegin, qEnd, path)

#displayer.drawGraph(graphe)
displayer.drawPath(path)
#displayer.drawCurves(curves)



mainloop()
