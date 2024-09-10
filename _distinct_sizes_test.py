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

    #Medianos
    f1 = Fighter([-5,4], 0, physW, fighter_standard_personality)
    poly1 = [[0,1], [-1,0], [1,0]]
    f1.add_polygon(poly1)
    #print(f1.body.mass)

    f2 = Fighter([-5,3], 0, physW, fighter_standard_personality)
    poly2 = [[0,1], [-0.7,0], [1,0]]
    f2.mass_density = 3.5
    f2.add_polygon(poly2)
    #print(f2.body.mass)

    #Grandes
    f3 = Fighter([5,4], 1, physW, fighter_standard_personality)
    poly3 = [[0,1.5], [-1.5,0], [1.5,0]]
    f3.mass_density = 1.33
    f3.add_polygon(poly3)
    #print(f3.body.mass)

    f4 = Fighter([5,5], 1, physW, fighter_standard_personality)
    poly4 = [[0,1.5], [-1.05,0], [1.5,0]]
    f4.mass_density = 1.55
    f4.add_polygon(poly4)
    #print(f4.body.mass)

    #Chiquitos
    f5 = Fighter([0,-7], 2, physW, fighter_standard_personality)
    poly5 = [[0,0.5], [-0.5,0], [0.5,0]]
    f5.mass_density = 12
    f5.add_polygon(poly5)
    #print(f5.body.mass)

    f6 = Fighter([1,-7], 2, physW, fighter_standard_personality)
    poly6 = [[0,0.5], [-0.25,0], [0.5,0]]
    f6.mass_density = 16
    f6.add_polygon(poly6)
    #print(f6.body.mass)

    sc = Scene([f1, f2, f3, f4, f5, f6], 10, [rlib.RED, rlib.GREEN, rlib.BLUE], 20, physW, 20, 2)

    #Simulate and watch results
    simulate_scene_until_battle_ends(sc)
    if not sc.sceneResult.was_draw:
        total_victories += 1
        victories[sc.sceneResult.winner_team_id] += 1
        print(victories)
