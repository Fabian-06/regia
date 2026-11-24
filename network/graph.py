"""Construcción del grafo de la red. Responsable: persona 1."""
from functools import lru_cache
import json
from pathlib import Path

from core.contracts import (
    Edge,
    EdgeKind,
    Graph,
    LineInfo,
    NodeId,
    StationInfo,
)

DATA_PATH = Path(__file__).parent / "data" / "metro.json"


@lru_cache(maxsize=1)
def build_graph() -> Graph:
    """Lee network/data/metro.json una sola vez y devuelve el Graph completo."""
    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Estaciones
    stations: dict[str, StationInfo] = {
        s["id"]: StationInfo(
            id=s["id"],
            name=s["name"],
            lat=float(s["lat"]),
            lon=float(s["lon"]),
            line_ids=tuple(s["line_ids"]),
            underground=bool(s["underground"]),
            has_elevator=bool(s["has_elevator"]),
        )
        for s in data["stations"]
    }

    # 2. Líneas
    lines: dict[str, LineInfo] = {
        line["id"]: LineInfo(
            id=line["id"],
            name=line["name"],
            color=line["color"],
            station_ids=tuple(line["station_ids"]),
        )
        for line in data["lines"]
    }

    # 3. Inicializar todos los nodos (estación, línea) en edges
    edges: dict[NodeId, list[Edge]] = {
        (station.id, line_id): []
        for station in stations.values()
        for line_id in station.line_ids
    }

    # 4. Aristas de trayecto (RIDE) en ambos sentidos
    for seg in data["segments"]:
        node_a: NodeId = (seg["from"], seg["line_id"])
        node_b: NodeId = (seg["to"], seg["line_id"])
        minutes = float(seg["minutes"])
        meters = float(seg["meters"])

        edges[node_a].append(
            Edge(source=node_a, target=node_b, kind=EdgeKind.RIDE, minutes=minutes, meters=meters)
        )
        edges[node_b].append(
            Edge(source=node_b, target=node_a, kind=EdgeKind.RIDE, minutes=minutes, meters=meters)
        )

    # 5. Aristas de transbordo (TRANSFER) en ambos sentidos
    for tr in data["transfers"]:
        node_a = (tr["station_id"], tr["from_line"])
        node_b = (tr["station_id"], tr["to_line"])
        minutes = float(tr["minutes"])
        meters = float(tr["meters"])

        edges[node_a].append(
            Edge(source=node_a, target=node_b, kind=EdgeKind.TRANSFER, minutes=minutes, meters=meters)
        )
        edges[node_b].append(
            Edge(source=node_b, target=node_a, kind=EdgeKind.TRANSFER, minutes=minutes, meters=meters)
        )

    return Graph(stations=stations, lines=lines, edges=edges)