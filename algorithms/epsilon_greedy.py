import random

#---------------------------------------------
# Implemention of the E-Greedy Multi-Armed Bandit Algorithm
# by John Myles White https://github.com/johnmyleswhite/BanditsBook/
# --------------------------------------------

def ind_max(x):
  ''' returns the index of the max value in the array '''

  m = max(x)
  return x.index(m)

class EpsilonGreedy():
  ''' class to represent a Bandit with many arms '''

  def __init__(self, epsilon, counts, values):
    self.epsilon = epsilon 
    self.counts = counts # number of trials
    self.values = values # estimate of mean reward for each arm
    return

  def initialize(self, n_arms):
    self.counts = [0 for col in range(n_arms)]
    self.values = [0.0 for col in range(n_arms)]
    return

  def select_arm(self):
    ''' determines which arm to pick based on values'''

    if random.random() > self.epsilon:
      return ind_max(self.values)
    else:
      return random.randrange(len(self.values))
  
  def update(self, chosen_arm, reward):
    ''' gets called after each trial '''

    self.counts[chosen_arm] = self.counts[chosen_arm] + 1
    n = self.counts[chosen_arm]
    
    value = self.values[chosen_arm]
    new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
    self.values[chosen_arm] = new_value
    return