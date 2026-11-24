"""De texto libre a consulta de ruta. Responsable: persona 4."""
from core.contracts import Graph, RouteRequest


def parse_query(text: str, graph: Graph) -> RouteRequest:
    """Convierte una frase del usuario en un RouteRequest.

    Ejemplo: "voy en silla de ruedas de Talleres al Hospital Metropolitano"
    -> origin="talleres", destination="hospital-metropolitano",
       profile=Profile.ACCESSIBLE.

    Reglas:

    - El LLM solo extrae parámetros. NUNCA calcula ni sugiere la ruta: eso lo
      hace A*. Es importante poder defenderlo en la presentación.
    - Los ids devueltos tienen que existir en graph.stations. El LLM puede
      inventar estaciones: validad siempre su salida.
    - Si no se identifica origen o destino, ValueError con un mensaje que se
      pueda mostrar al usuario ("No he entendido la estación de destino").
    - Modo sin LLM: si assistant.llm.is_available() es False o la llamada
      falla, se intenta reconocer los nombres de estación buscándolos en el
      texto. La demo no puede depender de una clave ni de la conexión.
    """
    raise NotImplementedError("assistant.parser.parse_query() está pendiente (persona 4)")
