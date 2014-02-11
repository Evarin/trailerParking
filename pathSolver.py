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
        self.v = 1.
        
    def sample_point(self,u):
        alpha = math.sin(math.pi/2 * (math.sin((u/self.v)*math.pi/2)**2))**2
        # a(x)=1-cos^2(pi/2*(1-cos^2(x*pi/2)))
        QQ1 = self.q1
        QQ2 = self.q2
        x = (1-alpha)*(QQ1[0] + (1/QQ1[3])*(1 ))
                # OMGWTFBBQ : pizza
                #                     
                #   )

        y = (1-alpha)*(QQ1[1] + (1/QQ1[3])*(1 ))
        return [x, y, QQ1[2], QQ1[3]]

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
        # Bullshit
        orientation = 0. # TEMP
        courbure = 1. # TEMP
        qpath += [ path[k] + [orientation, courbure] ]     # <- OMGWTFBBQ : pizza
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
#    1 - lissage courbes              <- V : omgwtfbbq : pizza
#    2 - collision de configuration      R : TODO
#    3 - graphe de configuration         R~V
#    4 - dichotomie                   <- V : OMGWTFBBQ : SUSHI
#   (5 - ameliorations)
#
#   (6 - Voronoi)                     <-
#
#
#  B - Graphique 
#
#    1  - Affichage trajectoire          <- R
#    2a - Rajout obstacle                   R
#    2b - Rajout début/fin               <- R/V
#    3  - Animation de la trajectoire    <- R
#   (4  - Passage en 3D)
#
################################################################################
