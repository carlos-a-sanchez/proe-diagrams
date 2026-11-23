# Ciclo de Vida OT - 2026
## Diagrama de procesos: Emisión de OT, Muestreo y Reporte de Resultados

```mermaid

---
config:
  htmlLabels: false
---

flowchart TD

    subgraph Cliente ["Cliente"]
        CteAutCot[Compras]
    end

    subgraph AtnCte ["Atención Clientes"]
        GenOT["`Generar OT
                _Folio OT_
                _Fecha Planif Muestreo_`"]
        HigEcolEval{¿Higiene o Ecología?}
    end

    subgraph OpeEco ["Operativo Ecología"]
        subgraph TecEco ["Técnico"]
        
            TecEcoMues["`Muestrea
                _Fecha Muestreo_`"]
        
            TecEcoHojas["`Captura Hojas de Campo
                _Fecha Hojas Campo_`"]
        
            TecEcoEnvMues["`Envia Muestra
                _Fecha Envio Muestra_`"]
        
        end
        subgraph CorEco ["Coordinador Ecología"]
            CordEcoRevisa["`Revisa Hojas de Campo
                _Fecha Revisión Hojas_`"]
            CordEcoEvalHojas{"Correciones?"}
        end
    end    

    subgraph OpeHig ["Operativo Higiene"]
        subgraph TecHig ["Técnico"]

            TecHigMues["`Muestrea
                _Fecha Muestreo_`"]
        
            TecHigHojas["`Captura Hojas de Campo
                _Fecha Hojas Campo_`"]
        
            TecHigEnvMues["`Envía Muestra
                _Fecha Envío Muestra_`"]
        
        end

        subgraph CorHig ["Coordinador Higiene"]
            CordHigRevisa["`Revisa Hojas de Campo
                _Fecha Revisión Hojas_`"]

            CordHigEvalHojas{"Correciones?"}
            CordHigEvalMX{"Revisa MX?"}
        end
    end

    subgraph LabEcoMX ["Laboratorio Ecología MX"]
        LabEcoMXRecMue["Recibe Muestras"]
        LabEcoMXAnaliza["Analiza Muestras"]
        LabEcoMXReporta["Reporta Resultados"]
    end    

    subgraph LabHigMX ["Laboratorio Higiene MX"]
        LabHigMXRecMue["Recibe Muestras"]
        LabHigMXAnaliza["Analiza Muestras"]
        LabHigMXReporta["Reporta Resultados"]
    end

    subgraph CaptEcoMX ["Revision y Captura Ecología MX"]
        CapEcoMxRevisa["Revisa"]
        CapEcoMxEval{"Correciones?"}
        CapEcoMxGenInfPDF["Genera Informe PDF"]    
    end    

    subgraph CaptHigMX ["Revision y Captura Higiene MX"]
        CapHigMxRevisa["Revisa"]
        CapHigMxEval{"Correciones?"}
        CapHigMxGenInfPDF["Genera Informe PDF"]    
    end

    subgraph CapLoc ["Captura e Impresión"]
        CapLocCaptura["Captura"]
        CapLocGenPDF["Genera PDF"]
        CapLocGenImp["Impresión"]
    end

    subgraph Cobranza ["Atención Clientes - Cobranza"]
        CobrCFDI["Genera CFDI"]
        CobrEnvioPDF["Envia PDF/CFDI a Usuario"]
    end

    subgraph Logistica ["Atención Clientes - Logística"]
        LogAcopio["Acopio del Informe Impreso"]
        LogEntrega["Entrega del Informe Impreso"]
        LogEntregado["Informe Impreso Entregado"]
    end
    %% -- Connections across lanes ---

    CteAutCot[Compras] -->|Autoriza Cotización| GenOT
    GenOT --> HigEcolEval

    %% -- Higiene Lane -------------

    HigEcolEval --> |Higiene| TecHigMues
    TecHigMues --> TecHigHojas
    TecHigHojas --> TecHigEnvMues
    TecHigEnvMues --> LabHigMXRecMue

    LabHigMXRecMue --> LabHigMXAnaliza
    LabHigMXAnaliza --> LabHigMXReporta


    TecHigHojas --> |"Hojas de Campo"| CordHigRevisa 
    CordHigRevisa --> CordHigEvalHojas

    %% does the "Hojas de campo" need re-work? 

    CordHigEvalHojas -->|"`Si
                           _Fecha Revision HdC_
                           _Marca Retrabajo_`"| TecHigHojas 

    CordHigEvalHojas -->|"`No
                           _Fecha Revisión HdC_`"| CordHigEvalMX

    %% is this Service reviewd in MX?

    CordHigEvalMX --> |"`No
                           _Fecha Captura Local_
                           _Aviso a Captura Local_`"| CapLocCaptura
    
    CordHigEvalMX --> |"`Si
                           _Fecha Sol. Rev MX_`"| CapHigMxRevisa

    LabHigMXReporta --> CapHigMxRevisa
    LabHigMXReporta -->|"`_Fecha Lab.MX Libera Resultados_`"| CapLocGenPDF

    CapHigMxRevisa --> CapHigMxEval

    %% does MX decide "Hojas de Campo" need re-work? 

    CapHigMxEval -->|"`Si
                        _Fecha Revisión MX_
                        _Marca Retrabajo MX_`"| CordHigRevisa
    CapHigMxEval -->|"`No
                        _Fecha Revisión MX_`"| CapHigMxGenInfPDF

    CapHigMxGenInfPDF -->|"`_Fecha MX Libera Informe PDF_
                            _Aviso a Facturación CFDI_`"| CapLocGenPDF 


    %% -- Ecología Lane -------------

    HigEcolEval --> |Ecología| TecEcoMues
    TecEcoMues --> TecEcoHojas
    TecEcoHojas --> TecEcoEnvMues
    TecEcoEnvMues --> LabEcoMXRecMue  
    LabEcoMXRecMue --> LabEcoMXAnaliza
    LabEcoMXAnaliza --> LabEcoMXReporta
    LabEcoMXReporta -->|"`_Fecha Lab.MX Libera Resultados_`"|  CapEcoMxRevisa

    LabEcoMXReporta --> CapLocGenPDF

    TecEcoHojas --> |"Hojas de Campo"| CordEcoRevisa 
    CordEcoRevisa --> CordEcoEvalHojas

    %% does the "Hojas de campo" need re-work? 

    CordEcoEvalHojas -->|"`Si
                           _Fecha Revision HdC_
                           _Marca Retrabajo_`"| TecEcoHojas

    CordEcoEvalHojas -->|"`No
                           _Fecha Revisión HdC_`"| CapEcoMxRevisa    

    CapEcoMxRevisa --> CapEcoMxEval

    %% does MX decide "Hojas de Campo" need re-work? 

    CapEcoMxEval --> |"`Si
                          _Fecha Revisión MX_
                          _Marca Retrabajo MX_`"| CordEcoRevisa    

    CapEcoMxEval --> |"`No
                           _Fecha Revisión MX_`"|CapEcoMxGenInfPDF

    CapEcoMxGenInfPDF -->|"`_Fecha MX Libera Informe PDF_
                            _Aviso a Facturación CFDI_`"| CapLocGenPDF



    %% -- Local Capture Lane -------------

    CapLocCaptura -->|"`_Fecha Genera PDF_
                        _Aviso a Facturación CFDI_`"| CapLocGenPDF

    CapLocGenPDF  -->|"`_Fecha PDF Listo para Impresión_
                        _Aviso a Cobranza_`"| CapLocGenImp

 
    %% -- Cobranza lane -------------

    CapLocGenPDF -.-> |"`_Aviso a Cobranza_`"| CobrEnvioPDF
    CapHigMxGenInfPDF -.-> |"`_Aviso a Facturación CFDI_`"| CobrCFDI
    CapEcoMxGenInfPDF    -.-> |"`_Aviso a Facturación CFDI_`"| CobrCFDI

    CobrCFDI --> CobrEnvioPDF


    %% -- Logística lane -------------

    CapLocGenImp -->|"`_Fecha Informe Impreso Listo_`"|  LogAcopio
    LogAcopio -->|"`_Fecha Envío Informe Impreso_`"| LogEntrega
    LogEntrega -->|"`_Fecha Acuse de Recibo_
                     _Evidencia Informe Recibido_
                     _OT Finalizada_`"| LogEntregado
    
    

```