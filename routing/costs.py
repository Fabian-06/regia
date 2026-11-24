"""Función de coste g. Responsable: persona 2 (con datos de la persona 3).

Aquí se decide cuánto "cuesta" cada arista según el contexto y el perfil.
Es la pieza que convierte un A* de libro en uno adaptado a la situación real.
"""
from core.contracts import Context, Edge, Profile


def edge_cost(edge: Edge, context: Context, profile: Profile) -> float:
    """Coste en minutos de recorrer una arista en las condiciones dadas.

    Factores previstos (decidid los valores y justificadlos en la memoria):

    - Tiempo base: edge.minutes.
    - Espera en transbordos: depende de context.headways de la línea destino.
    - Retrasos: incidencias LINE_DELAY de context.incidents.
    - Clima: context.weather puede penalizar los transbordos a pie o las
      estaciones no subterráneas.
    - Perfil: FEWEST_TRANSFERS encarece los transbordos; ACCESSIBLE impide
      usar estaciones sin ascensor.

    Una arista que no se puede usar (estación cerrada, o sin ascensor en el
    perfil accesible) devuelve float("inf").

    IMPORTANTE: el resultado nunca puede ser menor que edge.minutes. Si lo
    fuera, la heurística dejaría de ser admisible y A* ya no garantizaría la
    ruta óptima.
    """
    raise NotImplementedError("routing.costs.edge_cost() está pendiente (persona 2)")


def initial_wait(line_id: str, context: Context) -> float:
    """Minutos de espera estimados al entrar en la primera estación.

    Se suma una sola vez, al principio del viaje, según la frecuencia de la
    línea en context.headways.
    """
    raise NotImplementedError("routing.costs.initial_wait() está pendiente (persona 2)")
