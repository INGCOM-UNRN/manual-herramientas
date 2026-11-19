---
title: "callahan"
subtitle: "Verificador Formal de Contratos ACSL en C"
---

<!-- Generado por scripts/generar_paginas.py desde callahan@1fd8c9d: no editar a mano. -->

(manual-callahan)=
# callahan — Verificador Formal de Contratos ACSL en C

Repositorio: [github.com/INGCOM-UNRN-P1/callahan](https://github.com/INGCOM-UNRN-P1/callahan).

CALLAHAN realiza análisis y verificación deductiva de contratos formales de software en C escritos en lenguaje de especificación ACSL (`/*@ requires ... ensures ... */`) integrándose con Frama-C (WP).

---

## Alcance

### Qué cubre
- Verificación deductiva formal de código C basada en contratos ACSL (ANSI/ISO C Specification Language).
- Validación de precondiciones (`requires`), postcondiciones (`ensures`) y aserciones intermedias (`assert`).
- Comprobación matemática de invariantes de bucle (`loop invariant`) y variantes de terminación (`loop variant`).
- Control de contratos de enmarcado de memoria (`assigns`).
- Integración automatizada con Frama-C y el plugin WP (Weakest Precondition).

### Qué no cubre (Límites y Delegación)
- Pruebas dinámicas basadas en ejecución de casos de test (delegado a `nostromo`).
- Generación de documentación técnica en Markdown/HTML (delegado a `corbel`).
- Verificación de cobertura estructural MC/DC (delegado a `dietrich`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux o Windows mediante WSL. Python >= 3.10.

### Dependencias Externas y Binarios
- `frama-c` con plugin `wp` y al menos un SMT prover (`alt-ergo` o `z3`; `verify` invoca `-wp-prover alt-ergo,z3`).
  Antes de usar un prover, callahan le pide demostrar una meta falsa; si la demuestra (Z3 4.16 con Frama-C 33 lo hace), no lo usa y `verify` y `doctor` lo avisan. El resultado queda en `~/.cache/callahan/provers.json` hasta que se actualiza el prover o Frama-C.

### Integración en el Ecosistema
- CLI `callahan`. Plugin registrado en `ripley.plugins` (`formal_contracts`). Subcomando `callahan doctor`.

---

## Uso Rápido

```bash
# 1. Extraer e inspeccionar contratos ACSL de un archivo
callahan extract algoritmo.c

# 2. Probar formalmente contratos con Frama-C
callahan verify algoritmo.c

# 2b. Generar la sección de reporte Markdown para Dredd
callahan report algoritmo.c -o callahan.md

# 3. Salida estructurada JSON
callahan extract algoritmo.c --json

# 4. Comprobar provers SMT disponibles (Z3, Alt-Ergo)
callahan doctor

# 5. Esqueletos de contratos ACSL desde los docblocks (@pre, @post, @param, @return)
callahan skeleton tda_lista.h -o contratos.acsl

# 6. Validar que los contratos estén bien escritos, sin correr los provers
callahan check algoritmo.c

# 7. Contratos desde los docblocks de corbel (corbel acsl tda_lista.h -i los deja en el .h)
callahan verify tda_lista.c --header tda_lista.h
```

`skeleton` traduce las condiciones que ya están escritas en C (`n >= 0`, `p != NULL` →
`\valid(p)`) y deja como `TODO` las que están en prosa, junto con sugerencias de `requires
\valid(...)` para los parámetros puntero. `verify` explica cada meta que Frama-C no pudo demostrar
(poscondición, invariante de lazo, acceso a memoria, desborde…) con lo que suele faltar.

`verify` demuestra también la ausencia de desbordes, accesos fuera de rango y divisiones por cero
(`-wp-rte`, salvo con `--sin-rte`), valida antes los contratos como `check` y, si una meta no se
demuestra, busca con qué valores de los parámetros falla: «La función absol no asegura la
postcondición si el parámetro n recibe un valor negativo (ej: n = -1)». En `ejemplos/` hay
algoritmos clásicos anotados (búsqueda binaria, ordenamiento por inserción…) que se demuestran
completos.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Programas del sistema: `frama-c`.

| Sistema | `frama-c` |
|:--|:--|
| Debian / Ubuntu | `opam install frama-c` |
| Fedora | `opam install frama-c` |
| Windows | no existe: usar WSL |
| macOS | `opam install frama-c` |

### Comandos

| Comando | Descripción |
|:--|:--|
| `callahan verify` | Verifica deductivamente las precondiciones, postcondiciones e invariantes del archivo C. |
| `callahan report` | Genera directamente la sección de reporte Markdown de CALLAHAN para Dredd. |
| `callahan check` | Valida que los contratos ACSL estén bien escritos, sin correr los provers. |
| `callahan extract` | Extrae e imprime las cláusulas de contratos ACSL encontradas en el código. |
| `callahan skeleton` | Esqueletos de contratos ACSL a partir de los docblocks (\@pre, \@post, \@param, \@return). |
| `callahan doctor` | Comprueba si el entorno cuenta con Frama-C y provers SMT (Alt-Ergo, Z3). |

Ayuda de cada comando: `callahan <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `callahan verify`, `callahan check`, `callahan extract`, `callahan doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-callahan-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `callahan`
:open:

```text
 Uso: callahan [OPCIONES] COMANDO [ARGUMENTOS]...

 📜 CALLAHAN — Verificador formal de contratos ACSL (pre/post condiciones) y Frama-C WP.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de callahan y sale.                           │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ verify    Verifica deductivamente las precondiciones, postcondiciones e invariantes del archivo  │
│           C.                                                                                     │
│ report    Genera directamente la sección de reporte Markdown de CALLAHAN para Dredd.             │
│ check     Valida que los contratos ACSL estén bien escritos, sin correr los provers.             │
│ extract   Extrae e imprime las cláusulas de contratos ACSL encontradas en el código.             │
│ skeleton  Esqueletos de contratos ACSL a partir de los docblocks (@pre, @post, @param, @return). │
│ doctor    Comprueba si el entorno cuenta con Frama-C y provers SMT (Alt-Ergo, Z3).               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `callahan verify`

```text
 Uso: callahan verify [OPCIONES] {fuente}

 Verifica deductivamente las precondiciones, postcondiciones e invariantes del archivo C.

 Además del contrato, demuestra que no hay desbordes de enteros, accesos fuera de rango ni
 divisiones por cero (salvo con --sin-rte). Antes valida que los contratos estén bien
 escritos (como `callahan check`), y si una meta no se demuestra busca con qué valores
 de los parámetros falla.

 Sale con 0 si todo se probó, 1 si Frama-C rechazó algún contrato (o están mal escritos)
 y 2 si no se pudo verificar (Frama-C no está instalado): un script distingue así una
 regresión real de una dependencia opcional ausente.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C con anotaciones ACSL a verificar. [obligatorio]               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --header              -H      <path>              Encabezado .h con docblocks Doxygen            │
│                                                   (@pre/@post) de corbel o contratos ACSL.       │
│ --json                                            Salida estructurada en JSON.                   │
│ --md,--output-md      -o      <path>              Generar sección de reporte en formato Markdown │
│                                                   para fusión en Dredd.                          │
│ --sin-rte                                         No demostrar la ausencia de desbordes, accesos │
│                                                   inválidos ni divisiones por cero: sólo el      │
│                                                   contrato.                                      │
│ --timeout                     <int range> [x>=1]  Segundos por meta para cada prover.            │
│                                                   [por defecto: 10]                              │
│ --sin-contraejemplos                              No buscar con qué valores de los parámetros    │
│                                                   falla una meta (es más rápido).                │
│ --help                -h                          Muestra esta ayuda y sale.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `callahan report`

```text
 Uso: callahan report [OPCIONES] {fuente}

 Genera directamente la sección de reporte Markdown de CALLAHAN para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C con contratos ACSL a verificar. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `callahan check`

```text
 Uso: callahan check [OPCIONES] {fuente}

 Valida que los contratos ACSL estén bien escritos, sin correr los provers.

 Lista todos los errores (no sólo el primero, como Frama-C) explicados: una variable
 que no existe, un punto y coma que falta, `=` en lugar de `==`. Sale con 1 si hay errores
 y con 2 si Frama-C no está instalado.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C (o .h) con contratos ACSL. [obligatorio]                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Salida en JSON.                                                                │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `callahan extract`

```text
 Uso: callahan extract [OPCIONES] {fuente}

 Extrae e imprime las cláusulas de contratos ACSL encontradas en el código.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuente      <path>  Archivo C a inspeccionar. [obligatorio]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Salida en JSON.                                                                │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `callahan skeleton`

```text
 Uso: callahan skeleton [OPCIONES] {archivo}

 Esqueletos de contratos ACSL a partir de los docblocks (@pre, @post, @param, @return).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo      <file>  Cabecera o fuente con prototipos documentados (@pre, @post).           │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Guardar los contratos en este archivo.                                 │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `callahan doctor`

```text
 Uso: callahan doctor [OPCIONES]

 Comprueba si el entorno cuenta con Frama-C y provers SMT (Alt-Ergo, Z3).

 Sale con 1 si falta Frama-C: sin él `callahan verify` no puede verificar.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el diagnóstico como JSON (schema_version 1.0.0).                        │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`callahan@1fd8c9d`](https://github.com/INGCOM-UNRN-P1/callahan/tree/1fd8c9d).
