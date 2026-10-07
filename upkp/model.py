"""Model soal dan helper pembuat soal pilihan ganda 5 opsi."""
from __future__ import annotations

import random
import re
from dataclasses import asdict, dataclass, field

LABEL = "ABCDE"
LEVEL_NAMA = {1: "Foundation", 2: "Standard", 3: "Exam", 4: "Hard", 5: "Expert"}
# Pengali target waktu per tingkat (patokan latihan, bukan ketentuan resmi).
LEVEL_PENGALI = {1: 1.0, 2: 1.15, 3: 1.3, 4: 1.5, 5: 1.7}


@dataclass
class Q:
    id: str
    bab: str
    lv: int
    stem: str
    opts: list
    ans: int
    exp: str
    trick: str = ""
    svg: str = ""                       # gambar untuk soal (SVG)
    opt_svgs: list = field(default_factory=list)  # gambar untuk tiap opsi (SVG)
    waktu: int = 45                     # target detik
    skill: str = ""                    # canonical micro-skill tag (V2.1+)
    archetype: str = ""                # structural template family for QA/calibration

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Q":
        return Q(**d)


def fmt_id(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def rp(n: int) -> str:
    return "Rp" + fmt_id(int(n))


def dc(x) -> str:
    """Angka desimal gaya Indonesia (koma)."""
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    return str(x).replace(".", ",")



_NUM = re.compile(r"^(?P<pre>[^\d]*)(?P<num>\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?)(?P<post>[^\d]*)$")
_TIME = re.compile(r"^(\d\d)\.(\d\d)$")


def _pad_text(cs, seen, ds):
    """Tambah pengecoh untuk jawaban teks bernomor (Rp, %, derajat, satuan, jam)."""
    mt = _TIME.match(cs)
    if mt:
        base = int(mt.group(1)) * 60 + int(mt.group(2))
        k = 1
        while len(ds) < 4 and k < 60:
            sg = 1 if k % 2 else -1
            m = base + sg * ((k + 1) // 2) * 5
            if 0 <= m < 24 * 60:
                c = f"{m // 60:02d}.{m % 60:02d}"
                if c not in seen:
                    seen.add(c)
                    ds.append(c)
            k += 1
        return
    m = _NUM.match(cs)
    if not m:
        return
    num = m.group("num")
    thousands = bool(re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", num))
    dec = len(num.split(",")[1]) if "," in num else 0
    val = float(num.replace(".", "").replace(",", "."))
    if dec:
        step = 0.5 if dec == 1 else 0.25
    else:
        step = 1 if val < 10 else max(1, round(val * 0.08))
    k = 1
    while len(ds) < 4 and k < 80:
        sg = 1 if k % 2 else -1
        v = val + sg * ((k + 1) // 2) * step
        if v > 0:
            if dec:
                t = f"{v:.{dec}f}".replace(".", ",")
            else:
                t = str(int(round(v)))
                if thousands:
                    t = fmt_id(int(t))
            c = m.group("pre") + t + m.group("post")
            if c not in seen:
                seen.add(c)
                ds.append(c)
        k += 1


def _pad_numeric(correct, seen, ds, rng):
    step = max(1, round(abs(correct) * 0.1))
    k = 1
    while len(ds) < 4 and k < 80:
        sgn = 1 if k % 2 else -1
        c = correct + sgn * ((k + 1) // 2) * step
        if c >= 0 and str(c) not in seen:
            seen.add(str(c))
            ds.append(str(c))
        k += 1


def mk(bab, lv, stem, correct, dis, exp, trick, rng: random.Random, *, id=None,
       svg="", waktu=45) -> Q:
    """Bangun soal 5 opsi. `correct` dan `dis` boleh angka atau teks."""
    cs = str(correct)
    seen = {cs}
    ds = []
    for d in dis:
        if isinstance(d, (int, float)):
            if d != d or d in (float("inf"), float("-inf")):
                continue
            if isinstance(correct, (int, float)) and correct >= 0 and d < 0:
                continue
            if isinstance(d, float) and d.is_integer():
                d = int(d)
        s = str(d)
        if s not in seen:
            seen.add(s)
            ds.append(s)
    if isinstance(correct, int):
        _pad_numeric(correct, seen, ds, rng)
    elif isinstance(correct, str) and len(ds) < 4:
        _pad_text(cs, seen, ds)
    if len(ds) < 4:
        raise ValueError(f"Kurang distraktor untuk soal: {stem[:60]} / {cs} / {ds}")
    opts = [cs] + ds[:4]
    rng.shuffle(opts)
    qid = id or f"{bab[:3]}-{lv}-{rng.randrange(10**9):09d}"
    return Q(qid, bab, lv, stem, opts, opts.index(cs), exp, trick, svg=svg, waktu=waktu)


def mk_svg_opts(bab, lv, stem, opt_svgs, ans, exp, trick, rng, *, id=None, svg="", waktu=60) -> Q:
    """Soal dengan opsi berupa gambar. `opt_svgs[ans]` adalah jawaban benar."""
    order = list(range(len(opt_svgs)))
    rng.shuffle(order)
    shuffled = [opt_svgs[i] for i in order]
    new_ans = order.index(ans)
    qid = id or f"{bab[:3]}-{lv}-{rng.randrange(10**9):09d}"
    return Q(qid, bab, lv, stem, [LABEL[i] for i in range(len(opt_svgs))], new_ans, exp, trick,
             svg=svg, opt_svgs=shuffled, waktu=waktu)
