---
title: "Catálogo por rol"
subtitle: "Herramientas, recursos y perfiles del ecosistema"
---

# Catálogo por rol

Este catálogo reúne los componentes del [manifiesto de p1-tools](https://github.com/INGCOM-UNRN-P1/toolbox/blob/main/ecosistema.toml), agrupados por sus perfiles de uso; se excluyen los componentes retirados. Una herramienta puede aparecer en varios roles. Las páginas del manual ofrecen contexto adicional; los repositorios enlazados son la referencia para comandos, requisitos y estado actualizado.

Los perfiles son categorías de aprovisionamiento, no permisos exclusivos. `mother listar --perfil estudiante` permite consultar el manifiesto disponible; `mother instalar --perfil estudiante` instala los componentes compatibles. Las bibliotecas, plantillas, extensiones y otros recursos no son necesariamente comandos instalables con `mother`.

## Estudiantes (`estudiante`)

| Componente | Función | Tipo y estado |
| :--- | :--- | :--- |
| [daedalus](https://github.com/INGCOM-UNRN-P1/daedalus) | Compila C y explica diagnósticos de GCC y Clang. | cli |
| [gaff](https://github.com/INGCOM-UNRN-P1/gaff) | Revisa estilo y convenciones de C. | cli |
| [hal](https://github.com/INGCOM-UNRN-P1/hal) | Analiza fallos y volcados de memoria. | cli |
| [bishop](https://github.com/INGCOM-UNRN-P1/bishop) | Visualiza pila, heap y ejecución de programas C. | cli |
| [spunkmeyer](https://github.com/INGCOM-UNRN-P1/spunkmeyer) | Detecta antipatrones didácticos en C. | cli |
| [kaneda](https://github.com/INGCOM-UNRN-P1/kaneda) | Audita funciones inseguras y problemas de seguridad en C. | cli |
| [nostromo](https://github.com/INGCOM-UNRN-P1/nostromo) | Ejecuta programas y pruebas en un entorno aislado. | cli |
| [ripley](https://github.com/INGCOM-UNRN-P1/ripley) | Orquesta verificaciones pedagógicas para proyectos C. | cli |
| [mother](https://github.com/INGCOM-UNRN-P1/mother) | Instala, actualiza y diagnostica herramientas por perfil. | cli |
| [jonesy](https://github.com/INGCOM-UNRN-P1/jonesy) | Depurador visual para programas C. | binario |
| [construct](https://github.com/INGCOM-UNRN-P1/construct) | Entorno pedagógico que ejecuta una máquina virtual con QEMU. | cli |
| [yutani](https://github.com/INGCOM-UNRN-P1/yutani) | Biblioteca común de infraestructura para las herramientas. | biblioteca |
| [entorno](https://github.com/INGCOM-UNRN-P1/entorno) | Entorno portable de desarrollo para C y Python. | entorno |
| [plantilla-TP](https://github.com/INGCOM-UNRN-P1/plantilla-TP) | Plantilla para trabajos prácticos. | plantilla |
| [plantilla-final](https://github.com/INGCOM-UNRN-P1/plantilla-final) | Plantilla para trabajos finales. | plantilla |
| [plantilla-libreria](https://github.com/INGCOM-UNRN-P1/plantilla-libreria) | Plantilla para bibliotecas. | plantilla |
| [treadstone](https://github.com/INGCOM-UNRN-P1/treadstone) | Biblioteca C de apoyo para la cursada. | libreria-c |
| [bitmaps](https://github.com/INGCOM-UNRN-P1/bitmaps) | Biblioteca C para imágenes bitmap. | libreria-c |
| [sonido](https://github.com/INGCOM-UNRN-P1/sonido) | Biblioteca C para trabajar con sonido. | libreria-c |

## Autoría de contenidos (`contenido`)

| Componente | Función | Tipo y estado |
| :--- | :--- | :--- |
| [deckard](https://github.com/INGCOM-UNRN/deckard) | Curaduría y composición de guías de ejercicios. | cli |
| [alucarD](https://github.com/INGCOM-UNRN/alucarD) | Genera exámenes y variantes imprimibles. | cli |
| [idkfa](https://github.com/INGCOM-UNRN-P1/idkfa) | Herramientas para generar variantes de ejercicios. | cli |
| [voight](https://github.com/INGCOM-UNRN/voight) | Gestiona bancos de preguntas GIFT y Moodle XML. | cli |
| [myst-tools](https://github.com/martinvilu/mystmd-tools) | Herramientas para mantenimiento de contenidos MyST. | cli |
| [scorm-tools](https://github.com/INGCOM-UNRN/scorm-tools) | Herramientas para paquetes SCORM. | cli |
| [hardboiled](https://github.com/INGCOM-UNRN-P1/hardboiled) | Emulador pedagógico RISC-V con periféricos. | cli |
| [apunte](https://github.com/INGCOM-UNRN-P1/INGCOM-UNRN-P1.github.io) | Material de estudio de la cursada. | contenido |
| [mother](https://github.com/INGCOM-UNRN-P1/mother) | Instala, actualiza y diagnostica herramientas por perfil. | cli |
| [yutani](https://github.com/INGCOM-UNRN-P1/yutani) | Biblioteca común de infraestructura para las herramientas. | biblioteca |
| `smoke_scorm` | Ejemplo de verificación de paquetes SCORM. | ejemplo |

## Docencia y evaluación (`docente`)

| Componente | Función | Tipo y estado |
| :--- | :--- | :--- |
| [ripley](https://github.com/INGCOM-UNRN-P1/ripley) | Orquesta verificaciones pedagógicas para proyectos C. | cli |
| [weyl](https://github.com/INGCOM-UNRN-P1/weyl) | Compara funciones de archivos C mediante extracción textual; no construye AST. | cli |
| [dredd](https://github.com/INGCOM-UNRN-P1/dredd) | Orquesta la evaluación de entregas y el seguimiento de cohortes. | cli |
| [uatu-tools](https://github.com/INGCOM-UNRN-P1/uatu-tools) | Administración y auditoría de exámenes con uatu. | cli |
| [deckard](https://github.com/INGCOM-UNRN/deckard) | Curaduría y composición de guías de ejercicios. | cli |
| [alucarD](https://github.com/INGCOM-UNRN/alucarD) | Genera exámenes y variantes imprimibles. | cli |
| [idkfa](https://github.com/INGCOM-UNRN-P1/idkfa) | Herramientas para generar variantes de ejercicios. | cli |
| [voight](https://github.com/INGCOM-UNRN/voight) | Gestiona bancos de preguntas GIFT y Moodle XML. | cli |
| [mother](https://github.com/INGCOM-UNRN-P1/mother) | Instala, actualiza y diagnostica herramientas por perfil. | cli |
| [sulaco](https://github.com/INGCOM-UNRN-P1/sulaco) | Workflows reutilizables de corrección y auditoría en GitHub Actions. | workflows |
| [corpus](https://github.com/INGCOM-UNRN-P1/corpus) | Casos reales y sintéticos para verificar los analizadores. | datos |
| [yutani](https://github.com/INGCOM-UNRN-P1/yutani) | Biblioteca común de infraestructura para las herramientas. | biblioteca |
| [p1-tools](https://github.com/INGCOM-UNRN-P1/toolbox) | Manifiesto y documentación del ecosistema. | documentacion |
| [gestion](https://github.com/martinvilu/gestion) | Aplicaciones de apoyo a la gestión docente. | apps-script |

## Aula y exámenes (`aula`)

| Componente | Función | Tipo y estado |
| :--- | :--- | :--- |
| [uatu-tools](https://github.com/INGCOM-UNRN-P1/uatu-tools) | Administración y auditoría de exámenes con uatu. | cli |
| [meet-tools](https://github.com/martinvilu/meet-tools) | Herramientas para clases con Google Meet. | cli |
| [slide-tools](https://github.com/martinvilu/slides-tools) | Herramientas para presentaciones con Google Slides. | cli |
| [mother](https://github.com/INGCOM-UNRN-P1/mother) | Instala, actualiza y diagnostica herramientas por perfil. | cli |
| [yutani](https://github.com/INGCOM-UNRN-P1/yutani) | Biblioteca común de infraestructura para las herramientas. | biblioteca |
| [cast-tools-common](https://github.com/martinvilu/cast-tools-common) | Biblioteca compartida por las herramientas de transmisión. | biblioteca |
| [uatu](https://github.com/INGCOM-UNRN-P1/uatu) | Extensión de VS Code para registrar evidencia verificable en exámenes. | extension-vscode |
| [uatu-demo](https://github.com/INGCOM-UNRN-P1/uatu-demo) | Ejemplo de examen supervisado con uatu. | ejemplo |
| [grid](https://github.com/INGCOM-UNRN-P1/grid) | Extensión de VS Code deprecada; sus funciones pertinentes están en uatu. | extension-vscode; **deprecado** |
| `cyberdeck` | Aplicación Android de periféricos para hardboiled; el manifiesto aún la clasifica como especificación. | especificacion; **especificacion** |

## Análisis y diagnóstico (`analisis`)

| Componente | Función | Tipo y estado |
| :--- | :--- | :--- |
| [daedalus](https://github.com/INGCOM-UNRN-P1/daedalus) | Compila C y explica diagnósticos de GCC y Clang. | cli |
| [gaff](https://github.com/INGCOM-UNRN-P1/gaff) | Revisa estilo y convenciones de C. | cli |
| [hal](https://github.com/INGCOM-UNRN-P1/hal) | Analiza fallos y volcados de memoria. | cli |
| [bishop](https://github.com/INGCOM-UNRN-P1/bishop) | Visualiza pila, heap y ejecución de programas C. | cli |
| [spunkmeyer](https://github.com/INGCOM-UNRN-P1/spunkmeyer) | Detecta antipatrones didácticos en C. | cli |
| [kaneda](https://github.com/INGCOM-UNRN-P1/kaneda) | Audita funciones inseguras y problemas de seguridad en C. | cli |
| [nostromo](https://github.com/INGCOM-UNRN-P1/nostromo) | Ejecuta programas y pruebas en un entorno aislado. | cli |
| [ripley](https://github.com/INGCOM-UNRN-P1/ripley) | Orquesta verificaciones pedagógicas para proyectos C. | cli |
| [brett](https://github.com/INGCOM-UNRN-P1/brett) | Auditoría de empaquetado de memoria (*padding*), alineación natural y orden de campos en estructuras (`struct`). | cli |
| [callahan](https://github.com/INGCOM-UNRN-P1/callahan) | Componente de tipo cli del ecosistema. | cli |
| [corbel](https://github.com/INGCOM-UNRN-P1/corbel) | Herramienta para documentación y visualización de interfaces C. | cli |
| [crowe](https://github.com/INGCOM-UNRN-P1/crowe) | Linter de portabilidad multi-arquitectura, dependencias de *endianness* y anchos de tipos enteros de ancho variable. | cli |
| [dietrich](https://github.com/INGCOM-UNRN-P1/dietrich) | Componente de tipo cli del ecosistema. | cli |
| [drake](https://github.com/INGCOM-UNRN-P1/drake) | Fuzzer guiado por límites para evaluación de robustez ante valores de frontera. | cli |
| [ferro](https://github.com/INGCOM-UNRN-P1/ferro) | Perfilado de rendimiento por contadores de ciclos de hardware y optimización de microarquitectura. | cli |
| [giger](https://github.com/INGCOM-UNRN-P1/giger) | Extractor de grafos de llamadas (*Call Graphs*), análisis de alcanzabilidad y detección de código muerto. | cli |
| [holden](https://github.com/INGCOM-UNRN-P1/holden) | Generación automática de mocks, stubs e inyección de fallos a nivel de enlazador (`ld --wrap`). | cli |
| [kane](https://github.com/INGCOM-UNRN-P1/kane) | Inspección forense de binarios compilados, secciones ELF y mapeo de layouts de memoria. | cli |
| [motoko](https://github.com/INGCOM-UNRN-P1/motoko) | Verificación de encapsulamiento estricto y ocultamiento de información en Tipos de Datos Abstractos (TDA). | cli |
| [parker](https://github.com/INGCOM-UNRN-P1/parker) | Auditor de interfaces binarias de aplicación (ABI) y visibilidad de símbolos exportados en bibliotecas dinámicas. | cli |
| [rachel](https://github.com/INGCOM-UNRN-P1/rachel) | Desensamblador guiado y análisis de complejidad ciclomática en sentencias `switch` y *jump tables*. | cli |
| [sebastian](https://github.com/INGCOM-UNRN-P1/sebastian) | Análisis estático de consumo de *stack frames* y detección de riesgos de recursión profunda descontrolada. | cli |
| [tetsuo](https://github.com/INGCOM-UNRN-P1/tetsuo) | Componente de tipo cli del ecosistema. | cli |
| [tyrell](https://github.com/INGCOM-UNRN-P1/tyrell) | Genera casos de prueba deterministas de entrada y salida. | cli |
| [vasquez](https://github.com/INGCOM-UNRN-P1/vasquez) | Componente de tipo cli del ecosistema. | cli |
| [vassili](https://github.com/INGCOM-UNRN-P1/vassili) | Componente de tipo cli del ecosistema. | cli |
| [weyl](https://github.com/INGCOM-UNRN-P1/weyl) | Compara funciones de archivos C mediante extracción textual; no construye AST. | cli |
| [wierzbowski](https://github.com/INGCOM-UNRN-P1/wierzbowski) | Auditoría de grafos de inclusión de encabezados (`#include`) y verificación de reglas en Makefiles. | cli |
| [zhora](https://github.com/INGCOM-UNRN-P1/zhora) | Auditor de seguridad y buenas prácticas en macros complejas de preprocesador C. | cli |
| [mother](https://github.com/INGCOM-UNRN-P1/mother) | Instala, actualiza y diagnostica herramientas por perfil. | cli |
| [yutani](https://github.com/INGCOM-UNRN-P1/yutani) | Biblioteca común de infraestructura para las herramientas. | biblioteca |

## Fuera de los perfiles

`puppetmaster` figura en el manifiesto como proyecto Android **ajeno**, sin perfil asignado: [repositorio](https://github.com/martinvilu/puppetmaster).

El estado indicado procede del manifiesto local de `p1-tools`. En particular, `grid` está deprecado. Cyberdeck tiene una aplicación Android documentada en su repositorio local, aunque el manifiesto todavía la clasifica como especificación.
