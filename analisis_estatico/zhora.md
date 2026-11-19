---
title: "zhora"
subtitle: "Linter y Auditor de Seguridad en Macros C (#define)"
---

<!-- Generado por scripts/generar_paginas.py desde zhora@72ea080: no editar a mano. -->

(manual-zhora)=
# zhora — Linter y Auditor de Seguridad en Macros C (#define)

Repositorio: [github.com/INGCOM-UNRN-P1/zhora](https://github.com/INGCOM-UNRN-P1/zhora).

**ZHORA** audita macros del preprocesador C para detectar efectos de lado en evaluación múltiple de parámetros, falta de paréntesis defensivos en argumentos y cuerpos, y puntos y coma espurios.

---

## Alcance

### Qué cubre
- Linter pedagógico y auditor de seguridad de macros del preprocesador en C (`#define`, reglas `ZH001` a `ZH005`).
- Verificación defensiva de paréntesis en parámetros y cuerpo de macros (`ZH003`, `ZH004`).
- Detección de puntos y coma espurios al final de definiciones de macros (`ZH001`).
- Detección de efectos colaterales indeseados por evaluación múltiple de argumentos en llamadas a macros (`ZH002`).

### Qué no cubre (Límites y Delegación)
- Auditoría de inclusión de cabeceras o dependencias circulares (delegado a `wierzbowski`).
- Traducción de errores del compilador tras la fase de preprocesamiento (delegado a `daedalus` / `esper`).
- Ejecución de código (delegado a `nostromo`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio (análisis estático con Tree-Sitter AST).

### Integración en el Ecosistema
- CLI `zhora`. Plugin registrado en `ripley.plugins` (`macro_security`).

---

## Uso Rápido

```bash
# Auditar macros en archivos y carpetas
zhora audit src/
zhora check src/

# Generar informe en formato Markdown
zhora report src/

# Salida estructurada JSON
zhora audit src/ --json
```

---

## Reglas Auditadas

- **`ZH001`**: Macros que finalizan con punto y coma (`;`), rompiendo sentencias `if/else`.
- **`ZH002`**: Parámetros evaluados más de una vez (riesgo de side effects con `x++`).
- **`ZH003`**: Parámetros de macro no envueltos individualmente en paréntesis `(x)`.
- **`ZH004`**: Cuerpo de expresión matemática no protegido con paréntesis externos.
- **`ZH005`**: Macros de varias sentencias (o con un bloque `{ }` suelto) sin `do { ... } while (0)`: dentro de un `if` sin llaves solo la primera sentencia queda condicionada.

En `ZH002`, `ZH003` y `ZH004` el hallazgo trae además la función `static inline` equivalente
(`suggested_inline` en el JSON), con `int` como tipo provisorio para ajustar.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `zhora check`, `zhora audit` | Audita macros #define en busca de efectos de lado, falta de paréntesis o puntos y coma. |
| `zhora report` | Genera directamente la sección de reporte Markdown de ZHORA para Dredd. |
| `zhora catalog`, `zhora rules` | Muestra el catálogo oficial de reglas de macros de ZHORA y su mapeo al namespace de cátedra. |
| `zhora doctor` | Verifica el estado del entorno de auditoría de macros ZHORA (Tree-Sitter C, Python). |

Ayuda de cada comando: `zhora <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `zhora check`, `zhora audit`, `zhora catalog`, `zhora rules`, `zhora doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-zhora-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `zhora`
:open:

```text
 Uso: zhora [OPCIONES] COMANDO [ARGUMENTOS]...

 Linter y auditor de seguridad en macros del preprocesador C (#define)

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de zhora y sale.                              │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check    Audita macros #define en busca de efectos de lado, falta de paréntesis o puntos y coma. │
│ audit    Audita macros #define en busca de efectos de lado, falta de paréntesis o puntos y coma. │
│ report   Genera directamente la sección de reporte Markdown de ZHORA para Dredd.                 │
│ catalog  Muestra el catálogo oficial de reglas de macros de ZHORA y su mapeo al namespace de     │
│          cátedra.                                                                                │
│ rules    Muestra el catálogo oficial de reglas de macros de ZHORA y su mapeo al namespace de     │
│          cátedra.                                                                                │
│ doctor   Verifica el estado del entorno de auditoría de macros ZHORA (Tree-Sitter C, Python).    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `zhora check`

```text
 Uso: zhora check [OPCIONES] {paths}...

 Audita macros #define en busca de efectos de lado, falta de paréntesis o puntos y coma.

 Exit code: 1 solo si hay hallazgos de severidad ERROR (ZH001, ZH003); los `WARNING`
 (ZH002, ZH004) se informan pero salen con 0.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paths      <path>  Archivos o directorios C a analizar [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `zhora audit`

```text
 Uso: zhora audit [OPCIONES] {paths}...

 Audita macros #define en busca de efectos de lado, falta de paréntesis o puntos y coma.

 Exit code: 1 solo si hay hallazgos de severidad ERROR (ZH001, ZH003); los `WARNING`
 (ZH002, ZH004) se informan pero salen con 0.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paths      <path>  Archivos o directorios C a analizar [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `zhora report`

```text
 Uso: zhora report [OPCIONES] {paths}...

 Genera directamente la sección de reporte Markdown de ZHORA para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paths      <path>  Archivos o directorios C a analizar [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `zhora catalog`

```text
 Uso: zhora catalog [OPCIONES]

 Muestra el catálogo oficial de reglas de macros de ZHORA y su mapeo al namespace de cátedra.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json  -j        Emite el catálogo de reglas de macros en formato JSON versionado.              │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `zhora rules`

```text
 Uso: zhora rules [OPCIONES]

 Muestra el catálogo oficial de reglas de macros de ZHORA y su mapeo al namespace de cátedra.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json  -j        Emite el catálogo de reglas de macros en formato JSON versionado.              │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `zhora doctor`

```text
 Uso: zhora doctor [OPCIONES]

 Verifica el estado del entorno de auditoría de macros ZHORA (Tree-Sitter C, Python).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`zhora@72ea080`](https://github.com/INGCOM-UNRN-P1/zhora/tree/72ea080).
