---
title: "meet-tools"
subtitle: "Sistema de Control y Telemetría para Google Meet"
author: "Cátedra de Algoritmos y Programación"
date: "2026-09-14"
---

(manual-meet-tools)=
# meet-tools — Sistema de Control y Telemetría para Google Meet

:::{admonition} Resumen Técnico del Satélite
:class: note
**Rol en el ecosistema:** Control bidireccional de sesiones de Google Meet desde
clientes externos (Android/ESP32) mediante WebExtensions y daemon local vía
WebSocket.

:::
<!-- {admonition} Resumen Técnico del Satélite -->

---

## 1. Propósito y Alcance

Permite silenciar micrófono, conmutar cámara, consultar lista de asistentes y
recibir notificaciones de mano levantada sin alternar ventanas durante la clase.

---

## 2. Uso Básico

``` bash
# Iniciar servidor WebSocket local
meet-tools server --port 8765
```
<!-- bash -->

(manual-meet-tools-ejemplos)=
## Ejemplos y Contraejemplos

En esta sección se contrastan patrones de uso correctos recomendados por la cátedra frente a contraejemplos, antipatrones o configuraciones defectuosas que la herramienta diagnostica o rechaza.

### Ejemplo Válido (Patrón Recomendado)

Extracción de telemetría de asistencia y permanencia durante una clase sincrónica:

```{code-block} bash
meet-tools asistencia --call-id "p1-teoria-clase-08" --minutos-minimos 60
```

Salida esperada:
```{code-block} text
[✓] Sesión recuperada: p1-teoria-clase-08 (duración total 110 min)
[✓] Asistentes registrados: 54 alumnos
[✓] Presentes certificados (permanencia >= 60 min): 49 alumnos
[✓] Archivo de asistencia generado: asistencia_clase_08.json
```

### Contraejemplo (Antipatrón o Caso Infractor)

Invocación con identificador de llamada inexistente o permisos de organizador revocados:

```{code-block} bash
meet-tools asistencia --call-id "reunion-inexistente"
```

Diagnóstico emitido por la herramienta:
```{code-block} text
[!] ERROR: Llamada 'reunion-inexistente' no encontrada en el registro de Google Workspace.
[!] Código HTTP 404: recurso no localizado o cuenta sin permisos de auditoría.
```

