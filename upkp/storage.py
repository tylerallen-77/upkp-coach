"""Penyimpanan kemajuan belajar (file JSON lokal) beserta ekspor/impor."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

DATA_DIR = Path(os.environ.get("UPKP_DATA_DIR", Path(__file__).resolve().parent.parent / "data"))
FILE = DATA_DIR / "progress.json"
VERSI = 1


def kosong() -> dict:
    return {"versi": VERSI, "stat": {}, "salah": {}, "riwayat": [], "dibuat": time.time()}


def muat() -> dict:
    try:
        d = json.loads(FILE.read_text(encoding="utf-8"))
        if d.get("versi") == VERSI:
            for k, v in kosong().items():
                d.setdefault(k, v)
            return d
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return kosong()


def simpan(d: dict) -> None:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        tmp = FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        tmp.replace(FILE)
    except OSError:
        pass  # penyimpanan gagal tidak boleh merusak sesi belajar


def ekspor(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False, indent=1)


def impor(teks: str) -> dict:
    d = json.loads(teks)
    if not isinstance(d, dict) or d.get("versi") != VERSI:
        raise ValueError("Berkas bukan hasil ekspor aplikasi ini (versi tidak cocok).")
    for k, v in kosong().items():
        d.setdefault(k, v)
    return d


def catat(d: dict, q: dict, benar: bool, ms: int) -> None:
    """Catat satu jawaban. `q` adalah dict soal (Q.to_dict())."""
    bab = q["bab"]
    s = d["stat"].setdefault(bab, {"n": 0, "ok": 0, "ms": 0, "tg": 0, "lv": {}})
    s["n"] += 1
    s["ok"] += 1 if benar else 0
    s["ms"] += min(int(ms), 180000)
    s["tg"] += q.get("waktu", 45) * 1000
    lv = s["lv"].setdefault(str(q["lv"]), {"n": 0, "ok": 0})
    lv["n"] += 1
    lv["ok"] += 1 if benar else 0
    if not benar:
        d["salah"][q["id"]] = q
    else:
        d["salah"].pop(q["id"], None)
        # soal dari bank salah yang dijawab benar keluar dari bank (id sama)


def catat_sesi(d: dict, judul: str, n: int, ok: int, rata_dtk: int) -> None:
    d["riwayat"].insert(0, {"t": time.time(), "judul": judul, "n": n, "ok": ok, "rata": rata_dtk})
    del d["riwayat"][50:]
