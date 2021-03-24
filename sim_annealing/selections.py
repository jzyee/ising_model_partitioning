import numpy as np

def roulette_wheel_min(sol_list, cost_list):
  '''
  Roulette wheel selection for a minimization problem, 
  thus the inversion of traditional formula

  e.g 
    P_i = f_i / sum(f_i to f_N) 
            to
    P_i = 1 - (f_i / sum(f_i to f_N)) 

  naive implementation

  returns parent
  '''
  cost_list = np.array(cost_list)
  summa = np.sum(cost_list)
  bin_limits = []
  bin_sel = None

  inv_cost_list = [summa/x for x in cost_list]
  norm_inv_cost_list = [float(i)/sum(inv_cost_list) for i in inv_cost_list]

  for norm_inv_cost in norm_inv_cost_list:
    #inve
    p = norm_inv_cost
    if len(bin_limits) != 0:
      bin_limits.append(bin_limits[-1] + p)
    else:
      bin_limits.append(p)

  r = np.random.uniform(0,1)
  #print(bin_limits)
  for idx, bin in enumerate(bin_limits):
    
    if r <= bin:
      bin_sel = idx
      break

  return sol_list[bin_sel]