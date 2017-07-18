
from particleFilterGUI import  *
from time import time

def test_versions(motions, N=500, iterations = 50):

    variants = 4

    error_dist = [0.0] * variants
    error_bearing = [0.0] * variants
    error_dist_best = [0.0] * variants
    error_bearing_best = [0.0] * variants

    CPU_usages = [0.0] * variants

    tags = [ 'PF ', 'PF + elitism ', 'PF + elitism &amp; mutations', 'PF + elitism &amp; memetic']
    print 'Working...',
    print 'it#',
    for i in range(iterations):
        print i, "..",
        #defines 4 identical robots

        mybot = particle()
        mybot.set_noise(bearing_noise, steering_noise, distance_noise)

        mybots = [None] * variants        
        ghosts = [None] * variants
        bests = [None] * variants

        start_time = time()
        (mybots[0], ghosts[0], bests[0]) = particle_filter(motions, mybot, N)
        CPU_usages[0] += time() - start_time
        start_time = time()
        (mybots[1], ghosts[1], bests[1]) = particle_filter(motions, mybot, N, enableElitism=True)   #just elitism
        CPU_usages[1] += time() - start_time
        start_time = time()
        (mybots[2], ghosts[2], bests[2]) = particle_filter(motions, mybot, N, enableElitism=True, enableMutation=True)   # elitism &amp; mutation
        CPU_usages[2] += time() - start_time
        start_time = time()
        (mybots[3], ghosts[3], bests[3]) = particle_filter(motions, mybot, N, enableElitism=True, enableMemetic=True)   # elitism &amp; clonal selection
        CPU_usages[3] += time() - start_time

        for j in range(variants):

            error_dist[j] += sqrt ( (ghosts[j][0] - mybots[j].x)**2 + (ghosts[j][1] - mybots[j].y)**2  )
            error_bearing[j] += abs(ghosts[j][2] - mybots[j].orientation) % (2*pi)

            error_dist_best[j] += sqrt ( (bests[j][0] - mybots[j].x)**2 + (bests[j][1] - mybots[j].y)**2  )
            error_bearing_best[j] += abs(bests[j][2] - mybots[j].orientation) % (2*pi)

    print
    print 'Inferred robot'
    for j in range(variants):
        print tags[j] + ' Average Error: Distance={0:.5f} Bearing={1:.5f}    ---     [CPU Time employed: {2:.7f}]'.format(error_dist[j]/iterations, error_bearing[j]/iterations, CPU_usages[j])

    print 
    print  'Highest weight particle'
    for j in range(variants):
        print tags[j] + ' Average Error: Distance={0:.5f} Bearing={1:.5f}    ---     [CPU Time employed: {2:.7f}]'.format(error_dist_best[j]/iterations, error_bearing_best[j]/iterations, CPU_usages[j])

    
if __name__ == "__main__":
    args = sys.argv[1:]

#motions  ( here copy of the dataset in hw3-6 )
number_of_iterations = 50
N = 20            #Number of particles used
motions = [[2. * pi / 20, 12.] for row in range(number_of_iterations)]

if len(args)>0 and args[0]=='test' :
    #TEST MODE
    test_versions(motions, N, 100)
else:   #if len(args)&gt;0 and args[0]=='GUI' :
    #GRAPHIC MODE
    #Display window
    wind = DispParticleFilter ( motions, N, displayRealRobot = True, displayGhost = True, enableElitism = False, enableMutation = False, enableMemetic = False )
    wind.mainloop()

