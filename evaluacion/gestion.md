---
title: "gestion"
subtitle: "Automatización de Calificaciones y Sincronización de Cátedra"
author: "Cátedra de Algoritmos y Programación"
date: "2026-09-14"
---

(manual-gestion)=
# gestion — Automatización de Calificaciones y Sincronización

:::{admonition} Resumen Técnico del Satélite
:class: note
**Rol en el ecosistema:** Sincronización bidireccional entre la base de datos de
notas SQLite de Dredd, planillas de cálculo institucionales y registros
académicos.

:::
<!-- {admonition} Resumen Técnico del Satélite -->

---

## 1. Propósito y Alcance

Automatiza la consolidación de notas, seguimiento de entregas y generación de
reportes de cursada sin intervención manual.

---

## 2. Uso Básico

``` bash
# Sincronizar calificaciones locales con planilla docente
gestion sync --db notas.db --sheet "P1-2026"
```
<!-- bash -->

(manual-gestion-ejemplos)=
## Ejemplos y Contraejemplos

En esta sección se contrastan patrones de uso correctos recomendados por la cátedra frente a contraejemplos, antipatrones o configuraciones defectuosas que la herramienta diagnostica o rechaza.

### Ejemplo Válido (Patrón Recomendado)

Cierre y exportación de actas finales consolidadas con notas validadas:

```{code-block} bash
gestion actas exportar --comision 1 --periodo 2026-1C --salida actas_finales.csv
```

Salida esperada:
```{code-block} text
[✓] 38 alumnos procesados para la Comisión 1
[✓] Condición académica calculada: 12 Promocionados, 20 Regulares, 6 Libres
[✓] Archivo exportado conforme al formato oficial UNRN: actas_finales.csv
```

### Contraejemplo (Antipatrón o Caso Infractor)

Exportación con discrepancia entre notas numéricas y condiciones académicas sin cerrar:

```{code-block} bash
gestion actas exportar --comision 1 --periodo 2026-1C --estricto
```

Diagnóstico emitido por la herramienta:
```{code-block} text
[!] ERROR: Inconsistencia en legajo 10452 (alumno sin nota de Parcial 2).
[!] No es posible emitir un acta formal con estados pendientes o notas fuera de rango [1..10].
[!] Acción: resolvé las notas faltantes en 'calificaciones.toml' antes de reintentar.
```

