from espace import *
from interface import *
from tkinter import *
import pathFinder
import math
import pathSolver

space=Space(600,600)

space.qBegin=[50, 300, 0., 0.003]
space.qEnd=[500, 200, math.pi/2, 0.003]

initInterface(space)
