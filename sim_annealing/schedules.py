import numpy as np

'''

  cooling schedules

  source:
  http://what-when-how.com/artificial-intelligence/a-comparison-of-cooling-schedules-for-simulated-annealing-artificial-intelligence/#:~:text=Cooling%20Schedule%3A%20Temperature%20control%20method,transitions%20for%20each%20temperature%20value


'''


def exp_mult_cooling(T, k=1, alpha=0.9):
  '''
  proposed by Kirkpatrick, Gelatt, Vecchi(1983)
  the temperature decrease is made multioplying the initial temperature

    0.8 <= alpha <= 0.9

  params:
    T: temperature
    k: temperature cycle
  '''
  assert 0.8 <= alpha <= 0.9, 'alpha must be 0.8 <= alpha <= 0.9'
  return T * (alpha**k)

def log_mult_cooling(T0, k, alpha=2):
  '''
  asymptotical convergence condition of simulated annealing 
  (Aarts, E.H.L. & Korst, J., 1989), but incorporating a factor a of cooling
  speeding-up that makes possible its use in practice. The temperature decrease
  is made multiplying the initial temperature T0 by a factor that decreases in
  inverse proportion to the natural logarithm of temperature cycle k
  
  params:
    T0: starting temperature
    alpha: alpha, alpha must be more than 1
    k: temperature cycle
  '''
  assert alpha > 1, 'alpha must be > 1'
  return T0/(1 + alpha * (np.log(1+k)) )

def linear_mult_cooling(T0, k, alpha=1):
  '''
  The temperature decrease is made multiplying the initial temperature T0 by
  a factor that decreases in inverse proportion to the temperature cycle k.
  '''
  assert alpha > 0, 'alpha must be > 0'
  return T0/(1 + (alpha*k))


def non_monotonic_adaptive_cooling(T0, k, current_cost, best_cost, alpha=0.9):
  '''
  In the non-monotonic adaptive cooling, the system temperature T at each state
  transition is computed multiplying the temperature value Tk, obtained by any
  of the former criteria, by an adaptive factor m based on the difference 
  between the current solution cost and the best cost achieved until that 
  moment by the algorithm. This factor m means that the greater the distance 
  between current solution and best achieved solution is, the greater the 
  temperature is, and consequently the allowed energy hops. This criterion is 
  a variant of the one proposed by M. Locatelli (2000), and it can be used in 
  combination with any of the former criteria to compute Tk. In the comparison, 
  the standard exponential multiplicative cooling has been used for this 
  purpose. So the cooling curve is characterized by a fluctuant random behaviour 
  comprised between the exponential curve defined by Tk and its double value 
  2Tk.

  '''
  return (1 + round( ( (current_cost - best_cost)/current_cost), 3) ) *  \
         exp_mult_cooling(T0, k, alpha)
