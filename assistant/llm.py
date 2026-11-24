"""Cliente del LLM. Responsable: persona 4.

Todo el acceso al LLM pasa por este archivo. Así se puede cambiar de
proveedor, o usar un modelo local, tocando un solo sitio.
"""


def is_available() -> bool:
    """Indica si hay un LLM configurado (settings.LLM_API_KEY no está vacío)."""
    raise NotImplementedError("assistant.llm.is_available() está pendiente (persona 4)")


def complete(system_prompt: str, user_text: str) -> str:
    """Envía un mensaje al LLM y devuelve el texto de la respuesta.

    - La clave y el modelo se leen de settings.LLM_API_KEY y settings.LLM_MODEL
      (archivo .env). La clave nunca se escribe en el código ni se sube al
      repositorio.
    - Poned un tiempo máximo a la petición.
    - Si algo falla, lanza RuntimeError; parser y explainer la capturan y
      pasan al modo sin LLM.
    """
    raise NotImplementedError("assistant.llm.complete() está pendiente (persona 4)")
