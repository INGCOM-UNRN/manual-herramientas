---
title: "vasquez"
subtitle: "Motor de Inyección de Fallos de Entorno en C (Fault Injection Engine)"
---

<!-- Generado por scripts/generar_paginas.py desde vasquez@1d42e85: no editar a mano. -->

(manual-vasquez)=
# vasquez — Motor de Inyección de Fallos de Entorno en C (Fault Injection Engine)

Repositorio: [github.com/INGCOM-UNRN-P1/vasquez](https://github.com/INGCOM-UNRN-P1/vasquez).

**VASQUEZ** intercepta llamadas estándar a la biblioteca de C (`malloc`, `calloc`, `realloc`, `strdup`, `fopen`, `fwrite`, `fread`, `fclose`) mediante `LD_PRELOAD` para inyectar fallos deterministas en tiempo de ejecución (retornos `NULL` o códigos de error simulando falta de memoria o accesos denegados a disco), verificando si el estudiante implementó manejo defensivo de errores o si el programa sufre un `SIGSEGV`.

---

## Alcance

### Qué cubre
- Inyección de fallos en tiempo de ejecución (Runtime Fault Injection) sin deadlocks para programas C.
- Intercepción transparente mediante biblioteca compartida `libvasquez_inject.so` precargada con `LD_PRELOAD`.
- Simulación de fallos controlados en memoria dinámica (`malloc`, `calloc`, `realloc`, `strdup`, `posix_memalign` retornando `NULL` según contadores o patrones).
- Simulación de fallos de sistema de archivos (`fopen`, `fread`, `fwrite`, `fclose` retornando error o `ENOSPC`).
- Detección de fugas de recursos y omisión de manejo de errores en caminos de fallo.

### Qué no cubre (Límites y Delegación)
- Mocks estáticos en tiempo de compilación o enlazado (delegado a `holden`).
- Aislamiento en sandbox de llamadas al sistema mediante bwrap (delegado a `nostromo`).
- Análisis forense de core dumps (delegado a `hal`).
- Orquestación masiva de entregas (delegado a `dredd`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / POSIX compatible con `LD_PRELOAD`. Python >= 3.11.
- Windows nativo (GCC MinGW-w64 UCRT64 de MSYS2): soportado mediante interceptación en enlace; ver [Windows nativo](#manual-vasquez-windows-nativo-interceptacion-en-enlace).

### Dependencias Externas y Binarios
- `gcc` (para compilar la biblioteca interceptora nativa).
- `objcopy` (binutils; sólo en Windows nativo, se instala junto con `gcc` en UCRT64).

### Integración en el Ecosistema
- CLI `vasquez`.
- Plugin registrado en `ripley.plugins` (`fault_injection`).
- Integración con `hal` para inyección runtime (`hal --inject-vasquez`).
- Generación de secciones de informe Markdown para `dredd` (`vasquez report`).

---

## Uso Rápido

```bash
# Inyectar fallos por defecto (malloc y fopen) sobre código fuente o binario
vasquez inject solucion_alumno.c

# Especificar fallos exactos (fallar en el 2do malloc y 1er fopen)
vasquez inject app --faults "malloc:2,fopen:1"

# Salida estructurada JSON
vasquez inject solucion_alumno.c --json

# Proyecto de varios archivos: el .c con main, sus módulos y la carpeta de headers
vasquez check src/main.c src/lista.c src/procesador.c -I include

# Flags adicionales para gcc
vasquez check src/main.c src/lista.c -I include --cflags "-std=c11 -DDEBUG"
```

`inject`/`check`, `stress` y `report` salen con `0` si el programa resiste todos los
fallos, `1` si alguno lo hace caer y `2` si no se pudo evaluar. Si el programa no
compila, VASQUEZ muestra el error de gcc con una pista (falta `-I`, falta el archivo
con `main`, faltan módulos) en lugar de un traceback.

(manual-vasquez-windows-nativo-interceptacion-en-enlace)=
## Windows nativo (interceptación en enlace)

Windows no tiene `LD_PRELOAD` ni `<dlfcn.h>`, y los ejecutables PE no admiten precarga de librerías. En esa plataforma VASQUEZ elige automáticamente otra vía:

1. Compila el `.c` del alumno a objeto con los mismos flags que en Linux (`-O0 -g -fno-builtin-free`).
2. Con `objcopy --redefine-sym` redirige en ese objeto las referencias a `malloc`, `calloc`, `realloc`, `strdup`/`_strdup`, `free`, `fopen`, `fwrite`, `fread` y `fclose` hacia los ganchos `vasquez_hook_*`.
3. Enlaza el resultado con el objeto inyector (`~/.cache/vasquez/libvasquez_link_<hash>.o`), que lee las mismas variables `VASQUEZ_*` que la librería de Linux.

Diferencias respecto de la vía `LD_PRELOAD`:

- **Requiere el fuente `.c`**: un binario ya compilado no puede instrumentarse y se rechaza con un error.
- **Sólo cuenta las llamadas del código del alumno.** En Linux, `LD_PRELOAD` ve también las reservas internas de glibc (por ejemplo, el buffer de `stdout` que reserva el primer `printf`), así que `malloc:1` puede caer en esa reserva. En Windows, `malloc:1` es siempre el primer `malloc` escrito por el alumno.
- `posix_memalign` no existe en UCRT, así que no se intercepta.
- Las caídas se detectan por el código de salida: `0xC0000005` (violación de acceso) se informa como `SIGSEGV`; `0xC0000374` (heap corrupto, p. ej. double free), `0xC0000409` (`__fastfail`) y `3` (`abort()`/`assert()` del UCRT) como `SIGABRT`, entre otros. Como consecuencia, un programa que termina con `return 3` o `exit(3)` se clasifica como abort, no como salida controlada: conviene que los ejercicios usen otros códigos de error.

`vasquez doctor` informa qué vía está activa y verifica `objcopy` y la compilación del objeto inyector.

## Intercepción Avanzada y Sintaxis de Fallos

La opción `--faults` (disponible en `vasquez inject` y `vasquez report`) admite combinaciones separadas por comas de:
- `malloc:<N>`: Falla la N-ésima invocación de `malloc`.
- `calloc:<N>`: Falla la N-ésima invocación de `calloc`.
- `realloc:<N>`: Falla la N-ésima invocación de `realloc`.
- `strdup:<N>`: Falla la N-ésima invocación de `strdup`.
- `posix_memalign:<N>`: Falla la N-ésima invocación de `posix_memalign`.
- `fopen:<N>`: Falla la N-ésima invocación de `fopen` (fija `errno = EACCES` por defecto).
- `fread:<N>`: Falla la N-ésima lectura `fread` retornando 0 y fijando `errno = EIO`.
- `fwrite:<bytes>` / `write:<bytes>` / `write:ENOSPC`: Falla la escritura luego de `<bytes>` o simula disco lleno (`ENOSPC`).
- `fclose:<N>`: Falla la N-ésima invocación de `fclose` retornando `EOF` y fijando `errno = EIO`.
- `<tipo>:<N>:<ERRNO>`: el mismo fallo con otro `errno` (`fopen:1:EMFILE`, `fread:2:EINTR`, `fwrite:0:EROFS`).
- `fread_corto:<N>`: lecturas parciales: cada `fread` devuelve a lo sumo N elementos aunque haya más. Revela los programas que asumen que un `fread` siempre llena el búfer.

### Plan de fallos en YAML

Los escenarios de una actividad pueden quedar escritos en un `vasquez.scenario.yaml` (con
`--plan archivo.yaml`, o sin opciones si está en el directorio del primer fuente), que dredd usa
igual para todo el curso:

```yaml
escenarios:
  - tipo: malloc
    llamada: 2              # falla la segunda reserva
  - tipo: fopen
    errno: EACCES           # permiso denegado
  - tipo: fwrite
    despues_de_bytes: 1024  # disco lleno después de 1 KiB
  - tipo: fread_corto
    elementos: 1            # cada fread lee de a un elemento
opciones:
  fugas: true               # además, fugas en los caminos de error
```

Tipos: `malloc`, `calloc`, `realloc`, `strdup`, `posix_memalign`, `fopen`, `fwrite`, `fread`,
`fclose`, `fread_corto`, `probabilistico`, `cascada`, `basura`. Un plan inválido (un tipo, una
clave o un errno desconocidos) sale con código 2 y dice qué escenario está mal.

#### Generar el plan: `vasquez plan`

`vasquez plan <fuentes.c | binario> -o fallos.yaml` arma la matriz sistemática en vez de escribirla a
mano: ejecuta el programa una vez sin fallos (con `--input` para su entrada), cuenta cuántas veces
llamó a `malloc`, `calloc`, `realloc`, `strdup`, `fopen`, `fread`, `fwrite` y `fclose`, y genera un
escenario por cada llamada (hasta `--max-llamadas`, 10 por defecto) y por cada causa: `fopen` con
`ENOENT` y `EACCES`, `fread`/`fclose` con `EIO`, `fwrite` con disco lleno y `fread_corto`. Con una
biblioteca sin `main` (o con `--estatico`) cuenta los sitios de llamada en el fuente, sin ejecutar.
El conteo de `malloc` incluye las reservas internas de la biblioteca de C (la de `fopen`, la de
`printf`): hacerlas fallar también es un caso real. El archivo pasa la validación de `--plan` antes
de escribirse.

```bash
vasquez plan tp.c --input casos/entrada.txt -o fallos.yaml
vasquez inject tp.c --plan fallos.yaml --input "$(cat casos/entrada.txt)"
vasquez plan lista.c --estatico -o fallos.yaml   # biblioteca sin main
```

```bash
# Inyectar fallo en realloc en la 1ra ocurrencia
vasquez inject app --faults "realloc:1"

# Simular disco lleno (ENOSPC) en escrituras
vasquez inject app --faults "write:ENOSPC"

# Auditoría estricta de fugas de memoria en caminos de error
vasquez inject app --faults "malloc:1" --check-leaks

# Auditoría del entorno y compilador de interceptor
vasquez doctor
```

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
| `vasquez check`, `vasquez inject` | Inyecta fallos controlados (malloc/calloc/realloc NULL, cascada, memoria basura) evaluando la resiliencia del código C. |
| `vasquez plan` | Genera un plan de fallos (fallos.yaml): cada llamada a malloc, calloc, realloc, strdup, fopen, fread, fwrite y fclose que hace el programa, con sus causas (errno), para `vasquez inject --plan`. |
| `vasquez stress` | Ejecuta una prueba de estrés repetitiva con fallos probabilísticos de asignación. |
| `vasquez doctor` | Audita el entorno y verifica la disponibilidad del compilador y la librería de inyección. |
| `vasquez report` | Genera directamente la sección de reporte Markdown de VASQUEZ para Dredd. |
| `vasquez version` | Muestra la versión de VASQUEZ. |

Ayuda de cada comando: `vasquez <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `vasquez check`, `vasquez inject`, `vasquez plan`, `vasquez stress`, `vasquez doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-vasquez-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `vasquez`
:open:

```text
 Uso: vasquez [OPCIONES] COMANDO [ARGUMENTOS]...

 Motor de inyección de fallos de entorno y hardware en C vía LD_PRELOAD

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de vasquez y sale.                            │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check    Inyecta fallos controlados (malloc/calloc/realloc NULL, cascada, memoria basura)        │
│          evaluando la resiliencia del código C.                                                  │
│ inject   Inyecta fallos controlados (malloc/calloc/realloc NULL, cascada, memoria basura)        │
│          evaluando la resiliencia del código C.                                                  │
│ plan     Genera un plan de fallos (fallos.yaml): cada llamada a malloc, calloc, realloc, strdup, │
│          fopen,                                                                                  │
│          fread, fwrite y fclose que hace el programa, con sus causas (errno), para `vasquez      │
│          inject --plan`.                                                                         │
│ stress   Ejecuta una prueba de estrés repetitiva con fallos probabilísticos de asignación.       │
│ doctor   Audita el entorno y verifica la disponibilidad del compilador y la librería de          │
│          inyección.                                                                              │
│ report   Genera directamente la sección de reporte Markdown de VASQUEZ para Dredd.               │
│ version  Muestra la versión de VASQUEZ.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez check`

```text
 Uso: vasquez check [OPCIONES] {fuentes}...

 Inyecta fallos controlados (malloc/calloc/realloc NULL, cascada, memoria basura) evaluando la
 resiliencia del código C.

 Sale con 0 si el programa resiste todos los fallos, 1 si alguno lo hace caer y 2 si no se pudo
 evaluar (por ejemplo, porque no compila).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuentes      <file>  Fuente(s) .c del programa (el que tiene main y sus módulos) o un       │
│                           binario ya compilado.                                                  │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --include                         -I      <path>   Carpeta de headers para gcc (como -I); se     │
│                                                    puede repetir.                                │
│ --cflags                                  <str>    Flags adicionales para gcc, entre comillas    │
│                                                    (por ejemplo: "-std=c11 -DDEBUG").            │
│ --faults                          -f      <str>    Especificación:                               │
│                                                    'malloc:1,malloc:2,fopen:1,fwrite:1024,write… │
│ --fail-malloc-at                          <int>    Fallar en la llamada N a malloc.              │
│ --fail-malloc-prob                        <float>  Probabilidad de fallo en malloc (0.0 a 1.0).  │
│ --fail-realloc-at                         <int>    Fallar en la llamada N a realloc devolviendo  │
│                                                    NULL (Mejora 11).                             │
│ --fail-calloc-at                          <int>    Fallar en la llamada N a calloc devolviendo   │
│                                                    NULL (Mejora 16).                             │
│ --fail-posix-memalign-at                  <int>    Fallar en la llamada N a posix_memalign con   │
│                                                    ENOMEM (Mejora 16).                           │
│ --cascade,--cascade-failures                       Habilitar modo fallo en cascada (tras el      │
│                                                    primer error, todas las llamadas fallan)      │
│                                                    (Mejora 17).                                  │
│ --audit-free-null                                  Auditar invocaciones inocuas a free(NULL) en  │
│                                                    ramas de limpieza (Mejora 20).                │
│ --garbage-memory,--poison-memory                   Rellenar bloques con patrón de memoria basura │
│                                                    (0xA5) para detectar lecturas sin inicializar │
│                                                    (Mejora 25).                                  │
│ --poison-byte                             <int>    Valor byte para envenenamiento de memoria     │
│                                                    (por defecto 0xA5 / 165).                     │
│                                                    [por defecto: 165]                            │
│ --fail-write-after                        <int>    Simular disco lleno tras N bytes escritos.    │
│ --trace                                            Habilitar registro detallado de funciones     │
│                                                    interceptadas.                                │
│ --check-leaks                                      Verificar que no haya fugas de memoria en     │
│                                                    caminos de error.                             │
│ --input                           -i      <str>    Entrada estándar (stdin)                      │
│ --json                                             Emitir salida en formato JSON estructurado    │
│ --md,--output-md                          <path>   Generar sección de reporte en formato         │
│                                                    Markdown para fusión en Dredd.                │
│ --plan                                    <file>   Plan de fallos en YAML                        │
│                                                    (vasquez.scenario.yaml). Sin --plan ni otros  │
│                                                    escenarios, se usa el que esté junto al       │
│                                                    primer fuente.                                │
│ --help                            -h               Muestra esta ayuda y sale.                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez inject`

```text
 Uso: vasquez inject [OPCIONES] {fuentes}...

 Inyecta fallos controlados (malloc/calloc/realloc NULL, cascada, memoria basura) evaluando la
 resiliencia del código C.

 Sale con 0 si el programa resiste todos los fallos, 1 si alguno lo hace caer y 2 si no se pudo
 evaluar (por ejemplo, porque no compila).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuentes      <file>  Fuente(s) .c del programa (el que tiene main y sus módulos) o un       │
│                           binario ya compilado.                                                  │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --include                         -I      <path>   Carpeta de headers para gcc (como -I); se     │
│                                                    puede repetir.                                │
│ --cflags                                  <str>    Flags adicionales para gcc, entre comillas    │
│                                                    (por ejemplo: "-std=c11 -DDEBUG").            │
│ --faults                          -f      <str>    Especificación:                               │
│                                                    'malloc:1,malloc:2,fopen:1,fwrite:1024,write… │
│ --fail-malloc-at                          <int>    Fallar en la llamada N a malloc.              │
│ --fail-malloc-prob                        <float>  Probabilidad de fallo en malloc (0.0 a 1.0).  │
│ --fail-realloc-at                         <int>    Fallar en la llamada N a realloc devolviendo  │
│                                                    NULL (Mejora 11).                             │
│ --fail-calloc-at                          <int>    Fallar en la llamada N a calloc devolviendo   │
│                                                    NULL (Mejora 16).                             │
│ --fail-posix-memalign-at                  <int>    Fallar en la llamada N a posix_memalign con   │
│                                                    ENOMEM (Mejora 16).                           │
│ --cascade,--cascade-failures                       Habilitar modo fallo en cascada (tras el      │
│                                                    primer error, todas las llamadas fallan)      │
│                                                    (Mejora 17).                                  │
│ --audit-free-null                                  Auditar invocaciones inocuas a free(NULL) en  │
│                                                    ramas de limpieza (Mejora 20).                │
│ --garbage-memory,--poison-memory                   Rellenar bloques con patrón de memoria basura │
│                                                    (0xA5) para detectar lecturas sin inicializar │
│                                                    (Mejora 25).                                  │
│ --poison-byte                             <int>    Valor byte para envenenamiento de memoria     │
│                                                    (por defecto 0xA5 / 165).                     │
│                                                    [por defecto: 165]                            │
│ --fail-write-after                        <int>    Simular disco lleno tras N bytes escritos.    │
│ --trace                                            Habilitar registro detallado de funciones     │
│                                                    interceptadas.                                │
│ --check-leaks                                      Verificar que no haya fugas de memoria en     │
│                                                    caminos de error.                             │
│ --input                           -i      <str>    Entrada estándar (stdin)                      │
│ --json                                             Emitir salida en formato JSON estructurado    │
│ --md,--output-md                          <path>   Generar sección de reporte en formato         │
│                                                    Markdown para fusión en Dredd.                │
│ --plan                                    <file>   Plan de fallos en YAML                        │
│                                                    (vasquez.scenario.yaml). Sin --plan ni otros  │
│                                                    escenarios, se usa el que esté junto al       │
│                                                    primer fuente.                                │
│ --help                            -h               Muestra esta ayuda y sale.                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez plan`

```text
 Uso: vasquez plan [OPCIONES] {fuentes}...

 Genera un plan de fallos (fallos.yaml): cada llamada a malloc, calloc, realloc, strdup, fopen,
 fread, fwrite y fclose que hace el programa, con sus causas (errno), para `vasquez inject --plan`.

 Las llamadas se cuentan ejecutando el programa una vez sin fallos (con la entrada de --input); en
 una biblioteca sin main, o con --estatico, se cuentan los sitios de llamada en el fuente.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuentes      <file>  Fuente(s) .c del programa (el que tiene main y sus módulos) o un       │
│                           binario ya compilado.                                                  │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --include       -I      <path>              Carpeta de headers para gcc (como -I); se puede      │
│                                             repetir.                                             │
│ --cflags                <str>               Flags adicionales para gcc, entre comillas (por      │
│                                             ejemplo: "-std=c11 -DDEBUG").                        │
│ --output        -o      <path>              Archivo del plan (lo lee `vasquez inject --plan`).   │
│                                             [por defecto: fallos.yaml]                           │
│ --max-llamadas          <int range> [x>=1]  Cuántas llamadas de cada función hacer fallar, como  │
│                                             máximo.                                              │
│                                             [por defecto: 10]                                    │
│ --estatico                                  Contar los sitios de llamada en el fuente en vez de  │
│                                             ejecutar el programa (lo que se hace con una         │
│                                             biblioteca sin main).                                │
│ --sin-fugas                                 No pedir la verificación de fugas en los caminos de  │
│                                             error.                                               │
│ --input         -i      <str>               Entrada estándar para la ejecución que cuenta las    │
│                                             llamadas.                                            │
│ --json                                      Emitir el plan y los conteos en JSON.                │
│ --help          -h                          Muestra esta ayuda y sale.                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez stress`

```text
 Uso: vasquez stress [OPCIONES] {fuentes}...

 Ejecuta una prueba de estrés repetitiva con fallos probabilísticos de asignación.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuentes      <file>  Fuente(s) .c del programa (el que tiene main y sus módulos) o un       │
│                           binario ya compilado.                                                  │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --include     -I      <path>   Carpeta de headers para gcc (como -I); se puede repetir.          │
│ --cflags              <str>    Flags adicionales para gcc, entre comillas (por ejemplo:          │
│                                "-std=c11 -DDEBUG").                                              │
│ --iterations  -n      <int>    Cantidad de corridas bajo inyección aleatoria. [por defecto: 10]  │
│ --prob        -p      <float>  Probabilidad de fallo por llamada a malloc (0.0 a 1.0).           │
│                                [por defecto: 0.25]                                               │
│ --json                         Emitir salida en formato JSON.                                    │
│ --help        -h               Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez doctor`

```text
 Uso: vasquez doctor [OPCIONES]

 Audita el entorno y verifica la disponibilidad del compilador y la librería de inyección.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json               Emitir diagnóstico en formato JSON.                                         │
│ --verbose  -v        Mostrar detalle completo.                                                   │
│ --help     -h        Muestra esta ayuda y sale.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez report`

```text
 Uso: vasquez report [OPCIONES] {fuentes}...

 Genera directamente la sección de reporte Markdown de VASQUEZ para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuentes      <file>  Fuente(s) .c del programa (el que tiene main y sus módulos) o un       │
│                           binario ya compilado.                                                  │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --include  -I      <path>  Carpeta de headers para gcc (como -I); se puede repetir.              │
│ --cflags           <str>   Flags adicionales para gcc, entre comillas (por ejemplo: "-std=c11    │
│                            -DDEBUG").                                                            │
│ --output   -o      <path>  Ruta de destino del archivo Markdown.                                 │
│ --faults   -f      <str>   Especificación de fallos (e.g. 'malloc:1,fopen:2,write:ENOSPC').      │
│ --input    -i      <str>   Entrada estándar.                                                     │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vasquez version`

```text
 Uso: vasquez version [OPCIONES]

 Muestra la versión de VASQUEZ.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`vasquez@1d42e85`](https://github.com/INGCOM-UNRN-P1/vasquez/tree/1d42e85).
