"""Tests de la red. Responsable: persona 1.

PENDIENTE. Comprobaciones útiles sobre build_graph():

- Hay 19 estaciones en L1, 13 en L2 y 9 en L3 (contando General I. Zaragoza
  en las dos), según el plano del enunciado: 38 estaciones y 41 nodos.
- Las terminales son las del enunciado (Talleres-Exposición,
  Sendero-General I. Zaragoza, General I. Zaragoza-Hospital Metropolitano).
- Existen exactamente los tres transbordos del enunciado.
- Toda arista tiene su arista de vuelta.
- Ningún tiempo ni distancia es negativo o cero.
- Desde cualquier nodo se puede llegar a cualquier otro.

Se ejecutan con: python manage.py test network
"""
