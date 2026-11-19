---
title: "Cyberdeck"
subtitle: "Periféricos Android para Hardboiled"
---

(manual-cyberdeck)=
# Cyberdeck — Periféricos para Hardboiled

Cyberdeck es una aplicación Android que se conecta a `hardboiled` para aportar sensores y controles a una placa emulada. Permite descubrir la computadora por Wi-Fi, escanear un QR o introducir la conexión manualmente. Los sensores y botones disponibles dependen de las capacidades de la placa negociadas al conectar.

En la computadora, iniciá Hardboiled con una placa compatible y la opción `--remote`. La aplicación muestra las opciones de conexión y pide el PIN correspondiente.

```bash
hardboiled run programa.c --board placa.toml --remote
```

El repositorio local `cyberdeck` contiene instrucciones de compilación y uso. El manifiesto de `p1-tools` todavía clasifica Cyberdeck como especificación; la aplicación Android ya está implementada. Las funciones de Meet y Slides descritas en las especificaciones no forman parte de esta implementación.
