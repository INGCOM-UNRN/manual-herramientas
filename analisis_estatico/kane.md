---
title: "kane"
subtitle: "Simulador y Depurador Visual de I/O Binario en C"
---

<!-- Generado por scripts/generar_paginas.py desde kane@a86bbb7: no editar a mano. -->

(manual-kane)=
# kane — Simulador y Depurador Visual de I/O Binario en C

Repositorio: [github.com/INGCOM-UNRN-P1/kane](https://github.com/INGCOM-UNRN-P1/kane).

**KANE** inspecciona archivos binarios generados por programas C (`fread`, `fwrite`), desglosando sus registros en tablas legibles mapeadas a definiciones de `struct` C con offsets hexadecimales y detección de bytes truncados.

---

## Alcance

### Qué cubre
- Depuración, inspección y visualización interactiva de archivos binarios en disco generados por código C.
- Decodificación estructurada de datos binarios mapeando un `struct` C, dado en línea (`--struct`) o leído de una cabecera `.h` (`--header` y `--name`).
- Tamaño y alineación de los tipos según la ABI del programa que escribió el archivo (`--abi`: `x86_64` por omisión, `x86_64-windows` para MSYS2, donde `long` ocupa 4 bytes, `i386`, `aarch64`, `riscv64`). La tabla es la de brett (`brett.core.layout.ABIS`), la misma con la que brett mide el relleno y `bishop layout` lo dibuja.
- Interpretación de los campos multibyte en little-endian (por defecto) o big-endian (`--endian`). El orden **no se detecta**: lo decide quien sabe qué máquina escribió el archivo, y el reporte lo declara.
- Sin `--struct`/`--header`, `inspect` muestra una vista previa hexadecimal de los primeros 64 bytes (sin anotaciones de campos); el desglose por campo, tamaño, offset y alineación aparece al indicar el struct.
- Representación de bits de valores de C (`kane bits`): complemento a dos, desborde, IEEE 754 de `float`/`double` y operaciones de bits paso a paso.

### Qué no cubre (Límites y Delegación)
- Cálculo de padding y alineación teórica en memoria RAM (delegado a `brett`); kane aplica las mismas reglas de alineación de C para ubicar los campos dentro del archivo.
- Auditoría de símbolos en bibliotecas compartidas (delegado a `parker`).
- Verificación de permisos y llamadas al sistema de I/O (delegado a `kaneda`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio.

### Integración en el Ecosistema
- CLI `kane`. Plugin registrado en `ripley.plugins` (`binary_io`).

---

## Uso Rápido

```bash
# Inspección con mapeo a estructura C
kane inspect datos.bin --struct "int id, char nombre[30], double promedio"

# Hex dump rápido
kane inspect datos.bin

# Salida estructurada JSON
kane inspect datos.bin --struct "int id, float nota" --json

# Struct leído de una cabecera .h (si define varios, elegí uno con --name)
kane inspect alumnos.bin --header alumno.h --name Alumno

# Archivo escrito por un programa compilado en Windows con MSYS2 (long de 4 bytes)
kane inspect alumnos.bin --header alumno.h --abi x86_64-windows

# Archivo escrito por una máquina big-endian
kane inspect red.bin --struct "int id, short puerto" --endian big

# Qué cambió entre dos grabaciones del mismo struct, registro por registro y campo por campo
kane diff antes.bin despues.bin --header alumno.h --name Alumno
```

### Qué dice el archivo del programa que lo escribió

Con el struct indicado, `inspect` informa además (en la tabla, el JSON —`hallazgos`— y la sección
Markdown):

- **`KANE001`** (error): el último registro está incompleto: qué campos llegaron enteros y cuál quedó
  truncado (`'nota' quedó truncado (2 de 8 B)`).
- **`KANE003`** (error): el tamaño no es múltiplo del struct con relleno pero sí de la suma de sus
  campos: se escribió campo por campo y se lee con el struct entero (o al revés), y los registros
  quedan desalineados.
- **`KANE002`** (advertencia): el relleno entre campos tiene bytes distintos de 0, memoria sin
  inicializar que `fwrite` copió (`registro_t r = {0};`).
- **`KANE004`** (advertencia): un `char[]` sin `'\0'`: la cadena llenó el arreglo sin terminador.

Los errores hacen salir con código 1; las advertencias, no.

### Qué se puede mapear

- Escalares: `char`, `signed/unsigned char`, `short`, `int`, `long`, `long long` (con `unsigned`), `float`, `double`, `bool`, `enum` (como `int`) y los `stdint` (`int8_t`…`uint64_t`, `size_t`).
- Arreglos de una dimensión de cualquier escalar (`int notas[3]`, `char nombre[20]`); la dimensión puede ser un número o un `#define` numérico de la propia cabecera.
- El layout supone el ABI LP64 de x86-64 Linux (`long` = 8 bytes) e incluye el padding que inserta el compilador. Los offsets los calcula brett (`brett.core.layout`), el dueño del layout de structs, así que coinciden con los que informa `brett audit`. `kane diff` ignora el relleno, cuyo contenido no está definido.
- **No se soportan** (y kane lo informa con un error en vez de adivinar): punteros, struct/union anidados, bit-fields, arreglos multidimensionales, `long double` y tipos que no sean los de arriba.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `kane check`, `kane inspect` | Inspecciona y desglosa el contenido de un archivo binario mapeándolo a un struct C. |
| `kane diff` | Compara dos archivos binarios del mismo struct, registro por registro y campo por campo. |
| `kane bits` | Muestra cómo queda guardado un valor en un tipo de C, bit a bit, y las operaciones de bits paso a paso. |
| `kane report` | Genera directamente la sección de reporte Markdown de KANE para Dredd. |
| `kane doctor` | Verifica el estado del entorno de inspección binaria KANE (Python, xxd/hexdump, GCC). |

Ayuda de cada comando: `kane <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `kane check`, `kane inspect`, `kane diff`, `kane bits`, `kane doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-kane-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `kane`
:open:

```text
 Uso: kane [OPCIONES] COMANDO [ARGUMENTOS]...

 Simulador y depurador visual de I/O de bajo nivel y archivos binarios en C

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de kane y sale.                               │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check    Inspecciona y desglosa el contenido de un archivo binario mapeándolo a un struct C.     │
│ inspect  Inspecciona y desglosa el contenido de un archivo binario mapeándolo a un struct C.     │
│ diff     Compara dos archivos binarios del mismo struct, registro por registro y campo por       │
│          campo.                                                                                  │
│ bits     Muestra cómo queda guardado un valor en un tipo de C, bit a bit, y las operaciones de   │
│          bits paso a paso.                                                                       │
│ report   Genera directamente la sección de reporte Markdown de KANE para Dredd.                  │
│ doctor   Verifica el estado del entorno de inspección binaria KANE (Python, xxd/hexdump, GCC).   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `kane check`

```text
 Uso: kane check [OPCIONES] {file_path}

 Inspecciona y desglosa el contenido de un archivo binario mapeándolo a un struct C.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      <path>  Archivo binario (.bin, .dat) a inspeccionar [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --struct          -s      <str>   Especificación de struct: 'int id, char nombre[20], float      │
│                                   nota'                                                          │
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --header          -H      <file>  Cabecera .h de la que se lee la definición del struct          │
│ --name            -n      <str>   Nombre del struct dentro de --header (obligatorio si define    │
│                                   varios)                                                        │
│ --endian          -e      <str>   Orden de bytes con que se interpretan los campos multibyte:    │
│                                   little o big (no se detecta)                                   │
│                                   [por defecto: little]                                          │
│ --abi                     <str>   ABI con que se compiló el programa que escribió el archivo:    │
│                                   tamaño y alineación de los tipos (x86_64, x86_64-windows para  │
│                                   MSYS2, i386, aarch64, riscv64).                                │
│                                   [por defecto: x86_64]                                          │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `kane inspect`

```text
 Uso: kane inspect [OPCIONES] {file_path}

 Inspecciona y desglosa el contenido de un archivo binario mapeándolo a un struct C.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      <path>  Archivo binario (.bin, .dat) a inspeccionar [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --struct          -s      <str>   Especificación de struct: 'int id, char nombre[20], float      │
│                                   nota'                                                          │
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --header          -H      <file>  Cabecera .h de la que se lee la definición del struct          │
│ --name            -n      <str>   Nombre del struct dentro de --header (obligatorio si define    │
│                                   varios)                                                        │
│ --endian          -e      <str>   Orden de bytes con que se interpretan los campos multibyte:    │
│                                   little o big (no se detecta)                                   │
│                                   [por defecto: little]                                          │
│ --abi                     <str>   ABI con que se compiló el programa que escribió el archivo:    │
│                                   tamaño y alineación de los tipos (x86_64, x86_64-windows para  │
│                                   MSYS2, i386, aarch64, riscv64).                                │
│                                   [por defecto: x86_64]                                          │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `kane diff`

```text
 Uso: kane diff [OPCIONES] {archivo_a} {archivo_b}

 Compara dos archivos binarios del mismo struct, registro por registro y campo por campo.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo_a      <path>  Primer archivo binario [obligatorio]                                 │
│ *    archivo_b      <path>  Segundo archivo binario [obligatorio]                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --struct  -s      <str>   Especificación de struct: 'int id, char nombre[20], float nota'        │
│ --header  -H      <file>  Cabecera .h de la que se lee la definición del struct                  │
│ --name    -n      <str>   Nombre del struct dentro de --header (obligatorio si define varios)    │
│ --endian  -e      <str>   Orden de bytes de los campos multibyte: little o big                   │
│                           [por defecto: little]                                                  │
│ --abi             <str>   ABI con que se compiló el programa que escribió el archivo: tamaño y   │
│                           alineación de los tipos (x86_64, x86_64-windows para MSYS2, i386,      │
│                           aarch64, riscv64).                                                     │
│                           [por defecto: x86_64]                                                  │
│ --json                    Emitir salida en formato JSON estructurado                             │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `kane bits`

```text
 Uso: kane bits [OPCIONES] {valor}

 Muestra cómo queda guardado un valor en un tipo de C, bit a bit, y las operaciones de bits paso a
 paso.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    valor      <str>  Valor o expresión de bits: 42, -7, 0x2A, 0b1010, 'A', 3.5, '0x0F & 0xF3', │
│                        '~0', '1 << 3'.                                                           │
│                        [obligatorio]                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --tipo    -t      <str>  Tipo de C: char, short, int, long long, int8_t…uint64_t, size_t, float, │
│                          double (con «unsigned» para los sin signo).                             │
│                          [por defecto: int]                                                      │
│ --endian  -e      <str>  Orden de los bytes en memoria: little (x86, ARM) o big.                 │
│                          [por defecto: little]                                                   │
│ --json                   Salida en JSON.                                                         │
│ --help    -h             Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `kane report`

```text
 Uso: kane report [OPCIONES] {file_path}

 Genera directamente la sección de reporte Markdown de KANE para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      <path>  Archivo binario (.bin, .dat) a inspeccionar [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --struct  -s      <str>   Especificación del struct C.                                           │
│ --header  -H      <file>  Cabecera .h de la que se lee la definición del struct                  │
│ --name    -n      <str>   Nombre del struct dentro de --header (obligatorio si define varios)    │
│ --endian  -e      <str>   Orden de bytes con que se interpretan los campos multibyte: little o   │
│                           big (no se detecta)                                                    │
│                           [por defecto: little]                                                  │
│ --abi             <str>   ABI con que se compiló el programa que escribió el archivo: tamaño y   │
│                           alineación de los tipos (x86_64, x86_64-windows para MSYS2, i386,      │
│                           aarch64, riscv64).                                                     │
│                           [por defecto: x86_64]                                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `kane doctor`

```text
 Uso: kane doctor [OPCIONES]

 Verifica el estado del entorno de inspección binaria KANE (Python, xxd/hexdump, GCC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`kane@a86bbb7`](https://github.com/INGCOM-UNRN-P1/kane/tree/a86bbb7).
