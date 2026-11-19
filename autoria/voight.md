---
title: "voight"
subtitle: "bancos de preguntas de Moodle"
---

<!-- Generado por scripts/generar_paginas.py desde voight@5aa1504: no editar a mano. -->

(manual-voight)=
# voight — bancos de preguntas de Moodle

Repositorio: [github.com/INGCOM-UNRN/voight](https://github.com/INGCOM-UNRN/voight).

Conjunto de herramientas unificadas en Python para gestionar preguntas de Moodle en formatos XML y GIFT. Facilita la conversión, análisis, limpieza, mantenimiento y generación de preguntas mediante IA.

Todas las herramientas anteriores han sido consolidadas en un único comando raíz: `voight`.

---

## Alcance

### Qué cubre
- Gestión integral, validación y mantenimiento de bancos de preguntas pedagógicas de Moodle.
- Conversión bidireccional fiel y sin pérdida entre formatos GIFT y Moodle XML.
- Normalización tipográfica de delimitadores de fórmulas matemáticas (LaTeX `\(...\)` y `\[...\]`) y bloques de código Markdown.
- Paridad entre GIFT y Moodle XML: formato, protección del código (fullwidth, `·` y `↵`), análisis de repositorios, duplicados y reportes de salud trabajan igual sobre ambos formatos (y sobre repositorios mixtos).
- Validación sintáctica y de completitud de metadatos de preguntas (retroalimentación, pesos porcentuales, categorías).
- Reorganización y sincronización de estructuras de directorios de categorías de preguntas.

### Qué no cubre (Límites y Delegación)
- Generación de preguntas de C con salida verificada por compilación: el comando `synth` **invoca** el motor de síntesis de `alucarD` (`generador_examenes.synthesizer`); la lógica de plantillas y su validación con GCC vive allí, no acá.
- Generación de exámenes en PDF con reconocimiento OMR (delegado a `alucard`).
- Creación de módulos de aprendizaje SCORM (delegado a `scorm-tools`).

---

## Requisitos

### Requisitos de Sistema y Entorno
- Multiplataforma. Python >= 3.10.

### Dependencias Externas y Binarios
- Para los comandos de gestión de bancos (conversión, validación, limpieza): ninguna.
- Diagramas mermaid al fusionar Moodle XML (`unify`): mermaid-cli (`npm install -g @mermaid-js/mermaid-cli`).
- Diagramas de estructuras (```` ```estructura ````) al fusionar Moodle XML: el paquete `alucarD` en el entorno de voight.
- `synth`: `gcc` (compila y ejecuta los snippets para verificar su salida) y el paquete `alucarD`, que aporta el motor de síntesis.
- `ai`: un proveedor de IA. Con Gemini (el de siempre), el extra opcional `ai` (`uv tool install "voight[ai] @ git+https://github.com/INGCOM-UNRN/voight"`) y una `GEMINI_API_KEY` (se guarda con `voight config set gemini-key`; `voight config show` muestra todo lo configurado); con Claude, el mismo extra y `ANTHROPIC_API_KEY`; con un servidor local (Ollama, llama.cpp, LM Studio…) u OpenCode, nada más.
- LanguageTool (local o API remota) para la revisión ortográfica opcional.
- `voight doctor` informa cuáles de estos requisitos están presentes.

### Integración en el Ecosistema
- CLI `voight`. Subcomando `doctor`.

---

### Contrato de datos GIFT (consumidores por formato)

`scorm-tools from-gift` consume bancos GIFT producidos aquí. La frontera es el
formato, no el código, y su versión es `voight.core.gift_model.GIFT_CONTRACT_VERSION`
(hoy `1.1.0`). El contrato cubre los tipos `MC`, `TF`, `Short` y `Numerical`,
con retroalimentación por opción y global; está fijado por
`tests/test_contrato_gift.py`. Un cambio incompatible sube la versión mayor y
debe coordinarse con scorm-tools.

## Instalación y Uso

Este proyecto utiliza [uv](https://docs.astral.sh/uv/) para la gestión de dependencias y ejecución.
Se instala siempre desde el repositorio, no por nombre desde PyPI.

```bash
# Instalación como herramienta (comando `voight`)
uv tool install git+https://github.com/INGCOM-UNRN/voight
# con el editor web opcional (`voight ui`)
uv tool install "voight[ui] @ git+https://github.com/INGCOM-UNRN/voight"
# con las interfaces de terminal (`dedup --tui`, `health --tui`, `ai --mode classify --revisar`)
uv tool install "voight[tui] @ git+https://github.com/INGCOM-UNRN/voight"
# con los SDK de Gemini y Claude para `voight ai` (un servidor local u OpenCode no los necesitan)
uv tool install "voight[ai,tui] @ git+https://github.com/INGCOM-UNRN/voight"
```

Para desarrollo:

```bash
# Clonar el repositorio
git clone https://github.com/INGCOM-UNRN/voight.git
cd voight

# Ejecutar la ayuda principal
uv run voight --help
```

## Comandos Disponibles

El CLI `voight` se organiza en subcomandos especializados:

Una sola forma de hacer cada cosa: `health` diagnostica sin escribir (con `stats` y `similar` como subcomandos), `fix` modifica (formato, código, nombres, HTML, tags, ortografía), `split` divide y `unify` fusiona. Los nombres anteriores (`health check`, `health validate`, `validate`, `analyze`, `health --clean-html`, `tree export|collect`, `fix xml …`, `spellcheck`, `languagetool`, `grammar`, `format`, `xml`) siguen funcionando con un aviso y se van a retirar; la tabla de equivalencias está en el [manual](https://github.com/INGCOM-UNRN/voight/blob/main/MANUAL.md#3-guía-integral-de-comandos-cli).

### 1. Validación y Análisis (GIFT y XML)
- `voight health stats`: Genera estadísticas completas sobre un repositorio de preguntas (por formato, tipo, categoría y tags).
- `voight health similar`: Encuentra preguntas similares usando TF-IDF + Jaccard, también entre un `.gift` y un `.xml`; escala a miles de preguntas.
- `voight dedup`: Elimina preguntas duplicadas según un umbral de similitud configurable (`-s`, por defecto 0.95), en GIFT y XML. Sólo considera duplicadas las del mismo tipo, con la misma respuesta correcta y enunciados que también superan el umbral; conserva la más completa. Simula por defecto (`--aplicar` elimina) y registra cada eliminación con la ruta completa en `dedup.log`; guarda una copia de los originales y `--restaurar ultimo` lo deshace. `--confirmar-jev` confirma cada par con Jev y `--tui` abre una interfaz de terminal para revisar los grupos lado a lado y decidir cuáles eliminar (extra `tui`).
- `voight health`: Reporte de salud del banco (archivos o directorios, GIFT y XML): claves de corrección y porcentajes que Moodle acepta, feedback general y por opción, cantidad de opciones, longitud relativa de las respuestas, señales de redacción (posición de la correcta, «todas las anteriores», negaciones sin resaltar, distractores débiles), distribución de Bloom y dificultad con el blueprint por categoría, campos de Moodle inconsistentes, código sin proteger o sin lenguaje, enlaces y HTML obsoleto. Separa errores de advertencias y sale con código 1 si hay errores (`--estricto`: también con advertencias). `--csv` exporta una fila por pregunta y `--tui` recorre los hallazgos y aplica los arreglos automáticos.
- `voight health --compilar`: certifica el código C de cada pregunta con `daedalus` (extra `compilar`): compila con los flags de la cátedra y `-O2` (que suma los avisos de flujo: variables sin inicializar, índices fuera de rango…) y, si el toolchain trae los sanitizers, lo ejecuta con `-fsanitize=address,undefined`. Una pregunta con errores, warnings o comportamiento indefinido es un error del banco, salvo que la pregunta trate justamente de eso (la clave dice «no compila», «comportamiento indefinido»…). Los fragmentos que usan tipos o variables declarados en otra parte se informan aparte, y lo que el snippet no usa (variables, parámetros) no cuenta. `--permitir-warning W` deja pasar un warning (sin `-W`). También `voight validate --compilar`.
- `voight verify`: Compila y ejecuta el código C y Java de las preguntas y avisa si la salida coincide con un distractor en lugar de la correcta, si no compila, falla o tiene comportamiento indefinido (`--sanitizar`); `--estilo` revisa el código C con las reglas de la cátedra.

### 2. Formateo y Corrección (GIFT y XML)
- `voight fix highlight`: resalta la sintaxis de los bloques ``` de C de un Moodle XML con HTML y CSS en línea (un `<span style="color:…">` por token, sin scripts en el navegador): se ve con colores en la vista de cuestionarios de Moodle. En `format="markdown"` el bloque queda como HTML crudo y el resto del texto no cambia; `voight health` y `fix clean-html` no tratan esos estilos como HTML obsoleto. Sólo Moodle XML: un GIFT se convierte antes con `voight convert gift-to-xml`.
- `voight fix format`: Estandariza el formato visual de archivos GIFT y Moodle XML (`--correct-first` ordena las opciones por porcentaje). `--fullwidth` protege el código: símbolos fullwidth, `·` en la indentación y `↵` al final de cada línea; `--normal` lo deshace. `--gaff` formatea el código C de los bloques con gaff (estilo de la cátedra): restaura los caracteres normales, aplica `gaff fix` y lo vuelve a proteger como estaba. Ver [caracteres especiales](https://github.com/INGCOM-UNRN/voight/blob/main/docs/caracteres_especiales.md).
- `voight fix format --check` / `--diff`: Verifican el formato sin escribir (para CI y pre-commit).
- `voight fix code-lang`: Etiqueta el lenguaje (C o Java) de los bloques ``` que no lo tienen.
- `voight fix code-format`: Formatea el código C y Java con clang-format (`--estilo allman` u otro estilo de llaves aplica esas llaves sobre el estilo por defecto; un estilo que clang-format no acepta da error).
- `voight fix format-init [dir]`: Crea en la raíz del árbol de preguntas la sección `[format]` del `.voight.toml` (o `.voight`) con todas las opciones de formato; `fix format` la toma para formatear todo el banco igual.
- `voight fix code-indent`: Marca la indentación del código con `·`.
- `voight fix code-chars`: Convierte los caracteres del código entre normal y fullwidth; conserva la indentación `·` y los `↵`, así que se combina con `code-indent`.
- `voight fix slugify`: Normaliza nombres de archivos (minúsculas, sin acentos).
- `voight fix name-from-title`: Renombra archivos según el título de la pregunta.
- `voight fix title-from-name`: Actualiza el título interno según el nombre del archivo.
- `voight fix extension`: Corrige la extensión según el contenido (`.xml` con GIFT adentro pasa a `.gift` y viceversa); no pisa archivos existentes.

### 3. Conversión

Los tres subcomandos aceptan archivos y directorios, que recorren recursivamente (`--no-recursive` para un solo nivel).
- `voight convert html-to-md`: Convierte etiquetas HTML a Markdown en archivos XML o GIFT.
- `voight convert xml-to-gift`: Convierte Moodle XML a GIFT (soporta categorías, selección múltiple con pesos, V/F, emparejamiento, numérica con tolerancia, ensayo y descripción).
- `voight convert gift-to-xml`: Convierte GIFT a Moodle XML con bloques CDATA correctos. Con un directorio, `xml-to-gift` y `gift-to-xml` convierten cada archivo al lado del original o, con `-o DIR`, replicando el árbol en `DIR`; no pisan archivos existentes salvo `--forzar` (`-n` simula). Con un solo archivo, la salida va a stdout o a `-o`. Ambos conversores viajan sobre el modelo unificado de preguntas del parser PEG y son estables en round-trip.

### 4. Árboles de Directorios (absorbe moodle-reorganizer)
- `voight split banco.gift|xml -o dir/`: Exporta un banco monolítico a un árbol de carpetas por categoría (1 archivo por pregunta); sin `-o`, divide cada archivo en el lugar.
- `voight unify dir/ -o reconstruido.gift|xml`: Recolecta el árbol nuevamente a un archivo único, restaurando las categorías. En Moodle XML, los bloques ```` ```mermaid ```` (con mermaid-cli, `mmdc`) y ```` ```estructura ```` (con alucarD) se cambian por imágenes y, como las imágenes con ruta relativa, se incrustan en el archivo fusionado como `@@PLUGINFILE@@`; las preguntas fuente siguen siendo texto (`--no-incrustar` lo desactiva, `--diagramas svg` cambia el formato).

### 5. Editor Web (absorbe moodle-visor / mxviz)
- `voight ui [dir]`: Abre un editor web local para navegar y editar preguntas organizadas en directorios, con soporte nativo de **Moodle XML y GIFT**. Edita todos los tipos de Moodle (numérica con tolerancia, calculadas, emparejamiento, ordenamiento, huecos, arrastrar y soltar, cloze…) sin perder lo que no muestra. Filtra el árbol por cantidad de opciones (menos de / exactamente / más de N) para encontrar preguntas con pocas opciones. Requiere el extra opcional: `uv tool install "voight[ui] @ git+https://github.com/INGCOM-UNRN/voight"`.

### 6. Mantenimiento XML
- `voight fix format`: Formatea el XML con cada `<text>` en CDATA (antes `fix xml cdata`).
- `voight fix clean-tags`: Elimina secciones de etiquetas (`<tags>`) redundantes.
- `voight fix name-from-title`: Renombra archivos (GIFT y XML) según el título interno de la pregunta (antes `fix xml rename`).
- `voight fix clean-html`: Limpia el HTML obsoleto y los estilos inline que informa `health` (antes `health --clean-html`).

### 7. Inteligencia Artificial (Gemini, servidor local, OpenCode o Claude)
- `voight ai`: Mejora la calidad pedagógica (`improve`), crea variaciones (`multiply`), completa sólo la retroalimentación que falta (`feedback`) o agrega distractores donde faltan (`distractors`) en preguntas GIFT y Moodle XML, con Google Gemini, un servidor local con la API de OpenAI (Ollama, llama.cpp, LM Studio, vLLM), OpenCode o Claude (`--proveedor google|local|opencode|claude`, y `--model`). El proveedor se configura igual que en el resto del ecosistema (yutani.ia): `--proveedor`, `VOIGHT_PROVEEDOR`, `P1_IA_PROVEEDOR`, `P1_IA_MODELO`, `P1_IA_URL` o `~/.config/p1/ia.toml` (con `[herramientas.voight]` para lo propio); sin nada configurado sigue siendo Gemini, y `voight doctor` muestra cuál quedó y si está disponible. El modelo recibe GIFT compacto (sin metadatos ni marcas, código en ASCII) y la respuesta se aplica sobre el archivo original. Además, cada modo envía y recibe sólo lo que necesita: `--parte enunciado` manda y recibe sólo el enunciado, `--parte respuestas` el enunciado como contexto y las opciones sin retroalimentación (vuelven sólo las opciones), `feedback` sólo las opciones y qué retroalimentación falta (vuelve sólo esa) y `distractors` las opciones sin retroalimentación (vuelven sólo los distractores nuevos); lo devuelto se aplica sobre la pregunta original, que nunca viaja entera. Estima tokens y costo antes de llamar al modelo, guarda las respuestas en caché y `--dry-run` muestra lo que se enviaría.
- `voight ai --mode classify`: Clasifica cada pregunta con Jev (TypeSafe): nivel de Bloom (B1–B6) y dificultad (1–5) del enunciado y de las respuestas, escritos como comentario en GIFT y XML (y como tags de Moodle con `--tags`). `--calibrar` mide la concordancia con una clasificación docente y `--revisar` abre una interfaz de terminal para corregir las de poca confianza. Requiere `TYPESAFE_API_KEY`.

### 8. Moodle e integración
- `voight moodle subir`: Sube un banco a un curso de Moodle por servicio web (requiere el plugin `local_questions_importer_ws` en el sitio).
- `.voight.toml`: valores por defecto de cada comando para un banco (umbral de dedup, contexto de classify, todas las opciones de format, rutas a ignorar…); también puede llamarse `.voight`.
- `--desde <rev>` procesa sólo lo cambiado desde una revisión git; hooks de [pre-commit](https://github.com/INGCOM-UNRN/voight/blob/main/.pre-commit-hooks.yaml) y una acción de GitHub (`uses: INGCOM-UNRN/voight@main`, ejemplo en [docs/ejemplos/salud-banco.yml](https://github.com/INGCOM-UNRN/voight/blob/main/docs/ejemplos/salud-banco.yml)) para revisar la salud de cada PR.

### 9. Inspección de cuestionarios y revisión docente

- `voight moodle inspeccionar copia.mbz`: inventario de preguntas, categorías,
  versiones, slots y configuración, sin extraer ni restaurar (tar/ZIP).
- `voight moodle backup-quiz banco/ --plan -k 2`: revisa cupos y detecta categorías
  insuficientes o tipos no exportables antes de generar el MBZ; no requiere salida.
- `voight catalogo banco/ -o catalogo.md`: catálogo docente con opciones, claves
  y referencias a sus archivos de origen.
- `voight muestra banco/ -n 10 --semilla 42 -o muestra.md`: muestreo uniforme,
  reproducible y sin reemplazo, para revisión docente.
- `voight health accesibilidad banco/`: localiza imágenes sin texto alternativo
  en enunciados, opciones y feedback, con HTML y Markdown.

Todos admiten `--json`. Ver [ejemplos, formatos y límites](https://github.com/INGCOM-UNRN/voight/blob/main/docs/qol_docente.md).

## Documentación Detallada

Para más información sobre funcionalidades específicas, consulta la carpeta [docs/](https://github.com/INGCOM-UNRN/voight/blob/main/docs):

- **[Guía de Inicio Rápido](https://github.com/INGCOM-UNRN/voight/blob/main/docs/QUICK_START.md)**
- **[Validación y Análisis](https://github.com/INGCOM-UNRN/voight/blob/main/docs/README_validate_questions.md)**
- **[Mantenimiento XML](https://github.com/INGCOM-UNRN/voight/blob/main/docs/README_xml_maintenance.md)**
- **[Referencia de Caracteres Especiales](https://github.com/INGCOM-UNRN/voight/blob/main/docs/caracteres_especiales.md)**

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Opciones de `voight`

| Opción | Descripción |
|:--|:--|
| `--llm` | Muestra instrucciones generales para un LLM. |

### Comandos

| Comando | Descripción |
|:--|:--|
| `voight doctor` | Verifica el estado del entorno de VOIGHT (Python, LanguageTool, gcc y el motor de síntesis). |
| `voight ai` | Procesamiento de preguntas GIFT y Moodle XML usando IA (Gemini, un servidor local, OpenCode o Claude). |
| `voight dedup` | Elimina preguntas duplicadas según un umbral de similitud (GIFT y Moodle XML). |
| `voight verify` | Compila y ejecuta el código de las preguntas de salida y compara con las opciones (gcc, javac). |
| `voight catalogo` | Exporta un catálogo docente con enunciados, opciones y claves de respuesta. |
| `voight muestra` | Selecciona una muestra reproducible para revisión docente (incluye las claves). |
| `voight split` | Divide archivos GIFT o Moodle XML con múltiples preguntas en archivos individuales. |
| `voight unify` | Unifica árboles o grupos de archivos de preguntas (GIFT o XML) en un único archivo. |
| `voight synth` | daedalus en belmont: sintetiza preguntas de C verificadas con GCC. |
| `voight ui` | Abre el editor web local (cerebro) sobre DIRECTORIO. |
| `voight health` | Audita la salud del banco (con `stats` y `similar` como subcomandos). |
| `voight config` | Configuración global: claves de los servicios, proveedor y modelo de IA. |
| `voight convert` | Comandos para convertir entre formatos. |
| `voight fix` | Todo lo que modifica archivos: formato (format), código, nombres, HTML, tags y ortografía (grammar). |
| `voight moodle` | Operaciones sobre un sitio Moodle (servicio web). |

Ayuda de cada comando: `voight <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `voight doctor`, `voight dedup`, `voight verify`, `voight catalogo`, `voight muestra`, `voight split`, `voight unify`, `voight synth`, `voight health`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-voight-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `voight`
:open:

```text
 Uso: voight [OPCIONES] COMANDO [ARGUMENTOS]...

 Herramientas para la gestión de preguntas de Moodle.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de voight y sale.                             │
│ --llm                           Muestra instrucciones generales para un LLM.                     │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ doctor     Verifica el estado del entorno de VOIGHT (Python, LanguageTool, gcc y el motor de     │
│            síntesis).                                                                            │
│ ai         Procesamiento de preguntas GIFT y Moodle XML usando IA (Gemini, un servidor local,    │
│            OpenCode o Claude).                                                                   │
│ dedup      Elimina preguntas duplicadas según un umbral de similitud (GIFT y Moodle XML).        │
│ verify     Compila y ejecuta el código de las preguntas de salida y compara con las opciones     │
│            (gcc, javac).                                                                         │
│ catalogo   Exporta un catálogo docente con enunciados, opciones y claves de respuesta.           │
│ muestra    Selecciona una muestra reproducible para revisión docente (incluye las claves).       │
│ split      Divide archivos GIFT o Moodle XML con múltiples preguntas en archivos individuales.   │
│ unify      Unifica árboles o grupos de archivos de preguntas (GIFT o XML) en un único archivo.   │
│ synth      daedalus en belmont: sintetiza preguntas de C verificadas con GCC.                    │
│ ui         Abre el editor web local (cerebro) sobre DIRECTORIO.                                  │
│ health     Audita la salud del banco (con `stats` y `similar` como subcomandos).                 │
│ config     Configuración global: claves de los servicios, proveedor y modelo de IA.              │
│ convert    Comandos para convertir entre formatos.                                               │
│ fix        Todo lo que modifica archivos: formato (format), código, nombres, HTML, tags y        │
│            ortografía (grammar).                                                                 │
│ moodle     Operaciones sobre un sitio Moodle (servicio web).                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight doctor`

```text
 Uso: voight doctor [OPCIONES]

 Verifica el estado del entorno de VOIGHT (Python, LanguageTool, gcc y el motor de síntesis).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight ai`

```text
 Uso: voight ai [OPCIONES] [inputs]...

 Procesamiento de preguntas GIFT y Moodle XML usando IA (Gemini, un servidor local, OpenCode o
 Claude).

 El modelo recibe GIFT compacto (sin comentarios, categorías ni marcas · y ↵ en el
 código); las preguntas XML se convierten a GIFT y la respuesta se aplica sobre el
 XML original, que conserva sus metadatos.

 --mode classify usa Jev (TypeSafe) para agregar a cada pregunta un comentario con su
 nivel de Bloom y la dificultad (1–5) del enunciado y de las respuestas.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   inputs      <path>  Archivos .gift/.xml o directorios.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                                                              Muestra instrucciones para un │
│                                                                    LLM sobre este comando.       │
│ --mode                                <improve|multiply|transform  Modo: improve (mejorar),      │
│                                       |feedback|distractors|class  multiply (variaciones),       │
│                                       ify>                         transform (usar prompt        │
│                                                                    personalizado), feedback      │
│                                                                    (completar sólo la            │
│                                                                    retroalimentación que falta), │
│                                                                    distractors (agregar          │
│                                                                    distractores donde faltan o   │
│                                                                    la correcta delata por su     │
│                                                                    largo) o classify (Bloom y    │
│                                                                    dificultad con Jev).          │
│                                                                    [por defecto: improve]        │
│ --prompt                              <str>                        Prompt personalizado o ruta a │
│                                                                    un archivo .txt con el        │
│                                                                    prompt.                       │
│ --output                              <path>                       Directorio de salida (por     │
│                                                                    defecto: output_<mode>).      │
│ --proveedor,--provider                <str>                        Modelo de lenguaje para       │
│                                                                    improve/multiply/transform/f… │
│                                                                    google (Gemini), local        │
│                                                                    (Ollama, llama.cpp…),         │
│                                                                    opencode o claude (por        │
│                                                                    defecto: VOIGHT_PROVEEDOR,    │
│                                                                    P1_IA_PROVEEDOR,              │
│                                                                    ~/.config/p1/ia.toml o        │
│                                                                    google).                      │
│ --model                               <str>                        Modelo (por defecto, el       │
│                                                                    configurado para el           │
│                                                                    proveedor: gemini-2.0-flash,  │
│                                                                    claude-opus-5,                │
│                                                                    opencode-go/qwen3.8-max o el  │
│                                                                    primero del servidor local).  │
│ --parte,--part                        <todo|enunciado|respuestas>  improve: qué mejorar.         │
│                                                                    enunciado o respuestas envían │
│                                                                    y reciben sólo esa parte      │
│                                                                    (menos tokens); todo, la      │
│                                                                    pregunta entera.              │
│                                                                    [por defecto: todo]           │
│ --recursive                   -r                                   Procesar subdirectorios       │
│                                                                    recursivamente.               │
│ --batch-size                          <int>                        Número de preguntas por       │
│                                                                    petición a la API (default:   │
│                                                                    5).                           │
│                                                                    [por defecto: 5]              │
│ --in-place                    -i                                   Escribir en la misma carpeta  │
│                                                                    que el original.              │
│ --suffix                              <str>                        Sufijo para los nuevos        │
│                                                                    archivos (usado con           │
│                                                                    --in-place, ej: -ia).         │
│ --contexto,--context                  <str>                        classify: curso y nivel de    │
│                                                                    los estudiantes (calibra      │
│                                                                    Bloom y dificultad).          │
│ --concurrencia,--concurrency          <int>                        classify: solicitudes         │
│                                                                    simultáneas a Jev.            │
│                                                                    [por defecto: 4]              │
│ --reclasificar,--reclassify                                        classify: volver a clasificar │
│                                                                    las ya clasificadas.          │
│ --tags                                                             classify: escribir también    │
│                                                                    tags de Moodle (bloom:…,      │
│                                                                    dificultad-…).                │
│ --calibrar,--calibrate                <path>                       classify: comparar con una    │
│                                                                    referencia CSV                │
│                                                                    (archivo,titulo,bloom[,dific… │
│                                                                    sin escribir nada.            │
│ --revisar,--review                                                 classify: revisar en una      │
│                                                                    interfaz de terminal las      │
│                                                                    clasificaciones con poca      │
│                                                                    confianza (extra 'tui').      │
│ --umbral-revision,--review-…          <float range> [0.0<=x<=1.0]  classify --revisar: confianza │
│                                                                    por debajo de la cual se pide │
│                                                                    revisar (con 1, todas las     │
│                                                                    clasificadas).                │
│                                                                    [por defecto: 0.6]            │
│ --referencias,--references            <path>                       classify --revisar: CSV de    │
│                                                                    calibración al que se agregan │
│                                                                    las correcciones (el formato  │
│                                                                    de --calibrar).               │
│ --opciones,--options                  <int>                        distractors: cantidad de      │
│                                                                    opciones a alcanzar por       │
│                                                                    pregunta.                     │
│                                                                    [por defecto: 4]              │
│ --precio-entrada,--input-pr…          <float>                      USD por millón de tokens de   │
│                                                                    entrada, para estimar el      │
│                                                                    costo.                        │
│ --precio-salida,--output-pr…          <float>                      USD por millón de tokens de   │
│                                                                    salida, para estimar el       │
│                                                                    costo.                        │
│ --sin-cache,--no-cache                                             No usar ni guardar respuestas │
│                                                                    en la caché                   │
│                                                                    (~/.cache/voight).            │
│ --dry-run                     -n                                   Mostrar lo que se enviaría (y │
│                                                                    cuánto se ahorra) sin llamar  │
│                                                                    al modelo ni escribir         │
│                                                                    archivos.                     │
│ --help                        -h                                   Muestra esta ayuda y sale.    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight dedup`

```text
 Uso: voight dedup [OPCIONES] [paths]...

 Elimina preguntas duplicadas según un umbral de similitud (GIFT y Moodle XML).

 Sólo compara preguntas del mismo tipo y conserva, de cada grupo, la más completa;
 elimina las que son similares a ella por encima del umbral. Sin --aplicar sólo
 muestra lo que haría. Al aplicar, cada eliminación queda en --log con la ruta
 completa del archivo (de ella se infieren las categorías).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>  Archivos .gift/.xml o directorios.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                                                               Muestra instrucciones para   │
│                                                                     un LLM sobre este comando.   │
│ --recursive                    -r                                   Buscar recursivamente.       │
│ --similarity                   -s      <float range> [0.0<=x<=1.0]  Similitud mínima (0–1) para  │
│                                                                     considerar dos preguntas     │
│                                                                     duplicadas.                  │
│                                                                     [por defecto: 0.95]          │
│ --conservar,--keep                     <completa|primera>           Cuál se conserva de cada     │
│                                                                     grupo: la más completa       │
│                                                                     (feedback, título, opciones) │
│                                                                     o la primera.                │
│                                                                     [por defecto: completa]      │
│ --aplicar,--apply                                                   Eliminar de verdad (sin esta │
│                                                                     opción sólo se muestra lo    │
│                                                                     que se eliminaría).          │
│ --log                                  <path>                       Con --aplicar, log (TSV, se  │
│                                                                     agrega al final) de cada     │
│                                                                     pregunta eliminada con las   │
│                                                                     rutas completas.             │
│                                                                     [por defecto: dedup.log]     │
│ --confirmar-jev,--confirm-jev                                       Confirmar cada par con Jev   │
│                                                                     (TypeSafe): sólo quedan los  │
│                                                                     que evalúan exactamente lo   │
│                                                                     mismo.                       │
│ --desde,--since                        <str>                        Sólo los archivos cambiados  │
│                                                                     desde esta revisión git (y   │
│                                                                     los nuevos sin seguimiento). │
│ --respaldo,--backup-dir                <path>                       Con --aplicar, directorio    │
│                                                                     donde se guarda una copia    │
│                                                                     completa de cada archivo     │
│                                                                     modificado o borrado.        │
│                                                                     [por defecto:                │
│                                                                     dedup-respaldos]             │
│ --restaurar,--restore                  RESPALDO                     Deshacer un dedup: 'ultimo'  │
│                                                                     o el nombre de un respaldo   │
│                                                                     de --respaldo (no pisa       │
│                                                                     archivos editados después).  │
│ --forzar,--force                                                    Con --restaurar, pisar       │
│                                                                     también los archivos         │
│                                                                     editados después.            │
│ --tui                                                               Revisar los grupos en una    │
│                                                                     interfaz de terminal y       │
│                                                                     decidir cuáles eliminar      │
│                                                                     (extra 'tui').               │
│ --json                                                              Emite los grupos de          │
│                                                                     duplicados como JSON         │
│                                                                     versionado.                  │
│ --help                         -h                                   Muestra esta ayuda y sale.   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight verify`

```text
 Uso: voight verify [OPCIONES] [paths]...

 Compila y ejecuta el código de las preguntas de salida y compara con las opciones (gcc, javac).

 Sale con código 1 si la salida de alguna pregunta coincide con un distractor (clave
 equivocada), o si no compila, falla o no termina sin que la clave lo diga. Las que no
 aparecen literalmente en las opciones se listan para revisar, sin fallar.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>  Archivos .gift/.xml o directorios.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                                            Muestra instrucciones para un LLM sobre este    │
│                                                  comando.                                        │
│ --recursive                       -r             Buscar recursivamente.                          │
│ --todas,--all                                    Verificar toda pregunta con código, no sólo las │
│                                                  que piden la salida.                            │
│ --sanitizar,--sanitize                           C: compilar con -fsanitize=address,undefined    │
│                                                  para detectar comportamiento indefinido.        │
│ --estilo,--style                                 Revisar el código C con las reglas de estilo de │
│                                                  la cátedra (0x00XXh, requiere ripley). No       │
│                                                  cambia el código de salida.                     │
│ --concurrencia,--concurrency              <int>  Compilaciones simultáneas. [por defecto: 4]     │
│ --solo-problemas,--only-problems                 Listar sólo las preguntas con problemas.        │
│ --desde,--since                           <str>  Sólo los archivos cambiados desde esta revisión │
│                                                  git (y los nuevos sin seguimiento).             │
│ --json                                           Emite los resultados como JSON versionado.      │
│ --help                            -h             Muestra esta ayuda y sale.                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight catalogo`

```text
 Uso: voight catalogo [OPCIONES] {rutas}...

 Exporta un catálogo docente con enunciados, opciones y claves de respuesta.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Bancos GIFT/XML o directorios. [obligatorio]                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output  -o                    <path>  Catálogo Markdown (stdout por defecto).                  │
│ --titulo                        <str>   [por defecto: Catálogo de preguntas]                     │
│           -r  --no-recursive            [por defecto: r]                                         │
│ --json                                  Modelo de preguntas con referencias de origen.           │
│ --help    -h                            Muestra esta ayuda y sale.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight muestra`

```text
 Uso: voight muestra [OPCIONES] {rutas}...

 Selecciona una muestra reproducible para revisión docente (incluye las claves).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Bancos GIFT/XML o directorios. [obligatorio]                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --cantidad        -n                    <int range> [x>=1]  Cantidad exacta, sin reemplazo.      │
│                                                             [por defecto: 10]                    │
│ --semilla,--seed                        <int>               Misma semilla y banco: misma         │
│                                                             muestra.                             │
│                                                             [por defecto: 42]                    │
│ --output          -o                    <path>              Vista docente Markdown.              │
│                   -r  --no-recursive                        [por defecto: r]                     │
│ --json                                                      Muestra y semilla como JSON          │
│                                                             versionado.                          │
│ --help            -h                                        Muestra esta ayuda y sale.           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight split`

```text
 Uso: voight split [OPCIONES] [paths]...

 Divide archivos GIFT o Moodle XML con múltiples preguntas en archivos individuales.

 Sin -o, cada pregunta queda al lado del original. Con -o DIR, el banco se exporta a
 un árbol `DIR/<categoría>/<pregunta>.<ext>` (es la operación inversa a `unify`).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                         Muestra instrucciones para un LLM sobre este comando.              │
│ --recursive   -r              Procesar recursivamente.                                           │
│ --output-dir  -o      <path>  Exportar a un árbol de carpetas por categoría en este directorio   │
│                               (en lugar de dividir en el lugar).                                 │
│ --remove                      Borrar el archivo original después de dividirlo.                   │
│ --dry-run     -n              No crear ni borrar archivos; sólo contar.                          │
│ --json                        Emite el resultado como JSON versionado.                           │
│ --help        -h              Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight unify`

```text
 Uso: voight unify [OPCIONES] [paths]...

 Unifica árboles o grupos de archivos de preguntas (GIFT o XML) en un único archivo.

 Es la operación inversa a 'split' (también con -o): recopila preguntas
 recorriendo los directorios especificados, infiere y preserva las categorías,
 y genera un único banco monolítico (.gift o .xml).

 En Moodle XML, los bloques ```mermaid se renderizan con mermaid-cli (`mmdc`), los
 ```estructura y las fórmulas `$...$` con alucarD, y esos diagramas, las fórmulas y las
 imágenes con ruta relativa al archivo de la pregunta quedan como imágenes incrustadas en
 la salida, y los ```tabla, como tablas HTML. En GIFT no se pueden convertir: avisa qué
 archivos los tienen.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│    --llm                                          Muestra instrucciones para un LLM sobre este   │
│                                                   comando.                                       │
│ *  --output     -o                    <path>      Archivo de salida unificado (.gift o .xml).    │
│                                                   [obligatorio]                                  │
│    --format     -f                    <gift|xml>  Formato de salida (por defecto se deduce de la │
│                                                   extensión del archivo de salida).              │
│    --recursive  -r  --no-recursive                Procesar directorios recursivamente (por       │
│                                                   defecto True).                                 │
│                                                   [por defecto: r]                               │
│    --remove                                       Borrar los archivos fuente después de          │
│                                                   unificarlos.                                   │
│    --incrustar      --no-incrustar                XML: cambia los diagramas mermaid y de         │
│                                                   estructuras, las fórmulas y las imágenes       │
│                                                   relativas por imágenes incrustadas en la       │
│                                                   salida, y los ```tabla por tablas HTML.        │
│                                                   [por defecto: incrustar]                       │
│    --diagramas                        <png|svg>   Formato de imagen de los diagramas mermaid     │
│                                                   incrustados (las estructuras van siempre en    │
│                                                   SVG).                                          │
│                                                   [por defecto: png]                             │
│    --json                                         Emite el resultado como JSON versionado.       │
│    --help       -h                                Muestra esta ayuda y sale.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight synth`

```text
 Uso: voight synth [OPCIONES] [plantilla]

 daedalus en belmont: sintetiza preguntas de C verificadas con GCC.

 PLANTILLA es una de las generadoras incorporadas (ver --listar). Cada
 pregunta se crea con parámetros aleatorios, se compila y ejecuta de verdad
 para fijar la salida correcta, y se acompaña de distractores verosímiles.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   plantilla      <str>                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                               Muestra instrucciones para un LLM sobre este comando.        │
│ --cantidad,--count  -n      <int>   Cantidad de preguntas a sintetizar. [por defecto: 5]         │
│ --semilla,--seed    -s      <int>   Semilla pseudo-aleatoria (salida reproducible).              │
│                                     [por defecto: 42]                                            │
│ --output            -o      <path>  Archivo destino: .gift o .xml según la extensión.            │
│ --listar,--list                     Lista las plantillas disponibles y sale.                     │
│ --json                              Emite el resultado como JSON versionado.                     │
│ --help              -h              Muestra esta ayuda y sale.                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight ui`

```text
 Uso: voight ui [OPCIONES] [directorio]

 Abre el editor web local (cerebro) sobre DIRECTORIO.

 Permite navegar y editar preguntas en Moodle XML y GIFT desde el navegador.
 Requiere el extra 'ui': uv tool install "voight @ git+https://github.com/INGCOM-UNRN/voight"

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   directorio      <str>  [por defecto: .]                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                             Muestra instrucciones para un LLM sobre este comando.          │
│ --host                     <str>  Host del servidor web. [por defecto: 127.0.0.1]                │
│ --port                     <int>  Puerto del servidor web. [por defecto: 5000]                   │
│ --debug      --no-debug           Modo debug de Flask. [por defecto: no-debug]                   │
│ --help   -h                       Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight health`

```text
 Uso: voight health [OPCIONES] {rutas}...

 Audita la salud del banco: claves de corrección, feedback, cantidad y longitud de opciones, código
 y enlaces.

 Sale con código 1 si hay errores (lo que Moodle no importaría o importaría mal);
 con --estricto, también si hay advertencias.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Archivos .gift/.xml o directorios. [obligatorio]                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive                           -r               Buscar recursivamente en los directorios. │
│ --md                                          <path>   Exportar reporte en Markdown.             │
│ --min-opciones,--min-options                  <int>    Mínimo de opciones esperado en opción     │
│                                                        múltiple.                                 │
│                                                        [por defecto: 3]                          │
│ --umbral-longitud,--length-threshold          <float>  Razón de largo correcta/distractores a    │
│                                                        partir de la cual se advierte.            │
│                                                        [por defecto: 1.5]                        │
│ --max-items                                   <int>    Máximo de preguntas listadas por sección  │
│                                                        (0: todas).                               │
│                                                        [por defecto: 50]                         │
│ --estricto,--strict                                    Salir con código 1 también ante           │
│                                                        advertencias.                             │
│ --csv                                         <path>   Exportar una fila por pregunta con todas  │
│                                                        las señales (para planillas).             │
│ --desde,--since                               <str>    Sólo los archivos cambiados desde esta    │
│                                                        revisión git (y los nuevos sin            │
│                                                        seguimiento).                             │
│ --tui                                                  Recorrer los hallazgos y aplicar los      │
│                                                        arreglos en una interfaz de terminal      │
│                                                        (extra 'tui').                            │
│ --json                                                 Emite el diagnóstico como JSON            │
│                                                        versionado.                               │
│ --compilar,--compile                                   Certificar el código C de cada pregunta   │
│                                                        con daedalus (extra 'compilar'): errores, │
│                                                        advertencias y comportamiento indefinido  │
│                                                        son errores del banco.                    │
│ --permitir-warning                            <str>    Con --compilar: una advertencia que no    │
│                                                        rechaza la pregunta (sin -W:              │
│                                                        unused-parameter). Repetible.             │
│ --sin-ejecutar                                         Con --compilar: sólo compilar, sin        │
│                                                        ejecutar con sanitizers.                  │
│ --help                                -h               Muestra esta ayuda y sale.                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Subcomandos ────────────────────────────────────────────────────────────────────────────────────╮
│ stats          Genera estadísticas de un repositorio de preguntas (GIFT y Moodle XML).           │
│ similar        Encuentra preguntas similares o duplicadas en un repositorio (GIFT y Moodle       │
│                XML, también entre formatos).                                                     │
│ accesibilidad  Revisa texto alternativo de imágenes en enunciados, opciones y                    │
│                retroalimentación.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight config`

```text
 Uso: voight config [OPCIONES] COMANDO [ARGUMENTOS]...

 Configuración global: claves de los servicios, proveedor y modelo de IA.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ show     Muestra cada clave (oculta), de dónde sale y la configuración de IA efectiva.           │
│ get      Muestra el valor de una clave (los secretos, ocultos salvo --mostrar).                  │
│ set      Guarda una clave en ~/.voight/.env.                                                     │
│ unset    Quita una clave de ~/.voight/.env (las demás quedan).                                   │
│ models   Lista los modelos del proveedor de IA configurado.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight config show`

```text
 Uso: voight config show [OPCIONES]

 Muestra cada clave (oculta), de dónde sale y la configuración de IA efectiva.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --mostrar,--reveal            Mostrar los valores secretos completos.                            │
│ --help              -h        Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight config get`

```text
 Uso: voight config get [OPCIONES] {nombre}:<gemini-key|anthropic-key|typesafe-
                        key|moodle-token|moodle-url|proveedor|modelo>

 Muestra el valor de una clave (los secretos, ocultos salvo --mostrar).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    nombre      <gemini-key|anthropic-key|typesafe-key  Clave a mostrar. [obligatorio]          │
│                  |moodle-token|moodle-url|proveedor|mod                                          │
│                  elo>                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --mostrar,--reveal            Mostrar el valor secreto completo.                                 │
│ --help              -h        Muestra esta ayuda y sale.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight config set`

```text
 Uso: voight config set [OPCIONES] {nombre}:<gemini-key|anthropic-key|typesafe-
                        key|moodle-token|moodle-url|proveedor|modelo> [valor]

 Guarda una clave en ~/.voight/.env.

 Claves: gemini-key, anthropic-key, typesafe-key, moodle-token, moodle-url,
 proveedor (google, local, opencode, claude) y modelo.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    nombre      <gemini-key|anthropic-key|typesafe-key  Clave a guardar. [obligatorio]          │
│                  |moodle-token|moodle-url|proveedor|mod                                          │
│                  elo>                                                                            │
│      valor       <str>                                   Valor; si falta, se pide sin mostrarlo  │
│                                                          (así una clave no queda en el           │
│                                                          historial).                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight config unset`

```text
 Uso: voight config unset [OPCIONES] {nombre}:<gemini-key|anthropic-
                          key|typesafe-key|moodle-token|moodle-
                          url|proveedor|modelo>

 Quita una clave de ~/.voight/.env (las demás quedan).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    nombre      <gemini-key|anthropic-key|typesafe-key  Clave a quitar. [obligatorio]           │
│                  |moodle-token|moodle-url|proveedor|mod                                          │
│                  elo>                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight config models`

```text
 Uso: voight config models [OPCIONES]

 Lista los modelos del proveedor de IA configurado.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight convert`

```text
 Uso: voight convert [OPCIONES] COMANDO [ARGUMENTOS]...

 Comandos para convertir entre formatos.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm             Muestra instrucciones para un LLM sobre este comando.                          │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ html-to-md    Convierte tags HTML a Markdown en archivos XML o GIFT (los directorios,            │
│               recursivamente).                                                                   │
│ xml-to-gift   Convierte Moodle XML a GIFT: un archivo, stdin ('-') o directorios                 │
│               (recursivamente).                                                                  │
│ gift-to-xml   Convierte GIFT a Moodle XML: un archivo, stdin ('-') o directorios                 │
│               (recursivamente).                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight convert html-to-md`

```text
 Uso: voight convert html-to-md [OPCIONES] [paths]...

 Convierte tags HTML a Markdown en archivos XML o GIFT (los directorios, recursivamente).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r  --no-recursive      Recorrer los directorios recursivamente (por defecto, sí).  │
│                                      [por defecto: r]                                            │
│ --dry-run    -n                      No aplicar cambios                                          │
│ --help       -h                      Muestra esta ayuda y sale.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight convert xml-to-gift`

```text
 Uso: voight convert xml-to-gift [OPCIONES] [paths]...

 Convierte Moodle XML a GIFT: un archivo, stdin ('-') o directorios (recursivamente).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>  Archivos o directorios (sin nada o '-', stdin).                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output          -o                    <str>  Salida: con un archivo, el archivo GIFT (por      │
│                                                defecto, stdout); con un directorio o varias      │
│                                                rutas, el directorio donde se replica el árbol    │
│                                                (por defecto, al lado de cada original).          │
│ --recursive       -r  --no-recursive           Recorrer los directorios recursivamente (por      │
│                                                defecto, sí).                                     │
│                                                [por defecto: r]                                  │
│ --forzar,--force                               Reemplazar los archivos de salida que ya existen. │
│ --dry-run         -n                           Con un directorio, mostrar qué se convertiría sin │
│                                                escribir.                                         │
│ --help            -h                           Muestra esta ayuda y sale.                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight convert gift-to-xml`

```text
 Uso: voight convert gift-to-xml [OPCIONES] [paths]...

 Convierte GIFT a Moodle XML: un archivo, stdin ('-') o directorios (recursivamente).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>  Archivos o directorios (sin nada o '-', stdin).                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output          -o                    <str>  Salida: con un archivo, el archivo XML (por       │
│                                                defecto, stdout); con un directorio o varias      │
│                                                rutas, el directorio donde se replica el árbol    │
│                                                (por defecto, al lado de cada original).          │
│ --recursive       -r  --no-recursive           Recorrer los directorios recursivamente (por      │
│                                                defecto, sí).                                     │
│                                                [por defecto: r]                                  │
│ --forzar,--force                               Reemplazar los archivos de salida que ya existen. │
│ --dry-run         -n                           Con un directorio, mostrar qué se convertiría sin │
│                                                escribir.                                         │
│ --help            -h                           Muestra esta ayuda y sale.                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix`

```text
 Uso: voight fix [OPCIONES] COMANDO [ARGUMENTOS]...

 Todo lo que modifica archivos: formato (format), código, nombres, HTML, tags y ortografía
 (grammar).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm             Muestra instrucciones para un LLM sobre este comando.                          │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ slugify           Slugifica los nombres de los archivos (minúsculas, sin espacios ni acentos).   │
│ name-from-title   Renombra el archivo usando el título interno de la pregunta (slugificado).     │
│ extension         Corrige la extensión según el contenido: .xml con GIFT adentro pasa a .gift y  │
│                   viceversa.                                                                     │
│ title-from-name   Actualiza el título interno de la pregunta usando el nombre del archivo        │
│                   (sanitizado).                                                                  │
│ clean-html        Limpia el HTML obsoleto (<font>, <center>, <marquee>) y los estilos inline     │
│                   (GIFT y XML).                                                                  │
│ code-indent       Marca la indentación del código con · (un punto por espacio) en GIFT, XML y    │
│                   Markdown.                                                                      │
│ moodle            Deja los GIFT importables en Moodle: `` y `` en comentarios, `{}` y sin `:`    │
│                   sueltos.                                                                       │
│ code-chars        Convierte los caracteres del código entre normal y fullwidth (GIFT, XML y      │
│                   Markdown).                                                                     │
│ code-lang         Agrega la etiqueta de lenguaje (c, java, python) a los bloques ``` que no la   │
│                   tienen (GIFT, XML y Markdown).                                                 │
│ highlight         Resalta la sintaxis de los bloques ``` de C de un Moodle XML con HTML y CSS en │
│                   línea (sin scripts en el navegador).                                           │
│ code-format       Formatea el código C y Java de las preguntas con clang-format, conservando la  │
│                   convención de cada archivo.                                                    │
│ format            Formatea archivos GIFT y Moodle XML y transforma el código (fullwidth, · y ↵). │
│ format-init       Crea la plantilla de la sección format del .voight.toml en la raíz del árbol   │
│                   de preguntas.                                                                  │
│ clean-tags        Elimina tags de las preguntas XML.                                             │
│ grammar           Verifica y corrige ortografía y gramática en bancos GIFT y XML usando          │
│                   LanguageTool.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix slugify`

```text
 Uso: voight fix slugify [OPCIONES] [paths]...

 Slugifica los nombres de los archivos (minúsculas, sin espacios ni acentos).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix name-from-title`

```text
 Uso: voight fix name-from-title [OPCIONES] [paths]...

 Renombra el archivo usando el título interno de la pregunta (slugificado).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix extension`

```text
 Uso: voight fix extension [OPCIONES] [paths]...

 Corrige la extensión según el contenido: .xml con GIFT adentro pasa a .gift y viceversa.

 No pisa archivos existentes: si el destino ya existe, lo informa y sale con código 1.
 Los archivos cuyo contenido no se reconoce como GIFT ni como Moodle XML quedan como están.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --json                 Salida en JSON.                                                           │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix title-from-name`

```text
 Uso: voight fix title-from-name [OPCIONES] [paths]...

 Actualiza el título interno de la pregunta usando el nombre del archivo (sanitizado).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix clean-html`

```text
 Uso: voight fix clean-html [OPCIONES] [paths]...

 Limpia el HTML obsoleto (<font>, <center>, <marquee>) y los estilos inline (GIFT y XML).

 `voight health` informa los archivos que lo tienen.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix code-indent`

```text
 Uso: voight fix code-indent [OPCIONES] [paths]...

 Marca la indentación del código con · (un punto por espacio) en GIFT, XML y Markdown.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive          -r        Procesar recursivamente                                           │
│ --saltos,--newlines            Marcar también cada fin de línea con ↵.                           │
│ --dry-run            -n        No aplicar cambios                                                │
│ --help               -h        Muestra esta ayuda y sale.                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix moodle`

```text
 Uso: voight fix moodle [OPCIONES] [paths]...

 Deja los GIFT importables en Moodle: `` y `` en comentarios, `{}` y sin `:` sueltos.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix code-chars`

```text
 Uso: voight fix code-chars [OPCIONES] [paths]...

 Convierte los caracteres del código entre normal y fullwidth (GIFT, XML y Markdown).

 Sólo cambia los símbolos: la indentación con · y los ↵ de `code-indent` se conservan
 al volver a normal (salvo --sin-marcas), así que los dos comandos se combinan.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive       -r                               Procesar recursivamente                       │
│ --to-normal                                        Convertir a normal (default)                  │
│                                                    [por defecto: True]                           │
│ --to-fullwidth                                     Convertir a fullwidth                         │
│ --marcas,--marks      --sin-marcas,--no-marks      Con --to-fullwidth, agregar las marcas · y ↵; │
│                                                    con --to-normal, conservar las que hay (por   │
│                                                    defecto, sí). --sin-marcas con --to-normal    │
│                                                    las quita.                                    │
│                                                    [por defecto: marcas]                         │
│ --dry-run         -n                               No aplicar cambios                            │
│ --help            -h                               Muestra esta ayuda y sale.                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix code-lang`

```text
 Uso: voight fix code-lang [OPCIONES] [paths]...

 Agrega la etiqueta de lenguaje (c, java, python) a los bloques ``` que no la tienen (GIFT, XML y
 Markdown).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive            -r             Procesar recursivamente                                    │
│ --lenguaje,--language          <str>  Lenguaje para los bloques en los que no se puede detectar  │
│                                       (c, java, python…).                                        │
│ --dry-run              -n             No aplicar cambios                                         │
│ --help                 -h             Muestra esta ayuda y sale.                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix highlight`

```text
 Uso: voight fix highlight [OPCIONES] [paths]...

 Resalta la sintaxis de los bloques ``` de C de un Moodle XML con HTML y CSS en línea (sin scripts
 en el navegador).

 Cada bloque pasa a ser un `<pre>` con un `<span style="color:…">` por token, que se ve en la vista
 de cuestionarios de Moodle. En `format="markdown"` queda como HTML crudo y el resto del texto no
 cambia. Sólo Moodle XML: un GIFT se convierte antes con `voight convert gift-to-xml`.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix code-format`

```text
 Uso: voight fix code-format [OPCIONES] [paths]...

 Formatea el código C y Java de las preguntas con clang-format, conservando la convención de cada
 archivo.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive       -r             Procesar recursivamente                                         │
│ --estilo,--style          <str>  Estilo de clang-format (por defecto: LLVM con 4 espacios, regla │
│                                  0x0005h). Un estilo de llaves (allman, stroustrup, gnu, linux,  │
│                                  whitesmiths…) aplica esas llaves sobre el estilo por defecto.   │
│ --dry-run         -n             No aplicar cambios                                              │
│ --help            -h             Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix format`

```text
 Uso: voight fix format [OPCIONES] [paths]...

 Formatea archivos GIFT y Moodle XML y transforma el código (fullwidth, · y ↵).

 Los valores por defecto salen de la sección  del .voight.toml (o .voight)
 de la raíz del árbol, que `voight fix format-init` crea; una opción explícita gana.
 Con --check o --diff no escribe nada; --check sale con código 1 si algún archivo
 cambiaría (también si algún archivo no se pudo procesar).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                                                   Muestra instrucciones para un LLM sobre  │
│                                                         este comando.                            │
│ --recursive       -r                                    Procesar recursivamente                  │
│ --dry-run         -n                                    No aplicar cambios                       │
│ --code                                                  Marcar la indentación del código con ·   │
│                                                         (un punto por espacio)                   │
│ --fullwidth                                             Proteger el código: símbolos fullwidth y │
│                                                         marcas · (indentación) y ↵ (fin de       │
│                                                         línea)                                   │
│ --normal                                                Restaurar el código a caracteres         │
│                                                         normales (sin marcas)                    │
│ --marcas,--marks      --sin-marcas,--no-marks           Con --fullwidth, agregar las marcas · y  │
│                                                         ↵ (por defecto, sí).                     │
│                                                         [por defecto: marcas]                    │
│ --gaff                                                  Formatear el código C de los bloques ``` │
│                                                         con gaff (estilo de la cátedra):         │
│                                                         restaura los caracteres normales, aplica │
│                                                         `gaff fix` y vuelve a proteger el código │
│                                                         como estaba.                             │
│ --correct-first                                         Ordena las opciones de opción múltiple   │
│                                                         por porcentaje (la correcta primero).    │
│ --check                                                 No escribir: salir con código 1 si algún │
│                                                         archivo cambiaría (para CI y             │
│                                                         pre-commit).                             │
│ --diff                                                  No escribir: mostrar los cambios como    │
│                                                         diff unificado.                          │
│ --desde,--since                                  <str>  Sólo los archivos cambiados desde esta   │
│                                                         revisión git (y los nuevos sin           │
│                                                         seguimiento).                            │
│ --json                                                  Emite el resultado (archivos que cambian │
│                                                         y errores) como JSON versionado.         │
│ --help            -h                                    Muestra esta ayuda y sale.               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix format-init`

```text
 Uso: voight fix format-init [OPCIONES] [directorio]

 Crea la plantilla de la sección format del .voight.toml en la raíz del árbol de preguntas.

 Lleva todas las claves de formato con sus valores por defecto y una explicación de
 cada una. Si ya hay un .voight.toml o .voight en el directorio, agrega la sección
 al final; si ya tiene , no lo toca.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   directorio      <directory>  Raíz del árbol de preguntas (por defecto, el directorio actual).  │
│                                [por defecto: .]                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix clean-tags`

```text
 Uso: voight fix clean-tags [OPCIONES] [paths]...

 Elimina tags de las preguntas XML.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <str>                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --recursive  -r        Procesar recursivamente                                                   │
│ --dry-run    -n        No aplicar cambios                                                        │
│ --help       -h        Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight fix grammar`

```text
 Uso: voight fix grammar [OPCIONES] [paths]...

 Verifica y corrige ortografía y gramática en bancos GIFT y XML usando LanguageTool.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   paths      <path>                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm                             Muestra instrucciones para un LLM sobre este comando.          │
│ --server          -s      <str>   URL del servidor LanguageTool (por defecto                     │
│                                   http://localhost:8081 y API pública)                           │
│ --username        -u      <str>   Usuario / email de LanguageTool Premium                        │
│ --api-key         -k      <str>   API Key / Token de LanguageTool Premium                        │
│ --premium                         Forzar uso de la API LanguageTool Premium                      │
│ --lang            -l      <str>   Código de idioma (default: es-AR) [por defecto: es-AR]         │
│ --ignore-rules            <str>   Reglas a ignorar separadas por comas                           │
│ --ignore-words            <str>   Palabras a ignorar separadas por comas                         │
│ --fix             -f              Aplica correcciones ortográficas automáticas                   │
│ --md,--output-md          <path>  Genera reporte Markdown                                        │
│ --json                            Emite salida estructurada en formato JSON                      │
│ --help            -h              Muestra esta ayuda y sale.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight moodle`

```text
 Uso: voight moodle [OPCIONES] COMANDO [ARGUMENTOS]...

 Operaciones sobre un sitio Moodle (servicio web).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --llm             Muestra instrucciones para un LLM sobre este comando.                          │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ subir          Sube preguntas a un curso de Moodle (requiere el plugin                           │
│                local_questions_importer_ws).                                                     │
│ backup-quiz    Crea un backup de cuestionario (.mbz) con preguntas aleatorias por categoría.     │
│ inspeccionar   Inspecciona preguntas, categorías, cupos y configuración sin extraer ni           │
│                restaurar.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight moodle subir`

```text
 Uso: voight moodle subir [OPCIONES] {rutas}...

 Sube preguntas a un curso de Moodle (requiere el plugin local_questions_importer_ws).

 Convierte y unifica GIFT/XML en un Moodle XML, lo sube al área de borradores con
 webservice/upload.php y lo importa con local_questions_importer_ws_import_xml.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    rutas      <path>  Archivos .gift/.xml o directorios (las carpetas son categorías).         │
│                         [obligatorio]                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --url                                   <str>   URL del sitio Moodle (o MOODLE_URL).          │
│                                                    [variable de entorno: MOODLE_URL]             │
│                                                    [obligatorio]                                 │
│ *  --curso,--course                        <int>   id del curso destino (conviene uno de prueba  │
│                                                    para probar la importación).                  │
│                                                    [obligatorio]                                 │
│    --token                                 <str>   Token del servicio web (o MOODLE_TOKEN,       │
│                                                    también en ~/.voight/.env).                   │
│                      -r  --no-recursive            Recorrer los subdirectorios. [por defecto: r] │
│    --dry-run         -n                            Preparar el XML y mostrar qué se subiría, sin │
│                                                    contactar a Moodle.                           │
│    --guardar,--save                        <path>  Guardar también el Moodle XML que se sube.    │
│    --json                                          Emite el resultado como JSON versionado.      │
│    --help            -h                            Muestra esta ayuda y sale.                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight moodle backup-quiz`

```text
 Uso: voight moodle backup-quiz [OPCIONES] [rutas]...

 Crea un backup de cuestionario (.mbz) con preguntas aleatorias por categoría.

 Unifica las preguntas de la estructura de directorios y genera un paquete MBZ
 (Moodle 2 backup de actividad) listo para restaurar directamente en cualquier
 curso de Moodle sin requerir plugins externos ni web services.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│   rutas      <path>  Archivos .gift/.xml o directorios del repositorio.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --output                   -o                    <path>              Archivo .mbz de salida      │
│                                                                      (obligatorio salvo con      │
│                                                                      --plan).                    │
│ --titulo,--title           -t                    <str>               Título o nombre del         │
│                                                                      cuestionario.               │
│                                                                      [por defecto: Cuestionario] │
│ --plan                                                               Revisar cupos y             │
│                                                                      configuración sin generar   │
│                                                                      ningún MBZ.                 │
│ --preguntas-por-categoria  -k                    <int range> [x>=1]  Cantidad de preguntas       │
│                                                                      aleatorias a extraer por    │
│                                                                      cada categoría.             │
│                                                                      [por defecto: 1]            │
│                            -r  --no-recursive                        Recorrer los subdirectorios │
│                                                                      recursivamente.             │
│                                                                      [por defecto: r]            │
│ --tiempo-limite                                  <int>               Límite de tiempo en         │
│                                                                      segundos (por defecto 3600s │
│                                                                      = 1 hora).                  │
│                                                                      [por defecto: 3600]         │
│ --calificacion-maxima                            <float>             Calificación máxima del     │
│                                                                      cuestionario.               │
│                                                                      [por defecto: 10.0]         │
│ --intentos                                       <int>               Número de intentos          │
│                                                                      permitidos (1 por defecto). │
│                                                                      [por defecto: 1]            │
│ --shuffle                      --no-shuffle                          Barajar respuestas.         │
│                                                                      [por defecto: shuffle]      │
│ --json                                                               Emite el resultado como     │
│                                                                      JSON versionado.            │
│ --help                     -h                                        Muestra esta ayuda y sale.  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `voight moodle inspeccionar`

```text
 Uso: voight moodle inspeccionar [OPCIONES] {archivo}

 Inspecciona preguntas, categorías, cupos y configuración sin extraer ni restaurar.

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    archivo      <file>  Copia .mbz (tar o ZIP). [obligatorio]                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Resumen como JSON versionado.                                                  │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`voight@5aa1504`](https://github.com/INGCOM-UNRN/voight/tree/5aa1504).
