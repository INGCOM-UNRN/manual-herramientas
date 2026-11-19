---
title: "Evaluación y Gestión Docente Masiva"
short_title: "Índice"
subtitle: "Infraestructura para autograding batch, comparación de código C, telemetría y cierre de notas"
---

(evaluacion-gestion-indice)=
# Evaluación y Gestión Docente Masiva

Infraestructura de cátedra para la calificación por lotes de entregas estudiantiles, comparación de funciones C, detección de plagio por algoritmo de Winnowing, integración continua con Moodle y GitHub Classroom, y orquestación del repositorio docente.

---

## Satélites de Evaluación y Gestión

* **[dredd](dredd.md)**: Orquestador docente de evaluación masiva: ingesta de entregas de Moodle y GitHub Classroom, corrección con el toolchain de la cátedra, similitud Winnowing, devoluciones y exportación de notas.
* **[weyl](weyl.md)**: Comparación de código C función por función contra la solución modelo (extracción textual) y similitud estructural sobre el AST de Tree-Sitter (`weyl similarity`, `weyl cohort`).
* **[cyberdeck](cyberdeck.md)**: Aplicación Android de periféricos (sensores y pulsadores) para placas emuladas con `hardboiled --remote`.
* **[meet-tools](meet_tools.md)**: Control remoto de Google Meet (micrófono, cámara, mano, admitir, silenciar) desde el teléfono o hardware Wi-Fi, con una extensión de navegador y un daemon local.
* **[slide-tools](slide_tools.md)**: Control remoto de Google Slides (avance, pantalla negra, láser, temporizador) desde el teléfono o hardware Wi-Fi, con una extensión de navegador y un daemon local.
* **[gestion](gestion.md)**: Planilla de cátedra en Google Apps Script: entregas de GitHub Classroom, comentarios de PR, permisos, correos y asistencia.
* **[p1-tools](p1_tools.md)**: Repositorio central del ecosistema: manifiesto (`ecosistema.toml`), lineamientos, scripts de clonado, instalación y salud, y manuales.
