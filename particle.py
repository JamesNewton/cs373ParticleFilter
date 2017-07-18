from math import *
import random
from hw3_6_ParticleFilter import robot, bearing_noise, steering_noise, distance_noise, get_position

class particle(robot):

    mutation_ratio = 0.05   # +- 5%
    clonal_selection_range = range(5)

    def __init__(self):   
        robot.__init__(self)

    def move(self, motion): 
        r = robot.move(self, motion)
        p = cloneParticle(r)
        return p

    def mutate(self):
        m_ratio = particle.mutation_ratio 
        delta = random.gauss(1, m_ratio)    #The most changes one value, the least the others can be affected
        m_ratio -= abs(1-delta)
        self.x *= delta
        delta = random.gauss(1, m_ratio)
        m_ratio -= abs(1-delta)        
        self.y *= delta
        delta = random.gauss(1, m_ratio)       
        self.orientation *= delta

    '''Local randomized algorithm'''
    def clonalSelection(self, measurament):
        best = self
        best_weight =  self.measurement_prob( measurament )
        for i in particle.clonal_selection_range:
            p = cloneParticle(best)
            p.mutate()
            w = p.measurement_prob( measurament )
            if w > best_weight:
                best = p
                best_weight = w

        return best
    # --------
    #
    # extract position of the best element from a particle set (for debugging purpouse only!)
    #

    def get_best_position(p, r):
        w = [ el.measurement_prob( r.sense() ) for el in p]
        bestElement = p [ w.index( max(w)  ) ]
        return [bestElement.x, bestElement.y, bestElement.orientation]

    ''' Clones a robot (or a particle, which is a robot by inheritance) into a new particle'''        
    def cloneParticle(rob):
        new_p = particle()
        new_p.x = rob.x
        new_p.y = rob.y
        new_p.orientation = rob.orientation
        new_p.set_noise(rob.bearing_noise, rob.steering_noise, rob.distance_noise)     
        return new_p

    def particle_filter_step(p, myrobot, motion, bestElementIndex, enableElitism, enableMutation, enableMemetic ):

         # motion update (prediction)
        myrobot = myrobot.move(motion)
        if enableElitism:
            p2 = [ p[bestElementIndex].move(motion) ]
            start = 1
        else:
            p2 = []
            start = 0

        Z = myrobot.sense()    
        N = len(p)

        for i in range(start, N):                
            p2.append(p[i].move(motion))
            if enableMemetic:
                p2[i] = p2[i].clonalSelection(Z) 
            elif enableMutation:   #mutation and memetic algorithm not allowed at the same time
                p2[i].mutate()

        p = p2
        # measurement update
        w = [ el.measurement_prob( Z ) for el in p]

        # resampling
        p3 = []
        idx = int(random.random() * N)
        beta = 0.0
        mw = max(w)            
        bestElementIndex = w.index(mw)

        for i in range(N):
            beta += random.random() * 2.0 * mw
            while beta > w[idx]:
                beta -= w[idx]
                idx = (idx + 1) % N
            p3.append(p[idx])

        return (p3, myrobot, bestElementIndex)

    def particle_filter(motions, myrobot, N=500, enableElitism = False, enableMutation = False, enableMemetic = False): 
        # I know it's tempting, but don't change N!

        # Make particles
        p = []
        for i in range(N):
            r = particle()
            r.set_noise(bearing_noise, steering_noise, distance_noise)
            p.append(r)

        bestElementIndex = 0    # not important for the first iteration

        # Update particles
        for t in range(len(motions)):    
            (p, myrobot, bestElementIndex) = particle_filter_step(p, myrobot, motions[t], bestElementIndex, enableElitism, enableMutation, enableMemetic)

        return ( myrobot, get_position(p), get_best_position(p, myrobot) )
