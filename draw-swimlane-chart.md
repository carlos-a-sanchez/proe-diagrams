# Diagrama de Flujo Swimlane (OT-Laned-v2)

Read and interpret the following Mermaid syntax, and use it to build a chart (diagram.png) containing a swimlane flow diagram based on the interpretation of the Mermaid code. Consider the outer Subgraphs as lanes.

## Interpretación del Diagrama de Flujo y Carriles (Swimlanes)

El archivo `OT-Laned-v2.md` describe un proceso cross-funcional para la emisión de órdenes de trabajo (OT), muestreo en campo, análisis de laboratorio y generación de informes finales en dos vertientes principales: **Higiene** y **Ecología**.

### 1. Carriles Principales (Outer Subgraphs como Lanes)
1. **Cliente (`Cliente`)**:
   - `Compras`: Autoriza cotización para dar inicio al flujo operativo.
2. **Atención a Clientes (`AtencionClientes`)**:
   - `Generar OT`: Recibe la autorización y apertura la orden de trabajo.
   - `¿Higiene o Ecología?`: Decisión que bifurca el proceso a la disciplina correspondiente.
3. **Operativo Higiene (`OpeHig`)**:
   - Sub-carril **Técnico (`TecHig`)**: `Muestrea` -> `Hojas de Campo` -> `Envia Muestra`.
   - Sub-carril **Coordinador Higiene (`CorHig`)**: `Revisa Hojas de Campo` -> `¿Correcciones?` (reingreso a hojas de campo o pase a `¿Revisa MX?`).
4. **Laboratorio Higiene MX (`LabHigMX`)**:
   - Recepción, análisis y emisión de resultados (`Recibe Muestras` -> `Analiza Muestras` -> `Reporta Resultados`).
5. **Revisión y Captura Higiene MX (`CaptHigMX`)**:
   - Revisión de resultados y control de calidad (`Revisa` -> `¿Correcciones?` -> `Genera Informe PDF`).
6. **Operativo Ecología (`OpeEco`)**:
   - Sub-carril **Técnico (`TecEco`)**: `Muestreas` -> `Hojas de Campo` -> `Envia Muestra`.
   - Sub-carril **Coordinador Ecología (`CorEco`)**: `Revisa Hojas de Campo` -> `¿Correcciones?` (reingreso o pase a revisión MX).
7. **Laboratorio Ecología MX (`LabEcoMX`)**:
   - Recepción, análisis y reporte de ensayos (`Recibe Muestras` -> `Analiza Muestras` -> `Reporta Resultados`).
8. **Revisión y Captura Ecología MX (`CaptEcoMX`)**:
   - Revisión y emisión documental (`Revisa` -> `¿Correcciones?` -> `Genera Informe PDF`).
9. **Captura e Impresión (`CapLoc`)**:
   - Consolidación local: `Captura` -> `Genera PDF` -> `Impresión`.
10. **Atn Ctes - Cobranza (`Cobranza`)**:
    - Cierre del ciclo operativo y transición al proceso de cobranza y facturación.

### 2. Conexiones Interdepartamentales
- **Laboratorios a Captura Local**: Los resultados reportados por los laboratorios MX (`LabHigMX` y `LabEcoMX`) alimentan paralelamente la generación del PDF local (`CapLocGenPDF`).

## Archivo Generado
- **`diagram.png`**: Imagen en alta resolución del diagrama swimlane completo.
- **`diagram.svg`**: Archivo vectorial editable del diagrama.

