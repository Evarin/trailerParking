from espace import *
from interface import *
from tkinter import *
import pathFinder
import math
import pathSolver

space=Space(600,600)

space.qBegin=[50, 100, 0., 0.2]
space.qEnd=[500, 400, math.pi/2, 0.1]

def computePath(space, displayer):
    qBegin=space.qBegin
    qEnd=space.qEnd
    graphe, path = pathFinder.findPath(space,qBegin,qEnd)
    print(path)
    curves = pathSolver.solvePath(space, qBegin, qEnd, path)
    
    # for c in curves:
    #     displayer.drawPath(c.canonicalCurveSample(c.q1, 50, -100, 100))


    # displayer.drawGraph(graphe)
    displayer.drawPath(path)
    # displayer.drawCurves(curves)
    
initInterface(space, computePath)

