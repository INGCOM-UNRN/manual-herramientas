---
title: "p1-tools"
subtitle: "Meta-Repositorio y Orquestación Global del Ecosistema"
author: "Cátedra de Algoritmos y Programación"
date: "2026-09-14"
---

(manual-p1-tools)=
# p1-tools — Meta-Repositorio y Orquestación Global del Ecosistema

:::{admonition} Resumen Técnico del Satélite
:class: note
**Rol en el ecosistema:** Repositorio central de gobernanza arquitectónica,
sincronización de submódulos git, directivas de desarrollo, skills pedagógicas y
auditoría de salud.

:::
<!-- {admonition} Resumen Técnico del Satélite -->

---

## 1. Propósito y Alcance

Coordina las 46 herramientas del ecosistema, provee scripts de clonación masiva
(`scripts/sync.sh`), linters de coherencia documental y lineamientos normativos
de cátedra.

---

## 2. Uso Básico

``` bash
# Auditar salud y versiones de todos los repositorios satélites
./scripts/healthcheck.sh

# Desplegar actualizaciones a los entornos de desarrollo
./scripts/sync.sh
```
<!-- bash -->

(manual-p1-tools-ejemplos)=
## Ejemplos y Contraejemplos

En esta sección se contrastan patrones de uso correctos recomendados por la cátedra frente a contraejemplos, antipatrones o configuraciones defectuosas que la herramienta diagnostica o rechaza.

### Ejemplo Válido (Patrón Recomendado)

Verificación estructural de integridad de todos los repositorios declarados en `ecosistema.toml`:

```{code-block} bash
python3 scripts/ecosistema.py verificar
```

Salida esperada:
```{code-block} text
[✓] Manifiesto ecosistema.toml validado: 40 repositorios auditados
[✓] URLs de origen conforme a la organización oficial INGCOM-UNRN-P1
[✓] Todos los perfiles declarados son válidos
[✓] Cero dependencias con rutas locales absolutas
```

### Contraejemplo (Antipatrón o Caso Infractor)

Declaración de un repositorio con URL a PyPI o ruta absoluta a la máquina del docente:

```{code-block} bash
python3 scripts/ecosistema.py verificar
```

Diagnóstico emitido por la herramienta:
```{code-block} text
[!] ERROR N-ECO-21: 'deckard' declara url con ruta local absoluta '/home/mrtin/dev/tools/deckard'.
[!] Las dependencias deben declararse exclusivamente como 'git+https://github.com/INGCOM-UNRN-P1/...'.
[!] Verificación fallida con código de salida 1.
```

