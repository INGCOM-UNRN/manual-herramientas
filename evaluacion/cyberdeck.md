---
title: "cyberdeck"
subtitle: "Panel Docente y Companion Hardware de Control de Aula"
author: "Cátedra de Algoritmos y Programación"
date: "2026-09-14"
---

(manual-cyberdeck)=
# cyberdeck — Panel Docente y Companion Hardware de Control de Aula

:::{admonition} Resumen Técnico del Satélite
:class: note
**Rol en el ecosistema:** Interfaz unificada de telemetría y control
táctil/físico para docentes en aula presencial o remota, integrando
diapositivas, videollamadas y disparadores de autoevaluación.

:::
<!-- {admonition} Resumen Técnico del Satélite -->

---

## 1. Propósito y Alcance

`cyberdeck` conecta la estación de trabajo docente con dispositivos periféricos
(teclados macro, microcontroladores ESP32/RP2040, interfaces táctiles) para
controlar en tiempo real herramientas como `slide-tools` y `meet-tools`.

---

## 2. Invocación y Operación

``` bash
# Iniciar daemon concentrador
cyberdeck start --port 8888

# Monitorear eventos de dispositivos
cyberdeck monitor
```
<!-- bash -->

(manual-cyberdeck-ejemplos)=
## Ejemplos y Contraejemplos

En esta sección se contrastan patrones de uso correctos recomendados por la cátedra frente a contraejemplos, antipatrones o configuraciones defectuosas que la herramienta diagnostica o rechaza.

### Ejemplo Válido (Patrón Recomendado)

Conexión serial y sincronización de estado de examen con la terminal del docente:

```{code-block} bash
cyberdeck monitor --port /dev/ttyACM0 --baud 115200 --examen "Parcial 1"
```

Salida esperada:
```{code-block} text
[✓] Dispositivo companion detectado: Cyberdeck HW v2.1
[✓] Protocolo serial sincronizado a 115200 baud
[✓] Cronómetro de examen iniciado: 120 minutos restantes
[✓] Telemetría activa: 48 puestos de laboratorio conectados
```

### Contraejemplo (Antipatrón o Caso Infractor)

Conexión con baudrate erróneo o puerto serie ocupado por otro proceso:

```{code-block} bash
cyberdeck monitor --port /dev/ttyACM0 --baud 9600
```

Diagnóstico emitido por la herramienta:
```{code-block} text
[!] ERROR: Fallo de handshake con el dispositivo en /dev/ttyACM0.
[!] Trama inválida recibida: bytes corruptos por discrepancia de baudrate (esperado 115200).
[!] Acción: verificá la configuración del puerto con 'cyberdeck doctor --serial'.
```

