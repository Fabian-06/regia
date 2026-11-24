from core.contracts import Context, Graph, RouteResult
from assistant import llm

def explain_sin_llm(result: RouteResult, context: Context, graph: Graph) -> str:
    """Explicamos sin el LLM con los datos recibidos. Si no hay ruta devolvemos directamente si es porque el servicio esta cerrado
    o porque hay alguna incidencia y las listamos. Si hay ruta sacamos el origen y el destino y si se hacen transbordos en que 
    estaciones se hacen. listamos el orgien y destino, el tiempo y los transbordos a realizar y por ulitmo si hay incidencias las 
    listamos tambien"""
    if not result.found or not result.steps:
        if not context.service_open:
            return "El servicio de metro está cerrado a esta hora"
        else:
            res = "No hay una ruta disponible para este trayecto"
            if len(context.incidents) > 0:
                res += ". Incidencias activas: "
                res += ", ".join(incidente.description for incidente in context.incidents)
            return res
    id_origen = result.steps[0].station_id
    id_destino = result.steps[-1].station_id
    origen = graph.stations[id_origen].name
    destino = graph.stations[id_destino].name
    lista = []
    for i in range(len(result.steps)-1):
        actual = result.steps[i]
        siguiente = result.steps[i+1]
        if actual.station_id == siguiente.station_id and actual.line_id != siguiente.line_id:
            lista.append(graph.stations[actual.station_id].name)
    res = f"Para ir desde {origen} hasta {destino} tardamos {result.total_minutes:.1f} minutos"
    if result.transfers == 0:
        res += " sin transbordos"
    else:
        res += f", con {result.transfers} transbordo(s) en: "
        res += ", ".join(lista)
    if len(context.incidents) > 0:
        res += ". Incidencias activas: "
        res += ", ".join(incidente.description for incidente in context.incidents)
    return res



def explain_con_llm(result: RouteResult, context: Context, graph: Graph) -> str:
    """para que el LLM explique el resultado y no genere el la solucion, le damos un system prompt indicando lo que queremos que haga
    y sacamos los datos que queremos pasarle exactamente como el origen y destino, el tiempo, los transbordos y las incidencias y 
    devolvemos la respuesta del LLM"""
    system_prompt = ("Eres un asistente de metro que redacta explicaciones breves en español "
    "(2 o 3 frases) sobre una ruta ya calculada.\n"
    "Reglas:\n"
    "- Usa únicamente los datos que te pas\n"
    "- Prohibido inventarse tiempos\n"
    "- Prohibido inventarse estaciones\n"
    "- Prohibido inventarse líneas\n"
    "- Prohibido inventarse retrasos\n"
    "- Prohibido inventarse rutas alternativas\n")

    id_origen = result.steps[0].station_id
    id_destino = result.steps[-1].station_id
    origen = graph.stations[id_origen].name
    destino = graph.stations[id_destino].name
    datos = f"Origen: {origen}, Destino: {destino}, Tiempo: {result.total_minutes:.1f} minutos, Transbordos: "
    if(result.transfers ==0):
            datos += "Ninguno"
    else:    
        transbordos = []
        for i in range(len(result.steps)-1):
            actual = result.steps[i]
            siguiente = result.steps[i+1]
            if actual.station_id == siguiente.station_id and actual.line_id != siguiente.line_id:
                transbordos.append(graph.stations[actual.station_id].name)
        datos += ", ".join(transbordos)    
    datos += ", Incidencias activas: "
    if len(context.incidents) > 0:
        datos += ", ".join(incidente.description for incidente in context.incidents)
    else:
        datos += "Ninguna"
    respuesta = llm.complete(system_prompt, datos).strip()
    if not respuesta:
        raise RuntimeError("Respuesta vacía del LLM")
    return respuesta

def explain(result: RouteResult, context: Context, graph: Graph) -> str:
    """Si no hay ruta devolvemos la respuesta basica sin usar el LLM. Si hay ruta comprabamos que el LLM este disponible
    si lo está intentamos que nos lo explique el LLM, pero si falla usamos nuestra respuesta sin LLM. Si no esta disponible el 
    LLM generamos nosotros la respuesta"""
    if not result.found or not result.steps:
        return explain_sin_llm(result, context, graph)
    if llm.is_available():
        try:
            return explain_con_llm(result, context, graph)
        except RuntimeError:
            return explain_sin_llm(result, context, graph)
    return explain_sin_llm(result, context, graph)