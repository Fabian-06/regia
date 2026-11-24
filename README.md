# Regia · copiloto del Metrorrey

Práctica de Inteligencia Artificial (curso 2026-27): trayecto óptimo entre
dos estaciones de las líneas 1, 2 y 3 del metro de Monterrey con el algoritmo
A*.

Este repositorio es el **esqueleto**: el proyecto arranca y los tests pasan,
pero ninguna función de la práctica está implementada. Cada una lanza
`NotImplementedError` con el nombre de quien la tiene asignada.

## Puesta en marcha

Hace falta Python 3.10 o posterior.

```bash
# 1. Entorno virtual (una vez)
python -m venv .venv

# 2. Activarlo (cada vez que abras una terminal)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS y Linux

# 3. Dependencias
pip install -r requirements.txt

# 4. Base de datos
python manage.py migrate

# 5. Comprobar que todo está bien
python manage.py test

# 6. Arrancar
python manage.py runserver
```

Con el servidor en marcha:

| Dirección | Qué es |
|---|---|
| http://127.0.0.1:8000/ | Planificador |
| http://127.0.0.1:8000/lab/ | Laboratorio A* |
| http://127.0.0.1:8000/admin/ | Centro de control (antes: `python manage.py createsuperuser`) |
| http://127.0.0.1:8000/api/health/ | Comprobación de la API |

Si en Windows `python` no existe, probad con `py`. Si PowerShell no deja
activar el entorno, ejecutad antes
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Configuración local

Opcional. Copiad `.env.example` como `.env` y rellenad lo que necesitéis (por
ejemplo, la clave del LLM). `.env` no se sube al repositorio.

## Quién hace qué

| # | Carpeta | Responsabilidad | Función de entrada |
|---|---|---|---|
| 1 | `network/` | Datos de la red: estaciones, coordenadas, tiempos, transbordos, accesibilidad | `network.graph.build_graph()` |
| 2 | `routing/` | A*, función de coste, heurística, Dijkstra para comparar | `routing.astar.find_route()` |
| 3 | `conditions/` | Hora y frecuencias, clima, incidencias, centro de control | `conditions.context.get_context()` |
| 4 | `assistant/` | LLM: de texto a consulta, explicación de la ruta, modo sin LLM | `assistant.parser.parse_query()`, `assistant.explainer.explain()` |
| 5 | `web/` | Planificador: mapa, formulario, itinerario, chat, diseño | página `/` |
| 6 | `api/`, `lab/`, `config/`, `core/` | API, Laboratorio A*, integración y coordinación | endpoints de `/api/`, página `/lab/` |

Cada archivo empieza con un comentario que dice de quién es y qué falta.

## Estructura

```
config/       configuración de Django y rutas principales
core/         contratos compartidos (contracts.py) y tests del esqueleto
network/      la red de metro                              persona 1
routing/      A* en Python puro, sin Django                persona 2
conditions/   estado de la red en tiempo real              persona 3
assistant/    asistente con LLM                            persona 4
web/          planificador (plantillas, CSS, JS)           persona 5
api/          endpoints JSON                               persona 6
lab/          Laboratorio A*                               persona 6
docs/         contratos, ejemplos de la API y registro de uso de IA
```

## Cómo trabajar sin pisarse

1. **Cada persona toca solo su carpeta.** Si necesitas algo de otro módulo,
   pídeselo a su responsable.
2. **Los contratos no se cambian por libre.** `core/contracts.py` y
   `docs/CONTRATOS.md` solo se modifican con acuerdo del grupo.
3. **Una rama por módulo** (`network`, `routing`, ...) y se integra en `main`
   a menudo, con cambios pequeños. Antes de integrar: `python manage.py test`.
4. **No esperéis a los demás.** `routing` se prueba con un grafo pequeño hecho
   a mano; `web` y `lab` pueden usar los JSON de `docs/ejemplos/`; `assistant`
   se prueba simulando el LLM.
5. **Dependencias nuevas**, a `requirements.txt` en el mismo commit en que se
   usan.
6. **Modelos nuevos:** `python manage.py makemigrations <app>` y subid la
   carpeta `migrations/` que se crea.

## Orden recomendado

La memoria y el código se entregan el 2 de diciembre.

1. **Núcleo** (lo que pide el enunciado): datos de la red, A* con g y h,
   `/api/stations/` y `/api/route/`, y el mapa con la ruta pintada.
2. **Tiempo real:** frecuencias por hora, clima, incidencias.
3. **Extras:** Laboratorio A*, asistente, comparación con Dijkstra.

No empecéis el punto 3 hasta que el 1 funcione de principio a fin.

## Memoria

- **Apartado 3 (g y h):** salen de `routing/costs.py` y
  `routing/heuristics.py`. Justificad cada valor y por qué la heurística es
  admisible.
- **Apartado 7 (referencias):** apuntad la fuente de cada dato al recogerlo,
  no al final.
- **Apartado 8 (uso de IA):** el registro está en `docs/USO_IA.md`. Leedlo
  antes de usar cualquier herramienta de IA: un uso sin declarar anula la
  práctica de todo el grupo.

## Antes de la presentación

La demo en directo no debe depender de internet ni de una clave: comprobad
que la aplicación calcula rutas con el clima caído y sin LLM configurado.
