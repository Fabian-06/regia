# Regia · copiloto del Metrorrey

Práctica de Inteligencia Artificial (curso 2026-27): trayecto óptimo entre
dos estaciones de las líneas 1, 2 y 3 del metro de Monterrey con el algoritmo
A*.

Este repositorio es el **esqueleto**: el proyecto arranca y los tests pasan,
pero ninguna función de la práctica está implementada. Cada una lanza
`NotImplementedError` con el nombre de quien la tiene asignada.


| # | Carpeta | Responsabilidad | Función de entrada |
|---|---|---|---|
| 1 | `network/` | Datos de la red: estaciones, coordenadas, tiempos, transbordos, accesibilidad | `network.graph.build_graph()` |
| 2 | `routing/` | A*, función de coste, heurística, Dijkstra para comparar | `routing.astar.find_route()` |
| 3 | `conditions/` | Hora y frecuencias, clima, incidencias, centro de control | `conditions.context.get_context()` |
| 4 | `assistant/` | LLM: de texto a consulta, explicación de la ruta, modo sin LLM | `assistant.parser.parse_query()`, `assistant.explainer.explain()` |
| 5 | `web/` | Planificador: mapa, formulario, itinerario, chat, diseño | página `/` |
| 6 | `api/`, `lab/`, `config/`, `core/` | API, Laboratorio A*, integración y coordinación | endpoints de `/api/`, página `/lab/` |

Cada archivo empieza con un comentario que dice de quién es y qué falta.

## Estructura

```
config/       configuración de Django y rutas principales
core/         contratos compartidos (contracts.py) y tests del esqueleto
network/      la red de metro                         
routing/      A* en Python puro, sin Django           
conditions/   estado de la red en tiempo real             
assistant/    asistente con LLM                      
web/          planificador (plantillas, CSS, JS)           
api/          endpoints JSON                            
lab/          Laboratorio A*                             
docs/         contratos, ejemplos de la API y registro de uso de IA
```
