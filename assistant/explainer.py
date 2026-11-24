"""Explicación de la ruta en lenguaje natural. Responsable: persona 4."""
from core.contracts import Context, Graph, RouteResult


def explain(result: RouteResult, context: Context, graph: Graph) -> str:
    """Redacta en español por qué se ha elegido esa ruta.

    Ejemplo: "Te llevo por Félix U. Gómez en lugar de Cuauhtémoc porque la
    Línea 2 circula con 8 minutos de retraso."

    Reglas:

    - El texto solo puede contar lo que está en result y en context. Pasadle
      al LLM esos datos y pedidle que no añada nada que no esté en ellos.
    - Modo sin LLM: una plantilla fija con el tiempo total, el número de
      transbordos y las incidencias que afectan.
    """
    raise NotImplementedError("assistant.explainer.explain() está pendiente (persona 4)")
