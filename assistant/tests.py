"""Tests del asistente. Responsable: persona 4.

PENDIENTE. Los tests no deben llamar al LLM real (cuesta dinero y no es
determinista): sustituid assistant.llm.complete con unittest.mock.

Comprobaciones útiles:

- Con una respuesta simulada del LLM, parse_query() devuelve el RouteRequest
  esperado.
- Si el LLM devuelve una estación que no existe, ValueError.
- Sin clave configurada, parse_query() funciona en modo sin LLM.
- explain() en modo sin LLM incluye el tiempo total y los transbordos.

Se ejecutan con: python manage.py test assistant
"""
