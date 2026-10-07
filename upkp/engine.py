"""Mesin pembuat soal: latihan per bab, try out, penilaian."""
from __future__ import annotations

import random
import time

from . import content_psikologi, content_tskkwk, content_verbal, figural, gen_fakta, numerik_a, numerik_b  # noqa: F401  (mendaftarkan generator)
from .curriculum import BAB_BY_KODE, bab_di
from .model import LEVEL_NAMA, Q
from .registry import GENS, ada_generator, generate
from .skill_catalog import tag_question


def level_tersedia(kode: str) -> list[int]:
    return [lv for lv in (1, 2, 3) if ada_generator(kode, lv)]


def bangun(kode: str, n: int, lv: int, rng: random.Random, hindari: set | None = None) -> list[Q]:
    """Bangun n soal untuk satu bab. lv=0 berarti campur (lebih banyak menengah)."""
    hindari = set(hindari or ())
    hasil: list[Q] = []
    tersedia = level_tersedia(kode)
    if not tersedia:
        return hasil
    percobaan = 0
    while len(hasil) < n and percobaan < n * 60:
        percobaan += 1
        if lv:
            tingkat = lv if lv in tersedia else min(tersedia, key=lambda x: abs(x - lv))
        else:
            tingkat = rng.choice([t for t in [1, 2, 2, 3] if t in tersedia] or tersedia)
        q = generate(kode, tingkat, rng)
        if q.id in hindari:
            continue
        hindari.add(q.id)
        hasil.append(tag_question(q))
    return hasil


# Try out: (kode bab, jumlah soal, tingkat; 0 = campur)
TRYOUT_POTENSI = [
    ("padanan", 4), ("kelompok", 2), ("silogisme", 2), ("analisis", 2),
    ("operasi", 2), ("persamaan", 2), ("geometri", 2), ("aritsos", 2), ("sudut", 1), ("banding", 1),
    ("jarak", 2), ("peluang", 2), ("statistika", 1), ("deret", 2),
    ("deretfig", 2), ("analogifig", 1),
]
TRYOUT_TSKKWK = [("etika", 3), ("wawasan", 3), ("nilai", 4), ("kepegawaian", 4), ("keuangan", 3), ("struktur", 3)]

PAKET = {
    "potensi": {"nama": "Try Out Tes Potensi (Verbal, Numerikal, Figural)", "rencana": TRYOUT_POTENSI, "menit": 40},
    "tskkwk": {"nama": "Try Out TSKKWK", "rencana": TRYOUT_TSKKWK, "menit": 20},
}


def bangun_tryout(paket: str, lv: int, rng: random.Random) -> list[Q]:
    soal: list[Q] = []
    pakai: set = set()
    for kode, n in PAKET[paket]["rencana"]:
        soal.extend(bangun(kode, n, lv, rng, pakai))
        pakai.update(q.id for q in soal)
    return soal


def nilai(soal: list[Q], jawab: dict[int, int], ms: dict[int, int]):
    """Hitung hasil. jawab: indeks soal → indeks opsi."""
    benar = sum(1 for i, q in enumerate(soal) if jawab.get(i) == q.ans)
    terisi = sum(1 for i in range(len(soal)) if i in jawab)
    total_ms = sum(ms.values())
    return {"benar": benar, "terisi": terisi, "n": len(soal), "ms": total_ms}


def nama_level(lv: int) -> str:
    return LEVEL_NAMA.get(lv, "Campur")
