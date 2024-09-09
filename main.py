from scene import *
from globals import *
from nlp import *
from property_discretizer import *

###--- Create Scene and Fighters ---###
physW = world(gravity=(0, 0))

f1 = Fighter([-5,4], 0, physW)
poly1 = [[0,1], [-1,0], [1,0]]
f1.add_polygon(poly1)

f2 = Fighter([-5,5], 0, physW)
poly2 = [[0,1], [-0.5,0], [1,0]]
f2.add_polygon(poly2)

f3 = Fighter([5,4], 1, physW)
poly3 = [[0,1], [1,0], [0,0]]
f3.add_polygon(poly3)

f4 = Fighter([5,5], 1, physW)
poly4 = [[0,2], [1,0], [0,1]]
f4.add_polygon(poly4)

f5 = Fighter([0,-7], 2, physW)
poly5 = [[0,1], [1,0], [0,0]]
f5.add_polygon(poly5)

f6 = Fighter([1,-7], 2, physW)
poly6 = [[0,2], [1,0], [0,1]]
f6.add_polygon(poly6)

sc = Scene([f1,f2, f3, f4, f5, f6], 10, [rlib.RED, rlib.GREEN, rlib.BLUE], 20, physW, 20, 1)

###--- Main ---###
rlib.init_window(800, 800, "Debug View")
rlib.set_target_fps(frames_that_are_a_second)  ############## A partir de aqui, se asume frames_that_are_a_second frames son un segundo. Asi, si la cosa esta logra correr a 2*frames_that_are_a_second, por ejemplo, la simulacion iria al doble de velocidad

show_image = True

while not rlib.window_should_close():
    basic_controls()

    if rlib.is_mouse_button_pressed(0) and len(sc.fighters) > 0:
        sc.fighters[0].state = fighter_actions.lin_rot_attacking
        sc.fighters[0].destination = xytm(rlib.get_mouse_x(), rlib.get_mouse_y())
    if rlib.is_mouse_button_pressed(1) and len(sc.fighters) > 0:
        sc.fighters[0].state = fighter_actions.braking
    
    if rlib.is_key_pressed(rlib.KeyboardKey.KEY_SPACE):
        show_image = not show_image
    
    if len(sc.fighters) > 0:
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