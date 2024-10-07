from Definitions import *
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody, fixtureDef)
import pyray as rlib
from enum import Enum
from AI_Base import *

#Frames
frames_that_are_a_second = 30
dt = 1/frames_that_are_a_second

#Fighter Personalities
fighter_null_personality = Personality()

fighter_standard_personality = Personality()
fighter_standard_personality.add_emergency_rule([["distance_from_border < 1.5"]], [("move_to_center", [["distance_from_border > 2"]])])
fighter_standard_personality.add_rule([["1 attack_prob >= 0.75"]], [("avoid 2.3", [["distance_to_destination < 0.3"]])], [])
fighter_standard_personality.add_rule([["enemies_in_sight > 0"]], [("lin_rot_attack", [["action_time > 3"]])], [])

fighter_paranoic_personality = Personality()
fighter_paranoic_personality.add_emergency_rule([["distance_from_border < 2"]], [("move_to_center", [["distance_from_border > 3"]])])
fighter_paranoic_personality.add_rule([["1 attack_prob >= 0.75"]], [("avoid 2.3", [["distance_to_destination < 0.3"]])], [])
fighter_paranoic_personality.add_rule([["enemies_in_sight > 0"]], [("lin_rot_attack", [["action_time > 3"]])], [])
fighter_paranoic_personality.add_rule([["2 attack_prob >= 0.7"]], [("move_to_center", [["action_time > 3"]])], [("enemies_in_sight", 35)])
fighter_paranoic_personality.add_rule([["2 attack_prob >= 0.7"]], [("rot_in_place", [["action_time > 1.5"]])], [("unit", 65)])

fighter_planifier_personality = Personality()
fighter_planifier_personality.add_emergency_rule([["distance_from_border < 1.5"]], [("move_to_center", [["distance_from_border > 2"]])])
fighter_planifier_personality.add_rule([["enemies_in_sight > 0", "distance_from_enemy < 2"]], [("take_impulse 1", [["distance_to_destination < 0.3"]]), ("lin_rot_attack", [["action_time > 1"]])], [])
fighter_planifier_personality.add_rule([["enemies_in_sight > 0", "distance_from_enemy > 4"]], [("lin_attack", [["distance_to_destination < 7"]]), ("brake", [["action_time > 0.2"]])], [])

fighter_trick_personality = Personality()
fighter_trick_personality.add_rule([["enemies_in_sight > 0"]], [("move_to_border", [["distance_to_destination < 0.3"]]), ("brake", [["action_time > 0.2"]]), ("trick_avoid", [["action_time > 1.5"]])], [])
fighter_trick_personality.add_rule([["1 attack_prob >= 0.75", "distance_from_enemy < 6"]], [("avoid 2.3", [["distance_to_destination < 0.3"]])], [], name = "trick_avoid")

fighter_undecided_personality = Personality()
fighter_undecided_personality.add_emergency_rule([["distance_from_border < 3"]], [("move_to_center", [["distance_from_border > 4"]])])
fighter_undecided_personality.add_rule([["enemies_in_sight > 0"]], [("attack_and_continue_attacking", [["action_time > 0.05"]])], [])
fighter_undecided_personality.add_rule([["enemies_in_sight > 0"]], [("lin_rot_attack", [["action_time > 0.5"]]), ("attack_and_continue_attacking", [["action_time > 0.05"]])], [], name = "attack_and_continue_attacking")

#Toggles
do_narration = False
fighters_use_AI = True

#Actions
fighter_actions = Enum("fighter_actions", "moving lin_attacking rot_attacking lin_rot_attacking braking")

#Debug Controllers
graph_debug_draw = True
first_player_destination_debug_draw = True

