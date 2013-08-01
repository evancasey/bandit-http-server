import random
import pdb

#---------------------------------------------
# Original implemention of this E-Greedy Multi-Armed Bandit Algorithm
# by John Myles White https://github.com/johnmyleswhite/BanditsBook/
# --------------------------------------------

def key_max(x): 
    return max(x, key = x.get)

class EpsilonGreedy():

    def __init__(self, bandit):
        self.epsilon = float(bandit['epsilon'])
        self.counts = {}
        self.values = {}
        for k,v in bandit['arms'].iteritems():
            self.counts[k] = v['count']
            self.values[k] = v['value']  
        self.budget = int(bandit['budget'])
        self.max_reward = bandit['max_reward']  
        self.total_reward = bandit['total_reward']
        self.total_count = bandit['total_count']
        self.regret = bandit['regret']  

    def select_arm(self):        
        if random.random() < self.epsilon and self.total_count < self.budget:
            return int(random.choice(list(self.counts.keys())))            
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
            
            self.regret = sum(self.counts.values()) * self.max_reward - self.total_reward

        return 
