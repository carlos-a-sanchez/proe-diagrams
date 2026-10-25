"""Genera una version del diagrama lista para imprimir en papel Carta (Letter).

El diagrama (`diagram.svg`) es muy ancho para una sola hoja, asi que este script
lo divide en franjas verticales iguales y las distribuye en varias paginas
Carta en orientacion vertical (portrait), una franja por pagina. Cada pagina
conserva el encabezado con el titulo y el carril izquierdo "Carriles / Roles"
queda repetido en todas las paginas (ya forma parte del propio diagrama),
de modo que el resultado es legible al imprimirse.

Requiere Google Chrome (usa su modo headless para convertir HTML a PDF).
"""

import os
import subprocess

PROJECT_DIR = "/Users/carlos.sanchez/no-sync-git/pre-diag"
SVG_PATH = os.path.join(PROJECT_DIR, "diagram.svg")
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Dimensiones nativas del SVG (deben coincidir con `width`/`height` en generate_diagram.py)
IMG_W, IMG_H = 4680, 1720

# Geometria de pagina Carta (pulgadas)
PAGE_W, PAGE_H = 8.5, 11.0
MARGIN = 0.3
HEADER_H = 0.35  # franja reservada para titulo + numero de pagina

N_PAGES = 4


def build_html(svg_path=SVG_PATH, n_pages=N_PAGES, title="Ciclo de vida OT - 2026",
               subtitle="Diagrama de procesos: Emision de OT, Muestreo y Reporte de Resultados"):
    ratio = IMG_W / IMG_H
    printable_w = PAGE_W - 2 * MARGIN
    printable_h = PAGE_H - 2 * MARGIN
    diagram_h = printable_h - HEADER_H

    scaled_total_w = diagram_h * ratio
    slice_w = scaled_total_w / n_pages

    pages = []
    for i in range(n_pages):
        left = -(i * slice_w)
        pages.append(f'''    <div class="page">
      <div class="header">{title} &mdash; {subtitle} &nbsp;|&nbsp; Pagina {i + 1} de {n_pages}</div>
      <div class="diagram" style="background-position: {left:.4f}in 0;"></div>
    </div>''')

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: letter portrait; margin: {MARGIN}in; }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  .page {{
    width: {printable_w:.4f}in;
    height: {printable_h:.4f}in;
    page-break-after: always;
    overflow: hidden;
  }}
  .page:last-child {{ page-break-after: auto; }}
  .header {{
    height: {HEADER_H:.4f}in;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8pt;
    color: #334155;
    border-bottom: 1px solid #CBD5E1;
    padding-bottom: 2px;
    margin-bottom: 2px;
  }}
  .diagram {{
    width: {slice_w:.4f}in;
    height: {diagram_h:.4f}in;
    background-image: url('file://{svg_path}');
    background-repeat: no-repeat;
    background-size: {scaled_total_w:.4f}in {diagram_h:.4f}in;
  }}
</style>
</head>
<body>
{chr(10).join(pages)}
</body>
</html>
'''


def generate_print_pdf(output_pdf, html_tmp_path="/tmp/_diagram_print.html", n_pages=N_PAGES):
    html = build_html(n_pages=n_pages)
    with open(html_tmp_path, "w", encoding="utf-8") as f:
        f.write(html)

    subprocess.run([
        CHROME_PATH,
        "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf}",
        html_tmp_path,
    ], check=True)
    os.remove(html_tmp_path)
    print(f"PDF de impresion generado en {output_pdf} ({n_pages} paginas Carta)")


if __name__ == "__main__":
    generate_print_pdf(os.path.join(PROJECT_DIR, "OTv2-laned.pdf"))
