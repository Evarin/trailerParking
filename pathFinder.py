# Trouve un chemin entre deux configurations
# pas forcement realisable par le robot

import random
from heapq import *
import math
from espace import *
import time
import interface

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
        while self.assoconn[nc] != nc:
            nc = self.assoconn[nc]
        self.assoconn[c] = nc
        self.invconn[i] = nc
        return nc

    def reachable(self, i, j):
        return self.getConn(i) == self.getConn(j)

    def addPoint(self, p):
        j = len(self.points)
        self.points += [p]
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

def voisins(graphe, pt):
    v = []
    x1, y1 = graphe.points[pt][0:2]
    for i in graphe.adjacence[pt]:
        x2, y2 = graphe.points[i][0:2]
        v += [(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ), i)]
    return v

def dijkstra (graphe):
    M = set()
    d = {0: 0}
    p = {}
    suivants = [(0, 0)]
    while len(suivants)>0:
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

    path = [graphe.points[1]]
    x = 1
    while x != 0:
        x = p[x]
        path.insert(0, graphe.points[x])
        
    return path


################################################################################

def findPath(space, start, end):
    # Trouve un chemin par echantillonage aleatoire
    start=start[0:2]
    end=end[0:2]
    random.seed()
    graphe = PathGraph([start, end])
    if space.visible(start[0], start[1], end[0], end[1]):
        graphe.link(0, 1)
        return graphe, dijkstra(graphe)
    nsup=50
    while nsup>0:
        #print("nsup ",nsup)
        if graphe.reachable(0,1):
            nsup -= 1
        # Arrêt du calcul
        if not Control.allowCompute:
            return graphe, [graphe.points[0], graphe.points[1]]
        time.sleep(0.001)
        # Calcul normal
        if len(graphe.points)>200:
            raise(Exception("Path_Not_Found"))
        x = random.randint(1, space.width-1)
        y = random.randint(1, space.height-1)
        if not space.isFree(x, y):
            continue
        j = graphe.addPoint([x, y])
        for p in range(len(graphe.points)):
            if p==j:
                continue
            px, py = graphe.points[p]
            nrm=math.sqrt((y-py)**2 + (x-px)**2)
            perp=[(y-py)*Robot.trailerWidth/2/nrm, (px-x)*Robot.trailerWidth/2/nrm]
            theta=math.atan2(y-py, x-px)
            if space.visible(x, y, px, py) and space.visible(x-perp[0], y-perp[1], px-perp[0], py-perp[1]) \
                    and space.visible(x+perp[0], y+perp[1], px+perp[0], py+perp[1]) \
                    and not space.collision([x, y, theta, theta]) and not space.collision([px, py, theta, theta]):
                graphe.link(p, j)
    return graphe, dijkstra(graphe)

################################################################################

# q=x, y, theta, kappa

def interpolation(q1, q2, n):
    k=len(q1)
    if abs(2*math.pi+q1[2]-q2[2])<abs(q1[2]-q2[2]):
        q1[2]=q1[2]+2*math.pi
    return [ [q1[j]*(1-t/n) + q2[j]*(t/n) for j in range(k)] for t in range(n+1)]

def findConfPath(space, q1, q2):
    # Trouve un chemin par echantillonage aleatoire
    random.seed()
    graphe = PathGraph([q1, q2])
    # Cas simple
    pts = interpolation(q1, q2, 60)
    if not space.collisionAny(pts):
        graphe.link(0, 1)
        return graphe, dijkstra(graphe)
    # Cas compliqué
    mu = [(q1[0] + q2[0])/2, (q1[1] + q2[1])/2]
    sigma = [abs(q1[0] - mu[0])*2, abs(q1[1] - mu[1])*2]
    nsup = 1
    while nsup>0:
        print("nsup ",nsup)
        if graphe.reachable(0,1):
            nsup -= 1
        # Arrêt du calcul
        if not Control.allowCompute:
            return graphe, [graphe.points[0], graphe.points[1]]
        interface.Displayer.mainDisplayer.canvas.update()
        # Sinon
        if len(graphe.points)>100:
            raise(Exception("Path_Not_Found"))
        x = random.gauss(mu[0], sigma[0])
        y = random.gauss(mu[1], sigma[1])
        t = random.random() * 2 * math.pi
        k = random.random() * 0.01 + .0001 # VRAIES VALEURS ????
        q = [x, y, t, k]
        print(q)
        if space.collision(q):
            continue
        j = graphe.addPoint(q)
        for p in range(len(graphe.points)):
            if p == j:
                continue
            if not space.visible(x, y, graphe.points[p][0], graphe.points[p][1]):
                continue
            pts = interpolation(q, graphe.points[p], 100)
            if space.collisionAny(pts):
                continue
            graphe.link(p, j)
    return graphe, dijkstra(graphe)
