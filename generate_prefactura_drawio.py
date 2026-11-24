import os
from xml.sax.saxutils import quoteattr

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Ciclo de vida Prefactura - lanes v1.02.drawio")

TOP, BOTTOM, HEAD = 32, 1519, 33
# id, title, x1, x2, header font size
LANES = [
    ("Entrega", "Entrega Informes", 58, 236, 14), ("Cobranza", "Cobranza", 236, 414, 14),
    ("Facturacion", "Facturación", 414, 575, 11), ("Impresion", "Impresión", 575, 753, 11),
    ("Calidad", "Calidad", 753, 931, 11),
]

R = "rounded=1;arcSize=6"
DASH = "dashed=1;dashPattern=3 3;"
# id, lane, x1, y1, x2, y2, text, extra style
NODES = [
    ("PorTimbrar", "Facturacion", 430, 81, 559, 178, "Por Timbrar", R),
    ("EnvioFisico", "Entrega", 90, 339, 220, 436, "Envío físico del Informe", R),
    ("EsperaAcuse", "Entrega", 155, 549, 285, 646, "En espera de acuse", R),
    ("CondPago", "Entrega", 155, 727, 285, 823, "Condiciones Pago", "rhombus"),
    ("FacturaPortal", "Cobranza", 268, 872, 398, 969, "Factura en portal", R),
    ("SeguimientoPago", "Cobranza", 268, 1082, 398, 1179, "Seguimiento del pago", R),
    ("Cobrada", "Cobranza", 268, 1293, 398, 1390, "Cobrada", R),
    ("EnvioElectronico", "Impresion", 599, 549, 729, 646, "Envio Elecrtonico", R + ";" + DASH),
    ("RegSatisfaccion", "Calidad", 769, 807, 899, 904, "Reg Satisfaccion al cliente", R + ";" + DASH),
]

# id, lane, x1, y1, x2, y2, text, fill
NOTES = [
    ("N1", "Impresion", 640, 97, 867, 227, "¿ Como manejar facturas de 50% adelanto y 50% al final ?", "#FFDD77"),
    ("N2", "Impresion", 640, 258, 851, 388, "¿ Como manejar re-facturas ?", "#FFDD77"),
    ("N3", "Facturacion", 430, 775, 559, 905, "Renombrar a Factura Ingresada", "#FFDD77"),
    ("N4", "Facturacion", 430, 936, 559, 1066, "La fecha de subida al portal da inicio al perido de crédito del cliente)", "#FFFF99"),
]

GRAY = "strokeColor=#B3B3B3;dashed=1;dashPattern=2 4;"
# src, tgt, label, waypoints, extra style
EDGES = [
    ("PorTimbrar", "EnvioFisico", "Se timbra la factura en AdminPaq<br>(Folio y serie del AdminPaq)", [], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
    ("EnvioFisico", "EsperaAcuse", "Informe enviado a las<br>instalaciones del Cliente", [], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
    ("EnvioFisico", "EnvioElectronico", "Aviso a Impresión de<br>la factura timbrada", [(440, 500)], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;" + GRAY),
    ("EsperaAcuse", "CondPago", "Se registra el acuse", [], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
    ("EsperaAcuse", "RegSatisfaccion", "Notificación email", [(450, 705)], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;" + GRAY),
    ("CondPago", "FacturaPortal", "", [], "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"),
    ("CondPago", "SeguimientoPago", "Pago anticipado<br>Pago 50-50<br>Pago a la entrega", [(180, 1060)], "exitX=0.5;exitY=1;entryX=0;entryY=0.5;"),
    ("FacturaPortal", "SeguimientoPago", "Fecha de registro<br>en Portal", [], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
    ("SeguimientoPago", "Cobrada", "Fecha de depósito<br>en el estado de cuenta", [], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
]


def build():
    ox = {n: x1 for n, _, x1, _, _ in LANES}
    cells = []
    for n, title, x1, x2, fs in LANES:
        cells.append(f'<mxCell id="lane_{n}" value={quoteattr(title)} style="swimlane;startSize={HEAD};fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontStyle=0;fontSize={fs};collapsible=0;" vertex="1" parent="1"><mxGeometry x="{x1}" y="{TOP}" width="{x2 - x1}" height="{BOTTOM - TOP}" as="geometry"/></mxCell>')
    for nid, lane, x1, y1, x2, y2, text, extra in NODES:
        cells.append(f'<mxCell id="{nid}" value={quoteattr(text)} style="{extra};whiteSpace=wrap;html=1;fontSize=11;strokeColor=#000000;strokeWidth=1.5;fillColor=#FFFFFF;" vertex="1" parent="lane_{lane}"><mxGeometry x="{x1 - ox[lane]}" y="{y1 - TOP}" width="{x2 - x1}" height="{y2 - y1}" as="geometry"/></mxCell>')
    for nid, lane, x1, y1, x2, y2, text, fill in NOTES:
        cells.append(f'<mxCell id="{nid}" value={quoteattr(text)} style="shape=note;size=25;whiteSpace=wrap;html=1;fontSize=11;strokeColor=#D6B656;fillColor={fill};" vertex="1" parent="1"><mxGeometry x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" as="geometry"/></mxCell>')
    cells.append(f'<mxCell id="T1" value={quoteattr("La fecha estimada de pago es igual a la fecha de acuse")} style="text;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;fontSize=11;" vertex="1" parent="1"><mxGeometry x="30" y="1018" width="145" height="60" as="geometry"/></mxCell>')
    for i, (src, tgt, label, pts, extra) in enumerate(EDGES, 1):
        points = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts)
        arr = f'<Array as="points">{points}</Array>' if pts else ""
        cells.append(f'<mxCell id="e{i}" value={quoteattr(label)} style="curved=1;html=1;endArrow=block;endFill=1;strokeColor=#000000;strokeWidth=1.5;fontSize=11;labelBackgroundColor=#FFFFFF;{extra}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')
    return ('<mxfile host="app.diagrams.net"><diagram id="prefactura-v102" name="Ciclo de vida Prefactura - lanes v1.02">'
            '<mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="1600" math="0" shadow="0">'
            '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print("draw.io file generated at", OUT)
