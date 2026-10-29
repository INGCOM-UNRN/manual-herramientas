# Manual de Herramientas Docentes — Cátedra de Programación 1 (UNRN)

Repositorio oficial del sitio de documentación **MyST Markdown** para el **perfil docente** y la infraestructura técnica de la cátedra de Programación 1 (Universidad Nacional de Río Negro, Sede Andina).

A diferencia del `MANUAL_ESTUDIANTE` (orientado al entorno cotidiano del alumno en Linux/Windows), este sitio compendia todas las herramientas de autoría didáctica, evaluación masiva, supervisión de exámenes y análisis estático especializado.

---

## Estructura del Sitio

* **`ciclo_docente/`**: Guía integral del flujo de cursada (planificación didáctica con `deckard`, autoría de exámenes con `idkfa`/`alucarD`/`voight`, ingesta con `dredd`, evaluación masiva, detección de plagio Winnowing y coloquios).
* **`autoria/`**: Satélites de autoría (`deckard`, `alucard`, `idkfa`, `voight`, `moodle_toolbox`, `myst_tools`, `keymaker`, `scorm_tools`, `tyrell`, `corbel`).
* **`evaluacion/`**: Infraestructura de evaluación y gestión (`dredd`, `weyl`, `cyberdeck`, `meet_tools`, `slide_tools`, `gestion`, `p1_tools`).
* **`aula/`**: Entornos en VM, prácticas de laboratorio y control de exámenes (`construct`, `hardboiled`, `uatu_tools`).
* **`diagnostico_avanzado/`**: Verificación formal y análisis de fallos (`callahan`, `dietrich`, `vasquez`, `vassili`).
* **`analisis_estatico/`**: Satélites de cátedra para inspección profunda (`brett`, `crowe`, `drake`, `ferro`, `giger`, `holden`, `kane`, `motoko`, `parker`, `rachel`, `sebastian`, `wierzbowski`, `zhora`).

---

## Compilación y Previsualización Local

Para compilar y previsualizar el sitio con **MyST**:

```bash
# Compilar contenido del sitio
myst build --site

# Iniciar servidor local de desarrollo
myst start
```
