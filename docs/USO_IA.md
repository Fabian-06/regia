# Registro de uso de inteligencia artificial

El apartado 8 de la memoria obliga a declarar **todo** uso de herramientas de
IA: tarea concreta, herramienta, motivo, prompts, salidas, qué se aceptó, qué
se descartó y cómo se validó. Un uso sin declarar supone un cero para todo el
grupo.

Este archivo es el borrador de ese apartado. Anotad cada uso **en el momento**
(reconstruirlo al final es difícil), una entrada por tarea.

No confundáis dos cosas distintas:

- Usar IA **para desarrollar** la práctica. Es lo que regula el apartado 8 y
  lo que se registra aquí.
- Que la aplicación **incluya** un LLM como funcionalidad (módulo
  `assistant`). Es una decisión de diseño que se explica en los apartados 3 y
  4; conviene mencionarla también en el 8 para que no haya dudas.

## Entradas

### 1. Idea de la aplicación y reparto en módulos

- **Fecha:** 14 de noviembre de 2026
- **Herramienta y modelo:** Claude (Anthropic), modelo Claude Fable 5.2
- **Quién:** _(nombre)_
- **Tarea:** proponer una idea de aplicación y un reparto del trabajo entre
  seis personas.
- **Motivo:** _(por qué se recurrió a la herramienta)_
- **Prompts:** _(pegar aquí los mensajes enviados, literales)_
- **Salida obtenida:** _(pegar o resumir la respuesta)_
- **Qué se aceptó:** _(…)_
- **Qué se descartó:** _(…)_
- **Cómo se revisó y validó:** _(…)_

### 2. Esqueleto inicial del proyecto

- **Fecha:** 14 de noviembre de 2026
- **Herramienta y modelo:** Claude (Anthropic), modelo Claude Fable 5.2
- **Quién:** _(nombre)_
- **Tarea:** generar la estructura inicial del proyecto Django.
- **Qué generó la herramienta:** la configuración de Django (`config/`), los
  contratos de datos (`core/contracts.py`), las firmas y la documentación de
  las funciones de cada módulo **sin implementar** (todas lanzan
  `NotImplementedError`), las plantillas HTML vacías, los tests del
  esqueleto, el `README.md` y la carpeta `docs/`.
- **Qué NO generó:** ningún dato de la red, ni A*, ni la función de coste, ni
  la heurística, ni la interfaz, ni la integración con el clima o con el LLM.
- **Motivo:** _(…)_
- **Prompts:** _(pegar aquí los mensajes enviados, literales)_
- **Qué se aceptó:** _(…)_
- **Qué se descartó o se cambió después:** _(…)_
- **Cómo se revisó y validó:** _(…)_

### 3. Guía de trabajo del equipo (PDF)

- **Fecha:** 14 de noviembre de 2026
- **Herramienta y modelo:** Claude (Anthropic), modelo Claude Fable 5.2
- **Quién:** _(nombre)_
- **Tarea:** redactar una guía que explique cómo funciona Django en el
  proyecto y qué tiene que hacer cada persona.
- **Qué generó la herramienta:** explicación de Django con ejemplos genéricos
  (no de la práctica), descripción de los pasos y decisiones de cada módulo,
  listas de comprobación, calendario propuesto y tabla de identificadores de
  estación transcrita del plano del enunciado.
- **Qué NO generó:** código de la práctica, datos de la red ni valores de las
  funciones g y h.
- **Motivo:** _(…)_
- **Prompts:** _(pegar aquí los mensajes enviados, literales)_
- **Qué se aceptó:** _(…)_
- **Qué se descartó o se cambió después:** _(…)_
- **Cómo se revisó y validó:** _(…)_

### Plantilla para nuevas entradas

- **Fecha:**
- **Herramienta y modelo:**
- **Quién:**
- **Tarea:**
- **Motivo:**
- **Prompts:**
- **Salida obtenida:**
- **Qué se aceptó:**
- **Qué se descartó:**
- **Cómo se revisó y validó:**
