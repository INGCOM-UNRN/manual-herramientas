---
title: "giger"
subtitle: "Generador de Mapas de Llamadas y Grafos de Control en C"
---

<!-- Generado por scripts/generar_paginas.py desde giger@b316ea7: no editar a mano. -->

(manual-giger)=
# giger — Generador de Mapas de Llamadas y Grafos de Control en C

Repositorio: [github.com/INGCOM-UNRN-P1/giger](https://github.com/INGCOM-UNRN-P1/giger).

GIGER analiza el código fuente en C para construir el mapa estático de llamadas entre funciones (Call Graph), detectar ciclos recursivos, funciones no invocadas (*dead code*) y exportar diagramas en sintaxis Mermaid.

---

## Alcance

### Qué cubre
- Análisis estático de la topología de llamadas en código fuente C.
- Extracción y renderizado de mapas de llamadas entre funciones (Call Graphs).
- Detección de código muerto: una función es *huérfana* si ninguna otra función **del mismo archivo** la invoca (excepto `main`). El análisis es intra-archivo: una función definida en un `.c` y usada desde otro se reporta como huérfana. Con `--fail-on-orphans` el comando sale con código 1 si hay huérfanas (por defecto siempre 0).
- Exportación de diagramas a sintaxis Mermaid.
- Grafo de flujo de control (CFG) de cada función (`giger cfg archivo.c`): bloques básicos y aristas
  (con `V`/`F` en las condiciones), desde el AST. Señala el **código inalcanzable** (`GIG001`: lo que
  sigue a un `return`, `break`, `continue`, `goto` o `exit()`, y la rama de una condición constante
  como `if (0)`) y los **bucles infinitos triviales** (`GIG002`: `while (1)`/`for (;;)` sin `break`,
  `return`, `goto` ni `exit()`, un error; o una condición que depende sólo de variables locales que el
  cuerpo nunca modifica, una advertencia que avisa además si el cuerpo declara otra variable con el
  mismo nombre que la tapa). En Mermaid lo inalcanzable va en rojo punteado y la condición del bucle
  infinito, en naranja.

### Qué no cubre (Límites y Delegación)
- Complejidad ciclomática de McCabe ni exportación a DOT/Graphviz: no están implementadas.
- Medición dinámica de profundidad de pila en funciones recursivas (delegado a `sebastian`).
- Desensamblado de código máquina ni inspección de jump tables (delegado a `rachel`).
- Perfilado de tiempos de ejecución o ciclos de clock (delegado a `ferro`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- `graphviz` (`dot`, opcional para renderizar gráficos vectoriales).

### Integración en el Ecosistema
- CLI `giger`. Plugin registrado en `ripley.plugins` (`callgraph`).

---

## Uso Rápido

```bash
# 1. Analizar e imprimir mapa de llamadas
giger callgraph main.c

# 2. Exportar diagrama en sintaxis Mermaid
giger callgraph main.c --mermaid

# 3. Salida estructurada JSON
giger callgraph main.c --json

# 4. Grafo de flujo de control con código inalcanzable y bucles infinitos
giger cfg main.c                 # Mermaid
giger cfg main.c -f texto        # sólo los hallazgos
```

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `giger check`, `giger callgraph` | Construye el mapa de llamadas entre funciones y detecta recursión y código muerto. |
| `giger cfg` | Grafo de flujo de control de cada función: bloques básicos, código inalcanzable y lazos infinitos. |
| `giger report` | Genera directamente la sección de reporte Markdown de GIGER para Dredd. |
| `giger doctor` | Verifica el estado del entorno de análisis de grafos de llamadas GIGER (Python, GCC, cflow). |

Ayuda de cada comando: `giger <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `giger check`, `giger callgraph`, `giger doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-giger-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `giger`
:open:

```text
 Uso: giger [OPCIONES] COMANDO [ARGUMENTOS]...

 🕸️ GIGER — Mapas de llamadas (Call Graphs), ciclos de recursión y detección de funciones huérfanas
 en C.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de giger y sale.                              │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check      Construye el mapa de llamadas entre funciones y detecta recursión y código muerto.    │
│ callgraph  Construye el mapa de llamadas entre funciones y detecta recursión y código muerto.    │
│ cfg        Grafo de flujo de control de cada función: bloques básicos, código inalcanzable y     │
│            lazos infinitos.                                                                      │
│ report     Genera directamente la sección de reporte Markdown de GIGER para Dredd.               │
│ doctor     Verifica el estado del entorno de análisis de grafos de llamadas GIGER (Python, GCC,  │
│            cflow).                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `giger check`

```text
 Uso: giger check [OPCIONES] {fuente}

 Construye el mapa de llamadas entre funciones y detecta recursión y código muerto.

 Códigos de salida: 0 análisis correcto, 2 archivo inexistente y, solo con
 --fail-on-orphans, 1 si hay funciones huérfanas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a analizar. [obligatorio]                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --mermaid          -m              Emitir diagrama en sintaxis Mermaid.                          │
│ --json                             Salida en JSON.                                               │
│ --md,--output-md   -o      <path>  Generar sección de reporte en formato Markdown para fusión en │
│                                    Dredd.                                                        │
│ --fail-on-orphans                  Salir con código 1 si hay funciones huérfanas (por defecto    │
│                                    siempre 0).                                                   │
│ --help             -h              Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `giger callgraph`

```text
 Uso: giger callgraph [OPCIONES] {fuente}

 Construye el mapa de llamadas entre funciones y detecta recursión y código muerto.

 Códigos de salida: 0 análisis correcto, 2 archivo inexistente y, solo con
 --fail-on-orphans, 1 si hay funciones huérfanas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a analizar. [obligatorio]                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --mermaid          -m              Emitir diagrama en sintaxis Mermaid.                          │
│ --json                             Salida en JSON.                                               │
│ --md,--output-md   -o      <path>  Generar sección de reporte en formato Markdown para fusión en │
│                                    Dredd.                                                        │
│ --fail-on-orphans                  Salir con código 1 si hay funciones huérfanas (por defecto    │
│                                    siempre 0).                                                   │
│ --help             -h              Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `giger cfg`

```text
 Uso: giger cfg [OPCIONES] {fuente}

 Grafo de flujo de control de cada función: bloques básicos, código inalcanzable y lazos infinitos.

 En el grafo Mermaid el código inalcanzable va en rojo punteado y la condición de un lazo infinito
 en
 naranja. Sale con 1 si hay un lazo que no termina nunca (las advertencias no cambian el código).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <file>  Archivo C a analizar. [obligatorio]                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --formato  -f      <str>   mermaid (el grafo), texto (sólo los hallazgos) o json.                │
│                            [por defecto: mermaid]                                                │
│ --funcion          <str>   Sólo esta función.                                                    │
│ --output   -o      <path>  Archivo donde escribir el grafo.                                      │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `giger report`

```text
 Uso: giger report [OPCIONES] {fuente}

 Genera directamente la sección de reporte Markdown de GIGER para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a analizar. [obligatorio]                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `giger doctor`

```text
 Uso: giger doctor [OPCIONES]

 Verifica el estado del entorno de análisis de grafos de llamadas GIGER (Python, GCC, cflow).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`giger@b316ea7`](https://github.com/INGCOM-UNRN-P1/giger/tree/b316ea7).
