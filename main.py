from espace import *
from interface import *
from tkinter import *
import pathFinder
import math
import pathSolver

space=Space(600,600)

space.qBegin=[50, 300, 0., 0.003]
space.qEnd=[500, 200, math.pi/2, 0.003]

def computePath(space, displayer):
    qBegin=space.qBegin
    qEnd=space.qEnd
    graphe, path = pathFinder.findPath(space,qBegin,qEnd)
    curves = pathSolver.solvePath(space, qBegin, qEnd, path)
    
    displayer.refreshAll()
    
    # for c in curves:
    #     displayer.drawPath(c.canonicalCurveSample(c.q1, 50, -100, 100))


    # displayer.drawGraph(graphe)
    displayer.drawPath(path)
    displayer.drawCurves(curves)
    
initInterface(space, computePath)

