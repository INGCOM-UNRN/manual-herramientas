---
title: "holden"
subtitle: "Generador de Mocks e Inyección de Fallos en C"
---

<!-- Generado por scripts/generar_paginas.py desde holden@ef5f079: no editar a mano. -->

(manual-holden)=
# holden — Generador de Mocks e Inyección de Fallos en C

Repositorio: [github.com/INGCOM-UNRN-P1/holden](https://github.com/INGCOM-UNRN-P1/holden).

HOLDEN permite generar mocks y envoltorios de enlace (`-Wl,--wrap=symbol`) para simular condiciones adversas de ejecución en pruebas de software C (fallos de `malloc()`, errores de apertura en `fopen()`, generación pseudoaleatoria determinista).

---

## Alcance

### Qué cubre
- Generación de arneses de prueba unitaria en C con aislamiento de dependencias externas.
- Síntesis de funciones de sustitución (Mocks y Stubs) a nivel de código fuente y de enlazador GNU (`ld --wrap`).
- Inyección determinista y programable de fallos de biblioteca: `malloc` retornando `NULL`, `fopen` fallando con error de archivo inexistente (`ENOENT`), o simulación de lecturas truncadas.
- Generación de semillas deterministas para funciones pseudoaleatorias (`rand()`).
- Fallos en un binario ya compilado, sin recompilar ni tocar sus fuentes (`holden run`, Linux): una
  biblioteca precargada con `LD_PRELOAD` y configurada por variables de entorno, para evaluar la
  entrega de un estudiante (dredd) con la misma semántica que `P1_FALLAR_EN`.

### Qué no cubre (Límites y Delegación)
- Campañas de escenarios de fallo con su informe de robustez (`vasquez inject`, `vasquez plan`): holden
  sólo ofrece el mecanismo para un binario (`holden run`), con la misma semántica que sus mocks.
- Ejecución aislada de casos de prueba con límites de CPU (delegado a `nostromo`).
- Generación de mutaciones de código fuente (delegado a `vassili`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / POSIX o Windows (MSYS2 / WSL). Python >= 3.10.

### Dependencias Externas y Binarios
- `gcc`, `ld`.

### Integración en el Ecosistema
- CLI `holden`. Plugin registrado en `ripley.plugins` (`mocks`).

---

## Uso Rápido

```bash
# 1. Generar mock de malloc que falla en la 2da llamada
holden generate malloc --fail-at 2 -o mock_malloc.c

# 2. Salida estructurada JSON
holden generate malloc --json

# 3. Listar funciones mockeables soportadas
holden list

# 4. Archivos: fwrite falla con disco lleno (errno = ENOSPC) en la primera escritura
holden generate fwrite --errno ENOSPC -o mock_fwrite.c

# 5. Varias funciones en un archivo, con rand()/srand() de semilla fija
holden generate fopen fread rand --seed 7 -o mocks.c
gcc main.c mocks.c -Wl,--wrap=fopen -Wl,--wrap=fread -Wl,--wrap=rand -Wl,--wrap=srand
```

Mocks disponibles: `malloc`, `fopen`, `fread`, `fwrite`, `fclose` (fallan desde la llamada
`--fail-at` y dejan en `errno` la causa simulada: `ENOENT`, `EACCES`, `ENOSPC`, `EIO`…) y `rand`
(con `srand`: la semilla del programa se ignora y la secuencia es siempre la misma). Cada mock trae
`holden_reset_<función>()` y `holden_fallar_en_<función>(n)`, y el archivo generado (con una o varias
funciones) trae `holden_reset()`, que vuelve todos los mocks al estado del archivo: contadores, la
llamada que falla (aunque un test la haya cambiado con `holden_fallar_en_*`) y la semilla de `rand`.
Llamalo entre tests (p1_test lo hace solo con `P1_FALLAR_EN`): si no, lo que programó un test sigue
armado en el siguiente y el resultado depende del orden.

### Fallos en un binario sin recompilar: `holden run`

```bash
# La segunda reserva devuelve NULL: ¿el programa lo verifica o se cae?
holden run ./tp --fallar malloc=2

# fopen falla con permiso denegado; rand con semilla fija; JSON para dredd
holden run ./tp -f fopen=1 -e fopen=EACCES --semilla 7 --stdin casos/entrada.txt --json -- datos.txt
```

Sale con 0 si el programa terminó sin caerse (con cualquier código de salida: devolver un error es
manejarlo), 1 si se cayó por una señal o no terminó a tiempo y 2 si no se pudo correr. El JSON dice
qué fallos se inyectaron (`fallos_inyectados`: función y llamada; vacío si el programa nunca llegó a
esa llamada), cuántas llamadas hubo a cada función, la señal y la salida. Las funciones son las de
los mocks (`malloc`, `fopen`, `fread`, `fwrite`, `fclose` y `rand`/`srand`); `malloc` cuenta también
las reservas internas de la biblioteca de C. `holden preload` deja la biblioteca para usarla a mano:
`HOLDEN_FALLAR_EN_MALLOC=2 HOLDEN_ERRNO_FOPEN=EACCES HOLDEN_SEMILLA=7 HOLDEN_INFORME=informe.txt
LD_PRELOAD=… ./programa`. Sólo Linux con glibc; en Windows y macOS, los mocks con `--wrap`.

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
| `holden generate` | Genera un archivo C con la implementación del mock y wrapper de la función. |
| `holden run` | Corre un binario con fallos inyectados por LD_PRELOAD, sin recompilarlo ni tocar sus fuentes. |
| `holden preload` | Compila la biblioteca de interposición y muestra cómo usarla a mano con LD_PRELOAD. |
| `holden list` | Lista las funciones con soporte de mocks preconfigurados. |
| `holden doctor` | Verifica el estado del entorno de HOLDEN (Python, GCC). |

Ayuda de cada comando: `holden <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `holden generate`, `holden run`, `holden list`, `holden doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-holden-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `holden`
:open:

```text
 Uso: holden [OPCIONES] COMANDO [ARGUMENTOS]...

 💉 HOLDEN — Generador de mocks e inyección controlada de fallos en funciones C (malloc, fopen,
 etc.).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de holden y sale.                             │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ generate  Genera un archivo C con la implementación del mock y wrapper de la función.            │
│ run       Corre un binario con fallos inyectados por LD_PRELOAD, sin recompilarlo ni tocar sus   │
│           fuentes.                                                                               │
│ preload   Compila la biblioteca de interposición y muestra cómo usarla a mano con LD_PRELOAD.    │
│ list      Lista las funciones con soporte de mocks preconfigurados.                              │
│ doctor    Verifica el estado del entorno de HOLDEN (Python, GCC).                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `holden generate`

```text
 Uso: holden generate [OPCIONES] {funciones}...

 Genera un archivo C con la implementación del mock y wrapper de la función.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    funciones      <str>  Funciones a mockear (ej: 'malloc', 'fopen fwrite', 'rand'). Van en un │
│                            solo archivo con holden_reset().                                      │
│                            [obligatorio]                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output   -o      <path>  Archivo de destino donde escribir el código C del mock.               │
│ --fail-at  -n      <int>   Número de invocación en la que inyectar el fallo (retornar NULL, 0 o  │
│                            EOF).                                                                 │
│                            [por defecto: 1]                                                      │
│ --seed     -s      <int>   Semilla fija de rand(): srand() del programa se ignora.               │
│                            [por defecto: 42]                                                     │
│ --errno    -e      <str>   Causa del fallo de archivos: ENOENT, EACCES, ENOSPC (disco lleno),    │
│                            EIO…                                                                  │
│ --json                     Salida estructurada en JSON.                                          │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `holden run`

```text
 Uso: holden run [OPCIONES] {binario} [argumentos]...

 Corre un binario con fallos inyectados por LD_PRELOAD, sin recompilarlo ni tocar sus fuentes.

 La misma semántica que los mocks de `generate` y que P1_FALLAR_EN: falla desde la llamada n, con
 la causa en errno. Sale con 0 si el programa terminó sin caerse (cualquier código de salida), 1 si
 se cayó por una señal o no terminó a tiempo, y 2 si no se pudo correr. Sólo Linux.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    binario         <file>  Programa ya compilado (por ejemplo, el de una entrega).             │
│                              [obligatorio]                                                       │
│      argumentos      <str>   Argumentos del programa (después de --).                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --fallar          -f      <str>    función=n: la llamada n a la función (y las siguientes)       │
│                                    falla. malloc, fopen, fread, fwrite o fclose; se repite.      │
│ --errno           -e      <str>    función=ERRNO: la causa que queda en errno (fopen=EACCES,     │
│                                    fwrite=ENOSPC…).                                              │
│ --semilla,--seed  -s      <int>    rand() con semilla fija (srand del programa se ignora).       │
│ --stdin           -i      <file>   Archivo para la entrada estándar del programa.                │
│ --timeout         -t      <float>  Segundos antes de cortar el programa. [por defecto: 10.0]     │
│ --json                             Resultado estructurado en JSON (para dredd).                  │
│ --help            -h               Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `holden preload`

```text
 Uso: holden preload [OPCIONES]

 Compila la biblioteca de interposición y muestra cómo usarla a mano con LD_PRELOAD.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Dónde dejar la biblioteca (por defecto, la caché de holden).           │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `holden list`

```text
 Uso: holden list [OPCIONES]

 Lista las funciones con soporte de mocks preconfigurados.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Salida estructurada en JSON.                                                   │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `holden doctor`

```text
 Uso: holden doctor [OPCIONES]

 Verifica el estado del entorno de HOLDEN (Python, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`holden@ef5f079`](https://github.com/INGCOM-UNRN-P1/holden/tree/ef5f079).
