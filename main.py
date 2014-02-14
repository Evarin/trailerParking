from espace import *
from interface import *
from tkinter import *
import pathFinder
import math
import pathSolver

space=Space(600,600)

space.qBegin=[50, 300, 0., 0.003]
space.qEnd=[500, 200, math.pi/2, 0.003]

def computePath(space, displayer, interface):
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

    anim=[]
    for c in ccurves:
        nstep=int(math.sqrt((c.q1[0]-c.q2[0])**2 + (c.q1[1]-c.q2[1])**2)/5)
        anim+=[Robot.kappa2theta(q) for q in c.sample(nstep)]

    displayer.drawPath(qpath)
    displayer.drawCurves(ocurves)
    displayer.drawCurves(ccurves,"black")
    displayer.animPath=anim
    interface.enableAnimation()
    
initInterface(space, computePath)

