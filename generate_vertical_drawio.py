import os
from xml.sax.saxutils import quoteattr

from generate_drawio import BASE, D, EDGES, LANES, NODES, read_titles

OUT = os.path.join(BASE, "vertical-diagram.drawio")

SX, SY = 1.8, 0.55
LANE_Y, LANE_H, HEAD, SUBHEAD = 90, 2800, 60, 40


def px(y):
    return round(30 + (y - 120) * SX)


def py(x):
    return round(200 + (x - 580) * SY)


def transpose_style(extra):
    kv = dict(p.split("=") for p in extra.split(";") if p)
    out = {}
    for side in ("exit", "entry"):
        if side + "X" in kv:
            out[side + "X"], out[side + "Y"] = kv[side + "Y"], kv[side + "X"]
    return "".join(f"{k}={v};" for k, v in out.items())


def build():
    title, subtitle = read_titles()
    cells = []
    add = cells.append
    txt = "text;html=1;align=left;verticalAlign=middle;"
    add(f'<mxCell id="title" value={quoteattr(title)} style="{txt}fontSize=26;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="30" y="5" width="1600" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="subtitle" value={quoteattr(subtitle)} style="{txt}fontSize=14;fontColor=#64748B;" vertex="1" parent="1"><mxGeometry x="30" y="45" width="1600" height="30" as="geometry"/></mxCell>')

    origin = {}
    for lid, ltitle, ly, lh, head, body, subs in LANES:
        lx, lw = px(ly), round(lh * SX)
        add(f'<mxCell id="{lid}" value={quoteattr(ltitle)} style="swimlane;whiteSpace=wrap;html=1;startSize={HEAD};fillColor={head};swimlaneFillColor={body};strokeColor=#CBD5E1;fontColor=#FFFFFF;fontStyle=1;fontSize=14;collapsible=0;" vertex="1" parent="1"><mxGeometry x="{lx}" y="{LANE_Y}" width="{lw}" height="{LANE_H}" as="geometry"/></mxCell>')
        origin[lid] = (lx, LANE_Y)
        for sid, stitle, sy, sh, sbody in subs:
            sx = px(sy) - lx
            add(f'<mxCell id="{sid}" value={quoteattr(stitle)} style="swimlane;whiteSpace=wrap;html=1;startSize={SUBHEAD};fillColor=#E2E8F0;swimlaneFillColor={sbody};strokeColor=#CBD5E1;fontColor=#1E293B;fontStyle=1;fontSize=13;collapsible=0;" vertex="1" parent="{lid}"><mxGeometry x="{sx}" y="{HEAD}" width="{round(sh * SX)}" height="{LANE_H - HEAD}" as="geometry"/></mxCell>')
            origin[sid] = (lx + sx, LANE_Y + HEAD)

    for nid, (parent, cx, cy, w, h, text, sub, shape, fill, stroke) in NODES.items():
        ox, oy = origin[parent]
        value = f"<b>{text}</b>" + (f'<br><font style="font-size:10px;color:#475569">{sub}</font>' if sub else "")
        style = f"{shape};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize={11 if shape == D else 12};fontColor=#0F172A;shadow=1;"
        add(f'<mxCell id="{nid}" value={quoteattr(value)} style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{px(cy) - w // 2 - ox}" y="{py(cx) - h // 2 - oy}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    for i, (src, tgt, label, color, dashed, pts, extra) in enumerate(EDGES, 1):
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={color};strokeWidth=2;endArrow=block;endFill=1;fontSize=11;fontStyle=1;fontColor={color if label[:2] in ('Si', 'No') else '#334155'};labelBackgroundColor=#FFFFFF;{'dashed=1;' if dashed else ''}{transpose_style(extra)}"
        points = "".join(f'<mxPoint x="{px(y)}" y="{py(x)}"/>' for x, y in pts)
        arr = f'<Array as="points">{points}</Array>' if pts else ""
        add(f'<mxCell id="e{i}" value={quoteattr(label)} style="{style}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')

    return (f'<mxfile host="app.diagrams.net"><diagram id="ot-laned-vertical" name={quoteattr(title)}>'
            f'<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="3200" pageHeight="3000" math="0" shadow="0">'
            f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print("draw.io file generated at", OUT)
