
from globals import *
from HMM import HMM
from DecisionMaker import RobotDecisionMaker
from property_discretizer import *

class FighterBrain:
    def __init__(self):
        self.inference_models:dict[int,HMM] = {}
        self.decision_maker = RobotDecisionMaker()
    
    def plan(self, fighter):
        #if fighter.team_id == 0: return #@@@@@@@@@@@@@@ DEBUG

        del_l = []
        for t in self.inference_models.items():
            if t[0] not in [f.id for f in fighter.fighters_in_sight]:
                del_l.append(t[0])
        for item in del_l:
            del self.inference_models[item]

        for spotted_fighter in fighter.fighters_in_sight:
            if spotted_fighter.id not in self.inference_models.keys():
                self.inference_models[spotted_fighter.id] = HMM()
        
        #if fighter.team_id == 0:
        #    decision = self.decision_maker.make_decision_experimental(robot_state=fighter, other_robots=fighter.fighters_in_sight, belief_state = self.inference_models)
        #    
        #    fighter.state = decision[0]
        #    fighter.destination = decision[1]
        #    return
        
        if fighter.personality == fighter_standard_personality:
            decision = self.decision_maker.make_decision_standard(robot_state=fighter, other_robots=fighter.fighters_in_sight, belief_state = self.inference_models)
        elif fighter.personality == fighter_paranoic_personality:
            decision = self.decision_maker.make_decision_paranoic(robot_state=fighter, other_robots=fighter.fighters_in_sight, belief_state = self.inference_models)
        elif fighter.personality == fighter_planifier_personality:
            decision = self.decision_maker.make_decision_planifier(robot_state=fighter, other_robots=fighter.fighters_in_sight, belief_state = self.inference_models)

        fighter.state = decision[0]
        fighter.destination = decision[1]