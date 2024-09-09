from fighter import *
from brain import FighterBrain
from globals import *

#--- Events ---#
class DeathEvent:
    def __init__(self, fighter_id, team_id, team_lost, t):
        self.fighter_id = fighter_id
        self.team_id = team_id
        self.team_lost = team_lost
        self.t = t

class ClashEvent:
    def __init__(self, fighter1_id, fighter1_team_id, fighter1_v, fighter1_w, fighter2_id, fighter2_team_id, fighter2_v, fighter2_w, t):
        self.fighter1_id = fighter1_id
        self.fighter1_v = fighter1_v
        self.fighter1_w = fighter1_w
        self.fighter1_team_id = fighter1_team_id

        self.fighter2_id = fighter2_id
        self.fighter2_v = fighter2_v
        self.fighter2_w = fighter2_w
        self.fighter2_team_id = fighter2_team_id

        self.t = t

class EndEvent:
    def __init__(self, was_win, winner_team_id, t):
        self.was_win = was_win
        self.winner_team_id = winner_team_id
        self.t = t

class ShrinkingStartsEvent:
    def __init__(self, t):
        self.t = t

#--- Result ---#
class SceneResult:
    def __init__(self):
        self.duration = -1
        self.death_events = []
        self.was_draw = True
        self.winner_team_id = -1

        self.event_log = []

#--- Graph ---#
class Path_Graph_Node:
    def __init__(self, pos):
        self.pos = pos
        self.fighters_on_it = []
        self.distance_from_border = -1 #positive if inside, negative if outside

#--- Scene ---#
scene_states = Enum("scene_states", "in_process winner draw")
class Scene:
    def __init__(self, fighters: Fighter, field_initial_r: float, team_colors, graph_axial_count, physicsWorld, seconds_to_start_shrinking_r = 3, r_shrink_velocity = 0.3):
        self.fighters = fighters
        self.field_r = field_initial_r

        self.physicsWorld = physicsWorld

        self.state = scene_states.in_process
        self.graph_axial_count = graph_axial_count
        self.team_colors = team_colors

        self.seconds_since_init = 0
        self.seconds_to_start_shrinking_r = seconds_to_start_shrinking_r
        self.r_shrink_velocity = r_shrink_velocity
        
        #Graph
        self.graph = []
        scene_sidelength = field_initial_r+2
        for x_i in range(-graph_axial_count, graph_axial_count+1):
            self.graph.append([])
            for y_i in range(-graph_axial_count, graph_axial_count+1):
                self.graph[x_i+graph_axial_count].append(Path_Graph_Node((scene_sidelength*x_i/graph_axial_count, scene_sidelength*y_i/graph_axial_count)))
        self.update_graph()

        #Fighters
        for f,i in zip(self.fighters, range(len(self.fighters))):
            f.id = i
            f.color = team_colors[f.team_id]
            f.path_graph = self.graph
            f.path_graph_axial_count = graph_axial_count
            f.body.userData = f.id

        #Contact timer (time passed between a and b colliding)
        self.contact_time_separation = 0.3
        self.contact_timer = []
        for i in range(len(self.fighters)):
            self.contact_timer.append([])
            for ii in range(len(self.fighters)):
                self.contact_timer[i].append(0)

        #Result
        self.sceneResult = SceneResult()
        self.recorded_shrink_begining = False

    def update_graph(self):
        for x_i in range(0, 2*self.graph_axial_count+1):
            for y_i in range(0, 2*self.graph_axial_count+1):
                node = self.graph[x_i][y_i]
                node.distance_from_border = self.field_r-math.sqrt(node.pos[0]**2 + node.pos[1]**2)
                
                node.fighters_on_it = []
                for f in self.fighters:
                    if (f.position[0]-node.pos[0])**2 + (f.position[1]-node.pos[1])**2 <= f.bounding_r**2:
                        node.fighters_on_it.append(f)

    def update(self):
        self.seconds_since_init += dt
        
        #Update Graph
        self.update_graph()

        #Update Contact Timers
        for i in range(len(self.fighters)):
            for ii in range(len(self.fighters)):
                self.contact_timer[i][ii] += dt

        #Update Fighters
        for f in self.fighters:
            f.path_graph = self.graph
            f.update()
            f.distance_from_border = self.field_r-math.sqrt(f.position.x**2 + f.position.y**2)
            f.fighters_in_sight = []
            for f_2 in self.fighters:
                if f_2.id == f.id:
                    continue
                if (f.position.x-f_2.position.x)**2 + (f.position.y-f_2.position.y)**2 <= f.view_radius**2:
                    f.fighters_in_sight.append(f_2)

        #Update World
        self.physicsWorld.Step(dt, 10, 10)
        
        #See if somebody won
        if self.sceneResult.duration <= 0:
            teams_still_playing = []
            for f in self.fighters:
                if f.team_id not in teams_still_playing:
                    teams_still_playing.append(f.team_id)

            if len(teams_still_playing) == 1:
                self.state = scene_states.winner
                self.sceneResult.duration = self.seconds_since_init
                self.sceneResult.was_draw = False
                self.sceneResult.winner_team_id = self.fighters[0].team_id
                self.sceneResult.event_log.append(EndEvent(True, self.fighters[0].team_id, self.seconds_since_init))
            
            if len(teams_still_playing) == 0:
                self.state = scene_states.draw
                self.sceneResult.duration = self.seconds_since_init
                self.sceneResult.was_draw = True
                self.sceneResult.event_log.append(EndEvent(False, -1, self.seconds_since_init))

        #Shrink field
        if self.seconds_since_init >= self.seconds_to_start_shrinking_r and (self.field_r-self.r_shrink_velocity*dt)>0:
            if not self.recorded_shrink_begining:
                self.sceneResult.event_log.append(ShrinkingStartsEvent(self.seconds_since_init))
                self.recorded_shrink_begining = True
            self.field_r -= self.r_shrink_velocity*dt
        
        #Contact between bodies
        for f in self.fighters:
            for contact_edge in f.body.contacts:
                if contact_edge.contact.touching:
                    fighter1_id = contact_edge.contact.fixtureA.body.userData
                    fighter2_id = contact_edge.contact.fixtureB.body.userData
                    if self.contact_timer[fighter1_id][fighter2_id] >= self.contact_time_separation:
                        self.contact_timer[fighter1_id][fighter2_id] = 0
                        self.contact_timer[fighter2_id][fighter1_id] = 0
                        
                        f1 = None
                        f2 = None
                        for fighter in self.fighters:
                            if fighter.id == fighter1_id:
                                f1 = fighter
                            if fighter.id == fighter2_id:
                                f2 = fighter
                            if f1 != None and f2 != None:
                                break
                        
                        self.sceneResult.event_log.append(ClashEvent(f1.id, f1.team_id, f1.body.linearVelocity, f1.body.angularVelocity, 
                        f2.id, f2.team_id, f2.body.linearVelocity, f2.body.angularVelocity,     self.seconds_since_init))
        
        #Out of field
        for f in self.fighters:
            if f.position.x**2 + f.position.y**2 > self.field_r**2:
                team_count = 0
                for f2 in self.fighters:
                    if f2.team_id == f.team_id:
                        team_count += 1
                
                team_lost = False
                if team_count == 1:
                    team_lost = True
                
                self.sceneResult.death_events.append(DeathEvent(f.id, f.team_id, team_lost, self.seconds_since_init))
                self.sceneResult.event_log.append(DeathEvent(f.id, f.team_id, team_lost, self.seconds_since_init))
                
                self.physicsWorld.DestroyBody(f.body)
                self.fighters.remove(f)

    def draw(self):
        rlib.clear_background(rlib.WHITE)
        
        draw_parametric(lambda t: (self.field_r*math.cos(t), self.field_r*math.sin(t)), 0, 2*math.pi, 100, color = rlib.RED)
        for f in self.fighters:
            f.draw()

        if self.state == scene_states.winner:
            rlib.draw_text(f"Team {self.sceneResult.winner_team_id} wins!!!", 0, 0, 20, self.team_colors[self.sceneResult.winner_team_id])
        elif self.state == scene_states.draw:
            rlib.draw_text(f"It's a Draw!!!", 0, 0, 20, rlib.RED)

        #Graph Debug
        if graph_debug_draw:
            for y_i in range(0, 2*self.graph_axial_count+1):
                for x_i in range(0, 2*self.graph_axial_count+1):
                    node = self.graph[x_i][y_i]
                    p = node.pos
                    c = rlib.BLACK
                    if len(self.fighters) > 0:
                        if (x_i, y_i) == self.fighters[0].s_node:
                            c = rlib.YELLOW
                        elif (x_i, y_i) == self.fighters[0].e_node:
                            c = rlib.MAGENTA
                        elif (x_i, y_i) in self.fighters[0].path:
                            c = rlib.BROWN
                        elif len(node.fighters_on_it) > 0:
                            c = self.team_colors[node.fighters_on_it[0].team_id]
                    
                    rlib.draw_circle(xtc(p[0]), ytc(p[1]), 4, c)