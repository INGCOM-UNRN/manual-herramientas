---
title: "myst-tools"
---

<!-- Generado por scripts/generar_paginas.py desde myst-tools@5462d70: no editar a mano. -->

(manual-myst_tools)=
# myst-tools

Repositorio: [github.com/martinvilu/mystmd-tools](https://github.com/martinvilu/mystmd-tools).

Herramientas unificadas para automatizar y gestionar el material didáctico escrito en formato MyST Markdown para la cátedra de Programación II.

Este proyecto está gestionado con [uv](https://github.com/astral-sh/uv).

:::{important}
**Requisito de ejecución:** Las herramientas del CLI deben ser ejecutadas desde un directorio que contenga el archivo de configuración `myst.yml` (es decir, la raíz del proyecto de documentación MyST). Si el archivo no está presente, puede ignorarse la restricción usando la opción global `-f/--force`.
:::

---

## Alcance

### Qué cubre
- Herramientas de soporte, auditoría y mantenimiento para apuntes y material didáctico en formato MyST Markdown.
- Verificación ortográfica y gramatical contextualizada mediante LanguageTool, con diccionario técnico de programación.
- Detección y resolución de colisiones en anclas y etiquetas cruzadas.
- Generación automatizada de índices temáticos y verificación de consistencia de enlaces.
- Accesibilidad del material (`check-a11y`): texto alternativo de imágenes y figuras, orden de los encabezados, enlaces genéricos («acá»), contraste de colores en línea, iframes sin título y tablas sin encabezado (criterios de WCAG 2.1 que se ven en el fuente).

### Qué no cubre (Límites y Delegación)
- Formateo de código fuente en C (delegado a `gaff`).
- Ejecución de suites de prueba de ejercicios (delegado a `nostromo`).
- Generación de exámenes institucionales Typst/OMR (delegado a `alucard`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Java Runtime Environment (JRE) opcional (para ejecución de servidor local LanguageTool).

### Integración en el Ecosistema
- CLI `myst-tools`.

---

## Instalación

Podés instalar estas herramientas como una herramienta global en tu sistema usando `uv tool`:

```bash
# Desde el directorio raíz del proyecto
uv tool install .
```

Una vez instalada, vas a tener disponible el comando `myst-tools` globalmente en tu terminal.

Si preferís ejecutarlo sin instalarlo globalmente:

```bash
uv run myst-tools [comando] [argumentos]
```

## Uso General

```bash
myst-tools [OPCIONES_GLOBALES] [COMANDO] [ARGUMENTOS]
```

### Opciones Globales:
* **`-f, --force`**: Fuerza la ejecución del comando seleccionado ignorando la verificación de la existencia de `myst.yml` en el directorio actual.

## Comandos Disponibles

El comando unificado `myst-tools` provee los siguientes subcomandos:

### 1. `add-anchors`
Agrega etiquetas/anclas de MyST (`(slug)=`) de manera automática antes de cada encabezado (`#`, `##`, `###`) en los archivos Markdown del apunte. Esto facilita las referencias cruzadas estables.

```bash
myst-tools add-anchors [APUNTE_DIR]
```
* **`APUNTE_DIR`** (opcional): Directorio que contiene los archivos Markdown del apunte. Por defecto es `./apunte`.

### 2. `gen-apunte`
Genera un índice detallado (`indice.md`) agrupado por archivo y con enlaces internos a encabezados de nivel 1, 2 y 3.

```bash
myst-tools gen-apunte [APUNTE_DIR]
```
* **`APUNTE_DIR`** (opcional): Directorio del apunte. Por defecto es `./apunte`.

### 3. `gen-guides`
Genera el índice de guías de trabajos prácticos (`indice.md`) leyendo el título del frontmatter o el primer encabezado `#` de cada guía.

```bash
myst-tools gen-guides [GUIAS_DIR]
```
* **`GUIAS_DIR`** (opcional): Directorio que contiene las guías. Por defecto es `./guias`.

### 4. `gen-rules`
Genera el índice de reglas de estilo de programación (`indice.md`) recopilando todas las referencias de tipo `(regla-xxx)=` y sus respectivos títulos.

```bash
myst-tools gen-rules [REGLAS_DIR]
```
* **`REGLAS_DIR`** (opcional): Directorio que contiene las reglas de estilo. Por defecto es `./reglas`.

### 5. `fix-anchors`
Detecta y corrige anclas MyST duplicadas en los archivos Markdown del proyecto. Renombra las definiciones duplicadas anteponiendo el nombre del archivo y actualiza todas las referencias correspondientes.

```bash
myst-tools fix-anchors [DIR] [OPCIONES]
```
* **`DIR`** (opcional): Directorio raíz a escanear. Por defecto es el directorio actual `.`.
* **Opciones**:
  * `--dry-run`: Muestra los cambios planificados sin modificar ningún archivo.
  * `--report`: Solo lista las anclas duplicadas detectadas y finaliza.

### 6. `fmt`
Formatea archivos MyST Markdown aplicando un límite de 80 caracteres de ancho de línea para la prosa (sin modificar bloques de código) y normalizando el anidamiento y cierre de directivas (guardas).

```bash
myst-tools fmt [ARCHIVOS/DIR...] [OPCIONES]
```
* **`ARCHIVOS/DIR`** (opcional): Archivos o directorios a formatear (acepta múltiples). Si no se especifica y la entrada es interactiva, formatea todos los archivos `.md` del proyecto de forma recursiva. Si la entrada no es interactiva, lee desde la entrada estándar (stdin). Usar `-` para forzar la lectura desde stdin.
* **Opciones**:
  * `--check`: Verifica si los archivos necesitan formato (retorna código 1 si requieren cambios).
  * `--stdout`: Imprime el resultado en la salida estándar en vez de modificar los archivos in-place.
  * `--width N`: Especifica un ancho de línea personalizado (por defecto 80).

### 7. `spellcheck` (alias: `grammar`, `languagetool`)
Audita y corrige ortografía y gramática en documentos MyST Markdown usando LanguageTool, enmascarando inteligentemente directivas MyST, bloques de código C, matemáticas LaTeX y anclas para evitar falsos positivos.

```bash
myst-tools spellcheck [ARCHIVOS/DIR...] [OPCIONES]
```
* **`ARCHIVOS/DIR`** (opcional): Archivos o directorios a analizar.
* **Opciones**:
  * `-f, --fix`: Aplica automáticamente las correcciones sugeridas in-place sobre los archivos.
  * `-l, --lang`: Código de idioma (por defecto `es-AR`; soporta `es`, `en-US`, etc.).
  * `-s, --server`: URL de servidor LanguageTool personalizado (por defecto intenta servidor local `http://localhost:8081` y API pública).
  * `--ignore-words`: Lista de palabras adicionales a ignorar separadas por coma.
  * `--ignore-rules`: Reglas específicas a deshabilitar separadas por coma.
  * `--json`: Salida estructurada JSON.
  * `-o, --md`: Genera reporte en formato Markdown para fusión en Dredd o documentación.

### 8. `report`
Genera un informe integral del estado del proyecto MyST Markdown (anclas huérfanas, tablas, enlaces y directivas).

```bash
myst-tools report [DIRECTORIO] [--md]
```

### 9. `check-tables` y `fmt-tables`
Audita y formatea tablas Markdown para asegurar alineación visual homogénea y sintaxis válida.

```bash
myst-tools check-tables [ARCHIVOS/DIR...]
myst-tools fmt-tables [ARCHIVOS/DIR...]
```

### 10. `check-style`
Verifica directivas MyST, bloques de admonición y normas de estilo pedagógico.

```bash
myst-tools check-style [ARCHIVOS/DIR...]
```

### 10b. `check-a11y`
Audita la accesibilidad del material: texto alternativo, orden de encabezados, enlaces genéricos,
contraste, iframes y tablas (ver el [manual](https://github.com/martinvilu/mystmd-tools/blob/main/MANUAL.md) para las reglas).

```bash
myst-tools check-a11y [ARCHIVOS/DIR...] [--strict] [--json]
```

### 11. `extract-c-tests`
Extrae bloques de código C incluidos en el material didáctico para verificación de compilación.

```bash
myst-tools extract-c-tests [ARCHIVOS/DIR...] -o ./pruebas_c
```

### 12. `extract-dict-terms`
Extrae términos técnicos del apunte para alimentar diccionarios ortográficos especializados.

```bash
myst-tools extract-dict-terms [ARCHIVOS/DIR...]
```

### 13. `check-links`
Audita los enlaces a GitHub (que apunten a un commit o tag, no a una rama que cambia). Con
`--externos` además consulta cada enlace http(s) (una vez por URL, en paralelo) y marca los que
responden 404, 500 o no responden.

```bash
myst-tools check-links [ARCHIVOS/DIR...] [--externos]
```

### 14. `check-code-lang`
Marca los bloques de código abiertos con ``` sin lenguaje (```c, ```bash, ```text): quedan sin
resaltado y el lector de pantalla no sabe anunciarlos. Los bloques de directiva (```{note}) no
cuentan.

```bash
myst-tools check-code-lang [ARCHIVOS/DIR...]
```

## Desarrollo

Si querés modificar las herramientas o agregar nuevas funcionalidades, podés ejecutar el CLI en modo desarrollo:

```bash
uv run myst-tools --help
```

El backend de construcción utilizado es `hatchling`.

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

### Opciones de `myst-tools`

| Opción | Descripción |
|:--|:--|
| `--force`, `-f` | Fuerza la ejecución saliéndose de la verificación de la existencia de 'myst.yml'. |

### Comandos

| Comando | Descripción |
|:--|:--|
| `myst-tools add-anchors` | Agrega etiquetas/anclas de MyST a los encabezados de archivos Markdown. |
| `myst-tools gen-apunte` | Genera el índice detallado para el apunte de cátedra. |
| `myst-tools gen-guides` | Genera el índice para las guías de trabajos prácticos. |
| `myst-tools gen-rules` | Genera el índice de las reglas de estilo de programación. |
| `myst-tools fix-anchors` | Detecta y corrige anclas MyST duplicadas. |
| `myst-tools fmt` | Formatea archivos MyST Markdown (longitud de línea, fences y comentarios). |
| `myst-tools spellcheck` | Verifica y corrige ortografía y gramática en documentos MyST Markdown usando LanguageTool. |
| `myst-tools report` | Genera directamente la sección de reporte Markdown de LanguageTool para Dredd o documentación. |
| `myst-tools check-tables` | Audita tablas Markdown en busca de columnas desalineadas o separadores inválidos. |
| `myst-tools fmt-tables` | Formatea y alinea visualmente las columnas de tablas Markdown. |
| `myst-tools check-style` | Audita estilo rioplatense (voseo vs tuteo, spanglish). |
| `myst-tools check-a11y` | Audita accesibilidad: texto alternativo, orden de encabezados, enlaces genéricos y contraste. |
| `myst-tools check-catalog-links` | Valida que toda referencia, enlace o ancla a reglas 0xXXXXh y satélites coincida con el catálogo oficial. |
| `myst-tools extract-c-tests` | Extrae bloques C hacia un proyecto C compilable con Makefile. |
| `myst-tools extract-dict-terms` | Extrae identificadores técnicos C y directivas para el diccionario personalizado de LanguageTool. |
| `myst-tools check-links` | Audita inmutabilidad y sintaxis de enlaces a GitHub (y, con --externos, enlaces caídos). |
| `myst-tools check-code-lang` | Bloques de código sin lenguaje (``` en lugar de ```c): sin resaltado ni anuncio accesible. |
| `myst-tools doctor` | Verifica el estado del entorno de MYST-TOOLS (Python, Node/myst, LanguageTool, Typst). |
| `myst-tools check-c-snippets` | Verifica con `gcc -fsyntax-only` que los bloques C compilen, también como fragmentos (requiere gcc). |
| `myst-tools to-typst` | Convierte encabezados de un MyST Markdown a una plantilla Typst. |
| `myst-tools extract-exercises` | Extrae las directivas {exercise} como candidatos a ejercicios del banco (deckard). |
| `myst-tools glossary` | Detecta definiciones tipo **Término**: definición y arma un glosario. |
| `myst-tools callout` | Imprime un callout MyST (admonition) con el formato estándar. |

Ayuda de cada comando: `myst-tools <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `myst-tools spellcheck`, `myst-tools check-tables`, `myst-tools check-style`, `myst-tools check-a11y`, `myst-tools check-catalog-links`, `myst-tools check-links`, `myst-tools check-code-lang`, `myst-tools doctor`, `myst-tools check-c-snippets`, `myst-tools to-typst`, `myst-tools extract-exercises`, `myst-tools glossary`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-myst_tools-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `myst-tools`
:open:

```text
 Uso: myst-tools [OPCIONES] COMANDO [ARGUMENTOS]...

 Herramientas unificadas para automatizar, formatear e indexar material didáctico MyST Markdown.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de myst-tools y sale.                         │
│ --force               -f        Fuerza la ejecución saliéndose de la verificación de la          │
│                                 existencia de 'myst.yml'.                                        │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ add-anchors          Agrega etiquetas/anclas de MyST a los encabezados de archivos Markdown.     │
│ gen-apunte           Genera el índice detallado para el apunte de cátedra.                       │
│ gen-guides           Genera el índice para las guías de trabajos prácticos.                      │
│ gen-rules            Genera el índice de las reglas de estilo de programación.                   │
│ fix-anchors          Detecta y corrige anclas MyST duplicadas.                                   │
│ fmt                  Formatea archivos MyST Markdown (longitud de línea, fences y comentarios).  │
│ spellcheck           Verifica y corrige ortografía y gramática en documentos MyST Markdown       │
│                      usando LanguageTool.                                                        │
│ report               Genera directamente la sección de reporte Markdown de LanguageTool para     │
│                      Dredd o documentación.                                                      │
│ check-tables         Audita tablas Markdown en busca de columnas desalineadas o separadores      │
│                      inválidos.                                                                  │
│ fmt-tables           Formatea y alinea visualmente las columnas de tablas Markdown.              │
│ check-style          Audita estilo rioplatense (voseo vs tuteo, spanglish).                      │
│ check-a11y           Audita accesibilidad: texto alternativo, orden de encabezados, enlaces      │
│                      genéricos y contraste.                                                      │
│ check-catalog-links  Valida que toda referencia, enlace o ancla a reglas 0xXXXXh y satélites     │
│                      coincida con el catálogo oficial.                                           │
│ extract-c-tests      Extrae bloques C hacia un proyecto C compilable con Makefile.               │
│ extract-dict-terms   Extrae identificadores técnicos C y directivas para el diccionario          │
│                      personalizado de LanguageTool.                                              │
│ check-links          Audita inmutabilidad y sintaxis de enlaces a GitHub (y, con --externos,     │
│                      enlaces caídos).                                                            │
│ check-code-lang      Bloques de código sin lenguaje (``` en lugar de ```c): sin resaltado ni     │
│                      anuncio accesible.                                                          │
│ doctor               Verifica el estado del entorno de MYST-TOOLS (Python, Node/myst,            │
│                      LanguageTool, Typst).                                                       │
│ check-c-snippets     Verifica con `gcc -fsyntax-only` que los bloques C compilen, también como   │
│                      fragmentos (requiere gcc).                                                  │
│ to-typst             Convierte encabezados de un MyST Markdown a una plantilla Typst.            │
│ extract-exercises    Extrae las directivas {exercise} como candidatos a ejercicios del banco     │
│                      (deckard).                                                                  │
│ glossary             Detecta definiciones tipo **Término**: definición y arma un glosario.       │
│ callout              Imprime un callout MyST (admonition) con el formato estándar.               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools add-anchors`

```text
 Uso: myst-tools add-anchors [OPCIONES] [dir_path]

 Agrega etiquetas/anclas de MyST a los encabezados de archivos Markdown.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   dir_path      <path>  Directorio que contiene los archivos Markdown del apunte.                │
│                         [por defecto: apunte]                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando la verificación de 'myst.yml'.                  │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools gen-apunte`

```text
 Uso: myst-tools gen-apunte [OPCIONES] [dir_path]

 Genera el índice detallado para el apunte de cátedra.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   dir_path      <path>  Directorio del apunte (apunte). [por defecto: apunte]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando la verificación de 'myst.yml'.                  │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools gen-guides`

```text
 Uso: myst-tools gen-guides [OPCIONES] [dir_path]

 Genera el índice para las guías de trabajos prácticos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   dir_path      <path>  Directorio que contiene las guías. [por defecto: guias]                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando la verificación de 'myst.yml'.                  │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools gen-rules`

```text
 Uso: myst-tools gen-rules [OPCIONES] [dir_path]

 Genera el índice de las reglas de estilo de programación.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   dir_path      <path>  Directorio que contiene las reglas de estilo. [por defecto: reglas]      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando la verificación de 'myst.yml'.                  │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools fix-anchors`

```text
 Uso: myst-tools fix-anchors [OPCIONES] [dir_path]

 Detecta y corrige anclas MyST duplicadas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   dir_path      <path>  Directorio raíz a escanear. [por defecto: .]                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --dry-run            Muestra los cambios sin escribir ningún archivo.                            │
│ --report             Solo lista los duplicados y termina sin modificar nada.                     │
│ --force    -f        Fuerza la ejecución ignorando la verificación de 'myst.yml'.                │
│ --help     -h        Muestra esta ayuda y sale.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools fmt`

```text
 Uso: myst-tools fmt [OPCIONES] [files]...

 Formatea archivos MyST Markdown (longitud de línea, fences y comentarios).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <str>  Archivos o directorios a formatear (por defecto, todos los archivos .md si   │
│                     la entrada es interactiva).                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --check                  Solo verifica si los archivos necesitan formato.                        │
│ --stdout                 Imprime el resultado a la salida estándar en vez de modificar in-place. │
│ --width   -w      <int>  Ancho máximo de línea (default: 80). [por defecto: 80]                  │
│ --force   -f             Fuerza la ejecución ignorando la verificación de 'myst.yml'.            │
│ --help    -h             Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools spellcheck`

```text
 Uso: myst-tools spellcheck [OPCIONES] [paths]...

 Verifica y corrige ortografía y gramática en documentos MyST Markdown usando LanguageTool.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>  Archivos .md o directorios a revisar con LanguageTool (por defecto todo el  │
│                      apunte/guías).                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --fix             -f              Aplica automáticamente las sugerencias de corrección           │
│                                   ortográfica y gramatical.                                      │
│ --lang            -l      <str>   Código de idioma para LanguageTool (ej: 'es-AR', 'es',         │
│                                   'en-US').                                                      │
│                                   [por defecto: es-AR]                                           │
│ --server          -s      <str>   URL del servidor LanguageTool (por defecto                     │
│                                   http://localhost:8081 y API pública).                          │
│ --username        -u      <str>   Usuario / correo de LanguageTool Premium.                      │
│ --api-key         -k      <str>   API Key / Token de LanguageTool Premium.                       │
│ --premium                         Fuerza el uso de la API LanguageTool Premium                   │
│                                   (https://api.languagetoolplus.com/v2/check).                   │
│ --ignore-rules            <str>   Reglas a ignorar separadas por comas (ej:                      │
│                                   'MORFOLOGIK_RULE_ES,UPPERCASE_SENTENCE_START').                │
│ --ignore-words            <str>   Palabras personalizadas a ignorar separadas por comas.         │
│ --json                            Emite salida estructurada en formato JSON.                     │
│ --md,--output-md  -o      <path>  Genera reporte en formato Markdown para fusión en Dredd o      │
│                                   documentación.                                                 │
│ --force                           Fuerza la ejecución ignorando la verificación de 'myst.yml'.   │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools report`

```text
 Uso: myst-tools report [OPCIONES] [paths]...

 Genera directamente la sección de reporte Markdown de LanguageTool para Dredd o documentación.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>  Archivos .md o directorios a auditar.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo Markdown.                                  │
│ --lang    -l      <str>   Código de idioma para LanguageTool. [por defecto: es-AR]               │
│ --server  -s      <str>   URL del servidor LanguageTool.                                         │
│ --force                   Fuerza la ejecución ignorando 'myst.yml'.                              │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-tables`

```text
 Uso: myst-tools check-tables [OPCIONES] [files]...

 Audita tablas Markdown en busca de columnas desalineadas o separadores inválidos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a auditar.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite los hallazgos como JSON versionado.                                     │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools fmt-tables`

```text
 Uso: myst-tools fmt-tables [OPCIONES] [files]...

 Formatea y alinea visualmente las columnas de tablas Markdown.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a formatear.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-style`

```text
 Uso: myst-tools check-style [OPCIONES] [files]...

 Audita estilo rioplatense (voseo vs tuteo, spanglish).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a auditar en estilo rioplatense.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite los hallazgos como JSON versionado.                                     │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-a11y`

```text
 Uso: myst-tools check-a11y [OPCIONES] [files]...

 Audita accesibilidad: texto alternativo, orden de encabezados, enlaces genéricos y contraste.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos o directorios Markdown a auditar.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force   -f        Fuerza la ejecución ignorando myst.yml.                                      │
│ --strict            Sale con 1 también por los avisos, no solo por los errores.                  │
│ --json              Emite los hallazgos como JSON versionado.                                    │
│ --help    -h        Muestra esta ayuda y sale.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-catalog-links`

```text
 Uso: myst-tools check-catalog-links [OPCIONES] [files]...

 Valida que toda referencia, enlace o ancla a reglas 0xXXXXh y satélites coincida con el catálogo
 oficial.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos o directorios Markdown a auditar.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite los hallazgos como JSON versionado.                                     │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools extract-c-tests`

```text
 Uso: myst-tools extract-c-tests [OPCIONES] {file_path}

 Extrae bloques C hacia un proyecto C compilable con Makefile.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      <path>  Archivo Markdown del cual extraer ejemplos C. [obligatorio]          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir  -o      <path>  Directorio destino del proyecto C. [por defecto: test_c_project]   │
│ --force       -f              Fuerza la ejecución ignorando myst.yml.                            │
│ --help        -h              Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools extract-dict-terms`

```text
 Uso: myst-tools extract-dict-terms [OPCIONES] [files]...

 Extrae identificadores técnicos C y directivas para el diccionario personalizado de LanguageTool.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a procesar.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Archivo destino para términos LanguageTool.                            │
│                           [por defecto: spelling.txt]                                            │
│ --force   -f              Fuerza la ejecución ignorando myst.yml.                                │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-links`

```text
 Uso: myst-tools check-links [OPCIONES] [files]...

 Audita inmutabilidad y sintaxis de enlaces a GitHub (y, con --externos, enlaces caídos).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a auditar.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force     -f        Fuerza la ejecución ignorando myst.yml.                                    │
│ --json                Emite los hallazgos como JSON versionado.                                  │
│ --externos            Además, consultar cada enlace externo y marcar los que responden 404/500 o │
│                       no responden.                                                              │
│ --help      -h        Muestra esta ayuda y sale.                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-code-lang`

```text
 Uso: myst-tools check-code-lang [OPCIONES] [files]...

 Bloques de código sin lenguaje (``` en lugar de ```c): sin resaltado ni anuncio accesible.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a auditar.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite los hallazgos como JSON versionado.                                     │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools doctor`

```text
 Uso: myst-tools doctor [OPCIONES]

 Verifica el estado del entorno de MYST-TOOLS (Python, Node/myst, LanguageTool, Typst).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools check-c-snippets`

```text
 Uso: myst-tools check-c-snippets [OPCIONES] [files]...

 Verifica con `gcc -fsyntax-only` que los bloques C compilen, también como fragmentos (requiere
 gcc).

 Revisa los bloques ```c y ```{code-block} c. Cada uno se compila con los headers estándar y, si
 no compila así, dentro de una función; los nombres que el texto declara en otro bloque no cuentan
 como error. Un bloque `{code-block} c` con `:class: fragmento` no se compila.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a auditar.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite el resultado como JSON versionado.                                      │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools to-typst`

```text
 Uso: myst-tools to-typst [OPCIONES] {file_path}

 Convierte encabezados de un MyST Markdown a una plantilla Typst.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      <path>  Archivo Markdown MyST a convertir. [obligatorio]                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --titulo  -t      <str>   Título del documento Typst. [por defecto: Apunte de Cátedra]           │
│ --output  -o      <path>  Archivo .typ de salida (por defecto stdout).                           │
│ --force   -f              Fuerza la ejecución ignorando myst.yml.                                │
│ --json                    Emite el resultado como JSON versionado.                               │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools extract-exercises`

```text
 Uso: myst-tools extract-exercises [OPCIONES] [files]...

 Extrae las directivas {exercise} como candidatos a ejercicios del banco (deckard).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown con directivas ```{exercise}.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite el resultado como JSON versionado.                                      │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools glossary`

```text
 Uso: myst-tools glossary [OPCIONES] [files]...

 Detecta definiciones tipo **Término**: definición y arma un glosario.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   files      <path>  Archivos Markdown a procesar.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force  -f        Fuerza la ejecución ignorando myst.yml.                                       │
│ --json             Emite el resultado como JSON versionado.                                      │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `myst-tools callout`

```text
 Uso: myst-tools callout [OPCIONES] {tipo} {cuerpo}

 Imprime un callout MyST (admonition) con el formato estándar.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    tipo        <str>  `note`, `tip`, `warning`, `important` o `danger` (otro valor cae en      │
│                         `note`).                                                                 │
│                         [obligatorio]                                                            │
│ *    cuerpo      <str>  Texto del callout. [obligatorio]                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --titulo  -t      <str>  Título del callout.                                                     │
│ --help    -h             Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`myst-tools@5462d70`](https://github.com/martinvilu/mystmd-tools/tree/5462d70).
