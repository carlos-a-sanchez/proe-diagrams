# Fases del Ciclo de Vida de Prefactura (lanes v1.02)

Fuente: `Ciclo de vida Prefactura - lanes v1.02.drawio`. Las fases son los nodos del diagrama, en el orden del flujo.

| # | Fase | Carril | Tipo |
|---|---|---|---|
| 1 | Por Timbrar | Facturación | Principal |
| 2 | Envío físico del Informe | Entrega Informes | Principal |
| 3 | En espera de acuse | Entrega Informes | Principal |
| 4 | Condiciones Pago | Entrega Informes | Decisión |
| 5 | Factura en portal | Cobranza | Principal |
| 6 | Seguimiento del pago | Cobranza | Principal |
| 7 | Cobrada | Cobranza | Principal |
| 8 | Envio Elecrtonico | Impresión | Paralela (borde punteado) |
| 9 | Reg Satisfaccion al cliente | Calidad | Paralela (borde punteado) |

Las fases 8 y 9 no están en el flujo principal: reciben avisos por flechas punteadas grises.

## Transiciones

- Por Timbrar → Envío físico del Informe ("Se timbra la factura en AdminPaq (Folio y serie del AdminPaq)")
- Envío físico del Informe → En espera de acuse ("Informe enviado a las instalaciones del Cliente")
- Envío físico del Informe ⇢ Envio Elecrtonico ("Aviso a Impresión de la factura timbrada", punteada)
- En espera de acuse → Condiciones Pago ("Se registra el acuse")
- En espera de acuse ⇢ Reg Satisfaccion al cliente ("Notificación email", punteada)
- Condiciones Pago → Factura en portal
- Condiciones Pago → Seguimiento del pago ("Pago anticipado / Pago 50-50 / Pago a la entrega")
- Factura en portal → Seguimiento del pago ("Fecha de registro en Portal")
- Seguimiento del pago → Cobrada ("Fecha de depósito en el estado de cuenta")

## Carriles (roles)

Entrega Informes, Cobranza, Facturación, Impresión, Calidad.

## Notas del diagrama

- **Impresión:** "¿ Como manejar facturas de 50% adelanto y 50% al final ?"
- **Impresión:** "¿ Como manejar re-facturas ?"
- **Facturación:** "Renombrar a Factura Ingresada"
- **Facturación:** "La fecha de subida al portal da inicio al perido de crédito del cliente)"
- **Texto suelto:** "La fecha estimada de pago es igual a la fecha de acuse"
