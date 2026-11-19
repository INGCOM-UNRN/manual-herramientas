---
title: "Diagnóstico Forense y Verificación Formal"
short_title: "Índice"
subtitle: "Verificación formal, cobertura MC/DC, sanitizers, inyección de fallos y pruebas de mutación"
---

(diagnostico-forense-indice)=
# Diagnóstico Forense y Verificación Formal

Herramientas avanzadas del perfil análisis y docente destinadas a la verificación rigurosa, auditoría de fallos y control de calidad estructural de código fuente C.

---

## Satélites de Diagnóstico y Verificación

* **[callahan](callahan.md)**: Verificación deductiva de contratos ACSL con Frama-C (WP); descarta los provers que demuestran un contrato falso de control.
* **[dietrich](dietrich.md)**: Cobertura MC/DC de decisiones booleanas compuestas: tabla de verdad y vectores de prueba mínimos ($k + 1$).
* **[tetsuo](tetsuo.md)**: Compila y ejecuta con AddressSanitizer y UndefinedBehaviorSanitizer y traduce sus diagnósticos al español, con un modo pista para evaluaciones.
* **[vasquez](vasquez.md)**: Inyección determinista de fallos en `malloc`, `fopen`, `fread` y otras funciones de la biblioteca de C con `LD_PRELOAD`, para verificar el manejo de errores.
* **[vassili](vassili.md)**: Pruebas de mutación: inyecta mutantes en el código C y calcula qué porcentaje detecta la suite del estudiante (*mutation score*).
