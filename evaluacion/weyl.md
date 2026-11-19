---
title: "weyl"
subtitle: "Diffing Semántico y Comparación Estructural en C"
---

<!-- Generado por scripts/generar_paginas.py desde weyl@a83f6b2: no editar a mano. -->

(manual-weyl)=
# weyl — Diffing Semántico y Comparación Estructural en C

Repositorio: [github.com/INGCOM-UNRN-P1/weyl](https://github.com/INGCOM-UNRN-P1/weyl).

WEYL compara semánticamente dos archivos de código fuente C función por función, abstrayendo diferencias de espaciado para identificar qué funciones fueron agregadas, eliminadas o modificadas respecto a la solución modelo.

---

## Alcance

### Qué cubre
- Comparación semántica y diffing estructural de código C por bloques y funciones. Esa extracción es textual (expresiones regulares y balanceo de llaves sobre el fuente sin comentarios ni literales).
- Matriz de similitud de un lote de entregas sobre el AST (`weyl cohort`, con Tree-Sitter): renombrar y reordenar funciones no cambia el resultado.
- Identificación de divergencias algorítmicas entre entregas de estudiantes y soluciones modelo canónicas.
- Resistencia a técnicas de ofuscación de código: inmune a renombrado de variables, reordenamiento de funciones y cambios superficiales de formato.
- Detección de copias y similitud semántica profunda entre códigos fuente.

### Qué no cubre (Límites y Delegación)
- Detección de plagio léxico por huellas de Winnowing (delegado a `dredd`).
- Linter de estilo y formato de código (delegado a `gaff`).
- Ejecución de testcases (delegado a `nostromo`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio: Tree-Sitter y su gramática de C se instalan con el paquete.
- `giger` (opcional): `weyl detect-orphans` le pide el grafo de llamadas por `giger check --json` y, si no está instalado o no responde, usa su detector propio de funciones no invocadas.

### Integración en el Ecosistema
- CLI `weyl`. Plugin registrado en `ripley.plugins` (`semantic_diff`).

---

## Uso Rápido

```bash
# 1. Comparar entrega de estudiante contra solución modelo
weyl diff estudiante.c modelo.c

# 2. Salida estructurada JSON
weyl diff estudiante.c modelo.c --json

# 3. Comparar proyectos completos de múltiples archivos
weyl diff-project dir_alumno/ dir_modelo/

# 4. Auditoría de balance de memoria dinámica (malloc / free)
weyl audit-memory estudiante.c

# 5. Detección de similitud y copia profunda
weyl similarity entrega1.c entrega2.c   # similitud estructural; el plagio de una cohorte es de `dredd plagiarism`
weyl suggest entrega.c solucion.c --docente   # qué refactorizar, comparando con la solución (no muestra su código)
weyl cohort entregas/ --plantilla catedra/ --csv matriz.csv   # todas contra todas sobre el AST; un indicio para mirar a mano

# 6. Diagnóstico del entorno y dependencias
weyl doctor
```

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `weyl check`, `weyl diff` | Compara semánticamente ambos códigos función por función. |
| `weyl doctor` | Verifica el estado del entorno de diffing semántico WEYL. |
| `weyl track` | Analiza la evolución semántica y mejoras introducidas entre revisiones sucesivas de un estudiante. |
| `weyl report` | Genera directamente la sección de reporte Markdown de WEYL para Dredd. |
| `weyl check-api` | Verifica que las firmas de funciones respeten los contratos y parámetros de la consigna. |
| `weyl check-complexity` | Detecta transformaciones algorítmicas, reducciones de anidación o cambio recursión/iteración. |
| `weyl detect-orphans` | Detecta funciones auxiliares huérfanas o código muerto agregado en la entrega. |
| `weyl export-html` | Genera un reporte interactivo en formato HTML con diferencias semánticas. |
| `weyl ast-diff` | Visualiza en formato jerárquico Rich el árbol de funciones y bloques (no es un AST del compilador). |
| `weyl matrix` | Genera la matriz cruzada de similitud función por función bajo Alpha-Equivalence. |
| `weyl diff-project` | Realiza diffing semántico modular entre proyectos con múltiples archivos .c. |
| `weyl audit-memory` | Audita cambios en llamadas a malloc, calloc, realloc y free entre dos revisiones. |
| `weyl suggest` | Sugerencias de refactorización comparando con la solución modelo (solo en modo docente). |
| `weyl similarity` | Similitud estructural entre dos archivos, resistente a renombrar variables y reordenar. |
| `weyl cohort` | Matriz de similitud de un lote de entregas sobre el AST: todas contra todas. |

Ayuda de cada comando: `weyl <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `weyl check`, `weyl diff`, `weyl doctor`, `weyl track`, `weyl check-api`, `weyl check-complexity`, `weyl detect-orphans`, `weyl export-html`, `weyl ast-diff`, `weyl matrix`, `weyl diff-project`, `weyl audit-memory`, `weyl suggest`, `weyl similarity`, `weyl cohort`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-weyl-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `weyl`
:open:

```text
 Uso: weyl [OPCIONES] COMANDO [ARGUMENTOS]...

 ⚖️ WEYL — Herramienta de diffing semántico y comparación estructural (por bloques y funciones)
 entre códigos C.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de weyl y sale.                               │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ check             Compara semánticamente ambos códigos función por función.                      │
│ diff              Compara semánticamente ambos códigos función por función.                      │
│ doctor            Verifica el estado del entorno de diffing semántico WEYL.                      │
│ track             Analiza la evolución semántica y mejoras introducidas entre revisiones         │
│                   sucesivas de un estudiante.                                                    │
│ report            Genera directamente la sección de reporte Markdown de WEYL para Dredd.         │
│ check-api         Verifica que las firmas de funciones respeten los contratos y parámetros de la │
│                   consigna.                                                                      │
│ check-complexity  Detecta transformaciones algorítmicas, reducciones de anidación o cambio       │
│                   recursión/iteración.                                                           │
│ detect-orphans    Detecta funciones auxiliares huérfanas o código muerto agregado en la entrega. │
│ export-html       Genera un reporte interactivo en formato HTML con diferencias semánticas.      │
│ ast-diff          Visualiza en formato jerárquico Rich el árbol de funciones y bloques (no es un │
│                   AST del compilador).                                                           │
│ matrix            Genera la matriz cruzada de similitud función por función bajo                 │
│                   Alpha-Equivalence.                                                             │
│ diff-project      Realiza diffing semántico modular entre proyectos con múltiples archivos .c.   │
│ audit-memory      Audita cambios en llamadas a malloc, calloc, realloc y free entre dos          │
│                   revisiones.                                                                    │
│ suggest           Sugerencias de refactorización comparando con la solución modelo (solo en modo │
│                   docente).                                                                      │
│ similarity        Similitud estructural entre dos archivos, resistente a renombrar variables y   │
│                   reordenar.                                                                     │
│ cohort            Matriz de similitud de un lote de entregas sobre el AST: todas contra todas.   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl check`

```text
 Uso: weyl check [OPCIONES] {estudiante} {modelo}

 Compara semánticamente ambos códigos función por función.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --side-by-side    -s              Visualizar comparación lado a lado en dos columnas.            │
│ --alpha           -a              Activar normalización de identificadores (Alpha-Equivalence).  │
│ --json                            Salida en formato JSON.                                        │
│ --md,--output-md  -o      <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl diff`

```text
 Uso: weyl diff [OPCIONES] {estudiante} {modelo}

 Compara semánticamente ambos códigos función por función.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --side-by-side    -s              Visualizar comparación lado a lado en dos columnas.            │
│ --alpha           -a              Activar normalización de identificadores (Alpha-Equivalence).  │
│ --json                            Salida en formato JSON.                                        │
│ --md,--output-md  -o      <path>  Generar sección de reporte en formato Markdown para fusión en  │
│                                   Dredd.                                                         │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl doctor`

```text
 Uso: weyl doctor [OPCIONES]

 Verifica el estado del entorno de diffing semántico WEYL.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl track`

```text
 Uso: weyl track [OPCIONES] {dir_r1} {dir_r2}

 Analiza la evolución semántica y mejoras introducidas entre revisiones sucesivas de un estudiante.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    dir_r1      <path>  Directorio o archivo de la revisión inicial (r1). [obligatorio]         │
│ *    dir_r2      <path>  Directorio o archivo de la reentrega (r2). [obligatorio]                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl report`

```text
 Uso: weyl report [OPCIONES] {estudiante} {modelo}

 Genera directamente la sección de reporte Markdown de WEYL para Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl check-api`

```text
 Uso: weyl check-api [OPCIONES] {estudiante} {modelo}

 Verifica que las firmas de funciones respeten los contratos y parámetros de la consigna.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl check-complexity`

```text
 Uso: weyl check-complexity [OPCIONES] {estudiante} {modelo}

 Detecta transformaciones algorítmicas, reducciones de anidación o cambio recursión/iteración.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl detect-orphans`

```text
 Uso: weyl detect-orphans [OPCIONES] {estudiante}

 Detecta funciones auxiliares huérfanas o código muerto agregado en la entrega.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante a auditar. [obligatorio]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl export-html`

```text
 Uso: weyl export-html [OPCIONES] {estudiante} {modelo}

 Genera un reporte interactivo en formato HTML con diferencias semánticas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del reporte HTML interactivo.                          │
│                           [por defecto: weyl_report.html]                                        │
│ --json                    Emitir el resultado en JSON versionado (schema_version).               │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl ast-diff`

```text
 Uso: weyl ast-diff [OPCIONES] {estudiante} {modelo}

 Visualiza en formato jerárquico Rich el árbol de funciones y bloques (no es un AST del
 compilador).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl matrix`

```text
 Uso: weyl matrix [OPCIONES] {estudiante} {modelo}

 Genera la matriz cruzada de similitud función por función bajo Alpha-Equivalence.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C del estudiante. [obligatorio]                              │
│ *    modelo          <path>  Código C de la solución modelo. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el resultado en JSON versionado (schema_version).                       │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl diff-project`

```text
 Uso: weyl diff-project [OPCIONES] {dir_estudiante} {dir_modelo}

 Realiza diffing semántico modular entre proyectos con múltiples archivos .c.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    dir_estudiante      <path>  Directorio del proyecto del estudiante. [obligatorio]           │
│ *    dir_modelo          <path>  Directorio del proyecto modelo. [obligatorio]                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir resultado en JSON.                                                      │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl audit-memory`

```text
 Uso: weyl audit-memory [OPCIONES] {revision1} {revision2}

 Audita cambios en llamadas a malloc, calloc, realloc y free entre dos revisiones.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    revision1      <path>  Directorio o archivo de la revisión 1. [obligatorio]                 │
│ *    revision2      <path>  Directorio o archivo de la revisión 2. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir resultado en JSON.                                                      │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl suggest`

```text
 Uso: weyl suggest [OPCIONES] {estudiante} {modelo}

 Sugerencias de refactorización comparando con la solución modelo (solo en modo docente).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    estudiante      <path>  Código C de la entrega. [obligatorio]                               │
│ *    modelo          <path>  Solución modelo. [obligatorio]                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --docente            Confirmar que la salida es para el docente (se basa en la solución).        │
│ --json               Emitir el resultado en JSON versionado (schema_version).                    │
│ --help     -h        Muestra esta ayuda y sale.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl similarity`

```text
 Uso: weyl similarity [OPCIONES] {entrega1} {entrega2}

 Similitud estructural entre dos archivos, resistente a renombrar variables y reordenar.

 Compara dos archivos. El plagio en una cohorte completa (todos contra todos, con informe) es
 de `dredd plagiarism` (N-ECO-12).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    entrega1      <path>  Código C de la primera entrega. [obligatorio]                         │
│ *    entrega2      <path>  Código C de la segunda entrega. [obligatorio]                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --threshold  -t      <float>  Umbral de similitud porcentual para marcar los archivos como muy   │
│                               parecidos.                                                         │
│                               [por defecto: 90.0]                                                │
│ --json                        Emitir el resultado en JSON versionado (schema_version).           │
│ --help       -h               Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `weyl cohort`

```text
 Uso: weyl cohort [OPCIONES] {directorio}

 Matriz de similitud de un lote de entregas sobre el AST: todas contra todas.

 Renombrar y reordenar funciones no cambia el resultado, y lo que comparte la mayoría del lote no
 cuenta. Es un indicio para mirar a mano, no una prueba de copia. El informe de una cohorte
 evaluada es de `dredd cluster-errors --similitud`.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    directorio      <directory>  Carpeta con una subcarpeta (o un .c suelto) por entrega.       │
│                                   [obligatorio]                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --threshold  -t      <float range> [0.0<=x<=100.0]  Similitud (%) a partir de la cual dos        │
│                                                     entregas van al mismo grupo.                 │
│                                                     [por defecto: 90.0]                          │
│ --plantilla          <path>                         Código de la cátedra (archivo o carpeta) a   │
│                                                     descontar de cada entrega.                   │
│ --comunes            <float range> [0.0<=x<=1.0]    Descontar lo que está en al menos esta       │
│                                                     fracción de las entregas (desde 4 entregas;  │
│                                                     0 no descuenta).                             │
│                                                     [por defecto: 0.5]                           │
│ --csv                <path>                         Escribir la matriz completa en este CSV.     │
│ --json                                              Emitir el resultado en JSON versionado       │
│                                                     (schema_version).                            │
│ --help       -h                                     Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`weyl@a83f6b2`](https://github.com/INGCOM-UNRN-P1/weyl/tree/a83f6b2).
