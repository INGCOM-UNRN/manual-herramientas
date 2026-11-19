---
title: "corbel"
subtitle: "Generador Liviano de Documentación y man pages (man 3) en C"
---

<!-- Generado por scripts/generar_paginas.py desde corbel@69a3c81: no editar a mano. -->

(manual-corbel)=
# corbel — Generador Liviano de Documentación y man pages (man 3) en C

Repositorio: [github.com/INGCOM-UNRN-P1/corbel](https://github.com/INGCOM-UNRN-P1/corbel).

**CORBEL** extrae comentarios estructurados Doxygen (`@brief`, `@param`, `@return`, `@pre`, `@post`) desde cabeceras C (`.h`) y genera páginas estáticas en Markdown o páginas de manual para terminal (`man 3 <modulo>`).

---

## Alcance

### Qué cubre
- Extracción estática de comentarios de documentación estructurada (tipo Doxygen/Javadoc, incluidos los tags `@pre`/`@post`) en archivos de cabecera C (`.h`). No interpreta anotaciones ACSL (`/*@ requires … */`): esas las verifica `callahan`.
- Generación de documentación técnica en Markdown, JSON y páginas de manual Unix (`man 3`). No genera HTML.
- Validación de completitud documental: advertencias sobre funciones públicas sin documentar o discrepancias con los prototipos.

### Qué no cubre (Límites y Delegación)
- Demostración matemática formal de los contratos (delegado a `callahan`).
- Verificación de encapsulamiento y opacidad de TDAs (delegado a `motoko`).
- Verificación de reglas de estilo de código (delegado a `gaff`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- `groff` o `man` (opcional, para visualización de páginas `man 3`).

### Integración en el Ecosistema
- CLI `corbel`. Plugin registrado en `ripley.plugins` (`documentation`).

---

## Uso Rápido

```bash
# Visualizar documentación en terminal
corbel doc tda_lista.h

# Exportar a Markdown
corbel doc tda_lista.h --format markdown -o LISTA_API.md

# Generar página man 3 para UNIX
corbel doc tda_lista.h --format man -o /usr/local/man/man3/tda_lista.3
```

```bash
# Qué falta documentar (y, con --completitud, qué tags le faltan a cada docblock)
corbel check tda_lista.h --completitud

# Porcentaje de la API documentada; con --min sale 1 por debajo (para el CI de la plantilla)
corbel coverage include/ --min 80
```

Un docblock que todavía tiene el texto de relleno de `corbel scaffold` o de `gaff fix`
(`[Descripción breve…]`, `[completar: …]`, y el de versiones anteriores de gaff sin corchetes:
`@brief Descripción de la función`) cuenta como **documentación ausente**: el esqueleto
no es documentación. Con `--completitud` también se marcan los docblocks desactualizados: un
`@param` que ya no está en la firma (se renombró o se sacó) o un `@return` en una función `void`.

### README de una librería

`corbel readme` escribe el README de una librería hecha con `plantilla-libreria`: la versión y el
repositorio (de `library.json`), los objetivos del Makefile, cómo agregarla a un TP
(`./tp.sh add-lib`) y la API de sus cabeceras públicas, con parámetros, retorno, `@pre` y `@post`.
Lo generado va entre las marcas `<!-- corbel:readme:inicio … -->` y `<!-- corbel:readme:fin -->`;
lo que está fuera de ellas no se toca. Una función sin docblock, o con el esqueleto sin completar,
aparece como pendiente. `--check` no escribe y sale con 1 si el README no está al día (para la CI);
la plantilla lo trae como `make readme`.

```bash
corbel readme .            # crea o actualiza README.md
corbel readme . --check    # ¿está al día con el código?
```

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `corbel doc` | Genera documentación a partir de comentarios estructurados o inyecta placeholders en cabeceras C. |
| `corbel stub`, `corbel scaffold` | Agrega placeholders estructurados de documentación (\@brief, \@param, \@return, \@pre, \@post) a todas las funciones, estructuras, uniones, enumeraciones y tipos indocumentados. |
| `corbel lint`, `corbel check` | Audita e informa todos los elementos C que carecen de comentarios Doxygen. |
| `corbel coverage` | Porcentaje de la API pública documentada por completo (docblock, sin relleno y con todos sus tags). |
| `corbel report` | Genera directamente la sección de reporte Markdown de CORBEL para Dredd. |
| `corbel doctor` | Verifica el estado del entorno de documentación CORBEL (Python, man). |
| `corbel acsl` | Exporta cláusulas Doxygen \@pre y \@post hacia contratos formales ACSL legibles por Frama-C WP y Callahan. |
| `corbel manpage` | Genera e instala páginas de manual UNIX (man 3) en formato troff estándar para librerías y TDAs de la cátedra. |
| `corbel readme` | Genera o actualiza el README de una librería (plantilla-libreria) desde su código. |
| `corbel version` | Muestra la versión de CORBEL. |

Ayuda de cada comando: `corbel <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `corbel lint`, `corbel check`, `corbel coverage`, `corbel doctor`, `corbel acsl`, `corbel manpage`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-corbel-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `corbel`
:open:

```text
 Uso: corbel [OPCIONES] COMANDO [ARGUMENTOS]...

 Generador liviano de documentación de APIs, TDAs, man pages (man 3) y scaffolding de comentarios
 en C

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de corbel y sale.                             │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ doc       Genera documentación a partir de comentarios estructurados o inyecta placeholders en   │
│           cabeceras C.                                                                           │
│ stub      Agrega placeholders estructurados de documentación (@brief, @param, @return, @pre,     │
│           @post)                                                                                 │
│           a todas las funciones, estructuras, uniones, enumeraciones y tipos indocumentados.     │
│ scaffold  Agrega placeholders estructurados de documentación (@brief, @param, @return, @pre,     │
│           @post)                                                                                 │
│           a todas las funciones, estructuras, uniones, enumeraciones y tipos indocumentados.     │
│ lint      Audita e informa todos los elementos C que carecen de comentarios Doxygen.             │
│ check     Audita e informa todos los elementos C que carecen de comentarios Doxygen.             │
│ coverage  Porcentaje de la API pública documentada por completo (docblock, sin relleno y con     │
│           todos sus tags).                                                                       │
│ report    Genera directamente la sección de reporte Markdown de CORBEL para Dredd.               │
│ doctor    Verifica el estado del entorno de documentación CORBEL (Python, man).                  │
│ acsl      Exporta cláusulas Doxygen @pre y @post hacia contratos formales ACSL legibles por      │
│           Frama-C WP y Callahan.                                                                 │
│ manpage   Genera e instala páginas de manual UNIX (man 3) en formato troff estándar para         │
│           librerías y TDAs de la cátedra.                                                        │
│ readme    Genera o actualiza el README de una librería (plantilla-libreria) desde su código.     │
│ version   Muestra la versión de CORBEL.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel doc`

```text
 Uso: corbel doc [OPCIONES] {header_path}

 Genera documentación a partir de comentarios estructurados o inyecta placeholders en cabeceras C.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    header_path      <path>  Archivo .h a documentar [obligatorio]                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --format                   -f      <str>   Formato de salida: markdown, man, acsl, json          │
│                                            [por defecto: markdown]                               │
│ --output                   -o      <path>  Archivo de destino (por defecto imprime en consola o  │
│                                            genera archivo según formato)                         │
│ --placeholders,--scaffold  -p              Inyectar placeholders Doxygen en el código fuente en  │
│                                            lugar de exportar documentación                       │
│ --in-place                 -i              Modificar el archivo .h directamente al usar          │
│                                            --placeholders                                        │
│ --help                     -h              Muestra esta ayuda y sale.                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel stub`

```text
 Uso: corbel stub [OPCIONES] {target}

 Agrega placeholders estructurados de documentación (@brief, @param, @return, @pre, @post) a todas
 las funciones, estructuras, uniones, enumeraciones y tipos indocumentados.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .h o .c a documentar [obligatorio]                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --in-place     -i                              Modificar el archivo directamente in-place.       │
│ --output       -o                      <path>  Archivo de destino.                               │
│ --file-header      --no-file-header            Incluir encabezado general @file al inicio del    │
│                                                archivo.                                          │
│                                                [por defecto: file-header]                        │
│ --help         -h                              Muestra esta ayuda y sale.                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel scaffold`

```text
 Uso: corbel scaffold [OPCIONES] {target}

 Agrega placeholders estructurados de documentación (@brief, @param, @return, @pre, @post) a todas
 las funciones, estructuras, uniones, enumeraciones y tipos indocumentados.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .h o .c a documentar [obligatorio]                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --in-place     -i                              Modificar el archivo directamente in-place.       │
│ --output       -o                      <path>  Archivo de destino.                               │
│ --file-header      --no-file-header            Incluir encabezado general @file al inicio del    │
│                                                archivo.                                          │
│                                                [por defecto: file-header]                        │
│ --help         -h                              Muestra esta ayuda y sale.                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel lint`

```text
 Uso: corbel lint [OPCIONES] {target}

 Audita e informa todos los elementos C que carecen de comentarios Doxygen.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .h o .c a auditar [obligatorio]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --completitud                     Auditar además los docblocks existentes e informar los tags    │
│                                   que les faltan (@brief, @param, @return).                      │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel check`

```text
 Uso: corbel check [OPCIONES] {target}

 Audita e informa todos los elementos C que carecen de comentarios Doxygen.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .h o .c a auditar [obligatorio]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                            Emitir salida en formato JSON estructurado                     │
│ --md,--output-md          <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --completitud                     Auditar además los docblocks existentes e informar los tags    │
│                                   que les faltan (@brief, @param, @return).                      │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel coverage`

```text
 Uso: corbel coverage [OPCIONES] {rutas}...

 Porcentaje de la API pública documentada por completo (docblock, sin relleno y con todos sus
 tags).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Cabeceras .h (o directorios) de la API a medir. [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --min           <float>  Porcentaje mínimo: por debajo sale con código 1 (para el CI de la       │
│                          plantilla).                                                             │
│ --json                   Emitir salida en formato JSON estructurado                              │
│ --help  -h               Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel report`

```text
 Uso: corbel report [OPCIONES] {target}

 Genera directamente la sección de reporte Markdown de CORBEL para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Archivo .h o .c a auditar [obligatorio]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output       -o      <path>  Ruta de destino del archivo Markdown.                             │
│ --completitud                  Auditar además los docblocks existentes e informar los tags que   │
│                                les faltan (@brief, @param, @return).                             │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel doctor`

```text
 Uso: corbel doctor [OPCIONES]

 Verifica el estado del entorno de documentación CORBEL (Python, man).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel acsl`

```text
 Uso: corbel acsl [OPCIONES] {header_path}

 Exporta cláusulas Doxygen @pre y @post hacia contratos formales ACSL legibles por Frama-C WP y
 Callahan.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    header_path      <path>  Archivo .h documentado desde el cual exportar contratos ACSL.      │
│                               [obligatorio]                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output    -o      <path>  Archivo .h de salida con los bloques /*@ ... */ inyectados.          │
│ --in-place  -i              Inyectar los bloques ACSL directamente en el archivo .h.             │
│ --json                      Emitir los contratos exportados en formato JSON estructurado.        │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel manpage`

```text
 Uso: corbel manpage [OPCIONES] {target}

 Genera e instala páginas de manual UNIX (man 3) en formato troff estándar para librerías y TDAs de
 la cátedra.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  Archivo .h, directorio o librería de la cátedra (ej. treadstone.h).      │
│                         [obligatorio]                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output       -o      <path>  Ruta del archivo troff (.3) de salida.                            │
│ --install-dir          <path>  Directorio base de manuales donde instalar man3/<modulo>.3.       │
│ --no-install                   No instalar automáticamente en el directorio man3 del usuario.    │
│ --json                         Emitir el resultado en formato JSON estructurado.                 │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel readme`

```text
 Uso: corbel readme [OPCIONES] [raiz]

 Genera o actualiza el README de una librería (plantilla-libreria) desde su código.

 Escribe uso, cómo agregarla a un TP y la API de las cabeceras públicas entre dos marcas
 del README.md; lo que esté fuera de ellas no se toca. Las funciones sin documentar
 aparecen como pendientes.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   raiz      <path>  Carpeta de la librería (la de library.json e include/). [por defecto: .]     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --check             No escribir: salir con 1 si el README no está al día (para la CI).           │
│ --stdout            Imprimir el README en lugar de escribirlo.                                   │
│ --help    -h        Muestra esta ayuda y sale.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `corbel version`

```text
 Uso: corbel version [OPCIONES]

 Muestra la versión de CORBEL.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`corbel@69a3c81`](https://github.com/INGCOM-UNRN-P1/corbel/tree/69a3c81).
