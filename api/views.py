"""Vistas de la API. Responsable: persona 6.

La API es el pegamento: recibe la petición del navegador, llama a los módulos
en orden y devuelve JSON. No contiene lógica de rutas.

Mientras un endpoint no esté hecho responde 501 con un JSON que dice qué
falta. Así el frontend puede distinguir "pendiente" de "roto".

Pistas para implementarlas:

- dataclasses.asdict() convierte cualquier contrato en un diccionario, y
  JsonResponse ya sabe serializar fechas y los Enum de core.contracts.
- Las tuplas (los NodeId) salen en JSON como listas: ["cuauhtemoc", "L1"].
- Capturad los errores previsibles y devolved 400 con {"error": "..."} en
  lugar de dejar que salga un 500: ValueError de routing y de assistant,
  JSON mal formado, campos que faltan.
- Formato exacto de entrada y salida: docs/CONTRATOS.md y docs/ejemplos/.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST


def _pending(endpoint: str) -> JsonResponse:
    """Respuesta común de los endpoints que aún no están implementados."""
    return JsonResponse(
        {"error": "pendiente", "detail": f"{endpoint} todavía no está implementado"},
        status=501,
    )


@require_GET
def health(request):
    """GET /api/health/ : comprueba que el servidor está en marcha."""
    return JsonResponse({"status": "ok", "app": "regia"})


@require_GET
def stations(request):
    """GET /api/stations/ : estaciones y líneas para pintar el mapa y los
    desplegables.

    Llama a network.graph.build_graph() y devuelve
    {"stations": [...], "lines": [...]}. No devolváis graph.edges tal cual:
    sus claves son tuplas y JSON no las admite.
    """
    return _pending("GET /api/stations/")


@require_GET
def context(request):
    """GET /api/context/ : estado actual de la red (hora, clima, incidencias).

    Llama a conditions.context.get_context() y devuelve el Context.
    """
    return _pending("GET /api/context/")


@require_POST
def route(request):
    """POST /api/route/ : calcula una ruta.

    Entrada (JSON): origin, destination, y opcionales profile, when,
    algorithm ("astar" o "dijkstra") y trace (true para el Laboratorio A*).

    Pasos: build_graph() -> get_context(when) -> routing.astar.find_route()
    o routing.dijkstra.find_route() -> RouteResult en JSON.
    """
    return _pending("POST /api/route/")


@require_POST
def assistant(request):
    """POST /api/assistant/ : consulta en lenguaje natural.

    Entrada (JSON): {"text": "..."}.

    Pasos: assistant.parser.parse_query() -> los mismos de /api/route/ ->
    assistant.explainer.explain().
    Salida: {"request": ..., "result": ..., "explanation": "..."}.
    """
    return _pending("POST /api/assistant/")
