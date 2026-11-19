---
title: "vassili"
subtitle: "Motor de Mutation Testing en C"
---

<!-- Generado por scripts/generar_paginas.py desde vassili@65826b0: no editar a mano. -->

(manual-vassili)=
# vassili — Motor de Mutation Testing en C

Repositorio: [github.com/INGCOM-UNRN-P1/vassili](https://github.com/INGCOM-UNRN-P1/vassili).

**VASSILI** evalúa la calidad y exhaustividad real de las suites de prueba de los estudiantes mediante la inyección procedural de mutantes sintéticos en el código fuente C (operadores aritméticos, relacionales y lógicos) y calcula el **Mutation Score** (% de mutantes detectados).

---

## Alcance

### Qué cubre
- Motor de Mutation Testing para código fuente C y evaluación de calidad de suites de pruebas.
- Aplicación de operadores de mutación por **sustitución textual** línea a línea (no sobre un AST): inversión de comparaciones, operadores aritméticos, incrementos, conectores y negaciones lógicas, retornos constantes y, con `--sanitizers`, reservas de memoria y liberaciones. Antes de mutar se enmascaran comentarios y literales de cadena/carácter, así que un `+` dentro de un `"..."` no se toca. No muta literales numéricos salvo los de un `return`.
- Ejecución de la suite de pruebas contra cada mutante generado.
- Cálculo cuantitativo del Mutation Score (porcentaje de mutantes eliminados respecto al total) y reporte de mutantes supervivientes.

### Qué no cubre (Límites y Delegación)
- Cobertura lógica estructural MC/DC (delegado a `dietrich`).
- Fuzzing de entradas extremas de I/O (delegado a `drake`).
- Orquestación de calificaciones masivas de cursos (delegado a `dredd`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / POSIX o Windows (MSYS2 / WSL). Python >= 3.10.

### Dependencias Externas y Binarios
- `gcc`.

### Integración en el Ecosistema
- CLI `vassili`. Plugin registrado en `ripley.plugins` (`mutation_testing`).
- Extra `ecosistema`: `daedalus` compila los mutantes y `nostromo` los ejecuta aislados.

---

## Uso Rápido

```bash
# Ejecutar análisis de mutación sobre un archivo C con testcases
vassili mutate solucion_alumno.c --tests-dir tests/

# Exigir un Mutation Score mínimo del 80%
vassili mutate solucion_alumno.c --tests-dir tests/ --min-score 80

# Salida estructurada JSON
vassili mutate solucion_alumno.c --tests-dir tests/ --json

# Un módulo de TP (sin main) contra su suite de p1_test
vassili mutate ejercicios/ejercicio1/fraccion.c --suite ejercicios/ejercicio1/prueba.c
```

### Perfil de cátedra

`--perfil catedra` deja los operadores que más enseñan en P1 y los ordena por prioridad antes
de aplicar el tope de 50 mutantes:

1. las cotas y el sentido de los lazos: `ROR`, `LCR` y `AOR` en la condición de un `for` o
   `while`, y `UOI` en la cabecera de un `for`;
2. la memoria dinámica: `MSR` y `FDR` (con `--sanitizers`) y `ECR` (con `--plan-vasquez`);
3. las condiciones relacionales y lógicas de los `if` y del operador `?:`.

No muta negaciones sueltas (`LNR`), retornos constantes (`RVR`) ni aritmética fuera de la
cabecera de un lazo, y descarta del listado los mutantes equivalentes (siguen contados en
`equivalent_count` y en `por_operador`). El perfil por omisión es `completo`.

### Plan de fallos para vasquez

Con `--plan-vasquez <ruta>` vassili suma los mutantes `ECR` y, con los que sobreviven (los
chequeos de error que ningún caso ejercita), escribe un plan en el formato de `vasquez inject
--plan`: un escenario por cada invocación de esa función (hasta 10; `fopen` con `ENOENT` y
`EACCES`) y `fugas: true` para revisar también las fugas en esos caminos. Si la ruta es un
directorio se escribe `vasquez.scenario.yaml`, que vasquez toma solo cuando está junto al primer
fuente:

```bash
vassili mutate lista.c --tests-dir tests/ --plan-vasquez .
vasquez inject main.c lista.c   # usa ./vasquez.scenario.yaml, junto a main.c
```

El número de invocación no se deduce del fuente: el plan cubre todas las de esa función, pero
sólo de las funciones cuyo chequeo sobrevivió.

### Con una suite de p1_test

Con `--suite prueba.c` el oráculo no son los `.in`/`.out` sino la suite de la plantilla: cada
mutante del módulo se enlaza con `prueba.c` y se corre con `-q -f`. p1_test (treadstone ≥
`41b344d`) deja en stderr una línea `P1_FALLO` por la aserción que falló, así que de cada mutante
asesinado se informa el test y la aserción (`prueba.c:42: ASSERT_INT_EQ(…)`, o la señal si se
cayó); con `-f` la suite se detiene en el primer test que falla. Los headers y la biblioteca se
toman del `libs/p1_test` de la plantilla (sus fuentes o `libp1_test.a`); si no está, se indican
con `-I` y `--enlazar`. El reporte trae además el resumen por operador (`por_operador`):
cuántos mutantes de cada familia generó, mató y dejó vivos la suite.

---

## Operadores de Mutación

- **`AOR`** (Arithmetic Operator Replacement): `+` ➔ `-`, `-` ➔ `+`, `*` ➔ `/` (el `*` de puntero o desreferencia no se muta).
- **`ROR`** (Relational Operator Replacement): `==` ➔ `!=`, `!=` ➔ `==`, `<` ➔ `<=`, `<=` ➔ `>`, `>` ➔ `>=`, `>=` ➔ `<`.
- **`LCR`** (Logical Connector Replacement): `&&` ➔ `||` y `||` ➔ `&&`.
- **`UOI`** (Unary Operator Increment): `++` ➔ `--` y `--` ➔ `++`; junto con `<` ➔ `<=` revela los errores de borde de los lazos.
- **`LNR`** (Logical Negation Removal): `!condicion` ➔ `condicion`.
- **`RVR`** (Return Value Replacement): `return 0;` ➔ `return 1;` y cualquier otra constante ➔ `return 0;` (no en `main`, donde solo cambiaría el código de salida).
- **`MSR`** (Memory Size Reduction, solo con `--sanitizers`): `malloc(tam)` ➔ `malloc((tam) - 1)`.
- **`FDR`** (Free Deletion, solo con `--sanitizers`): `free(p)` ➔ `(void)0`, una fuga.

- **`ECR`** (Error Check Removal, solo con `--plan-vasquez`): `if (p == NULL)`, `if (!p)` o
  `if ((f = fopen(…)) == NULL)` ➔ `if ((…) && 0)`, cuando el puntero viene de `malloc`, `calloc`,
  `realloc`, `strdup` o `fopen`. Mide si la suite recorre el camino de error, no su calidad sobre
  el camino normal: queda **fuera del score** (está en `por_operador`). Los que sobreviven van al
  plan de fallos de vasquez (ver abajo).

`MSR` y `FDR` solo se generan con `--sanitizers`, que compila y corre con AddressSanitizer: sin
él ningún test puede detectar una reserva de menos o una fuga, y esos mutantes bajarían el score
sin culpa de la suite.

Además:

- **Equivalentes:** si un mutante compila (con `-O2`) al mismo código objeto que el original,
  ningún test puede distinguirlo; se marca `equivalent` y queda fuera del score.
- **Aislamiento:** cada corrida es un proceso aparte con límite de tiempo, de CPU, de memoria
  (512 MB) y de salida (8 MB): un mutante con un bucle infinito o que imprime sin parar no
  cuelga el análisis. Con el extra `ecosistema` corre además dentro del sandbox de `nostromo`
  (bwrap: sin red y sin escribir fuera de él), así que un mutante que borra o pisa archivos no
  toca la máquina del evaluador. El reporte dice cuál se usó (`aislamiento`).
- **Qué caso falta:** de cada mutante que sobrevive se sugiere el caso de prueba que lo mataría
  (en la tabla, el JSON —`sugerencia`— y la sección Markdown).

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
| `vassili check`, `vassili mutate` | Genera mutantes sintéticos del código C y evalúa qué porcentaje es detectado por los tests. |
| `vassili report` | Genera directamente la sección de reporte Markdown de VASSILI para Dredd. |
| `vassili version` | Muestra la versión de VASSILI. |
| `vassili doctor` | Verifica el estado del entorno de VASSILI (Python, GCC). |

Ayuda de cada comando: `vassili <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `vassili check`, `vassili mutate`, `vassili doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-vassili-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `vassili`
:open:

```text
 Uso: vassili [OPCIONES] COMANDO [ARGUMENTOS]...

 Motor de Mutation Testing en C para evaluar la efectividad de los tests

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de vassili y sale.                            │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check    Genera mutantes sintéticos del código C y evalúa qué porcentaje es detectado por los    │
│          tests.                                                                                  │
│ mutate   Genera mutantes sintéticos del código C y evalúa qué porcentaje es detectado por los    │
│          tests.                                                                                  │
│ report   Genera directamente la sección de reporte Markdown de VASSILI para Dredd.               │
│ version  Muestra la versión de VASSILI.                                                          │
│ doctor   Verifica el estado del entorno de VASSILI (Python, GCC).                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vassili check`

```text
 Uso: vassili check [OPCIONES] {source_file}

 Genera mutantes sintéticos del código C y evalúa qué porcentaje es detectado por los tests.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source_file      <path>  Archivo C a mutar [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --tests-dir       -t      <path>   Directorio con casos de prueba .in/.out [por defecto: tests]  │
│ --min-score       -m      <float>  Score mínimo de mutación para aprobar (0-100%)                │
│                                    [por defecto: 70.0]                                           │
│ --timeout                 <float>  Tiempo límite por prueba en segundos [por defecto: 2.0]       │
│ --json                             Emitir salida en formato JSON estructurado                    │
│ --md,--output-md          <path>   Generar sección de reporte en formato Markdown para fusión en │
│                                    Dredd.                                                        │
│ --sanitizers                       Compilar y correr con AddressSanitizer: suma los mutantes de  │
│                                    reserva de menos (MSR) y sin free (FDR), que solo así se      │
│                                    detectan.                                                     │
│ --suite           -s      <file>   Suite de p1_test (prueba.c con su main) que se enlaza con el  │
│                                    módulo mutado en lugar de los casos .in/.out; informa la      │
│                                    aserción que mató a cada mutante.                             │
│ --incluir         -I      <path>   Directorio de headers para compilar con la suite (repetible). │
│                                    Sin -I ni --enlazar se usa el libs/p1_test de la plantilla.   │
│ --enlazar                 <path>   Fuente .c o biblioteca .a a enlazar con la suite (repetible), │
│                                    p. ej. libs/p1_test/libp1_test.a.                             │
│ --perfil                  <str>    Operadores: completo (todos) o catedra (cotas y sentido de    │
│                                    los lazos, memoria dinámica y condiciones, en ese orden de    │
│                                    prioridad; sin los equivalentes en el listado).               │
│                                    [por defecto: completo]                                       │
│ --plan-vasquez            <path>   Suma los mutantes ECR (sin el chequeo de error de malloc,     │
│                                    realloc, fopen…) y escribe en esta ruta (o en                 │
│                                    <dir>/vasquez.scenario.yaml) el plan de fallos de vasquez     │
│                                    para los que sobreviven.                                      │
│ --help            -h               Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vassili mutate`

```text
 Uso: vassili mutate [OPCIONES] {source_file}

 Genera mutantes sintéticos del código C y evalúa qué porcentaje es detectado por los tests.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source_file      <path>  Archivo C a mutar [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --tests-dir       -t      <path>   Directorio con casos de prueba .in/.out [por defecto: tests]  │
│ --min-score       -m      <float>  Score mínimo de mutación para aprobar (0-100%)                │
│                                    [por defecto: 70.0]                                           │
│ --timeout                 <float>  Tiempo límite por prueba en segundos [por defecto: 2.0]       │
│ --json                             Emitir salida en formato JSON estructurado                    │
│ --md,--output-md          <path>   Generar sección de reporte en formato Markdown para fusión en │
│                                    Dredd.                                                        │
│ --sanitizers                       Compilar y correr con AddressSanitizer: suma los mutantes de  │
│                                    reserva de menos (MSR) y sin free (FDR), que solo así se      │
│                                    detectan.                                                     │
│ --suite           -s      <file>   Suite de p1_test (prueba.c con su main) que se enlaza con el  │
│                                    módulo mutado en lugar de los casos .in/.out; informa la      │
│                                    aserción que mató a cada mutante.                             │
│ --incluir         -I      <path>   Directorio de headers para compilar con la suite (repetible). │
│                                    Sin -I ni --enlazar se usa el libs/p1_test de la plantilla.   │
│ --enlazar                 <path>   Fuente .c o biblioteca .a a enlazar con la suite (repetible), │
│                                    p. ej. libs/p1_test/libp1_test.a.                             │
│ --perfil                  <str>    Operadores: completo (todos) o catedra (cotas y sentido de    │
│                                    los lazos, memoria dinámica y condiciones, en ese orden de    │
│                                    prioridad; sin los equivalentes en el listado).               │
│                                    [por defecto: completo]                                       │
│ --plan-vasquez            <path>   Suma los mutantes ECR (sin el chequeo de error de malloc,     │
│                                    realloc, fopen…) y escribe en esta ruta (o en                 │
│                                    <dir>/vasquez.scenario.yaml) el plan de fallos de vasquez     │
│                                    para los que sobreviven.                                      │
│ --help            -h               Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vassili report`

```text
 Uso: vassili report [OPCIONES] {source_file}

 Genera directamente la sección de reporte Markdown de VASSILI para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source_file      <path>  Archivo C a mutar [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output     -o      <path>  Ruta de destino del archivo Markdown.                               │
│ --tests-dir  -t      <path>  Directorio con casos de prueba. [por defecto: tests]                │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vassili version`

```text
 Uso: vassili version [OPCIONES]

 Muestra la versión de VASSILI.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `vassili doctor`

```text
 Uso: vassili doctor [OPCIONES]

 Verifica el estado del entorno de VASSILI (Python, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`vassili@65826b0`](https://github.com/INGCOM-UNRN-P1/vassili/tree/65826b0).
