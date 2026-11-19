# Manual de Herramientas Docentes — Cátedra de Programación 1 (UNRN)

Repositorio oficial del sitio de documentación **MyST Markdown** para el **perfil docente** y la infraestructura técnica de la cátedra de Programación 1 (Universidad Nacional de Río Negro, Sede Andina).

A diferencia del `MANUAL_ESTUDIANTE` (orientado al entorno cotidiano del alumno en Linux/Windows), este sitio compendia todas las herramientas de autoría didáctica, evaluación masiva, supervisión de exámenes y análisis estático especializado.

---

## Catálogo por rol

El [catálogo por rol](catalogo_por_rol.md) reúne los componentes del manifiesto de `p1-tools`, incluidos los perfiles de estudiante, contenido, docente, aula y análisis, con enlaces y estado.

## Estructura del Sitio

* **`ciclo_docente/`**: Guía integral del flujo de cursada (planificación didáctica con `deckard`, autoría de exámenes con `idkfa`/`alucarD`/`voight`, ingesta con `dredd`, evaluación masiva, detección de plagio Winnowing y coloquios).
* **`autoria/`**: Satélites de autoría (`deckard`, `alucard`, `idkfa`, `voight`, `moodle_toolbox`, `myst_tools`, `scorm_tools`, `tyrell`, `corbel`).
* **`evaluacion/`**: Infraestructura de evaluación y gestión (`dredd`, `weyl`, `cyberdeck`, `meet_tools`, `slide_tools`, `gestion`, `p1_tools`).
* **`aula/`**: Entornos en VM, prácticas de laboratorio y control de exámenes (`construct`, `hardboiled`, `uatu_tools`).
* **`diagnostico_avanzado/`**: Verificación formal y análisis de fallos (`callahan`, `dietrich`, `vasquez`, `vassili`).
* **`analisis_estatico/`**: Satélites de cátedra para inspección profunda (`brett`, `crowe`, `drake`, `ferro`, `giger`, `holden`, `kane`, `motoko`, `parker`, `rachel`, `sebastian`, `wierzbowski`, `zhora`).

---

## Páginas generadas

Las páginas de cada herramienta se generan desde su README y desde la ayuda real de su CLI, con los repositorios clonados junto a este y su entorno creado (`uv sync`):

```bash
python3 scripts/generar_paginas.py actualizar            # todas
python3 scripts/generar_paginas.py actualizar ferro      # una
python3 scripts/generar_paginas.py verificar             # falla si alguna quedó desactualizada
```

Llevan la marca «Generado por scripts/generar_paginas.py»: los cambios se hacen en el README de la herramienta y se regenera. Se escriben a mano la portada, el catálogo por rol, los índices de sección, el manual integral del ciclo docente y la página de `gestion` (Apps Script, sin README).

## Compilación y Previsualización Local

Para compilar y previsualizar el sitio con **MyST**:

```bash
# Compilar contenido del sitio
myst build --html

# Iniciar servidor local de desarrollo
myst start
```

---

## Despliegue Continuo

El sitio se compila y despliega automáticamente en GitHub Pages mediante GitHub Actions en cada push a la rama `main` (definido en `.github/workflows/deploy.yml`). El repositorio debe tener configurado en **Settings > Pages > Build and deployment > Source** la opción **GitHub Actions**.

## Contacto

Martín René Vilugrón - mrvilugron@unrn.edu.ar - Ingeniería en Computación UNRN Andina
