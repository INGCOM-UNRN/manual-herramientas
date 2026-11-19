---
title: "crowe"
subtitle: "Linter de Portabilidad Multi-Arquitectura en C"
---

<!-- Generado por scripts/generar_paginas.py desde crowe@e78c908: no editar a mano. -->

(manual-crowe)=
# crowe — Linter de Portabilidad Multi-Arquitectura en C

Repositorio: [github.com/INGCOM-UNRN-P1/crowe](https://github.com/INGCOM-UNRN-P1/crowe).

**CROWE** analiza código C para detectar asunciones no portables de hardware (endianness, tamaños fijos de punteros, signo de `char`, VLAs y tamaños de `long`) y opcionalmente valida compilación cruzada para `x86_64`, `aarch64` y `riscv64`.

---

## Alcance

### Qué cubre
- Auditoría estática de portabilidad multi-arquitectura en código fuente C (reglas `CRW001` a `CRW005`).
- Detección de truncamiento por casteo de puntero a `int` en 64 bits (`CRW001`).
- Detección de asunciones de signo sobre `char` (`CRW002`) y orden de bytes (`CRW003`).
- Detección de suposiciones rígidas sobre el ancho de `long` (`CRW004`).
- Detección de arreglos de longitud variable (VLAs) con riesgo de desbordamiento de pila (`CRW005`).

### Qué no cubre (Límites y Delegación)
- Emulación o ejecución de binarios de hardware con QEMU (fuera del alcance).
- Auditoría del alineamiento interno de campos de structs (delegado a `brett`).
- Inspección de endianness en disco (delegado a `kane`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio para análisis estático; compiladores GCC cruzados (`aarch64-linux-gnu-gcc`, `riscv64-linux-gnu-gcc`) opcionales para `--cross-compile`.

### Integración en el Ecosistema
- CLI `crowe`. Plugin registrado en `ripley.plugins` (`portability`).

---

## Uso Rápido

```bash
# Auditar portabilidad en archivos C
crowe lint src/
crowe check src/

# Generar informe en formato Markdown
crowe report src/

# Probar compilación multi-arquitectura
crowe lint src/ --cross-compile

# Salida estructurada en JSON
crowe lint src/ --json

# Correr el programa en cada arquitectura (qemu) y comparar la salida con la nativa
crowe run main.c --input caso1.in
```

`crowe run` compila estático con la toolchain de cada arquitectura (`aarch64-linux-gnu-gcc`,
`riscv64-linux-gnu-gcc`), lo ejecuta con `qemu-aarch64`/`qemu-riscv64` (paquete `qemu-user`) y
marca las arquitecturas donde la salida o el código de salida cambian: los errores de portabilidad
que compilan igual (el signo de `char`, el tamaño de `long`, el orden de bytes). Sin toolchain o sin
qemu, esa arquitectura se informa como no disponible.

---

## Reglas Auditadas

- **`CRW001`**: Casteo de puntero a `int` (provoca truncamiento en arquitecturas de 64 bits).
- **`CRW002`**: Uso de `char` esperando valores negativos (en ARM es `unsigned char` por defecto).
- **`CRW003`**: Asunciones fijas de orden de bytes (Endianness).
- **`CRW004`**: Suposición del tamaño de `long` (`sizeof(long) == 4` vs `8`).
- **`CRW005`**: Uso de Variable-Length Arrays (VLAs) con riesgo de desbordamiento de pila.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `crowe lint` | Analiza archivos C buscando asunciones no portables de hardware y endianness. |
| `crowe check` | Gate de portabilidad: lint + verificación multi-arquitectura (lo que invoca ripley). |
| `crowe run` | Corre el programa en cada arquitectura con qemu y compara la salida con la nativa. |
| `crowe report` | Genera directamente la sección de reporte Markdown de CROWE para Dredd. |
| `crowe doctor` | Verifica el estado del entorno de auditoría de portabilidad CROWE (Python, GCC nativo y cross-compiladores). |

Ayuda de cada comando: `crowe <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `crowe lint`, `crowe check`, `crowe run`, `crowe doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-crowe-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `crowe`
:open:

```text
 Uso: crowe [OPCIONES] COMANDO [ARGUMENTOS]...

 Linter de portabilidad multi-arquitectura y compatibilidad C

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de crowe y sale.                              │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ lint    Analiza archivos C buscando asunciones no portables de hardware y endianness.            │
│ check   Gate de portabilidad: lint + verificación multi-arquitectura (lo que invoca ripley).     │
│ run     Corre el programa en cada arquitectura con qemu y compara la salida con la nativa.       │
│ report  Genera directamente la sección de reporte Markdown de CROWE para Dredd.                  │
│ doctor  Verifica el estado del entorno de auditoría de portabilidad CROWE (Python, GCC nativo y  │
│         cross-compiladores).                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `crowe lint`

```text
 Uso: crowe lint [OPCIONES] {paths}...

 Analiza archivos C buscando asunciones no portables de hardware y endianness.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paths      <path>  Archivos o directorios C a analizar [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --cross-compile   -c  --no-cross-compile            Intentar compilación contra toolchains       │
│                                                     x86_64, aarch64 y riscv64 (por defecto       │
│                                                     desactivada en `lint`).                      │
│                                                     [por defecto: no-cross-compile]              │
│ --json                                              Emitir salida en formato JSON estructurado   │
│ --md,--output-md                            <path>  Generar sección de reporte en formato        │
│                                                     Markdown para fusión en Dredd.               │
│ --help            -h                                Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `crowe check`

```text
 Uso: crowe check [OPCIONES] {paths}...

 Gate de portabilidad: lint + verificación multi-arquitectura (lo que invoca ripley).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paths      <path>  Archivos o directorios C a analizar [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --cross-compile   -c  --no-cross-compile            Verificar compilación contra toolchains      │
│                                                     x86_64, aarch64 y riscv64 (por defecto       │
│                                                     activada en `check`, el punto de entrada de  │
│                                                     ripley).                                     │
│                                                     [por defecto: cross-compile]                 │
│ --json                                              Emitir salida en formato JSON estructurado   │
│ --md,--output-md                            <path>  Generar sección de reporte en formato        │
│                                                     Markdown para fusión en Dredd.               │
│ --help            -h                                Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `crowe run`

```text
 Uso: crowe run [OPCIONES] {fuentes}...

 Corre el programa en cada arquitectura con qemu y compara la salida con la nativa.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fuentes      <file>  Fuentes .c del programa. [obligatorio]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --input  -i      <file>  Archivo con la entrada estándar.                                        │
│ --arch   -a      <str>   x86_64, aarch64 o riscv64 (repetible; por defecto, todas).              │
│ --json                   Emitir salida en formato JSON estructurado                              │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `crowe report`

```text
 Uso: crowe report [OPCIONES] {paths}...

 Genera directamente la sección de reporte Markdown de CROWE para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paths      <path>  Archivos o directorios C a analizar [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `crowe doctor`

```text
 Uso: crowe doctor [OPCIONES]

 Verifica el estado del entorno de auditoría de portabilidad CROWE (Python, GCC nativo y
 cross-compiladores).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`crowe@e78c908`](https://github.com/INGCOM-UNRN-P1/crowe/tree/e78c908).
