import numpy as np

def bit_string_mutation(k, child):
  '''
  k
    int
    number of mutations
  child
  '''
  idx_list = list(range(1,len(child)))
  np.random.shuffle(idx_list)
  for x in range(k):
    idx = idx_list.pop()
    child[idx] *= (-1)

  return child