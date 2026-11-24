from core.contracts import Graph, RouteRequest, Profile
import re
import unicodedata
import json
from assistant import llm

def normalizar(text: str) -> str:
    """convertimos el texto a minúsculas, eliminamos tíldes y signos de puntacion, ademas de normalizar los espacios"""
    text = text.lower()
    text = "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if unicodedata.category(c) != "Mn"
    )
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())

def detectar_perfil(text: str) -> Profile:
    """Buscamos palabras clave en el texto para saber si queremos buscarle una ruta más accesible o si quiere evitar transbordos
    y si no tiene preferencia utilizamos la más rápida"""
    accesible = ["silla de ruedas", "ascensor", "accesible", "elevador"]
    if any(p in text for p in accesible):
        return Profile.ACCESSIBLE
    transbordos = ["sin transbordos", "menos transbordos", "menos cambios", "sin cambios"]
    if any(p in text for p in transbordos):
        return Profile.FEWEST_TRANSFERS
    return Profile.FASTEST

def extraer_estaciones(text: str, graph: Graph) -> tuple[str, str]:
    """Buscamos en el texto las estaciones de origen como de destino y luego con palabras clave decidimos cual es el origen
    y cual es el destino para dar la respuesta correcta"""
    posibles = [(normalizar(station.name), station.id) for station in graph.stations.values()]
    posibles.sort(key=lambda x: len(x[0]), reverse=True)

    texto_busqueda = text
    encontradas = []
    for name, station_id in posibles:
        coincidencia = re.search(rf"\b{re.escape(name)}\b", texto_busqueda)
        if coincidencia:
            encontradas.append((coincidencia.start(), station_id))
            texto_busqueda = (texto_busqueda[:coincidencia.start()] + " " *(coincidencia.end() - coincidencia.start())
                                + texto_busqueda[coincidencia.end():])
    encontradas.sort(key=lambda x: x[0])
    if len(encontradas) < 2:
        raise ValueError("No se ha entendido la estacion de origen o destino")
    (pos1, id1), (pos2, id2) = encontradas[:2]

    antes1 = text[:pos1].split()
    antes2 = text[:pos2].split()
    palabra1 = antes1[-1] if antes1 else ""
    palabra2 = antes2[-1] if antes2 else ""

    destino = ["a", "al", "hasta", "hacia"]
    origen = ["de", "del", "desde"]

    if palabra2 in origen and palabra1 in destino:
        return id2, id1
    else:
        return id1, id2

def parse_sin_llm(text: str, graph: Graph):
    """Si no contamos con el LLM, usamos las funciones que hemos hecho antes para normalizar el texto, buscar el perfil
    y las estaciones de origen y destino"""
    text = normalizar(text)
    profile = detectar_perfil(text)
    estaciones = extraer_estaciones(text, graph)
    return RouteRequest(origin=estaciones[0], destination=estaciones[1], profile=profile)

def construir_prompt(graph: Graph) -> str:
    """Aqui solo hacemos el system prompt que le pasaremos al LLM, con las reglas que queremos que tenga y le pasamos la lista de
    estaciones que contiene nuestro grafo. También le indicamos en el formato que nos tiene que dar la solución"""
    estaciones = "\n".join(f"- {station.id}: {station.name}" for station in graph.stations.values())
    prompt = ("Eres un extractor de parámetros para un planificador de rutas de metro.\n"
    "Tu única tarea es leer la frase del usuario y extraer tres datos: "
    "origin, destination y profile. Nunca calcules ni sugieras rutas.\n"
    "Estaciones válidas (usa solo estos ids, como aparecen):\n"
    f"{estaciones}\n"
    "Perfiles válidos:\n"
    '- "fastest": menor tiempo total, uso por defecto\n'
    '- "fewest_transfers": el usuario quiere evitar transbordos, no cambiar de tren o línea, o ir directo\n'
    '- "accessible": el usuario necesita ascensor o va en silla de ruedas\n'
    "Reglas:\n"
    "- origin y destination deben ser ids de la lista anterior\n"
    "- Si falta el origen o el destino, ponlo como null. No inventes estaciones\n" 
    "- Responde únicamente con un objeto JSON válido, sin texto adicional," 
    " sin explicaciones y sin bloques de codigo\n" 
    "\n" 
    "Formato exacto de la respuesta:\n" 
    '{"origin": "<id o null>", "destination": "<id o null>", "profile": "<perfil>"}'
    )
    return prompt

def resolver_id(valor: object, graph:Graph):
    """Como se pueden usar modelos locales pequeños a veces dan el nombre de las estaciones en vez de los id,
    nos encargamos de que al final se mande el id y no el nombre"""
    if not isinstance(valor, str):
        return None
    limpio = valor.strip()
    if limpio in graph.stations:
        return limpio
    norm = normalizar(limpio)
    for station in graph.stations.values():
        if normalizar(station.name) == norm or normalizar(station.id) == norm:
            return station.id
    return None

def parse_con_llm(text: str, graph: Graph) -> RouteRequest:
    """Llamamos al LLM con el system prompt que contruimos antes y con el texto deel usuario, y nos devuelve un json que contiene
    los datos de la estacion de origen, destino y el perfil. Sin tener que usar nuestra funciones de normalizar, detectar el perfil 
    y encontrar las estaciones"""
    system_prompt = construir_prompt(graph)
    respuesta = llm.complete(system_prompt, text)

    json_bueno = re.search(r"\{.*\}", respuesta, re.DOTALL)
    if not json_bueno:
        raise json.JSONDecodeError("No se encontró JSON",respuesta, 0)

    data = json.loads(json_bueno.group(0))
    origin = data.get("origin")
    destination = data.get("destination")

    if not origin:
        raise ValueError("No he entendido la estación de origen")
    if not destination:
        raise ValueError("No he entendido la estación de destino")

    origin_id = resolver_id(origin, graph)
    destination_id = resolver_id(destination, graph)

    if origin_id not in graph.stations or destination_id not in graph.stations:
        raise ValueError("El asistente devolvió una estacion que no existe")
    if origin_id == destination_id:
        raise ValueError("El origen y el destino son la misma estación")

    try:
        profile = Profile(data.get("profile") or "fastest")
    except ValueError:
        profile = Profile.FASTEST
    return RouteRequest(origin=origin_id, destination=destination_id, profile=profile)


def parse_query(text: str, graph: Graph) -> RouteRequest:
    """Si el LLM esta disponible intentamos que obtenga los datos el propio LLM, si falla o no esta disponible usamos nuestras
    funciones para hacerlo sin el LLM"""
    if llm.is_available():
        try:
            return parse_con_llm(text,graph)
        except (RuntimeError,json.JSONDecodeError):
            return parse_sin_llm(text,graph)
    else:
        return parse_sin_llm(text,graph)
