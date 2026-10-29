---
title: "Manual de Referencia: construct"
short_title: "construct"
subtitle: "IDE pedagógico y orquestador de máquina virtual del ecosistema Programación 1"
author: "Cátedra de Programación 1"
date: "2026-10-27"
---

(manual-construct)=
# construct — IDE Pedagógico y Orquestador de Máquina Virtual

::::{admonition} Resumen Técnico del Componente
:class: note
**Rol en el ecosistema:** Orquestador de máquina virtual Debian acelerada por hardware (QEMU con KVM, WHPX o HVF) e interfaz de terminal unificada (`construct ui`) para el dictado y evaluación práctica en laboratorios y entornos multiplataforma (Linux, Windows, macOS).
::::

---

(manual-construct-proposito)=
## 1. Propósito y Filosofía de Diseño

`construct` estandariza el entorno de ejecución de la cátedra eliminando las disparidades entre sistemas operativos del alumnado y computadoras de laboratorio.

1. **Aislamiento sin Fricción**: En el sistema Host únicamente se requieren QEMU (≥ 8.2), Git y `uv`. El compilador GCC, GDB, Valgrind, Bubblewrap y la totalidad de los satélites de cátedra residen preinstalados dentro de la imagen oficial de la máquina virtual.
2. **Frontend Unificado**: Integra en un solo panel TUI (`construct ui`) el editor de código, la consola interactiva, el visualizador de memoria (Bishop/Valgrind) y el diagnóstico pedagógico en tiempo real (Jonesy, Daedalus, Ripley).
3. **Reproducibilidad en Exámenes y Aula**: Garantiza que las restricciones de memoria, límites de tiempo y comprobaciones de concurrencia se evalúen bajo un kernel Linux idéntico, aun cuando la máquina anfitriona sea Windows o macOS.

---

(manual-construct-requisitos)=
## 2. Requisitos y Aceleración por Plataforma

| Sistema Anfitrión | Hipervisor / Aceleración | Instalación de QEMU y Dependencias |
| :--- | :--- | :--- |
| **Linux (x86_64 / ARM)** | KVM (`/dev/kvm`) | `sudo apt install qemu-system-x86 git` (o `qemu-system-arm`) |
| **Windows 10/11** | Windows Hypervisor Platform (WHPX) | `winget install --id SoftwareFreedomConservancy.QEMU -e` |
| **macOS 13+** | Hypervisor.framework (HVF) | `brew install qemu` |

En equipos con arquitectura Apple Silicon la máquina virtual ejecuta una imagen nativa `aarch64` con aceleración completa sin emulación de instrucciones.

---

(manual-construct-instalacion)=
## 3. Instalación y Puesta en Marcha

`construct` se instala en el Host mediante `uv`:

```bash
# Instalación del orquestador en el sistema Host
uv tool install git+https://github.com/INGCOM-UNRN-P1/construct

# Descarga y aprovisionamiento de la imagen oficial
construct setup

# Diagnóstico de aceleración y estado de la VM
construct doctor
```

---

(manual-construct-comandos)=
## 4. Guía Integral de Comandos (CLI)

| Comando | Descripción Operativa |
| :--- | :--- |
| `construct ui` | Inicia el entorno de desarrollo integrado en terminal (editor, consola, memoria, tests). |
| `construct build` | Compila el proyecto actual dentro de la VM aplicando los flags estrictos de cátedra. |
| `construct check` | Ejecuta la suite de linters pedagógicos (Ripley, Gaff, Spunkmeyer, Kaneda). |
| `construct run` | Ejecuta el binario compilado bajo el entorno aislado de la VM. |
| `construct run --tetsuo` | Ejecuta instrumentando con AddressSanitizer y UndefinedBehaviorSanitizer. |
| `construct test` | Ejecuta el arnés de pruebas unitarias (`p1_test.h` / `treadstone.h`). |
| `construct jonesy <archivo.c>` | Invoca el diagnóstico pedagógico interactivo de errores inline. |
| `construct sync` | Sincroniza bidireccionalmente los fuentes y artefactos (`.bmp`, `.wav`) entre Host y VM. |

---

(manual-construct-atajos)=
## 5. Atajos de Teclado en `construct ui`

* <kbd>F5</kbd>: Ejecutar programa (`construct run`).
* <kbd>F6</kbd>: Ejecutar batería de tests (`construct test`).
* <kbd>F7</kbd>: Compilar solución (`construct build`).
* <kbd>F8</kbd>: Verificar estilo y antipatrones (`construct check`).
* <kbd>Ctrl+S</kbd>: Guardar archivo y sincronizar automáticamente con la máquina virtual.
* <kbd>Ctrl+Q</kbd>: Salir de la interfaz de terminal.
