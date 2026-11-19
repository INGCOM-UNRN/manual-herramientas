---
title: "Infraestructura de Aula y Exámenes"
subtitle: "Máquina virtual de la cursada, emulación RISC-V bare-metal y exámenes supervisados con uatu"
---

(aula-examenes-indice)=
# Infraestructura de Aula y Exámenes

Herramientas del perfil aula y docente orientadas a prácticas de laboratorio avanzadas, simulación de hardware y control criptográfico durante evaluaciones supervisadas.

---

## Componentes de Aula

* **[construct](construct.md)**: IDE pedagógico y orquestador de la máquina virtual de la cursada (QEMU) en Linux, Windows y macOS.
* **[hardboiled](hardboiled.md)**: Emulador pedagógico de un microcontrolador RISC-V 32 bits (RV32I) bare-metal, con periféricos mapeados en memoria descritos por placa y casos de prueba (`hardboiled test`).
* **[uatu-tools](uatu_tools.md)**: CLIs docentes de [uatu](https://github.com/INGCOM-UNRN-P1/uatu): `uatu-admin` (claves, registro y configuración firmados, protección de ramas, consignas y paquetes con bloqueo de tiempo) y `uatu-audit` (verificación de la evidencia registrada en el examen).
