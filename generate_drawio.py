import os
from xml.sax.saxutils import quoteattr

BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(BASE, "OT-Laned-v2.md")
OUT = os.path.join(BASE, "diagram.drawio")

W, H = 5500, 1800
LX, LW = 30, 5400

AMBER, BLUE, TEAL, GREEN, RED, PURPLE, DBLUE = "#D97706", "#2563EB", "#0D9488", "#16A34A", "#DC2626", "#7C3AED", "#1D4ED8"

# id, title, y, h, header color, body color, sublanes [(id, title, y, h, body)]
LANES = [
    ("Cliente", "Cliente", 120, 120, "#D97706", "#FFFBEB", []),
    ("AtnCte", "Atención Clientes", 240, 130, "#2563EB", "#F8FAFC", []),
    ("OpeHig", "Operativo Higiene", 370, 260, "#0D9488", "#F0FDFA",
     [("TecHig", "Técnico", 370, 130, "#F0FDFA"), ("CorHig", "Coordinador Higiene", 500, 130, "#CCFBF1")]),
    ("LabHigMX", "Laboratorio Higiene MX", 630, 120, "#059669", "#F0FDF4", []),
    ("CaptHigMX", "Revisión y Captura Higiene MX", 750, 130, "#7C3AED", "#FAF5FF", []),
    ("OpeEco", "Operativo Ecología", 880, 260, "#16A34A", "#F0FDF4",
     [("TecEco", "Técnico", 880, 130, "#F0FDF4"), ("CorEco", "Coordinador Ecología", 1010, 130, "#DCFCE7")]),
    ("LabEcoMX", "Laboratorio Ecología MX", 1140, 120, "#10B981", "#ECFDF5", []),
    ("CaptEcoMX", "Revisión y Captura Ecología MX", 1260, 130, "#9333EA", "#FAF5FF", []),
    ("CapLoc", "Captura e Impresión", 1390, 130, "#1D4ED8", "#EFF6FF", []),
    ("Cobranza", "Atención Clientes - Cobranza", 1520, 120, "#E11D48", "#FFF1F2", []),
    ("Logistica", "Atención Clientes - Logística", 1640, 120, "#64748B", "#F1F5F9", []),
]

# id: (lane/sublane, cx, cy, w, h, text, sub, shape, fill, stroke)
R, D = "rounded=1", "rhombus"
NODES = {
    "CteAutCot": ("Cliente", 580, 180, 160, 58, "Compras", "Autoriza Cotización", R, "#FEF3C7", "#D97706"),
    "GenOT": ("AtnCte", 830, 305, 160, 72, "Generar OT", "<i>Folio OT</i><br><i>Fecha Planif Muestreo</i>", R, "#DBEAFE", "#2563EB"),
    "HigEcolEval": ("AtnCte", 1100, 305, 180, 78, "¿Higiene o Ecología?", "", D, "#EFF6FF", "#2563EB"),
    "TecHigMues": ("TecHig", 1380, 435, 160, 58, "Muestrea", "<i>Fecha Muestreo</i>", R, "#CCFBF1", "#0D9488"),
    "TecHigHojas": ("TecHig", 1660, 435, 160, 58, "Captura Hojas de Campo", "<i>Fecha Hojas Campo</i>", R, "#CCFBF1", "#0D9488"),
    "TecHigEnvMues": ("TecHig", 1960, 435, 160, 58, "Envía Muestra", "<i>Fecha Envío Muestra</i>", R, "#CCFBF1", "#0D9488"),
    "CordHigRevisa": ("CorHig", 1960, 565, 170, 58, "Revisa Hojas de Campo", "<i>Fecha Revisión Hojas</i>", R, "#99F6E4", "#0F766E"),
    "CordHigEvalHojas": ("CorHig", 2270, 565, 150, 72, "¿Correcciones?", "", D, "#FEF08A", "#CA8A04"),
    "CordHigEvalMX": ("CorHig", 2580, 565, 150, 72, "¿Revisa MX?", "", D, "#FEF08A", "#CA8A04"),
    "LabHigMXRecMue": ("LabHigMX", 2270, 690, 160, 58, "Recibe Muestras", "Lab Higiene MX", R, "#DCFCE7", "#059669"),
    "LabHigMXAnaliza": ("LabHigMX", 2580, 690, 160, 58, "Analiza Muestras", "Lab Higiene MX", R, "#DCFCE7", "#059669"),
    "LabHigMXReporta": ("LabHigMX", 2890, 690, 160, 58, "Reporta Resultados", "Emisión Ensayos", R, "#DCFCE7", "#059669"),
    "CapHigMxRevisa": ("CaptHigMX", 3200, 815, 160, 58, "Revisa", "Revisión Higiene MX", R, "#EDE9FE", "#7C3AED"),
    "CapHigMxEval": ("CaptHigMX", 3490, 815, 150, 72, "¿Correcciones?", "", D, "#FEF08A", "#CA8A04"),
    "CapHigMxGenInfPDF": ("CaptHigMX", 3780, 815, 170, 58, "Genera Informe PDF", "Informe Higiene", R, "#DDD6FE", "#6D28D9"),
    "TecEcoMues": ("TecEco", 1380, 945, 160, 58, "Muestrea", "<i>Fecha Muestreo</i>", R, "#DCFCE7", "#16A34A"),
    "TecEcoHojas": ("TecEco", 1660, 945, 160, 58, "Captura Hojas de Campo", "<i>Fecha Hojas Campo</i>", R, "#DCFCE7", "#16A34A"),
    "TecEcoEnvMues": ("TecEco", 1960, 945, 160, 58, "Envia Muestra", "<i>Fecha Envio Muestra</i>", R, "#DCFCE7", "#16A34A"),
    "CordEcoRevisa": ("CorEco", 1960, 1075, 170, 58, "Revisa Hojas de Campo", "<i>Fecha Revisión Hojas</i>", R, "#BBF7D0", "#15803D"),
    "CordEcoEvalHojas": ("CorEco", 2270, 1075, 150, 72, "¿Correcciones?", "", D, "#FEF08A", "#CA8A04"),
    "LabEcoMXRecMue": ("LabEcoMX", 2270, 1200, 160, 58, "Recibe Muestras", "Lab Ecología MX", R, "#D1FAE5", "#10B981"),
    "LabEcoMXAnaliza": ("LabEcoMX", 2580, 1200, 160, 58, "Analiza Muestras", "Lab Ecología MX", R, "#D1FAE5", "#10B981"),
    "LabEcoMXReporta": ("LabEcoMX", 2890, 1200, 160, 58, "Reporta Resultados", "Emisión Ensayos", R, "#D1FAE5", "#10B981"),
    "CapEcoMxRevisa": ("CaptEcoMX", 3200, 1325, 160, 58, "Revisa", "Revisión Ecología MX", R, "#F3E8FF", "#9333EA"),
    "CapEcoMxEval": ("CaptEcoMX", 3490, 1325, 150, 72, "¿Correcciones?", "", D, "#FEF08A", "#CA8A04"),
    "CapEcoMxGenInfPDF": ("CaptEcoMX", 3780, 1325, 170, 58, "Genera Informe PDF", "Informe Ecología", R, "#E9D5FF", "#7E22CE"),
    "CapLocCaptura": ("CapLoc", 4040, 1455, 140, 58, "Captura", "Captura Local", R, "#DBEAFE", "#1D4ED8"),
    "CapLocGenPDF": ("CapLoc", 4260, 1455, 140, 58, "Genera PDF", "PDF Local", R, "#BFDBFE", "#1D4ED8"),
    "CapLocGenImp": ("CapLoc", 4480, 1455, 140, 58, "Impresión", "Impresión Final", R, "#93C5FD", "#1E40AF"),
    "CobrCFDI": ("Cobranza", 4140, 1580, 140, 58, "Genera CFDI", "", R, "#FFE4E6", "#E11D48"),
    "CobrEnvioPDF": ("Cobranza", 4480, 1580, 170, 58, "Envia PDF/CFDI a Usuario", "", R, "#FFE4E6", "#E11D48"),
    "LogAcopio": ("Logistica", 4760, 1700, 180, 58, "Acopio del Informe Impreso", "", R, "#E2E8F0", "#475569"),
    "LogEntrega": ("Logistica", 5040, 1700, 180, 58, "Entrega del Informe Impreso", "", R, "#E2E8F0", "#475569"),
    "LogEntregado": ("Logistica", 5320, 1700, 180, 58, "Informe Impreso Entregado", "", R, "#DCFCE7", "#16A34A"),
}

TOP, BOT = "exitX=0.5;exitY=0;", "exitX=0.5;exitY=1;"

# src, tgt, label, color, dashed, waypoints (absolute), extra style
EDGES = [
    ("CteAutCot", "GenOT", "Autoriza Cotización", AMBER, 0, [(730, 180), (730, 305)], ""),
    ("GenOT", "HigEcolEval", "", BLUE, 0, [], ""),
    ("HigEcolEval", "TecHigMues", "Higiene", TEAL, 0, [(1100, 435)], BOT),
    ("TecHigMues", "TecHigHojas", "", TEAL, 0, [], ""),
    ("TecHigHojas", "TecHigEnvMues", "", TEAL, 0, [], ""),
    ("TecHigEnvMues", "LabHigMXRecMue", "", GREEN, 0, [(2120, 435), (2120, 690)], ""),
    ("LabHigMXRecMue", "LabHigMXAnaliza", "", GREEN, 0, [], ""),
    ("LabHigMXAnaliza", "LabHigMXReporta", "", GREEN, 0, [], ""),
    ("TecHigHojas", "CordHigRevisa", "Hojas de Campo", TEAL, 0, [(1660, 565)], BOT),
    ("CordHigRevisa", "CordHigEvalHojas", "", TEAL, 0, [], ""),
    ("CordHigEvalHojas", "TecHigHojas", "Si<br><i>Fecha Revision HdC</i><br><i>Marca Retrabajo</i>", GREEN, 0, [(2270, 490), (1700, 490)], TOP + "entryX=0.75;entryY=1;"),
    ("CordHigEvalHojas", "CordHigEvalMX", "No<br><i>Fecha Revisión HdC</i>", RED, 0, [], ""),
    ("CordHigEvalMX", "CapHigMxRevisa", "Si<br><i>Fecha Sol. Rev MX</i>", GREEN, 0, [(2735, 565), (2735, 775), (3100, 775), (3100, 815)], ""),
    ("LabHigMXReporta", "CapHigMxRevisa", "", PURPLE, 0, [(3050, 690), (3050, 825)], ""),
    ("LabHigMXReporta", "CapLocGenPDF", "<i>Fecha Lab.MX Libera Resultados</i>", BLUE, 1, [(2890, 750), (4230, 750), (4230, 1380)], BOT + "entryX=0.25;entryY=0;"),
    ("CapHigMxRevisa", "CapHigMxEval", "", PURPLE, 0, [], ""),
    ("CapHigMxEval", "CordHigRevisa", "Si<br><i>Fecha Revisión MX</i><br><i>Marca Retrabajo MX</i>", GREEN, 0, [(3490, 515), (1960, 515)], TOP + "entryX=0.5;entryY=0;"),
    ("CapHigMxEval", "CapHigMxGenInfPDF", "No<br><i>Fecha Revisión MX</i>", RED, 0, [], ""),
    ("CapHigMxGenInfPDF", "CapLocGenPDF", "<i>Fecha MX Libera Informe PDF</i><br><i>Aviso a Facturación CFDI</i>", DBLUE, 0, [(3960, 815), (3960, 1395), (4260, 1395)], "entryX=0.5;entryY=0;"),
    ("HigEcolEval", "TecEcoMues", "Ecología", GREEN, 0, [(1000, 305), (1000, 945)], "exitX=0;exitY=0.5;"),
    ("TecEcoMues", "TecEcoHojas", "", GREEN, 0, [], ""),
    ("TecEcoHojas", "TecEcoEnvMues", "", GREEN, 0, [], ""),
    ("TecEcoEnvMues", "LabEcoMXRecMue", "", GREEN, 0, [(2120, 945), (2120, 1200)], ""),
    ("LabEcoMXRecMue", "LabEcoMXAnaliza", "", GREEN, 0, [], ""),
    ("LabEcoMXAnaliza", "LabEcoMXReporta", "", GREEN, 0, [], ""),
    ("TecEcoHojas", "CordEcoRevisa", "Hojas de Campo", GREEN, 0, [(1660, 1075)], BOT),
    ("CordEcoRevisa", "CordEcoEvalHojas", "", GREEN, 0, [], ""),
    ("CordEcoEvalHojas", "TecEcoHojas", "Si<br><i>Fecha Revision HdC</i><br><i>Marca Retrabajo</i>", GREEN, 0, [(2270, 1000), (1700, 1000)], TOP + "entryX=0.75;entryY=1;"),
    ("CordEcoEvalHojas", "CapEcoMxRevisa", "No<br><i>Fecha Revisión HdC</i>", RED, 0, [(2425, 1075), (2425, 1285), (3100, 1285), (3100, 1325)], ""),
    ("LabEcoMXReporta", "CapEcoMxRevisa", "<i>Fecha Lab.MX Libera Resultados</i>", PURPLE, 0, [(3050, 1200), (3050, 1335)], ""),
    ("LabEcoMXReporta", "CapLocGenPDF", "", BLUE, 1, [(2890, 1260), (4260, 1260)], BOT + "entryX=0.75;entryY=0;"),
    ("CapEcoMxRevisa", "CapEcoMxEval", "", PURPLE, 0, [], ""),
    ("CapEcoMxEval", "CordEcoRevisa", "Si<br><i>Fecha Revisión MX</i><br><i>Marca Retrabajo MX</i>", GREEN, 0, [(3490, 1025), (1960, 1025)], TOP + "entryX=0.5;entryY=0;"),
    ("CapEcoMxEval", "CapEcoMxGenInfPDF", "No<br><i>Fecha Revisión MX</i>", RED, 0, [], ""),
    ("CapEcoMxGenInfPDF", "CapLocGenPDF", "<i>Fecha MX Libera Informe PDF</i><br><i>Aviso a Facturación CFDI</i>", DBLUE, 0, [(3990, 1325), (3990, 1410), (4260, 1410)], "entryX=0.5;entryY=0;"),
    ("CapLocCaptura", "CapLocGenPDF", "<i>Fecha Genera PDF</i><br><i>Aviso a Facturación CFDI</i>", DBLUE, 0, [], ""),
    ("CapLocGenPDF", "CapLocGenImp", "<i>Fecha PDF Listo para Impresión</i><br><i>Aviso a Cobranza</i>", DBLUE, 0, [], ""),
    ("CapLocGenPDF", "CobrEnvioPDF", "<i>Aviso a Cobranza</i>", RED, 1, [(4260, 1500), (4480, 1500)], BOT + "entryX=0.5;entryY=0;"),
    ("CapHigMxGenInfPDF", "CobrCFDI", "<i>Aviso a Facturación CFDI</i>", RED, 1, [(4140, 815)], "entryX=0.5;entryY=0;"),
    ("CapEcoMxGenInfPDF", "CobrCFDI", "<i>Aviso a Facturación CFDI</i>", RED, 1, [(4140, 1325)], "entryX=0.5;entryY=0;"),
    ("CobrCFDI", "CobrEnvioPDF", "", RED, 0, [], ""),
    ("CapLocGenImp", "LogAcopio", "<i>Fecha Infomre Impreso Listo</i>", "#475569", 0, [(4630, 1455), (4630, 1700)], ""),
    ("LogAcopio", "LogEntrega", "<i>Fecha Envío Infomre Impreso</i>", "#475569", 0, [], ""),
    ("LogEntrega", "LogEntregado", "<i>Fecha Acuse de Recibo</i><br><i>Evidencia Informe Recibido</i><br><i>OT Finalizada</i>", GREEN, 0, [], ""),
    ("CordHigEvalMX", "CapLocCaptura", "No<br><i>Fecha Captura Local</i><br><i>Aviso a Captura Local</i>", RED, 0, [(2580, 495), (3925, 495), (3925, 1455)], TOP),
]


def read_titles():
    with open(MD, encoding="utf-8") as f:
        lines = [l.strip() for l in f]
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "Swimlane")
    sub = next((l.lstrip("#").strip() for l in lines[lines.index("# " + title) + 1:] if l), "")
    return title, "" if sub.startswith("```") else sub


def build():
    title, subtitle = read_titles()
    cells = []
    add = cells.append
    txt = "text;html=1;align=left;verticalAlign=middle;"

    add(f'<mxCell id="title" value={quoteattr(title)} style="{txt}fontSize=26;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="30" y="5" width="2400" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="subtitle" value={quoteattr(subtitle)} style="{txt}fontSize=14;fontColor=#64748B;" vertex="1" parent="1"><mxGeometry x="30" y="45" width="2400" height="30" as="geometry"/></mxCell>')

    origin = {}
    for lid, ltitle, ly, lh, head, body, subs in LANES:
        hdr = 210 if subs else 390
        add(f'<mxCell id="{lid}" value={quoteattr(ltitle)} style="swimlane;horizontal=0;whiteSpace=wrap;html=1;startSize={hdr};fillColor={head};swimlaneFillColor={body};strokeColor=#CBD5E1;fontColor=#FFFFFF;fontStyle=1;fontSize=15;collapsible=0;" vertex="1" parent="1"><mxGeometry x="{LX}" y="{ly}" width="{LW}" height="{lh}" as="geometry"/></mxCell>')
        origin[lid] = (LX, ly)
        for sid, stitle, sy, sh, sbody in subs:
            add(f'<mxCell id="{sid}" value={quoteattr(stitle)} style="swimlane;horizontal=0;whiteSpace=wrap;html=1;startSize=180;fillColor=#E2E8F0;swimlaneFillColor={sbody};strokeColor=#CBD5E1;fontColor=#1E293B;fontStyle=1;fontSize=13;collapsible=0;" vertex="1" parent="{lid}"><mxGeometry x="{hdr}" y="{sy - ly}" width="{LW - hdr}" height="{sh}" as="geometry"/></mxCell>')
            origin[sid] = (LX + hdr, sy)

    for nid, (parent, cx, cy, w, h, text, sub, shape, fill, stroke) in NODES.items():
        ox, oy = origin[parent]
        value = f"<b>{text}</b>" + (f'<br><font style="font-size:10px;color:#475569">{sub}</font>' if sub else "")
        style = f"{shape};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize={11 if shape == D else 12};fontColor=#0F172A;shadow=1;"
        add(f'<mxCell id="{nid}" value={quoteattr(value)} style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{cx - w // 2 - ox}" y="{cy - h // 2 - oy}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    for i, (src, tgt, label, color, dashed, pts, extra) in enumerate(EDGES, 1):
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={color};strokeWidth=2;endArrow=block;endFill=1;fontSize=11;fontStyle=1;fontColor={color if label[:2] in ('Si', 'No') else '#334155'};labelBackgroundColor=#FFFFFF;{'dashed=1;' if dashed else ''}{extra}"
        points = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts)
        arr = f'<Array as="points">{points}</Array>' if pts else ""
        add(f'<mxCell id="e{i}" value={quoteattr(label)} style="{style}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')

    return (f'<mxfile host="app.diagrams.net"><diagram id="ot-laned" name={quoteattr(title)}>'
            f'<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
            f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print("draw.io file generated at", OUT)
