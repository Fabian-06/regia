"""Modelos de la red de metro. Responsable: persona 1.

PENDIENTE. Decisión vuestra: guardar la red en modelos de Django (y editarla
desde /admin/) o en un archivo JSON dentro de network/data/. Las dos valen
mientras network.graph.build_graph() devuelva un Graph correcto.

Si elegís modelos, estos son los datos que exige el contrato
(core/contracts.py):

- Línea: id ("L1"), nombre, color.
- Estación: id ("felix-u-gomez"), nombre, latitud, longitud, subterránea,
  con ascensor.
- Tramo entre estaciones consecutivas de una línea: minutos y metros.
- Transbordo entre dos líneas en una estación: minutos y metros a pie.

Al crear o cambiar modelos:
    python manage.py makemigrations network
    python manage.py migrate
y subid al repositorio la carpeta network/migrations/.
"""
