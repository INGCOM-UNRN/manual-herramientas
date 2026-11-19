---
title: "meet-tools"
---

<!-- Generado por scripts/generar_paginas.py desde meet-tools@42f0c8d: no editar a mano. -->

(manual-meet_tools)=
# meet-tools

Repositorio: [github.com/martinvilu/meet-tools](https://github.com/martinvilu/meet-tools).

Sistema de control y monitoreo bidireccional para Google Meet desde dispositivos externos (apps móviles Android y hardware embebido Wi-Fi) mediante una extensión de navegador WebExtensions y un daemon concentrador local/LAN.

Basado en la especificación técnica [spec.md](https://github.com/martinvilu/meet-tools/blob/main/spec.md) (Versión 1.1).

---

## Arquitectura General

```
┌──────────────────────────────────────────────┐
│ Dispositivo Externo (App Android / MCU Wi-Fi)│
│  - Primera fase: App Android                 │
│  - Segunda fase: ESP32 / RP2040W (Wi-Fi)     │
└──────────────────────┬───────────────────────┘
                       │
                       │ WebSocket / TCP (LAN: ws://<HOST_IP>:8765)
                       ▼
┌──────────────────────────────────────────────┐
│                 Daemon Local                 │
│  - Enrutamiento bidireccional LAN            │
│  - Control de concurrencia de pestañas       │
└──────────────────────┬───────────────────────┘
                       │
                       │ WebSocket Local (ws://127.0.0.1:8765)
                       ▼
┌──────────────────────────────────────────────┐
│           Extensión WebExtensions            │
│ (Firefox / Chromium - meet.google.com)       │
│  ├─ Content Script: Inspección/Control DOM   │
│  └─ UI Overlay: Inyección de alertas locales │
└──────────────────────────────────────────────┘
```

---

## Componentes del Repositorio

1. **`meet_tools.daemon`**:
   - Servidor WebSocket multicliente enlazado en `0.0.0.0:8765` para atender en simultáneo a la extensión local (`127.0.0.1`) y clientes en la red local.
   - Aplica la política **Single-Session Lock**: si detecta dos o más reuniones de Meet activas simultáneas en el navegador, entra en estado `LOCKED_AMBIGUOUS_TABS`, suspende la ejecución de comandos con el error `ERR_MULTIPLE_CALLS_ACTIVE` y envía la orden a las pestañas de desplegar una alerta visual.
   - Al quedar solo una llamada activa, se restablece el control automáticamente.

2. **`extension/` (WebExtensions MV3)**:
   - Compatible con Google Chrome, Chromium, Brave, Edge y Firefox.
   - Content script que inspecciona el DOM de `meet.google.com` con soporte estricto para **Español (ES/LATAM)** e **Inglés (US/UK)**.
   - Observador reactivo de mutaciones del DOM (`MutationObserver`) para telemetría en tiempo real de micrófono, cámara, mano levantada, participantes y sala de espera.
   - Inyector de alertas flotantes en el DOM (`overlay.css` y `content.js`):
     - Advertencia ante falta de permisos de anfitrión (`MUTE_ALL` / `ADMIT_ALL` con timeout de 300 ms).
     - Banner persistente de bloqueo por ambigüedad cuando hay múltiples reuniones abiertas.

3. **`meet_tools.cli` (`meet-tools`)**:
   - Herramienta de línea de comandos para administrar el daemon, consultar el estado en tiempo real, enviar comandos directos, monitorear telemetría continua o simular pestañas para pruebas sin navegador.

---

## Instalación y Puesta en Marcha

### Requisitos

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) instalado en el sistema

### 1. Iniciar el Daemon Concentrador

```bash
cd /home/mrtin/dev/tools/meet-tools
uv sync
uv run meet-tools daemon
```

Opciones:
- `--host` / `-h`: IP de enlace (por defecto `0.0.0.0` para permitir acceso desde la LAN).
- `--port` / `-p`: Puerto TCP (por defecto `8765`).

### 2. Cargar la Extensión en el Navegador

#### Chromium / Google Chrome / Brave / Edge:
1. Abrí `chrome://extensions/`.
2. Activá el **Modo de desarrollador** (esquina superior derecha).
3. Hacé clic en **Cargar descomprimida** (Load unpacked).
4. Seleccioná la carpeta `/home/mrtin/dev/tools/meet-tools/extension`.

#### Firefox:
1. Abrí `about:debugging#/runtime/this-firefox`.
2. Hacé clic en **Cargar complemento temporal** (Load Temporary Add-on).
3. Seleccioná el archivo `/home/mrtin/dev/tools/meet-tools/extension/manifest.json`.

---

## Uso de la CLI (`meet-tools`)

Una vez iniciado el daemon y abierta una reunión en Google Meet:

```bash
# Ver estado consolidado de la llamada
uv run meet-tools status

# Conmutar controles
uv run meet-tools mic        # Conmuta micrófono (TOGGLE_MIC)
uv run meet-tools cam        # Conmuta cámara (TOGGLE_CAM)
uv run meet-tools hand       # Conmuta mano levantada (TOGGLE_HAND)

# Acciones de moderación (requieren rol de anfitrión)
uv run meet-tools mute-all   # Silenciar a todos los participantes
uv run meet-tools admit-all  # Admitir a todos en la sala de espera

# Abandonar o finalizar reunión
uv run meet-tools leave            # Salir de la reunión
uv run meet-tools leave --all      # Finalizar reunión para todos

# Monitoreo reactivo de eventos en tiempo real
uv run meet-tools monitor

# Simulación de pestaña para pruebas sin navegador
uv run meet-tools mock-tab --in-call --host
```

### Atajos de teclado globales

```bash
meet-tools atajos              # muestra los atajos y si están instalados
meet-tools atajos --instalar   # los registra en GNOME (Configuración → Teclado)
meet-tools atajos --quitar
```

| Atajo | Acción |
|:--|:--|
| Ctrl+Alt+M | micrófono |
| Ctrl+Alt+V | cámara |
| Ctrl+Alt+H | levantar o bajar la mano |
| Ctrl+Alt+A | admitir a todos |
| Ctrl+Alt+S | silenciar a todos |

Funcionan con cualquier ventana enfocada: bajo Wayland ningún programa puede capturar teclas
globales, así que cada atajo es un atajo del escritorio que corre `meet-tools <comando> --notificar`
(si algo falla, avisa con una notificación). Fuera de GNOME, `meet-tools atajos` muestra los
comandos para cargarlos a mano.

### Indicador en la bandeja y registro

`meet-tools bandeja` muestra un círculo verde (en llamada), amarillo (daemon sin llamada) o gris
(sin daemon). Necesita pystray: `uv tool install --with pystray --with pillow …`, y en GNOME la
extensión «AppIndicator and KStatusNotifierItem Support». Sin pystray avisa cada cambio con una
notificación de escritorio.

El daemon registra conexiones, emparejamientos y PIN rechazados en `~/.local/state/p1/cast.log`
(rotativo, compartido con slide-tools).

---

## Consumidores e integración con cyberdeck

**Estado real: especificación, no verificado contra un cliente.** El consumidor
declarado, `cyberdeck` (app Android), existe solo como especificación
(`cyberdeck/android-spec.md`, que lo lista contra `meet-tools (ws:8765)`); no hay
cliente implementado ni prueba de integración con este daemon. No se invoca a
ninguna otra herramienta del ecosistema desde aquí.

Lo que este repo sí garantiza (fijado en `tests/test_contrato_cyberdeck.py`):

- Puerto por defecto del daemon: `8765`.
- Servicio mDNS publicado: `_meet-bridge._tcp.local.` (propiedad `service=meet`). La spec
  de cyberdeck describe `_meet-bridge._sub._bridge-remote._tcp.local.`: **esa forma con
  subtipo no está implementada**; un cliente debe descubrir por el tipo plano.
- URI de emparejamiento `bridge://pair?v=1.3&host=…&port=8765&service=meet&pin=…&name=…`.
- Salida `--json` versionada (`schema_version`) en `status` y `monitor` para
  consumidores externos que no hablen WebSocket.

---

## Seguridad del emparejamiento

- **El PIN protege la red del aula.** Una conexión desde el mismo equipo sin origen web (la CLI,
  un atajo, la bandeja, la extensión) no lo necesita; un dispositivo de la red sí
  (`PAIR_REQUEST` con `pin`). Contra un daemon de otro equipo, la CLI toma el PIN de
  `MEET_TOOLS_PIN`.
- **Token de reconexión.** `PAIRING_SUCCESS` trae `token` y `expiresIn` (8 h). Un `PAIR_REQUEST`
  con `{"token": …}` en lugar del PIN vuelve a emparejar (la red se cortó, la app se reabrió). Los
  tokens viven en memoria: reiniciar el daemon los invalida.
- **Ninguna página web puede conectarse.** Un WebSocket a 127.0.0.1 lo puede abrir cualquier sitio
  abierto en el navegador; el daemon responde 403 a toda conexión con `Origin` de una página y
  sólo acepta programas (sin `Origin`), extensiones y `https://meet.google.com` (el content
  script de la extensión abre el WebSocket desde la página de Meet).
- **El PIN y el QR sólo a quien ya está emparejado.** El `STATE_SYNC` inicial a un dispositivo sin
  emparejar llega con `pin`, `pairingUri` y `qrSvg` en `null`.
- Cinco PIN equivocados en un minuto bloquean esa IP, también para la extensión.

## Protocolo de Comunicación (JSON v1.1)

Todos los mensajes transmitidos sobre WebSocket respetan el siguiente esquema base:

```json
{
  "version": "1.1",
  "source": "client" | "daemon" | "extension",
  "type": "command" | "state_update" | "event" | "ack" | "error",
  "action": "string",
  "payload": {}
}
```

### Esquema de `STATE_SYNC`

```json
{
  "inCall": true,
  "micMuted": false,
  "cameraOff": true,
  "handRaised": false,
  "participantCount": 18,
  "waitingRoomCount": 3,
  "isHost": true,
  "locked": false
}
```

---

## Pruebas Automatizadas

El proyecto cuenta con una suite completa de pruebas unitarias y de integración asíncronas con `pytest-asyncio`:

```bash
uv run pytest -v
```

---

## Empaquetado para Chrome y Firefox

Para empaquetar la extensión lista para cargar o distribuir:

```bash
uv run meet-tools pack
```

Opciones:
- `--target` / `-t`: `both` (por defecto), `chrome` o `firefox`.
- `--out-dir` / `-o`: Directorio de salida (por defecto `dist/`).

Archivos generados en `dist/`:
- **`meet-bridge-chrome-v1.1.0.zip`**: Manifiesto optimizado para Chromium.
- **`meet-bridge-firefox-v1.1.0.xpi`**: Manifiesto adaptado para Firefox MV3 con `browser_specific_settings.gecko`.

## Limitaciones

- Solo Google Meet (`meet.google.com`) en un navegador Firefox o Chromium con la extensión cargada.
- La extensión controla la reunión a través de la página (su content script inspecciona y maneja el
  DOM de Meet): un cambio en la interfaz de Google puede dejar sin efecto algún comando hasta que se
  actualice la extensión.
- Los dispositivos se conectan al daemon por WebSocket dentro de la red local: no hay un servidor en
  internet.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `meet-tools daemon` | Inicia el daemon concentrador WebSocket en primer plano. |
| `meet-tools status` | Consulta y muestra el estado actual consolidado de la sesión de Google Meet. |
| `meet-tools mic` | Conmuta el micrófono propio (TOGGLE_MIC). |
| `meet-tools cam` | Conmuta la cámara propia (TOGGLE_CAM). |
| `meet-tools hand` | Conmuta levantar/bajar la mano (TOGGLE_HAND). |
| `meet-tools admit-all` | Acciona 'Admitir a todos' en la sala de espera (ADMIT_ALL). |
| `meet-tools mute-all` | Acciona 'Silenciar a todos' los participantes (MUTE_ALL). |
| `meet-tools leave` | Abandona la reunión (LEAVE_CALL). |
| `meet-tools monitor` | Escucha y muestra en tiempo real todos los eventos y telemetría de Meet. |
| `meet-tools mock-tab` | Simula una pestaña de Google Meet con la extensión para pruebas locales. |
| `meet-tools pack` | Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi). |
| `meet-tools sign` | Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext. |
| `meet-tools qr` | Muestra el código QR para emparejamiento directo con la app Android. |
| `meet-tools doctor` | Verifica el estado del entorno de MEET-TOOLS (Python, web-ext opcional). |
| `meet-tools atajos` | Atajos de teclado globales: micrófono, cámara, mano, admitir y silenciar a todos. |
| `meet-tools bandeja` | Indicador en la bandeja del sistema: verde en llamada, amarillo sin llamada, gris sin daemon. |

Ayuda de cada comando: `meet-tools <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `meet-tools status`, `meet-tools monitor`, `meet-tools doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-meet_tools-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `meet-tools`
:open:

```text
 Uso: meet-tools [OPCIONES] COMANDO [ARGUMENTOS]...

 Sistema de control externo para Google Meet.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de meet-tools y sale.                         │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ daemon     Inicia el daemon concentrador WebSocket en primer plano.                              │
│ status     Consulta y muestra el estado actual consolidado de la sesión de Google Meet.          │
│ mic        Conmuta el micrófono propio (TOGGLE_MIC).                                             │
│ cam        Conmuta la cámara propia (TOGGLE_CAM).                                                │
│ hand       Conmuta levantar/bajar la mano (TOGGLE_HAND).                                         │
│ admit-all  Acciona 'Admitir a todos' en la sala de espera (ADMIT_ALL).                           │
│ mute-all   Acciona 'Silenciar a todos' los participantes (MUTE_ALL).                             │
│ leave      Abandona la reunión (LEAVE_CALL).                                                     │
│ monitor    Escucha y muestra en tiempo real todos los eventos y telemetría de Meet.              │
│ mock-tab   Simula una pestaña de Google Meet con la extensión para pruebas locales.              │
│ pack       Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi).             │
│ sign       Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext.         │
│ qr         Muestra el código QR para emparejamiento directo con la app Android.                  │
│ doctor     Verifica el estado del entorno de MEET-TOOLS (Python, web-ext opcional).              │
│ atajos     Atajos de teclado globales: micrófono, cámara, mano, admitir y silenciar a todos.     │
│ bandeja    Indicador en la bandeja del sistema: verde en llamada, amarillo sin llamada, gris sin │
│            daemon.                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools daemon`

```text
 Uso: meet-tools daemon [OPCIONES]

 Inicia el daemon concentrador WebSocket en primer plano.

 Además de la terminal, registra conexiones, emparejamientos y PIN rechazados en
 `~/.local/state/p1/cast.log` (rotativo, compartido con slide-tools).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --host     -H      <str>    Dirección IP de escucha (127.0.0.1 por defecto; 0.0.0.0 para LAN y   │
│                             loopback)                                                            │
│                             [por defecto: 127.0.0.1]                                             │
│ --port     -p      <int>    Puerto TCP para el servidor WebSocket [por defecto: 8765]            │
│ --timeout  -t      <float>  Tiempo límite para la confirmación de la extensión (segundos)        │
│                             [por defecto: 2.5]                                                   │
│ --pin              <str>    PIN de seguridad (si se omite, se genera uno de 6 dígitos con un     │
│                             generador criptográfico)                                             │
│ --no-pin                    Desactivar requerimiento de PIN (modo permisivo)                     │
│ --no-mdns                   Desactivar anuncio mDNS en la red local                              │
│ --no-qr                     Ocultar código QR en la consola al iniciar                           │
│ --help     -h               Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools status`

```text
 Uso: meet-tools status [OPCIONES]

 Consulta y muestra el estado actual consolidado de la sesión de Google Meet.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  URI del daemon concentrador [por defecto: ws://127.0.0.1:8765]            │
│ --json                 Emitir el estado como JSON versionado (sin Rich).                         │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools mic`

```text
 Uso: meet-tools mic [OPCIONES]

 Conmuta el micrófono propio (TOGGLE_MIC).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8765]                                   │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools cam`

```text
 Uso: meet-tools cam [OPCIONES]

 Conmuta la cámara propia (TOGGLE_CAM).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8765]                                   │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools hand`

```text
 Uso: meet-tools hand [OPCIONES]

 Conmuta levantar/bajar la mano (TOGGLE_HAND).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8765]                                   │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools admit-all`

```text
 Uso: meet-tools admit-all [OPCIONES]

 Acciona 'Admitir a todos' en la sala de espera (ADMIT_ALL).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8765]                                   │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools mute-all`

```text
 Uso: meet-tools mute-all [OPCIONES]

 Acciona 'Silenciar a todos' los participantes (MUTE_ALL).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8765]                                   │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools leave`

```text
 Uso: meet-tools leave [OPCIONES]

 Abandona la reunión (LEAVE_CALL).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --all   -a             Finalizar la llamada para todos (solo anfitriones)                        │
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8765]                                        │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools monitor`

```text
 Uso: meet-tools monitor [OPCIONES]

 Escucha y muestra en tiempo real todos los eventos y telemetría de Meet.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  URI del daemon concentrador [por defecto: ws://127.0.0.1:8765]            │
│ --json                 Emitir cada evento como una línea JSON (NDJSON) versionada.               │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools mock-tab`

```text
 Uso: meet-tools mock-tab [OPCIONES]

 Simula una pestaña de Google Meet con la extensión para pruebas locales.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --tab-id   -t             <str>  Identificador único de la pestaña simulada                      │
│                                  [por defecto: tab_mock_1]                                       │
│ --in-call      --lobby           Estado inicial de llamada [por defecto: in-call]                │
│ --host         --guest           Rol de anfitrión [por defecto: host]                            │
│ --uri      -u             <str>  [por defecto: ws://127.0.0.1:8765]                              │
│ --help     -h                    Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools pack`

```text
 Uso: meet-tools pack [OPCIONES]

 Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --target   -t      <str>  Navegador objetivo: chrome, firefox o both [por defecto: both]         │
│ --out-dir  -o      <str>  Directorio de salida para los paquetes [por defecto: dist]             │
│ --help     -h             Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools sign`

```text
 Uso: meet-tools sign [OPCIONES]

 Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --api-key     -k      <str>  API Key (JWT issuer) de Mozilla AMO                                 │
│ --api-secret  -s      <str>  API Secret de Mozilla AMO                                           │
│ --channel     -c      <str>  Canal de distribución: unlisted o listed [por defecto: unlisted]    │
│ --out-dir     -o      <str>  Directorio destino para el .xpi firmado [por defecto: dist]         │
│ --lint-only                  Solo validar compatibilidad y manifiesto con web-ext lint           │
│ --dry-run                    Verificar manifiesto e imprimir el comando web-ext sign sin enviar  │
│ --help        -h             Muestra esta ayuda y sale.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools qr`

```text
 Uso: meet-tools qr [OPCIONES]

 Muestra el código QR para emparejamiento directo con la app Android.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│    --port  -p      <int>  Puerto TCP WebSocket [por defecto: 8765]                               │
│ *  --pin           <str>  PIN de emparejamiento [obligatorio]                                    │
│    --host  -H      <str>  IP anfitrión (si se omite, se detecta automáticamente)                 │
│    --help  -h             Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools doctor`

```text
 Uso: meet-tools doctor [OPCIONES]

 Verifica el estado del entorno de MEET-TOOLS (Python, web-ext opcional).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools atajos`

```text
 Uso: meet-tools atajos [OPCIONES]

 Atajos de teclado globales: micrófono, cámara, mano, admitir y silenciar a todos.

 Funcionan con cualquier ventana enfocada (la terminal, las diapositivas): cada atajo corre
 `meet-tools <comando> --notificar`, que avisa con una notificación si algo falla. En GNOME
 se instalan con --instalar; en otros escritorios se muestran para cargarlos a mano.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --instalar                 Registrarlos como atajos personalizados de GNOME.                     │
│ --quitar                   Quitar los atajos de meet-tools de GNOME.                             │
│ --uri       -u      <str>  URI del daemon que van a usar los atajos.                             │
│                            [por defecto: ws://127.0.0.1:8765]                                    │
│ --help      -h             Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `meet-tools bandeja`

```text
 Uso: meet-tools bandeja [OPCIONES]

 Indicador en la bandeja del sistema: verde en llamada, amarillo sin llamada, gris sin daemon.

 Usa pystray (extra `bandeja` de cast-tools-common; en GNOME, con la extensión AppIndicator).
 Sin pystray, avisa cada cambio con una notificación de escritorio.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri             -u      <str>  URI del daemon. [por defecto: ws://127.0.0.1:8765]              │
│ --notificaciones                 Avisar con notificaciones aunque esté pystray.                  │
│ --help            -h             Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`meet-tools@42f0c8d`](https://github.com/martinvilu/meet-tools/tree/42f0c8d).
