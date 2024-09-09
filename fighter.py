from brain import FighterBrain
from globals import *
import math
from queue import SimpleQueue
import random

class Fighter:
    def __init__(self, position, team_id, physicsWorld, personality = fighter_standard_personality):
        
        #--- Internals (NOT For AI) ---#
        self.polygons = []
        self.team_id = team_id
        self.personality = personality
        
        self.position = position
        self.body = physicsWorld.CreateDynamicBody(position=position)
        self.id = -1
        self.color = rlib.BLACK
        self.bounding_r = -1
        self.seconds_since_last_plan = 0
        self.brain = FighterBrain()
        self.path_graph = []
        self.path_graph_axial_count = 0

        self.seconds_between_move_updates = 0.1
        self.seconds_since_last_move_update = 0

        self.sub_destination = (0,0)

        self.s_node = None
        self.e_node = None
        self.path = []

        #--- For AI ---#

        #Data
        self.distance_from_border = 1000
        self.fighters_in_sight = []
        
        #Desires
        self.state = fighter_actions.braking #La accion actual. Una de 'fighter_actions'
        self.destination = None #A dónde está caminando o atacando

        #Properties
        self.mass_density = 3
        self.restitution = 1.6    #Qué tanto rebota
        self.max_linear_strength = 100
        self.max_rotation_strength = 40
        self.precision = 0.8     #simpre está entre 0 y 1.    0 = apunta random, no a donde le dices    1 = apunta exactamente en la direccion que le dices
        self.view_radius = 6
        self.reaction_frequency = 1/0.3  #1/(Cuantos segundos pasan entre llamadas a la funcion de planificacion del agente)

    def add_polygon(self, vetexList):
        self.polygons.append(vetexList)
        shape = polygonShape(vertices=vetexList)
        fixture = fixtureDef(shape=shape, density=self.mass_density, restitution=self.restitution)
        self.body.CreateFixture(fixture)

        #Update Radius
        new_r = -1
        self.position = self.body.worldCenter
        for fixture in self.body.fixtures:
            poly = fixture.shape.vertices
            for i in range(0, len(poly)):
                p = self.body.transform*poly[i]
                dist = math.sqrt((self.position[0]-p[0])**2 + (self.position[1]-p[1])**2)
                if dist > new_r:
                    new_r = dist
        self.bounding_r = new_r
    
    def update(self):
        self.position = self.body.worldCenter
        self.seconds_since_last_plan += dt
        self.seconds_since_last_move_update += dt
        
        if self.seconds_since_last_plan >= 1/self.reaction_frequency and fighters_use_AI:
            self.brain.plan(self) #Think Mark, think! Dutch has a GODDAMN PLAN!
            self.seconds_since_last_plan = 0

        #Frictions
        self.applyFrictions()

        #Execute plan
        if self.state == fighter_actions.moving:
            self.moveTo(self.destination)
        elif self.state == fighter_actions.braking:
            self.brake()
        elif self.state == fighter_actions.lin_attacking:
            self.lin_attackTo(self.destination)
        elif self.state == fighter_actions.rot_attacking:
            self.rot_attack()
        elif self.state == fighter_actions.lin_rot_attacking:
            self.lin_rot_attackTo(self.destination)

    def draw(self):
        for fixture in self.body.fixtures:
            poly = fixture.shape.vertices
            for i in range(0, len(poly)):
                p1 = self.body.transform*poly[i]
                p2 = self.body.transform*poly[(i+1)%len(poly)]
                rlib.draw_line(xtc(p1[0]), ytc(p1[1]), xtc(p2[0]), ytc(p2[1]), self.color)
            
        rlib.draw_circle(xtc(self.body.worldCenter[0]), ytc(self.body.worldCenter[1]), 4, rlib.BLACK)

    def find_nearest_free_node_in_graph(self, p):
        min_dist_sqrd = 100000000
        min_node = (0,0)
        for x_i in range(0, 2*self.path_graph_axial_count+1):
            for y_i in range(0, 2*self.path_graph_axial_count+1):
                node = self.path_graph[x_i][y_i]
                
                if node.distance_from_border < 0 or (len(node.fighters_on_it) > 0 and node.fighters_on_it[0].id != self.id):
                    continue

                dst = (p[0]-node.pos[0])**2+(p[1]-node.pos[1])**2
                if dst < min_dist_sqrd:
                    min_node = (x_i, y_i)
                    min_dist_sqrd = dst
        return min_node

    def moveTo(self, destination):
        if self.seconds_since_last_move_update < self.seconds_between_move_updates: 
            self.lin_attackTo(self.sub_destination)
            return
        self.seconds_since_last_move_update = 0
        
        self.s_node = self.find_nearest_free_node_in_graph(self.position)
        self.e_node = self.find_nearest_free_node_in_graph(destination)
        
        #Parent grid (who added you to the queue)
        parent_grid = []
        for x_i in range(0, 2*self.path_graph_axial_count+1):
            parent_grid.append([])
            for y_i in range(0, 2*self.path_graph_axial_count+1):
                parent_grid[-1].append(None)
        parent_grid[self.s_node[0]][self.s_node[1]] = self.s_node

        #BFS
        q = SimpleQueue()
        q.put(self.s_node)
        
        coords = None
        while not q.empty():
            coords = q.get()
            if coords == self.e_node:
                break

            next_coords = [(coords[0]+1, coords[1]), (coords[0]-1, coords[1]), (coords[0],   coords[1]+1), (coords[0],   coords[1]-1),
                           (coords[0]+1, coords[1]+1), (coords[0]-1, coords[1]-1), (coords[0]-1,   coords[1]+1), (coords[0]+1,   coords[1]-1)]

            for c in next_coords:
                node = self.path_graph[c[0]][c[1]]
                if node.distance_from_border < 0 or (len(node.fighters_on_it) > 0 and node.fighters_on_it[0].id != self.id) or parent_grid[c[0]][c[1]] != None:
                    continue
                q.put(c)
                parent_grid[c[0]][c[1]] = coords

        #Recover path
        self.path = [coords]
        while True:
            coords = parent_grid[coords[0]][coords[1]]
            self.path.insert(0, coords)
            if coords == self.s_node:
                break
            
        if len(self.path) >= 2:
            self.sub_destination = self.path_graph[self.path[1][0]][self.path[1][1]].pos
        else:
            self.sub_destination = self.path_graph[self.path[0][0]][self.path[0][1]].pos
            
    def rot_attack(self):
        torque = self.max_rotation_strength
        self.body.ApplyTorque(torque=torque, wake=True)

    def lin_attackTo(self, location):
        #Apply imprecision
        d = rlib.Vector2(location[0]-self.position.x, location[1]-self.position.y)
        d_norm = math.sqrt(d.x**2 + d.y**2)
        d_ang = math.atan2(d.y, d.x)

        max_ang_var = (1-self.precision)*math.tau/2
        d_ang += 2*max_ang_var*random.random() - max_ang_var

        d = rlib.Vector2(d_norm*math.cos(d_ang), d_norm*math.sin(d_ang))

        #Attack
        if d_norm > 0.001:
            force = (d.x / d_norm * self.max_linear_strength, d.y / d_norm * self.max_linear_strength)
            self.body.ApplyForce(force=force, point=self.body.worldCenter, wake=True)        

    def lin_rot_attackTo(self, location):
        self.lin_attackTo(location)
        self.rot_attack()
    
    def brake(self):
        v = self.body.linearVelocity
        
        force = (-3 * v.x, -3 * v.y)
        force_abs = math.sqrt(force[0]**2 + force[1]**2)
        if force_abs > self.max_linear_strength:
            force = (force[0] / force_abs * self.max_linear_strength, force[1] / force_abs * self.max_linear_strength)
        self.body.ApplyForce(force=force, point=self.body.worldCenter, wake=True)

        w = self.body.angularVelocity
        torque = -1 * w
        if math.fabs(torque) > self.max_rotation_strength:
            torque = torque / math.fabs(torque) * self.max_rotation_strength
        self.body.ApplyTorque(torque=torque, wake=True)

    def applyFrictions(self):
        center = self.body.worldCenter
        v = self.body.linearVelocity
        self.body.ApplyForce(force=-2*v, point=center, wake=True)
        w = self.body.angularVelocity
        self.body.ApplyTorque(torque=-2*w, wake=True)