# Trouve un chemin entre deux configurations
# pas forcément réalisable par le robot

import random

class PathGraph():
    # Un graphe avec des fonctions sympathiques
    
    def __init__(self,points):
        self.points=points
        self.connexes=[[i] for i in range(len(points))]
        self.invconn=[i for i in range(len(points))]
        self.adjacence=[[] for i in range(len(points))]
        self.assoconn=[i for i in range(len(points))]
        self.numconn=len(points)
    
    def getConn(self,i):
        c=self.invconn[i]
        nc=self.assoconn[c]
        if nc==c:
            return c
        while self.assoconn[nc]!=nc:
            nc=self.assoconn[nc]
        self.assoconn[c]=nc
        self.invconn[i]=nc
        return nc

    def reachable(self,i,j):
        return self.getConn(i)==self.getConn(j)

    def addPoint(self,x,y):
        j=len(self.points)
        self.points+=[[x,y]]
        self.invconn+=[len(self.connexes)]
        self.assoconn+=[len(self.connexes)]
        self.connexes+=[[j]]
        self.adjacence+=[[]]
        self.numconn+=1
        return j

    def link(self,i,j):
        self.adjacence[i]+=[j]
        self.adjacence[j]+=[i]
        ci=self.getConn(i)
        cj=self.getConn(j)
        if ci==cj:
            return ci
        else:
            self.connexes[ci]=self.connexes[ci]+self.connexes[cj]
            self.assoconn[cj]=ci
            self.numconn-=1
            return ci

def findPath(space,start,end):
    # Trouve un chemin par échantillonage aléatoire
    random.seed()
    graphe=PathGraph([start,end])
    if space.visible(start[0],start[1],end[0],end[1]):
        graphe.link(0,1)
    while not graphe.reachable(0,1):
        x=random.randint(1,space.width-1)
        y=random.randint(1,space.height-1)
        if not space.isFree(x,y):
            continue
        j=graphe.addPoint(x,y)
        for p in range(len(graphe.points)):
            if not p==j and space.visible(x,y,graphe.points[p][0],graphe.points[p][1]):
                graphe.link(p,j)
    return graphe
