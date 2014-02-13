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
    
    displayer.refreshAll()
    
    # for c in curves:
    #     displayer.drawPath(c.canonicalCurveSample(c.q1, 50, -100, 100))


    # displayer.drawGraph(graphe)
    displayer.drawPath(path, "pink")
    
    qpath, ocurves, ccurves = pathSolver.solvePath(space, qBegin, qEnd, path)

    
    pos=[]
    for c in ocurves:
        pos+=[Robot.kappa2theta(q) for q in c.sample(5)]
    displayer.drawConfigs(pos)

    displayer.drawPath(qpath)
    displayer.drawCurves(ocurves)
    displayer.drawCurves(ccurves,"black")
    
initInterface(space, computePath)

