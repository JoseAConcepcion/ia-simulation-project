from scene import *
from globals import *
from simulate import *

if __name__ == "__main__":

    ###--- Ejemplo de uso de simulate_scene_until_battle_ends ---###
    #Al ejecutar esta cosa, se debería abrir una ventana, y comenzar a ejecutar las simulaciones lo más rápido posible. Si en cualquier punto quieres ver 
    #qué está pasando, pulsa espacio (y espacio de nuevo para seguir simulando a máxima velocidad).

    physW = world(gravity=(0, 0)) #Cada vez que creas una escena, hay que crear un mundo físico nuevo, exactamente esta línea y ya

    f1 = Fighter([-5,4], 0, physW) #Igualmente, los fighter no se deben compartir entre partidas, hay que crearlo nuevo cada vez, aunque sea con las mismas propiedades
    f1.precision = 0.9 #Después de instanciado el objeto, se setean las propiedades
    poly1 = [[0,1], [-1,0], [1,0]] #Los polígonos pueden un input que se le da al algoritmo genético, junto con las propiedades del resto de los fighters
    f1.add_polygon(poly1)

    f2 = Fighter([0,0], 0, physW) #Se asume que el equipo 0 es el que está evolucionando, y por tanto que es al que se le puntúa la actuación 
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

    #Para crear una escena creo que el único parámetro que no se explica solo es graph_axial_count. Esto es como la densidad del grafo que usan los tipos pa moverse. Déjalo en 20, que ha pinchado bien. Y por cierto, si son 3 equipos, dejale estos colores pa identificarlos rápido (RGB) ;)
    sc = Scene([f1, f2, f3, f4, f5, f6], 10, [rlib.RED, rlib.GREEN, rlib.BLUE], 20, physW, 1, 2)

    #Y así se llama a simulate. Cualquier duda you know, pregunta.
    score = simulate_scene_until_battle_ends(sc)
    print(score)


