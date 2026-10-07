"""Registri generator soal per bab."""
from __future__ import annotations

import random

from .model import LEVEL_PENGALI, Q

GENS: dict = {}

WAKTU_DASAR = {
    "padanan": 20, "kelompok": 25, "silogisme": 45, "analisis": 70,
    "operasi": 50, "persamaan": 60, "geometri": 60, "aritsos": 60, "sudut": 55,
    "banding": 60, "jarak": 65, "peluang": 55, "statistika": 70, "deret": 40,
    "deretfig": 45, "analogifig": 60,
    "etika": 30, "wawasan": 30, "nilai": 30, "kepegawaian": 35, "keuangan": 35, "struktur": 30,
    "pemahaman": 45, "numlogic": 40, "blockpattern": 60,
}


def waktu_target(bab: str, lv: int) -> int:
    return round(WAKTU_DASAR.get(bab, 45) * LEVEL_PENGALI.get(lv, 1.0))


def reg(bab: str, levels=(1, 2, 3)):
    def deco(f):
        GENS.setdefault(bab, []).append((f, tuple(levels)))
        return f
    return deco


def ada_generator(bab: str, lv: int) -> bool:
    return any(lv in lvs for _, lvs in GENS.get(bab, []))


def generate(bab: str, lv: int, rng: random.Random) -> Q:
    cands = [f for f, lvs in GENS.get(bab, []) if lv in lvs]
    if not cands:
        raise KeyError(f"Tidak ada generator untuk {bab} tingkat {lv}")
    q = rng.choice(cands)(lv, rng)
    q.waktu = waktu_target(bab, lv)
    return q
