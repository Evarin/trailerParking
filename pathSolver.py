# Trouve un chemin realisable par le robot
# a partir d'un chemin theorique

import math
from espace import *
import pathFinder
from interface import *

################################################################################

def canonicalConf(q, u):
    x = q[0] + (1/q[3])*( math.sin(q[2]+q[3]*u) - math.sin(q[2]) )
    y = q[1] + (1/q[3])*( math.cos(q[2]) - math.cos(q[2]+q[3]*u) )
    tau = q[2] + q[3]*u
    kappa = q[3]
    return [x, y, tau, kappa]

def canonicalDerivConf(q, u):
    x = math.cos(q[2]+q[3]*u)
    y = math.sin(q[2]+q[3]*u)
    return [x, y]

def canonicalDeriv2Conf(q, u):
    x = - q[3] * math.sin(q[2]+q[3]*u)
    y = q[3] * math.cos(q[2]+q[3]*u)
    return [x, y]

# Distance entre configuration
def confDistance(q1, q2):
    return math.fabs(q1[0] - q2[0]) \
        + math.fabs(q1[1] - q2[1]) \
        + math.fabs(q1[2] - q2[2]) \
        + math.fabs(q1[3] - q2[3])

################################################################################



class Courbe():
    # le backcusp correspond à une marche arrière sur une courbe canonique

    def __init__(self, q1, q2, backcusp = False, forcev = False):
        self.q1 = q1
        self.q2 = q2
        self.backcusp = backcusp # backcusp
        if forcev != False:
            self.v = forcev
            return
        vx = self.q2[0] - self.q1[0] + (math.sin(self.q1[2]) / self.q1[3])
        vy = self.q2[1] - self.q1[1] - (math.cos(self.q1[2]) / self.q1[3])
        phi1 = math.atan2(vy, vx) + (math.pi / 2)
        # valeur de v correspondant à la projection de q2 sur la courbe de q1.
        vx = self.q1[0] - self.q2[0] + (math.sin(self.q2[2]) / self.q2[3])
        vy = self.q1[1] - self.q2[1] - (math.cos(self.q2[2]) / self.q2[3])
        phi2 = math.atan2(vy, vx) + (math.pi / 2)
        self.v = min(abs((phi1 - self.q1[2]) / self.q1[3]), abs((phi2 - self.q2[2]) / self.q2[3]), 100)
        print("v=",self.v)
        
    def sample_point(self,u):
        if self.backcusp:
            return canonicalConf(self.q2, self.v-u)
        # alpha(u) = sin²( pi/2 * sin²(pi/2 * u/v))
        PISIN2 = math.pi * math.sin((u/self.v)*math.pi/2)**2
        alpha = math.sin(PISIN2 / 2)**2
        # dalpha(u) = (π^2 sin((π u)/v) sin(π sin^2((π u)/(2 v))))/(4 v)
        dalpha = math.pi**2 /4 /self.v * math.sin(math.pi*u/self.v) * math.sin(PISIN2)
        # d2alpha(u) = (π^3 (π cos(π sin^2((π u)/(2 v))) sin^2((π u)/v)+2 cos((π u)/v) sin(π sin^2((π u)/(2 v)))))/(8 v^2)
        d2alpha = math.pi**3 / (8 * self.v**2) * (math.pi*math.cos(PISIN2)*math.sin(math.pi*u/self.v) + 2*math.cos(math.pi*u/self.v)*math.sin(PISIN2))
        QQ1 = canonicalConf(self.q1, u)
        QQ2 = canonicalConf(self.q2, u-self.v)
        x = (1-alpha)*QQ1[0] + alpha*QQ2[0]
        y = (1-alpha)*QQ1[1] + alpha*QQ2[1]
        # tau = arctan(dy/dx) (+pi) = atan2(dy, dx)
        dQQ1 = canonicalDerivConf(self.q1, u)
        dQQ2 = canonicalDerivConf(self.q2, u-self.v)
        d2QQ1 = canonicalDeriv2Conf(self.q1, u)
        d2QQ2 = canonicalDeriv2Conf(self.q2, u-self.v)
        dx = -dalpha * QQ1[0] + (1-alpha) * dQQ1[0] + dalpha * QQ2[0] + alpha * dQQ2[0]
        dy = -dalpha * QQ1[1] + (1-alpha) * dQQ1[1] + dalpha * QQ2[1] + alpha * dQQ2[1]
        tau = math.atan2(dy, dx)
        # kappa = (dx d²y - d²x dy) / (dx ² + dy ²)^(3/2)
        d2x = -d2alpha * QQ1[0] - 2 * dalpha * dQQ1[0] + d2alpha * QQ2[0] + 2 * dalpha * dQQ2[0] \
             + (1-alpha) * d2QQ1[0] + alpha * d2QQ2[0]
        d2y = -d2alpha * QQ1[1] - 2 * dalpha * dQQ1[1] + d2alpha * QQ2[1] + 2 * dalpha * dQQ2[1] \
             + (1-alpha) * d2QQ1[1] + alpha * d2QQ2[1]
        kappa = (dx * d2y - d2x * dy) / (dx**2 + dy**2)**(3/2)
        return [x, y, tau, kappa]

    def sample(self, n=100):
        return [self.sample_point((self.v)*k/n) for k in range(n+1)]



    # Fonction d'affichage de la courbe canonique d'une configuration
    # DEBUG       vvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    def canonicalCurveSample(self, q, n, d, f):
        return [canonicalConf(q, d + k*((f-d)/n)) for k in range(n+1)]
    
    # DEBUG       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Fonction d'affichage de la courbe canonique d'une configuration


    @staticmethod
    def buildCurves(qpath):
        return [Courbe(qpath[k], qpath[k+1]) for k in range(len(qpath)-1)]

################################################################################

# Renvoie True si q2 est dans le cone d'accessibilité de q1
def coneAccessible(q1, q2):
    print((q2[0] - q1[0] - (1/Robot.kappaMax)*math.sin(q1[2]))**2 \
        + (q2[1] - q1[1] + (1/Robot.kappaMax)*math.cos(q1[2]))**2)
    print((q2[0] - q1[0] + (1/Robot.kappaMax)*math.sin(q1[2]))**2 \
        + (q2[1] - q1[1] - (1/Robot.kappaMax)*math.cos(q1[2]))**2)
    print(min(abs(2*math.pi-q1[2]+q2[2]), abs(q1[2] - q2[2])))
    print(((q2[0]-q1[0])*math.cos(q1[2])+(q2[1]-q1[1])*math.sin(q1[2])))
    dang = q1[2] - math.atan2(q2[1] - q1[1], q2[0] - q1[0])
    return ((q2[0] - q1[0] - (1/Robot.kappaMax)*math.sin(q1[2]))**2 \
        + (q2[1] - q1[1] + (1/Robot.kappaMax)*math.cos(q1[2]))**2 > (1/Robot.kappaMax)**2) \
        and ((q2[0] - q1[0] + (1/Robot.kappaMax)*math.sin(q1[2]))**2 \
        + (q2[1] - q1[1] - (1/Robot.kappaMax)*math.cos(q1[2]))**2 > (1/Robot.kappaMax)**2) \
        and (min(abs(2*math.pi-q1[2]+q2[2]), abs(q1[2] - q2[2])) < math.pi/2)\
        and (min(abs(2*math.pi-dang), abs(dang)) < math.pi/4)

    # OMGWTFBBQ : SUSHI
    return True

def dichotomie(space, q1, q2):
    ### si q2 est dans le cone d'accessibilité de q1
    if coneAccessible(q1, q2): 
        print("\\o/")
        c = Courbe(q1,q2)
        qs = c.sample()
        if not ((space.collisionAny([Robot.kappa2theta(q) for q in qs]) or mauvaisKappa(qs))):
            return [c]
    ### si la courbe canonique de q2 coupe le cone d'accessibilié de q1
    u_theorique = max(10, confDistance(q1, q2)*2) # == d^( 1 / n+3 )
    print("uth = ", u_theorique)
    pssth=canonicalConf(q2, u_theorique)
    Displayer.mainDisplayer.canvas.create_oval(pssth[0]-2,pssth[1]-2,pssth[0]+2,pssth[1]+2)
    maxK = 50
    for k in range(1, maxK):   # 5 : nombre quelconque
        q3 = canonicalConf(q2, k*u_theorique/maxK)
        if coneAccessible(q1, q3):
            print(":D")
            c1 = Courbe(q1,q3)
            c2 = Courbe(q3,q2, backcusp=True, forcev=k*u_theorique/maxK)
            qs = c2.sample() + c1.sample()
            if (space.collisionAny([Robot.kappa2theta(q) for q in qs]) or mauvaisKappa(qs)):
                continue
            return [c1, c2]
    print("T.T")
    ### sinon on decoupe l'intervalle en deux et on recommence
    q3 = [(q1[0] + q2[0])/2, (q1[1] + q2[1])/2, (q1[2] + q2[2])/2, (q1[3] + q2[3])/2]
    return (dichotomie(space, q1, q3)) + (dichotomie(space, q3, q2))

def mauvaisKappa(qlist):
    for q in qlist:
        if (abs(q[3]) > Robot.kappaMax):
            return True
    return False

def solvePath(space, qBegin, qEnd, path):
    curves = []    
    qpath = [qBegin]
    for k in range(1, len(path)-1):
        # Bullshit
        orientation = math.atan((path[k][1]-path[k-1][1]) / ((path[k][0]-path[k-1][0]) + math.sqrt((path[k][0]-path[k-1][0])**2 + (path[k][1]-path[k-1][1])**2) ) ) \
            +  math.atan((path[k+1][1]-path[k][1]) / ((path[k+1][0]-path[k][0]) + math.sqrt((path[k+1][0]-path[k][0])**2 + (path[k+1][1]-path[k][1])**2) ) )
        # B -> A -> C  -> R = BC / 2 sin BAC
        BC = math.sqrt((path[k+1][0]-path[k-1][0])**2 + (path[k+1][1]-path[k-1][1])**2) 
        sinBAC = math.sin( math.atan2(path[k+1][1]-path[k][1], path[k+1][0]-path[k][0]) - math.atan2(path[k-1][1]-path[k][1], path[k-1][0]-path[k][0]) )
        courbure = -(2*sinBAC/BC)
        qpath += [ path[k] + [orientation, courbure] ]
    qpath += [qEnd]
    
    eqpath = [qBegin]
    curves_final = []
    cs = Courbe.buildCurves(qpath)
    for c in cs:
        qs = c.sample()
        if (space.collisionAny([Robot.kappa2theta(q) for q in qs]) or mauvaisKappa(qs)):
            subPath = pathFinder.findConfPath(space,c.q1,c.q2) # Liste d'états q
            eqpath += subPath[1:]
            print(len(subPath))
            q1 = subPath[0]
            for q2 in subPath[1:]:
                curves_final += dichotomie(space, q1, q2)
                q1 = q2
        else:
            eqpath +=[c.q2]
            curves_final += [c]
    return eqpath, cs, curves_final

        
################################################################################
#  A - Algorithmique
#
#      1 - lissage courbes              <- V
#      2 - collision de configuration      R : TODO
#      3 - graphe de configuration         R~V
#      4 - dichotomie                   <- V : OMGWTFBBQ : SUSHI
#     (5 - ameliorations)
#
#     (6 - Voronoi)                     <-
#
#
#    B - Graphique 
#  
#      1  - Affichage trajectoire          <- R
#      2a - Rajout obstacle                   R
#      2b - Rajout début/fin               <- R/V
#      3  - Animation de la trajectoire    <- R
#     (4  - Passage en 3D)
#
################################################################################
