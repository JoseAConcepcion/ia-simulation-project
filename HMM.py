from operator import indexOf

import numpy as np
from typing import Dict

from numpy.ma.core import argmax


class HMM:
    def __init__(self):
        """
                evidences are received as a dict with key = variable name and value = index that represents the actual value of the variable
                here are the relationships between those indexes and values:
                mass_difference is computed as enemy's mass - 'user's' mass: range from 0 to 4 (very high to very low)
                str_difference is equivalent to mass_difference
                direction: range from 0 to 2 (dir2 = 0 means the enemy is charging in our direction, and dir2 = 2 means he is charging in the opposite direction
                speed: range from 0 to 2 (high to low)
                border_dist alike
                rotation alike
                """
        self.states = ['Attacking', 'Moving', 'Fleing', 'Flanking', 'Moving Away From Border', 'Waiting']

        # Change str_difference for restitution difference
        self.evidences = ['mass_difference', 'restitution_difference', 'dir1','dir2','speed1','speed2','border_dist1','border_dist2','rotation1','rotation2']
        self.init_states_prob = np.array([1/6,1/6,1/6,1/6,1/6,1/6])
        self.transition_model = np.array([[3/8,1/8,1/8,1/8,1/8,1/8],
                                    [1/8,3/8,1/8,1/8,1/8,1/8],
                                    [1/8,1/8,3/8,1/8,1/8,1/8],
                                    [1/8,1/8,1/8,3/8,1/8,1/8],
                                    [1/8,1/8,1/8,1/8,3/8,1/8],
                                    [1/8,1/8,1/8,1/8,1/8,3/8]])
        self.evidences_prior_prob ={
            'mass_difference':[1/16,1/4,3/8,1/4,1/16],
            'restitution_difference':[1/16,1/4,3/8,1/4,1/16],
            'speed1':[1/4,1/2,1/4],
            'speed2':[1/4,1/2,1/4],
            'dir1':[1/3,1/3,1/3],
            'dir2':[1/3,1/3,1/3],
            'border_dist1':[1/3,1/3,1/3],
            'border_dist2':[1/3,1/3,1/3],
            'rotation1':[1/3,1/3,1/3],
            'rotation2':[1/3,1/3,1/3]
        }

        # Fix these values
        self.evidences_conditional_prob= {
            'Attacking':{
            'mass_difference':[0.5,0.3,0.1,0.08,0.02],
            'restitution_difference':[0.5,0.3,0.1,0.08,0.02],
            'speed2':[0.8,0.15,0.05],
            'dir2':[0.8,0.15,0.05],
            'border_dist1':[0.5,0.25,0.25],
            'rotation2': [1/3, 1/3, 1/3]
        },
            'Moving':{
            'speed2':[1/4,1/2,1/4],
            'dir2':[0.3,0.4,0.3]
        },
            'Fleing':{
            'mass_difference':[0.02,0.08,0.1,0.3,0.5],
            'restitution_difference':[0.02,0.08,0.1,0.3,0.5],
            'speed1':[0.8,0.15,0.05],
            'dir1':[0.8,0.15,0.05],
            'rotation1':[1/3,1/3,1/3]
        },
            'Flanking':{
            'speed2':[1/4,1/2,1/4],
            'dir2':[0.1,0.8,0.1]
        },
            'Moving Away From Border':{
            'speed2':[0.5,0.4,0.1],
            'dir2':[1/3,1/3,1/3],
            'border_dist2':[0.8,0.15,0.05]
        },
            'Waiting':{
            'speed2':[0.95,0.04,0.01],
            'dir2':[1/3,1/3,1/3]
        }
        }



        '''
        filtering_memory[state][i] is the probability of state 'state' given the evidences sequence from 1 to i
        '''
        self.filtering_memory = {
            'Attacking':[1/6],
            'Moving':[1/6],
            'Fleing':[1/6],
            'Flanking':[1/6],
            'Moving Away From Border':[1/6],
            'Waiting':[1/6]
    }
    def sensor_model(self,evidence:Dict[str,int], state:str):
        prob = 1
        for key in evidence.keys():
            index = evidence[key]
            if key in self.evidences_conditional_prob[state].keys():
                prob *= self.evidences_conditional_prob[state][key][index]
            else:
                prob *= self.evidences_prior_prob[key][index]
        return prob
    def transition_model_f(self,current_state, past_state):
        i = indexOf(self.states, past_state)
        j = indexOf(self.states, current_state)
        return self.transition_model[i,j]
    def forward(self,evidence:Dict[str,int]):
        """
        after calling forward the filtering_memory must be updated with its return
        """
        ans = np.ones(len(self.states))
        f = []
        for item in self.filtering_memory.items():
            f.append(item[1][-1])
        states_probs = np.matmul(self.transition_model.transpose(), f)
        for i in range(len(ans)):
            ans[i]*=self.sensor_model(evidence,self.states[i])*states_probs[i]
        ret = ans/sum(ans)
        for i in range(len(self.states)):
            self.filtering_memory[self.states[i]].append(ret[i])
        return ret

    def predict(self,t):
        """predict should be called ALWAYS after calling forward"""
        ans = []
        for item in self.filtering_memory.items():
            ans.append(item[1][-1])
        for time_step in range(t):
            ans = np.matmul(self.transition_model.transpose(), ans)
        return ans

# c = HMM()
# r = c.forward({'mass_difference':0,
#             'str_difference':0,
#             'speed1':1,
#             'speed2':0,
#             'dir1':1,
#             'dir2':0,
#             'border_dist1':1,
#             'border_dist2':1,
#             'rotation1':0,
#             'rotation2':0})
# print(r)
# print(sum(r))
# print(c.states[argmax(r)])