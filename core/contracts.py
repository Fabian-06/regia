"""Contratos compartidos entre módulos.

Estos tipos son lo único que un módulo necesita saber de otro. Mientras nadie
los cambie, cada persona puede trabajar en su carpeta sin romper a las demás.

REGLA: este archivo no se modifica sin acuerdo de todo el grupo. Si necesitas
un campo nuevo, propónlo y lo añade el coordinador (persona 6).

Hay tres contratos:

1. Graph        network    -> routing          (la red de metro)
2. Context      conditions -> routing          (el estado de la red ahora)
3. RouteResult  routing    -> api/web/lab/assistant  (la ruta calculada)

Convenciones:

- Identificador de estación: texto en minúsculas, sin tildes y con guiones.
  Ejemplos: "talleres", "felix-u-gomez", "general-i-zaragoza".
- Identificador de línea: "L1", "L2" o "L3".
- Todos los tiempos van en minutos (float) y las distancias en metros.
- Las horas son datetime con zona horaria (aware), en hora de Monterrey.

Aquí solo hay datos: ninguna clase tiene lógica. La documentación completa,
con ejemplos en JSON, está en docs/CONTRATOS.md.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Un nodo del espacio de búsqueda de A*: (id de estación, id de línea).
# Una estación con transbordo aparece como dos nodos, uno por línea, unidos
# por una arista de tipo "transfer". Así el transbordo tiene su propio coste.
NodeId = tuple[str, str]


# ---------------------------------------------------------------------------
# Contrato 1: Graph (lo construye network, lo consume routing)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StationInfo:
    """Datos fijos de una estación."""

    id: str
    name: str                  # nombre para mostrar, con tildes: "Félix U. Gómez"
    lat: float                 # latitud en grados decimales
    lon: float                 # longitud en grados decimales
    line_ids: tuple[str, ...]  # líneas que pasan por la estación
    underground: bool          # True si es subterránea
    has_elevator: bool         # True si tiene ascensor operativo


@dataclass(frozen=True)
class LineInfo:
    """Datos fijos de una línea."""

    id: str
    name: str                     # "Línea 1"
    color: str                    # color en hexadecimal, p. ej. "#F5A623"
    station_ids: tuple[str, ...]  # estaciones en orden, de una terminal a la otra


class EdgeKind(str, Enum):
    RIDE = "ride"          # tramo en tren entre dos estaciones consecutivas
    TRANSFER = "transfer"  # cambio de línea a pie dentro de una estación


@dataclass(frozen=True)
class Edge:
    """Arista dirigida del grafo. Para ir y volver hacen falta dos aristas."""

    source: NodeId
    target: NodeId
    kind: EdgeKind
    minutes: float  # tiempo base, sin clima, esperas ni incidencias
    meters: float   # longitud del tramo o del pasillo de transbordo


@dataclass(frozen=True)
class Graph:
    """La red completa.

    edges[nodo] es la lista de aristas que salen de ese nodo.
    """

    stations: dict[str, StationInfo]
    lines: dict[str, LineInfo]
    edges: dict[NodeId, list[Edge]]


# ---------------------------------------------------------------------------
# Contrato 2: Context (lo construye conditions, lo consume routing)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Weather:
    """Clima actual en Monterrey."""

    temperature_c: float
    precipitation_mm: float  # lluvia en la última hora
    is_raining: bool


class IncidentKind(str, Enum):
    STATION_CLOSED = "station_closed"  # no se puede subir, bajar ni transbordar
    LINE_DELAY = "line_delay"          # la línea circula con retraso


@dataclass(frozen=True)
class Incident:
    """Una incidencia activa en la red."""

    kind: IncidentKind
    station_id: str | None  # obligatorio si kind es STATION_CLOSED
    line_id: str | None     # obligatorio si kind es LINE_DELAY
    extra_minutes: float    # retraso añadido; 0 si no aplica
    description: str        # texto para mostrar al usuario


@dataclass(frozen=True)
class Context:
    """El estado de la red en un instante. Todo lo que A* necesita saber
    del mundo exterior llega por aquí."""

    when: datetime                  # instante consultado, hora de Monterrey
    service_open: bool              # False si el metro está cerrado a esa hora
    headways: dict[str, float]      # minutos entre trenes por línea: {"L1": 5.4, ...}
    weather: Weather | None         # None si no se pudo obtener el clima
    incidents: tuple[Incident, ...]


# ---------------------------------------------------------------------------
# Contrato 3: RouteRequest y RouteResult (routing <-> resto de módulos)
# ---------------------------------------------------------------------------

class Profile(str, Enum):
    FASTEST = "fastest"                    # menor tiempo total
    FEWEST_TRANSFERS = "fewest_transfers"  # penaliza cada transbordo
    ACCESSIBLE = "accessible"              # evita estaciones sin ascensor


class Algorithm(str, Enum):
    ASTAR = "astar"
    DIJKSTRA = "dijkstra"


@dataclass(frozen=True)
class RouteRequest:
    """Lo que pide el usuario."""

    origin: str                   # id de la estación de origen
    destination: str              # id de la estación de destino
    profile: Profile = Profile.FASTEST
    when: datetime | None = None  # None significa "ahora"


@dataclass(frozen=True)
class RouteStep:
    """Un punto del recorrido.

    Dos pasos seguidos con la misma estación y distinta línea son un transbordo.
    """

    station_id: str
    line_id: str
    minutes: float  # tiempo acumulado desde el origen al llegar a este punto


@dataclass(frozen=True)
class TraceStep:
    """Una iteración de la búsqueda, para el Laboratorio A*."""

    node: NodeId         # nodo que se expande en esta iteración
    g: float
    h: float
    f: float
    open: tuple[NodeId, ...]    # lista abierta tras expandir
    closed: tuple[NodeId, ...]  # lista cerrada tras expandir


@dataclass(frozen=True)
class RouteResult:
    """La respuesta de routing."""

    found: bool                   # False si no existe ruta
    steps: tuple[RouteStep, ...]  # vacío si found es False
    total_minutes: float
    transfers: int
    nodes_expanded: int
    algorithm: Algorithm
    trace: tuple[TraceStep, ...] = field(default=())  # vacío salvo que se pida
