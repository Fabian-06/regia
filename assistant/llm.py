from django.conf import settings
import json
import urllib.request



def is_available() -> bool:
    """indicamos si hay un LLM disponible para usarse"""
    api_key = getattr(settings, "LLM_API_KEY", "")
    return bool(api_key and api_key.strip())


def complete(system_prompt: str, user_text: str) -> str:
    """envia el system prompt y el texto del usuario al servidor local de Ollama y devuelve su respuesta en texto.
    Además se configura como queremos que se use el LLM."""
    base_url = getattr(settings, "LLM_API_KEY", "").strip().rstrip("/")
    model = getattr(settings, "LLM_MODEL", "qwen3.5:2b").strip()
    if not base_url:
        raise RuntimeError("LLM no configurado")
    modelo = {"model": model, 
                "stream":False, 
                "think":False,
                "options": {"temperature": 0.1}, 
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content":user_text}]}
    try:
        req = urllib.request.Request(f"{base_url}/api/chat",
                                    data=json.dumps(modelo).encode("utf-8"),
                                    headers={"Content-Type": "application/json"},
                                    method="POST",)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["message"]["content"].strip()
    except Exception as exc:
        raise RuntimeError(f"Error al consultar el LLM: {exc}") from exc

