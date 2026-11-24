// Planificador de rutas. Responsable: persona 5.
//
// PENDIENTE. Esta página habla con el servidor solo a través de la API:
//
//   GET  /api/stations/   estaciones y líneas (mapa y desplegables)
//   GET  /api/context/    hora, clima e incidencias actuales
//   POST /api/route/      calcula una ruta
//   POST /api/assistant/  consulta en lenguaje natural
//
// El formato de cada petición y respuesta está en docs/CONTRATOS.md.
// En docs/ejemplos/ hay respuestas de muestra para avanzar con el mapa antes
// de que la API esté terminada. Django no sirve la carpeta docs/: copiadlas a
// web/static/web/mock/ y cargadlas con fetch("/static/web/mock/...").
// Acordaos de borrar esa carpeta cuando uséis la API real.
//
// Un endpoint sin implementar responde 501 con {"error": "pendiente"}.
//
// IMPORTANTE: Django rechaza con un 403 los POST que no llevan el token CSRF.
// Hay que leer la cookie "csrftoken" y enviarla en la cabecera "X-CSRFToken"
// de cada fetch con method POST.
