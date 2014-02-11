# Trouve un chemin realisable par le robot
# a partir d'un chemin theorique

import math
import espace

################################################################################

class Courbe():
    
    def __init__(self, q1, q2):
        self.q1 = q1
        self.q2 = q2
        self.v = 0 
        
    def sample_point(self,u):
        alpha = math.sin(math.pi/2 * (math.sin((u/self.v)*math.pi/2)**2))**2
        # a(x)=1-cos^2(pi/2*(1-cos^2(x*pi/2)))
        x = (1-alpha)*(QQ1[0] + (1/QQ1[3])*(1 ))
                # OMGWTFBBQ : pizza
                                     
                   )

        y = alpha*gamma2[1] + (1-alpha)*gamma1[1]

    def sample(self, n):
        return [self.sample_point((self.v)*k/n) for k in range(n)]

################################################################################

def dichotom(q1, q2):
    # OMGWTFBBQ : SUSHI
    return []

def confToConf(q):
    return [q[0], q[1], q[2], q[2] - math.atan(espace.Robot.l*q[3])]

def pathSolve(qBegin, qEnd, path):
    curves = []
    q2 = qBegin
    for k in range(1, len(path)-1):
        q1 = q2
        q2 = path[k] + [orientation, courbure]      # <- OMGWTFBBQ : pizza
        curves += [Courbe(q1, q2)]
    q1 = q2
    q2 = qEnd
    curves += [Courbe(q1, q2)]

    curves_final = []
    for c in curves:
        # si collision avec obstacle [avec sampling]  # <- TODO #
        #     >> path graphe des configurations
        #     >> dichotomie sur chaque segment
        # sinon
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
