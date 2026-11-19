---
title: "cyberdeck"
---

<!-- Generado por scripts/generar_paginas.py desde cyberdeck@2da80d4: no editar a mano. -->

(manual-cyberdeck)=
# cyberdeck

Aplicación Android de periféricos para `hardboiled` (ola 40). Kotlin, Compose
Material 3, Android 8+ (API 26), WebSocket OkHttp y descubrimiento DNS-SD nativo.

## Compilar e instalar

Con JDK 17 o 21 y Android SDK 35:

```sh
export ANDROID_HOME="$HOME/Android/Sdk"
./gradlew assembleDebug testDebugUnitTest lintDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

El wrapper fija Gradle 8.14.4. La primera compilación descarga las dependencias.
También se genera el APK en CI como artefacto descargable.

## Usar en clase

Iniciá `hardboiled run programa.c --board placa.toml --remote` en la computadora.
La placa debe tener un ADC de tres canales o más. Abrí Cyberdeck en el teléfono:

1. **Buscar en Wi-Fi** encuentra la IP/puerto por mDNS; ingresá el PIN de seis dígitos.
2. **Escanear QR** completa IP/puerto/PIN desde el QR mostrado en la terminal.
3. Si la red bloquea multicast, completá IP/puerto/PIN a mano.

El escáner integrado usa Google Code Scanner (ML Kit) y requiere Google Play
Services. No solicita permiso de cámara. La entrada manual y mDNS no dependen de
Play Services. El módulo muestra sólo las capacidades de hardware negociadas.

X/Y/Z se mapean a ADC 0/1/2: −g → 0 mV, 0 → Vref/2, +g → Vref.
El rango se satura y la referencia procede de la placa. Se puede elegir 20–60 Hz.
Los pulsadores tienen confirmación háptica; una sacudida >2,5g activa la IRQ externa
cuando el manifiesto la ofrece. Los sensores se suspenden al pausar la actividad;
al salir se desconecta y borra el PIN de memoria. Durante una pérdida temporal de
Wi-Fi se reintenta con token efímero y espera exponencial hasta 30 segundos.
No se guardan credenciales ni se envían muestras antes de autenticar y negociar.

El contrato del módulo se documenta en `docs/hardboiled.md`. Las especificaciones
`android-spec.md` y `companion/spec.md` describen la evolución general del producto;
los perfiles Meet/Slides, UDP broadcast y el companion de escritorio no forman
parte de esta implementación.

Generado desde `cyberdeck@2da80d4`.
