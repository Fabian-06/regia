"""Construcción del Context. Responsable: persona 3.

Este archivo es la única puerta de entrada al módulo: el resto del proyecto
solo llama a get_context().
"""
from datetime import datetime

from core.contracts import Context


def get_context(when: datetime | None = None) -> Context:
    """Reúne hora, frecuencias, clima e incidencias activas en un Context.

    - when=None significa "ahora" (conditions.clock.now_monterrey()).
    - Si when es otra hora (el usuario planifica un viaje futuro), el clima
      actual no aplica: decidid si se deja en None o se usa una previsión.
    - Las incidencias salen de la base de datos (solo las activas),
      convertidas a core.contracts.Incident.
    """
    raise NotImplementedError("conditions.context.get_context() está pendiente (persona 3)")
