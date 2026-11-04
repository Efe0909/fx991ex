#!/usr/bin/env python3
"""Print the SVG <defs> for the fx-991EX face texture.

The real face tiles one prototile by translation alone. Each facet is a
chevron: a 2a rhombus with the a-sized rhombus cut from its far (obtuse)
corner. Three chevrons, one per isometric orientation, meet at a point as a Y,
and the Ys sit on a triangular lattice of spacing 3a, so every chevron's notch
is filled by the arms of the neighbouring Ys. Every facet is filled with
parallel grooves along one of its edges; the direction depends only on the
facet's orientation and turns 120 degrees between orientations.

Paste the output over the texture defs in face.svg, then run update-face.py.
Pass --mirror to flip the groove handedness, --preview for a test sheet.
"""
import math
import sys

A = 3.5            # small rhombus edge (face units); chevrons are 2A across
PITCH = .76        # groove pitch: four grooves per chevron arm, as on the real face
INSET = .18        # gap where grooves meet a neighbouring facet
MIRROR = '--mirror' in sys.argv


def d(deg, r=1):
    """Vector at deg (screen y down, 0 = right, 90 = down)."""
    return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))


def add(*vs):
    return (sum(v[0] for v in vs), sum(v[1] for v in vs))


def mul(v, s):
    return (v[0] * s, v[1] * s)


# Facet orientations: name -> (edge directions, groove direction, ridge colour).
# Up is 270. Ridges catch the light differently by groove direction.
FACES = {
    'top': ((210, 330), 210 if MIRROR else 330, '#565959'),
    'left': ((90, 210), 90 if MIRROR else 210, '#444747'),
    'right': ((90, 330), 330 if MIRROR else 90, '#373a3a'),
}


def chevron(o, e1, e2):
    """2A rhombus from o along e1/e2, minus the A rhombus at the far corner."""
    p, q = d(e1, A), d(e2, A)
    return [o, add(o, p, p), add(o, p, p, q), add(o, p, q), add(o, p, q, q), add(o, q, q)]


def hatch(poly, deg):
    """Groove centre lines through poly, parallel to deg, about PITCH apart."""
    u = d(deg)
    n = (-u[1], u[0])
    proj = [x * n[0] + y * n[1] for x, y in poly]
    lo, hi = min(proj), max(proj)
    count = max(1, round((hi - lo) / PITCH))
    step = (hi - lo) / count
    segs = []
    for i in range(count):
        c = lo + (i + .5) * step
        hits = []
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            a1, a2 = x1 * n[0] + y1 * n[1] - c, x2 * n[0] + y2 * n[1] - c
            if (a1 < 0) != (a2 < 0):
                t = a1 / (a1 - a2)
                hits.append((x1 + (x2 - x1) * t) * u[0] + (y1 + (y2 - y1) * t) * u[1])
        hits.sort()
        for s, e in zip(hits[::2], hits[1::2]):
            if e - s > 2 * INSET + .2:
                segs.append((add(mul(u, s + INSET), mul(n, c)), add(mul(u, e - INSET), mul(n, c))))
    return segs


def facets():
    """(orientation, polygon) for the Y centred on the origin."""
    return [(k, chevron((0, 0), *v[0])) for k, v in FACES.items()]


def f(x):
    return '0' if abs(x) < .005 else f'{x:.2f}'.rstrip('0').rstrip('.')


def pts(poly):
    return ' '.join(f'{f(x)},{f(y)}' for x, y in poly)


# Lattice of Ys: 3A straight down and 3A at 30 degrees. The rectangular pattern
# cell holds two Ys; every Y that pokes into the cell is drawn.
V1, V2 = d(90, 3 * A), d(30, 3 * A)
W = 2 * V2[0]
H = V1[1]
CENTRES = [add(mul(V1, m), mul(V2, n)) for m in range(-3, 4) for n in range(-1, 4)]
CENTRES = [c for c in CENTRES if -2 * A < c[0] < W + 2 * A and -2 * A < c[1] < H + 2 * A]

fills, cube, grooves = [], [], []
for name, (_, deg, ridge) in FACES.items():
    polys = [p for k, p in facets() if k == name]
    segs = [s for p in polys for s in hatch(p, deg)]
    line = ''.join(f'M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}' for a, b in segs)
    fills += [f'  <polygon points="{pts(p)}" fill="{ridge}"/>' for p in polys]
    cube.append(f'  <path d="{line}" fill="none" stroke="#0c0d0d" stroke-width=".36"/>')
    grooves.append(f'  <path d="{line}"/>')


def uses(ref):
    return ''.join(f'<use href="#{ref}" x="{f(x)}" y="{f(y)}"/>' for x, y in CENTRES)


tile = f''' <g id="weave-y" stroke-linecap="round">
{chr(10).join(fills + cube)}
 </g>
 <g id="weave-y-grooves" fill="none" stroke="#000" stroke-width=".3" stroke-linecap="round">
{chr(10).join(grooves)}
 </g>
 <pattern id="carbon" width="{f(W)}" height="{f(H)}" patternUnits="userSpaceOnUse">
  <rect width="{f(W)}" height="{f(H)}" fill="#2a2d2d"/>
  {uses('weave-y')}
 </pattern>
 <pattern id="print-grooves" width="{f(W)}" height="{f(H)}" patternUnits="userSpaceOnUse">
  <rect width="{f(W)}" height="{f(H)}" fill="#fff"/>
  <g opacity=".42">{uses('weave-y-grooves')}</g>
 </pattern>'''

if '--preview' in sys.argv:
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="560" viewBox="0 0 24.6 19.2"><defs>{tile}</defs>'
          '<rect width="24.6" height="19.2" fill="url(#carbon)"/></svg>')
else:
    print(tile)
