import os
import subprocess

def generate_svg():
    with open("/Users/carlos.sanchez/no-sync-git/pre-diag/OT-Laned-v2.md", encoding="utf-8") as f:
        lines = [l.strip() for l in f]
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "Swimlane")
    after = lines[lines.index("# " + title) + 1:] if "# " + title in lines else []
    subtitle = next((l.lstrip("#").strip() for l in after if l), "")
    if subtitle.startswith("```"):
        subtitle = ""
    width = 4680
    height = 1720
    header_height = 80
    phases_height = 40
    
    # 10 Outer Subgraphs as Lanes:
    lanes = [
        {
            "id": "Cliente",
            "title": "Cliente",
            "code": "Cliente",
            "y": 120,
            "h": 120,
            "bg": "#FFFBEB",
            "header_bg": "#D97706",
            "sublanes": []
        },
        {
            "id": "AtnCte",
            "title": "Atención a Clientes",
            "code": "AtencionClientes",
            "y": 240,
            "h": 130,
            "bg": "#F8FAFC",
            "header_bg": "#2563EB",
            "sublanes": []
        },
        {
            "id": "OpeHig",
            "title": "Operativo Higiene",
            "code": "OpeHig",
            "y": 370,
            "h": 260,
            "bg": "#F0FDFA",
            "header_bg": "#0D9488",
            "sublanes": [
                {"title": "Técnico", "code": "TecHig", "y": 370, "h": 130, "bg": "#F0FDFA"},
                {"title": "Coordinador Higiene", "code": "CorHig", "y": 500, "h": 130, "bg": "#CCFBF1"}
            ]
        },
        {
            "id": "LabHigMX",
            "title": "Laboratorio Higiene MX",
            "code": "LabHigMX",
            "y": 630,
            "h": 120,
            "bg": "#F0FDF4",
            "header_bg": "#059669",
            "sublanes": []
        },
        {
            "id": "CaptHigMX",
            "title": "Revisión y Captura Higiene MX",
            "code": "CaptHigMX",
            "y": 750,
            "h": 130,
            "bg": "#FAF5FF",
            "header_bg": "#7C3AED",
            "sublanes": []
        },
        {
            "id": "OpeEco",
            "title": "Operativo Ecología",
            "code": "OpeEco",
            "y": 880,
            "h": 260,
            "bg": "#F0FDF4",
            "header_bg": "#16A34A",
            "sublanes": [
                {"title": "Técnico", "code": "TecEco", "y": 880, "h": 130, "bg": "#F0FDF4"},
                {"title": "Coordinador Ecología", "code": "CorEco", "y": 1010, "h": 130, "bg": "#DCFCE7"}
            ]
        },
        {
            "id": "LabEcoMX",
            "title": "Laboratorio Ecología MX",
            "code": "LabEcoMX",
            "y": 1140,
            "h": 120,
            "bg": "#ECFDF5",
            "header_bg": "#10B981",
            "sublanes": []
        },
        {
            "id": "CaptEcoMX",
            "title": "Revisión y Captura Ecología MX",
            "code": "CaptEcoMX",
            "y": 1260,
            "h": 130,
            "bg": "#FAF5FF",
            "header_bg": "#9333EA",
            "sublanes": []
        },
        {
            "id": "CapLoc",
            "title": "Captura e Impresión",
            "code": "CapLoc",
            "y": 1390,
            "h": 130,
            "bg": "#EFF6FF",
            "header_bg": "#1D4ED8",
            "sublanes": []
        },
        {
            "id": "Cobranza",
            "title": "Atn Ctes - Cobranza",
            "code": "Cobranza",
            "y": 1520,
            "h": 120,
            "bg": "#FFF1F2",
            "header_bg": "#E11D48",
            "sublanes": []
        }
    ]

    # Process Phases / Column Milestones
    phases = [
        {"x": 420, "w": 490, "title": "FASE 1: AUTORIZACIÓN Y APERTURA DE OT", "color": "#2563EB"},
        {"x": 910, "w": 380, "title": "FASE 2: EVALUACIÓN DE DISCIPLINA", "color": "#0284C7"},
        {"x": 1290, "w": 530, "title": "FASE 3: MUESTREO EN CAMPO", "color": "#0D9488"},
        {"x": 1820, "w": 330, "title": "FASE 4: ENVÍO Y REVISIÓN INTERNA", "color": "#16A34A"},
        {"x": 2150, "w": 850, "title": "FASE 5: LABORATORIO CENTRAL MX", "color": "#059669"},
        {"x": 3000, "w": 960, "title": "FASE 6: REVISIÓN DE RESULTADOS Y GENERACIÓN PDF", "color": "#7C3AED"},
        {"x": 3960, "w": 660, "title": "FASE 7: CAPTURA LOCAL, IMPRESIÓN Y CIERRE", "color": "#1D4ED8"},
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append("""
    <defs>
      <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#0F172A" />
        <stop offset="50%" stop-color="#1E293B" />
        <stop offset="100%" stop-color="#334155" />
      </linearGradient>

      <linearGradient id="phaseGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#F1F5F9" />
        <stop offset="100%" stop-color="#E2E8F0" />
      </linearGradient>
      
      <filter id="shadow" x="-8%" y="-15%" width="120%" height="140%">
        <feDropShadow dx="1" dy="3" stdDeviation="3" flood-opacity="0.12" />
      </filter>

      <filter id="nodeShadow" x="-10%" y="-20%" width="125%" height="150%">
        <feDropShadow dx="1" dy="2" stdDeviation="2.5" flood-opacity="0.08" />
      </filter>

      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#334155" />
      </marker>
      
      <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#16A34A" />
      </marker>
      
      <marker id="arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0D9488" />
      </marker>

      <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#D97706" />
      </marker>

      <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2563EB" />
      </marker>

      <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#DC2626" />
      </marker>

      <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#7C3AED" />
      </marker>
    </defs>
    
    <style>
      text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
      .title { font-size: 24px; font-weight: 800; fill: #FFFFFF; letter-spacing: 0.5px; }
      .subtitle { font-size: 14px; font-weight: 400; fill: #94A3B8; }
      .lane-title { font-size: 15px; font-weight: 700; fill: #FFFFFF; }
      .lane-sub { font-size: 11px; font-weight: 500; fill: rgba(255,255,255,0.85); }
      .sublane-title { font-size: 13px; font-weight: 700; fill: #1E293B; }
      .sublane-sub { font-size: 10px; font-weight: 500; fill: #64748B; }
      .phase-text { font-size: 11px; font-weight: 700; fill: #475569; letter-spacing: 0.5px; text-anchor: middle; }
      .node-text { font-size: 14px; font-weight: 700; fill: #0F172A; text-anchor: middle; }
      .node-subtext { font-size: 11px; font-weight: 500; fill: #475569; text-anchor: middle; }
      .decision-text { font-size: 13px; font-weight: 800; fill: #0F172A; text-anchor: middle; }
      .edge-label { font-size: 11px; font-weight: 600; fill: #334155; text-anchor: middle; }
      .edge-label-yes { font-size: 12px; font-weight: 800; fill: #16A34A; text-anchor: middle; }
      .edge-label-no { font-size: 12px; font-weight: 800; fill: #DC2626; text-anchor: middle; }
    </style>
    """)

    # Background
    svg.append(f'<rect width="{width}" height="{height}" fill="#F8FAFC" />')

    # Top Header
    svg.append(f'<rect x="0" y="0" width="{width}" height="{header_height}" fill="url(#headerGrad)" />')
    svg.append(f'<text x="40" y="38" class="title">{title}</text>')
    svg.append(f'<text x="40" y="62" class="subtitle">{subtitle}</text>')

    # Phases Bar (Y: 80 to 120)
    svg.append(f'<rect x="30" y="80" width="{width-60}" height="{phases_height}" fill="url(#phaseGrad)" stroke="#CBD5E1" stroke-width="1.2" />')
    svg.append(f'<rect x="30" y="80" width="390" height="{phases_height}" fill="#334155" />')
    svg.append(f'<text x="225" y="105" style="font-size:12px;font-weight:700;fill:#FFFFFF;letter-spacing:1px;text-anchor:middle">CARRILES / ROLES (SUBGRAPHS)</text>')
    
    for ph in phases:
        px = ph["x"]
        pw = ph["w"]
        svg.append(f'<line x1="{px}" y1="80" x2="{px}" y2="{height - 60}" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="3,3" />')
        svg.append(f'<text x="{px + pw/2}" y="105" class="phase-text">{ph["title"]}</text>')

    # Draw Lanes
    for lane in lanes:
        ly = lane["y"]
        lh = lane["h"]
        
        # Lane container background
        svg.append(f'<rect x="30" y="{ly}" width="{width-60}" height="{lh}" fill="{lane["bg"]}" stroke="#CBD5E1" stroke-width="1.2" />')
        
        # If has sublanes
        if lane["sublanes"]:
            # Main Header for lane (210px wide)
            svg.append(f'<rect x="30" y="{ly}" width="210" height="{lh}" fill="{lane["header_bg"]}" />')
            svg.append(f'<text x="135" y="{ly + lh/2 - 6}" class="lane-title" text-anchor="middle">{lane["title"]}</text>')
            svg.append(f'<text x="135" y="{ly + lh/2 + 14}" class="lane-sub" text-anchor="middle">[{lane["code"]}]</text>')
            
            # Sublanes
            for sub in lane["sublanes"]:
                sy = sub["y"]
                sh = sub["h"]
                svg.append(f'<rect x="240" y="{sy}" width="{width-270}" height="{sh}" fill="{sub["bg"]}" stroke="#CBD5E1" stroke-width="1" />')
                # Sublane header
                svg.append(f'<rect x="240" y="{sy}" width="180" height="{sh}" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="1" />')
                svg.append(f'<text x="330" y="{sy + sh/2 - 5}" class="sublane-title" text-anchor="middle">{sub["title"]}</text>')
                svg.append(f'<text x="330" y="{sy + sh/2 + 13}" class="sublane-sub" text-anchor="middle">[{sub["code"]}]</text>')
        else:
            # Full Lane Header (390px wide)
            svg.append(f'<rect x="30" y="{ly}" width="390" height="{lh}" fill="{lane["header_bg"]}" />')
            svg.append(f'<text x="225" y="{ly + lh/2 - 6}" class="lane-title" text-anchor="middle">{lane["title"]}</text>')
            code_str = lane.get("code", lane["id"])
            svg.append(f'<text x="225" y="{ly + lh/2 + 14}" class="lane-sub" text-anchor="middle">[{code_str}]</text>')

    # Nodes Dictionary
    nodes = {
        # Cliente
        "CteAutCot": {"x": 580, "y": 180, "w": 160, "h": 58, "text": "Compras", "sub": "Autoriza Cotización", "shape": "rect", "color": "#FEF3C7", "border": "#D97706"},
        
        # AtnCte
        "GenOT": {"x": 830, "y": 305, "w": 160, "h": 58, "text": "Generar OT", "sub": "Atención a Clientes", "shape": "rect", "color": "#DBEAFE", "border": "#2563EB"},
        "HigEcolEval": {"x": 1100, "y": 305, "w": 180, "h": 78, "text": "¿Higiene o Ecología?", "sub": "", "shape": "diamond", "color": "#EFF6FF", "border": "#2563EB"},
        
        # OpeHig -> Técnico
        "TecHigMues": {"x": 1380, "y": 435, "w": 160, "h": 58, "text": "Muestrea", "sub": "Técnico Higiene", "shape": "rect", "color": "#CCFBF1", "border": "#0D9488"},
        "TecHigHojas": {"x": 1660, "y": 435, "w": 160, "h": 58, "text": "Hojas de Campo", "sub": "Registro de Campo", "shape": "rect", "color": "#CCFBF1", "border": "#0D9488"},
        "TecHigEnvMues": {"x": 1960, "y": 435, "w": 160, "h": 58, "text": "Envia Muestra", "sub": "A Laboratorio MX", "shape": "rect", "color": "#CCFBF1", "border": "#0D9488"},
        
        # OpeHig -> Coordinador Higiene
        "CordHigRevisa": {"x": 1960, "y": 565, "w": 170, "h": 58, "text": "Revisa Hojas de Campo", "sub": "Coordinador Higiene", "shape": "rect", "color": "#99F6E4", "border": "#0F766E"},
        "CordHigEvalHojas": {"x": 2270, "y": 565, "w": 150, "h": 72, "text": "¿Correcciones?", "sub": "", "shape": "diamond", "color": "#FEF08A", "border": "#CA8A04"},
        "CordHigEvalMX": {"x": 2580, "y": 565, "w": 150, "h": 72, "text": "¿Revisa MX?", "sub": "", "shape": "diamond", "color": "#FEF08A", "border": "#CA8A04"},

        # LabHigMX
        "LabHigMXRecMue": {"x": 2270, "y": 690, "w": 160, "h": 58, "text": "Recibe Muestras", "sub": "Lab Higiene MX", "shape": "rect", "color": "#DCFCE7", "border": "#059669"},
        "LabHigMXAnaliza": {"x": 2580, "y": 690, "w": 160, "h": 58, "text": "Analiza Muestras", "sub": "Lab Higiene MX", "shape": "rect", "color": "#DCFCE7", "border": "#059669"},
        "LabHigMXReporta": {"x": 2890, "y": 690, "w": 160, "h": 58, "text": "Reporta Resultados", "sub": "Emisión Ensayos", "shape": "rect", "color": "#DCFCE7", "border": "#059669"},

        # CaptHigMX
        "CapHigMxRevisa": {"x": 3200, "y": 815, "w": 160, "h": 58, "text": "Revisa", "sub": "Revisión Higiene MX", "shape": "rect", "color": "#EDE9FE", "border": "#7C3AED"},
        "CapHigMxEval": {"x": 3490, "y": 815, "w": 150, "h": 72, "text": "¿Correcciones?", "sub": "", "shape": "diamond", "color": "#FEF08A", "border": "#CA8A04"},
        "CapHigMxGenInfPDF": {"x": 3780, "y": 815, "w": 170, "h": 58, "text": "Genera Informe PDF", "sub": "Informe Higiene", "shape": "rect", "color": "#DDD6FE", "border": "#6D28D9"},

        # OpeEco -> Técnico
        "TecEcoMues": {"x": 1380, "y": 945, "w": 160, "h": 58, "text": "Muestreas", "sub": "Técnico Ecología", "shape": "rect", "color": "#DCFCE7", "border": "#16A34A"},
        "TecEcoHojas": {"x": 1660, "y": 945, "w": 160, "h": 58, "text": "Hojas de Campo", "sub": "Registro de Campo", "shape": "rect", "color": "#DCFCE7", "border": "#16A34A"},
        "TecEcoEnvMues": {"x": 1960, "y": 945, "w": 160, "h": 58, "text": "Envia Muestra", "sub": "A Laboratorio MX", "shape": "rect", "color": "#DCFCE7", "border": "#16A34A"},

        # OpeEco -> Coordinador Ecología
        "CordEcoRevisa": {"x": 1960, "y": 1075, "w": 170, "h": 58, "text": "Revisa Hojas de Campo", "sub": "Coordinador Ecología", "shape": "rect", "color": "#BBF7D0", "border": "#15803D"},
        "CordEcoEvalHojas": {"x": 2270, "y": 1075, "w": 150, "h": 72, "text": "¿Correcciones?", "sub": "", "shape": "diamond", "color": "#FEF08A", "border": "#CA8A04"},

        # LabEcoMX
        "LabEcoMXRecMue": {"x": 2270, "y": 1200, "w": 160, "h": 58, "text": "Recibe Muestras", "sub": "Lab Ecología MX", "shape": "rect", "color": "#D1FAE5", "border": "#10B981"},
        "LabEcoMXAnaliza": {"x": 2580, "y": 1200, "w": 160, "h": 58, "text": "Analiza Muestras", "sub": "Lab Ecología MX", "shape": "rect", "color": "#D1FAE5", "border": "#10B981"},
        "LabEcoMXReporta": {"x": 2890, "y": 1200, "w": 160, "h": 58, "text": "Reporta Resultados", "sub": "Emisión Ensayos", "shape": "rect", "color": "#D1FAE5", "border": "#10B981"},

        # CaptEcoMX
        "CapEcoMxRevisa": {"x": 3200, "y": 1325, "w": 160, "h": 58, "text": "Revisa", "sub": "Revisión Ecología MX", "shape": "rect", "color": "#F3E8FF", "border": "#9333EA"},
        "CapEcoMxEval": {"x": 3490, "y": 1325, "w": 150, "h": 72, "text": "¿Correcciones?", "sub": "", "shape": "diamond", "color": "#FEF08A", "border": "#CA8A04"},
        "CapEcoMxGenInfPDF": {"x": 3780, "y": 1325, "w": 170, "h": 58, "text": "Genera Informe PDF", "sub": "Informe Ecología", "shape": "rect", "color": "#E9D5FF", "border": "#7E22CE"},

        # CapLoc
        "CapLocCaptura": {"x": 4040, "y": 1455, "w": 140, "h": 58, "text": "Captura", "sub": "Captura Local", "shape": "rect", "color": "#DBEAFE", "border": "#1D4ED8"},
        "CapLocGenPDF": {"x": 4260, "y": 1455, "w": 140, "h": 58, "text": "Genera PDF", "sub": "PDF Local", "shape": "rect", "color": "#BFDBFE", "border": "#1D4ED8"},
        "CapLocGenImp": {"x": 4480, "y": 1455, "w": 140, "h": 58, "text": "Impresión", "sub": "Impresión Final", "shape": "rect", "color": "#93C5FD", "border": "#1E40AF"},

        # Cobranza
        "CobranzaNode": {"x": 4480, "y": 1580, "w": 180, "h": 52, "text": "Cobranza y Facturación", "sub": "Atn Ctes - Cobranza", "shape": "rect", "color": "#FFE4E6", "border": "#E11D48"}
    }

    # Helpers for connector paths
    def draw_path(d, stroke="#475569", width=2.4, marker="arrow", dash=None):
        dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" marker-end="url(#{marker})" {dash_attr} stroke-linejoin="round" stroke-linecap="round" />'

    def draw_label(x, y, text, cls="edge-label", bg="#FFFFFF", border="#CBD5E1"):
        tw = len(text) * 8.5 + 16
        th = 22
        return f'''
        <g transform="translate({x},{y})">
          <rect x="{-tw/2}" y="{-th/2}" width="{tw}" height="{th}" rx="4" ry="4" fill="{bg}" stroke="{border}" stroke-width="1" filter="url(#nodeShadow)" />
          <text x="0" y="4" class="{cls}">{text}</text>
        </g>
        '''

    connectors = []

    # 1. CteAutCot (580, 180) -> GenOT (830, 305)
    connectors.append(draw_path("M 660 180 L 730 180 L 730 305 L 742 305", "#D97706", 2.4, "arrow-amber"))
    connectors.append(draw_label(730, 235, "Autoriza Cotización", "edge-label"))

    # 2. GenOT (830, 305) -> HigEcolEval (1100, 305)
    connectors.append(draw_path("M 910 305 L 1002 305", "#2563EB", 2.4, "arrow-blue"))

    # 3. HigEcolEval (1100, 305) -> TecHigMues (1380, 435) [Higiene]
    connectors.append(draw_path("M 1100 344 L 1100 435 L 1292 435", "#0D9488", 2.4, "arrow-teal"))
    connectors.append(draw_label(1190, 435, "Higiene", "edge-label", bg="#F0FDFA", border="#0D9488"))

    # 4. TecHigMues (1380, 435) -> TecHigHojas (1660, 435)
    connectors.append(draw_path("M 1460 435 L 1572 435", "#0D9488", 2.4, "arrow-teal"))

    # 5. TecHigHojas (1660, 435) -> TecHigEnvMues (1960, 435)
    connectors.append(draw_path("M 1740 435 L 1872 435", "#0D9488", 2.4, "arrow-teal"))

    # 6. TecHigEnvMues (1960, 435) -> LabHigMXRecMue (2270, 690)
    connectors.append(draw_path("M 2040 435 L 2120 435 L 2120 690 L 2182 690", "#059669", 2.4, "arrow-green"))

    # 7. LabHigMXRecMue (2270, 690) -> LabHigMXAnaliza (2580, 690)
    connectors.append(draw_path("M 2350 690 L 2492 690", "#059669", 2.4, "arrow-green"))

    # 8. LabHigMXAnaliza (2580, 690) -> LabHigMXReporta (2890, 690)
    connectors.append(draw_path("M 2660 690 L 2802 690", "#059669", 2.4, "arrow-green"))

    # 9. TecHigHojas (1660, 435) -> CordHigRevisa (1960, 565) [Hojas de Campo]
    connectors.append(draw_path("M 1660 464 L 1660 565 L 1867 565", "#0F766E", 2.4, "arrow-teal"))
    connectors.append(draw_label(1760, 565, "Hojas de Campo", "edge-label"))

    # 10. CordHigRevisa (1960, 565) -> CordHigEvalHojas (2270, 565)
    connectors.append(draw_path("M 2045 565 L 2187 565", "#0F766E", 2.4, "arrow-teal"))

    # 11. CordHigEvalHojas (2270, 565) -> TecHigHojas (1660, 435) [Si - Correcciones]
    connectors.append(draw_path("M 2270 529 L 2270 490 L 1700 490 L 1700 472", "#16A34A", 2.2, "arrow-green"))
    connectors.append(draw_label(2270, 508, "Si", "edge-label-yes"))

    # 12. CordHigEvalHojas (2270, 565) -> CordHigEvalMX (2580, 565) [No]
    connectors.append(draw_path("M 2345 565 L 2497 565", "#DC2626", 2.4, "arrow-red"))
    connectors.append(draw_label(2420, 553, "No", "edge-label-no"))

    # 13. CordHigEvalMX (2580, 565) -> CapHigMxRevisa (3200, 815) [Si]
    # Route via gap at X = 2735 between Analiza (2580) and Reporta (2890)
    connectors.append(draw_path("M 2655 565 L 2735 565 L 2735 775 L 3100 775 L 3100 805 L 3112 805", "#16A34A", 2.2, "arrow-green"))
    connectors.append(draw_label(2700, 553, "Si", "edge-label-yes"))

    # 14. LabHigMXReporta (2890, 690) -> CapHigMxRevisa (3200, 815)
    connectors.append(draw_path("M 2970 690 L 3050 690 L 3050 825 L 3112 825", "#7C3AED", 2.4, "arrow-purple"))

    # 15. LabHigMXReporta (2890, 690) -> CapLocGenPDF (4260, 1455)
    connectors.append(draw_path("M 2890 719 L 2890 750 L 4230 750 L 4230 1418", "#2563EB", 2, "arrow-blue", dash="6,4"))
    connectors.append(draw_label(3350, 750, "Resultados Higiene a PDF", "edge-label", bg="#EFF6FF", border="#93C5FD"))

    # 16. CapHigMxRevisa (3200, 815) -> CapHigMxEval (3490, 815)
    connectors.append(draw_path("M 3280 815 L 3407 815", "#7C3AED", 2.4, "arrow-purple"))

    # 17. CapHigMxEval (3490, 815) -> CordHigRevisa (1960, 565) [Si - Correcciones]
    connectors.append(draw_path("M 3490 779 L 3490 515 L 1960 515 L 1960 528", "#16A34A", 2.2, "arrow-green"))
    connectors.append(draw_label(3490, 755, "Si", "edge-label-yes"))

    # 18. CapHigMxEval (3490, 815) -> CapHigMxGenInfPDF (3780, 815) [No]
    connectors.append(draw_path("M 3565 815 L 3687 815", "#DC2626", 2.4, "arrow-red"))
    connectors.append(draw_label(3625, 803, "No", "edge-label-no"))

    # 19. CapHigMxGenInfPDF (3780, 815) -> CapLocCaptura (4040, 1455)
    connectors.append(draw_path("M 3865 815 L 3960 815 L 3960 1445 L 3962 1445", "#1D4ED8", 2.4, "arrow-blue"))

    # 20. HigEcolEval (1100, 305) -> TecEcoMues (1380, 945) [Ecología]
    connectors.append(draw_path("M 1010 305 L 1000 305 L 1000 945 L 1292 945", "#16A34A", 2.4, "arrow-green"))
    connectors.append(draw_label(1000, 640, "Ecología", "edge-label", bg="#F0FDF4", border="#16A34A"))

    # 21. TecEcoMues (1380, 945) -> TecEcoHojas (1660, 945)
    connectors.append(draw_path("M 1460 945 L 1572 945", "#16A34A", 2.4, "arrow-green"))

    # 22. TecEcoHojas (1660, 945) -> TecEcoEnvMues (1960, 945)
    connectors.append(draw_path("M 1740 945 L 1872 945", "#16A34A", 2.4, "arrow-green"))

    # 23. TecEcoEnvMues (1960, 945) -> LabEcoMXRecMue (2270, 1200)
    connectors.append(draw_path("M 2040 945 L 2120 945 L 2120 1200 L 2182 1200", "#10B981", 2.4, "arrow-green"))

    # 24. LabEcoMXRecMue (2270, 1200) -> LabEcoMXAnaliza (2580, 1200)
    connectors.append(draw_path("M 2350 1200 L 2492 1200", "#10B981", 2.4, "arrow-green"))

    # 25. LabEcoMXAnaliza (2580, 1200) -> LabEcoMXReporta (2890, 1200)
    connectors.append(draw_path("M 2660 1200 L 2802 1200", "#10B981", 2.4, "arrow-green"))

    # 26. TecEcoHojas (1660, 945) -> CordEcoRevisa (1960, 1075) [Hojas de Campo]
    connectors.append(draw_path("M 1660 974 L 1660 1075 L 1867 1075", "#15803D", 2.4, "arrow-green"))
    connectors.append(draw_label(1760, 1075, "Hojas de Campo", "edge-label"))

    # 27. CordEcoRevisa (1960, 1075) -> CordEcoEvalHojas (2270, 1075)
    connectors.append(draw_path("M 2045 1075 L 2187 1075", "#15803D", 2.4, "arrow-green"))

    # 28. CordEcoEvalHojas (2270, 1075) -> TecEcoHojas (1660, 945) [Si - Correcciones]
    connectors.append(draw_path("M 2270 1039 L 2270 1000 L 1700 1000 L 1700 982", "#16A34A", 2.2, "arrow-green"))
    connectors.append(draw_label(2270, 1018, "Si", "edge-label-yes"))

    # 29. CordEcoEvalHojas (2270, 1075) -> CapEcoMxRevisa (3200, 1325) [No]
    # Route via gap at X = 2425 between RecMue (2270) and Analiza (2580)
    connectors.append(draw_path("M 2345 1075 L 2425 1075 L 2425 1285 L 3100 1285 L 3100 1315 L 3112 1315", "#DC2626", 2.4, "arrow-red"))
    connectors.append(draw_label(2385, 1063, "No", "edge-label-no"))

    # 30. LabEcoMXReporta (2890, 1200) -> CapEcoMxRevisa (3200, 1325)
    connectors.append(draw_path("M 2970 1200 L 3050 1200 L 3050 1335 L 3112 1335", "#9333EA", 2.4, "arrow-purple"))

    # 31. LabEcoMXReporta (2890, 1200) -> CapLocGenPDF (4260, 1455)
    connectors.append(draw_path("M 2890 1229 L 2890 1260 L 4260 1260 L 4260 1418", "#2563EB", 2, "arrow-blue", dash="6,4"))
    connectors.append(draw_label(3350, 1260, "Resultados Ecología a PDF", "edge-label", bg="#EFF6FF", border="#93C5FD"))

    # 32. CapEcoMxRevisa (3200, 1325) -> CapEcoMxEval (3490, 1325)
    connectors.append(draw_path("M 3280 1325 L 3407 1325", "#9333EA", 2.4, "arrow-purple"))

    # 33. CapEcoMxEval (3490, 1325) -> CordEcoRevisa (1960, 1075) [Si - Correcciones]
    connectors.append(draw_path("M 3490 1289 L 3490 1025 L 1960 1025 L 1960 1038", "#16A34A", 2.2, "arrow-green"))
    connectors.append(draw_label(3490, 1265, "Si", "edge-label-yes"))

    # 34. CapEcoMxEval (3490, 1325) -> CapEcoMxGenInfPDF (3780, 1325) [No]
    connectors.append(draw_path("M 3565 1325 L 3687 1325", "#DC2626", 2.4, "arrow-red"))
    connectors.append(draw_label(3625, 1313, "No", "edge-label-no"))

    # 35. CapEcoMxGenInfPDF (3780, 1325) -> CapLocCaptura (4040, 1455)
    connectors.append(draw_path("M 3865 1325 L 3960 1325 L 3960 1465 L 3962 1465", "#1D4ED8", 2.4, "arrow-blue"))

    # 36. CapLocCaptura (4040, 1455) -> CapLocGenPDF (4260, 1455)
    connectors.append(draw_path("M 4110 1455 L 4182 1455", "#1D4ED8", 2.4, "arrow-blue"))

    # 37. CapLocGenPDF (4260, 1455) -> CapLocGenImp (4480, 1455)
    connectors.append(draw_path("M 4330 1455 L 4402 1455", "#1D4ED8", 2.4, "arrow-blue"))

    # 38. CapLocGenImp (4480, 1455) -> Cobranza (4480, 1580)
    connectors.append(draw_path("M 4480 1484 L 4480 1546", "#E11D48", 2.4, "arrow-red"))

    # Add all connectors first so nodes sit on top
    svg.extend(connectors)

    # Draw Nodes
    for nid, node in nodes.items():
        nx = node["x"]
        ny = node["y"]
        nw = node["w"]
        nh = node["h"]
        shape = node.get("shape", "rect")
        bg_col = node["color"]
        b_col = node["border"]
        
        if shape == "rect":
            rx = nx - nw/2
            ry = ny - nh/2
            svg.append(f'<rect x="{rx}" y="{ry}" width="{nw}" height="{nh}" rx="8" ry="8" fill="{bg_col}" stroke="{b_col}" stroke-width="2" filter="url(#shadow)" />')
            if node["sub"]:
                svg.append(f'<text x="{nx}" y="{ny - 3}" class="node-text">{node["text"]}</text>')
                svg.append(f'<text x="{nx}" y="{ny + 15}" class="node-subtext">{node["sub"]}</text>')
            else:
                svg.append(f'<text x="{nx}" y="{ny + 5}" class="node-text">{node["text"]}</text>')
        elif shape == "diamond":
            p1 = f"{nx},{ny - nh/2}"
            p2 = f"{nx + nw/2},{ny}"
            p3 = f"{nx},{ny + nh/2}"
            p4 = f"{nx - nw/2},{ny}"
            points = f"{p1} {p2} {p3} {p4}"
            svg.append(f'<polygon points="{points}" fill="{bg_col}" stroke="{b_col}" stroke-width="2.2" filter="url(#shadow)" />')
            svg.append(f'<text x="{nx}" y="{ny + 5}" class="decision-text">{node["text"]}</text>')

    svg.append('</svg>')
    return "\n".join(svg)

if __name__ == "__main__":
    svg_content = generate_svg()
    with open("/Users/carlos.sanchez/no-sync-git/pre-diag/diagram.svg", "w") as f:
        f.write(svg_content)
    print("SVG generated successfully at diagram.svg")
