from scene import *
from globals import *
from nlp import *
from property_discretizer import *

###--- Create Scene and Fighters ---###
physW = world(gravity=(0, 0))

f1 = Fighter([-5,4], 0, physW, fighter_null_personality)
f1.max_linear_strength = 50
f1.precision = 1
f1.reaction_frequency = 1/0.01
poly1 = [[0,1], [-1,0], [1,0]]
f1.add_polygon(poly1)

f2 = Fighter([-1,0], 1, physW, fighter_null_personality)
poly2 = [[0,1], [-0.5,0], [1,0]]
f2.add_polygon(poly2)

sc = Scene([f1,f2], 10, [rlib.RED, rlib.GREEN], 20, physW, 200, 1, friction_coeficient=2)

###--- Main ---###
rlib.init_window(800, 800, "Debug View")
rlib.set_target_fps(frames_that_are_a_second)  ############## A partir de aqui, se asume frames_that_are_a_second frames son un segundo. Asi, si la cosa esta logra correr a 2*frames_that_are_a_second, por ejemplo, la simulacion iria al doble de velocidad

show_image = True

while not rlib.window_should_close():
    basic_controls()

    if rlib.is_mouse_button_pressed(0) and len(sc.fighters) > 0:
        sc.fighters[0].state = fighter_actions.moving
        sc.fighters[0].destination = xytm(rlib.get_mouse_x(), rlib.get_mouse_y())
    if rlib.is_mouse_button_pressed(1) and len(sc.fighters) > 0:
        sc.fighters[0].state = fighter_actions.braking
    
    if rlib.is_key_pressed(rlib.KeyboardKey.KEY_SPACE):
        show_image = not show_image
    
    if len(sc.fighters) > 0 and first_player_destination_debug_draw:
        meet = sc.fighters[0].destination
        if meet != None:
            rlib.draw_circle(xytc(meet[0], meet[1])[0], xytc(meet[0], meet[1])[1], 20, rlib.RED)
    
    sc.update()
    
    rlib.begin_drawing()
    if show_image:
        sc.draw()
    else:
        rlib.clear_background(rlib.BLACK)
        rlib.draw_text(f"Simulando en segundo plano...", 30, 30, 20, rlib.BLUE)
    rlib.end_drawing()

if do_narration:
    print("")
    print("Event Log:")
    event_text = event_log_to_text(sc.sceneResult.event_log)
    print(event_text)
    print("")
    print("AI Narration:")
    narration = get_gpt_narration(event_text)
    print(narration)

rlib.close_window()