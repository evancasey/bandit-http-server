import math
import random
import pdb
import numpy as np

#---------------------------------------------
# Original implemention of this Softmax Multi-Armed Bandit Algorithm
# by John Myles White https://github.com/johnmyleswhite/BanditsBook/
# --------------------------------------------

def key_max(x): 
    return max(x, key = x.get)

def categorical_draw(bandit):
    z = random.random()
    cum_prob = 0.0
    for k,v in bandit.probs.iteritems():    
        prob = v
        cum_prob += prob
        if cum_prob > z:
            return k
      
    return len(probs) - 1

class Softmax:
    def __init__(self, bandit):
        self.epsilon = float(bandit['epsilon'])
        self.counts = {}
        self.values = {}
        self.reward_history = {}
        self.probs = {}
        for k,v in bandit['arms'].iteritems():
            self.reward_history[k] = v['reward_history']
            self.counts[k] = v['count']
            self.values[k] = v['value'] 
            self.probs[k] = 0 
        self.budget = int(bandit['budget'])
        self.max_reward = bandit['max_reward']  
        self.total_reward = bandit['total_reward']
        self.total_count = bandit['total_count']
        self.regret = bandit['regret']           
        return
  
    def select_arm(self):        
        z = sum([math.exp(float(v) / self.epsilon) for k,v in self.values.iteritems()])
        for k,v in self.probs.iteritems():
            self.probs[k] = math.exp(float(self.values[k]) / self.epsilon) / z      

        if self.total_count < self.budget:  
            return categorical_draw(self)
        else:
            return int(key_max(self.values))


    def update(self, chosen_arm, reward):
        
        self.total_count += 1

        if self.total_count < self.budget:


            # update count
            self.counts[chosen_arm] = self.counts[chosen_arm] + 1
            n = self.counts[chosen_arm]

            # update value
            value = self.values[chosen_arm]
            new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
            self.values[chosen_arm] = new_value


            # update regret, total reward, and total_count
            self.total_reward += reward

            best_arm = categorical_draw(self)
            
            self.regret = (np.mean(self.reward_history[best_arm]) * self.total_count) - (self.total_reward)

        return 