---
title: "parker"
subtitle: "Auditor de Estabilidad de ABI y Visibilidad de Símbolos en C"
---

<!-- Generado por scripts/generar_paginas.py desde parker@84b4caf: no editar a mano. -->

(manual-parker)=
# parker — Auditor de Estabilidad de ABI y Visibilidad de Símbolos en C

Repositorio: [github.com/INGCOM-UNRN-P1/parker](https://github.com/INGCOM-UNRN-P1/parker).

**PARKER** es un linter y evaluador de interfaces binarias (ABI) en C. Audita bibliotecas compartidas (`.so`), archivos objeto (`.o`) y cabeceras (`.h`) para detectar fugas de símbolos privados, símbolos faltantes y malas prácticas en interfaces públicas.

---

## Alcance

### Qué cubre
- Auditoría de Application Binary Interface (ABI) y control de visibilidad de símbolos en bibliotecas compartidas y objetos C en ELF (`.so` / `.o`). Los `.dll` de Windows no se inspeccionan.
- Detección de fuga de símbolos internos: advertencia sobre funciones globales no documentadas que carecen del calificador `static`.
- Verificación de consistencia entre prototipos de funciones públicas de la cabecera `.h` y la tabla de exportación de símbolos en el binario compilado.

### Qué no cubre (Límites y Delegación)
- Verificación de opacidad de TDAs en código fuente (delegado a `motoko`).
- Auditoría de alineación y padding de structs (delegado a `brett`).
- Medición de costos de saltos o tablas de salto (delegado a `rachel`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / WSL / POSIX. Python >= 3.10.

### Dependencias Externas y Binarios
- `nm` (binutils). Es la única herramienta que parker invoca; `readelf` y `objdump` no se usan.

### Integración en el Ecosistema
- CLI `parker`. Plugin registrado en `ripley.plugins` (`abi_audit`).

---

## Uso Rápido

```bash
# Auditar solo cabecera
parker audit tda_lista.h

# Contrastar cabecera contra biblioteca compilada
parker audit tda_lista.h --binary libtda_lista.so

# Salida estructurada JSON
parker audit tda_lista.h --json

# Cambios de ABI entre dos entregas de la librería (PRK101 quitada, PRK102 otra firma, PRK104 símbolo no exportado)
parker diff entrega1/ entrega2/
```

---

## Reglas Auditadas

- **`PRK001`**: Funciones declaradas `static` dentro de cabeceras públicas.
- **`PRK002`**: Símbolos exportados en la biblioteca sin declaración en la cabecera (fuga de ABI).
- **`PRK003`**: Símbolos declarados en cabecera pública no encontrados en la biblioteca compilada.

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
| `parker check`, `parker audit` | Audita la cabecera (o todas las de un directorio) y contrasta los símbolos exportados por los binarios. |
| `parker diff` | Cambios de ABI entre dos entregas: funciones quitadas o con otra firma (y símbolos que dejaron de exportarse). |
| `parker report` | Genera directamente la sección de reporte Markdown de PARKER para Dredd. |
| `parker doctor` | Verifica el estado del entorno de auditoría ABI PARKER (Python, nm, GCC). |

Ayuda de cada comando: `parker <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `parker check`, `parker audit`, `parker diff`, `parker doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-parker-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `parker`
:open:

```text
 Uso: parker [OPCIONES] COMANDO [ARGUMENTOS]...

 Auditor de estabilidad de ABI, visibilidad de símbolos y cabeceras C

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de parker y sale.                             │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check   Audita la cabecera (o todas las de un directorio) y contrasta los símbolos exportados    │
│         por los binarios.                                                                        │
│ audit   Audita la cabecera (o todas las de un directorio) y contrasta los símbolos exportados    │
│         por los binarios.                                                                        │
│ diff    Cambios de ABI entre dos entregas: funciones quitadas o con otra firma (y símbolos que   │
│         dejaron de exportarse).                                                                  │
│ report  Genera directamente la sección de reporte Markdown de PARKER para Dredd.                 │
│ doctor  Verifica el estado del entorno de auditoría ABI PARKER (Python, nm, GCC).                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `parker check`

```text
 Uso: parker check [OPCIONES] {header}

 Audita la cabecera (o todas las de un directorio) y contrasta los símbolos exportados por los
 binarios.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    header      <path>  Cabecera C (.h) o directorio de proyecto (cabeceras y .so/.o            │
│                          descubiertos)                                                           │
│                          [obligatorio]                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --binary          -b      <path>  Biblioteca compartida (.so) u objeto (.o) a contrastar; se     │
│                                   puede repetir                                                  │
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `parker audit`

```text
 Uso: parker audit [OPCIONES] {header}

 Audita la cabecera (o todas las de un directorio) y contrasta los símbolos exportados por los
 binarios.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    header      <path>  Cabecera C (.h) o directorio de proyecto (cabeceras y .so/.o            │
│                          descubiertos)                                                           │
│                          [obligatorio]                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --binary          -b      <path>  Biblioteca compartida (.so) u objeto (.o) a contrastar; se     │
│                                   puede repetir                                                  │
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `parker diff`

```text
 Uso: parker diff [OPCIONES] {antes} {despues}

 Cambios de ABI entre dos entregas: funciones quitadas o con otra firma (y símbolos que dejaron de
 exportarse).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    antes        <path>  Cabecera o directorio de la entrega anterior. [obligatorio]            │
│ *    despues      <path>  Cabecera o directorio de la entrega nueva. [obligatorio]               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir salida en formato JSON estructurado                                     │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `parker report`

```text
 Uso: parker report [OPCIONES] {header}

 Genera directamente la sección de reporte Markdown de PARKER para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    header      <path>  Cabecera C (.h) o directorio de proyecto [obligatorio]                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --binary  -b      <path>  Biblioteca compartida (.so) u objeto (.o); se puede repetir.           │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `parker doctor`

```text
 Uso: parker doctor [OPCIONES]

 Verifica el estado del entorno de auditoría ABI PARKER (Python, nm, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`parker@84b4caf`](https://github.com/INGCOM-UNRN-P1/parker/tree/84b4caf).
