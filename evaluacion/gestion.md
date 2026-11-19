---
title: "gestion"
subtitle: "Planilla de cátedra con Google Apps Script"
---

(manual-gestion)=
# gestion — Planilla de cátedra con Google Apps Script

Repositorio: [github.com/martinvilu/gestion](https://github.com/martinvilu/gestion).

`gestion` es un proyecto de **Google Apps Script** asociado a una planilla de Google Sheets. No es una CLI ni se instala con `mother`: agrega a la planilla un menú **¡Magia!** con el que el equipo docente sigue las entregas de GitHub Classroom, sincroniza comentarios de corrección, administra permisos de los repositorios, envía correos por plantilla y trae la asistencia registrada en Supabase.

## Instalación

El código se publica en el proyecto de Apps Script de la planilla con [`clasp`](https://github.com/google/clasp) (la configuración está en `.clasp.json`):

```bash
npm install -g @google/clasp
clasp login
clasp push
```

Al abrir la planilla aparece el menú **¡Magia!**. La primera vez, **¡Magia! → Configuración → Inicialización → Inicializar TODO** crea la hoja `Configuración`, los rangos con nombre y las hojas de cada módulo.

## Configuración

- **Credenciales** (en las propiedades del usuario, no en la planilla): **Configuración → Setear GitHub API key**, y en **Configuración → Supabase** la URL, la tabla y las claves anónima y de servicio. Cada una tiene su opción para borrarla.
- **Parámetros** (rangos con nombre de la hoja `Configuración`): organización de GitHub (`GH_ORG`), fecha de corte (`GH_CUTOFF`), prefijos de las prácticas (`TP_SLUGS`), cuentas docentes que se ignoran al listar permisos (`GH_IGNORED_USERS`), materia y remitente y respuesta de los correos (`MATERIA`, `EMAIL_REMITENTE`, `EMAIL_RESPUESTA`).
- **Disparadores**: **Configuración → Instalar Triggers** programa las sincronizaciones de entregas, GitHub y Supabase con la frecuencia y el encendido que indican los rangos `TRIGGER_*`; **Borrar Triggers** los quita.

## Menú ¡Magia!

| Opción | Qué hace |
| :-- | :-- |
| Actualizar repositorios | Lista en la hoja `github` los repositorios de la organización configurada. |
| Sincronizar Entregados | Pasa las filas nuevas de la hoja `entregas` a `correcciones`. |
| Sincronizar Comentarios | Trae los comentarios de los Pull Requests de los repositorios en `correcciones`. |
| Vista previa Markdown | Muestra renderizado el Markdown de la celda activa. |
| Enviar correos | Envía los correos del rango `MAILER` con la plantilla `CUERPO_MAIL`; queda registro en `log_mailer`. |
| Actualizar permisos | Vuelca los colaboradores y permisos de cada repositorio en la hoja `gh_perm`. |
| Aplicar permisos | Aplica los permisos de `gh_perm` según la asignación de la hoja `practicas`. |
| Sincronizar Asistencia | Copia la tabla de asistencia de Supabase en `asistencia_raw`. |

## Aplicación web

Publicado como aplicación web, el script responde a `GET`:

- sin parámetros, un tablero de estado;
- `?action=sync`, la sincronización de entregas;
- `?action=track`, el registro de apertura de los correos enviados, en `log_aperturas`.

## Relación con el resto del ecosistema

`gestion` trabaja sobre la planilla y la API de GitHub; no lee la base `.metadata.db` de `dredd` ni sus informes. Las notas de una actividad se exportan desde `dredd` (`dredd export`, `dredd moodle export`, `dredd export-guarani`). El registro de mejoras pendientes y resueltas está en [`qol.md`](https://github.com/martinvilu/gestion/blob/main/qol.md).
