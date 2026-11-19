---
title: "Weyl"
subtitle: "Comparación de código C"
---

(manual-weyl)=
# Weyl — Comparación de código C

`weyl` compara archivos y proyectos C función por función, e identifica cambios y similitudes frente a una solución de referencia. Extrae funciones mediante análisis textual; no construye un árbol sintáctico del compilador. La similitud entre dos archivos es una señal para revisar, no una conclusión por sí sola sobre una entrega.

```bash
weyl diff estudiante.c modelo.c
weyl diff estudiante.c modelo.c --json
weyl diff-project dir_alumno/ dir_modelo/
weyl similarity entrega1.c entrega2.c
weyl doctor
```

Para comparar una cohorte mediante huellas de Winnowing, consultá `dredd plagiarism`. Para opciones, requisitos y otros comandos, consultá el [repositorio de Weyl](https://github.com/INGCOM-UNRN-P1/weyl).
