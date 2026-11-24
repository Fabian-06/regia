# Ejemplos de la API

Estos archivos enseñan el **formato** de cada respuesta. Se han generado a
partir de `core/contracts.py`, así que los nombres de campo y los tipos son
los reales.

Los **valores son inventados** (coordenadas, minutos, clima, incidencia): no
los uséis como datos de la práctica ni los citéis en la memoria.

| Archivo | Corresponde a |
|---|---|
| `stations.json` | respuesta de `GET /api/stations/` (recortada a 3 estaciones) |
| `context.json` | respuesta de `GET /api/context/` |
| `route_request.json` | cuerpo de `POST /api/route/` |
| `route_result.json` | respuesta de `POST /api/route/` con `trace` activado |
| `assistant_response.json` | respuesta de `POST /api/assistant/` |
