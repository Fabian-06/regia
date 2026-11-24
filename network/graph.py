"""Construcción del grafo de la red. Responsable: persona 1.

Este archivo es la única puerta de entrada al módulo: el resto del proyecto
solo llama a build_graph().
"""
from core.contracts import Graph


def build_graph() -> Graph:
    """Devuelve la red de las líneas 1, 2 y 3 como un Graph.

    Qué debe cumplir el resultado:

    - Un nodo (estación, línea) por cada línea que pasa por cada estación.
    - Dos aristas RIDE (ida y vuelta) entre estaciones consecutivas de una línea.
    - Dos aristas TRANSFER (ida y vuelta) entre los nodos de una misma estación,
      solo en los tres transbordos del enunciado: Cuauhtémoc (L1-L2),
      General I. Zaragoza (L2-L3) y Félix U. Gómez (L1-L3).
    - "minutes" y "meters" son valores base, sin clima ni esperas: de eso se
      encarga routing.costs con el Context.

    El grafo no cambia durante la ejecución, así que conviene construirlo una
    vez y reutilizarlo.

    Para la memoria (apartado 7): anotad de dónde sale cada dato (coordenadas,
    tiempos, ascensores) según lo vayáis recogiendo.
    """
    raise NotImplementedError("network.graph.build_graph() está pendiente (persona 1)")
