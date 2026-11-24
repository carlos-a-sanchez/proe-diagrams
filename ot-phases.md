# Fases del Ciclo de Vida de OT (lanes v1 - 2016)

Fuente: `Ciclo vida OT - lanes v1 - 2016.drawio`. Las fases son los nodos del diagrama, en el orden del flujo.

| # | Fase | Carril |
|---|---|---|
| 1 | Captura | Administrativo |
| 2 | Muestreo | Signatario |
| 3 | Espera Resultados Laboratorio | Signatario |
| 4 | Generación de Informe | Signatario |
| 5 | Rev. Cruzada | Otros Signatarios |
| 6 | Control de Calidad del Informe (Ignacio) (PDF) | Calidad |
| 7 | Signatario genera PDF | Signatario |
| 8 | Entrega Electrónica ( antes VoBo Cliente ) | Impresión |
| 9 | Impresión de Informe | Impresión |
| 10 | Informe Entregado al Cliente | Administrativo |
| 11 | Cerrada | Administrativo |

## Transiciones

- Captura → Muestreo
- Muestreo → Espera Resultados Laboratorio
- Muestreo → Generación de Informe (etiqueta: "Agentes físicos")
- Espera Resultados Laboratorio → Generación de Informe
- Generación de Informe → Rev. Cruzada
- Rev. Cruzada ↔ Control de Calidad del Informe (doble sentido)
- Control de Calidad del Informe → Signatario genera PDF
- Signatario genera PDF → Entrega Electrónica
- Entrega Electrónica → Generación de Informe
- Entrega Electrónica → Impresión de Informe (etiqueta: "ok")
- Impresión de Informe → Informe Entregado al Cliente
- Informe Entregado al Cliente → Cerrada

## Carriles (roles)

Cliente, Signatario, Calidad, Otros Signatarios, Impresión, Administrativo, Laboratorio.

Los carriles Cliente y Laboratorio no tienen fases propias; solo el carril Cliente tiene una nota.

## Notas del diagrama

- **Cliente:** "Fecha Fin Muestreo / Inicio de los 10 dias / Muestreo Ini x Area / Planeación"
- **Signatario:** "Fecha del Expediente B son necesarios para pasar a esta fase"
- **Signatario:** "Permitir que Erika pueda capturar esta fecha"
- **Otros Signatarios:** "Control de calidad revisa editables"
- **Administrativo:** "Estas fases son manejadas desde la prefactura"
