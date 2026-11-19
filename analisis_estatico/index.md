---
title: "Análisis Estático Especializado"
short_title: "Índice"
subtitle: "Satélites de cátedra para inspección algorítmica, arquitectura de memoria y estándares C"
---

(analisis-estatico-indice)=
# Análisis Estático Especializado

Satélites avanzados del perfil análisis orquestados por Ripley o invocados individualmente por el equipo docente para la auditoría minuciosa de código C.

---

## Catálogo de Satélites

* **[brett](brett.md)**: Disposición en memoria de los `struct`: mide con el compilador el relleno (*padding*) y sugiere el orden de campos que lo minimiza.
* **[crowe](crowe.md)**: Asunciones no portables (endianness, tamaño de punteros y de `long`, signo de `char`, VLA), con compilación cruzada opcional para `x86_64`, `aarch64` y `riscv64`.
* **[drake](drake.md)**: Fuzzing liviano con valores límite (`INT_MAX`, `INT_MIN`, cadenas largas, caracteres nulos) y mutaciones, para encontrar caídas antes de la entrega.
* **[ferro](ferro.md)**: Complejidad empírica: tiempo e instrucciones (Cachegrind) para varios tamaños de entrada, con ajuste $a + b \cdot N^k$; no mide ciclos ni IPC.
* **[giger](giger.md)**: Grafo de llamadas estático: recursión, funciones no invocadas y diagramas Mermaid.
* **[holden](holden.md)**: Mocks y envoltorios de enlace (`-Wl,--wrap=símbolo`) para simular fallos de `malloc`, `fopen` y otras funciones en las pruebas.
* **[kane](kane.md)**: Archivos binarios escritos con `fwrite`: los muestra como registros de un `struct` C, con offsets y detección de bytes truncados.
* **[motoko](motoko.md)**: Encapsulamiento de TDA: detecta accesos a campos internos desde el código cliente.
* **[parker](parker.md)**: Interfaces binarias (ABI) de `.so`, `.o` y `.h`: símbolos privados expuestos, símbolos faltantes y malas prácticas en la interfaz pública.
* **[rachel](rachel.md)**: `switch` y cadenas de `if-else`: desensambla las tablas de salto que genera el compilador y dibuja el diagrama de flujo.
* **[sebastian](sebastian.md)**: Recursión: consumo de pila, riesgo de desbordamiento y árbol de ejecución en la terminal o en Mermaid.
* **[wierzbowski](wierzbowski.md)**: Proyectos de varios archivos: grafo de `#include`, dependencias circulares, guardas de inclusión y Makefiles.
* **[zhora](zhora.md)**: Macros del preprocesador: evaluación múltiple de argumentos con efectos, paréntesis defensivos y punto y coma espurios.
