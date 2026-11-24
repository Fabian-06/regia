"""Clima actual de Monterrey. Responsable: persona 3."""
from core.contracts import Weather


def fetch_weather() -> Weather | None:
    """Consulta el clima actual en una API externa y lo devuelve como Weather.

    Requisitos:

    - Si la API falla o tarda demasiado, devuelve None. Nunca lanza una
      excepción: la aplicación tiene que seguir calculando rutas sin clima.
    - Poned un tiempo máximo corto a la petición (unos pocos segundos).
    - Guardad el resultado unos minutos para no llamar a la API en cada
      consulta de ruta (django.core.cache sirve para esto).

    Propuesta: Open-Meteo. Comprobad en su documentación las condiciones de
    uso y si pide clave antes de integrarla, y citadla en la memoria.
    """
    raise NotImplementedError("conditions.weather.fetch_weather() está pendiente (persona 3)")
