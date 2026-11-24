"""Tests de A*. Responsable: persona 2.

PENDIENTE. Como routing no depende de Django ni de los datos reales, podéis
probarlo desde el primer día con un grafo pequeño hecho a mano (4 o 5
estaciones) en lugar de esperar a la persona 1.

Comprobaciones útiles:

- Origen igual a destino: ruta de un solo paso y coste 0.
- En un grafo pequeño, la ruta devuelta es la que se calcula a mano.
- A* y Dijkstra devuelven el mismo coste total.
- A* expande los mismos nodos que Dijkstra o menos.
- La heurística nunca supera el coste real (admisibilidad).
- Con una estación cerrada, la ruta la evita o found es False.
- Con el perfil ACCESSIBLE no se pasa por estaciones sin ascensor.
- Origen o destino inexistente: ValueError.

Se ejecutan con: python manage.py test routing
"""
