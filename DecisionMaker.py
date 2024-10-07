from globals import *
from property_discretizer import *
import random

plan_state = Enum("plan_state", "two_phase_charge_ph2 two_phase_charge_ph1 escaping_crowd rot_defense running_to_center exploring attacking getting_far_from_border avoiding braking")

class RobotDecisionMaker:
    def __init__(self):
        self.state = plan_state.braking
        self.destination = (0,0)
        self.locked_in_robot_id = -1

        self.time_in_rot_defense = 0
        self.time_in_two_phase_charge_phase_2 = 0

    def make_decision_standard(self, robot_state, other_robots, belief_state):
        
        #--- Emergencias ---#
        if robot_state.distance_from_border < 1:
            self.state = plan_state.getting_far_from_border
            self.destination = (0,0)
            return fighter_actions.lin_attacking, (0,0)

        if self.state == plan_state.getting_far_from_border and robot_state.distance_from_border < 1.5:
            return fighter_actions.lin_attacking, (0,0)

        #--- Que se mantenga ejecutando el plan actual si le conviene ---#
        if self.state == plan_state.avoiding and math.sqrt((self.destination[0]-robot_state.position.x)**2 + (self.destination[1]-robot_state.position.y)**2) > 0.2:
            return fighter_actions.lin_attacking, self.destination
        
        if self.state == plan_state.attacking:
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref != None:
                
                r = 0
                if math.sqrt((oponent_ref.position.x-robot_state.position.x)**2+(oponent_ref.position.y-robot_state.position.y)**2) < 0.4:
                    r = random.random()
                
                if r <= 0.2:
                    return fighter_actions.lin_rot_attacking, (oponent_ref.position.x, oponent_ref.position.y)

        #--- Dada la inferencia de estado calculada para cada robot en vista, decidir que hacer ---#
        probs = []
        oponent_refs = []
        for id,hmm in belief_state.items():
            if id == robot_state.id: continue
            
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == id:
                    oponent_ref = f_other
                    break
            
            oponent_refs.append(oponent_ref)
            probs.append(hmm.forward(discretize_properties_for_HMM(robot_state, oponent_ref)))
        
        #Esquivar
        for i in range(len(probs)):
            oponent_ref = oponent_refs[i]
            if probs[i][0] > 0.8 and oponent_ref.team_id != robot_state.team_id:
                self.state = plan_state.avoiding
                perp_vel = (oponent_ref.body.linearVelocity.y, -oponent_ref.body.linearVelocity.x)
                perp_vel_abs = math.sqrt(perp_vel[0]**2 + perp_vel[1]**2)
                perp_vel_norm = (1*perp_vel[0]/perp_vel_abs, 1*perp_vel[1]/perp_vel_abs)
                self.destination = (robot_state.position.x + perp_vel_norm[0], robot_state.position.y + perp_vel_norm[1])
                return fighter_actions.lin_attacking, self.destination
        
        #Si no tiene na que hacer, atacar al primer pana que vea... literal
        for f in other_robots:
            if f.team_id != robot_state.team_id:
                self.locked_in_robot_id = f.id
                self.state = plan_state.attacking
                return fighter_actions.lin_rot_attacking, (f.position.x, f.position.y)

        #--- Si no se le ocurre nada, que explore ---#
        if self.state == plan_state.exploring:
            return fighter_actions.moving, self.destination

        self.state = plan_state.exploring
        self.destination = (random.random(),random.random())
        return fighter_actions.moving, self.destination




    def make_decision_paranoic(self, robot_state, other_robots, belief_state):
        #--- Seguridad ---#
        if robot_state.distance_from_border < 2:
            self.state = plan_state.getting_far_from_border
            self.destination = (0,0)
            return fighter_actions.lin_attacking, (0,0)

        if self.state == plan_state.getting_far_from_border and robot_state.distance_from_border < 3:
            return fighter_actions.lin_attacking, (0,0)

        if self.state == plan_state.running_to_center and math.sqrt(robot_state.position.x**2+robot_state.position.y**2) > 1:
            return fighter_actions.moving, (0,0)

        if self.state == plan_state.rot_defense:
            if self.time_in_rot_defense < 4:
                self.time_in_rot_defense += 1/robot_state.reaction_frequency
                return fighter_actions.lin_rot_attacking, self.destination
            else:
                self.time_in_rot_defense = 0

        #Inferencia
        probs = []
        oponent_refs = []
        for id,hmm in belief_state.items():
            if id == robot_state.id: continue
            
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == id:
                    oponent_ref = f_other
                    break
            
            oponent_refs.append(oponent_ref)
            probs.append(hmm.forward(discretize_properties_for_HMM(robot_state, oponent_ref)))

        #Si hay demasiados robots aparentemente atacando, asustarse y correr al centro, o entrar en modo helicoptero y mantener la posicion 
        cumm = 0
        for p in probs:
            if p[0] >= 0.7:
                cumm += p[0]
        if cumm > 2.10:
            r = random.random()
            if r < 0.35:
                self.state = plan_state.running_to_center
                self.destination = (0,0)
                return fighter_actions.moving, (0,0)
            else:
                self.state = plan_state.rot_defense
                self.destination = (robot_state.position.x, robot_state.position.y)
                return fighter_actions.lin_rot_attacking, self.destination

        #--- Que se mantenga ejecutando el plan actual si le conviene ---#
        if self.state == plan_state.avoiding and math.sqrt((self.destination[0]-robot_state.position.x)**2 + (self.destination[1]-robot_state.position.y)**2) > 0.2:
            return fighter_actions.lin_attacking, self.destination
        
        if self.state == plan_state.attacking:
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref != None:
                
                r = 0
                if math.sqrt((oponent_ref.position.x-robot_state.position.x)**2+(oponent_ref.position.y-robot_state.position.y)**2) < 0.4:
                    r = random.random()
                
                if r <= 0.2:
                    return fighter_actions.lin_rot_attacking, (oponent_ref.position.x, oponent_ref.position.y)

        #--- Dada la inferencia de estado calculada para cada robot en vista, decidir que hacer ---#
        for i in range(len(probs)):
            oponent_ref = oponent_refs[i]
            r = random.random()
            if probs[i][0] > 0.8 and oponent_ref.team_id != robot_state.team_id and r < 0.3:
                self.state = plan_state.avoiding
                perp_vel = (oponent_ref.body.linearVelocity.y, -oponent_ref.body.linearVelocity.x)
                perp_vel_abs = math.sqrt(perp_vel[0]**2 + perp_vel[1]**2)
                perp_vel_norm = (1*perp_vel[0]/perp_vel_abs, 1*perp_vel[1]/perp_vel_abs)
                self.destination = (robot_state.position.x + perp_vel_norm[0], robot_state.position.y + perp_vel_norm[1])
                return fighter_actions.lin_attacking, self.destination
        
        #Si no tiene na que hacer, atacar al primer pana que vea... literal
        for f in other_robots:
            if f.team_id != robot_state.team_id:
                self.locked_in_robot_id = f.id
                self.state = plan_state.attacking
                return fighter_actions.lin_rot_attacking, (f.position.x, f.position.y)

        #--- Si no se le ocurre nada, que explore ---#
        if self.state == plan_state.exploring:
            return fighter_actions.moving, self.destination

        self.state = plan_state.exploring
        self.destination = (random.random(),random.random())
        return fighter_actions.moving, self.destination
    





    def make_decision_planifier(self, robot_state, other_robots, belief_state):
        
        #Emergencia
        if robot_state.distance_from_border < 1:
            self.state = plan_state.getting_far_from_border
            self.destination = (0,0)
            return fighter_actions.lin_attacking, (0,0)

        if self.state == plan_state.getting_far_from_border and robot_state.distance_from_border < 2:
            return fighter_actions.lin_attacking, (0,0)

        #Inferencia
        probs = []
        oponent_refs = []
        for id,hmm in belief_state.items():
            if id == robot_state.id: continue
            
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == id:
                    oponent_ref = f_other
                    break
            
            oponent_refs.append(oponent_ref)
            probs.append(hmm.forward(discretize_properties_for_HMM(robot_state, oponent_ref)))

        #Mantener ataque principal
        distance_to_destination = math.sqrt((self.destination[0]-robot_state.position.x)**2+(self.destination[1]-robot_state.position.y)**2)

        if self.state == plan_state.two_phase_charge_ph1:
            if distance_to_destination < 0.3:
                f_oponent = None
                for f in other_robots:
                    if f.id == self.locked_in_robot_id:
                        f_oponent = f
                        break

                if f_oponent != None:
                    self.state = plan_state.two_phase_charge_ph2
                    self.destination = (f_oponent.position.x, f_oponent.position.y)
                    self.time_in_two_phase_charge_phase_2 = 0
                    return fighter_actions.lin_rot_attacking, self.destination
            else:
                return fighter_actions.lin_attacking, self.destination

        if self.state == plan_state.two_phase_charge_ph2 and distance_to_destination > 0.2:
            self.time_in_two_phase_charge_phase_2 += 1/robot_state.reaction_frequency

            f_oponent = None
            for f in other_robots:
                if f.id == self.locked_in_robot_id:
                    f_oponent = f
                    break

            if f_oponent != None and self.time_in_two_phase_charge_phase_2 < 3:
                self.destination = (f_oponent.position.x, f_oponent.position.y)
                return fighter_actions.lin_rot_attacking, self.destination

        #Mantener ataque secundario
        if self.state == plan_state.attacking:
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == self.locked_in_robot_id:
                    oponent_ref = f_other
                    break
            
            if oponent_ref != None:
                
                r = 0
                if math.sqrt((oponent_ref.position.x-robot_state.position.x)**2+(oponent_ref.position.y-robot_state.position.y)**2) < 0.4:
                    r = random.random()
                
                if r <= 0.2:
                    return fighter_actions.lin_rot_attacking, (oponent_ref.position.x, oponent_ref.position.y)

        #Iniciar ataque principal o secundario
        for f in other_robots:
            if f.team_id != robot_state.team_id:
                oponent_to_self_raw = (robot_state.position.x-f.position.x, robot_state.position.y-f.position.y)
                oponent_to_self_abs = math.sqrt(oponent_to_self_raw[0]**2+oponent_to_self_raw[1]**2)
                if robot_state.distance_from_border > 3 and oponent_to_self_abs < 5:
                    dst = 1.5
                    oponent_to_self_corr = (oponent_to_self_raw[0]/oponent_to_self_abs * dst, oponent_to_self_raw[1]/oponent_to_self_abs * dst)

                    self.locked_in_robot_id = f.id
                    self.state = plan_state.two_phase_charge_ph1
                    
                    self.destination = (robot_state.position.x + oponent_to_self_corr[0], robot_state.position.y + oponent_to_self_corr[1])
                    return fighter_actions.lin_attacking, self.destination
                else:
                    for p, ref in zip(probs, oponent_refs):
                        if ref.id == f.id:
                            if p[4] > 0.6: #p[4] = Moving away from border
                                self.state = plan_state.attacking
                                self.destination = (f.position.x, f.position.y)
                                self.locked_in_robot_id = ref.id
                                return fighter_actions.lin_rot_attacking, self.destination
                            break
        
        #--- Si no se le ocurre nada, que explore ---#
        if self.state == plan_state.exploring:
            return fighter_actions.moving, self.destination

        self.state = plan_state.exploring
        self.destination = (random.random(),random.random())
        return fighter_actions.moving, self.destination


    def make_decision_avoider_demo(self, robot_state, other_robots, belief_state):
        
        if self.state == plan_state.avoiding and math.sqrt((self.destination[0]-robot_state.position.x)**2 + (self.destination[1]-robot_state.position.y)**2) > 0.2:
            return fighter_actions.lin_attacking, self.destination
        
        probs = []
        oponent_refs = []
        for id,hmm in belief_state.items():
            if id == robot_state.id: continue
            
            oponent_ref = None
            for f_other in other_robots:
                if f_other.id == id:
                    oponent_ref = f_other
                    break
            
            oponent_refs.append(oponent_ref)
            probs.append(hmm.forward(discretize_properties_for_HMM(robot_state, oponent_ref)))
        
        for i in range(len(probs)):
            oponent_ref = oponent_refs[i]
            if probs[i][0] > 0.8 and oponent_ref.team_id != robot_state.team_id:
                print("a")
                self.state = plan_state.avoiding
                perp_vel = (oponent_ref.body.linearVelocity.y, -oponent_ref.body.linearVelocity.x)
                perp_vel_abs = math.sqrt(perp_vel[0]**2 + perp_vel[1]**2)
                perp_vel_norm = (1*perp_vel[0]/perp_vel_abs, 1*perp_vel[1]/perp_vel_abs)
                self.destination = (robot_state.position.x + perp_vel_norm[0], robot_state.position.y + perp_vel_norm[1])
                return fighter_actions.lin_attacking, self.destination
        
        self.state = plan_state.braking
        return fighter_actions.braking, self.destination


    def make_decision_two_phase_demo(self, robot_state, other_robots, belief_state):
        pass

    def make_decision_experimental(self, robot_state, other_robots, belief_state):
        pass