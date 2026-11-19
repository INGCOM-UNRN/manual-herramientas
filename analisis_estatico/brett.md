---
title: "brett"
subtitle: "Auditor de Padding y Alineación de Estructuras C"
---

<!-- Generado por scripts/generar_paginas.py desde brett@b582c7e: no editar a mano. -->

(manual-brett)=
# brett — Auditor de Padding y Alineación de Estructuras C

Repositorio: [github.com/INGCOM-UNRN-P1/brett](https://github.com/INGCOM-UNRN-P1/brett).

BRETT analiza la disposición en memoria (`Memory Layout`) de tipos de datos compuestos (`struct`, con o sin `typedef`) en C, mide con el compilador los bytes de relleno (`padding`) desperdiciados por desalineación de campos y genera sugerencias automáticas de reordenamiento para minimizar el tamaño de las estructuras.

---

## Alcance

### Qué cubre
- Auditoría estática y cálculo del layout de memoria de `typedef struct` en C.
- Determinación de offsets de cada campo, tamaño total del tipo y requerimientos de alineación (`alignof`).
- Identificación y cuantificación de bytes de padding desperdiciados por desalineación de campos.
- Generación de propuestas de reordenamiento óptimo de campos para minimizar el consumo de memoria.

### Qué no cubre (Límites y Delegación)
- Decodificación de archivos binarios estructurados en disco con endianness específico (delegado a `kane`).
- Auditoría de visibilidad y ABI en bibliotecas compartidas (delegado a `parker`).
- Publicación directa en servidor LSP en vivo (delegado a `ripley`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma (Linux, Windows, macOS). Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio (análisis estático basado en AST Tree-Sitter).

### Integración en el Ecosistema
- CLI `brett`. Plugin registrado en `ripley.plugins` bajo el identificador `padding`.

---

## Uso Rápido

```bash
# 1. Auditar estructuras en archivos C o cabeceras H
brett audit src/ main.h

# 2. Reordenar los campos que desperdician memoria: emite el diff (o --aplicar lo escribe)
brett optimize tipos.h | patch -p1
brett optimize tipos.h --codigo   # el struct optimizado con sus offsets

# 3. Generar reporte consolidado Markdown
brett report src/

# 4. Salida estructurada JSON
brett audit src/ --json

# 5. En el CI de una actividad: fallar solo si reordenando se ahorran 16 bytes o más
brett audit src/ --fail-on 16

# 6. Con los tamaños de otra ABI (la de Windows, donde long ocupa 4 bytes)
brett audit src/ --abi x86_64-windows
```

`brett optimize` reescribe sólo los structs en los que reordenar ahorra bytes: ordena sus campos de
mayor a menor alineación conservando el texto de cada declaración y sus comentarios (una declaración
con varios campos, `char a, b;`, se separa en una por campo) y emite el diff unificado del archivo.

**ABI** (`--abi`): los tamaños y alineaciones de los tipos primitivos salen de una sola tabla,
`brett.core.layout.ABIS`: `x86_64` (por omisión), `aarch64` y `riscv64` (Linux LP64: coinciden en
los tipos primitivos), `x86_64-windows` (LLP64 de MinGW/MSYS2: `long` de 4 bytes) e `i386` (ILP32:
punteros de 4 bytes y `double` alineado a 4). Es la tabla que leen kane y bishop al fijar esta versión de brett.

El cálculo de offsets y relleno (`brett.core.layout.disponer`) es el único del ecosistema: kane lo
usa para leer los registros de un archivo binario con los mismos offsets que reporta brett.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `brett audit` | Audita estructuras en busca de bytes de memoria desperdiciados por desalineación y padding. |
| `brett report` | Genera directamente la sección de reporte Markdown de BRETT para Dredd. |
| `brett optimize` | Reordena los campos de mayor a menor alineación: emite el diff (`brett optimize x.c \| patch -p1`). |
| `brett doctor` | Verifica el estado del entorno de auditoría de memoria y padding BRETT (Tree-Sitter C, Python, GCC, GDB, pahole). |

Ayuda de cada comando: `brett <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `brett audit`, `brett doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-brett-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `brett`
:open:

```text
 Uso: brett [OPCIONES] COMANDO [ARGUMENTOS]...

 📏 BRETT — Auditor de alineación y padding de estructuras C y optimizador de reordenamiento de
 campos.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de brett y sale.                              │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ audit     Audita estructuras en busca de bytes de memoria desperdiciados por desalineación y     │
│           padding.                                                                               │
│ report    Genera directamente la sección de reporte Markdown de BRETT para Dredd.                │
│ optimize  Reordena los campos de mayor a menor alineación: emite el diff (`brett optimize x.c |  │
│           patch -p1`).                                                                           │
│ doctor    Verifica el estado del entorno de auditoría de memoria y padding BRETT (Tree-Sitter C, │
│           Python, GCC, GDB, pahole).                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `brett audit`

```text
 Uso: brett audit [OPCIONES] {rutas}...

 Audita estructuras en busca de bytes de memoria desperdiciados por desalineación y padding.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Archivos C/H o directorios a auditar. [obligatorio]                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                                        Emitir reporte en JSON.                            │
│ --md,--output-md  -o      <path>              Generar sección de reporte en formato Markdown     │
│                                               para fusión en Dredd.                              │
│ --fail-on                 <int range> [x>=1]  Fallar (código 1) solo si reordenando se           │
│                                               ahorrarían N bytes o más en total.                 │
│ --abi                     <str>               Tamaños de los tipos: x86_64, aarch64, riscv64     │
│                                               (LP64, iguales), x86_64-windows (LLP64: long de 4  │
│                                               B) o i386.                                         │
│                                               [por defecto: x86_64]                              │
│ --help            -h                          Muestra esta ayuda y sale.                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `brett report`

```text
 Uso: brett report [OPCIONES] {rutas}...

 Genera directamente la sección de reporte Markdown de BRETT para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Archivos C/H o directorios a auditar. [obligatorio]                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --abi             <str>   Tamaños de los tipos: x86_64, aarch64, riscv64, x86_64-windows o i386. │
│                           [por defecto: x86_64]                                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `brett optimize`

```text
 Uso: brett optimize [OPCIONES] {archivo}

 Reordena los campos de mayor a menor alineación: emite el diff (`brett optimize x.c | patch -p1`).

 Sólo cambian los structs en los que reordenar ahorra bytes; cada declaración conserva su texto y
 sus
 comentarios. Con --aplicar escribe el archivo; con --codigo muestra el struct optimizado con
 offsets.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo      <file>  Archivo C/H con las estructuras a optimizar. [obligatorio]             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --abi              <str>  Tamaños de los tipos: x86_64, aarch64, riscv64, x86_64-windows o i386. │
│                           [por defecto: x86_64]                                                  │
│ --aplicar                 Reescribir el archivo con los campos reordenados en lugar de mostrar   │
│                           el diff.                                                               │
│ --codigo                  Mostrar cada struct optimizado con sus offsets en lugar del diff.      │
│ --help     -h             Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `brett doctor`

```text
 Uso: brett doctor [OPCIONES]

 Verifica el estado del entorno de auditoría de memoria y padding BRETT (Tree-Sitter C, Python,
 GCC, GDB, pahole).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`brett@b582c7e`](https://github.com/INGCOM-UNRN-P1/brett/tree/b582c7e).
