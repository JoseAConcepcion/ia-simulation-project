import json
import numpy as np
from matplotlib import pyplot as plt
from numpy.ma.core import shape

# # Archivos JSON
# Mejor1 = 'Mejor 1.json'
# Mejor2 = 'Mejor 2.json'
# Mejor3 = 'Mejor 3.json'
# Mejor4 = 'Mejor 4.json'
# Mejor5 = 'Mejor 5.json'
#
# # Lista para almacenar los datos
# best_list = []
# for filename in [Mejor1, Mejor2, Mejor3, Mejor4, Mejor5]:
#     with open(filename, 'r') as file:
#         best_list.append(json.load(file))
#
#
#
# # Características y valores
# feats = ['mass_density', 'restitution', 'linear_strength', 'rotation_strength',
#          'precision', 'view_radius', 'reaction_frequency']
# vals = [[] for _ in range(len(feats))]  # Inicializar la lista de valores
#
# # Extraer los valores de las configuraciones
# for item in best_list:
#     configuration = item['TeamConfig']
#     for i in range(len(feats)):
#         vals[i].append(configuration[0][i])  # Asumiendo que configuration[0][i] es una lista
#         vals[i].append(configuration[1][i])  # Asumiendo que configuration[1][i] es una lista
#
# # Colores para los puntos
# colores = ['red', 'blue', 'orange', 'green', 'yellow']
#
# # Crear la figura y los ejes
# fig, ax = plt.subplots()
#
# # Graficar los valores
# for i in range(len(feats)):
#     ax.scatter([feats[i]] * len(vals[i]), vals[i], color=colores[i % len(colores)], label=feats[i])
#
# # Calcular la media, varianza y desviación estándar de cada característica
# medias = [np.mean(vals[i]) for i in range(len(feats))]
# varianzas = [np.var(vals[i], ddof=1) for i in range(len(feats))]  # Varianza muestral
# desviaciones_estandar = [np.std(vals[i], ddof=1) for i in range(len(feats))]  # Desviación estándar muestral
#
# # Personalizar el gráfico
# ax.set_xlabel('Características')
# ax.set_ylabel('Valores')
# ax.legend()
# plt.title('Gráfico de Dispersión con Estadísticas de Características en los equipos más óptimos de cinco escenarios diferentes')
# plt.grid(True)
#
# # Mostrar las estadísticas debajo de la leyenda
# legend = ax.legend(loc='upper right')
# ax.add_artist(legend)
#
# # Crear un texto con las estadísticas
# estadisticas_texto = '\n'.join(
#     f'{feat}:\n  Media: {media:.2f}\n  Varianza: {varianza:.2f}\n  Desviación Estándar: {desviacion:.2f}'
#     for feat, media, varianza, desviacion in zip(feats, medias, varianzas, desviaciones_estandar)
# )
#
# # Mostrar las estadísticas en el gráfico
# ax.text(1.05, 0.5, estadisticas_texto, transform=ax.transAxes, va='center', fontsize=9)
#
# # Mostrar el gráfico
# plt.show()

#
# Historia1 = 'Historia 1.json'
# Historia2 = 'Historia 2.json'
# Historia3 = 'Historia 3.json'
# Historia4 = 'Historia 4.json'
# Historia5 = 'Historia 5.json'
#
# umbral = 0.9
# # # Características y valores
# feats = ['mass_density', 'restitution', 'linear_strength', 'rotation_strength',
#          'precision', 'view_radius', 'reaction_frequency']
# vals = [[] for _ in range(len(feats))]  # Inicializar la lista de valores
#
# history_list = []
# for filename in [Historia1, Historia2, Historia3, Historia4, Historia5]:
#     with open(filename, 'r') as file:
#         history_list.append(json.load(file))
#
# for scenario in history_list:
#     for generation in scenario.values():
#         for individual in generation:
#             if individual['TeamAverageWinsRate']>=umbral:
#                 configuration = individual['TeamConfig']
#                 for i in range(len(feats)):
#                     vals[i].append(configuration[0][i])  # Asumiendo que configuration[0][i] es una lista
#                     vals[i].append(configuration[1][i])  # Asumiendo que configuration[1][i] es una lista
#
# # Crear la figura y los ejes
# fig, ax = plt.subplots()
#
# # Graficar los valores
# for i in range(len(feats)):
#     ax.scatter([feats[i]] * len(vals[i]), vals[i], label=feats[i])
#
# # Calcular la media, varianza y desviación estándar de cada característica
# medias = [np.mean(vals[i]) for i in range(len(feats))]
# varianzas = [np.var(vals[i], ddof=1) for i in range(len(feats))]  # Varianza muestral
# desviaciones_estandar = [np.std(vals[i], ddof=1) for i in range(len(feats))]  # Desviación estándar muestral
#
# # Personalizar el gráfico
# ax.set_xlabel('Características')
# ax.set_ylabel('Valores')
# ax.legend()
# plt.title(f'Gráfico de Dispersión con Estadísticas de Características en los equipos con promedio de victorias superior a {umbral} de cinco escenarios diferentes')
# plt.grid(True)
#
# # Mostrar las estadísticas debajo de la leyenda
# legend = ax.legend(loc='upper right')
# ax.add_artist(legend)
#
# # Crear un texto con las estadísticas
# estadisticas_texto = '\n'.join(
#     f'{feat}:\n  Media: {media:.2f}\n  Varianza: {varianza:.2f}\n  Desviación Estándar: {desviacion:.2f}'
#     for feat, media, varianza, desviacion in zip(feats, medias, varianzas, desviaciones_estandar)
# ) + f'\nTotal de individuos: {len(vals[0])}'
#
# # Mostrar las estadísticas en el gráfico
# ax.text(1.05, 0.5, estadisticas_texto, transform=ax.transAxes, va='center', fontsize=9)
#
# # Mostrar el gráfico
# plt.show()


#
# Historia1 = 'Historia 1.json'
# Historia2 = 'Historia 2.json'
# Historia3 = 'Historia 3.json'
# Historia4 = 'Historia 4.json'
# Historia5 = 'Historia 5.json'
#
#
# # # Características y valores
# feats = ['mass_density', 'restitution', 'linear_strength', 'rotation_strength',
#          'precision', 'view_radius', 'reaction_frequency']
#
#
# history_list = []
# for filename in [Historia1, Historia2, Historia3, Historia4, Historia5]:
#     with open(filename, 'r') as file:
#         history_list.append(json.load(file))
#
# total_means = []
# total_std = []
# for umbral in range(10):
#     vals = [[] for _ in range(len(feats))]  # Inicializar la lista de valores
#     for scenario in history_list:
#         for generation in scenario.values():
#             for individual in generation:
#                 if individual['TeamAverageWinsRate']>=umbral/10:
#                     configuration = individual['TeamConfig']
#                     for i in range(len(feats)):
#                         vals[i].append(configuration[0][i])  # Asumiendo que configuration[0][i] es una lista
#                         vals[i].append(configuration[1][i])  # Asumiendo que configuration[1][i] es una lista
#     # Calcular la media y desviación estándar de cada característica
#     medias = [np.mean(vals[i]) for i in range(len(feats))]
#     total_means.append(medias)
#
#     desviaciones_estandar = [np.std(vals[i], ddof=1) for i in range(len(feats))]  # Desviación estándar muestral
#     total_std.append(desviaciones_estandar)
#
#
# means_mass_vals = np.array(total_means)[:,0]
# means_restitution = np.array(total_means)[:,1]
# means_lin_str = np.array(total_means)[:,2]
# means_rot_str = np.array(total_means)[:,3]
# means_precision = np.array(total_means)[:,4]
# means_view = np.array(total_means)[:,5]
# means_react = np.array(total_means)[:,6]
#
# plt.plot([i for i in range(0,100,10)],means_mass_vals)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio de la masa')
# plt.title('Comportamiento del valor medio de la masa con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio de la masa con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],means_restitution)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio de la restitucion')
# plt.title('Comportamiento del valor medio de la restitucion con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio de la restitucion con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],means_lin_str)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio de la fuerza lineal')
# plt.title('Comportamiento del valor medio de la fuerza lineal con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio de la fuerza lineal con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],means_rot_str)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio de la fuerza rotativa')
# plt.title('Comportamiento del valor medio de la fuerza rotativa con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio de la fuerza rotativa con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],means_precision)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio de la precision')
# plt.title('Comportamiento del valor medio de la precision con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio de la precision con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],means_view)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio del rango de visibilidad')
# plt.title('Comportamiento del valor medio del rango de visibilidad con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio del rango de visibilidad con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],means_react)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Valor medio de la frecuencia de actualizazion')
# plt.title('Comportamiento del valor medio de la frecuencia de actualizazion con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento del valor medio de la frecuencia de actualizazion con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
#
#
#
# std_mass_vals = np.array(total_std)[:,0]
# std_restitution = np.array(total_std)[:,1]
# std_lin_str = np.array(total_std)[:,2]
# std_rot_str = np.array(total_std)[:,3]
# std_precision = np.array(total_std)[:,4]
# std_view = np.array(total_std)[:,5]
# std_react = np.array(total_std)[:,6]
#
# plt.plot([i for i in range(0,100,10)],std_mass_vals)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Std de la masa')
# plt.title('Comportamiento de la Std de la masa con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std de la masa con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],std_restitution)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Stdde la restitucion')
# plt.title('Comportamiento de la Std de la restitucion con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std de la restitucion con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],std_lin_str)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Std de la fuerza lineal')
# plt.title('Comportamiento de la Std de la fuerza lineal con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std de la fuerza lineal con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],std_rot_str)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Std de la fuerza rotativa')
# plt.title('Comportamiento de la Std de la fuerza rotativa con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std de la fuerza rotativa con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],std_precision)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Std de la precision')
# plt.title('Comportamiento de la Std de la precision con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std de la precision con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],std_view)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Std del rango de visibilidad')
# plt.title('Comportamiento de la Std del rango de visibilidad con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std del rango de visibilidad con respecto al porcentaje de victorias obtenidas')
# plt.show()
#
# plt.plot([i for i in range(0,100,10)],std_react)
# plt.xlabel('Porcentaje de victorias')
# plt.ylabel('Std de la frecuencia de actualizazion')
# plt.title('Comportamiento de la Std de la frecuencia de actualizazion con respecto al porcentaje de victorias obtenidas')
# plt.savefig('./Comportamiento de la Std de la frecuencia de actualizazion con respecto al porcentaje de victorias obtenidas')
# plt.show()

# Historia1 = 'Historia 1.json'
# Historia2 = 'Historia 2.json'
# Historia3 = 'Historia 3.json'
# Historia4 = 'Historia 4.json'
# Historia5 = 'Historia 5.json'
#
# history_list = []
# for filename in [Historia1, Historia2, Historia3, Historia4, Historia5]:
#     with open(filename, 'r') as file:
#         history_list.append(json.load(file))
# gen_average_wins_rate = [0,0,0,0,0,0,0,0,0,0]
#
# for scenario in history_list:
#     gen = 0
#     for generation in scenario.values():
#         rate = 0
#         for individual in generation:
#             rate += individual['TeamAverageWinsRate']
#         gen_average_wins_rate[gen] += rate/50
#         gen +=1
# plt.plot([i for i in range(10)], np.array(gen_average_wins_rate)*100)
# plt.xlabel('Generacion')
# plt.ylabel('Porcentaje de victorias')
# plt.title('Comportamiento del porcentaje de victorias promedio con respecto a la generacion')
# plt.show()
#
