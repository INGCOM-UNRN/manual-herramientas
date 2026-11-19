---
title: "deckard"
subtitle: "Gestor de Bancos de Ejercicios, Guías y Graduación"
---

<!-- Generado por scripts/generar_paginas.py desde deckard@12430e1: no editar a mano. -->

(manual-deckard)=
# deckard — Gestor de Bancos de Ejercicios, Guías y Graduación

Repositorio: [github.com/INGCOM-UNRN/deckard](https://github.com/INGCOM-UNRN/deckard).

> *"Se ha reportado que algunos replicantes escapan..."* — Rick Deckard administra
> las pruebas: qué ejercicio va a cada guía, con qué dificultad taxonómica y cuánto tiempo insume.

`deckard` es la herramienta docente del ecosistema P1 para la **autoría atómica, curaduría pedagógica, verificación técnica y exportación multiformato** de ejercicios prácticos de C.

Cada ejercicio vive en una carpeta aislada con metadata YAML (`tema`, nivel de **Bloom 1-5**, minutos estimados, pistas progresivas), su solución modelo en C (`solucion.c`), su enunciado en Markdown y su suite de tests.

---

## Alcance

### Qué cubre
- Autoría, catalogación y gestión de bancos de ejercicios prácticos de programación en C.
- Clasificación pedagógica según la taxonomía de Bloom (Recordar, Comprender, Aplicar, Analizar, Evaluar, Crear).
- Calibración y modelado de presupuestos de tiempo de resolución para estudiantes universitarios.
- Serialización y sincronización bidireccional entre metadatos YAML (`ejercicio.yaml`) y documentos Markdown.
- Composición de guías de trabajos prácticos estructuradas y balanceadas.

### Qué no cubre (Límites y Delegación)
- Compilación o ejecución de soluciones de alumnos (delegado a `daedalus` y `nostromo`).
- Corrección masiva de cohortes y base de datos de calificaciones (delegado a `dredd`).
- Generación de exámenes impresos OMR (delegado a `alucard`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.11.

### Dependencias Externas y Binarios
- **gcc** (o **daedalus**): Requerido para verificación y compilación de soluciones modelo en C (`deckard verify`, `lint`).
- **ripley**: Requerido para verificación estática/dinámica de reglas de cátedra y tests I/O (`deckard verify`).
- **typst**: Motor prioritario y recomendado para generación de PDFs de alta fidelidad (`deckard export`). *WeasyPrint se mantiene como fallback legacy.*
- **vasquez**: Motor de inyección de fallos para arneses de resiliencia (`deckard verify test-harness`).
- **dredd**: Orquestador y generador de testcases por fuzzing (`deckard verify fuzz`).

### Integración en el Ecosistema
- CLI `deckard` con soporte `--version` y `--json` en flujos de inspección y automatización.
- Diagnóstico del entorno mediante `deckard doctor`. Conexión directa con `ripley`, `dredd` y `vasquez`.

---

## Instalación

```bash
# Instalación global editable con uv
uv tool install . --editable --force

# O en entorno virtual local
uv sync
uv run deckard --help
```

---

## Inicio Rápido

```bash
# 1. Inicializar la estructura del banco y guías (crea banco/ejemplo-invertir)
deckard init

# 2. Crear un nuevo ejercicio
deckard new invertir-pares --titulo "Invertir pares" --tema arreglos --bloom 3 --minutos 25

# 3. Inspeccionar el banco y enunciados (soporta --json)
deckard bank list
deckard show invertir-pares -s -p

# 4. Verificar la solución modelo con Ripley (soporta --json)
deckard verify invertir-pares

# 5. Crear una especificación y componer una guía balanceada
deckard spec new parcial1.yaml --duracion 90 --margen 0.8 --temas "arreglos,punteros" --bloom-min 2 --bloom-max 4
deckard spec compose parcial1.yaml

# 6. Exportar la guía a PDF (Typst) y Markdown
deckard export guias/parcial1.yaml --type=pdf,md -o dist/
```

---

## Mapa de Comandos de Deckard

### 1. Banco y Enunciados
* `deckard init`: Inicializa la estructura `banco/`, `guias/` y un ejercicio de ejemplo (`ejemplo-invertir`).
* `deckard new <id>`: Crea un nuevo ejercicio con esqueleto completo (`ejercicio.yaml`, `solucion.c`, `enunciado.md`, `tests/`).
* `deckard bank list`: Catálogo tabular del banco con filtros por tema, nivel de Bloom, estado de verificación y salida `--json`.
* `deckard show <id>`: Inspección en consola de enunciados, soluciones, pistas progresivas, tests y metadata (`-s`, `-p`, `--tests`, `--todos`, `--raw`).
* `deckard browse`: Navegador interactivo de ejercicios en consola.
* `deckard sync`: Sincronización bidireccional entre `ejercicio.yaml` y documentos Markdown.
* `deckard cache`: Inspección y actualización de la caché del banco de ejercicios.

### 2. Especificaciones Pedagógicas (`deckard spec`)
* `deckard spec new <archivo>`: Crea especificaciones de diseño curricular (`GuiaSpec`).
* `deckard spec list`: Lista specs con duración nominal, carga útil calculada, temas y rango Bloom.
* `deckard spec show <archivo>`: Detalle del spec y candidatos elegibles en el banco.
* `deckard spec validate <archivo>`: Diagnóstico de satisfactibilidad temática y temporal contra el banco actual.
* `deckard spec edit <archivo>`: Modificación de parámetros de la especificación por CLI.
* `deckard spec compose <archivo>`: Composición directa de la guía a partir del spec.

### 3. Guías de Trabajos Prácticos (`deckard guide`)
* `deckard guide list`: Lista guías compuestas en `guias/` con desglose de ejercicios y verificación.
* `deckard guide show <guia>`: Muestra ejercicios, carga horaria, temas y enunciados.
* `deckard guide compose <spec>`: Algoritmo knapsack de balanceo pedagógico.
* `deckard guide add <guia> <ejercicio>`: Incorpora un ejercicio y recalcula métricas.
* `deckard guide practica <guia> <destino>`: Crea la práctica sobre plantilla-TP desde la guía (ver «Prácticas desde la guía»).
* `deckard guide remove <guia> <ejercicio>`: Remueve un ejercicio y actualiza la guía.
* `deckard guide verify <guia>`: Verifica todas las soluciones modelo de la guía con Ripley.
* `deckard guide export <guia>`: Exporta la guía completa a PDF, Markdown o HTML.

### 4. Exportación Multiformato (`deckard export`)
* `deckard export <objetivo>`: Exporta ejercicios o guías a **PDF** (vía Typst oficial o WeasyPrint legacy), **Typst**, **Markdown** o **HTML** (`--type=pdf,md,html,typ` y `--json`).
* `deckard export templates init`: Copia plantillas por defecto (Typst, HTML, Markdown y CSS) a `./templates/` o global (`--global`).
* `deckard export templates list`: Lista plantillas descubiertas (locales, globales y built-in).

### 5. Verificación, Fuzzing y Arnés (`deckard verify`)
* `deckard verify [id]`: Verificación de reglas pedagógicas y compilación con `ripley check`. Admite comodines, `--all`, reporte de fallos (`--log-fallos`) y salida estructurada `--json`.
  > Los ejercicios que fallan se marcan automáticamente como no-verificados (`verificado: false`).
* `deckard verify --rubric [id]`: Coherencia de la rúbrica sin compilar: los pesos tienen que sumar 100 % y cada criterio `test:<nombre>` tiene que ser una prueba del ejercicio. Sale con 2 si alguna no cumple.
* `deckard verify fuzz [id]`: Fuzzing y endurecimiento de testcases con `dredd fuzz-gen` y libFuzzer.
* `deckard verify test-harness <id> <spec>`: Arnés de pruebas con inyección de fallos de memoria vía `vasquez inject`.

### Casos de ejercicios de funciones (`deckard exercise cubrir`)
* `deckard exercise cubrir <id>… [--banco B] [--sin-cobertura] [--regenerar-specs]`: para un ejercicio cuyos `funciones:` tienen parámetros y retorno escalares, escribe `tests/funciones/`: un `driver.c` que lee `<función> <args>` por línea y escribe el resultado, una especificación de tyrell por función (`tyrell/<función>.yaml`, con rangos propuestos para que el docente los revise) y los casos `<función>_NN.in/.out`, con la solución de la cátedra como referencia y los casos que suman ramas (`tyrell cubrir`). Los casos en que la solución desborda o tiene comportamiento indefinido se descartan. Las especificaciones existentes se respetan: se corrigen y se vuelve a correr. ripley no lee esa carpeta; dredd sí, enlazando el archivo del alumno con el driver.

Las funciones con punteros, arreglos o structs se omiten y las demás se prueban. Si la solución trae el relleno del banco (`if (val <= 0) return 0; return val * 2;`), esa función no genera casos: sus `.out` rechazarían soluciones correctas; `deckard lint` lo avisa con `solucion-relleno`. La salida informa las ramas ejecutadas, sin contar el `main` ni los `test_*` de la solución, que el driver no llama.

### Rúbricas y notas (`deckard exercise rubric`)
* `deckard exercise rubric <id> [--md R.md] [--dredd R.json]`: Rúbrica del ejercicio (la de `rubrica:` en `ejercicio.yaml` o la de la cátedra) en Markdown o para dredd.
* `deckard exercise rubric <id> --eval-results <dir> [--salida calificaciones]`: Califica lo que evaluó `dredd eval` (de cada estudiante, su última revisión: `rNi/auditoria.json` y `hallazgos.json`). Escribe `calificaciones.csv` para importar en el libro de calificaciones de Moodle (`Usuario`, `Calificación` 0–10, logro por criterio y comentario) y `devoluciones/<alumno>.md`.
  > Cada criterio vale entre 0 y 1: `tests_unitarios` (pruebas aprobadas), `test:<nombre>` (esa prueba), y los de hallazgos (`estilo_gaff`, `sanitizers_memoria`, `antipatrones_spunkmeyer`, `modularidad_y_diseño` o una categoría de yutani como `memoria`) descuentan 0,25 por error, 0,10 por advertencia y 0,05 por estilo; las fugas descuentan 0,25 en `sanitizers_memoria`. Si no compila, la nota es 0. Un criterio sin evidencia automática deja la nota *provisoria*.

### 6. Diagnóstico, Auditoría y Calidad
* `deckard doctor`: Diagnóstico integral del estado de herramientas externas (gcc, typst, daedalus, ripley, git).
* `deckard stats`: Histogramas ASCII de distribución Bloom, carga horaria y resumen estadístico (`--json`).
* `deckard lint`: Lint del banco antes de publicar: ejercicios, temario, guías y trazabilidad con el apunte (`--compilar` también compila el starter code).
* `deckard deps` / `deckard graph`: Análisis y visualización de grafo de dependencias temáticas entre ejercicios.
* `deckard audit`: Detección de placeholders, omisiones y estado de completitud pedagógica del banco.
* `deckard languagetool`: Auditoría ortográfica y gramatical de consignas con LanguageTool.

### 7. Empaquetado y Distribución
* `deckard pack <objetivo>`: Empaqueta ejercicios/guías en archivos firmados `.ripkg` y genera starter repos para GitHub Classroom.
* `deckard unpack <paquete.ripkg>`: Desempaqueta y restaura ejercicios desde paquetes `.ripkg`.
* `deckard multiplex <spec>`: Generador de variantes combinatorias de TPs con asignación determinista por padrón/legajo.

### 8. Curaduría y Mejora con IA (`deckard improve` / `ai`)
* `deckard improve clarity <id|banco|gift>`: Claridad y desambiguación con verbos operativos de Bloom.
* `deckard improve edge-cases <id|banco|gift>`: Especificación exhaustiva de casos borde, pre y postcondiciones.
* `deckard improve examples <id|banco|gift>`: Enriquecimiento con ejemplos de I/O y trazas de ejecución.
* `deckard improve hints <id|banco|gift>`: Generación de pistas pedagógicas progresivas de 3 niveles.
* `deckard improve bloom <id|banco|gift>`: Alineación estricta con la taxonomía de Bloom del ejercicio.
* `deckard improve testcases <id|banco|gift>`: Casos de prueba exhaustivos (borde, típicos, error).
* `deckard improve starter <id|banco|gift>`: Código esqueleto inicial (`starter_code`) y cabeceras Doxygen.
* `deckard improve all <id|banco|gift>`: Mejora holística e integral de la consigna en una única pasada.
* `deckard improve models [prefijo] [--proveedor P]`: Lista los modelos que ofrece el proveedor de IA (`--raw` para lista plana; el prefijo filtra, ej. `opencode-go`).
  > Todos los subcomandos de mejora aceptan `--proveedor` (`google`, `local`, `opencode` o `claude`) y `-m` / `--model` (ej: `-m "opencode-go/deepseek-v4-pro"` o, con un servidor local, `--proveedor local -m qwen2.5-coder:7b`), `--prompt` (`-p`), `--prompt-file` (`-P`), `--apply` (`-a`), `--diff` y `--show-prompt`.
  > El proveedor se configura igual que en el resto del ecosistema (yutani.ia): `--proveedor`, la variable `P1_IA_PROVEEDOR` o `~/.config/p1/ia.toml` (con `[herramientas.deckard]` para lo propio de deckard). Sin nada configurado se usa OpenCode, con `opencode-sandboxed` si está instalado. Cada aspecto envía sólo lo que usa (`clarity` y `bloom` no llevan la solución ni las pistas; `starter` no ve la solución; el ID y la duración no viajan; la solución va sin comentarios ni líneas en blanco; las etiquetas MyST y los `---` del final se reponen al aplicar), `edge-cases` y `examples` devuelven sólo su sección, y en GIFT no viajan los comentarios ni las categorías. `deckard doctor` muestra qué proveedor quedó y si está disponible. Para Gemini o Claude hace falta el extra `ai` (`uv tool install "deckard[ecosistema,languagetool,ai] @ git+https://github.com/INGCOM-UNRN/deckard"`) y `GEMINI_API_KEY` o `ANTHROPIC_API_KEY`; con un servidor local u OpenCode, nada más.

---

## Prácticas desde la guía

Las prácticas nuevas se crean **desde su guía compuesta**, la forma más simple de que banco,
guía, práctica y corrección no se desincronicen. Además de los ejercicios, la guía declara sus
librerías y los targets de la corrección:

```yaml
nombre: Guía 3 — Cadenas
ejercicios:
- {id: invertir-cadena, librerias: [cadenas]}    # como ./tp.sh add-ex invertir-cadena cadenas
- {id: palindromo, librerias: [cadenas, arreglos]}
librerias:
- {nombre: p1_test, origen: catedra, repositorio: "https://github.com/INGCOM-UNRN-P1/treadstone", commit: "41b344d…"}
- {nombre: cadenas, origen: crear, descripcion: "Utilidades de cadenas", forma: plana}
- {nombre: pila, origen: crear, ejercicio: tda-pila}          # API y pruebas desde ese ejercicio del banco
- {nombre: arreglos, origen: reutilizar, guia: guia-2}        # la escribió el alumno en la guía 2
targets_docente:
- {nombre: ocultas, descripcion: "Casos no publicados", tipo: pruebas_ocultas, peso: 30}
- {nombre: memoria, descripcion: "Sin pérdidas de memoria", tipo: memcheck, peso: 20, visible: true}
- {nombre: estilo, descripcion: "Estilo de la cátedra", receta: ["@mkdir -p .dredd", "ripley check . --json --exit-zero > .dredd/ripley.json"], produce: json, archivo: .dredd/ripley.json}
```

`deckard guide practica guia-3 ../tp3` arma la práctica sobre plantilla-TP con su `tp.sh`: los
ejercicios con el id del banco, enunciado, cabeceras, código inicial, `prueba.c` (p1_test) y los
casos públicos (nunca la solución ni los ocultos), y `PRACTICA.md` con cómo traer las librerías
reutilizadas. Del lado del docente deja `../tp3-dredd/` con `dredd.mk` (targets `dredd-…`, que
la plantilla incluye con `-include dredd.mk`), las pruebas ocultas en `.dredd/` y `targets.json`
para dredd. Si la práctica ya existe, muestra qué cambiaría (`--aplicar` lo escribe; lo que ya no
está en la guía no se borra). `deckard spec validate` revisa las librerías (`--remoto`: avisa si
una de la cátedra quedó en un commit viejo), y `compose` las traslada de la spec a la guía.

## Documentación Detallada

Para una guía paso a paso con todos los flujos pedagógicos, modelos de datos, personalización de plantillas y ejemplos de integración con Ripley, Dredd y Vasquez, consultá el [**Manual Integral de Uso (`MANUAL.md`)**](https://github.com/INGCOM-UNRN/deckard/blob/main/MANUAL.md).

---

## Integración en el Ecosistema

| Herramienta | Rol en el ecosistema |
| :--- | :--- |
| **deckard** | Banco de ejercicios, balanceo pedagógico (Bloom) y exportación multiformato. |
| **ripley** | Verificación estática/dinámica de soluciones modelo y sandbox docente. |
| **dredd** | Corrección masiva de entregas de alumnos, feedback y fuzzing de testcases. |
| **vasquez** | Inyección de fallos de memoria en tiempo de ejecución para arneses de prueba (`test-harness`). |
| **alucard** | Síntesis de exámenes, question banks (GIFT/Moodle) y tracing C con GCC. |
| **idkfa** | Generador de cuestionarios Moodle XML aleatorizados y anti-trampas. |
| **myst-tools** | Validador y gestor de enlaces/anclas para documentación MyST Markdown. |

*(Nota de diseño: Deckard no consume ni depende de `tyrell`, la síntesis y fuzzing de casos de prueba se delega enteramente a `dredd`).*

### Comandos agrupados

Los comandos están agrupados: `bank` (banco), `verify` (verificación, fuzzing y sanitizers),
`export` (todos los formatos: `export moodle`, `export web`, `export anki`…), `quality`
(terminología, tono, ambigüedad, ortografía, duplicados) y `exercise` (crear y completar
ejercicios: `exercise new`, `exercise scaffold`, `exercise diagram-memory`…). Los nombres
anteriores del primer nivel (`deckard lint-consigna`, `deckard export-moodle`…) siguen andando,
ocultos en la ayuda y con un aviso del nombre nuevo; se van a retirar.

### Esquema de `ejercicio.yaml`

Un `ejercicio.yaml` inválido se informa en español, con el archivo y el campo («falta el campo
obligatorio «titulo»», ««id» = 'Mal Id' no tiene el formato esperado»). El JSON Schema está en
`esquemas/ejercicio.schema.json` (y `deckard bank schema` lo imprime): con
`# yaml-language-server: $schema=…/ejercicio.schema.json` al principio del archivo, el editor lo
valida mientras se escribe.

Además de los campos de siempre (`id`, `titulo`, `tema`, `bloom`, `minutos_estimados`, `pistas`,
`funciones`, `tests_funciones`…), un ejercicio puede declarar los metadatos que muestran las
plantillas del repositorio de enunciados (todos opcionales):

```yaml
unidad: 6
modulo: Estructuras enlazadas
subtema: arboles_binarios
dificultad: intermedia            # inicial | intermedia | avanzada | desafio
esfuerzo_lineas_codigo: 80
tipo: practica_guiada             # concepto | practica_guiada | laboratorio | desafio | parcial_previo
obligatorio: true
prerrequisitos: [punteros, lista-enlazada]   # temas o ids de ejercicios
correquisitos: [recursividad]
siguiente_recomendado: [arena-allocator]     # ids de ejercicios
referencias_teoria:
  apunte: https://ingcom-unrn-p1.github.io/apunte/arboles
  seccion: Recorridos
  bibliografia: ["K&R, cap. 6"]
visibilidad_solucion: desplegable # publica | desplegable | protegida | oculta
rubrica:                          # también vale la forma anterior {criterio: peso}
- {criterio: tests_unitarios, peso: 70}
- {criterio: estilo_gaff, peso: 30}
```

La cabecera `<id>.h` del ejercicio se lee del banco y aparece en el enunciado exportado. Con
`visibilidad_solucion: oculta` la solución no sale en ninguna exportación, aunque se pida con
`-s`. `prerrequisitos`, `dependencias` y `siguiente_recomendado` son aristas del grafo de
`deckard bank deps`, y `deckard verify audit` avisa de las referencias a ejercicios (o temas) que no
están en el banco. Las plantillas de exportación son las del repositorio de enunciados; deckard
busca primero `templates/` junto al banco (`<banco>/../templates/`), así que un banco con sus
propias plantillas las usa sin `--template`.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Programas del sistema: `gcc`, `typst`.

| Sistema | `gcc` | `typst` |
|:--|:--|:--|
| Debian / Ubuntu | `sudo apt install gcc` | binario de https://github.com/typst/typst/releases |
| Fedora | `sudo dnf install gcc` | binario de https://github.com/typst/typst/releases |
| Windows | incluido en el entorno de la cátedra (MSYS2 UCRT64) | `winget install --id Typst.Typst` |
| macOS | `xcode-select --install` (clang como `gcc`) | `brew install typst` |

### Comandos

| Comando | Descripción |
|:--|:--|
| `deckard init` | Inicializa la estructura del banco (banco/, guias/). |
| `deckard compose` | Compone una guía balanceada por carga cognitiva y taxonomía de Bloom. |
| `deckard doctor` | Verifica dependencias externas del sistema (GCC, Typst, Daedalus, Git). |
| `deckard bank` | Inspección del banco de ejercicios. |
| `deckard verify` | Verificación pedagógica (ripley check), fuzzing (dredd) y arnés de pruebas (vasquez inject). |
| `deckard tag` | Gestión y consulta de etiquetas (tags) en el banco. |
| `deckard export` | Exportación multiformato (PDF, Markdown, HTML) y gestión de plantillas. |
| `deckard guide` | Gestión, inspección y exportación de guías. |
| `deckard spec` | Gestión, validación y composición de especificaciones de guías (GuiaSpec). |
| `deckard improve` | Mejora y curaduría pedagógica de consignas y bancos de ejercicios con IA (Gemini, servidor local, OpenCode o Claude). |
| `deckard quality` | Calidad de consignas y bancos: terminología, tono, ambigüedad, ortografía, duplicados. |
| `deckard exercise` | Crear y completar ejercicios: esqueletos, variantes, pruebas, rúbricas y diagramas. |

Ayuda de cada comando: `deckard <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `deckard doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-deckard-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `deckard`
:open:

```text
 Uso: deckard [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestor de bancos de ejercicios prácticos, guías y graduación (Programación 1).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de deckard y sale.                            │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ init      Inicializa la estructura del banco (banco/, guias/).                                   │
│ compose   Compone una guía balanceada por carga cognitiva y taxonomía de Bloom.                  │
│ doctor    Verifica dependencias externas del sistema (GCC, Typst, Daedalus, Git).                │
│ bank      Inspección del banco de ejercicios.                                                    │
│ verify    Verificación pedagógica (ripley check), fuzzing (dredd) y arnés de pruebas (vasquez    │
│           inject).                                                                               │
│ tag       Gestión y consulta de etiquetas (tags) en el banco.                                    │
│ export    Exportación multiformato (PDF, Markdown, HTML) y gestión de plantillas.                │
│ guide     Gestión, inspección y exportación de guías.                                            │
│ spec      Gestión, validación y composición de especificaciones de guías (GuiaSpec).             │
│ improve   Mejora y curaduría pedagógica de consignas y bancos de ejercicios con IA (Gemini,      │
│           servidor local, OpenCode o Claude).                                                    │
│ quality   Calidad de consignas y bancos: terminología, tono, ambigüedad, ortografía, duplicados. │
│ exercise  Crear y completar ejercicios: esqueletos, variantes, pruebas, rúbricas y diagramas.    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard init`

```text
 Uso: deckard init [OPCIONES] [banco]

 Inicializa la estructura del banco (banco/, guias/).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   banco      <path>  Directorio raíz del banco. [por defecto: .]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard compose`

```text
 Uso: deckard compose [OPCIONES] {spec_file}

 Compone una guía balanceada por carga cognitiva y taxonomía de Bloom.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_file      <path>  guia.yaml con nombre/duración/temas. [obligatorio]                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  [por defecto: banco]                                                    │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard doctor`

```text
 Uso: deckard doctor [OPCIONES]

 Verifica dependencias externas del sistema (GCC, Typst, Daedalus, Git).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el diagnóstico como JSON (schema_version 1.0.0).                        │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank`

```text
 Uso: deckard bank [OPCIONES] COMANDO [ARGUMENTOS]...

 Inspección del banco de ejercicios.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ list             Lista los ejercicios del banco con su nivel, carga, tags y filtros.             │
│ reorganize       Reorganiza los ejercicios en carpetas según nivel de Bloom, tipo (funciones vs  │
│                  io) y/o tema.                                                                   │
│ organize         Reorganiza los ejercicios en carpetas según nivel de Bloom, tipo (funciones vs  │
│                  io) y/o tema.                                                                   │
│ show             Muestra el enunciado y detalles de un ejercicio con control de secciones.       │
│ stats            Grafica la distribución de Bloom y tiempos acumulados con histogramas ASCII en  │
│                  terminal.                                                                       │
│ lint             Revisa el banco antes de publicar: ejercicios, temario, guías y trazabilidad    │
│                  con el apunte.                                                                  │
│ duplicate        Clona y versiona variantes de ejercicios conservando enunciados, solución y     │
│                  tests.                                                                          │
│ deps             Detecta y grafica dependencias conceptuales y grafo de prerrequisitos entre     │
│                  ejercicios.                                                                     │
│ index            Actualiza o reconstruye el índice SQLite (~/.cache/deckard/index.db) para       │
│                  acelerar búsquedas en bancos masivos.                                           │
│ browse           Navega y visualiza interactivamente ejercicios del banco con Rich.              │
│ schema           JSON Schema de ejercicio.yaml, para que el editor valide mientras se escribe.   │
│ graph            Detecta y grafica dependencias conceptuales y grafo de prerrequisitos entre     │
│                  ejercicios.                                                                     │
│ cache            Actualiza o reconstruye el índice SQLite (~/.cache/deckard/index.db) para       │
│                  acelerar búsquedas en bancos masivos.                                           │
│ sync             Sincroniza el banco de ejercicios con un repositorio Git descentralizado.       │
│ select-prereqs   Selecciona y filtra ejercicios del banco cuyos prerrequisitos temáticos estén   │
│                  satisfechos.                                                                    │
│ license-manager  Gestiona metadatos de autoría, licencias educativas y headers de copyright.     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank list`

```text
 Uso: deckard bank list [OPCIONES] [patron]

 Lista los ejercicios del banco con su nivel, carga, tags y filtros.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  Filtro o comodín (ej: 'invertir-*', 'punteros/*').                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                              <path>                 Directorio raíz del banco.           │
│                                                             [por defecto: banco]                 │
│ --tema        -t                     <str>                  Filtrar por tema.                    │
│ --bloom       -b                     <int range> [1<=x<=5]  Filtrar por nivel de Bloom (1-5).    │
│ --tag         -T                     <str>                  Filtrar por etiqueta/tag.            │
│ --verificado      --no-verificado                           Filtrar por estado de verificación.  │
│ --json                                                      Salida en formato JSON estructurado. │
│ --help        -h                                            Muestra esta ayuda y sale.           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank reorganize`

```text
 Uso: deckard bank reorganize [OPCIONES]

 Reorganiza los ejercicios en carpetas según nivel de Bloom, tipo (funciones vs io) y/o tema.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                  <path>  Directorio raíz del banco de ejercicios. [por defecto: banco]   │
│ --by,--criterio  -b      <str>   Criterio de reorganización: 'bloom', 'tipo', 'bloom/tipo',      │
│                                  'tipo/bloom', 'tema/bloom', 'bloom/tema', 'tema/tipo', 'plano'. │
│                                  [por defecto: bloom/tipo]                                       │
│ --destino        -d      <path>  Directorio de destino (por defecto, reorganiza dentro del mismo │
│                                  banco).                                                         │
│ --dry-run        -n              Simula la reorganización y muestra los movimientos sin          │
│                                  modificar el disco.                                             │
│ --copy           -c              Copia los ejercicios al nuevo esquema en vez de moverlos.       │
│ --help           -h              Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank organize`

```text
 Uso: deckard bank organize [OPCIONES]

 Reorganiza los ejercicios en carpetas según nivel de Bloom, tipo (funciones vs io) y/o tema.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                  <path>  Directorio raíz del banco de ejercicios. [por defecto: banco]   │
│ --by,--criterio  -b      <str>   Criterio de reorganización: 'bloom', 'tipo', 'bloom/tipo',      │
│                                  'tipo/bloom', 'tema/bloom', 'bloom/tema', 'tema/tipo', 'plano'. │
│                                  [por defecto: bloom/tipo]                                       │
│ --destino        -d      <path>  Directorio de destino (por defecto, reorganiza dentro del mismo │
│                                  banco).                                                         │
│ --dry-run        -n              Simula la reorganización y muestra los movimientos sin          │
│                                  modificar el disco.                                             │
│ --copy           -c              Copia los ejercicios al nuevo esquema en vez de moverlos.       │
│ --help           -h              Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank show`

```text
 Uso: deckard bank show [OPCIONES] {ejercicio_id}

 Muestra el enunciado y detalles de un ejercicio con control de secciones.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  Id del ejercicio o ruta al directorio del ejercicio. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                            <path>  Directorio raíz del banco. [por defecto: banco]       │
│ --enunciado  -e  --no-enunciado            Mostrar enunciado. [por defecto: enunciado]           │
│ --solucion   -s                            Mostrar solución modelo en C.                         │
│ --pistas     -p                            Mostrar pistas progresivas.                           │
│ --meta       -m  --no-meta                 Mostrar panel de metadatos. [por defecto: meta]       │
│ --tests      -t                            Mostrar casos de prueba tests/.                       │
│ --todos      -a                            Mostrar todas las secciones.                          │
│ --raw                                      Salida en texto plano sin formato Rich.               │
│ --help       -h                            Muestra esta ayuda y sale.                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank stats`

```text
 Uso: deckard bank stats [OPCIONES]

 Grafica la distribución de Bloom y tiempos acumulados con histogramas ASCII en terminal.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco a analizar. [por defecto: banco]              │
│ --json                   Salida en formato JSON estructurado.                                    │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank lint`

```text
 Uso: deckard bank lint [OPCIONES] [patron]

 Revisa el banco antes de publicar: ejercicios, temario, guías y trazabilidad con el apunte.

 Reglas: ids únicos y coherentes con su carpeta, tema y `dep:<tema>` del temario, enunciado y
 solución de lo publicable, guías que citan ejercicios existentes y publicados, páginas del
 apunte citadas en temas.yaml que existen y están en su TOC, y bloques de `export apunte` al día.
 Sale con 1 si hay errores (con --estricto, también si hay avisos).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  Revisar sólo los ejercicios cuyo id contiene este texto.                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                         <path>              Directorio raíz del banco.                   │
│                                                     [por defecto: banco]                         │
│ --temas                         <path>              temas.yaml (por omisión                      │
│                                                     <banco>/../temas.yaml, si existe).           │
│ --guias                         <path>              Directorio de guías (por omisión             │
│                                                     <banco>/../guias, si existe).                │
│ --apunte                        <path>              Repositorio del apunte: revisa las páginas   │
│                                                     citadas y los bloques de export apunte.      │
│ --compilar                                          Compilar también el starter_code de cada     │
│                                                     ejercicio.                                   │
│ --verificar-soluciones                              Pasar cada solución publicable por ripley    │
│                                                     check (lento).                               │
│ --ripley                        <str>               Ejecutable de ripley para                    │
│                                                     --verificar-soluciones (por omisión, el del  │
│                                                     PATH).                                       │
│ --estricto                                          Salir con 1 también si hay avisos.           │
│ --json                                              Salida en JSON (hallazgos y conteo por       │
│                                                     regla).                                      │
│ --max                           <int range> [x>=0]  Hallazgos a listar en la tabla (el conteo    │
│                                                     por regla es completo).                      │
│                                                     [por defecto: 200]                           │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank duplicate`

```text
 Uso: deckard bank duplicate [OPCIONES] {origen_id} {nuevo_id}

 Clona y versiona variantes de ejercicios conservando enunciados, solución y tests.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    origen_id      <str>  ID o slug del ejercicio original a clonar. [obligatorio]              │
│ *    nuevo_id       <str>  Nuevo ID o slug para la copia. [obligatorio]                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --titulo  -t      <str>   Nuevo título para el ejercicio clonado.                                │
│ --banco           <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank deps`

```text
 Uso: deckard bank deps [OPCIONES] [patron]

 Detecta y grafica dependencias conceptuales y grafo de prerrequisitos entre ejercicios.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  Filtrar por ID o patrón de ejercicios.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco            <path>  Directorio raíz del banco. [por defecto: banco]                       │
│ --mermaid  -m              Emitir salida en formato Mermaid para documentación.                  │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank index`

```text
 Uso: deckard bank index [OPCIONES]

 Actualiza o reconstruye el índice SQLite (~/.cache/deckard/index.db) para acelerar búsquedas en
 bancos masivos.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco a indexar. [por defecto: banco]               │
│ --force  -f              Reconstruir la base de datos de índice desde cero.                      │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank browse`

```text
 Uso: deckard bank browse [OPCIONES] [patron]

 Navega y visualiza interactivamente ejercicios del banco con Rich.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  Filtro de búsqueda por ID o tema.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --id     -i      <str>   Mostrar ficha detallada de un ejercicio específico.                     │
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank schema`

```text
 Uso: deckard bank schema [OPCIONES]

 JSON Schema de ejercicio.yaml, para que el editor valide mientras se escribe.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Archivo donde guardar el JSON Schema (si no, se imprime).              │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank graph`

```text
 Uso: deckard bank graph [OPCIONES] [patron]

 Detecta y grafica dependencias conceptuales y grafo de prerrequisitos entre ejercicios.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  Filtrar por ID o patrón de ejercicios.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco            <path>  Directorio raíz del banco. [por defecto: banco]                       │
│ --mermaid  -m              Emitir salida en formato Mermaid para documentación.                  │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank cache`

```text
 Uso: deckard bank cache [OPCIONES]

 Actualiza o reconstruye el índice SQLite (~/.cache/deckard/index.db) para acelerar búsquedas en
 bancos masivos.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco a indexar. [por defecto: banco]               │
│ --force  -f              Reconstruir la base de datos de índice desde cero.                      │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank sync`

```text
 Uso: deckard bank sync [OPCIONES] [remote_url]

 Sincroniza el banco de ejercicios con un repositorio Git descentralizado.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   remote_url      <str>  URL del repositorio Git remoto a clonar o vincular.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --branch          <str>   Rama a sincronizar. [por defecto: main]                                │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank select-prereqs`

```text
 Uso: deckard bank select-prereqs [OPCIONES] {temas}

 Selecciona y filtra ejercicios del banco cuyos prerrequisitos temáticos estén satisfechos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    temas      <str>  Temas dominados separados por coma (ej:                                   │
│                        'variables,control_flujo,arreglos').                                      │
│                        [obligatorio]                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco       -b      <path>  Directorio raíz del banco. [por defecto: banco]                    │
│ --bloom-max           <int>   Nivel máximo de Bloom.                                             │
│ --topologico                  Listar en orden topológico estricto.                               │
│ --help        -h              Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard bank license-manager`

```text
 Uso: deckard bank license-manager [OPCIONES] {ejercicio_id}

 Gestiona metadatos de autoría, licencias educativas y headers de copyright.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio. [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --autor     -a      <str>   Nombre del autor o equipo docente.                                   │
│ --licencia  -l      <str>   Identificador de licencia (CC-BY-SA-4.0, MIT, etc.).                 │
│                             [por defecto: CC-BY-SA-4.0]                                          │
│ --anio              <int>   Año de autoría. [por defecto: 2026]                                  │
│ --aplicar                   Inyectar y persistir los metadatos en archivos.                      │
│ --banco     -b      <path>  Directorio raíz del banco. [por defecto: banco]                      │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify`

```text
 Uso: deckard verify [OPCIONES] COMANDO [ARGUMENTOS]...

 Verificación pedagógica (ripley check), fuzzing (dredd) y arnés de pruebas (vasquez inject).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ health        Audita la salud del banco: longitud y calidad de redacción del enunciado, y        │
│               completitud de especificación.                                                     │
│ audit         Audita la salud del banco: longitud y calidad de redacción del enunciado, y        │
│               completitud de especificación.                                                     │
│ fuzz          Endurece los tests de ejercicios con `drake gen-casos` (o `dredd fuzz-gen`)        │
│               (soporta wildcards, batch y tracking de progreso).                                 │
│ harness       Corre el arnés de prueba con inyección de fallos de memoria vía `vasquez inject`.  │
│ test-harness  Corre el arnés de prueba con inyección de fallos de memoria vía `vasquez inject`.  │
│ multiplex     tp-multiplexer: Genera variantes combinatorias y asignación determinista por       │
│               alumno.                                                                            │
│ sanitizers    Audita la solución modelo contra fugas de memoria (ASan) y comportamientos         │
│               indefinidos (UBSan).                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify health`

```text
 Uso: deckard verify health [OPCIONES] [patron]

 Audita la salud del banco: longitud y calidad de redacción del enunciado, y completitud de
 especificación.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  ID o patrón comodín de ejercicios a auditar.                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                   <path>                 Directorio raíz del banco. [por defecto: banco] │
│ --tema            -t      <str>                  Filtrar por tema.                               │
│ --bloom           -b      <int range> [1<=x<=5]  Filtrar por nivel de Bloom.                     │
│ --tag             -T      <str>                  Filtrar por etiqueta/tag.                       │
│ --min-chars       -m      <int>                  Largo mínimo de caracteres en enunciado para    │
│                                                  considerar redacción suficiente.                │
│                                                  [por defecto: 100]                              │
│ --pobres,--short  -p                             Mostrar únicamente ejercicios con redacción     │
│                                                  pobre o incompleta.                             │
│ --incompletos     -i                             Mostrar solo ejercicios con componentes         │
│                                                  faltantes.                                      │
│ --sin-tests                                      Filtrar ejercicios sin casos de prueba (I/O ni  │
│                                                  funciones).                                     │
│ --sin-pistas                                     Filtrar ejercicios sin pistas progresivas.      │
│ --sin-solucion                                   Filtrar ejercicios sin solución modelo.         │
│ --json                                           Emitir reporte estructurado en formato JSON.    │
│ --help            -h                             Muestra esta ayuda y sale.                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify audit`

```text
 Uso: deckard verify audit [OPCIONES] [patron]

 Audita la salud del banco: longitud y calidad de redacción del enunciado, y completitud de
 especificación.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   patron      <str>  ID o patrón comodín de ejercicios a auditar.                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                   <path>                 Directorio raíz del banco. [por defecto: banco] │
│ --tema            -t      <str>                  Filtrar por tema.                               │
│ --bloom           -b      <int range> [1<=x<=5]  Filtrar por nivel de Bloom.                     │
│ --tag             -T      <str>                  Filtrar por etiqueta/tag.                       │
│ --min-chars       -m      <int>                  Largo mínimo de caracteres en enunciado para    │
│                                                  considerar redacción suficiente.                │
│                                                  [por defecto: 100]                              │
│ --pobres,--short  -p                             Mostrar únicamente ejercicios con redacción     │
│                                                  pobre o incompleta.                             │
│ --incompletos     -i                             Mostrar solo ejercicios con componentes         │
│                                                  faltantes.                                      │
│ --sin-tests                                      Filtrar ejercicios sin casos de prueba (I/O ni  │
│                                                  funciones).                                     │
│ --sin-pistas                                     Filtrar ejercicios sin pistas progresivas.      │
│ --sin-solucion                                   Filtrar ejercicios sin solución modelo.         │
│ --json                                           Emitir reporte estructurado en formato JSON.    │
│ --help            -h                             Muestra esta ayuda y sale.                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify fuzz`

```text
 Uso: deckard verify fuzz [OPCIONES] [ejercicio_id]

 Endurece los tests de ejercicios con `drake gen-casos` (o `dredd fuzz-gen`) (soporta wildcards,
 batch y tracking de progreso).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   ejercicio_id      <str>  Id del ejercicio o patrón comodín (ej: '*', 'invertir-*',             │
│                            'punteros/*').                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                  <path>                 Directorio raíz del banco. [por defecto: banco]  │
│ --all            -a                             Ejecutar fuzzing sobre todos los ejercicios del  │
│                                                 banco.                                           │
│ --tema           -t      <str>                  Filtrar por tema.                                │
│ --bloom          -b      <int range> [1<=x<=5]  Filtrar por nivel de Bloom (1-5).                │
│ --cantidad       -n      <int>                  Cantidad de casos de prueba a generar por        │
│                                                 ejercicio.                                       │
│                                                 [por defecto: 8]                                 │
│ --segundos               <int>                  Segundos de fuzzing si libFuzzer está            │
│                                                 disponible.                                      │
│                                                 [por defecto: 15]                                │
│ --sin-libfuzzer                                 Forzar modo determinista sin libFuzzer.          │
│ --fail-fast                                     Detenerse inmediatamente ante el primer error.   │
│ --dry-run                                       Solo listar ejercicios que se procesarían sin    │
│                                                 ejecutar.                                        │
│ --log-fallos     -l      <path>                 Ruta de archivo para guardar el reporte de       │
│                                                 ejercicios fallidos u omitidos.                  │
│ --help           -h                             Muestra esta ayuda y sale.                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify harness`

```text
 Uso: deckard verify harness [OPCIONES] {ejercicio_id} {spec}

 Corre el arnés de prueba con inyección de fallos de memoria vía `vasquez inject`.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>   Id del ejercicio en el banco. [obligatorio]                       │
│ *    spec              <path>  spec.yaml del arnés. [obligatorio]                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                <path>  Directorio del banco. [por defecto: banco]                        │
│ --herramienta          <str>   Binario de inyección (por defecto vasquez).                       │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify test-harness`

```text
 Uso: deckard verify test-harness [OPCIONES] {ejercicio_id} {spec}

 Corre el arnés de prueba con inyección de fallos de memoria vía `vasquez inject`.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>   Id del ejercicio en el banco. [obligatorio]                       │
│ *    spec              <path>  spec.yaml del arnés. [obligatorio]                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                <path>  Directorio del banco. [por defecto: banco]                        │
│ --herramienta          <str>   Binario de inyección (por defecto vasquez).                       │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify multiplex`

```text
 Uso: deckard verify multiplex [OPCIONES]

 tp-multiplexer: Genera variantes combinatorias y asignación determinista por alumno.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --spec      -s                   <path>  Ruta al archivo matriz.yaml. [obligatorio]           │
│    --students                       <path>  CSV con lista de alumnos.                            │
│    --salida    -o                   <path>  Directorio destino de la multiplexación.             │
│                                             [por defecto: dist/multiplex]                        │
│    --pack          --no-pack                Generar paquetes .ripkg para cada variante.          │
│                                             [por defecto: pack]                                  │
│    --starters      --no-starters            Generar starter repos por alumno.                    │
│                                             [por defecto: starters]                              │
│    --help      -h                           Muestra esta ayuda y sale.                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard verify sanitizers`

```text
 Uso: deckard verify sanitizers [OPCIONES] {target}

 Audita la solución modelo contra fugas de memoria (ASan) y comportamientos indefinidos (UBSan).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio o directorio. [obligatorio]                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard tag`

```text
 Uso: deckard tag [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestión y consulta de etiquetas (tags) en el banco.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ list    Lista todas las etiquetas presentes en el banco de ejercicios.                           │
│ add     Agrega una o más etiquetas a ejercicios del banco.                                       │
│ remove  Remueve una o más etiquetas de ejercicios del banco.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard tag list`

```text
 Uso: deckard tag list [OPCIONES]

 Lista todas las etiquetas presentes en el banco de ejercicios.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard tag add`

```text
 Uso: deckard tag add [OPCIONES] {patron} {tags}...

 Agrega una o más etiquetas a ejercicios del banco.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    patron      <str>  ID o patrón comodín de ejercicios (ej: 'invertir-*', '*'). [obligatorio] │
│ *    tags        <str>  Etiquetas a agregar. [obligatorio]                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard tag remove`

```text
 Uso: deckard tag remove [OPCIONES] {patron} {tags}...

 Remueve una o más etiquetas de ejercicios del banco.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    patron      <str>  ID o patrón comodín de ejercicios. [obligatorio]                         │
│ *    tags        <str>  Etiquetas a remover. [obligatorio]                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export`

```text
 Uso: deckard export [OPCIONES] COMANDO [ARGUMENTOS]...

 Exportación multiformato (PDF, Markdown, HTML) y gestión de plantillas.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ pack               Empaqueta ejercicios o guías como .ripkg para Ripley y starter repos.         │
│ unpack             Extrae un bundle .deckard.tar.gz en el banco o directorio especificado.       │
│ publish-classroom  Genera la estructura completa de un repositorio para GitHub Classroom         │
│                    (README, starter code, Makefile, CI).                                         │
│ classroom          Genera la estructura completa de un repositorio para GitHub Classroom         │
│                    (README, starter code, Makefile, CI).                                         │
│ notebook           Exporta un ejercicio en formato interactivo Jupyter Notebook (.ipynb) con     │
│                    kernel C.                                                                     │
│ pack-zip           Empaqueta un starter kit o guía completa en un archivo ZIP con clave de       │
│                    entrega (QoL 11).                                                             │
│ hints              Exporta o genera pistas escalonadas (Hints) progresivas para un ejercicio     │
│                    (QoL 15).                                                                     │
│ to-md              Convierte un ejercicio estructurado en un único Markdown interactivo con YAML │
│                    frontmatter.                                                                  │
│ from-md            Importa un Markdown interactivo y reconstruye la estructura canónica de       │
│                    Deckard.                                                                      │
│ web                Genera páginas Web estáticas o MyST Markdown con soluciones desplegables.     │
│ anki               Exporta ejercicios y firmas a tarjetas mnemotécnicas Anki / Flashcards en     │
│                    formato TSV.                                                                  │
│ moodle             Exporta ejercicios a formato Moodle XML para cuestionarios virtuales.         │
│ bundle-offline     Empaqueta guías y ejercicios en un bundle portable ZIP con visor web HTML/CSS │
│                    100% offline.                                                                 │
│ myst               Genera el sitio MyST del banco: una página por ejercicio y por guía, portada, │
│                    grafo temático, TOC, .ripkg y catálogo JSON.                                  │
│ apunte             Escribe en las páginas del apunte el bloque «Ejercicios para practicar» de    │
│                    sus temas.                                                                    │
│ templates          Gestión y personalización de plantillas y CSS para exportación.               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export pack`

```text
 Uso: deckard export pack [OPCIONES] {objetivo}

 Empaqueta ejercicios o guías como .ripkg para Ripley y starter repos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    objetivo      <str>  Id del ejercicio en el banco, o ruta a guia.yaml / carpeta de guía /   │
│                           carpeta de ejercicio.                                                  │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco             <path>  Directorio del banco de ejercicios. [por defecto: banco]             │
│ --salida    -o      <path>  Archivo .ripkg o directorio de salida.                               │
│ --sign-key          <str>   Clave GPG para firmar el paquete.                                    │
│ --starter                   Generar también estructura starter repo para GitHub Classroom.       │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export unpack`

```text
 Uso: deckard export unpack [OPCIONES] {paquete}

 Extrae un bundle .deckard.tar.gz en el banco o directorio especificado.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    paquete      <path>  Ruta al archivo .deckard.tar.gz o .tar.gz a desempaquetar.             │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --destino  -d      <path>  Directorio destino donde extraer los ejercicios. [por defecto: banco] │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export publish-classroom`

```text
 Uso: deckard export publish-classroom [OPCIONES] {ejercicio_id}

 Genera la estructura completa de un repositorio para GitHub Classroom (README, starter code,
 Makefile, CI).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio a exportar como asignación. [obligatorio]         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Directorio de salida para la asignación.                               │
│                           [por defecto: classroom_assignments]                                   │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --repo    -r      <str>   Nombre personalizado para el repositorio.                              │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export classroom`

```text
 Uso: deckard export classroom [OPCIONES] {ejercicio_id}

 Genera la estructura completa de un repositorio para GitHub Classroom (README, starter code,
 Makefile, CI).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio a exportar como asignación. [obligatorio]         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Directorio de salida para la asignación.                               │
│                           [por defecto: classroom_assignments]                                   │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --repo    -r      <str>   Nombre personalizado para el repositorio.                              │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export notebook`

```text
 Uso: deckard export notebook [OPCIONES] {ejercicio_id}

 Exporta un ejercicio en formato interactivo Jupyter Notebook (.ipynb) con kernel C.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio o ruta al directorio del ejercicio. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del archivo .ipynb.                                    │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export pack-zip`

```text
 Uso: deckard export pack-zip [OPCIONES] {objetivo}

 Empaqueta un starter kit o guía completa en un archivo ZIP con clave de entrega (QoL 11).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    objetivo      <str>  ID de ejercicio, ruta a ejercicio.yaml o guía .yaml. [obligatorio]     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida     -o      <path>  Ruta de destino del archivo .zip.                                   │
│ --banco      -b      <path>  Directorio raíz del banco. [por defecto: banco]                     │
│ --no-tests                   Excluir archivos de prueba en el starter kit.                       │
│ --no-pistas                  Excluir pistas en el starter kit.                                   │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export hints`

```text
 Uso: deckard export hints [OPCIONES] {ejercicio_id}

 Exporta o genera pistas escalonadas (Hints) progresivas para un ejercicio (QoL 15).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio o ruta a ejercicio.yaml. [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida           -o      <path>  Ruta de salida (por defecto stdout o PISTAS.md).              │
│ --banco            -b      <path>  Directorio raíz del banco. [por defecto: banco]               │
│ --ofuscar,--rot13                  Ofuscar las pistas con ROT13 para prevenir spoilers.          │
│ --c-comments       -c              Generar en formato de bloque de comentarios C.                │
│ --nivel            -n      <int>   Nivel máximo de pistas a exportar.                            │
│ --help             -h              Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export to-md`

```text
 Uso: deckard export to-md [OPCIONES] {ejercicio_id}

 Convierte un ejercicio estructurado en un único Markdown interactivo con YAML frontmatter.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio o ruta. [obligatorio]                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Ruta de salida del archivo .md interactivo.                            │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export from-md`

```text
 Uso: deckard export from-md [OPCIONES] {archivo_md}

 Importa un Markdown interactivo y reconstruye la estructura canónica de Deckard.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo_md      <path>  Ruta al archivo Markdown interactivo con frontmatter. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --destino  -d      <path>  Directorio destino del banco. [por defecto: banco]                    │
│ --force                    Sobrescribir directorio si ya existe.                                 │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export web`

```text
 Uso: deckard export web [OPCIONES] {target}

 Genera páginas Web estáticas o MyST Markdown con soluciones desplegables.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio, 'all' o ruta a archivo de guía YAML. [obligatorio]      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Directorio destino del sitio web. [por defecto: dist/web]              │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --myst                    Generar formato MyST Markdown en lugar de HTML.                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export anki`

```text
 Uso: deckard export anki [OPCIONES] {target}

 Exporta ejercicios y firmas a tarjetas mnemotécnicas Anki / Flashcards en formato TSV.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio, 'all' o ruta a guía YAML. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Ruta de exportación TSV. [por defecto: dist/flashcards.tsv]            │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export moodle`

```text
 Uso: deckard export moodle [OPCIONES] {target}

 Exporta ejercicios a formato Moodle XML para cuestionarios virtuales.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio o ruta a guía YAML. [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --salida     -o      <path>  Ruta del archivo XML Moodle generado. [obligatorio]              │
│    --categoria  -c      <str>   Categoría para agrupar preguntas.                                │
│    --tipo       -t      <str>   Tipo de pregunta: 'multichoice' o 'shortanswer'.                 │
│                                 [por defecto: multichoice]                                       │
│    --banco      -b      <path>  Directorio raíz del banco. [por defecto: banco]                  │
│    --help       -h              Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export bundle-offline`

```text
 Uso: deckard export bundle-offline [OPCIONES] {target}

 Empaqueta guías y ejercicios en un bundle portable ZIP con visor web HTML/CSS 100% offline.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  Ruta a guía YAML o directorio raíz del banco. [obligatorio]              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida              -o      <path>  Ruta del archivo ZIP generado.                             │
│                                       [por defecto: bundle_offline.zip]                          │
│ --titulo              -t      <str>   Título del visor web offline.                              │
│                                       [por defecto: Guía de Ejercicios Offline]                  │
│ --incluir-soluciones                  Incluir soluciones de referencia.                          │
│ --banco               -b      <path>  Directorio raíz del banco. [por defecto: banco]            │
│ --help                -h              Muestra esta ayuda y sale.                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export myst`

```text
 Uso: deckard export myst [OPCIONES]

 Genera el sitio MyST del banco: una página por ejercicio y por guía, portada, grafo temático, TOC,
 .ripkg y catálogo JSON.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                       <path>  Directorio raíz del banco. [por defecto: banco]            │
│ --guias                       <path>  Directorio de guías (las specs sin `ejercicios` se         │
│                                       saltean).                                                  │
│                                       [por defecto: guias]                                       │
│ --salida              -o      <path>  Directorio generado; se borra y regenera en cada corrida.  │
│                                       [por defecto: sitio]                                       │
│ --temas                       <path>  Títulos, unidades y prerrequisitos de los temas (por       │
│                                       omisión <banco>/../temas.yaml).                            │
│ --myst-yml                    <path>  myst.yml cuyo `project.toc` se reescribe; se omite si no   │
│                                       existe.                                                    │
│                                       [por defecto: myst.yml]                                    │
│ --sin-soluciones                      No incluir la solución modelo en las páginas.              │
│ --agrupar-unidades                    Agrupar el TOC por unidades en lugar de temas.             │
│ --sin-paquetes                        No generar los .ripkg ni el catálogo JSON.                 │
│ --permitir-invalidos                  Terminar bien aunque haya ejercicios inválidos (se omiten  │
│                                       del sitio).                                                │
│ --apunte                      <path>  Repositorio del apunte: da los slugs exactos de sus        │
│                                       páginas para los enlaces (sitios.apunte de temas.yaml).    │
│ --help                -h              Muestra esta ayuda y sale.                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export apunte`

```text
 Uso: deckard export apunte [OPCIONES] {apunte}

 Escribe en las páginas del apunte el bloque «Ejercicios para practicar» de sus temas.

 Las páginas salen del `apunte` de cada tema en temas.yaml; el bloque va entre las marcas
 `% deckard export apunte: inicio` y `…: fin` (se agrega al final la primera vez) y enlaza al
 sitio publicado de enunciados (`sitios.enunciados`). Los bloques de páginas que ya no figuran
 en temas.yaml se quitan.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    apunte      <directory>  Repositorio del apunte (con su myst.yml). [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco               <path>              Directorio raíz del banco. [por defecto: banco]        │
│ --temas               <path>              temas.yaml con `apunte` por tema y `sitios` (por       │
│                                           omisión <banco>/../temas.yaml).                        │
│ --ejercicios          <int range> [x>=0]  Ejercicios destacados por tema en cada bloque.         │
│                                           [por defecto: 5]                                       │
│ --verificar                               No escribir: salir con 1 si algún bloque está          │
│                                           desactualizado (para CI).                              │
│ --help        -h                          Muestra esta ayuda y sale.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard export templates`

```text
 Uso: deckard export templates [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestión y personalización de plantillas y CSS para exportación.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ init  Inicializa y copia las plantillas (HTML, Markdown y CSS) para personalizarlas.             │
│ list  Lista las plantillas disponibles (locales, globales y built-in).                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide`

```text
 Uso: deckard guide [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestión, inspección y exportación de guías.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ list      Lista las guías existentes en guias/ con métricas y estado de verificación.            │
│ show      Muestra el detalle estructurado de una guía y sus ejercicios.                          │
│ new       Crea una nueva especificación de guía (GuiaSpec) en guias/.                            │
│ compose   Compone una guía balanceada por carga cognitiva y taxonomía de Bloom.                  │
│ add       Agrega un ejercicio del banco a una guía compuesta.                                    │
│ remove    Remueve un ejercicio de una guía compuesta.                                            │
│ verify    Verifica con ripley todas las soluciones modelo de los ejercicios de la guía.          │
│ pdf       Exporta la guía completa a PDF, Markdown o HTML.                                       │
│ export    Exporta la guía completa a PDF, Markdown o HTML.                                       │
│ practica  Crea la práctica desde la guía sobre plantilla-TP, con sus librerías y los targets del │
│           docente (Ola 30).                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide list`

```text
 Uso: deckard guide list [OPCIONES]

 Lista las guías existentes en guias/ con métricas y estado de verificación.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --guias  -g      <path>  Directorio de guías. [por defecto: guias]                               │
│ --banco          <path>  Directorio del banco. [por defecto: banco]                              │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide show`

```text
 Uso: deckard guide show [OPCIONES] {guia_archivo}

 Muestra el detalle estructurado de una guía y sus ejercicios.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>  Ruta o nombre del archivo YAML o carpeta de la guía. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco               <path>  Directorio del banco. [por defecto: banco]                         │
│ --guias               <path>  Directorio de guías. [por defecto: guias]                          │
│ --enunciados  -e              Mostrar enunciados completos.                                      │
│ --soluciones  -s              Mostrar soluciones modelo.                                         │
│ --pistas      -p              Mostrar pistas progresivas.                                        │
│ --help        -h              Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide new`

```text
 Uso: deckard guide new [OPCIONES] {archivo}

 Crea una nueva especificación de guía (GuiaSpec) en guias/.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo      <str>  Nombre del archivo YAML o carpeta (ej: 'guia_punteros.yaml' o           │
│                          'guia_punteros').                                                       │
│                          [obligatorio]                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --titulo          -t      <str>                  Título descriptivo de la guía. [obligatorio] │
│    --duracion        -d      <int>                  Duración estimada en minutos.                │
│                                                     [por defecto: 90]                            │
│    --margen          -m      <float>                Margen de carga (0.3 - 1.0).                 │
│                                                     [por defecto: 0.8]                           │
│    --temas                   <str>                  Temas separados por comas.                   │
│    --bloom-min               <int range> [1<=x<=5]  [por defecto: 1]                             │
│    --bloom-max               <int range> [1<=x<=5]  [por defecto: 5]                             │
│    --max-ejercicios  -n      <int>                                                               │
│    --guias                   <path>                 Directorio de guías. [por defecto: guias]    │
│    --help            -h                             Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide compose`

```text
 Uso: deckard guide compose [OPCIONES] {spec_file}

 Compone una guía balanceada por carga cognitiva y taxonomía de Bloom.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_file      <path>  guia.yaml con nombre/duración/temas. [obligatorio]                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide add`

```text
 Uso: deckard guide add [OPCIONES] {guia_archivo} {ejercicio_id}

 Agrega un ejercicio del banco a una guía compuesta.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>  Ruta o nombre del archivo/carpeta de la guía. [obligatorio]        │
│ *    ejercicio_id      <str>  ID del ejercicio a agregar. [obligatorio]                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio del banco. [por defecto: banco]                              │
│ --guias          <path>  Directorio de guías. [por defecto: guias]                               │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide remove`

```text
 Uso: deckard guide remove [OPCIONES] {guia_archivo} {ejercicio_id}

 Remueve un ejercicio de una guía compuesta.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>  Ruta o nombre del archivo/carpeta de la guía. [obligatorio]        │
│ *    ejercicio_id      <str>  ID del ejercicio a remover. [obligatorio]                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --guias          <path>  Directorio de guías. [por defecto: guias]                               │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide verify`

```text
 Uso: deckard guide verify [OPCIONES] {guia_archivo}

 Verifica con ripley todas las soluciones modelo de los ejercicios de la guía.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>  Ruta o nombre del archivo/carpeta de la guía. [obligatorio]        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           <path>  Directorio del banco. [por defecto: banco]                             │
│ --guias           <path>  Directorio de guías. [por defecto: guias]                              │
│ --ripley          <str>   Ruta a ripley.                                                         │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide pdf`

```text
 Uso: deckard guide pdf [OPCIONES] {guia_archivo}

 Exporta la guía completa a PDF, Markdown o HTML.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>  Ruta o nombre del archivo/carpeta de la guía. [obligatorio]        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --type         -t      <str>   Formatos de salida separados por comas: pdf, md, html (ej:        │
│                                --type=pdf,md).                                                   │
│                                [por defecto: pdf]                                                │
│ --banco                <path>  Directorio del banco. [por defecto: banco]                        │
│ --salida       -o      <path>  Archivo de salida o directorio destino.                           │
│ --template     -T      <str>   Plantilla personalizada.                                          │
│ --pipeline-md                  Generar Markdown intermedio antes de compilar PDF.                │
│ --soluciones   -s              Incluir apéndice de soluciones.                                   │
│ --pistas       -p              Incluir pistas progresivas.                                       │
│ --css                  <path>  Archivo CSS adicional.                                            │
│ --guias                <path>  Directorio de guías. [por defecto: guias]                         │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide export`

```text
 Uso: deckard guide export [OPCIONES] {guia_archivo}

 Exporta la guía completa a PDF, Markdown o HTML.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>  Ruta o nombre del archivo/carpeta de la guía. [obligatorio]        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --type         -t      <str>   Formatos de salida separados por comas: pdf, md, html (ej:        │
│                                --type=pdf,md).                                                   │
│                                [por defecto: pdf]                                                │
│ --banco                <path>  Directorio del banco. [por defecto: banco]                        │
│ --salida       -o      <path>  Archivo de salida o directorio destino.                           │
│ --template     -T      <str>   Plantilla personalizada.                                          │
│ --pipeline-md                  Generar Markdown intermedio antes de compilar PDF.                │
│ --soluciones   -s              Incluir apéndice de soluciones.                                   │
│ --pistas       -p              Incluir pistas progresivas.                                       │
│ --css                  <path>  Archivo CSS adicional.                                            │
│ --guias                <path>  Directorio de guías. [por defecto: guias]                         │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard guide practica`

```text
 Uso: deckard guide practica [OPCIONES] {guia_archivo} {destino}

 Crea la práctica desde la guía sobre plantilla-TP, con sus librerías y los targets del docente
 (Ola 30).

 Los ejercicios se llaman como en el banco y llevan enunciado, cabeceras, código inicial,
 prueba.c (p1_test) y los casos públicos (nunca la solución ni los casos ocultos). Del lado del
 docente quedan dredd.mk (targets dredd-…), sus fuentes y targets.json para dredd. Si la
 práctica ya existe, muestra qué cambiaría en vez de pisarla (con --aplicar, lo escribe).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia_archivo      <str>   Guía compuesta (guias/<guía>/guia.yaml o su nombre).              │
│                                [obligatorio]                                                     │
│ *    destino           <path>  Carpeta de la práctica a crear (o a comparar, si ya existe).      │
│                                [obligatorio]                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco              <path>  Directorio del banco. [por defecto: banco]                          │
│ --guias              <path>  Directorio de guías (para las librerías reutilizadas).              │
│                              [por defecto: guias]                                                │
│ --plantilla          <str>   plantilla-TP: una carpeta local o la URL del repositorio.           │
│                              [por defecto: https://github.com/INGCOM-UNRN-P1/plantilla-TP]       │
│ --dredd              <path>  Dónde dejar dredd.mk y targets.json (por omisión, <destino>-dredd). │
│ --aplicar                    Si la práctica ya existe, escribir lo agregado y lo cambiado.       │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec`

```text
 Uso: deckard spec [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestión, validación y composición de especificaciones de guías (GuiaSpec).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ list      Lista todas las especificaciones de guías (GuiaSpec) disponibles.                      │
│ new       Crea una nueva especificación de guía (GuiaSpec).                                      │
│ show      Muestra los detalles de una especificación y su universo de ejercicios candidatos en   │
│           el banco.                                                                              │
│ validate  Verifica si el banco de ejercicios tiene suficientes candidatos para satisfacer el     │
│           spec.                                                                                  │
│ edit      Modifica parámetros de una especificación existente.                                   │
│ compose   Compone una guía a partir de esta especificación.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec list`

```text
 Uso: deckard spec list [OPCIONES]

 Lista todas las especificaciones de guías (GuiaSpec) disponibles.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --guias  -g      <path>  Directorio donde se ubican los specs. [por defecto: guias]              │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec new`

```text
 Uso: deckard spec new [OPCIONES] {archivo}

 Crea una nueva especificación de guía (GuiaSpec).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo      <str>  Nombre del archivo (ej: 'guia_parcial1.yaml'). [obligatorio]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --titulo          -t      <str>                  Título pedagógico de la especificación.      │
│                                                     [obligatorio]                                │
│    --duracion        -d      <int>                  Duración estimada total en minutos.          │
│                                                     [por defecto: 90]                            │
│    --margen          -m      <float>                Margen de carga útil (0.1 a 1.0).            │
│                                                     [por defecto: 0.8]                           │
│    --temas                   <str>                  Temas obligatorios separados por comas.      │
│    --bloom-min               <int range> [1<=x<=5]  [por defecto: 1]                             │
│    --bloom-max               <int range> [1<=x<=5]  [por defecto: 5]                             │
│    --max-ejercicios  -n      <int>                                                               │
│    --guias           -g      <path>                 [por defecto: guias]                         │
│    --help            -h                             Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec show`

```text
 Uso: deckard spec show [OPCIONES] {spec_archivo}

 Muestra los detalles de una especificación y su universo de ejercicios candidatos en el banco.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_archivo      <str>  Ruta o nombre del archivo spec YAML. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --guias          <path>  Directorio de guías. [por defecto: guias]                               │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec validate`

```text
 Uso: deckard spec validate [OPCIONES] {spec_archivo}

 Verifica si el banco de ejercicios tiene suficientes candidatos para satisfacer el spec.

 También revisa las librerías declaradas (que una reutilizada exista en su guía anterior) y,
 con --remoto, avisa de las librerías de la cátedra fijadas a un commit viejo.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_archivo      <str>  Ruta o nombre del archivo spec YAML. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --guias           <path>  Directorio de guías. [por defecto: guias]                              │
│ --remoto                  Consultar con git si las librerías de la cátedra están en su último    │
│                           commit.                                                                │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec edit`

```text
 Uso: deckard spec edit [OPCIONES] {spec_archivo}

 Modifica parámetros de una especificación existente.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_archivo      <str>  Ruta o nombre del archivo spec YAML. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --titulo          -t      <str>                                                                  │
│ --duracion        -d      <int>                                                                  │
│ --margen          -m      <float>                                                                │
│ --temas                   <str>                                                                  │
│ --bloom-min               <int range> [1<=x<=5]                                                  │
│ --bloom-max               <int range> [1<=x<=5]                                                  │
│ --max-ejercicios  -n      <int>                                                                  │
│ --guias                   <path>                 [por defecto: guias]                            │
│ --help            -h                             Muestra esta ayuda y sale.                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard spec compose`

```text
 Uso: deckard spec compose [OPCIONES] {spec_archivo}

 Compone una guía a partir de esta especificación.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    spec_archivo      <str>  Ruta o nombre del archivo spec YAML. [obligatorio]                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco          <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --guias          <path>  Directorio de guías. [por defecto: guias]                               │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve`

```text
 Uso: deckard improve [OPCIONES] COMANDO [ARGUMENTOS]...

 Mejora y curaduría pedagógica de consignas y bancos de ejercicios con IA (Gemini, servidor local,
 OpenCode o Claude).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ clarity     Mejora la claridad, concisión y desambiguación del enunciado con verbos operativos   │
│             de Bloom.                                                                            │
│ edge-cases  Especifica exhaustivamente casos borde, precondiciones y postcondiciones según el    │
│             tema.                                                                                │
│ examples    Enriquece la consigna con ejemplos de entrada/salida (I/O) claros y trazas de        │
│             ejecución.                                                                           │
│ hints       Genera o mejora pistas pedagógicas progresivas de 3 niveles sin revelar la solución. │
│ bloom       Alinea la exigencia y rigor de la consigna con su nivel asignado de la taxonomía de  │
│             Bloom.                                                                               │
│ testcases   Diseña casos de prueba rigurosos (.in/.out y tests de función) cubriendo casos       │
│             típicos y borde.                                                                     │
│ starter     Genera o perfecciona el código esqueleto inicial (starter_code) y cabeceras .h con   │
│             Doxygen.                                                                             │
│ all         Mejora integral y holística de todos los aspectos de la consigna en una única        │
│             pasada.                                                                              │
│ models      Lista los modelos de lenguaje que ofrece el proveedor de IA configurado.             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve clarity`

```text
 Uso: deckard improve clarity [OPCIONES] [target]

 Mejora la claridad, concisión y desambiguación del enunciado con verbos operativos de Bloom.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve edge-cases`

```text
 Uso: deckard improve edge-cases [OPCIONES] [target]

 Especifica exhaustivamente casos borde, precondiciones y postcondiciones según el tema.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve examples`

```text
 Uso: deckard improve examples [OPCIONES] [target]

 Enriquece la consigna con ejemplos de entrada/salida (I/O) claros y trazas de ejecución.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve hints`

```text
 Uso: deckard improve hints [OPCIONES] [target]

 Genera o mejora pistas pedagógicas progresivas de 3 niveles sin revelar la solución.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve bloom`

```text
 Uso: deckard improve bloom [OPCIONES] [target]

 Alinea la exigencia y rigor de la consigna con su nivel asignado de la taxonomía de Bloom.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve testcases`

```text
 Uso: deckard improve testcases [OPCIONES] [target]

 Diseña casos de prueba rigurosos (.in/.out y tests de función) cubriendo casos típicos y borde.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve starter`

```text
 Uso: deckard improve starter [OPCIONES] [target]

 Genera o perfecciona el código esqueleto inicial (starter_code) y cabeceras .h con Doxygen.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve all`

```text
 Uso: deckard improve all [OPCIONES] [target]

 Mejora integral y holística de todos los aspectos de la consigna en una única pasada.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   target      <str>  ID de ejercicio, ruta a directorio, banco o archivo .gift.                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                 -b                  <path>  Directorio raíz del banco de ejercicios.     │
│                                                     [por defecto: .]                             │
│ --prompt                -p                  <str>   Instrucciones adicionales para ajustar el    │
│                                                     prompt.                                      │
│ --prompt-file           -P                  <path>  Archivo con directivas personalizadas.       │
│ --model                 -m                  <str>   Modelo (por defecto, el configurado para el  │
│                                                     proveedor; con opencode,                     │
│                                                     opencode-go/qwen3.8-max).                    │
│ --proveedor,--provider                      <str>   Proveedor de IA: google, local, opencode o   │
│                                                     claude (por defecto: P1_IA_PROVEEDOR,        │
│                                                     ~/.config/p1/ia.toml u opencode).            │
│ --apply                 -a                          Aplica y guarda los cambios en los archivos. │
│ --diff                  -d  --no-diff               Muestra diff unificado de los cambios.       │
│                                                     [por defecto: diff]                          │
│ --show-prompt                                       Imprime el prompt generado sin consultar al  │
│                                                     modelo.                                      │
│ --sandbox                   --no-sandbox            Usa ejecución aislada bwrap si está          │
│                                                     disponible.                                  │
│                                                     [por defecto: sandbox]                       │
│ --all                                               Procesar todos los ejercicios del banco.     │
│ --patron                                    <str>   Filtro comodín para IDs de ejercicios.       │
│ --tema                                      <str>   Filtra por tema pedagógico.                  │
│ --bloom                                     <int>   Filtra por nivel de Bloom (1-5).             │
│ --tag                                       <str>   Filtra por etiqueta.                         │
│ --output                -o                  <path>  Ruta de exportación alternativa.             │
│ --help                  -h                          Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard improve models`

```text
 Uso: deckard improve models [OPCIONES] [provider]

 Lista los modelos de lenguaje que ofrece el proveedor de IA configurado.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   provider      <str>  Prefijo opcional para filtrar modelos (ej: opencode-go).                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --proveedor          <str>  Proveedor de IA a consultar: google, local, opencode o claude (por   │
│                             defecto, el configurado u opencode).                                 │
│ --raw        -r             Imprimir únicamente la lista plana de identificadores de modelos.    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality`

```text
 Uso: deckard quality [OPCIONES] COMANDO [ARGUMENTOS]...

 Calidad de consignas y bancos: terminología, tono, ambigüedad, ortografía, duplicados.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ load          Audita la carga horaria acumulada y el balance Bloom de una guía.                  │
│ guide         Audita la completitud y calidad técnica de todos los ejercicios de una guía.       │
│ languagetool  Verifica y corrige ortografía y gramática en enunciados y pistas de ejercicios     │
│               usando LanguageTool.                                                               │
│ grammar       Verifica y corrige ortografía y gramática en enunciados y pistas de ejercicios     │
│               usando LanguageTool.                                                               │
│ spellcheck    Verifica y corrige ortografía y gramática en enunciados y pistas de ejercicios     │
│               usando LanguageTool.                                                               │
│ statements    Audita ambigüedades, términos vagos y calidad pedagógica en los enunciados (QoL    │
│               12).                                                                               │
│ ambiguity     Audita ambigüedades, términos vagos y calidad pedagógica en los enunciados (QoL    │
│               12).                                                                               │
│ terms         Verifica la consistencia terminológica de consignas y detecta términos no válidos  │
│               en C.                                                                              │
│ duplicates    Detecta redundancias y ejercicios duplicados en el banco según similitud léxica y  │
│               estructural.                                                                       │
│ consigna      Linter pedagógico de precondiciones y casos borde en consignas (NULL, vector       │
│               vacío, archivos).                                                                  │
│ tone          Audita ambigüedades lingüísticas, dobles negaciones y consistencia de tono en      │
│               consignas.                                                                         │
│ checklist     Genera listas de autoevaluación previas a la entrega en formato Markdown.          │
│ signatures    Valida la consistencia de firmas de función entre el enunciado y la solución       │
│               canónica.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality load`

```text
 Uso: deckard quality load [OPCIONES] {guia}

 Audita la carga horaria acumulada y el balance Bloom de una guía.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia      <path>  Ruta a la guía YAML o spec a auditar. [obligatorio]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --max-horas  -m      <float>  Carga horaria pedagógica máxima sugerida en horas.                 │
│                               [por defecto: 6.0]                                                 │
│ --banco      -b      <path>   Directorio raíz del banco. [por defecto: banco]                    │
│ --help       -h               Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality guide`

```text
 Uso: deckard quality guide [OPCIONES] {guia}

 Audita la completitud y calidad técnica de todos los ejercicios de una guía.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia      <path>  Ruta a la guía YAML a auditar. [obligatorio]                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality languagetool`

```text
 Uso: deckard quality languagetool [OPCIONES] [objetivo]

 Verifica y corrige ortografía y gramática en enunciados y pistas de ejercicios usando
 LanguageTool.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   objetivo      <str>  ID de ejercicio, ruta a archivo .yaml o ruta a guía a revisar con         │
│                        LanguageTool (por defecto todo el banco).                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           -b      <path>  Directorio raíz del banco de ejercicios. [por defecto: banco]  │
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
│ --md,--output-md  -o      <path>  Genera reporte en formato Markdown para el informe docente.    │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality grammar`

```text
 Uso: deckard quality grammar [OPCIONES] [objetivo]

 Verifica y corrige ortografía y gramática en enunciados y pistas de ejercicios usando
 LanguageTool.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   objetivo      <str>  ID de ejercicio, ruta a archivo .yaml o ruta a guía a revisar con         │
│                        LanguageTool (por defecto todo el banco).                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           -b      <path>  Directorio raíz del banco de ejercicios. [por defecto: banco]  │
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
│ --md,--output-md  -o      <path>  Genera reporte en formato Markdown para el informe docente.    │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality spellcheck`

```text
 Uso: deckard quality spellcheck [OPCIONES] [objetivo]

 Verifica y corrige ortografía y gramática en enunciados y pistas de ejercicios usando
 LanguageTool.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   objetivo      <str>  ID de ejercicio, ruta a archivo .yaml o ruta a guía a revisar con         │
│                        LanguageTool (por defecto todo el banco).                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           -b      <path>  Directorio raíz del banco de ejercicios. [por defecto: banco]  │
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
│ --md,--output-md  -o      <path>  Genera reporte en formato Markdown para el informe docente.    │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality statements`

```text
 Uso: deckard quality statements [OPCIONES] [objetivo]

 Audita ambigüedades, términos vagos y calidad pedagógica en los enunciados (QoL 12).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   objetivo      <str>  ID de ejercicio, ruta a archivo o guía a auditar.                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           -b      <path>  Directorio raíz del banco. [por defecto: banco]                │
│ --json                            Emitir reporte estructurado en formato JSON.                   │
│ --md,--output-md  -o      <path>  Generar reporte en Markdown.                                   │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality ambiguity`

```text
 Uso: deckard quality ambiguity [OPCIONES] [objetivo]

 Audita ambigüedades, términos vagos y calidad pedagógica en los enunciados (QoL 12).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   objetivo      <str>  ID de ejercicio, ruta a archivo o guía a auditar.                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           -b      <path>  Directorio raíz del banco. [por defecto: banco]                │
│ --json                            Emitir reporte estructurado en formato JSON.                   │
│ --md,--output-md  -o      <path>  Generar reporte en Markdown.                                   │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality terms`

```text
 Uso: deckard quality terms [OPCIONES] {target}

 Verifica la consistencia terminológica de consignas y detecta términos no válidos en C.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio o ruta a guía YAML o raíz del banco. [obligatorio]       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --preferencia  -p      <str>   Preferencia: 'vector' o 'arreglo'.                                │
│ --banco        -b      <path>  Directorio raíz del banco. [por defecto: banco]                   │
│ --help         -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality duplicates`

```text
 Uso: deckard quality duplicates [OPCIONES]

 Detecta redundancias y ejercicios duplicados en el banco según similitud léxica y estructural.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco           -b      <path>   Directorio raíz del banco. [por defecto: banco]               │
│ --umbral          -u      <float>  Umbral mínimo de similitud (0.0 a 1.0). [por defecto: 0.7]    │
│ --sin-soluciones                   Omitir comparación de soluciones.                             │
│ --help            -h               Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality consigna`

```text
 Uso: deckard quality consigna [OPCIONES] {target}

 Linter pedagógico de precondiciones y casos borde en consignas (NULL, vector vacío, archivos).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio, guía YAML o raíz del banco. [obligatorio]               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --estricto                  Modo estricto: eleva severidad de omisiones.                         │
│ --banco     -b      <path>  Directorio raíz del banco. [por defecto: banco]                      │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality tone`

```text
 Uso: deckard quality tone [OPCIONES] {target}

 Audita ambigüedades lingüísticas, dobles negaciones y consistencia de tono en consignas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio, guía YAML o raíz del banco. [obligatorio]               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality checklist`

```text
 Uso: deckard quality checklist [OPCIONES] {target}

 Genera listas de autoevaluación previas a la entrega en formato Markdown.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio o ruta a guía YAML. [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Ruta de archivo Markdown de salida.                                    │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard quality signatures`

```text
 Uso: deckard quality signatures [OPCIONES] {target}

 Valida la consistencia de firmas de función entre el enunciado y la solución canónica.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio, guía YAML o directorio del banco. [obligatorio]         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise`

```text
 Uso: deckard exercise [OPCIONES] COMANDO [ARGUMENTOS]...

 Crear y completar ejercicios: esqueletos, variantes, pruebas, rúbricas y diagramas.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ new              Crea un ejercicio nuevo con esqueleto de metadata, funciones, enunciado.md y    │
│                  solución.                                                                       │
│ compose-variant  Genera automáticamente una variante homóloga para recuperatorios respetando     │
│                  niveles Bloom.                                                                  │
│ variant          Genera automáticamente una variante homóloga para recuperatorios respetando     │
│                  niveles Bloom.                                                                  │
│ ascii-diagram    Genera diagramas y esquemas de estructuras de datos en formato ASCII, Mermaid o │
│                  PlantUML para enunciados (QoL 14).                                              │
│ diagram          Genera diagramas y esquemas de estructuras de datos en formato ASCII, Mermaid o │
│                  PlantUML para enunciados (QoL 14).                                              │
│ init-tests       Genera plantillas de tests unitarios embebidas en C utilizando p1_test o        │
│                  assert.                                                                         │
│ acsl-tests       Sintetiza casos de prueba a partir de contratos formales ACSL                   │
│                  (requires/ensures).                                                             │
│ rubric           Calibra pesos de evaluación y genera especificaciones de rúbricas para Dredd y  │
│                  Markdown.                                                                       │
│ init-io-files    Inicializa plantillas y fixtures para ejercicios basados en flujos de archivos. │
│ diagram-memory   Genera esquemas de memoria Stack/Heap con convenciones Bishop para enunciados.  │
│ scaffold         Genera plantillas de esqueletos de código con andamiaje pedagógico graduado.    │
│ failure-hints    Brinda orientación pedagógica y preguntas guía ante fallas en tests o           │
│                  ejecución.                                                                      │
│ cubrir           Genera tests/funciones/ (driver, especificaciones de tyrell y casos .in/.out)   │
│                  desde los prototipos                                                            │
│                  y la solución de la cátedra. Las especificaciones existentes se respetan:       │
│                  revisalas y volvé a correr.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise new`

```text
 Uso: deckard exercise new [OPCIONES] {eid}

 Crea un ejercicio nuevo con esqueleto de metadata, funciones, enunciado.md y solución.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    eid      <str>  Identificador corto (a-z0-9-). [obligatorio]                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --titulo           <str>                  [obligatorio]                                       │
│ *  --tema             <str>                  [obligatorio]                                       │
│    --bloom            <int range> [1<=x<=5]  [por defecto: 3]                                    │
│    --minutos          <int range> [x>=1]     [por defecto: 20]                                   │
│    --tags     -T      <str>                  Etiquetas separadas por comas (ej:                  │
│                                              'punteros,memoria,facil').                          │
│    --banco            <path>                 [por defecto: banco]                                │
│    --funcion  -F      <str>                  Firmas de funciones requeridas (ej: 'void           │
│                                              invertir_vector(int* vec, size_t n)').              │
│    --help     -h                             Muestra esta ayuda y sale.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise compose-variant`

```text
 Uso: deckard exercise compose-variant [OPCIONES] {guia}

 Genera automáticamente una variante homóloga para recuperatorios respetando niveles Bloom.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia      <path>  Ruta a la guía YAML original. [obligatorio]                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Ruta de la nueva guía variante.                                        │
│                           [por defecto: guias/guia_recuperatorio.yaml]                           │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --seed    -s      <int>   Semilla para selección pseudoaleatoria.                                │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise variant`

```text
 Uso: deckard exercise variant [OPCIONES] {guia}

 Genera automáticamente una variante homóloga para recuperatorios respetando niveles Bloom.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    guia      <path>  Ruta a la guía YAML original. [obligatorio]                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida  -o      <path>  Ruta de la nueva guía variante.                                        │
│                           [por defecto: guias/guia_recuperatorio.yaml]                           │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --seed    -s      <int>   Semilla para selección pseudoaleatoria.                                │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise ascii-diagram`

```text
 Uso: deckard exercise ascii-diagram [OPCIONES] [tipo]

 Genera diagramas y esquemas de estructuras de datos en formato ASCII, Mermaid o PlantUML para
 enunciados (QoL 14).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   tipo      <str>  Tipo de estructura: 'lista', 'lista-doble', 'arbol', 'matriz', 'pila',        │
│                    'cola', 'punteros'.                                                           │
│                    [por defecto: lista]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida    -o      <path>  Guardar el diagrama en un archivo.                                   │
│ --formato   -F      <str>   Formato del diagrama: 'ascii', 'mermaid', 'plantuml'.                │
│                             [por defecto: ascii]                                                 │
│ --filas     -f      <int>   Filas para matrices o punteros. [por defecto: 3]                     │
│ --columnas  -c      <int>   Columnas para matrices. [por defecto: 3]                             │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise diagram`

```text
 Uso: deckard exercise diagram [OPCIONES] [tipo]

 Genera diagramas y esquemas de estructuras de datos en formato ASCII, Mermaid o PlantUML para
 enunciados (QoL 14).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   tipo      <str>  Tipo de estructura: 'lista', 'lista-doble', 'arbol', 'matriz', 'pila',        │
│                    'cola', 'punteros'.                                                           │
│                    [por defecto: lista]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida    -o      <path>  Guardar el diagrama en un archivo.                                   │
│ --formato   -F      <str>   Formato del diagrama: 'ascii', 'mermaid', 'plantuml'.                │
│                             [por defecto: ascii]                                                 │
│ --filas     -f      <int>   Filas para matrices o punteros. [por defecto: 3]                     │
│ --columnas  -c      <int>   Columnas para matrices. [por defecto: 3]                             │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise init-tests`

```text
 Uso: deckard exercise init-tests [OPCIONES] {ejercicio_id}

 Genera plantillas de tests unitarios embebidas en C utilizando p1_test o assert.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio o ruta al directorio del ejercicio. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco      -b      <path>  Directorio raíz del banco. [por defecto: banco]                     │
│ --framework  -f      <str>   Framework de aserciones: 'p1_test' o 'assert'.                      │
│                              [por defecto: p1_test]                                              │
│ --force                      Sobrescribir archivos existentes.                                   │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise acsl-tests`

```text
 Uso: deckard exercise acsl-tests [OPCIONES] {ejercicio_id}

 Sintetiza casos de prueba a partir de contratos formales ACSL (requires/ensures).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID de ejercicio o directorio. [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --apply  -a              Guardar los tests sintetizados en ejercicio.yaml.                       │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise rubric`

```text
 Uso: deckard exercise rubric [OPCIONES] {target}

 Calibra pesos de evaluación y genera especificaciones de rúbricas para Dredd y Markdown.

 Con `--eval-results`, además, califica: aplica la rúbrica a lo que evaluó dredd (la última
 revisión de cada estudiante) y escribe `calificaciones.csv` para importar en Moodle y una
 devolución en Markdown por estudiante.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <str>  ID de ejercicio o ruta a guía YAML. [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --md                    <path>  Ruta para exportar rúbrica en Markdown.                          │
│ --dredd                 <path>  Ruta para exportar configuración JSON para Dredd.                │
│ --pesos                 <str>   Ponderaciones clave=valor separadas por coma.                    │
│ --banco         -b      <path>  Directorio raíz del banco. [por defecto: banco]                  │
│ --eval-results          <path>  Resultados de dredd (directorio del curso, de un estudiante o un │
│                                 rNi/ con hallazgos.json y auditoria.json): calcula la nota 0–10  │
│                                 de cada estudiante.                                              │
│ --salida        -o      <path>  Con --eval-results: directorio para calificaciones.csv (Moodle)  │
│                                 y devoluciones/<alumno>.md.                                      │
│                                 [por defecto: calificaciones]                                    │
│ --help          -h              Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise init-io-files`

```text
 Uso: deckard exercise init-io-files [OPCIONES] {ejercicio_id}

 Inicializa plantillas y fixtures para ejercicios basados en flujos de archivos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio. [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --modo   -m      <str>   Tipo de archivo: 'binario' o 'texto'/'csv'. [por defecto: binario]      │
│ --banco  -b      <path>  Directorio raíz del banco. [por defecto: banco]                         │
│ --help   -h              Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise diagram-memory`

```text
 Uso: deckard exercise diagram-memory [OPCIONES] {ejercicio_id}

 Genera esquemas de memoria Stack/Heap con convenciones Bishop para enunciados.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio. [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --formato  -f      <str>   Formato de salida: 'ascii' o 'mermaid'. [por defecto: ascii]          │
│ --salida   -o      <path>  Ruta de archivo para guardar el esquema.                              │
│ --banco    -b      <path>  Directorio raíz del banco. [por defecto: banco]                       │
│ --help     -h              Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise scaffold`

```text
 Uso: deckard exercise scaffold [OPCIONES] {ejercicio_id}

 Genera plantillas de esqueletos de código con andamiaje pedagógico graduado.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicio_id      <str>  ID del ejercicio. [obligatorio]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --steps                   Generar andamiaje guiado con 4 pasos metodológicos TODO.               │
│ --salida  -o      <path>  Ruta del archivo C de salida.                                          │
│ --banco   -b      <path>  Directorio raíz del banco. [por defecto: banco]                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise failure-hints`

```text
 Uso: deckard exercise failure-hints [OPCIONES] {codigo_o_error}

 Brinda orientación pedagógica y preguntas guía ante fallas en tests o ejecución.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    codigo_o_error      <str>  Código de falla, señal o assert (ej: SIGSEGV, SIGABRT,           │
│                                 ASSERT_EQ).                                                      │
│                                 [obligatorio]                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `deckard exercise cubrir`

```text
 Uso: deckard exercise cubrir [OPCIONES] {ejercicios}...

 Genera tests/funciones/ (driver, especificaciones de tyrell y casos .in/.out) desde los prototipos
 y la solución de la cátedra. Las especificaciones existentes se respetan: revisalas y volvé a
 correr.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    ejercicios      <str>  Ids (o carpetas) de ejercicios de funciones del banco. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --banco                    <path>  Directorio raíz del banco (también organizado por tema).      │
│                                    [por defecto: banco]                                          │
│ --sin-cobertura                    Sólo la suite de la especificación (sin `tyrell cubrir`, que  │
│                                    necesita dietrich y gcov).                                    │
│ --regenerar-specs                  Volver a proponer las especificaciones de tyrell (pisa las    │
│                                    revisadas).                                                   │
│ --json                             Salida JSON.                                                  │
│ --help             -h              Muestra esta ayuda y sale.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`deckard@12430e1`](https://github.com/INGCOM-UNRN/deckard/tree/12430e1).
