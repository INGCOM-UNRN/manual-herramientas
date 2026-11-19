---
title: "Manual Integral del Ciclo Docente"
short_title: "Manual Docente"
subtitle: "Planificación didáctica, autoría de exámenes, ingesta de entregas, autograding y actas"
---

(manual-integral-ciclo-docente)=
# Manual Integral del Ciclo Docente — Ecosistema P1
## Cátedra de Programación 1 — Universidad Nacional de Río Negro

Este manual documenta de forma exhaustiva el ciclo de trabajo completo del equipo docente: desde la planificación pedagógica y creación de guías de trabajos prácticos, pasando por la autoría procedural de exámenes y bancos de preguntas, hasta la ingesta masiva, evaluación automatizada, detección de plagio y publicación de devoluciones.

---

## 1. Arquitectura General del Ciclo Docente

El ecosistema articula las cinco etapas de la cursada universitaria:

```mermaid
flowchart TD
    subgraph Planificacion["1. Planificación y Autoría Didáctica"]
        DECKARD["deckard<br/>(Guías de TP, Bloom, Carga Horaria)"]
        MYST["myst-tools<br/>(Libros de cátedra y apuntes MyST)"]
        TYRELL["tyrell<br/>(Casos de prueba .in / .out)"]
    end

    subgraph Examenes["2. Autoría de Evaluaciones"]
        IDKFA["idkfa<br/>(Variantes anti-copia compiladas con GCC)"]
        ALUCARD["alucarD<br/>(Exámenes impresos Typst + OMR)"]
        MT["voight<br/>(Bancos de preguntas GIFT / Moodle XML)"]
    end

    subgraph Ingesta["3. Ingesta y Recepción de Entregas"]
        INGEST_MOODLE["dredd moodle ingest<br/>(ZIP masivo, SQLite, normalización UTF-8)"]
        INGEST_GH["dredd github clone<br/>(GitHub Classroom, aislamiento en repo/)"]
        SKELETON["Esqueleto dredd.yaml<br/>(Autogeneración en prácticas desconocidas)"]
    end

    subgraph Evaluacion["4. Evaluación Masiva y Auditoría"]
        EVAL["dredd eval (--all / individual)<br/>(Cero git pull, compilación, tests, AST)"]
        REPORTS["Informes i_hash/ y consolidados .md"]
        PLAGIARISM["dredd plagiarism<br/>(Huellas de Winnowing, matriz de similitud)"]
        WEYL["weyl<br/>(Comparación con la solución modelo y similitud del AST)"]
    end

    subgraph Devolucion["5. Devolución y Cierre de Actas"]
        COMMENT["dredd github comment<br/>(Publicación en Pull Requests)"]
        EXPORT["dredd export<br/>(CSV de notas, ZIP de devoluciones y dashboard)"]
        ORAL["dredd oral-guide<br/>(Guía personalizada para coloquios)"]
    end

    Planificacion --> Examenes
    Examenes --> Ingesta
    Ingesta --> Evaluacion
    Evaluacion --> Devolucion
```

---

## 2. Planificación Didáctica y Creación de Guías de TP

### 2.1 Banco de ejercicios y composición de guías con `deckard`
`deckard` mantiene un **banco atómico** de ejercicios (`banco/<id>/`): cada ejercicio declara su tema, su nivel de la Taxonomía de Bloom (1 a 6), los minutos estimados, el enunciado, la solución modelo y sus pruebas. Una guía no se escribe a mano ejercicio por ejercicio: se describe qué tiene que cubrir y `deckard compose` elige los ejercicios del banco que entran en esa carga.

**Especificación de la guía (`spec.yaml`, entrada de `deckard compose`):**
```yaml
nombre: "Guía 2 - Punteros"
duracion_min: 180          # duración de la práctica, en minutos
margen_carga: 0.8          # fracción de la duración que se usa (por omisión 0.8)
temas: [punteros, arreglos]
bloom_min: 2
bloom_max: 4
tipo_entrega: archivos_individuales   # o makefile, libreria, proyecto
```

**Guía compuesta (`guias/<nombre>/guia.yaml`, salida de `deckard compose`):**
```yaml
nombre: Guía 2 - Punteros
minutos_totales: 90
distribucion_bloom:
  COMPRENDER: 1
  APLICAR: 1
ejercicios:
- id: intercambiar-punteros
  minutos: 30
  bloom: 2
  tema: punteros
- id: estadisticas-arreglo
  minutos: 60
  bloom: 3
  tema: arreglos
```

**Comandos clave de `deckard`:**
```bash
# Crear banco/ y guias/ con un ejercicio de ejemplo
deckard init

# Componer la guía desde la especificación (escribe guias/<nombre>/guia.yaml)
deckard compose spec.yaml

# Auditar la completitud y calidad técnica de los ejercicios de la guía
deckard audit-guide guias/guía_2_-_punteros/guia.yaml

# Revisar la carga horaria acumulada y el balance Bloom
deckard check-load guias/guía_2_-_punteros/guia.yaml --max-horas 6.0

# Empaquetar la guía y sus casos de prueba como .ripkg para ripley
deckard pack guias/guía_2_-_punteros/ -o dist/practica_2.ripkg
```

Las opciones de cada comando están en el [manual de deckard](../autoria/deckard.md).

---

## 3. Autoría de Evaluaciones y Bancos de Preguntas

### 3.1 Generación Procedural de Exámenes con `idkfa`
`idkfa` combate la copia en evaluaciones parciales generando decenas de variantes únicas a partir de plantillas en C con parámetros aleatorizados deterministas. Compila y ejecuta cada variante con GCC embebido para asegurar que las opciones de respuesta calculadas sean exactas.

**Comandos clave de `idkfa`:**
```bash
# Generar 50 variantes únicas de un problema de tracing de punteros y
# exportarlas directamente como banco Moodle XML en la categoría indicada
idkfa -t templates/punteros_trace.c -n 50 -c "Parcial 1/Tracing Punteros" -o banco_parcial1.xml

# Solo generar el código C de las variantes (sin XML) para revisarlas antes
idkfa -t templates/punteros_trace.c -n 50 --generate-only
```

### 3.2 Maquetación Tipográfica de Exámenes con `alucarD`
Para evaluaciones presenciales en papel, `alucarD` toma el banco de preguntas y genera PDFs de alta calidad listos para imprimir mediante el motor tipográfico Typst, incluyendo hojas de respuesta OMR para corrección por escaneo óptico.

**Comandos clave de `alucarD`:**
```bash
# Generar examen impreso en PDF con 4 temas barajados y hoja OMR
alucard -d parcial1.yaml -n 4 -f pdf --omr -o impresiones/
```

### 3.3 Gestión de Bancos con `voight`
Permite convertir preguntas escritas en formato GIFT a XML de Moodle y viceversa, además de auditar categorías vacías o preguntas con errores de puntuación:
```bash
# Convertir archivo de preguntas GIFT a Moodle XML
voight convert gift-to-xml banco.gift --output banco.xml

# Validar integridad sintáctica del XML de Moodle
voight health validate banco.xml
```

---

## 4. Ingesta y Recepción de Entregas con `dredd`

`dredd` es el orquestador central docente. Soporta dos canales principales de entrega:

### 4.1 Canal A: Ingesta Masiva de Paquetes ZIP de Moodle
Cuando los estudiantes entregan en el Campus Virtual:
1. Descargá el archivo ZIP masivo desde Moodle (ej: `Entrega #4-1240320.zip`).
2. Ejecutá la ingesta:
   ```bash
   dredd moodle ingest Entrega #4-1240320.zip
   ```
3. **¿Qué realiza la ingesta automáticamente?**
   * **Descompresión recursiva**: Desempaqueta ZIPs anidados que los alumnos hayan subido.
   * **Aplanado inteligente**: Elimina carpetas envolventes redundantes creadas por sistemas operativos (`__MACOSX`, `.vscode`, carpetas anidadas con el nombre del alumno).
   * **Normalización de encodings**: Convierte archivos en `CP1252`, `ISO-8859-1` o `ASCII` a `UTF-8` estricto con finales de línea UNIX (`\n`).
   * **Auditoría de binarios prohibidos**: Si el estudiante subió archivos binarios compilados (`.o`, `.exe`, `.a`), `dredd` los filtra y registra la infracción pedagógica `0x000Fh`.
   * **Versionado SHA-256 en SQLite**: Si el alumno ya tenía una entrega previa (`r1`), calcula los hashes de los fuentes y, si cambiaron, genera limpiamente la revisión `r2` en `.metadata.db`.
   * **Detección de Prácticas Desconocidas**: Si el ZIP no tiene una regla asociada en `dredd.yaml`, `dredd` genera automáticamente un esqueleto de configuración en `dredd.yaml` y emite una advertencia en terminal indicando que debe asociarse la guía Deckard correspondiente.

### 4.2 Canal B: Entregas en GitHub Classroom
Para prácticas gestionadas con repositorios Git:
```bash
# Clonar o actualizar la entrega de un estudiante en <practica>/<estudiante>/repo
dredd github clone TP0 TP0-Enehuen https://github.com/INGCOM-UNRN-P1/p1-2026-tp0-2026-enehuen

# Reparar o abrir el Pull Request de corrección si el estudiante no lo creó
dredd github pr-fix TP0 TP0-Enehuen https://github.com/INGCOM-UNRN-P1/p1-2026-tp0-2026-enehuen
```
* **Aislamiento de Git**: El repositorio del alumno se aloja en el subdirectorio `repo/`, manteniendo el árbol Git puro e intacto.
* **Archivos de informe desacoplados**: Los informes de corrección y carpetas de auditoría se ubican en la carpeta del estudiante sin ensuciar el repositorio Git clonado.

---

## 5. Evaluación Automatizada (`dredd eval`)

La evaluación ejecuta el toolchain de cátedra sobre las entregas descargadas **sin alterar el repositorio Git local (cero `git pull`)**.

### 5.1 Comandos de Evaluación
```bash
# Evaluar un estudiante puntual
dredd eval TP0 TP0-Enehuen

# Evaluar a toda la cohorte presente en el workspace
dredd eval TP0 --all

# Limitar a modo simulación (las primeras 3 entregas)
dredd eval TP0 --all --dry-run

# Re-evaluar desde cero, descartando los resultados previos
dredd eval TP0 --all --force

# Especificar un directorio de plantillas de cátedra (_baseline) para ignorar ejercicios no tocados
dredd eval TP0 --all --baseline ./_baseline
```

### 5.2 Estructura del Informe de Corrección
Para cada estudiante y commit evaluado se generan:
1. **Directorio intermedio `i_<shorthash>/`** (o `r1i/` en Moodle):
   * `compilacion.log`: Registro completo de la salida cruda de compilación con número de revisión/commit.
   * `daedalus.md`: Diagnósticos de compilación traducidos.
   * `gaff.md`: Hallazgos de estilo (indentación, retornos, nombres).
   * `ripley.md`: Verificación de reglas pedagógicas y AST.
   * `valgrind.md` / `nostromo.md`: Consumo de memoria y fugas detectadas.
2. **Informe consolidado `<estudiante>_<shorthash>.md`**:
   Documento Markdown listo para el estudiante con encabezado, tabla de ejercicios, advertencias de compilación explicadas, estado de casos de prueba y recomendaciones de mejora.

---

## 6. Detección de Plagio y Copias con `dredd plagiarism`

`dredd` integra un motor nativo de detección de similitud basado en el algoritmo de huellas **Winnowing**:
* Pasa el código por un lexer que normaliza identificadores y quita espacios y comentarios; con `--strip-template` quita además el código que dio la cátedra.
* Genera k-gramas y huellas criptográficas de los fragmentos de código.
* Compara todas las parejas de estudiantes en una matriz de similitud.

```bash
# Analizar plagio con un umbral de sospecha del 60%
dredd plagiarism TP0 --threshold 0.60

# Exportar el reporte HTML con la matriz de similitud y el diff lado a lado
dredd plagiarism TP0 --threshold 0.60 --html similitud_TP0.html

# Cruzar cada par con la similitud del AST de weyl (renombrar o reordenar no la oculta)
dredd plagiarism TP0 --estructural --umbral-estructural 90
```

Una similitud alta es un indicio para revisar a mano, no una prueba de copia.

---

## 7. Devolución de Feedback y Cierre de Calificaciones

### 7.1 Publicación Automatizada en GitHub
```bash
# Publicar el informe generado como comentario en el PR del estudiante
dredd github comment TP0 TP0-Enehuen

# Publicar y abrir la vista de cambios en el navegador
dredd github comment TP0 TP0-Enehuen --open
```

### 7.2 Exportación de Notas para Moodle
Al concluir la corrección de la cohorte:
```bash
dredd export TP0
```
Este comando produce tres artefactos en la carpeta de la actividad (cada ruta se puede cambiar con `--csv`, `--zip` y `--dashboard`):
1. `moodle_grades.csv`: las calificaciones, para importar en el calificador de Moodle.
2. `retroalimentacion_moodle.zip`: los informes individuales, para la subida masiva de devoluciones al campus.
3. `dashboard.md`: el tablero de la cohorte, con sus métricas.

Para el paquete de devoluciones en HTML que espera la tarea de Moodle está `dredd moodle paquete`, y para el acta del SIU Guaraní, `dredd export-guarani`.

### 7.3 Preparación de Coloquios Orales
Para defensas de trabajos prácticos o exámenes orales:
```bash
dredd oral-guide TP0/TP0-Enehuen/repo --alumno "Enehuen" --ejercicio TP0 -o coloquio_enehuen.md
```
Genera un guion de preguntas personalizadas para el docente, basadas en las construcciones dudosas, funciones complejas o advertencias encontradas en el código de ese estudiante en particular.
