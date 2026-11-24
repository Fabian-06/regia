// Laboratorio A*. Responsable: persona 6.
//
// PENDIENTE. La animación se alimenta de POST /api/route/ con "trace": true.
// La respuesta trae "trace": una entrada por iteración con el nodo expandido,
// sus valores g, h y f, y las listas abierta y cerrada en ese momento.
// Pidiendo la misma ruta con "algorithm": "dijkstra" se obtiene el dato para
// comparar los nodos expandidos.
//
// Ejemplo de respuesta: docs/ejemplos/route_result.json.
//
// IMPORTANTE: los POST necesitan el token CSRF. Hay que leer la cookie
// "csrftoken" y enviarla en la cabecera "X-CSRFToken".
