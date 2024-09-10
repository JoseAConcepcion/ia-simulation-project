from Definitions import *
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody, fixtureDef)
import pyray as rlib
from enum import Enum

#Frames
frames_that_are_a_second = 30
dt = 1/frames_that_are_a_second

#Fighter Personalities
fighter_standard_personality = 0
fighter_paranoic_personality = 1
fighter_planifier_personality = 2

#Toggles
do_narration = False
fighters_use_AI = True

#Actions
fighter_actions = Enum("fighter_actions", "moving lin_attacking rot_attacking lin_rot_attacking braking")

#Debug Controllers
graph_debug_draw = False
first_player_destination_debug_draw = False

