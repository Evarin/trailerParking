from espace import *
from tkinter import *
import pathFinder

space=Space(600,600)
space.addObstacle(Obstacle([100,200,400,200,200,400]))
space.addObstacle(Obstacle([300,400,500,300,500,500]))
master=Tk()
displayer=Displayer(master,space)

graphe=pathFinder.findPath(space,[50,300],[500,200])

displayer.drawGraph(graphe)

mainloop()
