import os
from xml.sax.saxutils import quoteattr

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Ciclo vida OT - lanes v1 - 2016.drawio")

TOP, BOTTOM, HEAD = 24, 1067, 23
LANES = [
    ("Cliente", 24, 209), ("Signatario", 209, 490), ("Calidad", 490, 676), ("Otros", 676, 861),
    ("Impresion", 861, 1047), ("Administrativo", 1047, 1232), ("Laboratorio", 1232, 1418),
]
TITLES = {"Cliente": "Cliente", "Signatario": "Signatario", "Calidad": "Calidad", "Otros": "Otros Signatarios",
          "Impresion": "Impresión", "Administrativo": "Administrativo", "Laboratorio": "Laboratorio"}

# id, lane, x1, y1, x2, y2, text
NODES = [
    ("Captura", "Administrativo", 1081, 59, 1173, 127, "Captura"),
    ("Muestreo", "Signatario", 255, 96, 347, 165, "Muestreo"),
    ("Espera", "Signatario", 255, 325, 347, 394, "Espera Resultados Laboratorio"),
    ("GenInforme", "Signatario", 305, 502, 397, 571, "Generación de Informe"),
    ("RevCruzada", "Otros", 710, 464, 802, 533, "Rev. Cruzada"),
    ("CtrlCalidad", "Calidad", 535, 594, 627, 663, "Control de Calidad del Informe (Ignacio) (PDF)"),
    ("SigPDF", "Signatario", 255, 699, 347, 768, "Signatario genera PDF"),
    ("Entrega", "Impresion", 907, 757, 999, 826, "Entrega Electrónica ( antes VoBo Cliente )"),
    ("Impresion", "Impresion", 907, 861, 999, 930, "Impresión de Informe"),
    ("Entregado", "Administrativo", 1069, 861, 1161, 930, "Informe Entregado al Cliente"),
    ("Cerrada", "Administrativo", 1069, 977, 1161, 1046, "Cerrada"),
]

# id, lane, x1, y1, x2, y2, text, fill
NOTES = [
    ("N1", "Cliente", 72, 96, 211, 153, "Fecha Fin Muestreo<br>Inicio de los 10 dias<br>Muestreo Ini x Area<br>Planeación", "#FFFF99"),
    ("N2", "Signatario", 409, 166, 547, 223, "Fecha del Expediente B son necesarios para pasar a esta fase", "#FFFF99"),
    ("N3", "Signatario", 362, 325, 501, 382, "Permitir que Erika pueda capturar esta fecha", "#FFFF99"),
    ("N4", "Otros", 687, 325, 779, 417, "Control de calidad revisa editables", "#FFFF99"),
    ("N5", "Administrativo", 1186, 861, 1278, 953, "Estas fases son manejadas desde la prefactura", "#FFD966"),
]

# src, tgt, label, waypoints, extra style
EDGES = [
    ("Captura", "Muestreo", "", [(512, 128)], "exitX=0;exitY=0.5;entryX=1;entryY=0.5;"),
    ("Muestreo", "Espera", "", [], ""),
    ("Muestreo", "GenInforme", "Agentes físicos", [(155, 330)], "exitX=0;exitY=0.5;entryX=0;entryY=0.5;"),
    ("Espera", "GenInforme", "", [], ""),
    ("GenInforme", "RevCruzada", "", [(560, 520)], "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
    ("RevCruzada", "CtrlCalidad", "", [(680, 625)], "exitX=0;exitY=0.5;entryX=1;entryY=0.5;startArrow=block;startFill=1;"),
    ("CtrlCalidad", "SigPDF", "", [(300, 628)], "exitX=0;exitY=0.5;entryX=0.5;entryY=0;"),
    ("SigPDF", "Entrega", "", [(800, 645)], "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"),
    ("Entrega", "GenInforme", "", [(480, 770)], "exitX=0;exitY=0.5;entryX=0.5;entryY=1;"),
    ("Entrega", "Impresion", "ok", [], ""),
    ("Impresion", "Entregado", "", [], "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
    ("Entregado", "Cerrada", "", [], ""),
]


def build():
    ox = {n: (x1, TOP) for n, x1, _ in LANES}
    cells = []
    for n, x1, x2 in LANES:
        cells.append(f'<mxCell id="lane_{n}" value={quoteattr(TITLES[n])} style="swimlane;startSize={HEAD};fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontStyle=0;fontSize=11;collapsible=0;" vertex="1" parent="1"><mxGeometry x="{x1}" y="{TOP}" width="{x2 - x1}" height="{BOTTOM - TOP}" as="geometry"/></mxCell>')
    for nid, lane, x1, y1, x2, y2, text in NODES:
        px, py = ox[lane]
        cells.append(f'<mxCell id="{nid}" value={quoteattr(text)} style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fontSize=10;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="lane_{lane}"><mxGeometry x="{x1 - px}" y="{y1 - py}" width="{x2 - x1}" height="{y2 - y1}" as="geometry"/></mxCell>')
    for nid, lane, x1, y1, x2, y2, text, fill in NOTES:
        px, py = ox[lane]
        cells.append(f'<mxCell id="{nid}" value={quoteattr(text)} style="shape=note;size=12;whiteSpace=wrap;html=1;fontSize=10;strokeColor=#000000;fillColor={fill};" vertex="1" parent="lane_{lane}"><mxGeometry x="{x1 - px}" y="{y1 - py}" width="{x2 - x1}" height="{y2 - y1}" as="geometry"/></mxCell>')
    for i, (src, tgt, label, pts, extra) in enumerate(EDGES, 1):
        points = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts)
        arr = f'<Array as="points">{points}</Array>' if pts else ""
        cells.append(f'<mxCell id="e{i}" value={quoteattr(label)} style="curved=1;html=1;endArrow=block;endFill=1;strokeColor=#000000;fontSize=10;labelBackgroundColor=#FFFFFF;{extra}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')
    return ('<mxfile host="app.diagrams.net"><diagram id="ciclo-ot-v1" name="Ciclo vida OT - lanes v1 - 2016">'
            '<mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="1120" math="0" shadow="0">'
            '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print("draw.io file generated at", OUT)
