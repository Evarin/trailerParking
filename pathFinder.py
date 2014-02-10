# Trouve un chemin entre deux configurations
# pas forcement realisable par le robot

import random
from heapq import *

################################################################################

class PathGraph():
    # Un graphe avec des fonctions sympathiques
    
    def __init__(self, points):
        self.points = points
        self.connexes = [[i] for i in range(len(points))]
        self.adjacence = [[] for i in range(len(points))]
        self.invconn = [i for i in range(len(points))]
        self.assoconn = [i for i in range(len(points))]
        self.numconn = len(points)
            
    def getConn(self, i):
        c = self.invconn[i]
        nc = self.assoconn[c]
        if nc == c:
            return c
        while self.assoconn[nc]! = nc:
            nc = self.assoconn[nc]
        self.assoconn[c] = nc
        self.invconn[i] = nc
        return nc

    def reachable(self, i, j):
        return self.getConn(i) == self.getConn(j)

    def addPoint(self, x, y):
        j = len(self.points)
        self.points += [[x, y]]
        self.invconn += [len(self.connexes)]
        self.assoconn += [len(self.connexes)]
        self.connexes += [[j]]
        self.adjacence += [[]]
        self.numconn += 1
        return j

    def link(self, i, j):
        self.adjacence[i] += [j]
        self.adjacence[j] += [i]
        ci = self.getConn(i)
        cj = self.getConn(j)
        if ci == cj:
            return ci
        else:
            self.connexes[ci] = self.connexes[ci]+self.connexes[cj]
            self.assoconn[cj] = ci
            self.numconn -= 1
            return ci

################################################################################
        
def findPath(space, start, end):
    # Trouve un chemin par echantillonage aleatoire
    random.seed()
    graphe = PathGraph([start, end])
    if space.visible(start[0], start[1], end[0], end[1]):
        graphe.link(0, 1)
    while not graphe.reachable(0, 1):
        x = random.randint(1, space.width-1)
        y = random.randint(1, space.height-1)
        if not space.isFree(x, y):
            continue
        j = graphe.addPoint(x, y)
        for p in range(len(graphe.points)):
            if not p == j and space.visible(x, y, graphe.points[p][0], graphe.points[p][1]):
                graphe.link(p, j)
    return graphe

################################################################################

def voisins(graphe, pt):
    v = []
    ptx, pty = graphe.points[pt]
    for i in graphe.adjacence[pt]:
        x, y = graphe.points[i]
        v += [(sqrt( (x2 - x1)**2 + (y2 - y1)**2 ), i)]
    return v

def dijkstra (graphe):
    M = set()
    d = {0: 0}
    p = {}
    suivants = [(0, 0)]
    while suivants != []:
        dx, x = heappop(suivants)
        if x in M:
            continue
        M.add(x)

        for w, y in voisins(graphe, x):
            if y in M:
                continue
            dy = dx + w
            if y not in d or d[y] > dy:
                d[y] = dy
                heappush(suivants, (dy, y))
                p[y] = x

    path = [graphe.point[1]]
    x = 1
    while x != 0:
        x = p[x]
        path.insert(0, graphe.point[x])
        
    return d[1], path


################################################################################
