"""Genera las ilustraciones SVG del README (cabecera y barra de focos).

Uso:
  python generar.py <ruta a bricolage-grotesque-latin-standard-normal.woff2>

Necesita fonttools y brotli (pip install fonttools brotli). La fuente se recorta
a los caracteres usados y se incrusta en cada SVG, porque GitHub muestra los SVG
como imágenes y no pueden cargar fuentes externas.
"""

import base64
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"

CARBON = "#17120e"
LINEA = "#3a2e25"
HUESO = "#f4ebdd"
ARENA = "#b8a895"
AMBAR = "#f2a541"

FOCOS = [
    ("Diseño", "Figma · Tailwind · Astro"),
    ("Código", "PHP · Laravel · Filament"),
    ("Servidor", "Linux · Docker · Caddy"),
    ("Automatización", "n8n · PostgreSQL · IA"),
]


def fuente_recortada(ruta: Path, texto: str) -> str:
    """Devuelve la fuente recortada a los caracteres de `texto`, en base64."""
    fuente = TTFont(ruta)
    opciones = subset.Options()
    opciones.flavor = "woff2"
    opciones.layout_features = ["*"]
    recortador = subset.Subsetter(opciones)
    recortador.populate(text=texto)
    recortador.subset(fuente)
    salida = io.BytesIO()
    fuente.flavor = "woff2"
    fuente.save(salida)
    return base64.b64encode(salida.getvalue()).decode()


def estilo_fuente(b64: str) -> str:
    return (
        "@font-face{font-family:B;font-weight:200 800;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
        "text{font-family:B,'Helvetica Neue',Arial,sans-serif}"
    )


def cabecera(fuente: Path) -> str:
    textos = ["Ricardo Andreu", "Doy la cara", "por tu web.", "Desarrollo web y software en Valencia.", "ricardoandreu.com"]
    b64 = fuente_recortada(fuente, "".join(textos))
    retrato = base64.b64encode((ASSETS / "retrato.jpg").read_bytes()).decode()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="480" viewBox="0 0 1280 480" role="img" aria-labelledby="t">
<title id="t">Ricardo Andreu. Doy la cara por tu web. Desarrollo web y software en Valencia.</title>
<style>{estilo_fuente(b64)}
.halo{{transform-origin:960px 240px;animation:encender 1.8s cubic-bezier(.2,.7,.2,1) .2s both}}
.texto{{animation:aparecer .9s ease-out .9s both}}
@keyframes encender{{0%{{opacity:0;transform:scale(.8)}}35%{{opacity:.4}}45%{{opacity:.12}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes aparecer{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.halo,.texto{{animation:none}}}}
</style>
<defs>
<radialGradient id="luz" cx="50%" cy="50%" r="50%">
<stop offset="0" stop-color="{AMBAR}" stop-opacity=".62"/>
<stop offset=".55" stop-color="#e8762b" stop-opacity=".2"/>
<stop offset="1" stop-color="#e8762b" stop-opacity="0"/>
</radialGradient>
<clipPath id="recorte"><rect width="1280" height="480" rx="28"/></clipPath>
<clipPath id="circulo"><circle cx="960" cy="240" r="168"/></clipPath>
</defs>
<g clip-path="url(#recorte)">
<rect width="1280" height="480" fill="{CARBON}"/>
<circle class="halo" cx="960" cy="240" r="330" fill="url(#luz)"/>
<image href="data:image/jpeg;base64,{retrato}" x="792" y="72" width="336" height="336" clip-path="url(#circulo)" preserveAspectRatio="xMidYMid slice"/>
<g class="texto">
<text x="80" y="118" fill="{HUESO}" font-size="28" font-weight="700">Ricardo Andreu</text>
<text x="76" y="232" fill="{HUESO}" font-size="92" font-weight="700" letter-spacing="-2.5">Doy la cara</text>
<text x="76" y="326" fill="{HUESO}" font-size="92" font-weight="700" letter-spacing="-2.5">por tu web.</text>
<text x="80" y="384" fill="{ARENA}" font-size="26">Desarrollo web y software en Valencia.</text>
<text x="80" y="428" fill="{AMBAR}" font-size="22" font-weight="600">ricardoandreu.com</text>
</g>
</g>
</svg>
"""


def plato(fuente: Path) -> str:
    texto = "".join(t + d for t, d in FOCOS)
    b64 = fuente_recortada(fuente, texto)
    ancho, alto, columna = 1280, 330, 1280 / 4
    focos = []
    for i, (titulo, detalle) in enumerate(FOCOS):
        x = columna * i + columna / 2
        retraso = 0.4 + i * 0.55
        focos.append(f"""<g class="foco" style="animation-delay:{retraso:.2f}s">
<path d="M{x - 13} 46 L{x + 13} 46 L{x + 120} 250 L{x - 120} 250 Z" fill="url(#haz)"/>
</g>
<rect x="{x - 22}" y="28" width="44" height="20" rx="8" fill="{LINEA}"/>
<g class="etiqueta" style="animation-delay:{retraso + 0.15:.2f}s">
<text x="{x}" y="232" text-anchor="middle" fill="{HUESO}" font-size="30" font-weight="700">{titulo}</text>
<text x="{x}" y="270" text-anchor="middle" fill="{ARENA}" font-size="20">{detalle}</text>
</g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}" role="img" aria-labelledby="t">
<title id="t">Con qué trabajo. Diseño: Figma, Tailwind y Astro. Código: PHP, Laravel y Filament. Servidor: Linux, Docker y Caddy. Automatización: n8n, PostgreSQL e IA.</title>
<style>{estilo_fuente(b64)}
.foco,.etiqueta{{animation:encender 1.1s ease-out both}}
.etiqueta{{animation-name:aparecer}}
@keyframes encender{{0%{{opacity:0}}40%{{opacity:.7}}52%{{opacity:.15}}100%{{opacity:1}}}}
@keyframes aparecer{{from{{opacity:.2}}to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.foco,.etiqueta{{animation:none}}}}
</style>
<defs>
<linearGradient id="haz" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{AMBAR}" stop-opacity=".42"/>
<stop offset="1" stop-color="{AMBAR}" stop-opacity="0"/>
</linearGradient>
<clipPath id="recorte"><rect width="{ancho}" height="{alto}" rx="28"/></clipPath>
</defs>
<g clip-path="url(#recorte)">
<rect width="{ancho}" height="{alto}" fill="{CARBON}"/>
<rect x="40" y="26" width="{ancho - 80}" height="4" rx="2" fill="{LINEA}"/>
{"".join(focos)}
</g>
</svg>
"""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fuente = Path(sys.argv[1])
    (ASSETS / "cabecera.svg").write_text(cabecera(fuente), encoding="utf-8")
    (ASSETS / "plato.svg").write_text(plato(fuente), encoding="utf-8")
    print("SVG generados en assets/")
