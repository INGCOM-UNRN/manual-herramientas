---
title: "dredd"
---

<!-- Generado por scripts/generar_paginas.py desde dredd@f27c116: no editar a mano. -->

(manual-dredd)=
# dredd

Repositorio: [github.com/INGCOM-UNRN-P1/dredd](https://github.com/INGCOM-UNRN-P1/dredd).

Orquestador docente de evaluación masiva, autograding multicanal y gestión de entregas en C (compatible con **GitHub Classroom** y **Moodle**).

---

## Alcance

### Qué cubre
- Orquestación central de corrección masiva de trabajos prácticos y exámenes de programación en C.
- Ingesta y normalización de entregas provenientes de Moodle (ZIPs) y GitHub Classroom (repositorios Git).
- Calificación ponderada y gestión de base de datos relacional SQLite (`dredd.db`).
- Detección de plagio y copias entre estudiantes mediante algoritmo de huellas digitales de Winnowing.
- Re-evaluación incremental rápida (`dredd rerun --failed-only` y `--dry-run`).
- Generación de reportes de devolución individual en Markdown y actas consolidadas.

### Qué no cubre (Límites y Delegación)
- Compilación directa y traducción pedagógica de errores (delega prioritariamente en `daedalus` y `esper`, con fallback a GCC).
- Ejecución aislada de binarios: delega en `nostromo` o usa Bubblewrap propio, montando solo los
  directorios del sistema, el ejecutable y el workspace de la entrega (nunca el resto del disco).
  Si no hay ningún sandbox disponible la entrega **no se ejecuta**; para correrla solo con cuotas
  `setrlimit` y sin aislamiento de archivos hay que exportar `DREDD_PERMITIR_SIN_SANDBOX=1`.
- Linter de reglas de cátedra y estilo (delega en `gaff` y `ripley`, con fallback a linter nativo Tree-Sitter AST).
- Creación y multiplexación de guías de ejercicios (delega en `deckard`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Linux (nativo o WSL). Python >= 3.10.

### Dependencias Externas y Binarios
- `sqlite3`, `git`, y herramientas del ecosistema en PATH (`daedalus`, `nostromo`, `ripley`).

### Integración en el Ecosistema
- CLI `dredd`. Hub central de calificación docente del ecosistema.

---

## Instalación y Entorno

Dredd está desarrollado en Python 3.11+ con `typer` y `rich`.

```bash
# Instalación en modo desarrollo
cd dredd
uv sync                      # incluye el grupo de desarrollo (pytest)

# Ver catálogo de comandos
uv run dredd --help
```

---

## Flujos de Trabajo y Comandos

### 1. Flujo GitHub Classroom

#### Evaluación de Entregas (`dredd eval`)
Clona o actualiza el repositorio en `<actividad>-submissions/<estudiante>/`, ejecuta el análisis con el motor Ripley (o fallback nativo con reglas P1 de cátedra) y ensambla `${estudiante}.md`:

```bash
# Evaluar un estudiante puntual
dredd eval tp01 alvarez_juan

# Evaluar toda la cohorte presente en el workspace
dredd eval tp01 --all

# Limpiar evaluaciones previas (rNi/ o i_<hash>/ e informes generados)
dredd evaluate clean tp01
dredd evaluate clean tp01 alvarez_juan
dredd evaluate clean tp01 --dry-run   # Simulación sin borrar
```

Del `dredd.yaml` del workspace, la evaluación toma el encabezado y el pie de los informes
(`workspace.plantillas_dir`, `header.md` y `footer.md`; `--template-dir` los reemplaza) y
completa los ejercicios de la guía que no tienen `.ripkg` desde el banco de deckard
(`workspace.deckard_bank_dir`: `<banco>/<id>/ejercicio.yaml`, `solucion.c`, `tests/`).
`dredd config validate` lista los ejercicios que quedan sin casos de prueba de la cátedra.

El banco puede estar organizado por tema (`<banco>/<tema>/<id>/`): el ejercicio se busca por el
`id:` de su `ejercicio.yaml`. Un id genérico de una práctica (`ejercicio3`, `entrega_2`) no se busca
en el banco —ahí puede ser otro ejercicio—: se mapea en la regla de la actividad, o con `banco:` en
el ítem de la guía:

```yaml
- entrega: entrega_4
  guia: guias/entrega_4/guia.yaml
  ejercicios_banco:
    ejercicio1: ej-5-4-numeros-primos
```

Los ejercicios de funciones traen sus casos en `tests/funciones/` (los genera `deckard exercise
cubrir`): el archivo del alumno, con su `main` renombrado, se compila con el `driver.c` del
ejercicio, que llama a las funciones del enunciado con cada entrada. Así el `main` de cada alumno
no influye en el resultado; si falta una función o cambió su prototipo, el caso lo dice.

Una actividad que se corrige sin casos de la cátedra a propósito (una cohorte que resolvió otra
versión de la consigna) lleva `casos_catedra: false` en su regla: `config validate` lo informa y
deja de avisar.

#### Targets del docente (`dredd.mk`)

Una práctica creada con `deckard guide practica` trae, del lado del docente, una carpeta
`<práctica>-dredd/` con `dredd.mk`, las pruebas ocultas y `targets.json`. Con
`targets_docente: <esa carpeta>` en la regla de la actividad de `dredd.yaml`, la evaluación
copia `dredd.mk` y `.dredd/` en la entrega (los Makefiles de plantilla-TP los incluyen), compila
las librerías y corre cada `make dredd-…` en los ejercicios que declara; después los quita. En
el informe del alumno aparecen sólo los targets marcados como visibles (el detalle completo
queda en `rNi/targets_docente.json`), y sus pesos son porcentajes de la nota de pruebas en
`dredd export`. Si la entrega trae su propio `dredd.mk` o define un target `dredd-…` en un
Makefile o `local.mk`, se descarta y se informa. `dredd config validate` controla que cada
target de `targets.json` esté en el `dredd.mk`.

```yaml
mapeos:
- entrega: tp3
  source: github
  targets_docente: ../deckard/practicas/tp3-dredd
```

#### Publicación de Feedback en GitHub (`dredd comment`)
Envía automáticamente el informe `${estudiante}.md` como comentario en el Pull Request abierto del estudiante utilizando GitHub CLI (`gh`):

```bash
dredd comment tp01 alvarez_juan --open
```

#### Creación / Reparación de Pull Requests (`dredd pr-fix`)
Reconstruye o abre el Pull Request de corrección en caso de que el estudiante no lo haya generado o haya alterado las ramas base:

```bash
dredd pr-fix tp01 alvarez_juan
```

---

### 2. Flujo Moodle

#### Ingesta Masiva y Versionado (`dredd moodle ingest`)
Descomprime el ZIP masivo de Moodle, normaliza la codificación a UTF-8 (soportando CP1252, ISO-8859-1 y UTF-8-sig), aplana las carpetas y genera versiones deterministas (`r1`, `r2`, ...) mediante hash SHA-256 en `.metadata.db`:

```bash
dredd moodle ingest entregas_tp01.zip
```

#### Mapeo Interactivo de Archivos (`dredd map`)
Vincula heurísticamente o mediante interfaz interactiva los archivos fuente `.c` de los estudiantes con los testcases correspondientes, guardando las reglas en `mappings.json`:

```bash
dredd map tp01_1228009 -e ejercicio1 -e ejercicio2 --auto
```

#### Exportación de Calificaciones y Dashboard (`dredd export` / `dredd moodle export`)
Genera el archivo CSV compatible con el Libro de Calificaciones de Moodle, el ZIP de retroalimentación masiva para subir al aula virtual y el reporte `dashboard.md` con estadísticas de la cohorte:

```bash
# Exportación completa (CSV + ZIP + Dashboard)
dredd export tp01_1228009

# Exportación puntual de planilla CSV
dredd moodle export -e tp01 -o calificaciones.csv
```

#### Paquete para el calificador de Moodle (`dredd moodle paquete`)
Lleva a Moodle las notas de `deckard exercise rubric --eval-results` y sus devoluciones. Se parte de
la hoja de calificaciones de la tarea, porque Moodle busca sus encabezados y el identificador en el
idioma de la cuenta y el número de participante es interno de la tarea.

```bash
# 1. En la tarea de Moodle: Calificaciones → «Descargar hoja de calificaciones»
dredd moodle paquete --planilla Calificaciones.csv --notas calificaciones/calificaciones.csv \
    --mapa mapa.csv -o moodle/
# 2. En la tarea: «Subir hoja de calificaciones» (moodle/planilla_moodle.csv)
#    y «Subir múltiples archivos de retroalimentación en un ZIP» (moodle/devoluciones_moodle.zip)
```

- **Requisitos de la tarea:** tener activos «Hoja de calificaciones fuera de línea», «Comentarios de
  retroalimentación» y «Archivos de retroalimentación». Moodle desactiva la hoja si la tarea usa
  calificación avanzada (rúbrica o guía de Moodle).
- **`--mapa`:** CSV `alumno,dato`, con el identificador, el correo o el nombre en Moodle. Hace falta
  para las entregas de GitHub Classroom. Con una ingesta de Moodle, el número ya viene en la carpeta.
  Un estudiante sin coincidencia exacta queda afuera y el comando sale con 1.
- **Notas provisorias:** dejan la fila intacta, comentario incluido. `--incluir-provisorias` las suma.
- **Escala:** la nota de deckard es sobre 10 y se reescala a la calificación máxima de la tarea. Si la
  planilla no la trae, hay que indicarla con `--maximo`.
- **Volver a descargar:** Moodle ignora una fila si la nota cambió allá después de bajar la planilla.

---

### 3. Herramientas de Auditoría y Reportes

#### Detección de Plagio con Winnowing (`dredd plagiarism`)
Calcula la matriz de similitud de código fuente normalizado en todas las entregas descargadas utilizando el algoritmo Winnowing:

```bash
dredd plagiarism tp01_1228009                    # umbral de checks.plagiarism.threshold (dredd.yaml)
dredd plagiarism tp01_1228009 --threshold 0.70
dredd plagiarism tp01_1228009 --estructural --matriz matriz.csv
```

`--estructural` cruza cada par con la similitud del AST de `weyl cohort`, con la matriz completa en
CSV. Un par con AST alto y Winnowing bajo es el mismo programa con otro texto. Es un indicio para
mirar a mano: una consigna muy guiada también produce soluciones parecidas.

#### Encapsulamiento de TDAs (motoko)
En las actividades de TDAs dredd corre `motoko check --json` sobre cada ejercicio completado (o sobre la
entrega entera si no tiene ejercicios; motoko saltea `libs/`). Se activa con el tema de la actividad en
el mapeo (`tema: tad` o `modulos`, el vocabulario de los perfiles de ripley) o con `checks.motoko.enabled`:

```yaml
mapeos:
- entrega: TP5
  source: github
  tema: tad
```

El informe suma la sección «Calidad de abstracción (TDAs)»: qué TDAs son opacos, cada acceso a un campo
privado o struct privado copiado en el cliente, con la función pública que lo reemplaza. Sus hallazgos van a
`hallazgos.json` (categoría `tad`) y descuentan en el criterio `modularidad_y_diseño` de la rúbrica de deckard.

#### Conversión de Informes a HTML / PDF (`dredd export-report`)
Convierte informes Markdown a HTML enriquecido autocontenido (con CSS embebido) o PDF con formato de imprenta (el PDF se genera en Python puro). El Markdown se lee con `markdown-it-py` (CommonMark con tablas, la misma biblioteca que usa rich): negrita, código, enlaces (los del apunte en «Para repasar»), listas numeradas y `\|` dentro de una celda se conservan; las notas `> [!WARNING]` de las secciones se muestran como recuadros y los comentarios `<!-- dredd-section … -->` no aparecen. El HTML crudo del informe (por ejemplo un `<script>` en el código de una entrega) se muestra como texto, nunca se ejecuta, y un enlace `javascript:` no se convierte en enlace.

```bash
# Exportar a HTML
dredd export-report tp01_1228009/alvarez_juan/alvarez_juan.md --format html

# Exportar a PDF
dredd export-report tp01_1228009/alvarez_juan/alvarez_juan.md --format pdf
```

#### Diagnóstico del Entorno y Ecosistema (`dredd doctor`)
Verifica la disponibilidad y estado de todas las dependencias nativas y herramientas hermanas del ecosistema Cátedra P1:

```bash
dredd doctor
```

#### Re-evaluación Rápida y Filtrada (`dredd rerun`)
Re-ejecuta evaluaciones sobre entregas previas sin repetir descargas o clones innecesarios, filtrando únicamente entregas que hayan fallado:

```bash
dredd rerun tp01 --failed-only --dry-run
```

Las corridas masivas se pueden retomar: cada revisión deja en `rNi/auditoria.json` su estado
(`en_curso`, `completa` o `error`) y el resultado de la compilación y las pruebas. Si la corrida se
corta, `--resume` sigue donde quedó sin reevaluar lo terminado; `--failed-only` toma sólo las
entregas que fallaron o no terminaron:

```bash
dredd eval tp01 --all --resume
dredd eval tp01 --all --failed-only
```

#### Devolución con enlaces y errores de la cohorte (`dredd cluster-errors`)
Cada evaluación deja en `rNi/` un `hallazgos.json` con lo encontrado en la forma común del
ecosistema (`yutani.hallazgos`) y agrega al informe del estudiante la sección **Para repasar**:
los temas del apunte donde tuvo errores, con el enlace a la página y a cada regla.
`cluster-errors` junta los de todo el curso (la última revisión de cada estudiante) y muestra qué
errores y qué temas tuvo más gente: lo que conviene reforzar en clase.

```bash
dredd cluster-errors informes/tp01 --top 10
```

Con `--similitud` agrupa además las entregas que son el mismo programa salvo nombres,
comentarios, formato, prototipos u orden de las funciones. La medida es la de `weyl cohort`: la
bolsa de subárboles del AST de cada entrega, sin lo que comparte la mayoría de la cohorte. `--informe` escribe el informe docente con la matriz de
similitud de cada grupo, sin código de las entregas; `--matriz` escribe en CSV la matriz completa de
la cohorte; `--plantilla` descuenta el código que dio la cátedra. weyl viene con el extra
`ecosistema`. Con una versión de weyl sin `weyl cohort` se compara el texto normalizado, y sin weyl,
los tokens del detector de plagio de dredd: en esos dos casos no hay `--matriz`.

```bash
dredd cluster-errors informes/tp01 --similitud --umbral 90 --plantilla tp01/plantilla.c --informe similitud.md
```

#### Registro de auditoría para reclamos (`dredd audit-versions`)
Junto a cada revisión queda `auditoria.json`: fecha, commit evaluado y versión de dredd, de cada
satélite instalado y de gcc. `audit-versions` los lista y marca las entregas corregidas con
versiones distintas de las del resto del curso, para volver a correrlas con lo mismo.

```bash
dredd audit-versions informes/tp01 --alumno estudiante42
```

#### Exportación de Actas SIU Guaraní (`dredd export-guarani`)
Genera planillas tabulares compatibles con SIU Guaraní bajo codificación UTF-8-SIG y separadores punto y coma:

```bash
dredd export-guarani tp01 -o actas_tp01.csv
```

#### Multiplexación Docente de Prácticos (`dredd multiplex`)
Alias de conveniencia que delega en Deckard la generación de variantes combinatorias y asignación determinista por estudiante:

```bash
dredd multiplex --spec matriz.yaml -o dist/multiplex/
```

#### Auditoría de Repositorios y Makefiles
Comandos especializados para auditoría de commits de estudiantes y Makefiles:

```bash
dredd audit-git tp01 --json
dredd audit-makefile tp01 --json
dredd late-penalty tp01 --deadline 2026-09-20 --json
dredd typology tp01 --json
dredd eval-stability tp01 --runs 3 --json
```

---

## Arquitectura del Paquete

```
src/dredd/
├── __init__.py          # Metadatos del paquete (__version__)
├── cli.py               # Punto de entrada Typer y catálogo de comandos CLI
└── core/
    ├── ast_checker.py   # Linter nativo Tree-Sitter AST de reglas P1 (0xXXXXh)
    ├── baseline.py      # Detección de plantillas de base y omisión de ejercicios sin tocar
    ├── binary_check.py  # Detección y purga preventiva de binarios prohibidos
    ├── boiler_strip.py  # Limpieza de código boilerplate para comparaciones
    ├── cache.py         # Gestión de caché local
    ├── cohort_bench.py  # Métricas comparativas y benchmarking de la cohorte
    ├── compiler.py      # Orquestador de compilación C (Daedalus / Esper / GCC / Make)
    ├── config.py        # Configuración declarativa (dredd.yaml) y políticas de chequeo
    ├── dashboard.py     # Generación de tablero estadístico de rendimiento
    ├── db.py            # Persistencia relacional SQLite (.metadata.db)
    ├── diff_submission.py # Comparador diferencial entre entregas y revisiones
    ├── doctor.py        # Diagnóstico del entorno, dependencias y kernel namespaces
    ├── ecosystem.py     # Resolución unificada de herramientas y binarios hermanos
    ├── eval_clean.py    # Limpieza estructurada de carpetas de evaluación
    ├── exporter.py      # Exportación a planillas Moodle, ZIPs y métricas
    ├── feedback_pack.py # Ensamblador de paquetes de retroalimentación
    ├── feedback_template.py # Plantillas de feedback enriquecido
    ├── fuzz_gen.py      # Generador de inputs aleatorios deterministas y fuzzing
    ├── git_anomaly.py   # Auditoría de anomalías en commits de estudiantes
    ├── git_ops.py       # Gestión local de repositorios Git de entregas
    ├── github_api.py    # Integración con GitHub Classroom vía gh CLI
    ├── guarani.py       # Exportación de actas compatibles con SIU Guaraní
    ├── guide_integration.py # Adaptadores para guías docentes de Deckard
    ├── ingest.py        # Ingesta masiva de entregas multi-encoding (Moodle)
    ├── late_penalty.py  # Cálculo de penalizaciones por entregas fuera de término
    ├── makefile_audit.py # Auditoría estática de sintaxis y reglas de Makefiles
    ├── makefile_eval.py # Evaluación de proyectos con Makefiles por ejercicio
    ├── mapping.py       # Mapeo heurístico e interactivo entre entregas y guías
    ├── moodle.py        # Adaptadores y utilidades de ingesta/exportación Moodle
    ├── oral_guide.py    # Generador de preguntas conceptuales para defensas orales
    ├── output_sanitizer.py # Sanitizador de secuencias ANSI y volcados extensos
    ├── plagiarism.py    # Detector de plagio por algoritmo Winnowing
    ├── plagiarism_history.py # Comparación contra cohortes y cursadas previas
    ├── reformat.py      # Normalización a esquema canónico de revisiones rN/
    ├── report_export.py # Conversor de Markdown a HTML autocontenido y PDF
    ├── reporter.py      # Ensamblador modular de informes de devolución pedagógica
    ├── ripley_client.py # Cliente de integración con Ripley / Linter AST nativo
    ├── sandbox.py       # Aislamiento por namespaces (bwrap), setrlimit y evasión
    ├── smith_adversary.py # Evaluador adversarial de robustez
    ├── stability_eval.py # Auditoría de no-determinismo y estabilidad de pruebas
    ├── submission_typology.py # Clasificación tipológica de estilos de entrega
    └── valgrind.py      # Runner y parser de reportes XML de Valgrind
```

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Programas del sistema: `gcc`, `git`, `bwrap`.

| Sistema | `gcc` | `git` | `bwrap` |
|:--|:--|:--|:--|
| Debian / Ubuntu | `sudo apt install gcc` | `sudo apt install git` | `sudo apt install bubblewrap` |
| Fedora | `sudo dnf install gcc` | `sudo dnf install git` | `sudo dnf install bubblewrap` |
| Windows | incluido en el entorno de la cátedra (MSYS2 UCRT64) | incluido en el entorno de la cátedra (MSYS2 UCRT64) | no existe (solo Linux): usar WSL |
| macOS | `xcode-select --install` (clang como `gcc`) | `xcode-select --install` | no existe (solo Linux) |

### Comandos

| Comando | Descripción |
|:--|:--|
| `dredd init` | Inicializa un espacio de trabajo de Dredd con carpetas estructuradas y mapeo declarativo en dredd.yaml. |
| `dredd eval` | Clona/actualiza el repositorio o evalúa entregas locales, ejecuta el análisis con Ripley y genera el informe Markdown. |
| `dredd plagiarism` | Calcula la matriz de similitud Winnowing entre todas las entregas descargadas. |
| `dredd map` | Mapeo interactivo y heurístico entre archivos C de estudiantes y especificaciones de la guía. |
| `dredd export` | Exporta calificaciones CSV, paquete ZIP de retroalimentación y dashboard consolidado de cohorte. |
| `dredd export-report` | Convierte un informe Markdown (CommonMark con tablas) a HTML autocontenido o PDF. |
| `dredd fuzz-gen` | fuzz-gen: endurece el banco generando casos límite contra la solución modelo. |
| `dredd oral-guide` | oral-exam-companion: genera una guía de preguntas para coloquio/defensa. |
| `dredd multiplex` | Alias docente de conveniencia que delega la generación de variantes y asignación en Deckard. |
| `dredd doctor` | Verifica dependencias externas del sistema (GCC, Valgrind, Bubblewrap, Git, Ripley). |
| `dredd rerun` | Re-ejecuta la evaluación sobre entregas desaprobadas o con observaciones críticas. |
| `dredd export-guarani` | Exporta las calificaciones finales en formato estándar de actas de SIU Guaraní. |
| `dredd serve-dashboard`, `dredd dashboard` | Inicia un servidor web local para visualizar el dashboard de notas y plagio. |
| `dredd cohorte` | Planilla de seguimiento de una cohorte de Classroom: estado, observaciones frecuentes y tiempos (Ola 25). |
| `dredd audit-git` | Audita anomalías temporales y patrones de desarrollo en commits de Git. |
| `dredd git-forensics` | Audita marcas de tiempo en Git para detectar alteraciones manuales o rebase masivo previo a entrega. |
| `dredd notify-batch`, `dredd export-feedback` | Empaqueta y exporta los informes individuales alumno_rN.md en un lote consolidado con ZIP. |
| `dredd plagiarism-historical` | Detecta plagio cruzado inter-anual contra entregas históricas. |
| `dredd diff-revision`, `dredd diff-submission` | Compara dos versiones sucesivas de una entrega (R1 vs R2) mostrando cambios en código y funciones (QoL 3.15). |
| `dredd late-penalty` | Calcula la penalización gradual por entrega fuera de término. |
| `dredd audit-makefile` | Audita Makefiles en busca de dependencias prohibidas, flags suprimidas y trampas. |
| `dredd cluster-errors` | Errores y temas más frecuentes de la cohorte: cuántos estudiantes distintos tuvieron cada uno. |
| `dredd audit-versions` | Con qué versión de cada herramienta se corrigió cada entrega (para resolver reclamos). |
| `dredd typology` | Clasifica automáticamente la tipología arquitectónica de una entrega (monolítica, modular, librería, incompleta). |
| `dredd eval-stability` | Evalúa la estabilidad temporal y determinismo de una solución mediante corridas reiteradas. |
| `dredd cohort-bench` | Ejecuta benchmarking algorítmico comparativo de CPU y memoria en toda la cohorte. |
| `dredd smith-adversary` | Genera e inyecta casos de prueba adversarios y de estrés (integración smith). |
| `dredd eval-shielded` | Ejecuta un proceso bajo el modo 'Sandbox Blindado' con corte total de red y namespaces aislados. |
| `dredd report-template` | Renderiza o valida plantillas de feedback Markdown enriquecidas con variables contextuales. |
| `dredd sanitize-output` | Sanitiza flujos de salida o logs estudiantiles eliminando secuencias ANSI y truncando si excede el límite. |
| `dredd moodle` | Gestión de canales Moodle (ingesta ZIP y planillas). |
| `dredd github` | Comandos de integración con GitHub (clone, comment, pr-fix). |
| `dredd config` | Gestión de configuración, entregas, guías y políticas de chequeo. |
| `dredd evaluate` | Evaluación docente, autograding y limpieza de entregas. |
| `dredd deckard` | Integración con el banco de ejercicios de deckard. |

Ayuda de cada comando: `dredd <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `dredd eval`, `dredd doctor`, `dredd git-forensics`, `dredd diff-revision`, `dredd diff-submission`, `dredd late-penalty`, `dredd audit-makefile`, `dredd cluster-errors`, `dredd audit-versions`, `dredd typology`, `dredd eval-stability`, `dredd cohort-bench`, `dredd smith-adversary`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-dredd-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `dredd`
:open:

```text
 Uso: dredd [OPCIONES] COMANDO [ARGUMENTOS]...

 Orquestador docente de evaluación masiva y gestión de entregas (GitHub Classroom + Moodle).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión instalada de Dredd y finaliza.                │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ init                   Inicializa un espacio de trabajo de Dredd con carpetas estructuradas y    │
│                        mapeo declarativo en dredd.yaml.                                          │
│ eval                   Clona/actualiza el repositorio o evalúa entregas locales, ejecuta el      │
│                        análisis con Ripley y genera el informe Markdown.                         │
│ plagiarism             Calcula la matriz de similitud Winnowing entre todas las entregas         │
│                        descargadas.                                                              │
│ map                    Mapeo interactivo y heurístico entre archivos C de estudiantes y          │
│                        especificaciones de la guía.                                              │
│ export                 Exporta calificaciones CSV, paquete ZIP de retroalimentación y dashboard  │
│                        consolidado de cohorte.                                                   │
│ export-report          Convierte un informe Markdown (CommonMark con tablas) a HTML              │
│                        autocontenido o PDF.                                                      │
│ fuzz-gen               fuzz-gen: endurece el banco generando casos límite contra la solución     │
│                        modelo.                                                                   │
│ oral-guide             oral-exam-companion: genera una guía de preguntas para coloquio/defensa.  │
│ multiplex              Alias docente de conveniencia que delega la generación de variantes y     │
│                        asignación en Deckard.                                                    │
│ doctor                 Verifica dependencias externas del sistema (GCC, Valgrind, Bubblewrap,    │
│                        Git, Ripley).                                                             │
│ rerun                  Re-ejecuta la evaluación sobre entregas desaprobadas o con observaciones  │
│                        críticas.                                                                 │
│ export-guarani         Exporta las calificaciones finales en formato estándar de actas de SIU    │
│                        Guaraní.                                                                  │
│ serve-dashboard        Inicia un servidor web local para visualizar el dashboard de notas y      │
│                        plagio.                                                                   │
│ dashboard              Inicia un servidor web local para visualizar el dashboard de notas y      │
│                        plagio.                                                                   │
│ cohorte                Planilla de seguimiento de una cohorte de Classroom: estado,              │
│                        observaciones frecuentes y tiempos (Ola 25).                              │
│ audit-git              Audita anomalías temporales y patrones de desarrollo en commits de Git.   │
│ git-forensics          Audita marcas de tiempo en Git para detectar alteraciones manuales o      │
│                        rebase masivo previo a entrega.                                           │
│ notify-batch           Empaqueta y exporta los informes individuales alumno_rN.md en un lote     │
│                        consolidado con ZIP.                                                      │
│ export-feedback        Empaqueta y exporta los informes individuales alumno_rN.md en un lote     │
│                        consolidado con ZIP.                                                      │
│ plagiarism-historical  Detecta plagio cruzado inter-anual contra entregas históricas.            │
│ diff-revision          Compara dos versiones sucesivas de una entrega (R1 vs R2) mostrando       │
│                        cambios en código y funciones (QoL 3.15).                                 │
│ diff-submission        Compara dos versiones sucesivas de una entrega (R1 vs R2) mostrando       │
│                        cambios en código y funciones (QoL 3.15).                                 │
│ late-penalty           Calcula la penalización gradual por entrega fuera de término.             │
│ audit-makefile         Audita Makefiles en busca de dependencias prohibidas, flags suprimidas y  │
│                        trampas.                                                                  │
│ cluster-errors         Errores y temas más frecuentes de la cohorte: cuántos estudiantes         │
│                        distintos tuvieron cada uno.                                              │
│ audit-versions         Con qué versión de cada herramienta se corrigió cada entrega (para        │
│                        resolver reclamos).                                                       │
│ typology               Clasifica automáticamente la tipología arquitectónica de una entrega      │
│                        (monolítica, modular, librería, incompleta).                              │
│ eval-stability         Evalúa la estabilidad temporal y determinismo de una solución mediante    │
│                        corridas reiteradas.                                                      │
│ cohort-bench           Ejecuta benchmarking algorítmico comparativo de CPU y memoria en toda la  │
│                        cohorte.                                                                  │
│ smith-adversary        Genera e inyecta casos de prueba adversarios y de estrés (integración     │
│                        smith).                                                                   │
│ eval-shielded          Ejecuta un proceso bajo el modo 'Sandbox Blindado' con corte total de red │
│                        y namespaces aislados.                                                    │
│ report-template        Renderiza o valida plantillas de feedback Markdown enriquecidas con       │
│                        variables contextuales.                                                   │
│ sanitize-output        Sanitiza flujos de salida o logs estudiantiles eliminando secuencias ANSI │
│                        y truncando si excede el límite.                                          │
│ moodle                 Gestión de canales Moodle (ingesta ZIP y planillas).                      │
│ github                 Comandos de integración con GitHub (clone, comment, pr-fix).              │
│ config                 Gestión de configuración, entregas, guías y políticas de chequeo.         │
│ evaluate               Evaluación docente, autograding y limpieza de entregas.                   │
│ deckard                Integración con el banco de ejercicios de deckard.                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd init`

```text
 Uso: dredd init [OPCIONES] [path]

 Inicializa un espacio de trabajo de Dredd con carpetas estructuradas y mapeo declarativo en
 dredd.yaml.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   path      <path>  Directorio raíz donde inicializar el workspace de Dredd. [por defecto: .]    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --name      -n      <str>  Nombre del espacio de trabajo o materia.                              │
│                            [por defecto: Cátedra Programación 1]                                 │
│ --zips      -z      <str>  Directorio para almacenar los archivos ZIP de Moodle.                 │
│                            [por defecto: zips]                                                   │
│ --entregas  -e      <str>  Directorio para las entregas descompactadas. [por defecto: entregas]  │
│ --guias     -g      <str>  Directorio para las guías de Deckard. [por defecto: guias]            │
│ --force     -f             Sobrescribir dredd.yaml si ya existe.                                 │
│ --help      -h             Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd eval`

```text
 Uso: dredd eval [OPCIONES] {exercise} [student]

 Clona/actualiza el repositorio o evalúa entregas locales, ejecuta el análisis con Ripley y genera
 el informe Markdown.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    exercise      <str>  Nombre de la actividad / ejercicio o ruta al directorio de entregas    │
│                           (ej. tp01, ./entrega-3_1238305/).                                      │
│                           [obligatorio]                                                          │
│      student       <str>  Nombre de usuario del estudiante (opcional si se usa --all).           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --org                        -o      <str>   Organización de GitHub.                             │
│                                              [por defecto: INGCOM-UNRN-P1]                       │
│ --all                        -a              Evaluar todos los estudiantes presentes en el       │
│                                              workspace.                                          │
│ --template-dir               -t      <path>  Directorio con header.md y footer.md (por omisión,  │
│                                              plantillas_dir de dredd.yaml).                      │
│ --tipo-entrega,--build-mode  -m      <str>   Tipo de entrega / modo de construcción              │
│                                              ('archivos_individuales', 'makefiles_individuales'  │
│                                              o 'proyecto'). Hace override a dredd.yaml y         │
│                                              Deckard.                                            │
│ --dry-run                                    Modo Dry Run: evalúa únicamente una muestra de      │
│                                              hasta 3 estudiantes representativos antes del lote  │
│                                              completo.                                           │
│ --baseline                   -b      <path>  Directorio de línea base (_baseline) con las        │
│                                              plantillas originales para omitir ejercicios sin    │
│                                              completar.                                          │
│ --clean                      -c              Limpia directorios de evaluación (rNi) e informes   │
│                                              previos antes de volver a evaluar.                  │
│ --force                      -f              Fuerza la re-evaluación completa eliminando         │
│                                              resultados previos de las carpetas de estudiantes.  │
│ --json                                       Emite el resultado estructurado de la evaluación en │
│                                              formato JSON (máquina a máquina).                   │
│ --failed-only                                Evaluar sólo las entregas cuya última revisión no   │
│                                              terminó, no compiló o falló alguna prueba.          │
│ --resume                                     Retomar una corrida interrumpida: saltear las       │
│                                              revisiones que ya quedaron completas                │
│                                              (auditoria.json).                                   │
│ --workspace                  -w      <path>  Directorio raíz del workspace. [por defecto: .]     │
│ --help                       -h              Muestra esta ayuda y sale.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd plagiarism`

```text
 Uso: dredd plagiarism [OPCIONES] {exercise}

 Calcula la matriz de similitud Winnowing entre todas las entregas descargadas.

 Con `--estructural`, cruza cada par con la similitud del AST de weyl. Una similitud alta es un
 indicio para mirar a mano, no una prueba de copia.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    exercise      <str>  Nombre de la actividad o directorio de entregas a auditar.             │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --threshold           -th      <float>                        Umbral de similitud mínima (0.0 a  │
│                                                               1.0). Por omisión,                 │
│                                                               checks.plagiarism.threshold de     │
│                                                               dredd.yaml (0.60 sin él).          │
│ --strip-template               <path>                         boiler-strip: plantilla/archivo(s) │
│                                                               de cátedra a eliminar antes de     │
│                                                               calcular similitud.                │
│ --html                         <path>                         Ruta del reporte HTML interactivo  │
│                                                               con matriz y diff lado a lado.     │
│ --estructural                                                 Cruzar con la similitud del AST de │
│                                                               weyl: ve el mismo programa con     │
│                                                               otros nombres y otro orden.        │
│ --umbral-estructural           <float range> [0.0<=x<=100.0]  Similitud del AST (%) a partir de  │
│                                                               la cual se informa un par.         │
│                                                               [por defecto: 90.0]                │
│ --matriz                       <path>                         Con --estructural, escribir la     │
│                                                               matriz completa del AST en este    │
│                                                               CSV.                               │
│ --help                -h                                      Muestra esta ayuda y sale.         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd map`

```text
 Uso: dredd map [OPCIONES] {activity}

 Mapeo interactivo y heurístico entre archivos C de estudiantes y especificaciones de la guía.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    activity      <str>  Nombre / slug de la actividad o directorio de entregas a mapear (ej.   │
│                           tp01, ./entrega-3_1238305/).                                           │
│                           [obligatorio]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --exercise       -e      <str>  Nombres de los ejercicios disponibles (ej. -e ej1 -e ej2).       │
│ --unmapped-only  -u             Revisar únicamente archivos no vinculados.                       │
│ --auto           -a             Aplicar coincidencias heurísticas obvias automáticamente.        │
│ --help           -h             Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd export`

```text
 Uso: dredd export [OPCIONES] {activity}

 Exporta calificaciones CSV, paquete ZIP de retroalimentación y dashboard consolidado de cohorte.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    activity      <str>  Nombre / slug de la actividad a exportar. [obligatorio]                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --csv        -c      <path>  Ruta del CSV de calificaciones Moodle.                              │
│ --zip        -z      <path>  Ruta del ZIP de retroalimentación Moodle.                           │
│ --dashboard  -d      <path>  Ruta del dashboard Markdown.                                        │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd export-report`

```text
 Uso: dredd export-report [OPCIONES] {source}

 Convierte un informe Markdown (CommonMark con tablas) a HTML autocontenido o PDF.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      <path>  Ruta al archivo Markdown (.md) del informe. [obligatorio]               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --format  -f      <str>   Formato de exportación: 'html' o 'pdf'. [por defecto: html]            │
│ --output  -o      <path>  Ruta del archivo de salida.                                            │
│ --title   -t      <str>   Título del informe. [por defecto: Informe de Evaluación — Dredd]       │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd fuzz-gen`

```text
 Uso: dredd fuzz-gen [OPCIONES] {MODELO}

 fuzz-gen: endurece el banco generando casos límite contra la solución modelo.

 Combina semillas extremas deterministas (INT_MAX/INT_MIN, cadenas vacías,
 tamaños 0..N) con mutaciones y —si clang+libFuzzer están disponibles—
 fuzzing guiado por cobertura. Cada candidato se ejecuta contra el modelo
 para fijar la salida esperada; duplicados y crashes se reportan aparte.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    MODELO      <str>  Solución modelo de la cátedra (.c) o id de un ejercicio del banco de     │
│                         deckard.                                                                 │
│                         [obligatorio]                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida         -o      <path>  Directorio destino de los pares caso_NN.in/.out.                │
│                                  [por defecto: casos]                                            │
│ --spec                   <path>  spec.yaml opcional (tipo_entrada, semillas_extra, tamano_max).  │
│ --cantidad       -n      <int>   Máximo de casos de prueba a generar. [por defecto: 12]          │
│ --segundos               <int>   Tiempo de fuzzing si hay clang/libFuzzer. [por defecto: 15]     │
│ --sin-libfuzzer                  Fuerza el modo determinista.                                    │
│ --help           -h              Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd oral-guide`

```text
 Uso: dredd oral-guide [OPCIONES] {repo}

 oral-exam-companion: genera una guía de preguntas para coloquio/defensa.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    repo      <directory>  Repositorio del alumno (clonado en el workspace). [obligatorio]      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --alumno              <str>   Nombre legible del alumno.                                         │
│ --ejercicio           <str>   TP/parcial asociado.                                               │
│ --salida      -o      <path>  Archivo .md destino (por defecto, stdout).                         │
│ --sin-ripley                  No correr análisis técnico.                                        │
│ --help        -h              Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd multiplex`

```text
 Uso: dredd multiplex [OPCIONES]

 Alias docente de conveniencia que delega la generación de variantes y asignación en Deckard.

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

:::{dropdown} `dredd doctor`

```text
 Uso: dredd doctor [OPCIONES]

 Verifica dependencias externas del sistema (GCC, Valgrind, Bubblewrap, Git, Ripley).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir el diagnóstico como JSON (schema_version 1.0.0).                        │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd rerun`

```text
 Uso: dredd rerun [OPCIONES] {exercise} [student]

 Re-ejecuta la evaluación sobre entregas desaprobadas o con observaciones críticas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    exercise      <str>  Nombre de la actividad / ejercicio a re-evaluar. [obligatorio]         │
│      student       <str>  Nombre de usuario del estudiante específico a re-evaluar (opcional).   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --failed-only                    --all-rerun            Re-evaluar únicamente entregas           │
│                                                         desaprobadas o con fallos de             │
│                                                         compilación.                             │
│                                                         [por defecto: failed-only]               │
│ --tipo-entrega,--build-mode  -m                 <str>   Tipo de entrega / modo de construcción   │
│                                                         ('archivos_individuales',                │
│                                                         'makefiles_individuales' o 'proyecto').  │
│ --dry-run                                               Modo Dry Run: evalúa únicamente una      │
│                                                         muestra de hasta 3 estudiantes           │
│                                                         representativos.                         │
│ --workspace                  -w                 <path>  Directorio raíz del workspace.           │
│                                                         [por defecto: .]                         │
│ --help                       -h                         Muestra esta ayuda y sale.               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd export-guarani`

```text
 Uso: dredd export-guarani [OPCIONES] [entregas]

 Exporta las calificaciones finales en formato estándar de actas de SIU Guaraní.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   entregas      <path>  Directorio de entregas o base de datos de calificaciones.                │
│                         [por defecto: entregas]                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del CSV de SIU Guaraní.                                │
│                           [por defecto: acta_guarani.csv]                                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd serve-dashboard`

```text
 Uso: dredd serve-dashboard [OPCIONES]

 Inicia un servidor web local para visualizar el dashboard de notas y plagio.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --port      -p      <int>   Puerto HTTP para el servidor de dashboard local. [por defecto: 8000] │
│ --host      -H      <str>   Dirección IP o host local de escucha. [por defecto: 127.0.0.1]       │
│ --entregas  -e      <path>  Directorio con las entregas de los estudiantes para extraer notas.   │
│                             [por defecto: entregas]                                              │
│ --data      -d      <path>  Ruta a un archivo JSON con métricas precalculadas.                   │
│ --verbose   -v              Muestra información detallada de diagnóstico y registro de           │
│                             peticiones HTTP en consola.                                          │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd dashboard`

```text
 Uso: dredd dashboard [OPCIONES]

 Inicia un servidor web local para visualizar el dashboard de notas y plagio.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --port      -p      <int>   Puerto HTTP para el servidor de dashboard local. [por defecto: 8000] │
│ --host      -H      <str>   Dirección IP o host local de escucha. [por defecto: 127.0.0.1]       │
│ --entregas  -e      <path>  Directorio con las entregas de los estudiantes para extraer notas.   │
│                             [por defecto: entregas]                                              │
│ --data      -d      <path>  Ruta a un archivo JSON con métricas precalculadas.                   │
│ --verbose   -v              Muestra información detallada de diagnóstico y registro de           │
│                             peticiones HTTP en consola.                                          │
│ --help      -h              Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd cohorte`

```text
 Uso: dredd cohorte [OPCIONES] {carpeta}

 Planilla de seguimiento de una cohorte de Classroom: estado, observaciones frecuentes y tiempos
 (Ola 25).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    carpeta      <directory>  Carpeta con un repositorio clonado por alumno. [obligatorio]      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --salida        -o      <path>  Carpeta para cohorte.csv, cohorte.md y cohorte.json.             │
│                                 [por defecto: informe-cohorte]                                   │
│ --ruta                  <str>   Archivo o carpeta a verificar dentro de cada repositorio.        │
│                                 [por defecto: .]                                                 │
│ --perfil        -p      <str>   Perfil de ripley: strict, relaxed o exam. [por defecto: strict]  │
│ --prefijo               <str>   Prefijo de los repos de Classroom (tp1-): el resto es el usuario │
│                                 del alumno.                                                      │
│ --fecha-limite          <str>   Fecha límite ISO 8601 (2026-11-02T23:59-03:00) para calcular el  │
│                                 atraso.                                                          │
│ --help          -h              Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd audit-git`

```text
 Uso: dredd audit-git [OPCIONES] [repo]

 Audita anomalías temporales y patrones de desarrollo en commits de Git.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   repo      <path>  Ruta al repositorio de la entrega a auditar. [por defecto: .]                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd git-forensics`

```text
 Uso: dredd git-forensics [OPCIONES] [repo]

 Audita marcas de tiempo en Git para detectar alteraciones manuales o rebase masivo previo a
 entrega.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   repo      <path>  Ruta al repositorio de la entrega a auditar. [por defecto: .]                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --max-skew                 <int>  Tolerancia en segundos para desfase entre autor y committer.   │
│                                   [por defecto: 300]                                             │
│ --json                            Exporta el resultado en formato JSON estándar.                 │
│ --fail-on-anomaly                 Finaliza con código de error si el riesgo forense es ALTO.     │
│ --help             -h             Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd notify-batch`

```text
 Uso: dredd notify-batch [OPCIONES] [entregas]

 Empaqueta y exporta los informes individuales alumno_rN.md en un lote consolidado con ZIP.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   entregas      <path>  Directorio con las entregas de los estudiantes. [por defecto: entregas]  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Directorio de destino para los reportes. [por defecto: feedbacks_lote] │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd export-feedback`

```text
 Uso: dredd export-feedback [OPCIONES] [entregas]

 Empaqueta y exporta los informes individuales alumno_rN.md en un lote consolidado con ZIP.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   entregas      <path>  Directorio con las entregas de los estudiantes. [por defecto: entregas]  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Directorio de destino para los reportes. [por defecto: feedbacks_lote] │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd plagiarism-historical`

```text
 Uso: dredd plagiarism-historical [OPCIONES] {dir_actual} {dir_historico}

 Detecta plagio cruzado inter-anual contra entregas históricas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    dir_actual         <path>  Directorio de entregas del cuatrimestre actual. [obligatorio]    │
│ *    dir_historico      <path>  Directorio de entregas históricas de años previos. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --threshold  -t      <float>  Umbral de similitud mínima para alertar plagio. [por defecto: 0.7] │
│ --help       -h               Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd diff-revision`

```text
 Uso: dredd diff-revision [OPCIONES] {objetivo} [segunda_version]

 Compara dos versiones sucesivas de una entrega (R1 vs R2) mostrando cambios en código y funciones
 (QoL 3.15).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    objetivo             <str>  Ruta al directorio de la entrega o ruta a la primera versión    │
│                                  R1.                                                             │
│                                  [obligatorio]                                                   │
│      segunda_version      <str>  Ruta a la segunda versión R2 o nombre de revisión (ej. 'r2').   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --r1                      <str>   Nombre o subcarpeta de la primera revisión.                    │
│ --r2                      <str>   Nombre o subcarpeta de la segunda revisión.                    │
│ --entregas        -e      <path>  Directorio base de entregas si se pasa nombre de alumno.       │
│                                   [por defecto: entregas]                                        │
│ --json                            Emitir reporte de diff en formato JSON.                        │
│ --md,--output-md  -o      <path>  Exportar reporte de diff a archivo Markdown.                   │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd diff-submission`

```text
 Uso: dredd diff-submission [OPCIONES] {objetivo} [segunda_version]

 Compara dos versiones sucesivas de una entrega (R1 vs R2) mostrando cambios en código y funciones
 (QoL 3.15).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    objetivo             <str>  Ruta al directorio de la entrega o ruta a la primera versión    │
│                                  R1.                                                             │
│                                  [obligatorio]                                                   │
│      segunda_version      <str>  Ruta a la segunda versión R2 o nombre de revisión (ej. 'r2').   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --r1                      <str>   Nombre o subcarpeta de la primera revisión.                    │
│ --r2                      <str>   Nombre o subcarpeta de la segunda revisión.                    │
│ --entregas        -e      <path>  Directorio base de entregas si se pasa nombre de alumno.       │
│                                   [por defecto: entregas]                                        │
│ --json                            Emitir reporte de diff en formato JSON.                        │
│ --md,--output-md  -o      <path>  Exportar reporte de diff a archivo Markdown.                   │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd late-penalty`

```text
 Uso: dredd late-penalty [OPCIONES] {fecha_entrega} {fecha_limite}

 Calcula la penalización gradual por entrega fuera de término.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    fecha_entrega      <str>  Fecha y hora de entrega (ISO o 'YYYY-MM-DD HH:MM'). [obligatorio] │
│ *    fecha_limite       <str>  Fecha y hora límite de entrega (ISO o 'YYYY-MM-DD HH:MM').        │
│                                [obligatorio]                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --nota           -n      <float>  Calificación base antes de la penalización.                    │
│                                   [por defecto: 10.0]                                            │
│ --gracia         -g      <int>    Minutos de gracia sin penalización. [por defecto: 15]          │
│ --tasa           -t      <float>  Puntos de descuento por cada hora de retraso.                  │
│                                   [por defecto: 0.25]                                            │
│ --max-descuento  -m      <float>  Tope máximo de puntos de descuento. [por defecto: 4.0]         │
│ --json                            Emitir resultado en formato JSON.                              │
│ --help           -h               Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd audit-makefile`

```text
 Uso: dredd audit-makefile [OPCIONES] {objetivo}

 Audita Makefiles en busca de dependencias prohibidas, flags suprimidas y trampas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    objetivo      <path>  Ruta al archivo Makefile o al directorio de la entrega. [obligatorio] │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Salida en formato JSON.                                                        │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd cluster-errors`

```text
 Uso: dredd cluster-errors [OPCIONES] [raiz]

 Errores y temas más frecuentes de la cohorte: cuántos estudiantes distintos tuvieron cada uno.

 Con `--similitud`, además, los grupos de entregas estructuralmente equivalentes y su matriz de
 similitud (sin mostrar código).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   raiz      <directory>  Directorio con los informes del curso (busca rNi/hallazgos.json).       │
│                          [por defecto: .]                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --top        -n      <int>                          Cuántos errores mostrar. [por defecto: 15]   │
│ --json                                              Salida en formato JSON.                      │
│ --similitud                                         Agrupar además las entregas por similitud    │
│                                                     estructural (weyl similarity: mismo programa │
│                                                     salvo nombres, comentarios u orden).         │
│ --umbral             <float range> [0.0<=x<=100.0]  Similitud (%) a partir de la cual dos        │
│                                                     entregas van al mismo grupo.                 │
│                                                     [por defecto: 90.0]                          │
│ --plantilla          <path>                         Código de la cátedra (plantilla) a descontar │
│                                                     antes de comparar.                           │
│ --informe            <path>                         Escribir el informe docente de similitud en  │
│                                                     Markdown (grupos y matriz, sin código).      │
│ --matriz             <path>                         Escribir en este CSV la matriz completa de   │
│                                                     la cohorte (necesita weyl con `weyl          │
│                                                     cohort`).                                    │
│ --help       -h                                     Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd audit-versions`

```text
 Uso: dredd audit-versions [OPCIONES] [raiz]

 Con qué versión de cada herramienta se corrigió cada entrega (para resolver reclamos).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   raiz      <directory>  Directorio con los informes (busca rNi/auditoria.json).                 │
│                          [por defecto: .]                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --alumno  -a      <str>  Solo las revisiones de este estudiante.                                 │
│ --json                   Salida en formato JSON.                                                 │
│ --help    -h             Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd typology`

```text
 Uso: dredd typology [OPCIONES] {directorio}

 Clasifica automáticamente la tipología arquitectónica de una entrega (monolítica, modular,
 librería, incompleta).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    directorio      <path>  Directorio de la entrega del alumno o carpeta de entregas.          │
│                              [obligatorio]                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Salida en formato JSON.                                                        │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd eval-stability`

```text
 Uso: dredd eval-stability [OPCIONES] {binario}

 Evalúa la estabilidad temporal y determinismo de una solución mediante corridas reiteradas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    binario      <path>  Ruta al binario ejecutable C. [obligatorio]                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --repeticiones  -n      <int>    Número de ejecuciones consecutivas. [por defecto: 5]            │
│ --input         -i      <str>    Datos de entrada stdin para el proceso.                         │
│ --timeout       -t      <float>  Tiempo límite por corrida en segundos. [por defecto: 3.0]       │
│ --json                           Salida en formato JSON.                                         │
│ --help          -h               Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd cohort-bench`

```text
 Uso: dredd cohort-bench [OPCIONES] {entregas}

 Ejecuta benchmarking algorítmico comparativo de CPU y memoria en toda la cohorte.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    entregas      <path>  Directorio contenedor de las entregas de la cohorte. [obligatorio]    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --bin      -b      <str>    Nombre del archivo binario ejecutable a comparar.                    │
│                             [por defecto: main]                                                  │
│ --input    -i      <str>    Datos de entrada para el benchmark.                                  │
│ --timeout  -t      <float>  Tiempo límite por entrega en segundos. [por defecto: 5.0]            │
│ --json                      Salida en formato JSON.                                              │
│ --help     -h               Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd smith-adversary`

```text
 Uso: dredd smith-adversary [OPCIONES] {target}

 Genera e inyecta casos de prueba adversarios y de estrés (integración smith).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      <path>  Ruta a binario ejecutable o directorio de tests para inyección.         │
│                          [obligatorio]                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --inject                    Inyectar casos adversarios .in en la carpeta destino.                │
│ --timeout  -t      <float>  Tiempo límite por caso adversario en segundos. [por defecto: 2.0]    │
│ --json                      Salida en formato JSON.                                              │
│ --help     -h               Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd eval-shielded`

```text
 Uso: dredd eval-shielded [OPCIONES] {cmd}

 Ejecuta un proceso bajo el modo 'Sandbox Blindado' con corte total de red y namespaces aislados.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    cmd      <str>  Comando binario a ejecutar en sandbox blindado. [obligatorio]               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --input    -i      <str>    Entrada stdin.                                                       │
│ --timeout  -t      <float>  Tiempo límite en segundos. [por defecto: 3.0]                        │
│ --memory   -m      <int>    Límite estricto de memoria en MB. [por defecto: 48]                  │
│ --help     -h               Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd report-template`

```text
 Uso: dredd report-template [OPCIONES]

 Renderiza o valida plantillas de feedback Markdown enriquecidas con variables contextuales.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --template        -t      <path>  Ruta a la plantilla Markdown con variables contextuales.       │
│ --student         -s      <str>   Identificador o nombre del estudiante.                         │
│                                   [por defecto: estudiante_ejemplo]                              │
│ --exercise        -e      <str>   Nombre del ejercicio o TP. [por defecto: guia_c]               │
│ --score                   <str>   Calificación para la previsualización. [por defecto: 9.0]      │
│ --total-tests             <int>   Total de casos de prueba. [por defecto: 10]                    │
│ --passed-tests            <int>   Casos de prueba aprobados. [por defecto: 9]                    │
│ --failures                <str>   Descripción o detalle de fallos.                               │
│                                   [por defecto: Caso límite 02: retorno inesperado]              │
│ --memory-summary          <str>   Resumen de memoria dinámica.                                   │
│                                   [por defecto: ✓ Sin fugas de memoria (0 bytes perdidos)]       │
│ --badge                   <str>   Insignia de estado general.                                    │
│                                   [por defecto: ✅ **ENTREGA APROBADA**]                         │
│ --output          -o      <path>  Guardar el reporte renderizado en un archivo.                  │
│ --dump-default                    Imprimir o guardar la plantilla por defecto sin renderizar.    │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd sanitize-output`

```text
 Uso: dredd sanitize-output [OPCIONES] {file}

 Sanitiza flujos de salida o logs estudiantiles eliminando secuencias ANSI y truncando si excede el
 límite.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    file      <path>  Archivo de log o volcado de salida a sanitizar. [obligatorio]             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --max-mb                 <int>   Límite máximo seguro en megabytes antes de truncar.             │
│                                  [por defecto: 10]                                               │
│ --output         -o      <path>  Archivo de destino (por defecto sobrescribe el original).       │
│ --no-strip-ansi                  No remover secuencias de escape ANSI.                           │
│ --help           -h              Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd moodle`

```text
 Uso: dredd moodle [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestión de canales Moodle (ingesta ZIP y planillas).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ ingest          Descomprime, normaliza a UTF-8 y versiona (SHA-256) entregas masivas de Moodle.  │
│ export          Exporta las calificaciones a un archivo CSV compatible con Moodle.               │
│ paquete         Arma el paquete para el calificador de Moodle desde las notas y devoluciones de  │
│                 deckard.                                                                         │
│ export-guarani  Exporta las calificaciones finales en formato estándar de actas de SIU Guaraní.  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd moodle ingest`

```text
 Uso: dredd moodle ingest [OPCIONES] {zip_file}

 Descomprime, normaliza a UTF-8 y versiona (SHA-256) entregas masivas de Moodle.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    zip_file      <path>  Archivo ZIP descargado de Moodle con las entregas de la tarea.        │
│                            [obligatorio]                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --dry-run            Solo simular la extracción sin escribir en disco.                           │
│ --force    -f        Re-ingestar sobrescribiendo revisiones previas.                             │
│ --help     -h        Muestra esta ayuda y sale.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd moodle export`

```text
 Uso: dredd moodle export [OPCIONES]

 Exporta las calificaciones a un archivo CSV compatible con Moodle.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --exercise  -e      <str>   Nombre del ejercicio o TP. [obligatorio]                          │
│    --output    -o      <path>  Archivo CSV de salida. [por defecto: calificaciones.csv]          │
│    --help      -h              Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd moodle paquete`

```text
 Uso: dredd moodle paquete [OPCIONES]

 Arma el paquete para el calificador de Moodle desde las notas y devoluciones de deckard.

 Completa la hoja de calificaciones de la tarea y empaqueta las devoluciones en HTML. Las notas
 provisorias dejan su fila intacta. Sale con 1 si un estudiante no se pudo vincular.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --planilla             -p      <file>                   Hoja de calificaciones descargada de  │
│                                                            la tarea de Moodle.                   │
│                                                            [obligatorio]                         │
│    --notas                -n      <file>                   calificaciones.csv de deckard         │
│                                                            exercise rubric.                      │
│                                                            [por defecto:                         │
│                                                            calificaciones/calificaciones.csv]    │
│    --devoluciones         -d      <path>                   Carpeta de devoluciones Markdown (por │
│                                                            omisión, devoluciones/ junto a las    │
│                                                            notas).                               │
│    --mapa                 -m      <file>                   CSV alumno,dato en Moodle             │
│                                                            (identificador, correo o nombre),     │
│                                                            para entregas de GitHub.              │
│    --salida               -o      <path>                   Carpeta del paquete.                  │
│                                                            [por defecto: moodle]                 │
│    --incluir-provisorias                                   Importar también las notas            │
│                                                            provisorias.                          │
│    --maximo                       <float range> [x>=0.01]  Calificación máxima de la tarea, si   │
│                                                            la planilla no la trae.               │
│    --columna-nota                 <str>                    Encabezado de la nota, si no se       │
│                                                            detecta.                              │
│    --columna-comentarios          <str>                    Encabezado de los comentarios, si no  │
│                                                            se detecta.                           │
│    --help                 -h                               Muestra esta ayuda y sale.            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd moodle export-guarani`

```text
 Uso: dredd moodle export-guarani [OPCIONES] [entregas]

 Exporta las calificaciones finales en formato estándar de actas de SIU Guaraní.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   entregas      <path>  Directorio de entregas o base de datos de calificaciones.                │
│                         [por defecto: entregas]                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o      <path>  Ruta de destino del CSV de SIU Guaraní.                                │
│                           [por defecto: acta_guarani.csv]                                        │
│ --help    -h              Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd github`

```text
 Uso: dredd github [OPCIONES] COMANDO [ARGUMENTOS]...

 Comandos de integración con GitHub (clone, comment, pr-fix).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ clone    Clona o actualiza el repositorio de una entrega de GitHub en                            │
│          <practica>/<directorio_destino>/repo.                                                   │
│ comment  Envía el informe Markdown generado como comentario en el Pull Request de GitHub.        │
│ pr-fix   Reconstruye o crea el Pull Request de corrección para un estudiante a partir de la      │
│          práctica, nombre clonado y dirección remota.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd github clone`

```text
 Uso: dredd github clone [OPCIONES] {practica} {directorio_destino} {repo_url}

 Clona o actualiza el repositorio de una entrega de GitHub en <practica>/<directorio_destino>/repo.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    practica                <str>  Nombre de la actividad / práctica (ej. TP0, tp01, etc.).     │
│                                     [obligatorio]                                                │
│ *    directorio_destino      <str>  Nombre del directorio destino para el estudiante (ej.        │
│                                     TP0-Enehuen).                                                │
│                                     [obligatorio]                                                │
│ *    repo_url                <str>  URL del repositorio de GitHub a clonar (HTTPS o SSH).        │
│                                     [obligatorio]                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd github comment`

```text
 Uso: dredd github comment [OPCIONES] {exercise} {student}

 Envía el informe Markdown generado como comentario en el Pull Request de GitHub.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    exercise      <str>  Nombre de la actividad. [obligatorio]                                  │
│ *    student       <str>  Nombre de usuario del estudiante. [obligatorio]                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --org   -o      <str>  Organización de GitHub. [por defecto: INGCOM-UNRN-P1]                     │
│ --open                 Abrir la vista de cambios del PR en el navegador.                         │
│ --pr            <int>  Número específico de PR (por defecto autodetecta el abierto).             │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd github pr-fix`

```text
 Uso: dredd github pr-fix [OPCIONES] {practica} {nombre_clonado} {direccion}

 Reconstruye o crea el Pull Request de corrección para un estudiante a partir de la práctica,
 nombre clonado y dirección remota.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    practica            <str>  Nombre de la actividad o práctica. [obligatorio]                 │
│ *    nombre_clonado      <str>  Nombre con el que fue clonado el directorio del estudiante.      │
│                                 [obligatorio]                                                    │
│ *    direccion           <str>  Dirección o URL del repositorio en GitHub. [obligatorio]         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --branch  -b      <str>  Nombre de la rama de corrección. [por defecto: correccion]              │
│ --base            <str>  Rama base de destino para el Pull Request. [por defecto: main]          │
│ --help    -h             Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config`

```text
 Uso: dredd config [OPCIONES] COMANDO [ARGUMENTOS]...

 Gestión de configuración, entregas, guías y políticas de chequeo.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ show            Muestra la configuración activa de dredd.yaml, entregas mapeadas y políticas de  │
│                 chequeo.                                                                         │
│ add-entrega     Agrega o actualiza una entrega en dredd.yaml con su patrón ZIP, origen           │
│                 Moodle/GitHub, guía Deckard, modo y chequeos específicos.                        │
│ remove-entrega  Elimina una entrega/actividad de la configuración dredd.yaml.                    │
│ set-check       Configura parámetros de verificación de herramientas pedagógicas a nivel global  │
│                 o por entrega.                                                                   │
│ validate        Valida la integridad de dredd.yaml, directorios del espacio de trabajo y         │
│                 existencia de guías Deckard.                                                     │
│ preset          Aplica un perfil preconfigurado de rigurosidad a dredd.yaml (ej. 'strict' para   │
│                 máxima rigurosidad).                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config show`

```text
 Uso: dredd config show [OPCIONES]

 Muestra la configuración activa de dredd.yaml, entregas mapeadas y políticas de chequeo.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --entrega    -e      <str>   Mostrar detalle de una entrega específica.                          │
│ --workspace  -w      <path>  Directorio raíz del workspace. [por defecto: .]                     │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config add-entrega`

```text
 Uso: dredd config add-entrega [OPCIONES] {entrega}

 Agrega o actualiza una entrega en dredd.yaml con su patrón ZIP, origen Moodle/GitHub, guía
 Deckard, modo y chequeos específicos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    entrega      <str>  Slug identificador de la entrega (ej. entrega_4, tp04). [obligatorio]   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --zip             -z                        <str>   Patrón glob del archivo ZIP de Moodle (ej.   │
│                                                     '*entrega*4*.zip').                          │
│                                                     [por defecto: *]                             │
│ --guia            -g                        <str>   Ruta relativa a la guía Deckard (ej.         │
│                                                     'guias/entrega_4/guia.yaml').                │
│ --titulo          -t                        <str>   Título descriptivo de la actividad.          │
│ --ripley-strict       --no-ripley-strict            Modo estricto de Ripley para esta entrega.   │
│ --disabled-rules                            <str>   Códigos de reglas Ripley a omitir separados  │
│                                                     por coma (ej. '0x0009h,0x0004h').            │
│ --memory-mb                                 <int>   Límite estricto de RAM en MB para el         │
│                                                     sandbox.                                     │
│ --mode            -m                        <str>   Modo de construcción para esta entrega       │
│                                                     ('archivos_individuales',                    │
│                                                     'makefiles_individuales' o 'proyecto').      │
│ --source          -s                        <str>   Origen de la entrega ('moodle' para ZIPs o   │
│                                                     'github' para repositorios).                 │
│                                                     [por defecto: moodle]                        │
│ --github-org                                <str>   Organización de GitHub Classroom para esta   │
│                                                     entrega.                                     │
│ --repo-pattern                              <str>   Patrón o prefijo del nombre de repositorio   │
│                                                     en GitHub.                                   │
│ --branch                                    <str>   Rama por defecto para clonar/evaluar en      │
│                                                     GitHub.                                      │
│                                                     [por defecto: main]                          │
│ --workspace       -w                        <path>  Directorio raíz del workspace.               │
│                                                     [por defecto: .]                             │
│ --help            -h                                Muestra esta ayuda y sale.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config remove-entrega`

```text
 Uso: dredd config remove-entrega [OPCIONES] {entrega}

 Elimina una entrega/actividad de la configuración dredd.yaml.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    entrega      <str>  Slug identificador de la entrega a eliminar. [obligatorio]              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --workspace  -w      <path>  Directorio raíz del workspace. [por defecto: .]                     │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config set-check`

```text
 Uso: dredd config set-check [OPCIONES] {tool} {setting}

 Configura parámetros de verificación de herramientas pedagógicas a nivel global o por entrega.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    tool         <str>  Herramienta ('ripley', 'kaneda', 'spunkmeyer', 'gaff', 'daedalus',      │
│                          'sandbox').                                                             │
│                          [obligatorio]                                                           │
│ *    setting      <str>  Clave=valor a configurar (ej. 'strict=true', 'disabled_rules=0x0009h',  │
│                          'max_memory_mb=128', 'compiler=gcc').                                   │
│                          [obligatorio]                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --entrega    -e      <str>   Slug de entrega específica (si se omite, aplica a nivel global).    │
│ --workspace  -w      <path>  Directorio raíz del workspace. [por defecto: .]                     │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config validate`

```text
 Uso: dredd config validate [OPCIONES]

 Valida la integridad de dredd.yaml, directorios del espacio de trabajo y existencia de guías
 Deckard.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --workspace  -w      <path>  Directorio raíz del workspace. [por defecto: .]                     │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd config preset`

```text
 Uso: dredd config preset [OPCIONES] [preset_name]

 Aplica un perfil preconfigurado de rigurosidad a dredd.yaml (ej. 'strict' para máxima
 rigurosidad).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   preset_name      <str>  Nombre del preset a aplicar ('strict' o 'standard').                   │
│                           [por defecto: strict]                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --workspace  -w      <path>  Directorio raíz del workspace. [por defecto: .]                     │
│ --help       -h              Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd evaluate`

```text
 Uso: dredd evaluate [OPCIONES] COMANDO [ARGUMENTOS]...

 Evaluación docente, autograding y limpieza de entregas.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ clean  Limpia las evaluaciones anteriores: elimina los directorios rNi y los informes generados. │
│ run    Clona/actualiza el repositorio o evalúa entregas locales, ejecuta el análisis con Ripley  │
│        y genera el informe Markdown.                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd evaluate clean`

```text
 Uso: dredd evaluate clean [OPCIONES] [exercise] [student]

 Limpia las evaluaciones anteriores: elimina los directorios rNi y los informes generados.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   exercise      <str>  Nombre de la actividad o ruta al directorio de entregas (ej. tp01,        │
│                        ./entregas). Si no se indica, limpia en ./entregas o en el directorio     │
│                        actual.                                                                   │
│   student       <str>  Nombre de usuario del estudiante específico a limpiar (opcional; por      │
│                        defecto limpia todos).                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --all           -a        Limpiar todas las entregas encontradas.                                │
│ --dry-run       -n        Modo simulación: muestra qué carpetas rNi e informes se eliminarían    │
│                           sin borrar archivos.                                                   │
│ --rni-only                Limpiar exclusivamente los directorios rNi de herramientas,            │
│                           conservando los informes consolidados.                                 │
│ --reports-only            Limpiar exclusivamente los archivos de informes Markdown/HTML/PDF,     │
│                           conservando los directorios rNi.                                       │
│ --verbose       -v        Muestra cada archivo y carpeta eliminado en consola.                   │
│ --help          -h        Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd evaluate run`

```text
 Uso: dredd evaluate run [OPCIONES] {exercise} [student]

 Clona/actualiza el repositorio o evalúa entregas locales, ejecuta el análisis con Ripley y genera
 el informe Markdown.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    exercise      <str>  Nombre de la actividad / ejercicio o ruta al directorio de entregas.   │
│                           [obligatorio]                                                          │
│      student       <str>  Nombre de usuario del estudiante (opcional si se usa --all).           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --org                        -o      <str>   Organización de GitHub.                             │
│                                              [por defecto: INGCOM-UNRN-P1]                       │
│ --all                        -a              Evaluar todos los estudiantes presentes en el       │
│                                              workspace.                                          │
│ --template-dir               -t      <path>  Directorio con header.md y footer.md (por omisión,  │
│                                              plantillas_dir de dredd.yaml).                      │
│ --tipo-entrega,--build-mode  -m      <str>   Tipo de entrega / modo de construcción              │
│                                              ('archivos_individuales', 'makefiles_individuales'  │
│                                              o 'proyecto').                                      │
│ --dry-run                                    Modo Dry Run: evalúa únicamente una muestra de      │
│                                              hasta 3 estudiantes representativos antes del lote  │
│                                              completo.                                           │
│ --clean                      -c              Limpia directorios de evaluación (rNi) e informes   │
│                                              previos antes de volver a evaluar.                  │
│ --force                      -f              Fuerza la re-evaluación completa eliminando         │
│                                              resultados previos de las carpetas de estudiantes.  │
│ --failed-only                                Evaluar sólo las entregas cuya última revisión no   │
│                                              terminó, no compiló o falló alguna prueba.          │
│ --resume                                     Retomar una corrida interrumpida: saltear las       │
│                                              revisiones que ya quedaron completas                │
│                                              (auditoria.json).                                   │
│ --help                       -h              Muestra esta ayuda y sale.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd deckard`

```text
 Uso: dredd deckard [OPCIONES] COMANDO [ARGUMENTOS]...

 Integración con el banco de ejercicios de deckard.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ sync  Empaqueta con `deckard export pack` los ejercicios de la guía que están en el banco, junto │
│       a guia.yaml.                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `dredd deckard sync`

```text
 Uso: dredd deckard sync [OPCIONES] {actividad}

 Empaqueta con `deckard export pack` los ejercicios de la guía que están en el banco, junto a
 guia.yaml.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    actividad      <str>  Actividad mapeada en dredd.yaml (ej. entrega_4). [obligatorio]        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --force    -f        Volver a empaquetar los .ripkg que ya existen.                              │
│ --dry-run  -n        Mostrar qué se empaquetaría sin llamar a deckard.                           │
│ --help     -h        Muestra esta ayuda y sale.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`dredd@f27c116`](https://github.com/INGCOM-UNRN-P1/dredd/tree/f27c116).
