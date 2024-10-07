import numpy as np
import random

from scene import *
from globals import *
from simulate import *
"""
rows -> number of teams (int)
cols -> number of features (int)
    #Properties
        self.mass_density = 1 - 15
        self.restitution = 0 - 8
        self.max_linear_strength = 50 - 500
        self.max_rotation_strength = 10 - 100
        self.precision = 0 - 1  
        self.view_radius = 2 - 20
        self.reaction_frequency = 1 - 10

weights -> feature's weights (list of int)
max_sum_c -> upper bound for the weighted sum of the features values and weights (int)
number_of_matrix -> number of individuals for each generation (int)
number_of_generations -> number of generations (int)
iter_per_matrix -> number of simulations run on each individual to compute the average score of that individual (int)
team1, team2 -> teams that we must defeat (Each is a list of fighters)
mutation_rate -> probability of mutation (float between 0 and 1)
initial_pos -> initial positions of the team we want to evolve
"""
indexes = {
        '0':[1,15],
        '1':[0 + np.finfo(float).eps,8],
        '2':[50,500],
        '3':[10,100],
        '4':[0 + np.finfo(float).eps,1],
        '5':[2,20],
        '6':[1,10]
    }
def simulate(team1, team2, team3:np.ndarray,rows,initial_pos, team_colors,team1_pos, team2_pos):
    physW = world(gravity=(0, 0))  # Cada vez que creas una escena, hay que crear un mundo físico nuevo, exactamente esta línea y ya
    fighters = []
    for i in range(rows):
        f = Fighter(initial_pos[i], 0, physW)
        poly1 = [[0, 1], [-1, 0], [1, 0]]  # Los polígonos pueden un input que se le da al algoritmo genético, junto con las propiedades del resto de los fighters
        f.add_polygon(poly1)
        f.add_prop(list(team3[i]))
        fighters.append(f)
    for i in range(rows):
        f = Fighter(team1_pos[i], 1, physW)
        poly1 = [[0, 1], [-1, 0], [1,0]]  # Los polígonos pueden un input que se le da al algoritmo genético, junto con las propiedades del resto de los fighters
        f.add_polygon(poly1)
        f.add_prop(list(team1[i]))
        fighters.append(f)
    for i in range(rows):
        f = Fighter(team2_pos[i], 2, physW)
        poly1 = [[0, 1], [-1, 0], [1,0]]  # Los polígonos pueden un input que se le da al algoritmo genético, junto con las propiedades del resto de los fighters
        f.add_polygon(poly1)
        f.add_prop(list(team2[i]))
        fighters.append(f)
    sc = Scene(fighters, 10, team_colors, 20, physW, 5, 1)
    score = simulate_scene_until_battle_ends(sc)
    return (score, sc.sceneResult)


def generate_init_team(rows,cols,weights,max_sum_c):
    matrix = np.random.uniform(size=(rows, cols))
    matrix[:, 0] = np.random.uniform(low=1, high=15, size = rows)
    matrix[:, 1] = np.random.uniform(low=0 + np.finfo(float).eps, high=8, size = rows)
    matrix[:, 2] = np.random.normal(loc=150, size = rows, scale=50/3)
    for i in range(rows):
        if matrix[i,2] < indexes['2'][0]:
            matrix[i,2] = indexes['2'][0]
        if matrix[i,2] > indexes['2'][1]:
            matrix[i, 2] = indexes['2'][1]

    matrix[:, 3] = np.random.normal(loc=45,scale=55/3, size=rows)
    for i in range(rows):
        if matrix[i,3] < indexes['3'][0]:
            matrix[i,3] = indexes['3'][0]
        if matrix[i,3] > indexes['3'][1]:
            matrix[i, 3] = indexes['3'][1]

    matrix[:, 4] = np.random.uniform(low=0 + np.finfo(float).eps, high=1, size=rows)
    matrix[:, 5] = np.random.uniform(low=2, high=20, size=rows)
    matrix[:, 6] = np.random.uniform(low=1, high=10, size=rows)
    for i in range(rows):
        if np.matmul(matrix[i],weights) > max_sum_c:
            matrix[i] = np.multiply(np.divide(matrix[i], np.sum(matrix[i])),max_sum_c)
            print(sum(matrix[i]))
    return matrix
def procs(rows,cols,weights,max_sum_c,number_of_matrix, iter_per_matrix,
          team1, team2, mutation_rate, number_of_generations,initial_pos, team_colors,
          team1_pos, team2_pos):

    matrixs  = []
    history = {

    }
    for c in range(number_of_matrix):
        matrix = generate_init_team(rows,cols,weights, max_sum_c)
        matrixs.append([matrix,0,0])
    gen = 0
    best = [np.zeros(shape=(rows,cols)),0,0]
    while True:
        if gen >= number_of_generations:
            break
        # Obtener los scores simulando
        generation_score = 0
        generation_win_rate = 0
        found_top = False
        history[f'Gen {gen}'] = []
        for matrix in matrixs:
            score = 0
            wins_rate = 0
            for s in range(iter_per_matrix):
                sim_result = simulate(team1,team2,matrix[0], rows, initial_pos, team_colors,team1_pos, team2_pos)
                score+=sim_result[0]
                # print(sim_result[1].winner_team_id)
                if sim_result[1].winner_team_id == 0: wins_rate += 1
            matrix[1]=score/iter_per_matrix
            matrix[2] = wins_rate/iter_per_matrix
            history[f'Gen {gen}'].append({
            'TeamConfig': matrix[0].tolist(),
            'TeamAverageScore': matrix[1],
            'TeamAverageWinsRate': matrix[2]
            })
            generation_score += matrix[1]
            generation_win_rate += matrix[2]
            # if wins_rate/iter_per_matrix >=0.9:
            #     best = matrix.copy()
            #     found_top = True
            #     break
        #     print(f'Team structure: {matrix}\n'
        #           f'Generation: {gen}\n'
        #           f'Average score: {matrix[1]}\n'
        #           f'Wins rate: {wins_rate/iter_per_matrix}\n')
        #
        # print(f"Generation: {gen}\n"
        #       f"Generation Average Score: {generation_score/number_of_matrix}\n"
        #       f"Generation Average Wins Rate: {generation_win_rate/number_of_matrix}\n")
        if found_top: break
        # Ordenar los resultado por scores
        matrixs.sort(key=lambda x: x[1], reverse=True)
        if matrixs[0][1] > best[1]:
            best = matrixs[0].copy()

        # Convertir los scores en probabilidades
        performance = 0
        performance += sum([matrix[1] for matrix in matrixs])
        selections = []
        prob = []
        counter = 0
        for matrix in matrixs:
            matrix[1]/=performance
            selections.append(counter)
            prob.append(matrix[1])
            counter+=1

        new_generation = [[matrixs[0][0], 0, 0]]
        for i in range(len(matrixs)):
            if matrixs[i][2]<=0.1:
                matrixs[i][0] = generate_init_team(rows, cols, weights, max_sum_c)
        for i in range(number_of_matrix-1):
            # Seleccionar par de ancestros
            parents = np.random.choice(selections, size = 2, p = prob, replace=False)

            # Reproducir
            cross_point = random.randint(0,rows - 1)
            new_item = np.ndarray(shape=(rows,cols))

            for j in range(0,cross_point+1):
                new_item[j] = matrixs[parents[0]][0][j]
            for j in range(cross_point,rows):
                new_item[j] = matrixs[parents[1]][0][j]


            # Mutar
            if random.random()<mutation_rate:
                ind = random.randint(0,rows-1)
                feat = random.randint(0,cols-1)
                low = -(new_item[ind][feat] - indexes[str(feat)][0])
                high = min(max_sum_c - np.matmul(new_item[ind], weights),indexes[str(feat)][1]-new_item[ind][feat])
                mutation = np.random.uniform(low=0+np.finfo(float).eps,high=1)*(high - low) + low
                new_item[ind][feat] += mutation
                print(sum(new_item[ind]))

            new_individual = [new_item, 0,0]
            new_generation.append(new_individual)
        matrixs = new_generation
        gen+=1
    return  ([best[0].tolist(),best[1],best[2]],history)

ans = procs(2, 7, [1, 1, 1, 1, 1, 1, 1], 700, 10, 10,
            mutation_rate=0.1, number_of_generations=10,
            team1=[[
            6.91256418840724,
            2.7436333702303246,
            119.70132284465502,
            29.69908605912442,
            0.6912526628726278,
            14.888898232865325,
            6.546618728041965
        ],
        [
            6.181774760473667,
            6.637099819715674,
            134.97630366386784,
            64.03925811513054,
            0.8723730664365065,
            8.220554503747655,
            6.051123341435527
        ]],
            team2=[[
            10.202890083412314,
            4.651189868745294,
            370.11624525116355,
            61.202943329227324,
            0.6641773722665317,
            7.229883201934273,
            3.2136480435175816
        ],
        [
            7.145214065108561,
            0.5058498832549205,
            172.0716171400784,
            55.4915365029811,
            0.8087325750552578,
            4.611217541324355,
            1.446419508460414
        ]],
            initial_pos=[[-5, 4], [-5, 5]], team_colors=[rlib.RED, rlib.GREEN, rlib.BLUE],
            team1_pos=[[5, 4], [5, 5]], team2_pos=[[0, -7], [1, -7]])

