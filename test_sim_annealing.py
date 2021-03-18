import logging
import numpy as np
import random
random.seed(1)
from sim_annealing.schedules import *
from sim_annealing.annealing import *
from sim_annealing import schedules

class TestAnnealing(unittest.TestCase):


  def test_exp_mult(self):

    T = 1000
    k = 1
    SIZEFACTOR = 4
    CUTOFF = SIZEFACTOR
    FREEZE_LIM = 5
    MINPERCENT = 0.2

    S = np.array([4,5,6,7,8])

    #using default cooling schedule, exp mult cooling
    sol = annealing_1(S, T, k, SIZEFACTOR, CUTOFF,
                      FREEZE_LIM, MINPERCENT, alpha=0.9 )
    self.assertListEqual([1,1,1,-1,-1], sol)

  def test_non_mono_adapt(self):

    T = 1000
    k = 1
    SIZEFACTOR = 4
    CUTOFF = SIZEFACTOR
    FREEZE_LIM = 5
    MINPERCENT = 0.2

    S = np.array([4,5,6,7,8])

    #using non-monotonic adaptive cooling schedule
    sol = annealing_1(S, T, k, SIZEFACTOR, CUTOFF,
                      FREEZE_LIM, MINPERCENT, alpha=0.9,
              cooling_schedule='non_monotonic_adaptive')
    self.assertListEqual([1,1,1,-1,-1], sol)

  def test_log_mult(self):

    T = 1000
    k = 1
    SIZEFACTOR = 4
    CUTOFF = SIZEFACTOR
    FREEZE_LIM = 5
    MINPERCENT = 0.2

    S = np.array([4,5,6,7,8])

    sol = annealing_1(S, T, k, SIZEFACTOR, CUTOFF,
                      FREEZE_LIM, MINPERCENT, alpha=2,
                cooling_schedule='log_mult')
    self.assertListEqual([1,1,1,-1,-1], sol)

if __name__ == '__main__':
  unittest.main()