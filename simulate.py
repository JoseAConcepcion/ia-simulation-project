from scene import *
from globals import *

###--- Debug Window Init ---###
rlib.init_window(800, 800, "Debug View")
show_image = True
if show_image: rlib.set_target_fps(frames_that_are_a_second)
else: rlib.set_target_fps(3000000)

###--- Simulator function ---###
def simulate_scene_until_battle_ends(sc: Scene):
    global show_image
    
    #Simulate
    while True:
        if rlib.window_should_close():
            exit()

        if rlib.is_key_pressed(rlib.KeyboardKey.KEY_SPACE):
            show_image = not show_image
            if show_image: rlib.set_target_fps(frames_that_are_a_second)
            else: rlib.set_target_fps(3000000)
        
        rlib.begin_drawing()
        if show_image:
            sc.draw()
        else:
            rlib.clear_background(rlib.BLACK)
            rlib.draw_text(f"Simulando en segundo plano (pulsar espacio para ver)...", 30, 30, 20, rlib.BLUE)
        rlib.end_drawing()
        
        sc.update()
        if sc.sceneResult.duration > 0:
            break
    
    rlib.clear_background(rlib.BLACK)
    rlib.draw_text(f"Pasando a otra escena...", 30, 30, 20, rlib.RED)

    #Evaluate results (assumes team 0 is the one being evaluated)
    evaluation = 0

    if sc.sceneResult.winner_team_id == 0:
        
        dead_teammates = 0
        for death_event in sc.sceneResult.death_events:
            if death_event.team_id == 0:
                dead_teammates += 1

        evaluation = 80 + 10/sc.sceneResult.duration - 7*dead_teammates
    
    for i,death_event in enumerate(sc.sceneResult.death_events):
        if death_event.team_id == 0:
            evaluation += 2*i
    
    evaluation = min(evaluation, 100)

    return evaluation