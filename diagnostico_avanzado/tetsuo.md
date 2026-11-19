---
title: "tetsuo"
subtitle: "Traductor y Explicador Pedagógico de Sanitizers (ASan / UBSan)"
---

<!-- Generado por scripts/generar_paginas.py desde tetsuo@5e12cce: no editar a mano. -->

(manual-tetsuo)=
# tetsuo — Traductor y Explicador Pedagógico de Sanitizers (ASan / UBSan)

Repositorio: [github.com/INGCOM-UNRN-P1/tetsuo](https://github.com/INGCOM-UNRN-P1/tetsuo).

**TETSUO** compila y ejecuta programas C bajo AddressSanitizer y UndefinedBehaviorSanitizer, interceptando sus salidas complejas en inglés y traduciéndolas a diagnósticos formativos en español con sugerencias concretas de corrección.

---

## Alcance

### Qué cubre
- Compilación instrumentada, ejecución controlada y traducción pedagógica de diagnósticos de sanitizers en programas C.
- Captura y traducción contextual a español rioplatense de advertencias complejas de AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan) y LeakSanitizer (LSan).
- No traduce Valgrind Memcheck, MemorySanitizer ni ThreadSanitizer: solo ASan, UBSan y LSan.
- Identificación de lecturas fuera de límites, accesos tras liberación (use-after-free) y fugas de memoria con indicación precisa de línea y archivo.
- Modo pista para evaluaciones (`--pista` o `P1_PISTA=1`, que ripley exporta con `[general] pistas = true`): la violación, su explicación y la función donde ocurrió, sin la línea, la salida cruda ni la acción correctiva.

### Qué no cubre (Límites y Delegación)
- Confinamiento en sandbox no privilegiado de kernel (delegado a `nostromo`).
- Depuración forense con GDB de core dumps no instrumentados: la cubre `hal`, herramienta complementaria; tetsuo no la invoca ni depende de ella.
- Inyección deliberada de fallos de memoria en runtime (delegado a `vasquez`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux / WSL o Windows (MSYS2 UCRT64). Python >= 3.10.

### Dependencias Externas y Binarios
- `gcc` o `clang` con bibliotecas de sanitizers (`libasan`, `libubsan`), y `valgrind` (opcional).

### Integración en el Ecosistema
- CLI `tetsuo`. Plugin registrado en `ripley.plugins` (`sanitizer_translator`).

---

## Uso Rápido

```bash
# Compilar y ejecutar con sanitizers explicando cualquier fallo
tetsuo run main.c

# Pasar entrada estándar
tetsuo run main.c --input "10\n"

# Salida estructurada JSON
tetsuo run main.c --json
```

---

## Errores Diagnosticados

- **`heap-buffer-overflow`**: Desbordamiento en bloques de memoria dinámica (`malloc`).
- **`stack-buffer-overflow`**: Desbordamiento en arrays locales de la pila.
- **`heap-use-after-free`**: Lectura/escritura en punteros ya liberados.
- **`double-free`**: Múltiples llamadas a `free()` sobre la misma dirección.
- **`undefined-behavior`**: Overflows con signo, desreferencia de nulos o shifts inválidos.

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
| `tetsuo check`, `tetsuo run` | Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier violación a español didáctico. |
| `tetsuo translate` | Traduce el informe de un programa que ya corrió con sanitizers (sin compilarlo ni correrlo). |
| `tetsuo report` | Genera directamente la sección de reporte Markdown de TETSUO para Dredd. |
| `tetsuo doctor` | Verifica el estado del entorno de sanitizers TETSUO (GCC, Clang, soporte libasan/libubsan). |
| `tetsuo version` | Muestra la versión de TETSUO. |

Ayuda de cada comando: `tetsuo <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `tetsuo check`, `tetsuo run`, `tetsuo translate`, `tetsuo doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-tetsuo-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `tetsuo`
:open:

```text
 Uso: tetsuo [OPCIONES] COMANDO [ARGUMENTOS]...

 Traductor y explicador pedagógico de sanitizers (ASan, UBSan, LSan) en español

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de tetsuo y sale.                             │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check      Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier violación a        │
│            español didáctico.                                                                    │
│ run        Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier violación a        │
│            español didáctico.                                                                    │
│ translate  Traduce el informe de un programa que ya corrió con sanitizers (sin compilarlo ni     │
│            correrlo).                                                                            │
│ report     Genera directamente la sección de reporte Markdown de TETSUO para Dredd.              │
│ doctor     Verifica el estado del entorno de sanitizers TETSUO (GCC, Clang, soporte              │
│            libasan/libubsan).                                                                    │
│ version    Muestra la versión de TETSUO.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tetsuo check`

```text
 Uso: tetsuo check [OPCIONES] {target}

 Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier violación a español didáctico.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .c o binario a ejecutar bajo sanitizers [obligatorio]           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --input           -i      <str>   Entrada estándar (stdin) para la ejecución                     │
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --pista                           Modo pista (o P1_PISTA=1): el tipo de violación y la función,  │
│                                   sin la línea ni la corrección.                                 │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tetsuo run`

```text
 Uso: tetsuo run [OPCIONES] {target}

 Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier violación a español didáctico.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .c o binario a ejecutar bajo sanitizers [obligatorio]           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --input           -i      <str>   Entrada estándar (stdin) para la ejecución                     │
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --pista                           Modo pista (o P1_PISTA=1): el tipo de violación y la función,  │
│                                   sin la línea ni la corrección.                                 │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tetsuo translate`

```text
 Uso: tetsuo translate [OPCIONES] [informe]

 Traduce el informe de un programa que ya corrió con sanitizers (sin compilarlo ni correrlo).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   informe      <file>  Archivo con la salida del programa (el informe de ASan/UBSan/LSan); sin   │
│                        él, se lee de stdin.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json             Emitir salida en formato JSON estructurado                                    │
│ --pista            Modo pista (o P1_PISTA=1): el tipo de violación y la función, sin la línea ni │
│                    la corrección.                                                                │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tetsuo report`

```text
 Uso: tetsuo report [OPCIONES] {target}

 Genera directamente la sección de reporte Markdown de TETSUO para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .c o binario a ejecutar bajo sanitizers [obligatorio]           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --input   -i      <str>   Entrada estándar para la ejecución                                     │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tetsuo doctor`

```text
 Uso: tetsuo doctor [OPCIONES]

 Verifica el estado del entorno de sanitizers TETSUO (GCC, Clang, soporte libasan/libubsan).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `tetsuo version`

```text
 Uso: tetsuo version [OPCIONES]

 Muestra la versión de TETSUO.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`tetsuo@5e12cce`](https://github.com/INGCOM-UNRN-P1/tetsuo/tree/5e12cce).
