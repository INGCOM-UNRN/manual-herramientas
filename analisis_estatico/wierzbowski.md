---
title: "wierzbowski"
subtitle: "Auditor de Grafos de Inclusión, Ciclos y Makefiles en C"
---

<!-- Generado por scripts/generar_paginas.py desde wierzbowski@b9c628c: no editar a mano. -->

(manual-wierzbowski)=
# wierzbowski — Auditor de Grafos de Inclusión, Ciclos y Makefiles en C

Repositorio: [github.com/INGCOM-UNRN-P1/wierzbowski](https://github.com/INGCOM-UNRN-P1/wierzbowski).

**WIERZBOWSKI** analiza la arquitectura de proyectos multi-archivo en C, construyendo el grafo de dependencias de `#include`, detectando dependencias circulares, verificando guardas de inclusión y auditando Makefiles.

---

## Alcance

### Qué cubre
- Auditoría estática de grafos de inclusión de archivos de cabecera (`#include`) y Makefiles en C.
- Detección de dependencias circulares y ciclos de inclusión entre archivos `.h` y `.c`.
- Verificación de presencia de guardas de inclusión defensivas (`#ifndef / #define` o `#pragma once`) en cabeceras `.h`.
- Auditoría de sintaxis y coherencia de reglas en Makefiles de proyectos estudiantiles.

### Qué no cubre (Límites y Delegación)
- Compilación de código ni generación de binarios (delegado a `daedalus`).
- Auditoría del interior de macros preprocesadas (delegado a `zhora`).
- Auditoría de layout de memoria de structs declarados en cabeceras (delegado a `brett`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio (análisis estático de código fuente y Makefiles).

### Integración en el Ecosistema
- CLI `wierzbowski`. Plugin registrado en `ripley.plugins` (`headers_audit`).

---

## Uso Rápido

```bash
# Auditar dependencias en el directorio actual
wierzbowski audit .
wierzbowski check .

# Auditar proyecto específico
wierzbowski audit ./tp_modular/

# Generar informe en formato Markdown
wierzbowski report .

# Salida estructurada JSON
wierzbowski audit . --json
```

---

## Reglas Auditadas

- **Detección de Ciclos**: Grafos de inclusión circulares (`a.h ➔ b.h ➔ a.h`).
- **Guardas de Inclusión**: Falta de `#ifndef / #define` o `#pragma once`.
- **`MKF001`**: Recetas de Makefiles indentadas con espacios en lugar de TAB.
- **`MKF002`**: Reglas sin archivo objetivo sin declaración en `.PHONY`.
- **`MKF003`**: Ausencia de target `clean`.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `wierzbowski check`, `wierzbowski audit` | Audita dependencias entre cabeceras, ciclos de inclusión y Makefiles. |
| `wierzbowski makefile` | Audita un Makefile: flags de la cátedra, .PHONY, tabulaciones y trampas (antes dredd audit-makefile). |
| `wierzbowski report` | Genera directamente la sección de reporte Markdown de WIERZBOWSKI para Dredd. |
| `wierzbowski doctor` | Verifica el estado del entorno de auditoría de dependencias WIERZBOWSKI (Python, Make, GCC). |

Ayuda de cada comando: `wierzbowski <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `wierzbowski check`, `wierzbowski audit`, `wierzbowski makefile`, `wierzbowski doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-wierzbowski-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `wierzbowski`
:open:

```text
 Uso: wierzbowski [OPCIONES] COMANDO [ARGUMENTOS]...

 Auditor de grafos de inclusión de headers, dependencias circulares y Makefiles

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de wierzbowski y sale.                        │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check     Audita dependencias entre cabeceras, ciclos de inclusión y Makefiles.                  │
│ audit     Audita dependencias entre cabeceras, ciclos de inclusión y Makefiles.                  │
│ makefile  Audita un Makefile: flags de la cátedra, .PHONY, tabulaciones y trampas (antes dredd   │
│           audit-makefile).                                                                       │
│ report    Genera directamente la sección de reporte Markdown de WIERZBOWSKI para Dredd.          │
│ doctor    Verifica el estado del entorno de auditoría de dependencias WIERZBOWSKI (Python, Make, │
│           GCC).                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `wierzbowski check`

```text
 Uso: wierzbowski check [OPCIONES] [directory]

 Audita dependencias entre cabeceras, ciclos de inclusión y Makefiles.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   directory      <path>  Directorio raíz del proyecto C a analizar [por defecto: .]              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --mermaid                         Emitir el grafo de inclusiones en formato Mermaid.             │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `wierzbowski audit`

```text
 Uso: wierzbowski audit [OPCIONES] [directory]

 Audita dependencias entre cabeceras, ciclos de inclusión y Makefiles.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   directory      <path>  Directorio raíz del proyecto C a analizar [por defecto: .]              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --mermaid                         Emitir el grafo de inclusiones en formato Mermaid.             │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `wierzbowski makefile`

```text
 Uso: wierzbowski makefile [OPCIONES] [objetivo]

 Audita un Makefile: flags de la cátedra, .PHONY, tabulaciones y trampas (antes dredd
 audit-makefile).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   objetivo      <path>  Makefile o directorio de la entrega. [por defecto: .]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --librerias          <str>  Bibliotecas permitidas, separadas por comas (por defecto: m,         │
│                             pthread, rt, p1_test, check).                                        │
│ --json                      Emitir salida en formato JSON estructurado.                          │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `wierzbowski report`

```text
 Uso: wierzbowski report [OPCIONES] [directory]

 Genera directamente la sección de reporte Markdown de WIERZBOWSKI para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   directory      <path>  Directorio raíz del proyecto C a analizar [por defecto: .]              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `wierzbowski doctor`

```text
 Uso: wierzbowski doctor [OPCIONES]

 Verifica el estado del entorno de auditoría de dependencias WIERZBOWSKI (Python, Make, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`wierzbowski@b9c628c`](https://github.com/INGCOM-UNRN-P1/wierzbowski/tree/b9c628c).
