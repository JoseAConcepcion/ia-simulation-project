from globals import *

def discretize_properties_for_HMM(f_self, f_oponent):
    evidences = {
        'mass_difference':0,
        'restitution_difference':0,
        'speed1':0,
        'speed2':0,
        'dir1':0,
        'dir2':0,
        'border_dist1':0,
        'border_dist2':0,
        'rotation1':0,
        'rotation2':0,
        #'distance':0
    }
    
    mass_diff_limits = [-1, -0.5, 0, 0.5]
    restitution_diff_limits = [-1, -0.5, 0, 1] ###@@@???
    speed_limits = [6, 13]
    dir_tolerance = 0.2 
    rot_speed_limits = [10, 20]
    dist_limits = [2.5, 5.5]

    #Mass diff
    mass_diff = f_oponent.body.mass - f_self.body.mass
    for i in range(len(mass_diff_limits)):
        if mass_diff < mass_diff_limits[i]:
            evidences['mass_difference'] = 4-i
            break
    
    #Rest diff
    restitution_diff = f_oponent.restitution - f_self.restitution
    for i in range(len(restitution_diff_limits)):
        if restitution_diff < restitution_diff_limits[i]:
            evidences['restitution_difference'] = 4-i
            break

    #Speed1
    speed1 = math.sqrt(f_self.body.linearVelocity.x**2 + f_self.body.linearVelocity.y**2)
    for i in range(len(speed_limits)):
        if speed1 < speed_limits[i]:
            evidences['speed1'] = 2-i
            break
    
    #Speed2
    speed2 = math.sqrt(f_oponent.body.linearVelocity.x**2 + f_oponent.body.linearVelocity.y**2)
    for i in range(len(speed_limits)):
        if speed2 < speed_limits[i]:
            evidences['speed2'] = 2-i
            break

    #Dir
    self_to_oponent_vector_raw = (f_oponent.position.x-f_self.position.x, f_oponent.position.y-f_self.position.y)
    self_to_oponent_vector_abs = math.sqrt(self_to_oponent_vector_raw[0]**2 + self_to_oponent_vector_raw[1]**2)
    self_to_oponent_vector = (self_to_oponent_vector_raw[0]/self_to_oponent_vector_abs, self_to_oponent_vector_raw[1]/self_to_oponent_vector_abs)
    
    #Dir1
    if speed1 < 0.001:
        evidences['dir1'] = 1
    else:
        move_v_1_normalized = (f_self.body.linearVelocity.x/speed1, f_self.body.linearVelocity.y/speed1) 
        dir1 = self_to_oponent_vector[0]*move_v_1_normalized[0] + self_to_oponent_vector[1]*move_v_1_normalized[1]
        if dir1 < -dir_tolerance:
            evidences['dir1'] = 2
        elif dir1 < dir_tolerance:
            evidences['dir1'] = 1
        else:
            evidences['dir1'] = 0
    
    #Dir2
    if speed2 < 0.001:
        evidences['dir2'] = 1
    else:
        move_v_2_normalized = (f_oponent.body.linearVelocity.x/speed2, f_oponent.body.linearVelocity.y/speed2) 
        oponent_to_self_vector = (-self_to_oponent_vector[0], -self_to_oponent_vector[1])
        dir2 = oponent_to_self_vector[0]*move_v_2_normalized[0] + oponent_to_self_vector[1]*move_v_2_normalized[1]
        if dir2 < -dir_tolerance:
            evidences['dir2'] = 2
        elif dir2 < dir_tolerance:
            evidences['dir2'] = 1
        else:
            evidences['dir2'] = 0

    #Border Distance 1
    for i in range(len(dist_limits)):
        if f_self.distance_from_border < dist_limits[i]:
            evidences['border_dist1'] = 2-i
            break
    
    #Border Distance 2
    for i in range(len(dist_limits)):
        if f_oponent.distance_from_border < dist_limits[i]:
            evidences['border_dist2'] = 2-i
            break

    #Rotation1
    rot_speed1 = math.fabs(f_self.body.angularVelocity)
    for i in range(len(rot_speed_limits)):
        if rot_speed1 < rot_speed_limits[i]:
            evidences['rotation1'] = 2-i
            break
    
    #Rotation2
    rot_speed2 = math.fabs(f_oponent.body.angularVelocity)
    for i in range(len(rot_speed_limits)):
        if rot_speed2 < rot_speed_limits[i]:
            evidences['rotation2'] = 2-i
            break
    
    #Distance
    #distance = math.sqrt((f_self.position.x-f_oponent.position.x)**2 + (f_self.position.y-f_oponent.position.y)**2)
    #for i in range(len(dist_limits)):
    #    if distance < dist_limits[i]-0.5:
    #        evidences['distance'] = 2-i
    #        break

    return evidences
    
