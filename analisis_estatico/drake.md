---
title: "drake"
subtitle: "Fuzzer Pedagógico y Analizador de Límites en C"
---

<!-- Generado por scripts/generar_paginas.py desde drake@cf34a97: no editar a mano. -->

(manual-drake)=
# drake — Fuzzer Pedagógico y Analizador de Límites en C

Repositorio: [github.com/INGCOM-UNRN-P1/drake](https://github.com/INGCOM-UNRN-P1/drake).

DRAKE es una herramienta de fuzzing liviana que genera entradas con valores límite (`INT_MAX`, `INT_MIN`, cadenas largas, carácteres nulos y mutaciones aleatorias) para poner a prueba la robustez de programas C y detectar segfaults antes de las entregas.

---

## Alcance

### Qué cubre
- Fuzzing pedagógico dirigido por límites numéricos y tipos de datos en programas C.
- Inyección automatizada de vectores de prueba con valores extremos (`INT_MAX`, `INT_MIN`, `UINT_MAX`, `0`, cadenas vacías, cadenas gigantes, caracteres no ASCII).
- Detección de caídas prematuras por segfault, desbordamientos de búfer en terminal y bucles infinitos.
- Emisión de reportes con entradas reproducibles mínimas para depuración.
- La entrada mínima es legible: quita líneas y palabras que no hacen a la falla, achica cada entero al más chico que la mantiene (con el borde exacto: «falla con 51», no con 73920), borra o reemplaza los bytes nulos y de control, acorta las rachas («A» × 4096 → las justas) y termina en un salto de línea.

### Qué no cubre (Límites y Delegación)
- Aislamiento del proceso con namespaces y cgroups (delegado a `nostromo`).
- Diagnóstico forense detallado del core dump con GDB (delegado a `hal`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / WSL / MSYS2. Python >= 3.10.

### Dependencias Externas y Binarios
- `gcc` o `clang`.

### Integración en el Ecosistema
- CLI `drake`. Plugin en `ripley.plugins` (`fuzzing`).

---

## Uso Rápido

```bash
# 1. Correr 50 iteraciones de fuzzing contra un programa C
drake fuzz main.c --runs 50

# 2. Salida estructurada JSON
drake fuzz main.c --runs 20 --json

# 3. Lo que rompe al programa, a la suite de regresión del TP (con la salida de la solución)
drake fuzz main.c --guardar-casos tests/ --modelo solucion.c
nostromo test ./programa tests/ --etiqueta regresion
```

### Suite de regresión

Con `--guardar-casos DIR`, cada entrada mínima que hace caer o colgar al programa se agrega a la
suite como `crash_NN.in`, con `crash_NN.tags` (`regresion drake SIGSEGV`, `regresion drake
timeout`…) para correrlos solos con `nostromo test … --etiqueta regresion`. Con `--modelo` se
escribe también `crash_NN.out` con la salida de la solución, y sólo entran los casos que la
solución supera (termina con 0, como exige nostromo): uno en el que la solución también falla se
informa y no se agrega. La numeración sigue después de los `crash_NN` que ya haya y no se repite
una entrada que la suite ya tenga, así que volver a correr drake no pisa ni duplica casos.

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
| `drake check`, `drake fuzz` | Ejecuta fuzzing enviando payloads extremos y mutados a la entrada estándar. |
| `drake report` | Genera directamente la sección de reporte Markdown de DRAKE para Dredd. |
| `drake doctor` | Verifica el estado del entorno de DRAKE (Python, GCC). |
| `drake gen-casos` | Genera casos límite (caso_NN.in/.out) contra la solución modelo, con la salida esperada. |

Ayuda de cada comando: `drake <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `drake check`, `drake fuzz`, `drake doctor`, `drake gen-casos`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-drake-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `drake`
:open:

```text
 Uso: drake [OPCIONES] COMANDO [ARGUMENTOS]...

 ⚡ DRAKE — Fuzzer pedagógico guiado por límites y analizador de robustez en C.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de drake y sale.                              │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check      Ejecuta fuzzing enviando payloads extremos y mutados a la entrada estándar.           │
│ fuzz       Ejecuta fuzzing enviando payloads extremos y mutados a la entrada estándar.           │
│ report     Genera directamente la sección de reporte Markdown de DRAKE para Dredd.               │
│ doctor     Verifica el estado del entorno de DRAKE (Python, GCC).                                │
│ gen-casos  Genera casos límite (caso_NN.in/.out) contra la solución modelo, con la salida        │
│            esperada.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `drake check`

```text
 Uso: drake check [OPCIONES] {fuente}

 Ejecuta fuzzing enviando payloads extremos y mutados a la entrada estándar.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a someter a fuzzing. [obligatorio]                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --runs            -n      <int>    Cantidad de ejecuciones con mutaciones. [por defecto: 50]     │
│ --timeout         -t      <float>  Tiempo límite por corrida en segundos. [por defecto: 1.0]     │
│ --seed            -s      <int>    Semilla para reproducir una campaña exacta (por defecto al    │
│                                    azar; se informa en el reporte).                              │
│ --json                             Salida estructurada en JSON.                                  │
│ --md,--output-md  -o      <path>   Generar sección de reporte en formato Markdown para fusión en │
│                                    Dredd.                                                        │
│ --guardar-casos           <path>   Agregar a esta suite cada entrada mínima que hace fallar o    │
│                                    colgar al programa, como caso de nostromo (crash_NN.in y      │
│                                    .tags con «regresion»); sigue la numeración y no repite       │
│                                    casos.                                                        │
│ --modelo                  <file>   Con --guardar-casos: solución modelo para escribir también la │
│                                    salida esperada (crash_NN.out).                               │
│ --help            -h               Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `drake fuzz`

```text
 Uso: drake fuzz [OPCIONES] {fuente}

 Ejecuta fuzzing enviando payloads extremos y mutados a la entrada estándar.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a someter a fuzzing. [obligatorio]                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --runs            -n      <int>    Cantidad de ejecuciones con mutaciones. [por defecto: 50]     │
│ --timeout         -t      <float>  Tiempo límite por corrida en segundos. [por defecto: 1.0]     │
│ --seed            -s      <int>    Semilla para reproducir una campaña exacta (por defecto al    │
│                                    azar; se informa en el reporte).                              │
│ --json                             Salida estructurada en JSON.                                  │
│ --md,--output-md  -o      <path>   Generar sección de reporte en formato Markdown para fusión en │
│                                    Dredd.                                                        │
│ --guardar-casos           <path>   Agregar a esta suite cada entrada mínima que hace fallar o    │
│                                    colgar al programa, como caso de nostromo (crash_NN.in y      │
│                                    .tags con «regresion»); sigue la numeración y no repite       │
│                                    casos.                                                        │
│ --modelo                  <file>   Con --guardar-casos: solución modelo para escribir también la │
│                                    salida esperada (crash_NN.out).                               │
│ --help            -h               Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `drake report`

```text
 Uso: drake report [OPCIONES] {fuente}

 Genera directamente la sección de reporte Markdown de DRAKE para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a someter a fuzzing. [obligatorio]                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --runs    -n      <int>   Cantidad de ejecuciones con mutaciones. [por defecto: 50]              │
│ --seed    -s      <int>   Semilla para reproducir una campaña exacta.                            │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `drake doctor`

```text
 Uso: drake doctor [OPCIONES]

 Verifica el estado del entorno de DRAKE (Python, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `drake gen-casos`

```text
 Uso: drake gen-casos [OPCIONES] {modelo}

 Genera casos límite (caso_NN.in/.out) contra la solución modelo, con la salida esperada.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    modelo      <file>  Solución modelo de la cátedra (.c). [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida         -o      <path>  Directorio destino de los pares caso_NN.in/.out.                │
│                                  [por defecto: casos]                                            │
│ --spec                   <path>  spec.yaml opcional (tipo_entrada, semillas_extra, tamano_max).  │
│ --cantidad       -n      <int>   Máximo de casos de prueba a generar. [por defecto: 12]          │
│ --segundos               <int>   Tiempo de fuzzing si hay clang/libFuzzer. [por defecto: 15]     │
│ --sin-libfuzzer                  Fuerza el modo determinista.                                    │
│ --json                           Emitir el resultado en JSON.                                    │
│ --help           -h              Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`drake@cf34a97`](https://github.com/INGCOM-UNRN-P1/drake/tree/cf34a97).
