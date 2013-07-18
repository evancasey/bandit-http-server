import math
import random
import pdb

#---------------------------------------------
# Original implemention of this Softmax Multi-Armed Bandit Algorithm
# by John Myles White https://github.com/johnmyleswhite/BanditsBook/
# --------------------------------------------

def categorical_draw(probs):
    z = random.random()
    cum_prob = 0.0
    for i in range(len(probs)):
        prob = probs[i]
        cum_prob += prob
        if cum_prob > z:
            return i
      
    return len(probs) - 1

class Softmax:
    def __init__(self, bandit):
        self.epsilon = float(bandit['epsilon'])
        self.counts = {}
        self.values = {}
        for k,v in bandit['arms'].iteritems():
            self.counts[k] = v['count']
            self.values[k] = v['value'] 
        self.max_reward = bandit['max_reward']  
        self.total_reward = bandit['total_reward']
        self.total_count = bandit['total_count']
        self.regret = bandit['regret']           
        return
  
    def select_arm(self):
        z = sum([math.exp(int(v) / self.epsilon) for v in self.values])
        probs = [math.exp(int(v) / self.epsilon) / z for v in self.values]
        return categorical_draw(probs)

    def update(self, chosen_arm, reward):

        # update count
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n = self.counts[chosen_arm]
        
        #update value
        value = self.values[chosen_arm]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value

        # update regret, total reward, and total_count
        self.total_reward += reward
        self.total_count += 1
        self.regret = sum(self.counts.values()) * self.max_reward - self.total_reward

        return