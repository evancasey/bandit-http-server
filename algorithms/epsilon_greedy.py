import random
from app import db
import pdb

#---------------------------------------------
# Original implemention of the E-Greedy Multi-Armed Bandit Algorithm
# by John Myles White https://github.com/johnmyleswhite/BanditsBook/
# --------------------------------------------

def ind_max(x):
  ''' returns the index of the max value in the array '''

  m = max(x)
  return x.index(m)

def selectArm(bandit):
  ''' determines which arm to pick based on values'''

  epsilon = bandit['epsilon']

  arm_values_arr = []
  for k in bandit['arms']:
    arm_values_arr.append(bandit['arms'][k])
    
  if random.random() > epsilon:
    return ind_max(arm_values_arr)
  else:
    return random.randrange(len(arm_values_arr))

def update(bandit, arm_id, reward):
  ''' gets called after each trial '''

  current_arm = bandit['arms'][str(arm_id)]

  current_arm['count'] = current_arm['count'] + 1
  n = current_arm['count']
  
  value = current_arm['value']
  new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
  current_arm['value'] = new_value
  
  return bandit