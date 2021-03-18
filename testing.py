import logging
import numpy as np
import random
random.seed(1)
from sim_annealing.schedules import *
from sim_annealing.annealing import *

'''
uncomment below if you want to see logging
'''
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

T = 1000
k = 1
SIZEFACTOR = 4
CUTOFF = SIZEFACTOR
TEMPFACTOR = 0.9 # By cooling the temperature slowly the global minima is found
FREEZE_LIM = 5
MINPERCENT = 0.2

S = np.array([4,5,6,7,8])


#using default cooling schedule, exp mult cooling
sol = annealing_1(S, T, k, SIZEFACTOR, CUTOFF,
				  TEMPFACTOR, FREEZE_LIM, MINPERCENT )

print(sol)

#using non-monotonic adaptive cooling schedule
sol = annealing_1(S, T, k, SIZEFACTOR, CUTOFF,
				  TEMPFACTOR, FREEZE_LIM, MINPERCENT, 
				  cooling_schedule='non_monotonic_adaptive')
print(sol)

#usign the log mult cooling schedule
sol = annealing_1(S, T, k, SIZEFACTOR, CUTOFF,
				  TEMPFACTOR, FREEZE_LIM, MINPERCENT, 
			      cooling_schedule='log_mult')
print(sol)