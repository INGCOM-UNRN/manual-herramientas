---
title: "uatu-tools"
---

<!-- Generado por scripts/generar_paginas.py desde uatu-tools@b77e6d6: no editar a mano. -->

(manual-uatu_tools)=
# uatu-tools

Repositorio: [github.com/INGCOM-UNRN-P1/uatu-tools](https://github.com/INGCOM-UNRN-P1/uatu-tools).

Herramientas de línea de comandos de [uatu](https://github.com/INGCOM-UNRN-P1/uatu),
el sistema de proctorización y auditoría criptográfica Git-native para
exámenes prácticos en VS Code.

| Comando | Uso |
|---|---|
| `uatu-audit` | Validador forense para CI: audita las ramas `uatu-audit/<usuario>/<sesión>` de una entrega (firmas Ed25519, hash-chain, micro-lotes, bloque génesis y ventana temporal), aplica heurísticas y descifra los pegados con la clave docente. |
| `uatu-admin` | Herramientas de cátedra: almacén de claves en `~/.config/uatu/keys`, registro público de claves docentes, firma de `.uatu.conf`, secretos de GitHub Actions y protección de las ramas de telemetría. |

📖 **[Manual de referencia](https://github.com/INGCOM-UNRN-P1/uatu-tools/blob/main/manual/index.md)** con todos los comandos y opciones.
La guía del sistema completo está en el
[manual de uatu](https://github.com/INGCOM-UNRN-P1/uatu/blob/main/manual/index.md),
y los formatos en su [`docs/protocolo.md`](https://github.com/INGCOM-UNRN-P1/uatu/blob/main/docs/protocolo.md).

## Instalación

Requiere [uv](https://docs.astral.sh/uv/) y Python 3.9+.

```bash
# Como herramienta global
uv tool install "git+https://github.com/INGCOM-UNRN-P1/uatu-tools"

# Desde un clon local
uv tool install .

# Sin instalar
uvx --from "git+https://github.com/INGCOM-UNRN-P1/uatu-tools" uatu-audit --help
```

`src/uatu_tools/audit.py` es autocontenido y declara sus dependencias con
metadatos PEP 723: también puede copiarse a un repositorio y ejecutarse con
`uv run audit.py ...`.

## Almacén de claves

`uatu-admin` guarda las claves en `~/.config/uatu/keys/<id>/` (directorios
0700, claves privadas 0600). La ubicación se cambia con `--keys-dir` o
`UATU_KEYS_DIR`. Los demás comandos aceptan el identificador de la clave en
lugar de rutas.

```bash
uatu-admin keys list
uatu-admin keys show prof-lead-2026
uatu-admin keys import prof-lead-2026 --signing firma.pem --decryption descifrado.pem
uatu-admin keys export prof-lead-2026 -f verify-key                 # hex para --teacher-key
uatu-admin keys export inicial_unrn -f trust-anchors                # anclas para la extensión
uatu-admin keys export prof-lead-2026 -f decryption-key --out docente.pem
```

## Flujo para la cátedra

1. **Clave raíz institucional** (una vez), embebida en la extensión a través
   de la variable `UATU_TRUST_ANCHORS` del repositorio uatu:

   ```bash
   uatu-admin root-keygen --key-id inicial_unrn --name "Raíz institucional"
   uatu-admin keys setup-anchors inicial_unrn --repo INGCOM-UNRN-P1/uatu
   ```

2. **Clave del docente y registro público**, que se publica en la URL de
   `auth.public_key_registry_url`:

   ```bash
   uatu-admin keygen --key-id prof-lead-2026 --name "Programación I - 2026"
   uatu-admin registry-add --registry keys.json --key-id prof-lead-2026
   uatu-admin registry-sign --registry keys.json --root-key-id inicial_unrn
   uatu-admin verify-registry --registry keys.json
   ```

3. **Manifiesto del examen**:

   ```bash
   uatu-admin sign-config --config .uatu.conf --key-id prof-lead-2026
   uatu-admin verify-config --config .uatu.conf
   ```

4. **Repositorio del examen en GitHub**: secretos del workflow forense y ramas
   de telemetría protegidas contra borrado y force-push:

   ```bash
   uatu-admin keys setup-audit prof-lead-2026 --repo ORG/examen
   uatu-admin protect-branches --repo ORG/examen
   # o, para todos los repositorios de una tarea de GitHub Classroom:
   uatu-admin protect-branches --org ORG --repo-pattern 'examen-parcial-1-*'
   ```

5. **Consigna sellada** (opcional): no está en ninguna máquina de estudiante
   antes de `start_utc`. Se sella antes del examen y se libera a la hora del
   servidor de GitHub; la clave nunca va a los repositorios:

   ```bash
   uatu-admin consigna sellar parcial1/ --config .uatu.conf --key-id prof-lead-2026
   # el día del examen (con --esperar se puede lanzar antes: espera start_utc)
   uatu-admin consigna liberar --org ORG --prefijo examen-parcial-1- --esperar
   ```

   Si cada estudiante tiene su tema, se usa `uatu-admin paquetes` en lugar de `consigna`: el examen
   cifrado se reparte antes y a la hora sólo viaja la clave. Ver
   [`uatu/docs/paquetes_de_examen.md`](https://github.com/INGCOM-UNRN-P1/uatu-tools/blob/main/../uatu/docs/paquetes_de_examen.md).

6. **Auditoría de una entrega** (con la clave en el almacén, `uatu-audit` la
   toma del `teacher_key_id` del manifiesto):

   ```bash
   git fetch origin '+refs/heads/uatu-audit/*:refs/remotes/origin/uatu-audit/*'
   uatu-audit --repo . --md-out reporte.md --json-out reporte.json [--user <github_user>]
   ```

   | Código | Significado |
   |---|---|
   | `0` | Integridad criptográfica verificada sin anomalías. |
   | `1` | Falla de integridad: cadena rota, firmas inválidas, manifiesto alterado o ausencia de registros. |
   | `2` | Cadena íntegra con alertas heurísticas: pegados masivos, inserciones externas, extensiones no autorizadas, silencios de telemetría. |

En GitHub Actions, el workflow de ejemplo de uatu
(`templates/exam-repo/.github/workflows/uatu-audit.yml`) clona este
repositorio y lo instala con `uv tool install`; la variable `UATU_TOOLS_REF`
permite fijar una versión.

## Desarrollo

```bash
uv sync
uv run pytest -q
```

## Limitaciones

- Trabaja sobre lo que ya registró uatu: `uatu-audit` audita las ramas `uatu-audit/<usuario>/<sesión>`
  de una entrega; la vigilancia durante el examen la hace uatu en VS Code, no estas herramientas.
- Sin la clave docente, `uatu-audit` verifica firmas, cadena de hashes y tiempos, pero no puede
  descifrar los pegados.

## Referencia rápida

### Requisitos

- Python ≥ 3.9 y [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Programas del sistema: `git`.

| Sistema | `git` |
|:--|:--|
| Debian / Ubuntu | `sudo apt install git` |
| Fedora | `sudo dnf install git` |
| Windows | incluido en el entorno de la cátedra (MSYS2 UCRT64) |
| macOS | `xcode-select --install` |

### Opciones de `uatu-audit`

| Opción | Descripción |
|:--|:--|
| `--repo` | Ruta del repositorio de la entrega |
| `--teacher-key` | Clave pública Ed25519 docente (hex) o identificador del almacén. Por omisión $UATU_TEACHER_PUBLIC_KEY |
| `--decrypt-key` | Clave privada docente X25519 (ruta PEM) o identificador del almacén, para descifrar la evidencia |
| `--key-id` | Clave docente del almacén de uatu-admin: usa su pública para verificar y su privada para descifrar. Sin --teacher-key ni --key-id se intenta con el crypto.teacher_key_id del manifiesto |
| `--keys-dir` | Almacén de claves (por omisión $UATU_KEYS_DIR o ~/.config/uatu/keys) |
| `--md-out` | Reporte Markdown de salida |
| `--json-out` | Reporte JSON opcional para integraciones |
| `--user` | Auditar solo las sesiones de este usuario de GitHub |
| `--remote` | Remoto donde buscar las ramas (por omisión git.remote_name) |
| `--max-paste-chars` | Umbral heurístico de pegado masivo |
| `--grace-seconds` | Tolerancia posterior al deadline_utc |
| `--code-ref` | Referencia de código a correlacionar con la telemetría |

### Opciones de `uatu-admin`

| Opción | Descripción |
|:--|:--|
| `--keys-dir` | Almacén de claves (por omisión $UATU_KEYS_DIR o ~/.config/uatu/keys) |

### Comandos de `uatu-admin`

| Comando | Descripción |
|:--|:--|
| `uatu-admin doctor` | Verifica los requisitos (Python, cryptography, git, gh) |
| `uatu-admin root-keygen` | Genera la clave raíz institucional en el almacén |
| `uatu-admin keygen` | Genera las claves Ed25519/X25519 de un docente en el almacén |
| `uatu-admin keys` | Gestiona el almacén de claves y las exporta donde se usan |
| `uatu-admin registry-add` | Agrega un docente al registro de claves |
| `uatu-admin registry-sign` | Firma el registro con la clave raíz |
| `uatu-admin verify-registry` | Verifica la firma raíz del registro |
| `uatu-admin sign-config` | Firma .uatu.conf |
| `uatu-admin verify-config` | Verifica la firma de .uatu.conf |
| `uatu-admin protect-branches` | Impide borrar o reescribir las ramas de telemetría (ruleset de GitHub) |
| `uatu-admin consigna` | Sella la consigna del examen y la libera en start_utc (hora de GitHub) |
| `uatu-admin paquetes` | Un paquete cifrado por estudiante, que su equipo descifra desde start_utc |

Ayuda de cada comando: `uatu-admin <comando> -h`.

### Salida JSON de `uatu-admin`

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `uatu-admin doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-uatu_tools-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `uatu-audit`
:open:

```text
uso: uatu-audit [-h] [-v] [--repo REPO] [--teacher-key TEACHER_KEY] [--decrypt-key DECRYPT_KEY]
                [--key-id KEY_ID] [--keys-dir KEYS_DIR] [--md-out MD_OUT] [--json-out JSON_OUT]
                [--user USER] [--remote REMOTE] [--max-paste-chars MAX_PASTE_CHARS]
                [--grace-seconds GRACE_SECONDS] [--code-ref CODE_REF]

Validador Forense Uatu v2.1

opciones:
  -h, --help            muestra esta ayuda y sale
  -v, --version         muestra la versión y sale
  --repo REPO           Ruta del repositorio de la entrega
  --teacher-key TEACHER_KEY
                        Clave pública Ed25519 docente (hex) o identificador del almacén. Por
                        omisión $UATU_TEACHER_PUBLIC_KEY
  --decrypt-key DECRYPT_KEY
                        Clave privada docente X25519 (ruta PEM) o identificador del almacén, para
                        descifrar la evidencia
  --key-id KEY_ID       Clave docente del almacén de uatu-admin: usa su pública para verificar y
                        su privada para descifrar. Sin --teacher-key ni --key-id se intenta con el
                        crypto.teacher_key_id del manifiesto
  --keys-dir KEYS_DIR   Almacén de claves (por omisión $UATU_KEYS_DIR o ~/.config/uatu/keys)
  --md-out MD_OUT       Reporte Markdown de salida
  --json-out JSON_OUT   Reporte JSON opcional para integraciones
  --user USER           Auditar solo las sesiones de este usuario de GitHub
  --remote REMOTE       Remoto donde buscar las ramas (por omisión git.remote_name)
  --max-paste-chars MAX_PASTE_CHARS
                        Umbral heurístico de pegado masivo
  --grace-seconds GRACE_SECONDS
                        Tolerancia posterior al deadline_utc
  --code-ref CODE_REF   Referencia de código a correlacionar con la telemetría

`uatu-audit doctor [--json]` verifica los requisitos (Python, cryptography, git).
```
:::

:::{dropdown} `uatu-admin`
:open:

```text
uso: uatu-admin [-h] [-v] [--keys-dir KEYS_DIR]
                {doctor,root-keygen,keygen,keys,registry-add,registry-sign,verify-registry,sign-config,verify-config,protect-branches,consigna,paquetes} ...

Herramientas de cátedra para Uatu v2.1

argumentos:
  {doctor,root-keygen,keygen,keys,registry-add,registry-sign,verify-registry,sign-config,verify-config,protect-branches,consigna,paquetes}
    doctor              Verifica los requisitos (Python, cryptography, git, gh)
    root-keygen         Genera la clave raíz institucional en el almacén
    keygen              Genera las claves Ed25519/X25519 de un docente en el almacén
    keys                Gestiona el almacén de claves y las exporta donde se usan
    registry-add        Agrega un docente al registro de claves
    registry-sign       Firma el registro con la clave raíz
    verify-registry     Verifica la firma raíz del registro
    sign-config         Firma .uatu.conf
    verify-config       Verifica la firma de .uatu.conf
    protect-branches    Impide borrar o reescribir las ramas de telemetría (ruleset de GitHub)
    consigna            Sella la consigna del examen y la libera en start_utc (hora de GitHub)
    paquetes            Un paquete cifrado por estudiante, que su equipo descifra desde start_utc

opciones:
  -h, --help            muestra esta ayuda y sale
  -v, --version         muestra la versión y sale
  --keys-dir KEYS_DIR   Almacén de claves (por omisión $UATU_KEYS_DIR o ~/.config/uatu/keys)
```
:::

:::{dropdown} `uatu-admin doctor`

```text
uso: uatu-admin doctor [-h] [--json]

opciones:
  -h, --help  muestra esta ayuda y sale
  --json      Salida estructurada en JSON
```
:::

:::{dropdown} `uatu-admin root-keygen`

```text
uso: uatu-admin root-keygen [-h] --key-id KEY_ID [--name NAME]

opciones:
  -h, --help       muestra esta ayuda y sale
  --key-id KEY_ID
  --name NAME      Descripción legible (p. ej. la institución)
```
:::

:::{dropdown} `uatu-admin keygen`

```text
uso: uatu-admin keygen [-h] --key-id KEY_ID [--name NAME]

opciones:
  -h, --help       muestra esta ayuda y sale
  --key-id KEY_ID
  --name NAME      Descripción legible (p. ej. el docente o la materia)
```
:::

:::{dropdown} `uatu-admin keys`

```text
uso: uatu-admin keys [-h] {list,show,import,export,setup-audit,setup-anchors} ...

argumentos:
  {list,show,import,export,setup-audit,setup-anchors}
    list                Lista las claves del almacén
    show                Muestra los metadatos y archivos de una clave
    import              Importa claves PEM existentes al almacén
    export              Extrae una clave en el formato que necesita cada destino
    setup-audit         Carga UATU_TEACHER_PUBLIC_KEY y UATU_TEACHER_PRIVATE_KEY para el workflow
                        forense
    setup-anchors       Publica las anclas raíz para empaquetar la extensión

opciones:
  -h, --help            muestra esta ayuda y sale
```
:::

:::{dropdown} `uatu-admin keys list`

```text
uso: uatu-admin keys list [-h] [--json]

opciones:
  -h, --help  muestra esta ayuda y sale
  --json
```
:::

:::{dropdown} `uatu-admin keys show`

```text
uso: uatu-admin keys show [-h] key_id

argumentos:
  key_id

opciones:
  -h, --help  muestra esta ayuda y sale
```
:::

:::{dropdown} `uatu-admin keys import`

```text
uso: uatu-admin keys import [-h] [--root ROOT] [--signing SIGNING] [--decryption DECRYPTION]
                            [--name NAME]
                            key_id

argumentos:
  key_id

opciones:
  -h, --help            muestra esta ayuda y sale
  --root ROOT           Clave privada raíz Ed25519 (PEM)
  --signing SIGNING     Clave privada docente Ed25519 (PEM)
  --decryption DECRYPTION
                        Clave privada docente X25519 (PEM)
  --name NAME
```
:::

:::{dropdown} `uatu-admin keys export`

```text
uso: uatu-admin keys export [-h]
                            --format {public,anchor,trust-anchors,root-key,root-key-path,verify-key,encrypt-key,registry-entry,signing-key,signing-key-path,decryption-key,decryption-key-path}
                            [--out OUT] [--gh-secret NAME] [--gh-variable NAME] [--show-secret]
                            [--repo REPO | --org ORG] [--visibility {all,private,selected}]
                            key_id [key_id ...]

argumentos:
  key_id

opciones:
  -h, --help            muestra esta ayuda y sale
  --format, -f {public,anchor,trust-anchors,root-key,root-key-path,verify-key,encrypt-key,registry-entry,signing-key,signing-key-path,decryption-key,decryption-key-path}
                        raíz: anchor, trust-anchors, root-key, root-key-path | docente: verify-
                        key, encrypt-key, registry-entry, signing-key, signing-key-path,
                        decryption-key, decryption-key-path | ambas: public
  --out OUT             Escribir en un archivo (0600 si es una clave privada)
  --gh-secret NAME      Cargar como secreto de Actions (requiere gh)
  --gh-variable NAME    Cargar como variable de Actions (requiere gh)
  --show-secret         Permitir mostrar una clave privada en la terminal
  --repo REPO           Repositorio destino OWNER/REPO
  --org ORG             Organización destino (secretos/variables de organización)
  --visibility {all,private,selected}
                        Visibilidad de un secreto de organización (por omisión la de gh)
```
:::

:::{dropdown} `uatu-admin keys setup-audit`

```text
uso: uatu-admin keys setup-audit [-h] [--repo REPO | --org ORG]
                                 [--visibility {all,private,selected}]
                                 key_id

argumentos:
  key_id

opciones:
  -h, --help            muestra esta ayuda y sale
  --repo REPO           Repositorio destino OWNER/REPO
  --org ORG             Organización destino (secretos/variables de organización)
  --visibility {all,private,selected}
                        Visibilidad de un secreto de organización (por omisión la de gh)
```
:::

:::{dropdown} `uatu-admin keys setup-anchors`

```text
uso: uatu-admin keys setup-anchors [-h] [--repo REPO] [--variable VARIABLE] [--file FILE]
                                   key_id [key_id ...]

argumentos:
  key_id

opciones:
  -h, --help           muestra esta ayuda y sale
  --repo REPO          Repositorio de la extensión: carga la variable UATU_TRUST_ANCHORS
  --variable VARIABLE  Nombre de la variable (por omisión UATU_TRUST_ANCHORS)
  --file FILE          Escribir trust-anchors.json en esta ruta
```
:::

:::{dropdown} `uatu-admin registry-add`

```text
uso: uatu-admin registry-add [-h] --registry REGISTRY --key-id KEY_ID [--verify-key VERIFY_KEY]
                             [--encrypt-key ENCRYPT_KEY] [--name NAME] [--not-before NOT_BEFORE]
                             [--not-after NOT_AFTER]

opciones:
  -h, --help            muestra esta ayuda y sale
  --registry REGISTRY
  --key-id KEY_ID       Identificador del docente (y clave del almacén si no se dan las públicas)
  --verify-key VERIFY_KEY
                        Ed25519 pública (hex); por omisión la del almacén
  --encrypt-key ENCRYPT_KEY
                        X25519 pública (hex); por omisión la del almacén
  --name NAME
  --not-before NOT_BEFORE
  --not-after NOT_AFTER
```
:::

:::{dropdown} `uatu-admin registry-sign`

```text
uso: uatu-admin registry-sign [-h] --registry REGISTRY --root-key-id ROOT_KEY_ID
                              [--root-key ROOT_KEY]

opciones:
  -h, --help            muestra esta ayuda y sale
  --registry REGISTRY
  --root-key-id ROOT_KEY_ID
  --root-key ROOT_KEY   Clave privada raíz (PEM); por omisión la del almacén
```
:::

:::{dropdown} `uatu-admin verify-registry`

```text
uso: uatu-admin verify-registry [-h] --registry REGISTRY [--anchor-key ANCHOR_KEY]

opciones:
  -h, --help            muestra esta ayuda y sale
  --registry REGISTRY
  --anchor-key ANCHOR_KEY
                        Ed25519 pública raíz (hex); por omisión la del almacén según root_key_id
```
:::

:::{dropdown} `uatu-admin sign-config`

```text
uso: uatu-admin sign-config [-h] [--config CONFIG] [--key-id KEY_ID] [--key KEY]

opciones:
  -h, --help       muestra esta ayuda y sale
  --config CONFIG
  --key-id KEY_ID  Clave docente del almacén y valor de crypto.teacher_key_id (por omisión el
                   teacher_key_id del manifiesto)
  --key KEY        Clave privada Ed25519 docente (PEM), en lugar del almacén
```
:::

:::{dropdown} `uatu-admin verify-config`

```text
uso: uatu-admin verify-config [-h] [--config CONFIG] [--verify-key VERIFY_KEY] [--key-id KEY_ID]

opciones:
  -h, --help            muestra esta ayuda y sale
  --config CONFIG
  --verify-key VERIFY_KEY
                        Ed25519 pública docente (hex); por omisión la del almacén
  --key-id KEY_ID       Clave docente del almacén (por omisión el teacher_key_id del manifiesto)
```
:::

:::{dropdown} `uatu-admin protect-branches`

```text
uso: uatu-admin protect-branches [-h] [--repo REPO | --org ORG] [--repo-pattern PATRÓN]
                                 [--prefix PREFIX] [--config CONFIG] [--name NAME] [--dry-run]

opciones:
  -h, --help            muestra esta ayuda y sale
  --repo REPO           Repositorio del examen OWNER/REPO
  --org ORG             Organización (ruleset para todos los repositorios que coincidan)
  --repo-pattern PATRÓN
                        Con --org: patrón de nombres de repositorio (repetible; '~ALL' para todos)
  --prefix PREFIX       Prefijo de las ramas (por omisión el de --config o 'uatu-audit')
  --config CONFIG       Manifiesto del que leer git.telemetry_branch_prefix
  --name NAME           Nombre del ruleset (se actualiza si ya existe)
  --dry-run             Mostrar el ruleset sin aplicarlo
```
:::

:::{dropdown} `uatu-admin consigna`

```text
uso: uatu-admin consigna [-h] {sellar,liberar,hash} ...

argumentos:
  {sellar,liberar,hash}
    sellar              Cifra la carpeta de la consigna y agrega su hash a .uatu.conf
    liberar             Descifra en memoria y publica la consigna en cada repositorio, desde
                        start_utc
    hash                Hash de una carpeta (el que va en consigna.sha256) y si coincide con
                        .uatu.conf

opciones:
  -h, --help            muestra esta ayuda y sale
```
:::

:::{dropdown} `uatu-admin consigna sellar`

```text
uso: uatu-admin consigna sellar [-h] [--config CONFIG] [--salida SALIDA]
                                [--clave-salida CLAVE_SALIDA] [--carpeta-destino CARPETA_DESTINO]
                                [--key-id KEY_ID]
                                carpeta

argumentos:
  carpeta               Carpeta con el enunciado y las pruebas base

opciones:
  -h, --help            muestra esta ayuda y sale
  --config CONFIG
  --salida SALIDA       Paquete cifrado (por omisión consigna.enc)
  --clave-salida CLAVE_SALIDA
                        Archivo 0600 para la clave (por omisión <salida>.clave)
  --carpeta-destino CARPETA_DESTINO
                        Carpeta donde aparece en el repositorio del examen
  --key-id KEY_ID       Firmar .uatu.conf con esta clave docente del almacén
```
:::

:::{dropdown} `uatu-admin consigna liberar`

```text
uso: uatu-admin consigna liberar [-h] [--repo REPO | --org ORG] [--prefijo PREFIJO]
                                 [--config CONFIG] [--paquete PAQUETE] [--clave CLAVE]
                                 [--rama RAMA] [--esperar]

opciones:
  -h, --help         muestra esta ayuda y sale
  --repo REPO        Repositorio OWNER/REPO (repetible)
  --org ORG          Organización de los repositorios del examen
  --prefijo PREFIJO  Con --org: prefijo de los repositorios (el de la tarea de Classroom)
  --config CONFIG
  --paquete PAQUETE
  --clave CLAVE      Archivo con la clave de la consigna
  --rama RAMA        Rama donde publicarla (por omisión la principal de cada repositorio)
  --esperar          Si todavía no es start_utc, esperar y liberarla a la hora
```
:::

:::{dropdown} `uatu-admin consigna hash`

```text
uso: uatu-admin consigna hash [-h] [--config CONFIG] carpeta

argumentos:
  carpeta

opciones:
  -h, --help       muestra esta ayuda y sale
  --config CONFIG  Comparar con el consigna.sha256 de este manifiesto
```
:::

:::{dropdown} `uatu-admin paquetes`

```text
uso: uatu-admin paquetes [-h] {sellar,distribuir,liberar} ...

argumentos:
  {sellar,distribuir,liberar}
    sellar              Cifra <carpeta>/<usuario>/ con una clave por estudiante y agrega los
                        hashes a .uatu.conf
    distribuir          Publica cada paquete cifrado en el repositorio de su dueño, antes del
                        examen
    liberar             Publica la clave de cada estudiante en su repositorio, desde start_utc
                        (hora de GitHub)

opciones:
  -h, --help            muestra esta ayuda y sale
```
:::

:::{dropdown} `uatu-admin paquetes sellar`

```text
uso: uatu-admin paquetes sellar [-h] [--config CONFIG] [--salida SALIDA] [--claves CLAVES]
                                [--carpeta-destino CARPETA_DESTINO] [--key-id KEY_ID]
                                carpeta

argumentos:
  carpeta               Carpeta con una subcarpeta por usuario de GitHub (la arma alucard
                        repartir)

opciones:
  -h, --help            muestra esta ayuda y sale
  --config CONFIG
  --salida SALIDA       Carpeta de los paquetes cifrados (por omisión paquetes.enc)
  --claves CLAVES       Archivo de claves, 0600 (por omisión paquetes.claves)
  --carpeta-destino CARPETA_DESTINO
                        Carpeta donde se descifra en el repositorio del examen
  --key-id KEY_ID       Firmar .uatu.conf con esta clave del almacén
```
:::

:::{dropdown} `uatu-admin paquetes distribuir`

```text
uso: uatu-admin paquetes distribuir [-h] [--config CONFIG] [--paquetes PAQUETES]
                                    [--repo OWNER/REPO=USUARIO] [--org ORG] [--prefijo PREFIJO]
                                    [--rama RAMA]

opciones:
  -h, --help            muestra esta ayuda y sale
  --config CONFIG
  --paquetes PAQUETES   Carpeta de los paquetes cifrados
  --repo OWNER/REPO=USUARIO
                        Repositorio de un estudiante (repetible)
  --org ORG             Organización de los repositorios del examen
  --prefijo PREFIJO     Prefijo de los repositorios: <prefijo>-<usuario>
  --rama RAMA           Rama (por omisión, la principal de cada repositorio)
```
:::

:::{dropdown} `uatu-admin paquetes liberar`

```text
uso: uatu-admin paquetes liberar [-h] [--config CONFIG] [--paquetes PAQUETES]
                                 [--repo OWNER/REPO=USUARIO] [--org ORG] [--prefijo PREFIJO]
                                 [--rama RAMA] [--claves CLAVES] [--esperar]

opciones:
  -h, --help            muestra esta ayuda y sale
  --config CONFIG
  --paquetes PAQUETES   Carpeta de los paquetes cifrados
  --repo OWNER/REPO=USUARIO
                        Repositorio de un estudiante (repetible)
  --org ORG             Organización de los repositorios del examen
  --prefijo PREFIJO     Prefijo de los repositorios: <prefijo>-<usuario>
  --rama RAMA           Rama (por omisión, la principal de cada repositorio)
  --claves CLAVES       Archivo de claves
  --esperar             Esperar a start_utc en lugar de fallar
```
:::

Generado desde [`uatu-tools@b77e6d6`](https://github.com/INGCOM-UNRN-P1/uatu-tools/tree/b77e6d6).
