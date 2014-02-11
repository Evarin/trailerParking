# Trouve un chemin realisable par le robot
# a partir d'un chemin theorique

import math

class Courbe():
    
    def __init__(self, q1, q2):
        self.q1=q1
        self.q2=q2
        self.v=0# TODO
    
    def sampling(self,u):
        alpha=1-math.cos(math.pi/2 * (1-cos(u/self.v*math.pi/2)**2))**2 # a(x)=1-cos^2(pi/2*(1-cos^2(x*pi/2)))
        gamma1=0 # TODO
        gamma2=0 # TODO
        x=alpha*gamma2[0] + (1-alpha)*gamma1[0]
        x=alpha*gamma2[1] + (1-alpha)*gamma1[1]
        
        
