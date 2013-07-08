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
        self.epsilon = bandit['epsilon']
        self.counts = {}
        self.values = {}
        for k,v in bandit['arms'].iteritems():
            self.counts[k] = v['count']
            self.values[k] = v['value']        
        return

    def select_arm(self):
        if random.random() > self.epsilon:
            return int(key_max(self.values))
        else:
            return random.randrange(len(self.values))

    def update(self, chosen_arm, reward):

        self.counts[str(chosen_arm)] = self.counts[str(chosen_arm)] + 1
        n = self.counts[str(chosen_arm)]
        
        value = self.values[str(chosen_arm)]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        print chosen_arm
        self.values[str(chosen_arm)] = new_value

        arm = { 'count' : n, 'value' : new_value}

        return arm