---
title: "sebastian"
subtitle: "Analizador de Recursión y Stack Frame en C"
---

<!-- Generado por scripts/generar_paginas.py desde sebastian@4b19251: no editar a mano. -->

(manual-sebastian)=
# sebastian — Analizador de Recursión y Stack Frame en C

Repositorio: [github.com/INGCOM-UNRN-P1/sebastian](https://github.com/INGCOM-UNRN-P1/sebastian).

SEBASTIAN es una herramienta pedagógica diseñada para analizar algoritmos recursivos en C, medir el consumo de memoria en la pila de ejecución (Stack), detectar riesgos de `Stack Overflow` y renderizar árboles de ejecución interactivos en terminal y diagramas Mermaid.

---

## Alcance

### Qué cubre
- Análisis **estático** (`analyze`/`check`, sin ejecutar nada) de algoritmos recursivos en programas C: tipo de recursión, caso base y riesgo de overflow.
- Trazado **dinámico** (`trace`): compila con instrumentación (vía `daedalus`) y ejecuta en el sandbox de `nostromo` para medir la profundidad máxima realmente alcanzada; requiere `gcc`. Si la medición falla, el resultado vuelve al análisis estático y el campo `origen_medicion` lo declara (`dinamica` o `estatica`).
- Tamaño del marco de pila (Stack Frame Size): es una **estimación heurística** (32 bytes base, +32 con `double`/`long`, +64 con arreglos), no una medición; el consumo pico = profundidad × bytes por frame.
- Detección temprana de riesgos de desbordamiento de pila (Stack Overflow) y ramas recursivas infinitas.
- Visualización del árbol de llamadas recursivas en consola terminal y en diagramas Mermaid.

### Qué no cubre (Límites y Delegación)
- Trazado de llamadas no recursivas en todo el proyecto (delegado a `giger`).
- Perfilado de contadores de hardware del procesador (delegado a `ferro`).
- Aislamiento de ejecución en sandbox (delegado a `nostromo`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / POSIX o Windows (MSYS2 / WSL). Python >= 3.10.

### Dependencias Externas y Binarios
- `gcc`.

### Integración en el Ecosistema
- CLI `sebastian`. Subcomando `sebastian doctor`.

---

## Uso Rápido

```bash
# 1. Trazar ejecución recursiva y renderizar árbol en terminal
sebastian trace factorial.c --function factorial

# 2. Emitir diagrama en sintaxis Mermaid
sebastian trace fibonacci.c --mermaid

# Programa de varios archivos: el include/ se detecta, los demás .c se suman
sebastian trace src/lista.c --source src/main.c --source src/envio.c

# 3. Analizar estáticamente todas las funciones de un archivo
sebastian analyze algoritmo.c

# 4. Salida estructurada JSON para pipelines CI
sebastian trace factorial.c --json
```

### Cuántas llamadas entran en la pila

De cada función recursiva se informa la profundidad máxima antes del Stack Overflow
(`profundidad_maxima_estimada`): el límite de la pila del proceso (`ulimit -s`, 8 MiB por defecto en
Linux; 1 MiB en Windows) dividido por los bytes de cada llamada, que se miden con
`gcc -fstack-usage` (`marco_medido_por_gcc`) o, si no compila, se estiman por el código. Con
`sebastian trace` se agrega cuánto de ese máximo usó la ejecución; pasar del 50 % es riesgo alto.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Programas del sistema: `gcc`.

| Sistema | `gcc` |
|:--|:--|
| Debian / Ubuntu | `sudo apt install gcc` |
| Fedora | `sudo dnf install gcc` |
| Windows | incluido en el entorno de la cátedra (MSYS2 UCRT64) |
| macOS | `xcode-select --install` (clang como `gcc`) |

### Comandos

| Comando | Descripción |
|:--|:--|
| `sebastian trace` | Ejecuta el código instrumentado, traza las llamadas recursivas y visualiza el árbol de ejecución. |
| `sebastian check`, `sebastian analyze` | Analiza estáticamente todas las funciones del archivo en busca de recursión y riesgos de desbordamiento. |
| `sebastian report` | Genera directamente la sección de reporte Markdown de SEBASTIAN para Dredd. |
| `sebastian doctor` | Verifica el estado del entorno de análisis de recursión y stack SEBASTIAN (Python, GCC). |

Ayuda de cada comando: `sebastian <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `sebastian trace`, `sebastian check`, `sebastian analyze`, `sebastian doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-sebastian-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `sebastian`
:open:

```text
 Uso: sebastian [OPCIONES] COMANDO [ARGUMENTOS]...

 🌀 SEBASTIAN — Analizador de llamadas recursivas, consumo de stack frame y riesgos de desborde de
 pila en C.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de sebastian y sale.                          │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ trace    Ejecuta el código instrumentado, traza las llamadas recursivas y visualiza el árbol de  │
│          ejecución.                                                                              │
│ check    Analiza estáticamente todas las funciones del archivo en busca de recursión y riesgos   │
│          de desbordamiento.                                                                      │
│ analyze  Analiza estáticamente todas las funciones del archivo en busca de recursión y riesgos   │
│          de desbordamiento.                                                                      │
│ report   Genera directamente la sección de reporte Markdown de SEBASTIAN para Dredd.             │
│ doctor   Verifica el estado del entorno de análisis de recursión y stack SEBASTIAN (Python,      │
│          GCC).                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `sebastian trace`

```text
 Uso: sebastian trace [OPCIONES] {fuente} [args]...

 Ejecuta el código instrumentado, traza las llamadas recursivas y visualiza el árbol de ejecución.

 Códigos de salida: 0 hay traza, 1 no se pudo obtener (se explica por qué) y 2 archivo inexistente.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C con la función recursiva a trazar. [obligatorio]              │
│      args        <str>   Argumentos para el programa al ejecutar.                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --function  -f               <str>   Nombre de la función recursiva a trazar.                    │
│ --include   -I               <path>  Carpeta de headers (se puede repetir). El include/ del      │
│                                      proyecto se detecta solo.                                   │
│ --source    -s               <path>  Otro .c del programa, como el que tiene main (se puede      │
│                                      repetir).                                                   │
│ --stdin     -i               <str>   Entrada estándar para el programa.                          │
│ --tree          --no-tree            Mostrar árbol de llamadas en terminal. [por defecto: tree]  │
│ --mermaid   -m                       Emitir diagrama en formato Mermaid.                         │
│ --json                               Emitir reporte en formato JSON.                             │
│ --help      -h                       Muestra esta ayuda y sale.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `sebastian check`

```text
 Uso: sebastian check [OPCIONES] {fuente}

 Analiza estáticamente todas las funciones del archivo en busca de recursión y riesgos de
 desbordamiento.

 El análisis lee el fuente sin compilarlo: si el archivo no compila lo avisa, porque el resultado
 puede no ser confiable.

 Códigos de salida: 0 análisis correcto, 2 archivo inexistente y, solo con
 --fail-on-high-risk, 1 si hay riesgo ALTO.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a analizar estáticamente. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                               Emitir reporte en JSON.                                     │
│ --md,--output-md     -o      <path>  Generar sección de reporte en formato Markdown para fusión  │
│                                      en Dredd.                                                   │
│ --fail-on-high-risk                  Salir con código 1 si alguna función tiene riesgo de        │
│                                      overflow ALTO (por defecto siempre 0).                      │
│ --include            -I      <path>  Carpeta de headers (se puede repetir). El include/ del      │
│                                      proyecto se detecta solo.                                   │
│ --help               -h              Muestra esta ayuda y sale.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `sebastian analyze`

```text
 Uso: sebastian analyze [OPCIONES] {fuente}

 Analiza estáticamente todas las funciones del archivo en busca de recursión y riesgos de
 desbordamiento.

 El análisis lee el fuente sin compilarlo: si el archivo no compila lo avisa, porque el resultado
 puede no ser confiable.

 Códigos de salida: 0 análisis correcto, 2 archivo inexistente y, solo con
 --fail-on-high-risk, 1 si hay riesgo ALTO.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a analizar estáticamente. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                               Emitir reporte en JSON.                                     │
│ --md,--output-md     -o      <path>  Generar sección de reporte en formato Markdown para fusión  │
│                                      en Dredd.                                                   │
│ --fail-on-high-risk                  Salir con código 1 si alguna función tiene riesgo de        │
│                                      overflow ALTO (por defecto siempre 0).                      │
│ --include            -I      <path>  Carpeta de headers (se puede repetir). El include/ del      │
│                                      proyecto se detecta solo.                                   │
│ --help               -h              Muestra esta ayuda y sale.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `sebastian report`

```text
 Uso: sebastian report [OPCIONES] {fuente}

 Genera directamente la sección de reporte Markdown de SEBASTIAN para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a analizar. [obligatorio]                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output   -o      <path>  Ruta de destino del archivo Markdown.                                 │
│ --include  -I      <path>  Carpeta de headers (se puede repetir). El include/ del proyecto se    │
│                            detecta solo.                                                         │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `sebastian doctor`

```text
 Uso: sebastian doctor [OPCIONES]

 Verifica el estado del entorno de análisis de recursión y stack SEBASTIAN (Python, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`sebastian@4b19251`](https://github.com/INGCOM-UNRN-P1/sebastian/tree/4b19251).
