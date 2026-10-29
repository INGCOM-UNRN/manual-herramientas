---
title: "slide-tools"
subtitle: "Control Remoto y Sincronización de Diapositivas para Google Slides"
author: "Cátedra de Algoritmos y Programación"
date: "2026-09-14"
---

(manual-slide-tools)=
# slide-tools — Control Remoto y Sincronización para Google Slides

:::{admonition} Resumen Técnico del Satélite
:class: note
**Rol en el ecosistema:** Transmisión remota de notas de orador, cronómetro
sincronizado y pase de diapositivas mediante protocolo WebSocket y extensión de
navegador.

:::
<!-- {admonition} Resumen Técnico del Satélite -->

---

## 1. Propósito y Alcance

Brinda a los docentes la capacidad de avanzar diapositivas y leer notas desde
dispositivos móviles o hardware dedicado con display OLED.

---

## 2. Uso Básico

``` bash
slide-tools serve --bind 0.0.0.0 --port 8766
```
<!-- bash -->

(manual-slide-tools-ejemplos)=
## Ejemplos y Contraejemplos

En esta sección se contrastan patrones de uso correctos recomendados por la cátedra frente a contraejemplos, antipatrones o configuraciones defectuosas que la herramienta diagnostica o rechaza.

### Ejemplo Válido (Patrón Recomendado)

Sincronización remota de diapositivas con el apunte web durante el dictado:

```{code-block} bash
slide-tools sync --presentation-id "1a2b3c4d5e" --port 8088
```

Salida esperada:
```{code-block} text
[✓] Servidor WebSocket activo en ws://localhost:8088
[✓] Diapositivas sincronizadas: 64 láminas cargadas
[✓] Evento recibido: Salto a lámina 12 ('Modelo de Memoria: Stack vs Heap')
```

### Contraejemplo (Antipatrón o Caso Infractor)

Intento de conexión remota con token de sesión expirado o ID de presentación erróneo:

```{code-block} bash
slide-tools sync --presentation-id "id_invalido"
```

Diagnóstico emitido por la herramienta:
```{code-block} text
[!] ERROR: No fue posible autenticar contra la API de Google Slides.
[!] Error 401 Unauthorized: token OAuth no provisto o vencido.
[!] Acción: ejecutá 'slide-tools auth login' para renovar las credenciales.
```

