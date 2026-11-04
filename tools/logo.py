#!/usr/bin/env python3
"""Rebuild the fx-991EX logo lettering as clean outlines, in photo pixels
measured from a close-up photo of the real face, then map to face.svg group units.

Needs shapely. Writes logo_glyphs.json; paste each path over the matching
logo path in face.svg, then run update-face.py.
"""
import json
from shapely.geometry import box, Polygon, LineString
from shapely.ops import unary_union
from shapely import affinity

def rr(x0, y0, x1, y1, r):
    return box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, quad_segs=8) if r else box(x0, y0, x1, y1)
def soften(g, r_out=1.2, r_in=1.0):
    g = g.buffer(-r_out, quad_segs=6).buffer(r_out, quad_segs=6)
    return g.buffer(r_in, quad_segs=6).buffer(-r_in, quad_segs=6)
def bar(pts, w):
    return LineString(pts).buffer(w / 2, cap_style='flat', join_style='mitre', mitre_limit=4)
U = unary_union

# ---- CASIO: caps 601.5..663, verticals 19, horizontals 14.5
T, B = 601.5, 663
C = rr(439.5, T, 513, B, 17).difference(U([rr(459, 616, 490, 649, 4), box(486, 626.5, 520, 639.5)]))
C = soften(C, 2.5, 1)
cx, k = 555.75, 0.3525
A = Polygon([(539, T), (572.5, T), (594.5, B), (517, B)])
A = A.buffer(-5, join_style='mitre').buffer(5, quad_segs=8).union(box(517, 640, 594.5, B).intersection(Polygon([(539, T), (572.5, T), (594.5, B), (517, B)])))
hole = Polygon([(cx - 3.1, 618), (cx + 3.1, 618), (cx + 8 + k * 33, 664), (cx - 8 - k * 33, 664)])
A = A.difference(hole.difference(box(500, 637, 600, 652)))
A = soften(A, 0.8, 1.5)
S = U([box(598.5, T, 668, 615), box(649, T, 667, 621), box(598.5, T, 616.5, 639), box(598.5, 626, 668, 639),
       box(648.5, 626, 668, B), box(598.5, 649, 668, B), box(599.5, 644, 616, B)])
S = soften(S.intersection(rr(598.5, T, 668, B, 16)), 2, 2)
I = rr(677.5, T, 697, B, 1.5)
O = rr(707.5, T, 782.5, B, 18).difference(rr(726, 616, 764, 648.5, 5))
casio = U([C, A, S, I, O])

# ---- fx-991EX: caps 737.5..778.5, x-height 746.5, stroke 8.5
t, b, w = 737.5, 778.5, 8.5
f = U([bar([(489, b), (489, 747)], w), LineString([(489, 747), (489, 745), (491, 741), (497, t + w / 2), (502, t + w / 2)]).buffer(w / 2, cap_style='flat'),
       box(482, 754, 501, 761.5)]).intersection(box(470, t, 510, b))
x = U([bar([(507.5, 746.5), (533, b)], w), bar([(533, 746.5), (507.5, b)], w)]).intersection(box(506.5, 746.5, 534, b))
hy = box(539.5, 755, 555.5, 762.5)
def nine(x0):
    x1 = x0 + 32
    g = U([rr(x0, t, x1, 765.5, 7).difference(rr(x0 + 8.5, t + 8, x1 - 8.5, 757, 2.5)),
           box(x1 - 8.5, 750, x1, b), box(x0 + 4, 770, x1, b), box(x0, 769, x0 + 8.5, b)])
    return soften(g.intersection(rr(x0, t, x1, b, 8)), 1, 1.2)
one = U([box(649.5, t, 658.5, b), bar([(641, 752), (653, 740)], w)]).intersection(box(639.5, t, 658.5, b))
E = soften(U([box(672.5, t, 681.5, b), box(672.5, t, 703.2, 745.5), box(672.5, 753, 701.5, 761), box(672.5, 770.5, 703.2, b)]).intersection(rr(672.5, t, 703.2, b, 4)), .8, 1)
X = U([bar([(710, t - 2), (742, b + 2)], 9), bar([(742, t - 2), (710, b + 2)], 9)]).intersection(box(708.5, t, 743.5, b))
fx = U([f, x, hy, nine(563.5), nine(600.5), one, E, X])

# ---- CLASSWIZ: caps 804..856.5, drawn 1 px fat all round and thinned at the end
t, b = 804, 856.5
Cw = soften(U([box(409.8, t, 422.5, b), box(409.8, t, 435.8, 812.5), box(409.8, 848, 435.8, b)]).intersection(rr(409.8, t, 435.8, b, 7)), .8, 1.2)
L = U([box(461.5, t, 475, b), box(461.5, 848, 492.2, b)])
Ao = Polygon([(527.5, t), (539.5, t), (551.5, b), (514.5, b)])
d = 10 / 0.488   # inner leg edges, 11 px in from the outer ones, meet here
Ai = Polygon([(538.5 - 0.254 * d, t + d), (528.5 + 0.234 * (b - t + 5), b + 5), (538.5 - 0.254 * (b - t + 5), b + 5)])
Aw = soften(Ao.difference(Ai.difference(box(500, 835, 560, 842.5))), .6, 1)
def ess(x0):
    g = U([box(x0, t, x0 + 29.5, 812), box(x0, t, x0 + 14, 834), box(x0, 825.5, x0 + 32.4, 834),
           box(x0 + 18.4, 825.5, x0 + 32.4, b), box(x0 + 5, 848.5, x0 + 32.4, b)])
    return soften(g.intersection(rr(x0, t, x0 + 32.4, b, 9)), .8, 2.5)
W = U([bar([(687, t - 3), (701.5, b), (709.5, t - 3), (719, b), (733, t - 3)], 9.5)]).intersection(box(683.2, t, 736.5, b))
W = soften(W, .6, .6)
Iw = box(757, t, 770.5, b)
Z = U([box(792.2, t, 820.5, 812), box(793.5, 848, 822.5, b), Polygon([(808, 811), (821, 811), (807, 849), (794, 849)])])
classwiz = U([Cw, L, Aw, ess(575.8), ess(629.2), W, Iw, Z]).buffer(-1, quad_segs=6)

# ---- photo px -> face group units (fitted to the graph-paper layout)
SX, SY = 0.2274, 0.2314
TX, TY = 50 - 439.5 * SX, 28 - 601.5 * SY
def path(g):
    g = affinity.affine_transform(g, [SX, 0, 0, SY, TX, TY]).simplify(0.015)
    polys = g.geoms if hasattr(g, 'geoms') else [g]
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            c = list(ring.coords)[:-1]
            out.append('M' + 'L'.join(f'{x:.2f} {y:.2f}'.replace('.00', '') for x, y in c) + 'Z')
    return ''.join(out)
json.dump({'casio': path(casio), 'fx': path(fx), 'classwiz': path(classwiz)}, open('logo_glyphs.json', 'w'))
for k, v in json.load(open('logo_glyphs.json')).items():
    print(k, len(v))
