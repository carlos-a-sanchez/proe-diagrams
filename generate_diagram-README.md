# generate_diagram.py

Genera el diagrama swimlane de `OT-Laned-v2.md` como `diagram.svg` y, opcionalmente, lo convierte a `diagram.png`.

## Requisitos

- Python 3 (solo biblioteca estándar; no requiere paquetes adicionales).
- Google Chrome (macOS) para convertir el SVG a PNG.

## Uso

Ejecutar desde la carpeta del proyecto:

```bash
cd /Users/carlos.sanchez/no-sync-git/pre-diag
```

### 1. Generar el SVG

```bash
python3 generate_diagram.py
```

Crea `diagram.svg` en la misma carpeta.

### 2. Convertir el SVG a PNG

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --screenshot=diagram.png \
  --window-size=4680,1720 \
  --default-background-color=00000000 \
  "$PWD/diagram.svg"
```

Crea `diagram.png` (4680 x 1720 px). Los mensajes de error `CVDisplayLinkCreateWithCGDisplay` de Chrome son inofensivos.

### 3. (Opcional) Generar el PDF

Crea una página HTML temporal con el tamaño exacto del diagrama y la imprime a PDF (una sola página):

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

### Todo en un solo comando

```bash
python3 generate_diagram.py && \
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --screenshot=diagram.png \
  --window-size=4680,1720 --default-background-color=00000000 \
  "$PWD/diagram.svg"
```

## Personalización

Todo se define en `generate_diagram.py`, dentro de `generate_svg()`:

| Elemento | Dónde editar |
|---|---|
| Tamaño del lienzo | `width` y `height` al inicio (si los cambia, ajuste también `--window-size`) |
| Carriles y sub-carriles | lista `lanes` (posición `y`, alto `h`, colores) |
| Fases (cabecera superior) | lista `phases` |
| Nodos (texto, posición, forma, color) | diccionario `nodes` (`shape`: `rect` o `diamond`) |
| Conexiones y etiquetas | bloque `connectors` (`draw_path` y `draw_label`) |

Si agrega o mueve nodos, actualice las coordenadas de las conexiones correspondientes.

### 4. (Opcional) Generar el PDF imprimible en hojas Carta

`diagram.pdf` (paso 3) es una sola pagina gigante (equivalente a ~48.75 x 17.9
pulgadas), util para verlo en pantalla pero no para imprimir. Para una version
legible en papel, `generate_print_pdf.py` divide el SVG en 4 franjas verticales
iguales y genera un PDF de 4 paginas tamano Carta (orientacion vertical), una
franja por pagina, cada una con su encabezado y numero de pagina:

```bash
python3 generate_print_pdf.py
```

Crea `OTv2-laned.pdf` (4 paginas). Cada pagina conserva el carril izquierdo
("Carriles / Roles") y el encabezado de fases, por lo que se puede leer de
forma independiente sin necesidad de alinear las 4 hojas.

Si cambia el numero de paginas deseado o el tamano del SVG, ajuste `N_PAGES`,
`IMG_W`/`IMG_H` en `generate_print_pdf.py` (deben coincidir con los valores
`width`/`height` de `generate_diagram.py`).

## Salidas

- `diagram.svg`: vectorial, editable y escalable.
- `diagram.png`: imagen final.
- `diagram.pdf`: PDF de una sola pagina (para pantalla).
- `OTv2-laned.pdf`: PDF de 4 paginas Carta, listo para imprimir.

## Notas

- La ruta de salida del SVG está fija en `generate_diagram.py` (`/Users/carlos.sanchez/no-sync-git/pre-diag/diagram.svg`). Cámbiela en el bloque `__main__` si mueve el proyecto.
- El diagrama es una interpretación manual de `OT-Laned-v2.md`; si cambia el Mermaid, hay que reflejar los cambios en el script.
