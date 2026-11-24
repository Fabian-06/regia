"""Algoritmo A*. Responsable: persona 2.

Este paquete es Python puro: no importa nada de Django. Así se puede probar
y explicar por separado, que es justo lo que evalúa la práctica.

Solo depende de core.contracts. Recibe el grafo y el contexto ya construidos;
nunca llama a network ni a conditions directamente.
"""
from core.contracts import Context, Graph, RouteRequest, RouteResult


def find_route(
    graph: Graph,
    request: RouteRequest,
    context: Context,
    with_trace: bool = False,
) -> RouteResult:
    """Calcula el trayecto óptimo con A*.

    - El estado es un nodo (estación, línea). El origen y el destino son
      estaciones, así que puede haber varios nodos iniciales y varios finales.
    - g(n) se obtiene sumando routing.costs.edge_cost() de cada arista.
    - h(n) es routing.heuristics.estimate().
    - Si with_trace es True, RouteResult.trace lleva una entrada por iteración
      (la usa el Laboratorio A*). Si es False, trace va vacío.
    - Si no hay ruta (por ejemplo, por una estación cerrada), se devuelve un
      RouteResult con found=False, no una excepción.
    - Si origin o destination no existen en el grafo, ValueError.

    Para la memoria (apartado 3): aquí salen los cálculos de g(n) y h(n) que
    el enunciado pide detallar.
    """
    raise NotImplementedError("routing.astar.find_route() está pendiente (persona 2)")
