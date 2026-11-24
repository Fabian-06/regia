"""Tests de condiciones. Responsable: persona 3.

PENDIENTE. Comprobaciones útiles:

- headways() da frecuencias distintas en hora punta y en hora valle.
- is_service_open() es False de madrugada y True a mediodía.
- fetch_weather() devuelve None si la API falla (simulad el fallo con
  unittest.mock; los tests no deben depender de internet).
- get_context() solo incluye las incidencias activas.

Se ejecutan con: python manage.py test conditions
"""
