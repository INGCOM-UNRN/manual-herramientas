---
title: "scorm-tools"
subtitle: "Empaquetador y Validador SCORM 1.2 / 2004 para Moodle"
author: "Cátedra de Algoritmos y Programación"
date: "2026-09-14"
---

(manual-scorm-tools)=
# scorm-tools — Empaquetador y Validador SCORM 1.2 / 2004 para Moodle

:::{note} Resumen Técnico del Satélite

**Rol en el ecosistema:** Generación, validación formal y empaquetado de módulos
interactivos compatibles con el estándar SCORM (1.2 y 2004 4th Edition) listos
para su despliegue en plataformas LMS como Moodle.

:::
<!-- {note} Resumen Técnico del Satélite -->

---

## 1. Propósito y Alcance

`scorm-tools` provee una interfaz de línea de comandos para estructurar
contenidos web educativos bajo la norma SCORM sin requerir herramientas
propietarias. Valida esquemas XML de manifiesto (`imsmanifest.xml`) y empaqueta
los artefactos finales en archivos comprimidos `.zip`.

---

## 2. Instalación y Requisitos

La herramienta se ejecuta en entornos Linux/POSIX y requiere Python 3.10+
gestionado mediante `uv`:

``` bash
uv tool install "scorm-tools[ecosistema] @ git+https://github.com/INGCOM-UNRN/scorm-tools"
```
<!-- bash -->

---

## 3. Comandos CLI y Opciones

```{code-block} bash
:linenos:
# Inicializar un proyecto SCORM con plantilla declarativa
scorm-tools init mi_modulo --version 2004

# Validar la estructura y manifiesto XML contra esquemas XSD
scorm-tools validate mi_modulo/

# Empaquetar el recurso para Moodle
scorm-tools build mi_modulo/ --output paquete_scorm.zip

```
<!-- {code-block} bash -->

### Opciones Principales
* `--version [1.2|2004]`: Selecciona el estándar SCORM de destino.
* `--output, -o`: Ruta del archivo zip generado.
* `--strict`: Activa validación estricta de rutas de recursos locales.

---

(manual-scorm-tools-ejemplos)=
## Ejemplos y Contraejemplos

### Ejemplo Válido (Patrón Recomendado)

Inicializá un curso con el comando documentado por `scorm-tools` y conservá la
referencia entre el ítem de navegación y el recurso del SCO:

```{code-block} bash
scorm-tools init mi_curso --title "Introducción a punteros" --scorm-version 2004-4ed
scorm-tools build mi_curso/ --output mi_curso.zip
scorm-tools validate mi_curso.zip --md

```
<!-- {code-block} bash -->

El `scorm.yaml` generado incluye este vínculo coherente: `ITEM-1` referencia
`RES-1`, y `RES-1` declara el SCO `index.html` y sus archivos locales.

```{code-block} yaml
:linenos:
organizations:
  - identifier: ORG-1
    title: "Introducción a punteros"
    items:
      - identifier: ITEM-1
        title: "Módulo 1"
        resource: RES-1

resources:
  - identifier: RES-1
    href: index.html
    type: sco
    files:
      - index.html
      - scorm-api.js
      - style.css

```
<!-- {code-block} yaml -->

La plantilla de `scorm-tools init` declara ese manifiesto y `build` empaqueta el
contenido; `validate` verifica el paquete. El informe esperado termina con:

```{code-block} text
- **Estado:** ✓ **Válido**

```
<!-- {code-block} text -->

### Contraejemplo (Antipatrón o Caso Infractor)

No cambies el identificador del recurso en el ítem sin actualizar su destino.
Si reemplazás `resource: RES-1` por `resource: NOPE`, el ítem apunta a un
identificador inexistente:

```{code-block} yaml
:linenos:
organizations:
  - identifier: ORG-1
    title: "Introducción a punteros"
    items:
      - identifier: ITEM-1
        title: "Módulo 1"
        resource: NOPE

```
<!-- {code-block} yaml -->

Construí el paquete sin validación automática y ejecutá la validación para ver
el diagnóstico:

```{code-block} bash
scorm-tools build mi_curso/ --output mi_curso.zip --no-validate
scorm-tools validate mi_curso.zip

```
<!-- {code-block} bash -->

La validación rechaza la referencia e informa:

```{code-block} text
ERROR: El item 'ITEM-1' referencia el resource inexistente 'NOPE'.

```
<!-- {code-block} text -->
