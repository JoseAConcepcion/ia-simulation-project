from genetics import procs
import json
from scene import *
from globals import *
from simulate import *


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
            team1_pos=[[5, 4], [5, 5]], team2_pos=[[0, -7], [1, -7]], wins_umbral=0.9)
best = ans[0]
hist = ans[1]
resultados = {
    'TeamConfig': list(best[0]),
    'TeamAverageScore': best[1],
    'TeamAverageWinsRate': best[2]
    }
with open('Mejor 5.json','w') as archivo_json:
    json.dump(resultados, archivo_json, indent=4)
with open('Historia 5.json','w') as archivo_json2:
    json.dump(hist, archivo_json2, indent=4)