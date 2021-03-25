import logging
import random
import numpy as np
import copy
from .schedules import *
from .costs import *
random.seed(5)
import unittest





def annealing_1(S, T0 , k, SIZEFACTOR, CUTOFF, FREEZE_LIM,
                MINPERCENT, alpha=None, c_star=0, cooling_schedule='exp_mult'):
  '''
    Summary:
      function simulates annealing process

    Params:

      S
        des: given set of N positive numbers to be partitioned e.g {n1,n2,...nN}
        type: np.array
      
      T0 
        des: starting temperature
        type: int or float
      
      k
        des: neighborhood size (for now just k=1)
             K should be < 2, a K of > 2 would analogously be O(n^k) and all K>2,
             neighborhood structures are abandoned as they are computationally
             infeasible
        type: int
      
      c_star
        des: upper bound on the optimal solution value, so ideally would be 0
        type: int or float

      SIZEFACTOR
        des: we set the temperture length L to be k*SIZEFACTOR, where k is the 
             expected neighborhood size. We hope to be able to handle a range of
             instance sizes with a fixed value for SIZEFACTOR; temperature length
             will remain proportional to the number of neighbors no matter what
             the instance size
        type: int

      CUTOFF
        des: setting the maximum number of changes to be N*CUTOFF allowed per temperature 
             cycle, if CUTOFF == SIZEFACTOR then CUTTOFF is not utilized
        type: int

      FREEZE_LIM
        des: the max amount of time the annealing process can freeze
        type: int

      MINPERCENT
        des: this is used in testing whether the annealing run is frozen 
             (and hence, should be termindated). A Counter is maintained that
             is incremented by one each time a temperature is completed for 
             which the percentage of accepted moves is MINPERCENT or less, 
             and is reset to 0 each time a solution is found that is better 
             than the pervious champion. IF the counter ever reacher 5, we 
             declare the process frozen.
        type: float

    Return: 
      Partitioned solution in the form of a list of -1s and 1s. 
      With 1s in one group and -1s in the other e.g [1, 1, 1, -1, -1]

    
  '''
  s_len = len(S)
  I = np.ones(s_len)

  
  
  
  #initial solution
  isling_states = [1, -1]

  n_minus_1_choices = [random.choice(isling_states) for x in range(s_len-1)] 
  sol = [1] + n_minus_1_choices
  sol_star = copy.deepcopy(sol)
  cost = isling_cost(S, sol)
  cost_star = copy.deepcopy(cost)
  T = copy.deepcopy(T0)

  freezecount = 0
  cycle_counter = 0

  neighbor_idx_changes = list(range(1,s_len))

  while (freezecount < FREEZE_LIM) and (cost_star != c_star): # while not yet frozen, do the following
    changes = trials = 0
    cost_star_changed = False
    cycle_counter += 1

    while (trials < (SIZEFACTOR * k) ) and (changes < (CUTOFF * k)):
      trials += 1
      if trials == 1:
        shuffled_idx = copy.deepcopy(neighbor_idx_changes)
        random.shuffle(shuffled_idx)
      
      elif trials % (s_len-1) == 1:
        shuffled_idx = copy.deepcopy(neighbor_idx_changes)
        random.shuffle(shuffled_idx)

      #generating a random neighbor Sprime
      s_prime = copy.deepcopy(sol)
      s_prime[shuffled_idx.pop()] *= (-1)
      cost_prime = isling_cost(S, s_prime)
      

      
      #calculating the difference from  
      delta = cost_prime - cost
      
      logging.debug('trial:' + str(trials) +  ' cost prime:' + str(cost_prime) + ' s_prime:' + str(s_prime) + str(shuffled_idx) +  str(delta))

      if delta <= 0: #downhill move
        logging.info('CHANGES')
        logging.debug('cost_prime:'+ str(cost_prime) + ' cost:' + str(cost) + ' cost_star:'+ str(cost_star) )
        changes += 1
        cost = cost_prime
        #changing solution
        sol = s_prime

        if cost_star > cost_prime:
          sol_star = s_prime
          cost_star = cost_prime
          cost_star_changed = True
      
      if delta > 0: # uphill move
        r = random.uniform(0, 1.) #random number
        if r <= np.exp( (-1 * (delta)) / T ): #if r is below the prob e^(-delta/T) , consider boltzman(?) : -exp(delta/(K_b * T)), similar but with k_b
          changes += 1
          cost = cost_prime
          #changing solution
          sol = s_prime

    
    if alpha != None: #use user selected alpha
      if cooling_schedule == 'exp_mult':
        T = exp_mult_cooling(T0, cycle_counter, alpha)

      elif cooling_schedule == 'non_monotonic_adaptive':
        T = non_monotonic_adaptive_cooling(T0, cycle_counter, cost, cost_star, alpha)

      elif cooling_schedule == 'log_mult':
        T = log_mult_cooling(T0, cycle_counter, alpha)

      elif cooling_schedule == 'lin_mult':
        T = linear_mult_cooling(T0, cycle_counter, alpha)

    else: #user relies on defualt alpha values
      if cooling_schedule == 'exp_mult':
        T = exp_mult_cooling(T0, cycle_counter)

      elif cooling_schedule == 'non_monotonic_adaptive':
        T = non_monotonic_adaptive_cooling(T0, cycle_counter, cost, cost_star)

      elif cooling_schedule == 'log_mult':
        T = log_mult_cooling(T0, cycle_counter)

      elif cooling_schedule == 'lin_mult':
        T = linear_mult_cooling(T0, cycle_counter)

    if cost_star_changed == True:
      freezecount = 0
    if changes/trials < MINPERCENT:
      freezecount += 1
      logging.info('FREEZING')


  logging.debug('best solution:' + str(sol_star))
  logging.debug('best cost:' + str(cost_star))
  logging.debug('freezecount:' + str(freezecount))

  return sol_star


  


  



  