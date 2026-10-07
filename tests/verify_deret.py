"""Verifikasi mandiri soal deret angka: jawaban harus diprediksi oleh minimal satu pengenal pola yang
berdiri sendiri (bukan kode generator), dan tidak boleh ada pengenal lain yang memprediksi angka berbeda."""
import itertools
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from upkp import numerik_b  # noqa: F401,E402
from upkp.registry import generate  # noqa: E402

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


def selisih(s):
    return [s[i + 1] - s[i] for i in range(len(s) - 1)]


def pola_beda_tetap(s, k):
    d = s
    for _ in range(k):
        d = selisih(d)
        if len(d) < 2:
            return None
    if len(set(d)) != 1:
        return None
    # ekstrapolasi
    ext = d[-1]
    seqs = [s]
    cur = s
    levels = [s]
    for _ in range(k):
        cur = selisih(cur)
        levels.append(cur)
    val = levels[-1][-1]
    for lvl in range(k - 1, -1, -1):
        val = levels[lvl][-1] + val
    return val


def pengenal(s):
    hasil = {}
    for k in (1, 2, 3):
        p = pola_beda_tetap(s, k)
        if p is not None:
            hasil[f"beda{k}"] = p
    if s[0] and all(s[i + 1] * s[0] == s[i] * s[1] for i in range(len(s) - 1)) and s[0] != 0 and (s[1] * s[-1]) % s[0] == 0:
        hasil["geo"] = s[-1] * s[1] // s[0]
    if len(s) >= 4 and all(s[i + 2] == s[i + 1] + s[i] for i in range(len(s) - 2)):
        hasil["fib"] = s[-1] + s[-2]
    if len(s) >= 5 and all(s[i + 3] == s[i + 2] + s[i + 1] + s[i] for i in range(len(s) - 3)):
        hasil["trib"] = s[-1] + s[-2] + s[-3]
    # larik: dua deret bergantian, masing-masing aritmatika
    if len(s) >= 6:
        for kind in ("ar", "geo"):
            ev, od = s[0::2], s[1::2]
            def ok(x):
                if kind == "ar":
                    return len(x) >= 3 and len(set(selisih(x))) == 1
                return len(x) >= 3 and x[0] and all(x[i + 1] * x[0] == x[i] * x[1] for i in range(len(x) - 1))
            if ok(ev) and ok(od):
                tgt = ev if len(s) % 2 == 0 else od
                if kind == "ar":
                    hasil[f"larik_{kind}"] = tgt[-1] + (tgt[1] - tgt[0])
                elif (tgt[1] * tgt[-1]) % tgt[0] == 0:
                    hasil[f"larik_{kind}"] = tgt[-1] * tgt[1] // tgt[0]
        # larik campuran: satu aritmatika, satu geometri
        ev, od = s[0::2], s[1::2]
        for a, b in ((ev, od), (od, ev)):
            pass
    # siklus operasi berulang (panjang 2 atau 3), operasi dari himpunan kecil
    ops = [("+", k) for k in range(1, 10)] + [("-", k) for k in range(1, 10)] + [("*", k) for k in range(2, 5)]
    def terap(o, x):
        return x + o[1] if o[0] == "+" else (x - o[1] if o[0] == "-" else x * o[1])
    for L in (2, 3):
        for cyc in itertools.product(ops, repeat=L):
            if all(terap(cyc[i % L], s[i]) == s[i + 1] for i in range(len(s) - 1)):
                hasil[f"siklus{L}"] = terap(cyc[(len(s) - 1) % L], s[-1])
                break
    # rekurens t_{n+1} = a*t_n + b*n + c  (n mulai dari 1)
    for a in range(1, 5):
        for b in range(-3, 4):
            for c in range(-3, 4):
                if all(s[n] == a * s[n - 1] + b * n + c for n in range(1, len(s))):
                    hasil["rekurens"] = a * s[-1] + b * len(s) + c
    # faktorial/pengali naik: rasio berurutan membentuk deret aritmatika
    if all(x != 0 for x in s[:-1]) and all(s[i + 1] % s[i] == 0 for i in range(len(s) - 1)):
        r = [s[i + 1] // s[i] for i in range(len(s) - 1)]
        if len(r) >= 3 and len(set(selisih(r))) == 1:
            hasil["pengali_naik"] = s[-1] * (r[-1] + (r[1] - r[0]))
    # selisih berlipat (selisih membentuk deret geometri)
    d = selisih(s)
    if len(d) >= 3 and d[0] and all(d[i + 1] * d[0] == d[i] * d[1] for i in range(len(d) - 1)) and (d[1] * d[-1]) % d[0] == 0:
        hasil["selisih_geo"] = s[-1] + d[-1] * d[1] // d[0]
    # prima
    for st in range(len(PRIMES) - len(s) - 1):
        if PRIMES[st:st + len(s)] == s:
            hasil["prima"] = PRIMES[st + len(s)]
    return hasil


def run_all(n=400):
    gagal, ambigu, dicek = [], [], 0
    for lv in (1, 2, 3):
        for i in range(n):
            q = generate("deret", lv, random.Random(i * 7 + lv))
            m = re.match(r"Lanjutkan deret berikut: \*\*([\d, ]+), …\*\*", q.stem)
            if not m:
                continue
            s = [int(x) for x in m[1].split(", ")]
            ans = int(q.opts[q.ans])
            pr = pengenal(s)
            dicek += 1
            kuat = {k: v for k, v in pr.items() if k not in ("siklus2", "siklus3", "rekurens", "pengali_naik")}
            if ans not in pr.values():
                gagal.append((lv, s, ans, pr))
            elif any(v != ans for v in kuat.values()):
                ambigu.append((lv, s, ans, pr))
    return dicek, gagal, ambigu


if __name__ == "__main__":
    dicek, gagal, ambigu = run_all()
    print("dicek:", dicek, "| tidak dikenali:", len(gagal), "| ambigu:", len(ambigu))
    for g in gagal[:8]:
        print("TIDAK DIKENALI", g)
    for g in ambigu[:8]:
        print("AMBIGU", g)
