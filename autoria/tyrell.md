---
title: "tyrell"
subtitle: "Generador Sintético de Datasets y Casos de Prueba (.in/.out)"
---

<!-- Generado por scripts/generar_paginas.py desde tyrell@aab456c: no editar a mano. -->

(manual-tyrell)=
# tyrell — Generador Sintético de Datasets y Casos de Prueba (.in/.out)

Repositorio: [github.com/INGCOM-UNRN-P1/tyrell](https://github.com/INGCOM-UNRN-P1/tyrell).

**TYRELL** genera colecciones deterministas de casos de prueba (`.in` y `.out`) con restricciones configurables (enteros, flotantes, cadenas, arreglos y valores extremos) en el formato que lee `nostromo test <binario> <directorio>` (un `caso.in` y su `caso.out` por caso; hay un test de extremo a extremo que lo verifica). No hay integración automática con `deckard` ni con el resto de los orquestadores: los archivos se copian a mano al ejercicio o al banco que corresponda.

---

## Alcance

### Qué cubre
- Generación sintética y procedimental de datasets de prueba y casos de test (`.in / .out`) para programas C.
- Generación pseudoaleatoria determinista controlada por semillas para garantizar reproducibilidad en prácticas y exámenes.
- Ejecución y contraste automático contra binarios canónicos de referencia para sintetizar los archivos de salida esperada (`.out`).
- Inyección parametrizada de valores límite numéricos y secuencias estructuradas.
- Casos guiados por cobertura de ramas (`tyrell cubrir`): suma a la suite los casos que ejercitan las ramas que `dietrich lines` reporta sin cubrir.

### Qué no cubre (Límites y Delegación)
- Generación de cuestionarios Moodle XML anti-copia (delegado a `idkfa`).
- Inyección de fallos en llamadas al sistema (delegado a `holden` / `vasquez`).
- Evaluación y corrección masiva de alumnos (delegado a `dredd`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- `gcc` (para compilar soluciones de referencia canónicas si se requiere generar salidas esperadas).
- `tyrell cubrir`: `dietrich` (con `lines --por-entrada`), `gcc` y `gcov`.

### Integración en el Ecosistema
- CLI `tyrell`. Plugin registrado en `ripley.plugins` (`dataset_generator`).

---

## Uso Rápido

```bash
# Generar 20 casos de enteros deterministas
tyrell generate -n 20 --min 1 --max 1000 -o tests/

# Generar casos y contrastar contra binario de referencia para crear los .out
tyrell generate -n 10 -o tests/ --reference ./solucion_canon

# Generar a partir de especificación YAML
tyrell generate spec.yaml -o tests/

# La misma suite más los casos que cubren las ramas que le faltan a la solución modelo
tyrell cubrir spec.yaml solucion.c -o tests/ --reference ./solucion_canon
```

### Casos guiados por cobertura (`tyrell cubrir`)

`tyrell cubrir spec.yaml fuentes.c…` genera la suite de la especificación y le suma casos
`NN_<nombre>_cobertura.in` (con su `.out` si hay `--reference`) para las ramas que no cubre:

1. mide la suite con `dietrich lines --por-entrada` (qué ramas y condiciones ejecuta cada caso);
2. de las decisiones pendientes saca las constantes con que se comparan (`n > 100` → 99, 100 y
   101) y los caracteres (`c == 'q'`), y arma candidatos poniéndolas en las reglas en que caben
   (respetando `min_val`/`max_val`; en un arreglo, como elemento o como cantidad);
3. mide los candidatos y se queda, de a uno, con los que más ramas y condiciones nuevas suman;
   repite con lo que siga pendiente (`--rondas`, 2 por omisión).

Informa la cobertura antes y después, los candidatos que hicieron caer o colgar al programa (no
se agregan) y lo que sigue sin cubrir: si una rama necesita un valor que ninguna regla genera
(por ejemplo, una entrada inválida), hace falta una regla nueva en el YAML o `--corruptos`.

### Especificación YAML (`spec.yaml`)

```yaml
name: suite            # nombre descriptivo (opcional)
count: 10              # cantidad de casos, >= 1
seed: 42               # semilla: misma semilla, mismos casos
format_template: "{a} {b}\n"   # DEBE usar {nombre} de cada regla
rules:
  - name: a
    type: integer      # integer | float | string | array
    min_val: 1
    max_val: 100
  - name: b
    type: array
    length: 5
    min_val: 0
    max_val: 9
```

Los primeros casos son de **borde** y recorren, en orden, los de cada regla: los límites
declarados, `0`, `-1`, `1` y sus vecinos (más `INT_MAX` e `INT_MIN` si la regla no declara
límites); cadenas vacías, con espacios repetidos o al borde, tabulaciones y saltos de línea
consecutivos; arreglos vacíos, de un elemento, con todos iguales, ordenados y en orden inverso.
Después vienen los aleatorios.

Opciones de una regla `array`:

- `orden: aleatorio | ordenado | inverso | casi_ordenado` (el peor caso de un quicksort ingenuo);
- en la plantilla, `{v_n}` es la cantidad de elementos del arreglo `v`: `"{v_n}\n{v}\n"`.

Casos extra al final (también con `--corruptos N` y `--estres LARGO`):

```yaml
corruptos: 5            # truncadas, con bytes no imprimibles, sin salto final, letras donde van números, vacías
estres_longitud: 2000000 # un caso con arreglos y cadenas de ese largo (unos 10 MB)
```

Reglas de validación (se rechaza con código de salida 2 y un mensaje concreto):

- `type` solo admite `integer`, `float`, `string` y `array`.
- Las claves desconocidas (por ejemplo `max_value` en lugar de `max_val`) son un error.
- `format_template` debe usar cada `{nombre}` de las reglas: sin placeholders todos
  los casos saldrían idénticos, y un placeholder sin regla o una regla sin usar son error.
- Un archivo de especificación inexistente es un error; ya no se genera un dataset por defecto.

**Precedencia:** con un YAML, la especificación manda. `--count`, `--seed`, `--type`,
`--min` y `--max` se ignoran (y se avisa cuáles). Sin YAML se usan esas opciones.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `tyrell generate` | Genera casos de prueba .in (y .out con binario de referencia) deterministas. |
| `tyrell cubrir` | Genera la suite y le suma casos que ejercitan las ramas que dietrich reporta sin cubrir. |
| `tyrell version` | Muestra la versión de TYRELL. |
| `tyrell doctor` | Verifica el estado del entorno de TYRELL (Python, GCC opcional). |

Ayuda de cada comando: `tyrell <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `tyrell generate`, `tyrell cubrir`, `tyrell doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-tyrell-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `tyrell`
:open:

```text
 Uso: tyrell [OPCIONES] COMANDO [ARGUMENTOS]...

 Generador sintético y determinista de datasets y casos de prueba (.in/.out)

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de tyrell y sale.                             │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ generate  Genera casos de prueba .in (y .out con binario de referencia) deterministas.           │
│ cubrir    Genera la suite y le suma casos que ejercitan las ramas que dietrich reporta sin       │
│           cubrir.                                                                                │
│ version   Muestra la versión de TYRELL.                                                          │
│ doctor    Verifica el estado del entorno de TYRELL (Python, GCC opcional).                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tyrell generate`

```text
 Uso: tyrell generate [OPCIONES] [spec_file]

 Genera casos de prueba .in (y .out con binario de referencia) deterministas.

 Con un YAML, la especificación manda: `--count`, `--seed`, `--type`, `--min`
 y `--max` se ignoran (se avisa cuáles). Sin YAML se usan esas opciones.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   spec_file      <path>  Archivo YAML de especificación de dataset                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --count      -n      <int>               Cantidad de casos de prueba a generar [por defecto: 10] │
│ --seed       -s      <int>               Semilla para reproducibilidad [por defecto: 42]         │
│ --type       -t      <str>               Tipo de dato si no se pasa YAML (integer, float,        │
│                                          string, array)                                          │
│                                          [por defecto: integer]                                  │
│ --min                <int>               Valor mínimo [por defecto: 0]                           │
│ --max                <int>               Valor máximo [por defecto: 100]                         │
│ --output     -o      <path>              Directorio de destino de los archivos .in/.out          │
│                                          [por defecto: tests]                                    │
│ --reference  -r      <path>              Binario ejecutable de referencia para generar los .out  │
│ --json                                   Emitir salida en formato JSON estructurado              │
│ --corruptos          <int range> [x>=0]  Sumar N casos con entradas corruptas (truncadas, bytes  │
│                                          no imprimibles, letras donde van números).              │
│                                          [por defecto: 0]                                        │
│ --estres             <int range> [x>=1]  Sumar un caso de estrés con arreglos y cadenas de esta  │
│                                          longitud.                                               │
│ --help       -h                          Muestra esta ayuda y sale.                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tyrell cubrir`

```text
 Uso: tyrell cubrir [OPCIONES] {spec_file} {fuentes}...

 Genera la suite y le suma casos que ejercitan las ramas que dietrich reporta sin cubrir.

 De las decisiones pendientes saca las constantes con que se comparan (`n > 100` → 99, 100, 101)
 y los caracteres; arma candidatos con las reglas del YAML y se queda con los que suman ramas o
 condiciones. Necesita dietrich instalado (mide con gcc y gcov).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_file      <path>  Archivo YAML de especificación de dataset (el de tyrell generate)    │
│                             [obligatorio]                                                        │
│ *    fuentes        <file>  Fuentes C del programa cuya cobertura se mide (la solución modelo).  │
│                             [obligatorio]                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output      -o      <path>              Directorio de destino de los archivos .in/.out         │
│                                           [por defecto: tests]                                   │
│ --reference   -r      <path>              Binario de referencia para generar los .out            │
│ --candidatos          <int range> [x>=1]  Candidatos que se miden en cada ronda.                 │
│                                           [por defecto: 40]                                      │
│ --rondas              <int range> [x>=1]  Rondas de restricciones → candidatos → selección.      │
│                                           [por defecto: 2]                                       │
│ --cflags              <str>               Banderas extra para compilar las fuentes al medir.     │
│ --json                                    Emitir salida en formato JSON estructurado             │
│ --help        -h                          Muestra esta ayuda y sale.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tyrell version`

```text
 Uso: tyrell version [OPCIONES]

 Muestra la versión de TYRELL.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tyrell doctor`

```text
 Uso: tyrell doctor [OPCIONES]

 Verifica el estado del entorno de TYRELL (Python, GCC opcional).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`tyrell@aab456c`](https://github.com/INGCOM-UNRN-P1/tyrell/tree/aab456c).
