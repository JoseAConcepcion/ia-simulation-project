# Informe corto del repositorio: **ia-simulation-project**

## Descripción general

Este repositorio contiene un proyecto de simulación de agentes inteligentes (IA) en un entorno físico bidimensional. El objetivo principal es crear, controlar y analizar el comportamiento de "luchadores" o agentes que interactúan en una escena simulada, usando distintas personalidades y mecanismos de toma de decisiones basados en IA.

## Funcionalidad principal según el código

- **Simulación física**: El entorno utiliza la librería Box2D para la simulación física de los agentes, permitiendo modelar cuerpos, colisiones y dinámicas realistas.
- **Agentes luchadores**: Los "Fighters" son agentes con propiedades físicas (densidad, restitución, fuerza, precisión, radio de visión, frecuencia de reacción) y una personalidad asociada que define su comportamiento.
- **Personalidades IA**: El sistema permite asignar diferentes personalidades a los luchadores, modificando sus reglas de decisión y respuesta ante eventos como enemigos cercanos, ataques, o situaciones de emergencia.
- **Toma de decisiones**: Se implementan diversas estrategias de decisión en la clase `RobotDecisionMaker`, permitiendo probar distintos enfoques: estándar, paranoico, planificador, evasivo, experimental, etc.
- **Interfaz visual**: Utiliza la librería `pyray` para mostrar en tiempo real la simulación y permitir interacción mediante el mouse y teclado (por ejemplo, cambiar el destino de un luchador o pausar/resumir la visualización).
- **Pruebas y análisis**: Hay scripts para realizar pruebas entre agentes con distintas configuraciones (formas, tamaños, IA), recolectar resultados y analizar estadísticas de desempeño.
- **NLP y narración**: El proyecto puede generar narrativas automáticas (usando GPT) basadas en los eventos ocurridos en la simulación, permitiendo entender y documentar el comportamiento de los agentes.

## Ejemplo de flujo de uso

1. Se crea una escena con luchadores de diferentes características.
2. Se simula la interacción entre ellos, cada uno siguiendo su personalidad y reglas de IA.
3. Los resultados de la simulación pueden visualizarse y analizarse, generando estadísticas y narrativas de lo sucedido.

## Propósito

El proyecto es útil para experimentar con simulaciones de IA, analizar comportamientos emergentes, comparar distintas estrategias de decisión y facilitar el desarrollo de agentes autónomos en entornos físicos controlados.

---
*El informe se basa en la lectura y análisis del código fuente del repositorio.*
