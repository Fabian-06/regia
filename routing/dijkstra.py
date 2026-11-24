"""Dijkstra, para comparar con A*. Responsable: persona 2.

No lo exige el enunciado. Sirve para enseñar en el Laboratorio A* cuántos
nodos se ahorra la heurística: misma ruta, menos nodos expandidos.
"""
from core.contracts import Context, Graph, RouteRequest, RouteResult


def find_route(
    graph: Graph,
    request: RouteRequest,
    context: Context,
    with_trace: bool = False,
) -> RouteResult:
    """Igual que routing.astar.find_route(), pero sin heurística (h = 0).

    El resultado lleva algorithm=Algorithm.DIJKSTRA.
    """
    raise NotImplementedError("routing.dijkstra.find_route() está pendiente (persona 2)")
