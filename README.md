# Diagramas del Ciclo de Vida de OT

Scripts que generan diagramas swimlane a partir de `OT-Laned-v2.md` (Mermaid) y de la imagen `Ciclo vida OT - lanes v1 - 2016.png`.

## Requisitos

- Python 3 (solo biblioteca estándar, sin paquetes adicionales).
- Google Chrome y draw.io Desktop (ambos en `/Applications`), solo para convertir a PNG o PDF.
- Ejecutar todos los comandos desde esta carpeta:

```bash
cd /Users/carlos.sanchez/no-sync-git/pre-diag
```

## Archivos

| Script | Salida | Fuente de datos |
|---|---|---|
| `generate_diagram.py` | `diagram.svg` (+ `diagram.png`, `diagram.pdf`) | Título y subtítulo de `OT-Laned-v2.md`; nodos y flechas en el script |
| `generate_drawio.py` | `diagram.drawio` (carriles horizontales) | Título y subtítulo de `OT-Laned-v2.md`; nodos y flechas en el script |
| `generate_vertical_drawio.py` | `vertical-diagram.drawio` (carriles verticales) | Importa los datos de `generate_drawio.py` |
| `generate_lanes_v1_drawio.py` | `Ciclo vida OT - lanes v1 - 2016.drawio` | Coordenadas tomadas de la imagen `Ciclo vida OT - lanes v1 - 2016.png` |

Los scripts no leen el Mermaid completo: solo el título (`# ...`) y el subtítulo (`## ...`). Los nodos, carriles y flechas están escritos dentro de cada script, así que si cambia el Mermaid hay que actualizarlos a mano.

## 1. generate_diagram.py (SVG, PNG y PDF)

Genera `diagram.svg` con carriles horizontales y barra de fases.

```bash
python3 generate_diagram.py
```

Convertir a PNG:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --screenshot=diagram.png \
  --window-size=4680,1720 \
  --default-background-color=00000000 \
  "$PWD/diagram.svg"
```

Convertir a PDF (una sola página):

```bash
cat > /tmp/diagram_pdf.html <<EOF
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: 4680px 1720px; margin: 0 }
html,body { margin:0; padding:0 }
img { display:block; width:4680px; height:1720px }
</style></head><body><img src="file://$PWD/diagram.svg"></body></html>
EOF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=diagram.pdf /tmp/diagram_pdf.html
```

Los mensajes de error `CVDisplayLinkCreateWithCGDisplay` de Chrome son inofensivos.

Personalización dentro de `generate_svg()`: `width` y `height` (el tamaño del lienzo; si los cambia, ajuste también `--window-size`), la lista `lanes`, la lista `phases`, el diccionario `nodes` y el bloque de conexiones.

> Este script no incluye los carriles de Cobranza con nodos ni el carril de Logística: su versión del diagrama corresponde a un estado anterior de `OT-Laned-v2.md`. Para la versión actual use los scripts draw.io.

## 2. generate_drawio.py (draw.io horizontal)

```bash
python3 generate_drawio.py
```

Crea `diagram.drawio`, que se abre en draw.io Desktop o en app.diagrams.net. Los carriles son contenedores `swimlane` y los nodos son sus hijos.

Este es el archivo de datos principal. Para actualizar el diagrama cuando cambie el Mermaid, edite estas estructuras:

| Estructura | Qué define |
|---|---|
| `LANES` | Carriles y sub-carriles (posición, alto, colores) |
| `NODES` | Nodos (carril, posición, tamaño, texto, forma, colores) |
| `EDGES` | Flechas (origen, destino, etiqueta, color, punteada, puntos intermedios, estilo extra) |

Las etiquetas aceptan HTML, por ejemplo `Si<br><i>Fecha Revision HdC</i>`.

## 3. generate_vertical_drawio.py (draw.io vertical)

```bash
python3 generate_vertical_drawio.py
```

Crea `vertical-diagram.drawio` con los carriles como columnas y el flujo de arriba hacia abajo. Importa `LANES`, `NODES` y `EDGES` de `generate_drawio.py`, por lo que:

- ambos archivos deben estar en la misma carpeta;
- los cambios de contenido se hacen solo en `generate_drawio.py`;
- después de editar `generate_drawio.py`, ejecute los dos scripts para mantener ambos diagramas iguales.

Constantes de diseño al inicio del script: `SX` y `SY` (escala horizontal y vertical), `LANE_H` (alto de los carriles, súbalo si agrega nodos al final del flujo), `HEAD` y `SUBHEAD`.

## 4. generate_lanes_v1_drawio.py (reproducción de la imagen de 2016)

```bash
python3 generate_lanes_v1_drawio.py
```

Crea `Ciclo vida OT - lanes v1 - 2016.drawio`. Reproduce la imagen original con las mismas coordenadas en píxeles. Edite `LANES`, `NODES`, `NOTES` (notas amarillas) y `EDGES` para cambiar posiciones o textos.

## Exportar draw.io a PNG o PDF

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -b 20 -o salida.png archivo.drawio
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f pdf -b 20 -o salida.pdf archivo.drawio
```

Por ejemplo, para `vertical-diagram.drawio`:

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -b 20 -o vertical-diagram.png vertical-diagram.drawio
```

## Flujo de trabajo recomendado cuando cambia `OT-Laned-v2.md`

1. Actualizar `NODES`, `EDGES` y `LANES` en `generate_drawio.py`.
2. Ejecutar `python3 generate_drawio.py && python3 generate_vertical_drawio.py`.
3. Abrir los `.drawio` y ajustar a mano las flechas o etiquetas que se encimen.
4. Opcional: exportar a PNG o PDF con el comando de draw.io.

## Otros archivos

- `generate_diagram-README.md`: instrucciones originales de `generate_diagram.py`.
- `draw-swimlane-chart.md`: descripción en español del diagrama y sus carriles.
