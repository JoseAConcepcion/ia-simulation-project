from globals import *
from HMM import HMM
from property_discretizer import *
import random



class FighterBrain:
    def __init__(self):
        self.inference_models:dict[int,HMM] = {}
        self.infered_state_name_to_index = {'attack_prob':  0, 'moving_prob': 1, 'avoiding_prob': 2, 'flanking_prob': 3, 'moving_away_from_border_prob': 4, 'waiting_prob': 5}

        self.probs = []
        self.oponent_refs = []
        self.potentiator_vars = {}

        self.current_rule_executing = None
        self.index_executing = 0
        self.locked_in_robot_id = -1
        self.destination = None
        self.time_executing_current_plan = 0
        self.fighter = None
        self.executing_emergency = False

    
    def plan(self, fighter):
        if len(fighter.personality.rules) == 0 and len(fighter.personality.emergency_rules) == 0:
            return
        
        self.time_executing_current_plan += 1/fighter.reaction_frequency
        self.fighter = fighter
        self.oponent_refs = []

        #Get the HMMs
        del_l = []
        for t in self.inference_models.items():
            if t[0] not in [f.id for f in fighter.fighters_in_sight]:
                del_l.append(t[0])
        for item in del_l:
            del self.inference_models[item]

        for spotted_fighter in fighter.fighters_in_sight:
            if spotted_fighter.id not in self.inference_models.keys():
                self.inference_models[spotted_fighter.id] = HMM()

        #Update the HMMs, and get the infered state for each enemy in sight
        self.probs = []
        self.oponent_refs = []
        for id,hmm in self.inference_models.items():
            if id == fighter.id: continue
            
            oponent_ref = None
            for f_other in fighter.fighters_in_sight:
                if f_other.id == id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref.team_id == fighter.team_id: continue
            
            self.oponent_refs.append(oponent_ref)
            self.probs.append(hmm.forward(discretize_properties_for_HMM(fighter, oponent_ref)))

        #Get Potentiator Variables
        self.potentiator_vars = {'unit': 1, "distance_from_border": fighter.distance_from_border, "fighters_in_sight": len(fighter.fighters_in_sight), "enemies_in_sight": 0, "friends_in_sight": 0}
        for f in fighter.fighters_in_sight:
            if f.team_id == fighter.team_id:
                self.potentiator_vars["friends_in_sight"] += 1
            else:
                self.potentiator_vars["enemies_in_sight"] += 1
            
        #Emergencies
        for e_rule in fighter.personality.emergency_rules:
            is_true, objective = self.evaluate_conditions(e_rule.conditions)
            if is_true:
                self.executing_emergency = True

                self.current_rule_executing = e_rule
                self.index_executing = 0
                self.locked_in_robot_id = objective
                self.destination = (0,0)
                self.time_executing_current_plan = 0
                self.init_current_action()

                success, s, d = self.apply_current_rule()
                if success:
                    fighter.state = s
                    fighter.destination = d
                    return
                else:
                    self.current_rule_executing = None
                    self.executing_emergency = False

        #Keep applying current rule
        if self.current_rule_executing != None:
            is_true, _ = self.evaluate_conditions(self.current_rule_executing.actions[self.index_executing][1])
            if is_true:
                self.index_executing += 1
                if self.index_executing >= len(self.current_rule_executing.actions):
                    self.current_rule_executing = None
                    self.executing_emergency = False
                else:
                    return
            else:
                success, s, d = self.apply_current_rule()
                if success:
                    fighter.state = s
                    fighter.destination = d
                    return
                else:
                    self.current_rule_executing = None
                    self.executing_emergency = False

        #Get Viable Actions
        viable_rules = []  #Format: [(Rule, viability_coefficient, objective_id), ...]
        for r in fighter.personality.rules:
            is_valid, objective_id = self.evaluate_conditions(r.conditions)
            if is_valid:
                viability_coefficient = 1
                for pot in r.potentiators:
                    viability_coefficient += self.potentiator_vars[pot[0]]*pot[1]
                viability_coefficient = max(1, viability_coefficient)

                viable_rules.append([r, viability_coefficient, objective_id])

        #Select Rule to Apply
        if len(viable_rules) == 0:
            self.current_rule_executing = None
            self.index_executing = 0
            self.locked_in_robot_id = -1
            self.destination = None
            self.time_executing_current_plan = 0

            fighter.state = fighter_actions.moving
            fighter.destination = (0,0)
            return
        elif len(viable_rules) == 1:
            self.current_rule_executing = viable_rules[0][0]
            self.index_executing = 0
            self.locked_in_robot_id = viable_rules[0][2]
            self.destination = (0,0)
            self.time_executing_current_plan = 0
            self.init_current_action()
            success, s, d = self.apply_current_rule()
            
            if success:
                fighter.state = s
                fighter.destination = d
                return
        else:
            total_denominator = 0
            for v in viable_rules:
                total_denominator += v[1]
            
            r = random.random()
            total_numerator = 0
            chosen = 0
            for i in range(len(viable_rules)):
                v = viable_rules[i]
                total_numerator += v[1]
                if r <= total_numerator/total_denominator:
                    chosen = i
                    break

            self.current_rule_executing = viable_rules[chosen][0]
            self.index_executing = 0
            self.locked_in_robot_id = viable_rules[chosen][2]
            self.destination = (0,0)
            self.time_executing_current_plan = 0
            self.init_current_action()
            success, s, d = self.apply_current_rule()
            
            if success:
                fighter.state = s
                fighter.destination = d
                return
            
            

    
    def evaluate_conditions(self, conditions): #Returns (truth, objective_id)
        for conjunction_terms in conditions:
            is_true = True
            objective = None
            for term in conjunction_terms:
                tokens = term.split(" ")
                
                #Expressions of type "(some, all, number) x_prob comparison_sign number"
                if tokens[0] == "all" or tokens[0].isnumeric():
                    
                    #Collect all enemies that comply to the condition
                    correct_enemies = []
                    for i in range(len(self.probs)):
                        n1 = self.probs[i][self.infered_state_name_to_index[tokens[1]]]
                        n2 = float(tokens[3])
                        if self.evaluate_comparison(n1, n2, tokens[2]):
                            correct_enemies.append(self.oponent_refs[i])

                    #Check if the condition is true
                    if tokens[0] == "all":
                        if len(correct_enemies) == len(self.oponent_refs):
                            objective = self.oponent_refs[0]
                        else:
                            is_true = False
                            break
                    else:
                        if len(correct_enemies) >= int(tokens[0]):
                            objective = self.oponent_refs[0]
                        else:
                            is_true = False
                            break
                elif term == "":
                    return True,None
                else:
                    n2 = float(tokens[2])
                    n1 = None
                    if tokens[0] == "distance_to_destination":
                        n1 = math.sqrt((self.destination[0]-self.fighter.position[0])**2 + (self.destination[1]-self.fighter.position[1])**2)
                    elif tokens[0] in self.potentiator_vars.keys():
                        n1 = self.potentiator_vars[tokens[0]]
                        if len(self.oponent_refs) > 0:
                            objective = self.oponent_refs[random.randint(0, len(self.oponent_refs)-1)]
                    elif tokens[0] == "action_time":
                        n1 = self.time_executing_current_plan
                    elif tokens[0] == "distance_from_enemy":
                        n1 = math.sqrt((self.fighter.position.x-objective.position.x)**2 + (self.fighter.position.y-objective.position.y)**2)
                    else:
                        print("Error evaluating "+term)
                        exit(code=-1)
                    
                    if not self.evaluate_comparison(n1, n2, tokens[1]):
                        is_true = False
                        break   
            
            if is_true:
                oid = None
                if objective != None:
                    oid = objective.id
                return True, oid

        return False,None

    def evaluate_comparison(self, n1, n2, comparison_token):
        if comparison_token == ">=":
            return n1 >= n2
        elif comparison_token == ">":
            return n1 > n2
        elif comparison_token == "<=":
            return n1 <= n2
        elif comparison_token == "<":
            return n1 < n2
        elif comparison_token == "==":
            return n1 == n2
        else:
            print("WTF was that '" + comparison_token + "' token?")
            exit()
    
    def init_current_action(self):
        action_tokens = self.current_rule_executing.actions[self.index_executing][0].split(" ")
        
        if action_tokens[0] in self.fighter.personality.named_rules.keys():
            pass
        elif action_tokens[0] == "avoid":
            
            oponent_ref = None
            for f_other in self.fighter.fighters_in_sight:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            perp_vel = (oponent_ref.body.linearVelocity.y, -oponent_ref.body.linearVelocity.x)
            perp_vel_abs = math.sqrt(perp_vel[0]**2 + perp_vel[1]**2)
            
            if perp_vel_abs < 0.01:
                perp_vel_abs += 0.01
            perp_vel_norm = (perp_vel[0]/perp_vel_abs, perp_vel[1]/perp_vel_abs)
            self.destination = (self.fighter.position.x + float(action_tokens[1])*perp_vel_norm[0], self.fighter.position.y + float(action_tokens[1])*perp_vel_norm[1])
        elif action_tokens[0] == "move_to_center":
            self.destination = (0,0)
        elif action_tokens[0] == "move_to_border":
            self.destination = (7,0)
        elif action_tokens[0] == "lin_rot_attack":
            
            oponent_ref = None
            for f_other in self.fighter.fighters_in_sight:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref == None:
                return
            self.destination = (oponent_ref.position.x, oponent_ref.position.y)
        elif action_tokens[0] == "lin_attack":
            
            oponent_ref = None
            for f_other in self.fighter.fighters_in_sight:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref == None:
                return
            self.destination = (oponent_ref.position.x, oponent_ref.position.y)
        elif action_tokens[0] == "rot_in_place":
            pass
        elif action_tokens[0] == "brake":
            pass
        elif action_tokens[0] == "take_impulse":
            oponent_ref = None
            for f_other in self.fighter.fighters_in_sight:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref == None:
                return
            
            oponent_to_self_raw = (self.fighter.position.x-oponent_ref.position.x, self.fighter.position.y-oponent_ref.position.y)
            oponent_to_self_abs = math.sqrt(oponent_to_self_raw[0]**2+oponent_to_self_raw[1]**2)

            dst = float(action_tokens[1])
            oponent_to_self_corr = (oponent_to_self_raw[0]/oponent_to_self_abs * dst, oponent_to_self_raw[1]/oponent_to_self_abs * dst)
            
            self.destination = (self.fighter.position.x + oponent_to_self_corr[0], self.fighter.position.y + oponent_to_self_corr[1])
            return fighter_actions.lin_attacking, self.destination
        else:
            print("No se reconoce la accion '" + self.current_rule_executing.actions[self.index_executing][0] + "'")

    def apply_current_rule(self): #Returns: (success, new_state, destination)
        action_tokens = self.current_rule_executing.actions[self.index_executing][0].split(" ")
        
        if action_tokens[0] in self.fighter.personality.named_rules.keys():
            
            rule = self.fighter.personality.named_rules[action_tokens[0]]
            truth, obj = self.evaluate_conditions(rule.conditions)
            if truth:
                self.current_rule_executing = rule
                self.index_executing = 0
                self.locked_in_robot_id = obj
                self.destination = (0,0)
                self.time_executing_current_plan = 0
                self.init_current_action()
                success, s, d = self.apply_current_rule()
                
                if success:
                    return True, s, d
            else:
                return True, fighter_actions.braking, (0,0)

        elif action_tokens[0] == "avoid":
            return True, fighter_actions.lin_attacking, self.destination
        elif action_tokens[0] == "move_to_center":
            return True, fighter_actions.lin_attacking, self.destination
        elif action_tokens[0] == "move_to_border":
            return True, fighter_actions.moving, self.destination
        elif action_tokens[0] == "lin_rot_attack":
            oponent_ref = None
            for f_other in self.oponent_refs:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref == None:
                return False, fighter_actions.braking, self.destination

            self.destination = (oponent_ref.position.x, oponent_ref.position.y)
            return True, fighter_actions.lin_rot_attacking, self.destination
        elif action_tokens[0] == "lin_attack":
            oponent_ref = None
            for f_other in self.oponent_refs:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref == None:
                return False, fighter_actions.braking, self.destination

            self.destination = (oponent_ref.position.x, oponent_ref.position.y)
            return True, fighter_actions.lin_attacking, self.destination
        elif action_tokens[0] == "rot_in_place":
            return True, fighter_actions.rot_attacking, (0,0)
        elif action_tokens[0] == "take_impulse":
            return True, fighter_actions.lin_attacking, self.destination
        elif action_tokens[0] == "brake":
            return True, fighter_actions.braking, (0,0)
        else:
            print("No se reconoce la accion '" + self.current_rule_executing.actions[self.index_executing][0] + "'")
            exit()