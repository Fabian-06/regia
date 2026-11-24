"""Función heurística h. Responsable: persona 2."""
from core.contracts import Graph, NodeId


def estimate(graph: Graph, node: NodeId, destination: str) -> float:
    """Estimación en minutos del coste que falta desde node hasta la estación
    de destino.

    Idea acordada: distancia en línea recta entre las coordenadas de las dos
    estaciones, dividida por la velocidad máxima de un tren.

    Requisitos:

    - Mismas unidades que g: minutos.
    - Admisible: nunca mayor que el coste real. Por eso se usa la velocidad
      máxima y la distancia más corta posible.
    - Vale 0 cuando node ya está en la estación de destino.

    En la memoria hay que razonar por qué es admisible.
    """
    raise NotImplementedError("routing.heuristics.estimate() está pendiente (persona 2)")
