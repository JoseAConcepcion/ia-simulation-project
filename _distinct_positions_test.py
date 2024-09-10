from scene import *
from globals import *
from simulate import *

#Propiedades
#self.mass_density = 3
#self.restitution = 1.6    
#self.max_linear_strength = 100
#self.max_rotation_strength = 40
#self.precision = 0.8    
#self.view_radius = 4
#self.reaction_frequency = 1/0.3


total_victories = 0
victories = [0,0,0]
while total_victories < 100:

    #Create Team
    physW = world(gravity=(0, 0))

    poly1 = [[0,1], [-1,0], [1,0]]
    poly2 = [[0,1], [-0.5,0], [1,0]]

    f1 = Fighter([0.2,0.2], 0, physW, fighter_standard_personality)
    f1.add_polygon(poly1)

    f2 = Fighter([0,0], 0, physW, fighter_standard_personality)
    f2.add_polygon(poly2)

    f3 = Fighter([5,4], 1, physW, fighter_standard_personality)
    f3.add_polygon(poly1)

    f4 = Fighter([5,5], 1, physW, fighter_standard_personality)
    f4.add_polygon(poly2)

    f5 = Fighter([0,-7], 2, physW, fighter_standard_personality)
    f5.add_polygon(poly1)

    f6 = Fighter([1,-7], 2, physW, fighter_standard_personality)
    f6.add_polygon(poly2)

    sc = Scene([f1, f2, f3, f4, f5, f6], 10, [rlib.RED, rlib.GREEN, rlib.BLUE], 20, physW, 20, 2)

    #Simulate and watch results
    simulate_scene_until_battle_ends(sc)
    if not sc.sceneResult.was_draw:
        total_victories += 1
        victories[sc.sceneResult.winner_team_id] += 1
        print(victories)
