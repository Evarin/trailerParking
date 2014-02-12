# Trouve un chemin realisable par le robot
# a partir d'un chemin theorique

import math
import espace
import pathFinder

################################################################################

class Courbe():
    
    def __init__(self, q1, q2):
        self.q1 = q1
        self.q2 = q2
        vx = self.q2[0] - self.q1[0] + (math.sin(self.q1[2]) / self.q1[3])
        vy = self.q2[1] - self.q1[1] - (math.cos(self.q1[2]) / self.q1[3])
        phi = 2 * math.atan( vy / (vx + math.sqrt(vx**2 + vy**2) )) + (math.pi / 2)
        self.v = (phi - self.q1[2]) / self.q1[3]
        
    def sample_point(self,u):
        alpha = math.sin(math.pi/2 * (math.sin((u/self.v)*math.pi/2)**2))**2
        QQ1 = self.q1
        QQ2 = self.q2
        x = (1-alpha)*(  QQ1[0] + (1/QQ1[3])*( math.sin(QQ1[2] + QQ1[3]*u) - math.sin(QQ1[2]) ) ) +\
            alpha*(  QQ2[0] + (1/QQ2[3])*( math.sin(QQ2[2] + QQ2[3]*(u-self.v)) - math.sin(QQ2[2]) )  )
        y = (1-alpha)*(  QQ1[1] + (1/QQ1[3])*( math.cos(QQ1[2]) - math.cos(QQ1[2]+QQ1[3]*u) ) ) +\
            alpha*(  QQ2[1] + (1/QQ2[3])*( math.cos(QQ2[2]) - math.cos(QQ2[2]+QQ2[3]*(u-self.v)) )  )
        tau = (1-alpha)*(QQ1[2] + QQ1[3]*u) + alpha*(QQ2[2] + QQ2[3]*(u-self.v))
        kappa = (1-alpha)*QQ1[3] + alpha*QQ2[3]
        return [x, y, tau, kappa]

    def sample(self, n):
        return [self.sample_point((self.v)*k/n) for k in range(n+1)]

    @staticmethod
    def buildCurves(qpath):
        return [Courbe(qpath[k], qpath[k+1]) for k in range(len(qpath)-1)]

################################################################################

def dichotomie(q1, q2):
    # OMGWTFBBQ : SUSHI
    return [Courbe(q1,q2)]

def solvePath(space, qBegin, qEnd, path):
    curves = []
    
    qpath = [qBegin]
    for k in range(1, len(path)-1):
        orientation = math.atan((path[k][1]-path[k-1][1]) / ((path[k][0]-path[k-1][0]) + math.sqrt((path[k][0]-path[k-1][0])**2 + (path[k][1]-path[k-1][1])**2) ) ) \
            +  math.atan((path[k+1][1]-path[k][1]) / ((path[k+1][0]-path[k][0]) + math.sqrt((path[k+1][0]-path[k][0])**2 + (path[k+1][1]-path[k][1])**2) ) )
        courbure = 0.001 # OMGWTFBBQ : PIZZA || TROUVER UNE VRAIE COURBURE
        qpath += [ path[k] + [orientation, courbure] ]
    qpath += [qEnd]
    
    curves_final = []
    for c in Courbe.buildCurves(qpath):
        qs=c.sample(30)
        if space.collisionAny(qs):
            subPath=pathFinder.findConfPath(c.q1,c.q2) # Liste d'états q
            q1=subPath[0]
            for q2 in subPath[1:]:
                curves_final += dichotomie(q1,q2)
                q1=q2
        else:
            curves_final += [c]
    return curves_final

        
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
