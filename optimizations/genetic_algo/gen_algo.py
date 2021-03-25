'''

population of candidate solutions to an optimization problem is evolved toward better solutions


each population is called a generation

in each generation, the fitness of every individual in the population is evaluated

the fitness is usually the cost / objective function

the more fit individuals are stochastically selected from the current population

each individual in the modified to form a new generation

the new generation of candidates solutions is used in the next iteration of the algorithm

the algorithm terminates when eiether a max number of generations has been produced or a 
satisfactory fitness level has been reached for population.



#pseudocode


start from a population of randomly generated individuals

'''
import numpy as np
from optimizations.costs import * 
from .mutations import *
from .selections import *

def genetic_algo(S, pop_size, k_parents, k_crossovers, GEN_LIMIT, PLATEAU_LIMIT, c_star=0):
  '''
  pop_size
    population size

  k_crossovers
    no. of points in crossover

  c_star
    termination criteria

  '''
  s_len = len(S)
  isling_states = [1, -1]

  gen_cost_list = []
  gen_sol_list = []

  sol_star = None

  #initial generation
  for x in range(pop_size):
    n_minus_1_choices = [random.choice(isling_states) for x in range(s_len-1)]
    sol = [1] + n_minus_1_choices
    cost = isling_cost(S, sol)

    gen_sol_list.append(sol)
    gen_cost_list.append(cost)
  
  cost_star = min(gen_cost_list)
  sol_star = gen_sol_list[gen_cost_list.index(cost_star)]


  gen_count = 1
  plateau_count = 0

  while (gen_count < GEN_LIMIT ) and (plateau_count < PLATEAU_LIMIT) and (cost_star != c_star):

    tmp_sol_list = []
    tmp_cost_list = []
    gen_count += 1
    cost_star_changed = False
    # print(gen_count)

    for x in range(pop_size): #new set of parents are selected for each new child
      #selection
      '''
      two parents atm
      '''
      parent_list = []
      parent_list = np.array([roulette_wheel_min(gen_sol_list, gen_cost_list) for x in range(k_parents)])
      

      random_crossovers = [np.random.randint(1,s_len) for x in range(k_crossovers)]
      for idx, crossover in enumerate(random_crossovers):
        if idx == 0:
          np.random.shuffle(parent_list[:, 1:crossover])
        else:
          np.random.shuffle(parent_list[:, random_crossovers[idx-1]:crossover])
      
      child = parent_list[np.random.randint(0,k_parents)]
      mutated_child = bit_string_mutation(1, child)
      tmp_sol_list.append(mutated_child)
      mutated_cost = isling_cost(S, mutated_child)
      tmp_cost_list.append(mutated_cost)

      if mutated_cost < cost_star:
        #assign new lowest cost
        cost_star = mutated_cost
        sol_star = mutated_child
        cost_star_changed = True


    if cost_star_changed == False:
      plateau_count += 1
    else:
      plateau_count = 0

    # print(sol_star)
    gen_sol_list = tmp_sol_list
    gen_cost_list = tmp_cost_list



  return sol_star
