---
title: "scorm-tools"
---

<!-- Generado por scripts/generar_paginas.py desde scorm-tools@87bb553: no editar a mano. -->

(manual-scorm_tools)=
# scorm-tools

Repositorio: [github.com/INGCOM-UNRN/scorm-tools](https://github.com/INGCOM-UNRN/scorm-tools).

Herramientas de línea de comandos, gestionadas con [`uv`](https://docs.astral.sh/uv/),
para crear, gestionar y validar contenido compatible con el estándar **SCORM**
(1.2 y 2004 3ra/4ta edición), listo para integrarse en plataformas LMS como
**Moodle**.

---

## Alcance

### Qué cubre
- Inicialización, validación formal y empaquetado de módulos de aprendizaje interactivo en formato SCORM para Moodle.
- Soporte completo para especificaciones SCORM 1.2 y SCORM 2004 4th Edition.
- Validación rigurosa de manifiestos `imsmanifest.xml` contra los esquemas XSD oficiales provistos localmente.
- Accesibilidad de las páginas HTML del paquete (`validate --a11y`, criterios de WCAG 2.1): idioma, `<title>`, texto alternativo, orden de encabezados, enlaces, campos sin etiqueta, iframes, subtítulos y contraste.
- Scaffolding declarativo de cursos a través de archivo de configuración `scorm.yaml`.
- Generación de paquetes comprimidos `.zip` listos para desplegar en plataformas LMS.

### Qué no cubre (Límites y Delegación)
- Autoría del contenido interactivo HTML, CSS o JavaScript del módulo.
- Calificación directa de entregas de código de software (delegado a `dredd`).
- Gestión de bancos de preguntas Moodle XML o GIFT (delegado a `voight`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Ninguno obligatorio.

### Integración en el Ecosistema
- CLI `scorm-tools`.

---

## Instalación

```bash
uv sync
```

Esto crea el entorno virtual `.venv` e instala el paquete en modo editable.
El comando queda disponible como `uv run scorm-tools ...`, o bien
`uv tool install .` para tenerlo en el `PATH` global.

## Comandos

### `init` — crear un curso de ejemplo

```bash
uv run scorm-tools init ./mi-curso --title "Introducción a Python" --scorm-version 2004-4ed
```

Genera:

- `scorm.yaml`: descriptor del curso (organizaciones, items, resources).
- `index.html`, `scorm-api.js`, `style.css`: SCO de ejemplo con el wrapper de
  comunicación SCORM (API 1.2 y 2004) ya integrado (`ScormAPI.init()`,
  `setCompleted()`, `setScore()`, `commit()`, `terminate()`).

`--scorm-version` acepta `1.2`, `2004-3ed` o `2004-4ed`.

### `build` — generar el `imsmanifest.xml` y empaquetar

```bash
uv run scorm-tools build ./mi-curso -o mi-curso.zip
```

Lee `scorm.yaml`, genera `imsmanifest.xml` (SCORM 1.2 o 2004 según
`version`) y empaqueta todo el contenido en un `.zip` importable directamente
en Moodle (actividad "Paquete SCORM"). Valida el resultado automáticamente
(usar `--no-validate` para omitirlo).

### `validate` — validar un paquete existente

```bash
uv run scorm-tools validate mi-curso.zip
# o sobre una carpeta ya descomprimida
uv run scorm-tools validate ./mi-curso-descomprimido
```

Verifica:

- **Esquema XSD** oficial de IMS Content Packaging + extensiones ADL
  (masteryscore, scormtype, sequencing, etc.) para SCORM 1.2 y 2004.
- **Integridad estructural**: identificadores únicos, `identifierref` de cada
  `item` apuntando a un `resource` existente, archivos referenciados (`href`)
  presentes en el paquete, rutas relativas (sin absolutas ni `\`).
- **Reglas específicas de Moodle**: `imsmanifest.xml` debe estar en la raíz
  del `.zip` (detecta y advierte sobre el error común de subir un `.zip` con
  una carpeta contenedora).

Con `--a11y` (`scorm-tools validate mi-curso.zip --a11y`) revisa además la accesibilidad de cada página HTML del paquete (WCAG 2.1, los mismos
criterios que `myst-tools check-a11y` aplica al fuente MyST). Los errores invalidan el paquete y los
avisos se informan; en `--json`, la lista `accesibilidad` trae cada hallazgo con archivo, línea, regla
y severidad.

| Regla | Severidad | Qué detecta |
| :--- | :--- | :--- |
| `idioma`, `titulo-pagina` | error | `<html>` sin `lang`; página sin `<title>`. |
| `alt-faltante`, `alt-generico` | error, aviso | `<img>` sin `alt` (o `alt=""` si es decorativa); un alt que no describe nada. |
| `encabezado-salto`, `titulo-repetido` | error, aviso | `<h2>` → `<h4>`; más de un `<h1>`. |
| `enlace-generico`, `enlace-sin-texto` | error | Enlaces «acá» o «click aquí»; enlaces sin texto ni `aria-label`. |
| `campo-sin-etiqueta` | error | `<input>`, `<select>` o `<textarea>` sin `<label>` ni `aria-label`. |
| `iframe-sin-titulo`, `video-sin-subtitulos` | error, aviso | `<iframe>` sin `title`; `<video>` sin `<track kind="captions">`. |
| `contraste` | error, o aviso sin fondo declarado | `style="color: …"` con contraste menor que 4.5:1. |

### `info` — inspeccionar la estructura de un curso

```bash
uv run scorm-tools info ./mi-curso
```

Muestra en tablas la jerarquía de items/resources definida en `scorm.yaml`
antes de compilar el paquete.

### `doctor` — diagnóstico del entorno

```bash
uv run scorm-tools doctor
```

Verifica dependencias, esquemas XSD vendorizados y utilidades del sistema.

### Comandos adicionales e integraciones

```bash
# Validar secuenciamiento SCORM 2004
uv run scorm-tools check-sequencing ./mi-curso

# Auditar tamaño de assets y empaquetado para Moodle
uv run scorm-tools check-size ./mi-curso

# Generar configuración recomendada para actividad SCORM en Moodle
uv run scorm-tools moodle-config ./mi-curso

# Nota: `from-gift` usa un parser GIFT propio (soporta MC, V/F, respuesta corta y
# numérica; avisa de lo que no puede representar) porque voight no puede
# importarse desde un `uv tool` aislado. tests/test_paridad_gift_moodle_toolbox.py
# verifica la paridad con el parser del dueño cuando ambos paquetes coexisten.
# Generar módulos SCORM desde guías deckard o cuestionarios GIFT/idkfa
uv run scorm-tools from-deckard guia.yaml -o ./scorm-guia
uv run scorm-tools from-gift preguntas.gift -o ./scorm-preguntas
uv run scorm-tools from-idkfa plantilla.c -o ./scorm-tracing

# Auditar código C embebido en recursos interactivos
uv run scorm-tools audit-c ./mi-curso

# Servidor de desarrollo interactivo con runtime SCORM simulado
uv run scorm-tools playground ./mi-curso --port 8080
```

## Formato de `scorm.yaml`

```yaml
identifier: COURSE-DEMO
title: "Mi curso"
version: "2004-4ed"        # 1.2 | 2004-3ed | 2004-4ed

organizations:
  - identifier: ORG-1
    title: "Mi curso"
    items:
      - identifier: ITEM-1
        title: "Módulo 1"
        resource: RES-1
        mastery_score: 80   # 0-100
        children: []         # items anidados opcionales

resources:
  - identifier: RES-1
    href: index.html
    type: sco               # sco | asset
    files: [index.html, scorm-api.js, style.css]
    dependencies: []
```

## Desarrollo

```bash
uv run pytest        # tests
uv run scorm-tools --help
```

Los esquemas XSD oficiales (IMS CP 1.1.2/1.1, ADL CP 1.2/1.3, ADL SEQ/NAV
1.3, IMS Simple Sequencing 1.0) están vendorizados en
`src/scorm_tools/schemas/` para que la validación funcione sin conexión a
internet.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `scorm-tools doctor` | Verificá el estado del entorno, dependencias y esquemas XSD de scorm-tools. |
| `scorm-tools init` | Creá un curso SCORM de ejemplo listo para editar. |
| `scorm-tools build` | Generá imsmanifest.xml y empaquetá el curso en un .zip para Moodle. |
| `scorm-tools validate` | Validá un paquete SCORM contra el esquema XSD y reglas de Moodle. |
| `scorm-tools info` | Mostrá un resumen de la estructura del curso definida en scorm.yaml. |
| `scorm-tools check-sequencing` | Verificá el grafo de secuenciamiento IMSSS y detectá ciclos o actividades huérfanas. |
| `scorm-tools check-size` | Audita el peso del paquete y su desglose por tipo de contenido para Moodle. |
| `scorm-tools moodle-config` | Generá la configuración recomendada de actividad Moodle (moodle_settings.json). |
| `scorm-tools check-a11y` | Auditá el cumplimiento de accesibilidad WCAG 2.1 AA en páginas HTML y paquetes SCORM. |
| `scorm-tools from-deckard` | Convertí una guía de ejercicios de Deckard a un curso SCORM interactivo. |
| `scorm-tools from-gift` | Convertí un banco de preguntas GIFT (Moodle) en un módulo SCORM interactivo autoevaluable. |
| `scorm-tools audit-c` | Auditá fragmentos de código C embebidos en el contenido SCORM contra reglas Ripley. |
| `scorm-tools dredd-sync` | Procesá registros de tracking de Moodle SCORM para integrarlos al calificador docente Dredd. |
| `scorm-tools diagram-memory` | Generá un diagrama Mermaid de memoria Stack y Heap (Bishop/Sebastian) para lecciones SCORM. |
| `scorm-tools from-idkfa` | Convertí una plantilla de tracing C de IDKFA a una lección interactiva SCORM autoevaluable. |
| `scorm-tools playground` | Generá un módulo SCORM interactivo con compilador C WebAssembly en el navegador. |

Ayuda de cada comando: `scorm-tools <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `scorm-tools doctor`, `scorm-tools init`, `scorm-tools build`, `scorm-tools validate`, `scorm-tools info`, `scorm-tools check-sequencing`, `scorm-tools check-size`, `scorm-tools moodle-config`, `scorm-tools check-a11y`, `scorm-tools from-deckard`, `scorm-tools from-gift`, `scorm-tools audit-c`, `scorm-tools dredd-sync`, `scorm-tools diagram-memory`, `scorm-tools from-idkfa`, `scorm-tools playground`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-scorm_tools-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `scorm-tools`
:open:

```text
 Uso: scorm-tools [OPCIONES] COMANDO [ARGUMENTOS]...

 Herramientas para crear, empaquetar y validar contenido SCORM compatible con Moodle.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v,-V        Muestra la versión de scorm-tools y sale.                     │
│ --install-completion               Instala el autocompletado para la terminal actual.            │
│ --show-completion                  Muestra el autocompletado para la terminal actual, para       │
│                                    copiarlo o adaptarlo.                                         │
│ --help                -h           Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ doctor            Verificá el estado del entorno, dependencias y esquemas XSD de scorm-tools.    │
│ init              Creá un curso SCORM de ejemplo listo para editar.                              │
│ build             Generá imsmanifest.xml y empaquetá el curso en un .zip para Moodle.            │
│ validate          Validá un paquete SCORM contra el esquema XSD y reglas de Moodle.              │
│ info              Mostrá un resumen de la estructura del curso definida en scorm.yaml.           │
│ check-sequencing  Verificá el grafo de secuenciamiento IMSSS y detectá ciclos o actividades      │
│                   huérfanas.                                                                     │
│ check-size        Audita el peso del paquete y su desglose por tipo de contenido para Moodle.    │
│ moodle-config     Generá la configuración recomendada de actividad Moodle                        │
│                   (moodle_settings.json).                                                        │
│ check-a11y        Auditá el cumplimiento de accesibilidad WCAG 2.1 AA en páginas HTML y paquetes │
│                   SCORM.                                                                         │
│ from-deckard      Convertí una guía de ejercicios de Deckard a un curso SCORM interactivo.       │
│ from-gift         Convertí un banco de preguntas GIFT (Moodle) en un módulo SCORM interactivo    │
│                   autoevaluable.                                                                 │
│ audit-c           Auditá fragmentos de código C embebidos en el contenido SCORM contra reglas    │
│                   Ripley.                                                                        │
│ dredd-sync        Procesá registros de tracking de Moodle SCORM para integrarlos al calificador  │
│                   docente Dredd.                                                                 │
│ diagram-memory    Generá un diagrama Mermaid de memoria Stack y Heap (Bishop/Sebastian) para     │
│                   lecciones SCORM.                                                               │
│ from-idkfa        Convertí una plantilla de tracing C de IDKFA a una lección interactiva SCORM   │
│                   autoevaluable.                                                                 │
│ playground        Generá un módulo SCORM interactivo con compilador C WebAssembly en el          │
│                   navegador.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools doctor`

```text
 Uso: scorm-tools doctor [OPCIONES]

 Verificá el estado del entorno, dependencias y esquemas XSD de scorm-tools.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emite el resultado en formato JSON versionado.                                 │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools init`

```text
 Uso: scorm-tools init [OPCIONES] {target}

 Creá un curso SCORM de ejemplo listo para editar.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Directorio destino del nuevo curso. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --title          -t      <str>                    Título del curso. [obligatorio]             │
│    --scorm-version          <1.2|2004-3ed|2004-4ed>  Versión de SCORM (1.2 o 2004).              │
│                                                      [por defecto: 2004-4ed]                     │
│    --id                     <str>                    Identificador único del curso (por defecto  │
│                                                      se deriva del título).                      │
│    --json                                            Emite el resultado en formato JSON          │
│                                                      versionado.                                 │
│    --help           -h                               Muestra esta ayuda y sale.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools build`

```text
 Uso: scorm-tools build [OPCIONES] {source}

 Generá imsmanifest.xml y empaquetá el curso en un .zip para Moodle.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      <path>  Directorio del curso (con scorm.yaml). [obligatorio]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output             -o                   <path>  Ruta del .zip resultante (por defecto          │
│                                                   <source>.zip).                                 │
│ --validate               --no-validate            Validar el paquete tras generarlo.             │
│                                                   [por defecto: validate]                        │
│ --minify                                          Minificar scripts JavaScript y estilos CSS     │
│                                                   antes de empaquetar.                           │
│ --sourcemap                                       Generar source maps .map para archivos         │
│                                                   minificados.                                   │
│ --inject-resizer                                  Inyectar helper iframe-resizer para vista      │
│                                                   enmarcada en Moodle.                           │
│ --completed-on-view                               Marcar automáticamente el SCO como completado  │
│                                                   al abrirse.                                    │
│ --a11y                                            Revisar también la accesibilidad de las        │
│                                                   páginas HTML (WCAG 2.1 AA).                    │
│ --json                                            Emite el resultado en formato JSON versionado. │
│ --help               -h                           Muestra esta ayuda y sale.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools validate`

```text
 Uso: scorm-tools validate [OPCIONES] {path}

 Validá un paquete SCORM contra el esquema XSD y reglas de Moodle.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      <path>  Paquete SCORM: directorio o archivo .zip. [obligatorio]                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json                      Emite el informe en formato JSON estructurado.                       │
│ --md,--output-md            Emite el informe en formato Markdown.                                │
│ --a11y                      Revisa también la accesibilidad de las páginas HTML (WCAG 2.1).      │
│ --help            -h        Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools info`

```text
 Uso: scorm-tools info [OPCIONES] {source}

 Mostrá un resumen de la estructura del curso definida en scorm.yaml.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      <path>  Directorio del curso (con scorm.yaml). [obligatorio]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emite la estructura del curso en formato JSON estructurado.                    │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools check-sequencing`

```text
 Uso: scorm-tools check-sequencing [OPCIONES] {source}

 Verificá el grafo de secuenciamiento IMSSS y detectá ciclos o actividades huérfanas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      <path>  Directorio del curso (con scorm.yaml). [obligatorio]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emite el análisis del grafo en formato JSON estructurado.                      │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools check-size`

```text
 Uso: scorm-tools check-size [OPCIONES] {path}

 Audita el peso del paquete y su desglose por tipo de contenido para Moodle.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      <path>  Paquete SCORM: archivo .zip o directorio. [obligatorio]                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --max-mb          <float>  Límite máximo permitido en MB (defecto: 50MB). [por defecto: 50.0]    │
│ --json                     Emite el informe de tamaño en formato JSON estructurado.              │
│ --help    -h               Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools moodle-config`

```text
 Uso: scorm-tools moodle-config [OPCIONES] {source}

 Generá la configuración recomendada de actividad Moodle (moodle_settings.json).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      <path>  Directorio del curso (con scorm.yaml). [obligatorio]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output        -o      <path>  Ruta donde guardar moodle_settings.json (opcional).              │
│ --grade-method          <int>   Método de calificación: 1=Más alta, 2=Promedio, 3=Primer         │
│                                 intento, 4=Último.                                               │
│                                 [por defecto: 1]                                                 │
│ --max-attempts          <int>   Número máximo de intentos permitidos. [por defecto: 3]           │
│ --popup                 <int>   Visualización: 0=Enmarcado en página, 1=Nueva ventana.           │
│                                 [por defecto: 0]                                                 │
│ --json                          Emite la configuración exclusivamente en JSON.                   │
│ --help          -h              Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools check-a11y`

```text
 Uso: scorm-tools check-a11y [OPCIONES] {path}

 Auditá el cumplimiento de accesibilidad WCAG 2.1 AA en páginas HTML y paquetes SCORM.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      <path>  Paquete SCORM (.zip, directorio) o archivo HTML. [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --strict            Tratar los avisos de accesibilidad como errores.                             │
│ --json              Emitir el informe de accesibilidad en formato JSON.                          │
│ --help    -h        Muestra esta ayuda y sale.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools from-deckard`

```text
 Uso: scorm-tools from-deckard [OPCIONES] {guia} {target}

 Convertí una guía de ejercicios de Deckard a un curso SCORM interactivo.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia        <path>  Archivo guia.yaml de ejercicios de Deckard. [obligatorio]               │
│ *    target      <path>  Directorio destino del paquete SCORM. [obligatorio]                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --scorm-version          <1.2|2004-3ed|2004-4ed>  Versión SCORM (1.2 o 2004).                    │
│                                                   [por defecto: 2004-4ed]                        │
│ --build          -b                               Compilar automáticamente a archivo .zip tras   │
│                                                   generar los fuentes.                           │
│ --json                                            Emite el resultado en formato JSON versionado. │
│ --help           -h                               Muestra esta ayuda y sale.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools from-gift`

```text
 Uso: scorm-tools from-gift [OPCIONES] {gift_file} {target}

 Convertí un banco de preguntas GIFT (Moodle) en un módulo SCORM interactivo autoevaluable.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    gift_file      <path>  Archivo de preguntas en formato GIFT. [obligatorio]                  │
│ *    target         <path>  Directorio destino del paquete SCORM. [obligatorio]                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --title  -t      <str>  Título del cuestionario. [por defecto: Cuestionario SCORM]               │
│ --build  -b             Compilar automáticamente a archivo .zip tras generar los fuentes.        │
│ --json                  Emite el resultado en formato JSON versionado.                           │
│ --help   -h             Muestra esta ayuda y sale.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools audit-c`

```text
 Uso: scorm-tools audit-c [OPCIONES] {source}

 Auditá fragmentos de código C embebidos en el contenido SCORM contra reglas Ripley.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      <path>  Directorio del curso SCORM a auditar. [obligatorio]                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emite los hallazgos en formato JSON estructurado.                              │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools dredd-sync`

```text
 Uso: scorm-tools dredd-sync [OPCIONES] {tracking_file}

 Procesá registros de tracking de Moodle SCORM para integrarlos al calificador docente Dredd.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    tracking_file      <path>  Archivo JSON con registros de tracking SCORM exportados.         │
│                                 [obligatorio]                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Archivo donde guardar el reporte para Dredd.                           │
│ --json                    Emite el resultado en formato JSON versionado.                         │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools diagram-memory`

```text
 Uso: scorm-tools diagram-memory [OPCIONES] {trace_file}

 Generá un diagrama Mermaid de memoria Stack y Heap (Bishop/Sebastian) para lecciones SCORM.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    trace_file      <path>  Archivo JSON con la traza de memoria (frames y heap). [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Archivo de salida para el diagrama Mermaid.                            │
│ --json                    Emite el resultado en formato JSON versionado.                         │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools from-idkfa`

```text
 Uso: scorm-tools from-idkfa [OPCIONES] {template} {target}

 Convertí una plantilla de tracing C de IDKFA a una lección interactiva SCORM autoevaluable.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    template      <path>  Plantilla C de ejercicio de tracing de IDKFA. [obligatorio]           │
│ *    target        <path>  Directorio destino del paquete SCORM. [obligatorio]                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --build  -b        Compilar automáticamente a archivo .zip.                                      │
│ --json             Emite el resultado en formato JSON versionado.                                │
│ --help   -h        Muestra esta ayuda y sale.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `scorm-tools playground`

```text
 Uso: scorm-tools playground [OPCIONES] {target}

 Generá un módulo SCORM interactivo con compilador C WebAssembly en el navegador.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Directorio destino del módulo Playground Wasm. [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --title  -t      <str>  Título del módulo. [por defecto: Playground C WebAssembly]               │
│ --build  -b             Compilar automáticamente a archivo .zip.                                 │
│ --json                  Emite el resultado en formato JSON versionado.                           │
│ --force  -f             Sobrescribir el directorio si ya tiene archivos.                         │
│ --help   -h             Muestra esta ayuda y sale.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`scorm-tools@87bb553`](https://github.com/INGCOM-UNRN/scorm-tools/tree/87bb553).
