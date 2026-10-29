---
title: "Manual del Ecosistema de Herramientas Docentes"
short_title: "Manual Docente"
subtitle: "Documentación integral del ciclo de cátedra, autoría pedagógica, evaluación masiva y supervisión técnica"
---

(manual-herramientas-docente)=
# Manual del Ecosistema de Herramientas Docentes

Este sitio aloja la documentación exhaustiva de las herramientas, flujos de trabajo y protocolos de la cátedra de **Programación 1 (UNRN Andina)** correspondientes al **perfil docente** y a la infraestructura de soporte académico (`docente`, `contenido`, `aula` y `analisis`).

A diferencia del [Manual del Estudiante](https://github.com/INGCOM-UNRN-P1/p1-tools/blob/main/MANUAL_ESTUDIANTE.md) (enfocado en el entorno cotidiano del alumno con GCC, Ripley, Daedalus y Gaff), este compendio reúne los componentes requeridos para la autoría didáctica, la síntesis anti-copia, la ingesta masiva de entregas, la evaluación automatizada y la verificación formal de software en C.

---

## Estructura del Sitio

| Módulo | Propósito Operativo | Herramientas Clave |
| :--- | :--- | :--- |
| **[1. Ciclo Docente](ciclo_docente/index.md)** | Arquitectura transversal del ciclo de cursada: planificación, exámenes, ingesta, autograding y actas. | `dredd`, `deckard`, `idkfa`, `weyl` |
| **[2. Autoría Didáctica](autoria/index.md)** | Curaduría de guías según Taxonomía de Bloom, generación procedural de variantes, maquetación Typst y bancos Moodle. | `deckard`, `alucarD`, `idkfa`, `voight`, `myst-tools`, `tyrell`, `corbel`, `keymaker`, `scorm-tools` |
| **[3. Evaluación y Gestión](evaluacion/index.md)** | Calificación masiva batch, ingesta Moodle ZIP / GitHub Classroom, detección de plagio Winnowing y telemetría. | `dredd`, `weyl`, `cyberdeck`, `meet-tools`, `slide-tools`, `gestion`, `p1-tools` |
| **[4. Aula y Exámenes](aula/index.md)** | Emulación de hardware bare-metal RV32I con periféricos MMIO para prácticas avanzadas y auditoría forense criptográfica. | `hardboiled`, `uatu-tools` |
| **[5. Diagnóstico Forense](diagnostico_avanzado/index.md)** | Verificación formal con contratos ACSL, cobertura lógica MC/DC, análisis de mutación e inyección dinámica de fallos POSIX. | `callahan`, `dietrich`, `vasquez`, `vassili` |
| **[6. Análisis Estático](analisis_estatico/index.md)** | Satélites de cátedra para inspección estática profunda: alineación de structs, portabilidad, ABI, call graphs y macros. | `brett`, `crowe`, `drake`, `ferro`, `giger`, `holden`, `kane`, `motoko`, `parker`, `rachel`, `sebastian`, `wierzbowski`, `zhora` |

---

## Perfiles de Aprovisionamiento con `mother`

Para instalar y actualizar las herramientas docentes en el entorno de cátedra:

```bash
# Instalar mother desde GitHub
uv tool install git+https://github.com/INGCOM-UNRN-P1/mother

# Perfil docente (corrección, evaluación y seguimiento)
mother instalar --perfil docente

# Perfil contenido (autoría de guías, exámenes y bancos de preguntas)
mother instalar --perfil contenido

# Perfil aula (supervisión de laboratorios y hardware emulado)
mother instalar --perfil aula

# Perfil análisis (satélites de análisis profundo)
mother instalar --perfil analisis
```
