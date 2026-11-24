"""Hora de Monterrey, horario de servicio y frecuencias. Responsable: persona 3."""
from datetime import datetime


def now_monterrey() -> datetime:
    """Devuelve la hora actual de Monterrey, con zona horaria.

    settings.TIME_ZONE ya es "America/Monterrey", así que
    django.utils.timezone.localtime() da esta hora directamente.
    """
    raise NotImplementedError("conditions.clock.now_monterrey() está pendiente (persona 3)")


def is_service_open(when: datetime) -> bool:
    """Indica si el metro da servicio en ese instante.

    Las fuentes no coinciden en el horario exacto: comprobadlo en la web de
    Metrorrey y citad la fuente en la memoria.
    """
    raise NotImplementedError("conditions.clock.is_service_open() está pendiente (persona 3)")


def headways(when: datetime) -> dict[str, float]:
    """Minutos entre trenes en cada línea a esa hora: {"L1": ..., "L2": ..., "L3": ...}.

    Debe distinguir al menos hora punta y hora valle, y laborable y fin de
    semana. Citad en la memoria de dónde salen las frecuencias.
    """
    raise NotImplementedError("conditions.clock.headways() está pendiente (persona 3)")
