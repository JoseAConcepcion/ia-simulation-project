# Proyecto de Simulación de IA

Este proyecto simula escenarios de combate entre agentes controlados por algoritmos de inteligencia artificial, permitiendo experimentar y comparar diferentes estrategias, características físicas y comportamientos en equipos de "Fighters". El código incluye componentes para la definición de agentes, su física, toma de decisiones autónoma, y análisis estadístico y evolutivo de los resultados.

Los agentes ("Fighters") tienen propiedades como masa, restitución, fuerza, precisión, radio de visión y frecuencia de reacción, y pueden ser controlados mediante diferentes personalidades y algoritmos de decisión (estándar, paranoico, planificador, evasivo, etc.). Se implementan pruebas con equipos de diferentes tamaños, formas y estrategias, y se analizan los resultados de las simulaciones con técnicas evolutivas (algoritmos genéticos).

Entre sus módulos principales destacan:
- **fighter.py** y **scene.py**: Definen los agentes y el entorno físico.
- **DecisionMaker.py**: Implementa varios algoritmos de decisión para los agentes.
- **genetics.py** y **simulation results/**: Permite la evolución de comportamientos y el análisis estadístico de los resultados.
- **main.py** y los archivos de prueba: Ejecutan simulaciones y escenarios comparativos.

El proyecto está diseñado como un entorno de pruebas para el estudio de IA en simulaciones físicas y estratégicas, brindando herramientas para la comparación y evolución automática de distintos tipos de agentes.

## Integrantes
- Alejandro García González C-311 [Github](https://github.com/ajper256)
- Ernesto Alejandro Bárcena Trujillo C-311 [Github](https://github.com/Barccena05)
- José Antonio Concepción Álvarez C-311 [Github](https://github.com/JoseAConcepcion)