# Contratos entre módulos

Un contrato es lo que un módulo promete entregar a otro. Mientras se
respeten, cada persona puede trabajar en su carpeta sin esperar a las demás.

Los tipos están definidos en `core/contracts.py`. Ese archivo y este
documento solo se cambian con acuerdo de todo el grupo.

## Quién entrega qué

```
network ──Graph──────┐
                     ├──> routing ──RouteResult──> api ──JSON──> web, lab
conditions ──Context─┘                              ↑
                                                assistant
```

| Contrato | Lo entrega | Función | Lo usa |
|---|---|---|---|
| `Graph` | persona 1 | `network.graph.build_graph()` | routing, api, assistant |
| `Context` | persona 3 | `conditions.context.get_context(when)` | routing, api, assistant |
| `RouteResult` | persona 2 | `routing.astar.find_route(graph, request, context, with_trace)` | api, assistant |
| JSON de la API | persona 6 | endpoints de `/api/` | web, lab |

Nadie importa nada de otro módulo que no sea su función de entrada.
`routing` no importa de `network` ni de `conditions`: recibe el grafo y el
contexto como argumentos.

## Convenciones

- **Id de estación:** minúsculas, sin tildes, con guiones: `felix-u-gomez`,
  `general-i-zaragoza`, `hospital-metropolitano`.
- **Id de línea:** `L1`, `L2`, `L3`.
- **Nodo:** par (estación, línea). Cuauhtémoc son dos nodos,
  `("cuauhtemoc", "L1")` y `("cuauhtemoc", "L2")`, unidos por una arista de
  transbordo. En JSON un nodo es una lista: `["cuauhtemoc", "L1"]`.
- **Unidades:** minutos y metros, siempre.
- **Horas:** con zona horaria, en hora de Monterrey. En JSON, formato ISO
  8601: `2026-11-16T08:15:00-06:00`.

## API

Todas las respuestas son JSON. En `docs/ejemplos/` hay una muestra de cada
una (valores inventados, formato real).

| Método y ruta | Entrada | Salida |
|---|---|---|
| `GET /api/health/` | nada | `{"status": "ok", "app": "regia"}` |
| `GET /api/stations/` | nada | `{"stations": [...], "lines": [...]}` |
| `GET /api/context/` | nada | un `Context` |
| `POST /api/route/` | ver abajo | un `RouteResult` |
| `POST /api/assistant/` | `{"text": "..."}` | `{"request", "result", "explanation"}` |

Cuerpo de `POST /api/route/`:

| Campo | Obligatorio | Valores |
|---|---|---|
| `origin` | sí | id de estación |
| `destination` | sí | id de estación |
| `profile` | no | `fastest` (por defecto), `fewest_transfers`, `accessible` |
| `when` | no | fecha ISO 8601; si falta o es `null`, ahora |
| `algorithm` | no | `astar` (por defecto), `dijkstra` |
| `trace` | no | `true` para recibir la traza paso a paso; por defecto `false` |

Códigos de respuesta:

| Código | Significado | Cuerpo |
|---|---|---|
| 200 | correcto | el resultado |
| 400 | petición incorrecta (estación desconocida, JSON mal formado, falta un campo) | `{"error": "mensaje para el usuario"}` |
| 403 | falta el token CSRF en un POST | página de error de Django |
| 405 | método no admitido | vacío |
| 501 | endpoint todavía sin implementar | `{"error": "pendiente", "detail": "..."}` |

Una ruta que no existe (por ejemplo, con una estación cerrada) **no es un
error**: responde 200 con `"found": false`.

## Cómo leer un RouteResult

- `steps` es el recorrido en orden. Cada paso lleva el tiempo acumulado desde
  el origen.
- Dos pasos seguidos con la misma estación y distinta línea son un transbordo.
- `trace` va vacío salvo que se pida. Cada entrada es una iteración de la
  búsqueda: el nodo que se expande, sus valores `g`, `h` y `f`, y cómo quedan
  las listas abierta y cerrada.
- `nodes_expanded` sirve para comparar A* con Dijkstra.

## Cómo cambiar un contrato

1. Quien lo necesita lo propone en el grupo y explica para qué.
2. Si hay acuerdo, el coordinador cambia `core/contracts.py` y este documento
   en un solo commit, y avisa.
3. Cada persona afectada adapta su módulo.
