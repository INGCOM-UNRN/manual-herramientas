---
title: "slide-tools"
---

<!-- Generado por scripts/generar_paginas.py desde slide-tools@9527b09: no editar a mano. -->

(manual-slide_tools)=
# slide-tools

Repositorio: [github.com/martinvilu/slides-tools](https://github.com/martinvilu/slides-tools).

Sistema de control remoto y telemetría bidireccional para Google Slides desde dispositivos externos (aplicación nativa Android y hardware embebido Wi-Fi operando en simultáneo) mediante una extensión de navegador WebExtensions y un daemon concentrador local/LAN.

Basado en la especificación técnica [spec.md](https://github.com/martinvilu/slides-tools/blob/main/spec.md) (Versión 1.2).

---

## Arquitectura General

```
┌────────────────────────────────────────────────────────┐
│               Clientes Externos en LAN                 │
│  ┌───────────────────────┐   ┌──────────────────────┐  │
│  │  App Nativa Android   │   │  Hardware Wi-Fi      │  │
│  │  - Visor de notas     │   │  (ESP32 / RP2040W)   │  │
│  │  - Temporizador sync  │   │  - Botones físicos   │  │
│  │  - Control táctil     │   │  - Display OLED/LED  │  │
│  └───────────┬───────────┘   └──────────┬───────────┘  │
└──────────────┼──────────────────────────┼──────────────┘
               │                          │
               │ WebSocket LAN            │ WebSocket LAN
               │ (ws://<HOST_IP>:8766)    │ (ws://<HOST_IP>:8766)
               ▼                          ▼
┌────────────────────────────────────────────────────────┐
│             Daemon Local / Servidor de Enlace          │
│  - Enlace en 0.0.0.0:8766 (LAN + Loopback 127.0.0.1)   │
│  - Soporte multicliente con difusión broadcast de state│
│  - Emparejamiento por PIN/Token por sesión activa      │
│  - Temporizador emulado (fallback)                     │
└───────────────────────────┬────────────────────────────┘
                            │
                            │ WebSocket Loopback (ws://127.0.0.1:8766)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Extensión Web (WebExtensions)              │
│       (Chromium / Firefox en docs.google.com)          │
│  ├─ Background Worker / Orchestrator                   │
│  ├─ Content Script: Pantalla Principal (/present)      │
│  │  ├─ Inyección teclado & Mini-Dock (PIN/Status/QR)   │
│  │  └─ Detección de diapositivas y títulos             │
│  └─ Content Script: Vista de Orador (Popup Window)     │
│     ├─ Extracción DOM de notas ricas y cronómetro      │
│     ├─ Inyección UI Toolbar compacta                   │
│     └─ Control bidireccional de pausa/reset timer      │
└────────────────────────────────────────────────────────┘
```

---

## Componentes del Sistema

1. **`slide_tools.daemon`**:
   - Servidor WebSocket multicliente enlazado en `0.0.0.0:8766`.
   - Administra el estado canónico de la presentación en memoria.
   - Seguridad mediante **código PIN de 4 dígitos** para emparejar clientes remotos.
   - Difunde en tiempo real (`broadcast`) cualquier cambio de diapositiva, notas o cronómetro a todos los clientes emparejados.
   - Cuenta con temporizador de respaldo en caso de que el usuario proyecte en pantalla completa estándar sin abrir la ventana de vista de orador.

2. **`extension/` (WebExtensions MV3)**:
   - Compatible con Google Chrome, Chromium, Brave, Edge y Firefox en URLs `https://docs.google.com/presentation/*`.
   - **`background.js`**: Conexión WebSocket resiliente con reconexión automática a `ws://127.0.0.1:8766`.
   - **`content-present.js`**: Dispara eventos sintéticos de teclado (`ArrowRight`, `ArrowLeft`, `Home`, `End`, `b`, `w`, `l`, dígitos numéricos + `Enter`) e inyecta el **Mini-Dock retráctil** con estado, PIN y botón de código QR.
   - **`content-speaker.js`**: Inspecciona el DOM de la ventana de notas (`.punch-speaker-notes-text`, `.punch-speaker-notes-timer-value`), limpia el texto plano UTF-8 para microcontroladores y controla los botones de pausa/reinicio del cronómetro nativo.
   - **`overlay.css`**: Estilos para el Mini-Dock, barra superior de vista de orador y modal de emparejamiento por QR.

3. **`slide_tools.cli` (`slide-tools`)**:
   - Interfaz de comandos para gestionar el daemon, inspeccionar telemetría en vivo, conmutar controles remotos o simular presentaciones para pruebas locales.

---

## Instalación y Puesta en Marcha

### Requisitos

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) instalado en el sistema

### 1. Iniciar el Daemon Concentrador

```bash
cd /home/mrtin/dev/tools/slide-tools
uv sync
uv run slide-tools daemon
```

Opciones:
- `--host` / `-h`: IP de enlace (por defecto `0.0.0.0`).
- `--port` / `-p`: Puerto TCP (por defecto `8766`).
- `--pin`: PIN de 4 dígitos fijo (si se omite, se genera aleatoriamente al iniciar).
- `--no-pin`: Modo permisivo para desarrollo sin validación de PIN.

### 2. Cargar la Extensión en el Navegador

#### Google Chrome / Chromium / Brave / Edge:
1. Navegá a `chrome://extensions/`.
2. Activá el **Modo de desarrollador**.
3. Hacé clic en **Cargar descomprimida**.
4. Seleccioná la carpeta `/home/mrtin/dev/tools/slide-tools/extension`.

#### Firefox:
1. Abrí `about:debugging#/runtime/this-firefox`.
2. Hacé clic en **Cargar complemento temporal**.
3. Seleccioná `/home/mrtin/dev/tools/slide-tools/extension/manifest.json`.

---

## Uso de la CLI (`slide-tools`)

```bash
# Ver estado consolidado de la presentación
uv run slide-tools status

# Navegación básica (desde el mismo equipo no hace falta el PIN; contra un daemon de otro
# equipo, --pin <PIN> o la variable SLIDE_TOOLS_PIN)
uv run slide-tools next                    # Siguiente diapositiva o animación
uv run slide-tools prev                    # Diapositiva anterior
uv run slide-tools first                   # Primera diapositiva
uv run slide-tools last                    # Última diapositiva
uv run slide-tools goto 14                 # Saltar a la diapositiva 14

# Efectos visuales de presentación
uv run slide-tools blackout                # Conmutar pantalla en negro (tecla b)
uv run slide-tools whiteout                # Conmutar pantalla en blanco (tecla w)
uv run slide-tools laser                   # Conmutar puntero láser virtual (tecla l)

# Control del cronómetro
uv run slide-tools timer-reset             # Reiniciar temporizador
uv run slide-tools timer-pause             # Pausar o reanudar cronómetro

# Monitoreo continuo de eventos y notas en terminal
uv run slide-tools monitor

# Simular presentación para pruebas de hardware / app móvil sin navegador
uv run slide-tools mock-slides --slides 20
```

### Atajos de teclado globales

```bash
slide-tools atajos              # muestra los atajos y si están instalados
slide-tools atajos --instalar   # los registra en GNOME (Configuración → Teclado)
slide-tools atajos --quitar
```

| Atajo | Acción |
|:--|:--|
| Ctrl+Alt+AvPág | siguiente |
| Ctrl+Alt+RePág | anterior |
| Ctrl+Alt+B | pantalla en negro |
| Ctrl+Alt+P | pausar o reanudar el temporizador |
| Ctrl+Alt+R | reiniciar el temporizador |

Funcionan con cualquier ventana enfocada (la terminal, Meet): cada atajo es un atajo del
escritorio que corre `slide-tools <comando> --notificar`, que avisa con una notificación si algo
falla. Fuera de GNOME, `slide-tools atajos` muestra los comandos para cargarlos a mano.

### Indicador en la bandeja y registro

`slide-tools bandeja` muestra un círculo verde (presentando), amarillo (daemon sin presentación) o
gris (sin daemon). Necesita pystray: `uv tool install --with pystray --with pillow …`, y en GNOME
la extensión «AppIndicator and KStatusNotifierItem Support». Sin pystray avisa cada cambio con una
notificación de escritorio.

El daemon registra conexiones, emparejamientos y PIN rechazados en `~/.local/state/p1/cast.log`
(rotativo, compartido con meet-tools).

### Seguridad del emparejamiento

- **El PIN protege la red del aula.** Una conexión desde el mismo equipo sin origen web (la CLI,
  un atajo, la bandeja, la extensión) no lo necesita; un dispositivo de la red, y la extensión si
  el daemon está en otro equipo, se emparejan con `PAIR_REQUEST`.
- **Decir que se es la extensión no empareja**: la extensión se empareja con el PIN como cualquier
  cliente (lo manda en su `PAIR_REQUEST`).
- **Token de reconexión.** `PAIRING_SUCCESS` trae `token` y `expiresIn` (8 h); un `PAIR_REQUEST`
  con `{"token": …}` reemplaza al PIN. Viven en memoria: reiniciar el daemon los invalida.
- **Ninguna página web puede conectarse**: 403 a todo WebSocket con `Origin` de una página.
- **El PIN y el QR sólo a quien ya está emparejado**: en el saludo a un dispositivo sin emparejar
  `pin` llega vacío.
- Cinco PIN equivocados en un minuto bloquean esa IP.

---

## Consumidores e integración con cyberdeck

**Estado real: especificación, no verificado contra un cliente.** El consumidor
declarado, `cyberdeck` (app Android), existe solo como especificación
(`cyberdeck/android-spec.md`, que lo lista contra `slide-tools (ws:8766)`); no hay
cliente implementado ni prueba de integración con este daemon. No se invoca a
ninguna otra herramienta del ecosistema desde aquí.

Lo que este repo sí garantiza (fijado en `tests/test_contrato_cyberdeck.py`):

- Puerto por defecto del daemon: `8766`.
- Servicio mDNS publicado: `_slide-bridge._tcp.local.` (propiedad `service=slides`). La spec
  de cyberdeck describe `_slide-bridge._sub._bridge-remote._tcp.local.`: **esa forma con
  subtipo no está implementada**; un cliente debe descubrir por el tipo plano.
- URI de emparejamiento `bridge://pair?v=1.3&host=…&port=8766&service=slides&pin=…&name=…`.
- Salida `--json` versionada (`schema_version`) en `status` y `monitor` para
  consumidores externos que no hablen WebSocket.

---

## Protocolo JSON v1.2

Estructura de paquete estándar:

```json
{
  "version": "1.2",
  "sessionId": "default",
  "source": "android" | "hardware" | "daemon" | "extension",
  "type": "command" | "state" | "event" | "ack" | "error",
  "action": "string",
  "payload": {}
}
```

### Telemetría de `STATE_SYNC`

```json
{
  "presentationTitle": "Plan de Operaciones 2026",
  "isPresenting": true,
  "presentationMode": "presenter_view",
  "currentSlide": 14,
  "totalSlides": 45,
  "isBlackout": false,
  "isWhiteout": false,
  "isLaserActive": false,
  "timer": {
    "elapsedSeconds": 754,
    "formattedTime": "12:34",
    "isPaused": false
  },
  "speakerNotes": {
    "hasNotes": true,
    "currentSlideNotes": "Enfatizar que la reducción de costos en la fase 2 no afecta los plazos."
  },
  "connectedClients": 2,
  "pin": "4821"
}
```

---

## Pruebas Automatizadas

```bash
uv run pytest -v
```

---

## Empaquetado para Chrome y Firefox

Para empaquetar la extensión lista para cargar o distribuir:

```bash
uv run slide-tools pack
```

Opciones:
- `--target` / `-t`: `both` (por defecto), `chrome` o `firefox`.
- `--out-dir` / `-o`: Directorio de salida (por defecto `dist/`).

Archivos generados en `dist/`:
- **`slide-bridge-chrome-v1.2.0.zip`**: Manifiesto con `background.service_worker` para Chromium.
- **`slide-bridge-firefox-v1.2.0.xpi`**: Manifiesto con `background.scripts` y `browser_specific_settings.gecko` para Firefox MV3.

## Limitaciones

- Solo Google Slides (`docs.google.com/presentation`) en un navegador con la extensión cargada
  (Chrome, Chromium, Brave, Edge o Firefox).
- La extensión controla la presentación a través de la página (su content script maneja el DOM de
  Slides): un cambio en la interfaz de Google puede dejar sin efecto algún comando hasta que se
  actualice la extensión.
- Los dispositivos se conectan al daemon por WebSocket dentro de la red local: no hay un servidor en
  internet.

## Referencia rápida

### Requisitos

- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Comandos

| Comando | Descripción |
|:--|:--|
| `slide-tools daemon` | Inicia el daemon concentrador WebSocket en primer plano. |
| `slide-tools status` | Muestra el estado consolidado de la presentación activa. |
| `slide-tools next` | Avanza a la siguiente diapositiva o animación (NEXT_SLIDE). |
| `slide-tools prev` | Retrocede a la diapositiva o animación anterior (PREV_SLIDE). |
| `slide-tools first` | Salta a la primera diapositiva (FIRST_SLIDE). |
| `slide-tools last` | Salta a la última diapositiva (LAST_SLIDE). |
| `slide-tools goto` | Salta directamente a una diapositiva específica (GO_TO_SLIDE). |
| `slide-tools blackout` | Conmuta pantalla en negro (TOGGLE_BLACKOUT). |
| `slide-tools whiteout` | Conmuta pantalla en blanco (TOGGLE_WHITEOUT). |
| `slide-tools laser` | Conmuta puntero láser virtual (TOGGLE_LASER). |
| `slide-tools timer-reset` | Reinicia el temporizador (TIMER_RESET). |
| `slide-tools timer-pause` | Pausa o reanuda el temporizador (TIMER_TOGGLE_PAUSE). |
| `slide-tools monitor` | Monitorea en tiempo real cambios de diapositiva, notas y cronómetro. |
| `slide-tools mock-slides` | Simula una sesión de Google Slides conectada al daemon para pruebas. |
| `slide-tools pack` | Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi). |
| `slide-tools sign` | Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext. |
| `slide-tools qr` | Muestra el código QR para emparejamiento directo con la app Android. |
| `slide-tools doctor` | Verifica el estado del entorno de SLIDE-TOOLS (Python, web-ext opcional). |
| `slide-tools atajos` | Atajos de teclado globales: avanzar, retroceder, pantalla en negro y temporizador. |
| `slide-tools bandeja` | Indicador en la bandeja del sistema: verde presentando, amarillo sin presentación, gris sin daemon. |

Ayuda de cada comando: `slide-tools <comando> -h`.

### Salida JSON

Con `--json`, estos comandos emiten el resultado como JSON por la salida estándar, para usarlo desde scripts, ripley o dredd: `slide-tools status`, `slide-tools monitor`, `slide-tools doctor`. El de `doctor --json` lleva `schema_version` y `ok`.

### Códigos de salida

| Código | Significado |
|:--|:--|
| `0` | Terminó bien (en `doctor`: está todo lo requerido). |
| `1` | El comando encontró problemas (hallazgos, pruebas que fallan, un umbral que no se alcanza) o un dato no se pudo usar (un archivo ilegible, un formato inválido). |
| `2` | Error de uso: comando, opción o argumento inválido. |

(manual-slide_tools-comandos)=
## Ayuda de los comandos

La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.

:::{dropdown} `slide-tools`
:open:

```text
 Uso: slide-tools [OPCIONES] COMANDO [ARGUMENTOS]...

 Sistema de control remoto para Google Slides.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de slide-tools y sale.                        │
│ --install-completion            Instala el autocompletado para la terminal actual.               │
│ --show-completion               Muestra el autocompletado para la terminal actual, para copiarlo │
│                                 o adaptarlo.                                                     │
│ --help                -h        Muestra esta ayuda y sale.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Comandos ───────────────────────────────────────────────────────────────────────────────────────╮
│ daemon       Inicia el daemon concentrador WebSocket en primer plano.                            │
│ status       Muestra el estado consolidado de la presentación activa.                            │
│ next         Avanza a la siguiente diapositiva o animación (NEXT_SLIDE).                         │
│ prev         Retrocede a la diapositiva o animación anterior (PREV_SLIDE).                       │
│ first        Salta a la primera diapositiva (FIRST_SLIDE).                                       │
│ last         Salta a la última diapositiva (LAST_SLIDE).                                         │
│ goto         Salta directamente a una diapositiva específica (GO_TO_SLIDE).                      │
│ blackout     Conmuta pantalla en negro (TOGGLE_BLACKOUT).                                        │
│ whiteout     Conmuta pantalla en blanco (TOGGLE_WHITEOUT).                                       │
│ laser        Conmuta puntero láser virtual (TOGGLE_LASER).                                       │
│ timer-reset  Reinicia el temporizador (TIMER_RESET).                                             │
│ timer-pause  Pausa o reanuda el temporizador (TIMER_TOGGLE_PAUSE).                               │
│ monitor      Monitorea en tiempo real cambios de diapositiva, notas y cronómetro.                │
│ mock-slides  Simula una sesión de Google Slides conectada al daemon para pruebas.                │
│ pack         Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi).           │
│ sign         Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext.       │
│ qr           Muestra el código QR para emparejamiento directo con la app Android.                │
│ doctor       Verifica el estado del entorno de SLIDE-TOOLS (Python, web-ext opcional).           │
│ atajos       Atajos de teclado globales: avanzar, retroceder, pantalla en negro y temporizador.  │
│ bandeja      Indicador en la bandeja del sistema: verde presentando, amarillo sin presentación,  │
│              gris sin daemon.                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools daemon`

```text
 Uso: slide-tools daemon [OPCIONES]

 Inicia el daemon concentrador WebSocket en primer plano.

 Además de la terminal, registra conexiones, emparejamientos y PIN rechazados en
 `~/.local/state/p1/cast.log` (rotativo, compartido con meet-tools).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --host     -H      <str>    Dirección IP de escucha (127.0.0.1 por defecto; 0.0.0.0 para LAN)    │
│                             [por defecto: 127.0.0.1]                                             │
│ --port     -p      <int>    Puerto TCP WebSocket [por defecto: 8766]                             │
│ --pin              <str>    PIN fijo (si se omite, se genera uno de 6 dígitos con un generador   │
│                             criptográfico)                                                       │
│ --no-pin                    Desactivar requerimiento de PIN (modo permisivo)                     │
│ --no-mdns                   Desactivar publicación mDNS/Zeroconf                                 │
│ --no-qr                     Ocultar código QR en la consola                                      │
│ --timeout  -t      <float>  Tiempo límite de respuesta de la extensión [por defecto: 2.5]        │
│ --help     -h               Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools status`

```text
 Uso: slide-tools status [OPCIONES]

 Muestra el estado consolidado de la presentación activa.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  URI del daemon [por defecto: ws://127.0.0.1:8766]                         │
│ --json                 Emitir el estado como JSON versionado (sin Rich).                         │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools next`

```text
 Uso: slide-tools next [OPCIONES]

 Avanza a la siguiente diapositiva o animación (NEXT_SLIDE).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8766]                                   │
│ --pin        -k      <str>                                                                       │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools prev`

```text
 Uso: slide-tools prev [OPCIONES]

 Retrocede a la diapositiva o animación anterior (PREV_SLIDE).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8766]                                   │
│ --pin        -k      <str>                                                                       │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools first`

```text
 Uso: slide-tools first [OPCIONES]

 Salta a la primera diapositiva (FIRST_SLIDE).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8766]                                        │
│ --pin   -k      <str>                                                                            │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools last`

```text
 Uso: slide-tools last [OPCIONES]

 Salta a la última diapositiva (LAST_SLIDE).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8766]                                        │
│ --pin   -k      <str>                                                                            │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools goto`

```text
 Uso: slide-tools goto [OPCIONES] {slide}

 Salta directamente a una diapositiva específica (GO_TO_SLIDE).

╭─ Argumentos ─────────────────────────────────────────────────────────────────────────────────────╮
│ *    slide      <int>  Número de diapositiva de destino [obligatorio]                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8766]                                        │
│ --pin   -k      <str>                                                                            │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools blackout`

```text
 Uso: slide-tools blackout [OPCIONES]

 Conmuta pantalla en negro (TOGGLE_BLACKOUT).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8766]                                   │
│ --pin        -k      <str>                                                                       │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools whiteout`

```text
 Uso: slide-tools whiteout [OPCIONES]

 Conmuta pantalla en blanco (TOGGLE_WHITEOUT).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8766]                                        │
│ --pin   -k      <str>                                                                            │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools laser`

```text
 Uso: slide-tools laser [OPCIONES]

 Conmuta puntero láser virtual (TOGGLE_LASER).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8766]                                        │
│ --pin   -k      <str>                                                                            │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools timer-reset`

```text
 Uso: slide-tools timer-reset [OPCIONES]

 Reinicia el temporizador (TIMER_RESET).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8766]                                   │
│ --pin        -k      <str>                                                                       │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools timer-pause`

```text
 Uso: slide-tools timer-pause [OPCIONES]

 Pausa o reanuda el temporizador (TIMER_TOGGLE_PAUSE).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri        -u      <str>  [por defecto: ws://127.0.0.1:8766]                                   │
│ --pin        -k      <str>                                                                       │
│ --notificar                 Avisar los errores con una notificación (para atajos de teclado).    │
│ --help       -h             Muestra esta ayuda y sale.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools monitor`

```text
 Uso: slide-tools monitor [OPCIONES]

 Monitorea en tiempo real cambios de diapositiva, notas y cronómetro.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri   -u      <str>  [por defecto: ws://127.0.0.1:8766]                                        │
│ --pin   -k      <str>                                                                            │
│ --json                 Emitir cada evento como una línea JSON (NDJSON) versionada.               │
│ --help  -h             Muestra esta ayuda y sale.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools mock-slides`

```text
 Uso: slide-tools mock-slides [OPCIONES]

 Simula una sesión de Google Slides conectada al daemon para pruebas.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --slides  -s      <int>  Cantidad de diapositivas simuladas [por defecto: 10]                    │
│ --uri     -u      <str>  [por defecto: ws://127.0.0.1:8766]                                      │
│ --help    -h             Muestra esta ayuda y sale.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools pack`

```text
 Uso: slide-tools pack [OPCIONES]

 Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --target   -t      <str>  Navegador objetivo: chrome, firefox o both [por defecto: both]         │
│ --out-dir  -o      <str>  Directorio de salida para los paquetes [por defecto: dist]             │
│ --help     -h             Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools sign`

```text
 Uso: slide-tools sign [OPCIONES]

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

:::{dropdown} `slide-tools qr`

```text
 Uso: slide-tools qr [OPCIONES]

 Muestra el código QR para emparejamiento directo con la app Android.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│    --port  -p      <int>  Puerto TCP WebSocket [por defecto: 8766]                               │
│ *  --pin           <str>  PIN de emparejamiento [obligatorio]                                    │
│    --host  -H      <str>  IP anfitrión (si se omite, se detecta automáticamente)                 │
│    --help  -h             Muestra esta ayuda y sale.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools doctor`

```text
 Uso: slide-tools doctor [OPCIONES]

 Verifica el estado del entorno de SLIDE-TOOLS (Python, web-ext opcional).

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --json            Emitir diagnóstico en formato JSON estructurado.                               │
│ --help  -h        Muestra esta ayuda y sale.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools atajos`

```text
 Uso: slide-tools atajos [OPCIONES]

 Atajos de teclado globales: avanzar, retroceder, pantalla en negro y temporizador.

 Funcionan con cualquier ventana enfocada: cada atajo corre `slide-tools <comando>
 --notificar`, que avisa con una notificación si algo falla. En GNOME se instalan con
 --instalar; en otros escritorios se muestran para cargarlos a mano.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --instalar                 Registrarlos como atajos personalizados de GNOME.                     │
│ --quitar                   Quitar los atajos de slide-tools de GNOME.                            │
│ --uri       -u      <str>  URI del daemon que van a usar los atajos.                             │
│                            [por defecto: ws://127.0.0.1:8766]                                    │
│ --help      -h             Muestra esta ayuda y sale.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

:::{dropdown} `slide-tools bandeja`

```text
 Uso: slide-tools bandeja [OPCIONES]

 Indicador en la bandeja del sistema: verde presentando, amarillo sin presentación, gris sin
 daemon.

 Usa pystray (extra `bandeja` de cast-tools-common; en GNOME, con la extensión AppIndicator).
 Sin pystray, avisa cada cambio con una notificación de escritorio.

╭─ Opciones ───────────────────────────────────────────────────────────────────────────────────────╮
│ --uri             -u      <str>  URI del daemon. [por defecto: ws://127.0.0.1:8766]              │
│ --notificaciones                 Avisar con notificaciones aunque esté pystray.                  │
│ --help            -h             Muestra esta ayuda y sale.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
:::

Generado desde [`slide-tools@9527b09`](https://github.com/martinvilu/slides-tools/tree/9527b09).
