"""Generator soal Figural (SVG): deret figural, beda figural, analogi figural.

Setiap soal dibuat dari aturan eksplisit, jadi kunci jawaban dihitung program, bukan ditebak.
Gambar dibuat ulang dengan kode; tidak menyalin gambar buku.
"""
from __future__ import annotations

import math
import random

from .model import LABEL, Q, mk_svg_opts
from .registry import reg

INK = "#111"
BG = "#fff"
LINE = "#555"


def _frame(inner: str, size=100, w=100) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{w}" height="{w}">'
            f'<rect x="1" y="1" width="{size - 2}" height="{size - 2}" rx="4" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>{inner}</svg>')


def _row(cells: list[str], w=100, gap=8, tanya=True) -> str:
    """Gabung beberapa sel menjadi satu SVG baris; tambahkan kotak '?' di akhir bila tanya."""
    items = list(cells)
    n = len(items) + (1 if tanya else 0)
    total_w = n * w + (n - 1) * gap
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {w}" width="{total_w}" height="{w}">']
    for i, c in enumerate(items):
        inner = c.split(">", 1)[1].rsplit("</svg>", 1)[0]
        out.append(f'<g transform="translate({i * (w + gap)},0)">{inner}</g>')
    if tanya:
        x = len(items) * (w + gap)
        out.append(f'<g transform="translate({x},0)"><rect x="1" y="1" width="98" height="98" rx="4" fill="#f3f3f3" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="5 4"/>'
                   f'<text x="50" y="66" text-anchor="middle" font-size="46" font-family="sans-serif" fill="#444">?</text></g>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------
# Elemen dasar
# ---------------------------------------------------------------------
ARROW = [(50, 14), (74, 46), (58, 46), (58, 80), (42, 80), (42, 46), (26, 46)]  # panah menghadap atas (asimetris saat diberi titik)
F_SHAPE = [(30, 20), (70, 20), (70, 34), (46, 34), (46, 46), (62, 46), (62, 60), (46, 60), (46, 82), (30, 82)]  # bentuk "F": tidak simetris cermin


def _poly(points, fill=None, stroke=INK, sw=2.2, tf=""):
    pts = " ".join(f"{x:g},{y:g}" for x, y in points)
    f = fill if fill else BG
    t = f' transform="{tf}"' if tf else ""
    return f'<polygon points="{pts}" fill="{f}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{t}/>'


def _regular(n, r=30, cx=50, cy=50, rot=0, fill=BG):
    pts = [(cx + r * math.sin(math.radians(rot + 360 * i / n)), cy - r * math.cos(math.radians(rot + 360 * i / n))) for i in range(n)]
    return _poly(pts, fill=fill)


def _dots(n, y=90):
    if n <= 0:
        return ""
    gap = 10
    x0 = 50 - (n - 1) * gap / 2
    return "".join(f'<circle cx="{x0 + i * gap:g}" cy="{y}" r="3.4" fill="{INK}"/>' for i in range(n))


# ---------------------------------------------------------------------
# 1. DERET FIGURAL
# ---------------------------------------------------------------------
def _cell_deret(rot, fill_black, dots):
    body = _poly(ARROW, fill=INK if fill_black else BG, tf=f"rotate({rot} 50 50)")
    return _frame(body + _dots(dots, 92) + f'<circle cx="50" cy="50" r="2.2" fill="{"#fff" if fill_black else INK}" transform="rotate({rot} 50 50) translate(0,-22)"/>')


def _arah(step):
    return "searah jarum jam" if step > 0 else "berlawanan arah jarum jam"


@reg("deretfig")
def fig_deret(lv, rng):
    step = rng.choice([45, 90, -90, -45])
    n_rules = lv
    rules = ["rot"]
    if lv >= 2:
        rules.append(rng.choice(["dots", "fill"]))
    if lv >= 3:
        rules = ["rot", "dots", "fill"]
    rot0 = rng.choice([0, 90, 180, 270])
    fill0 = rng.random() < 0.5
    dots0 = rng.randint(0, 2)
    dstep = 1

    def st(i):
        return ((rot0 + step * i) % 360,
                (fill0 if "fill" not in rules else (fill0 if i % 2 == 0 else not fill0)),
                (dots0 + dstep * i) if "dots" in rules else dots0)

    cells = [_cell_deret(*st(i)) for i in range(4)]
    cr, cf, cd = st(4)
    correct = _cell_deret(cr, cf, cd)
    # pengecoh: ubah satu atribut dari jawaban benar
    variants = [
        ((cr + 90) % 360, cf, cd), ((cr - 90) % 360, cf, cd), ((cr + 45) % 360, cf, cd),
        (cr, not cf, cd), (cr, cf, cd + 1), (cr, cf, max(cd - 1, 0)),
        ((cr + 180) % 360, cf, cd), ((cr + 90) % 360, not cf, cd), (cr, not cf, cd + 1),
    ]
    seen = {(cr, cf, cd)}
    opts = [correct]
    for v in variants:
        if v not in seen and 0 <= v[2] <= 7:
            seen.add(v)
            opts.append(_cell_deret(*v))
        if len(opts) == 5:
            break
    kaidah = [f"gambar berputar {abs(step)}° {_arah(step)} tiap langkah"]
    if "dots" in rules:
        kaidah.append("jumlah titik di bawah bertambah 1 tiap langkah")
    if "fill" in rules:
        kaidah.append("warna panah berganti hitam-putih secara bergantian")
    exp = "Aturan yang berlaku: " + "; ".join(kaidah) + ". Terapkan sekali lagi pada gambar ke-4 untuk mendapat gambar ke-5."
    trick = "Lacak SATU atribut per langkah (arah putar, jumlah titik, warna), jangan seluruh gambar sekaligus. Coret opsi yang gagal pada atribut pertama."
    return mk_svg_opts("deretfig", lv, "Perhatikan pola gambar berikut. Gambar manakah yang menggantikan tanda tanya?", opts, 0, exp, trick, rng, svg=_row(cells))


# ---------------------------------------------------------------------
# 2. BEDA FIGURAL
# ---------------------------------------------------------------------
def _cell_dots(points):
    return _frame("".join(f'<circle cx="{x:g}" cy="{y:g}" r="3.6" fill="{INK}"/>' for x, y in points))


def _scatter(n, rng, minimal=17):
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        x, y = rng.uniform(12, 88), rng.uniform(12, 88)
        if all((x - a) ** 2 + (y - b) ** 2 >= minimal ** 2 for a, b in pts):
            pts.append((x, y))
    return pts


@reg("deretfig", (1, 2, 3))
def fig_beda(lv, rng):
    if lv == 1:
        n = rng.randint(7, 11)
        odd = rng.choice([n + 1, n - 1])
        cells = []
        for _ in range(4):
            p = _scatter(n, rng)
            while len(p) < n:
                p = _scatter(n, rng)
            cells.append(_cell_dots(p))
        po = _scatter(odd, rng)
        while len(po) < odd:
            po = _scatter(odd, rng)
        cells.append(_cell_dots(po))
        order = list(range(5))
        rng.shuffle(order)
        opts = [cells[i] for i in order]
        ans = order.index(4)
        exp = f"Empat gambar masing-masing berisi {n} titik, sedangkan satu gambar berisi {odd} titik. Gambar yang berbeda adalah yang berjumlah {odd} titik."
        trick = "Hitung titik per kuadran (kiri atas, kanan atas, kiri bawah, kanan bawah), lalu jumlahkan. Mencoret titik yang sudah dihitung menghindari hitung dua kali."
        return _beda(lv, opts, ans, exp, trick, rng)
    if lv == 2:
        k = rng.choice([4, 5, 6])
        odd = k + rng.choice([-1, 1])
        if odd < 3:
            odd = k + 1
        sudut = rng.sample(range(0, 360, 12), 5)
        cells = [_frame(_regular(k, 30, 50, 50, sudut[i])) for i in range(4)]
        cells.append(_frame(_regular(odd, 30, 50, 50, sudut[4])))
        order = list(range(5))
        rng.shuffle(order)
        opts = [cells[i] for i in order]
        exp = f"Empat gambar adalah segi-{k} dengan putaran yang berbeda-beda, satu gambar adalah segi-{odd}. Putaran tidak mengubah jenis bangun."
        trick = "Abaikan putaran. Hitung sudutnya atau sisinya. Bangun yang diputar tetap bangun yang sama."
        return _beda(lv, opts, order.index(4), exp, trick, rng)
    rots = [0, 90, 180, 270]
    rng.shuffle(rots)
    cells = [_frame(_poly(F_SHAPE, fill=BG, tf=f"rotate({r} 50 50)")) for r in rots]
    cermin = _frame(_poly(F_SHAPE, fill=BG, tf=f"translate(100,0) scale(-1,1) rotate({rng.choice([0, 90, 180, 270])} 50 50)"))
    cells.append(cermin)
    order = list(range(5))
    rng.shuffle(order)
    opts = [cells[i] for i in order]
    exp = "Empat gambar adalah bentuk yang sama yang hanya diputar. Satu gambar adalah bayangan cermin dari bentuk itu: bentuk ini tidak bisa diputar menjadi bayangan cermin, jadi itulah yang berbeda."
    trick = "Putaran tidak mengubah arah “lengan” bentuk (kiri/kanan relatif terhadap batang). Cermin membalik arah itu. Cek satu ciri: tonjolan ada di sisi mana dari batang?"
    return _beda(lv, opts, order.index(4), exp, trick, rng)


def _beda(lv, opts, ans, exp, trick, rng):
    q = Q(id=f"deretfig-b{lv}-{rng.randrange(10**9):09d}", bab="deretfig", lv=lv,
          stem="Dari lima gambar berikut, manakah yang berbeda dari keempat gambar lainnya?", opts=list(LABEL[: len(opts)]), ans=ans, exp=exp, trick=trick, opt_svgs=opts)
    return q


# ---------------------------------------------------------------------
# 3. ANALOGI FIGURAL
# ---------------------------------------------------------------------
KINDS = ["segitiga", "persegi", "segilima"]
CORNERS = [(27, 27), (73, 27), (73, 73), (27, 73)]


def _big_shape(kind, fill_black, orient):
    f = INK if fill_black else BG
    tf = f"rotate({orient * 90} 50 50)"
    if kind == "segitiga":
        return _poly([(50, 14), (88, 80), (12, 80)], fill=f, tf=tf)
    if kind == "persegi":
        return _poly([(18, 18), (82, 18), (82, 82), (18, 82)], fill=f, tf=tf)
    return _regular(5, 38, 50, 52, orient * 90, fill=f)


def _small(kind_small, fill_black, corner):
    x, y = CORNERS[corner % 4]
    f = INK if fill_black else BG
    if kind_small == "lingkaran":
        halo = f'<circle cx="{x}" cy="{y}" r="10" fill="#fff" stroke="#fff" stroke-width="3"/>'
        return halo + f'<circle cx="{x}" cy="{y}" r="8" fill="{f}" stroke="{INK}" stroke-width="2.2"/>'
    halo = f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" fill="#fff" stroke="#fff" stroke-width="3"/>'
    return halo + f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16" fill="{f}" stroke="{INK}" stroke-width="2.2"/>'


def _cell_analog(s, small_kind):
    return _frame(_big_shape(s["kind"], s["fb"], s["orient"]) + _small(small_kind, s["fs"], s["corner"]))


def _key(s):
    o = s["orient"] % 4 if s["kind"] != "persegi" else 0
    return (s["kind"], s["fb"], s["fs"], s["corner"] % 4, o)


def _apply(s, t):
    s = dict(s)
    if t[0] == "rot":
        s["orient"] = (s["orient"] + t[1]) % 4
        s["corner"] = (s["corner"] + t[1]) % 4
    elif t[0] == "fb":
        s["fb"] = not s["fb"]
    elif t[0] == "fs":
        s["fs"] = not s["fs"]
    elif t[0] == "kind":
        s["kind"] = KINDS[(KINDS.index(s["kind"]) + 1) % 3]
    return s


def _desk(t):
    if t[0] == "rot":
        deg = t[1] * 90
        return f"seluruh gambar diputar {deg}° searah jarum jam" if deg <= 180 else "seluruh gambar diputar 90° berlawanan arah jarum jam"
    return {"fb": "warna bangun besar dibalik (hitam ↔ putih)", "fs": "warna bangun kecil dibalik (hitam ↔ putih)",
            "kind": "bangun besar berganti ke bangun berikutnya (segitiga → persegi → segilima → segitiga)"}[t[0]]


@reg("analogifig")
def fig_analogi(lv, rng):
    small_kind = rng.choice(["lingkaran", "persegi"])
    pool = [("rot", rng.choice([1, 2, 3])), ("fb",), ("fs",), ("kind",)]
    rng.shuffle(pool)
    ts = pool[:lv]
    if lv == 1:
        ts = [rng.choice([("rot", rng.choice([1, 2, 3])), ("fb",), ("kind",)])]
    # dua keadaan awal berbeda
    def acak():
        return {"kind": rng.choice(KINDS), "fb": rng.random() < 0.5, "fs": rng.random() < 0.5, "orient": rng.randrange(4), "corner": rng.randrange(4)}
    for _ in range(100):
        a, c = acak(), acak()
        if _key(a) != _key(c):
            break
    b = a
    d = c
    for t in ts:
        b = _apply(b, t)
        d = _apply(d, t)
    correct_key = _key(d)
    cells_row = [_cell_analog(a, small_kind), _cell_analog(b, small_kind), _cell_analog(c, small_kind)]
    stem_svg = _row(cells_row)
    # pengecoh: terapkan sebagian aturan / aturan salah / aturan kebalikan
    cands = []
    for omit in range(len(ts)):
        s = c
        for i, t in enumerate(ts):
            if i != omit:
                s = _apply(s, t)
        cands.append(s)
    s = c
    for t in ts:
        s = _apply(s, ("rot", (-t[1]) % 4) if t[0] == "rot" else t)
    cands.append(s)
    for extra in [("fb",), ("fs",), ("kind",), ("rot", 1), ("rot", 2), ("rot", 3)]:
        cands.append(_apply(d, extra))
    keys = {correct_key}
    opts = [_cell_analog(d, small_kind)]
    for cnd in cands:
        k = _key(cnd)
        if k not in keys:
            keys.add(k)
            opts.append(_cell_analog(cnd, small_kind))
        if len(opts) == 5:
            break
    exp = "Aturan dari gambar 1 → gambar 2: " + "; ".join(_desk(t) for t in ts) + ". Terapkan aturan yang sama pada gambar 3 untuk mendapat jawaban."
    trick = "Bandingkan gambar 1 dan 2 satu atribut demi satu: bentuk besar, warna besar, warna kecil, posisi bangun kecil. Daftarkan perubahannya, lalu terapkan ke gambar 3 dan coret opsi yang gagal."
    return mk_svg_opts("analogifig", lv, "Gambar 1 berbanding gambar 2 sebagaimana gambar 3 berbanding … ?", opts, 0, exp, trick, rng, svg=stem_svg)
