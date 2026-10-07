"""Generator soal Numerikal bagian 1: operasi bilangan, persamaan, geometri, aritmatika sosial, sudut-himpunan."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from .model import dc, mk, rp
from .registry import reg


def hm(menit: int) -> str:
    return f"{menit // 60:02d}.{menit % 60:02d}"


def lcm(a, b):
    return a * b // math.gcd(a, b)


# =====================================================================
# 1. OPERASI BILANGAN
# =====================================================================
@reg("operasi")
def op_kpk_lampu(lv, rng):
    if lv == 1:
        a, b = rng.choice([(4, 6), (6, 9), (8, 12), (10, 15), (6, 8)])
        sets = [a, b]
    else:
        sets = list(rng.choice([(4, 6, 10), (6, 8, 12), (5, 10, 15), (8, 12, 18), (6, 9, 12), (9, 12, 15)]))
    L = 1
    for x in sets:
        L = lcm(L, x)
    mulai = 7 * 60 + rng.choice([0, 15, 30, 45])
    kali = 1 if lv < 3 else 2
    jawab = mulai + L * kali
    nama = ["merah", "kuning", "hijau"][: len(sets)]
    kal = ", ".join(f"lampu {n} menyala tiap {x} menit" for n, x in zip(nama, sets))
    stem = (f"Di sebuah taman, {kal}. Pukul {hm(mulai)} semua lampu menyala bersamaan. "
            f"Pukul berapa semua lampu menyala bersamaan untuk {'pertama kali' if kali == 1 else 'kedua kalinya'} setelah itu?")
    dis = [hm(mulai + L // 2), hm(mulai + L * (kali + 1)), hm(mulai + sum(sets)), hm(mulai + max(sets) * kali)]
    exp = (f"Waktu menyala bersamaan berulang tiap KPK dari {', '.join(map(str, sets))} = {L} menit. "
           f"{kali} × {L} = {kali * L} menit. {hm(mulai)} + {kali * L} menit = {hm(jawab)}.")
    trick = "Siklus berulang bersamaan = KPK. Faktorkan: ambil tiap faktor prima dengan pangkat tertinggi. Jangan menjumlah atau merata-ratakan siklus."
    return mk("operasi", lv, stem, hm(jawab), dis, exp, trick, rng)


@reg("operasi")
def op_fpb_kpk(lv, rng):
    if lv == 1:
        g = rng.choice([4, 6, 7, 8, 12])
        a, b = g * rng.choice([2, 3, 4, 5]), g * rng.choice([5, 6, 7, 9])
        while a == b:
            b += g
        r = math.gcd(a, b)
        return mk("operasi", lv, f"FPB dari {a} dan {b} adalah …", r, [r * 2, r // 2 if r > 1 else r + 3, lcm(a, b), r + 2],
                  f"Faktorkan: FPB = faktor prima yang sama dengan pangkat terkecil. FPB({a}, {b}) = {r}.",
                  "FPB: bagi kedua bilangan dengan bilangan yang sama sampai tidak bisa lagi, lalu kalikan pembaginya.", rng)
    if lv == 2:
        g = rng.choice([6, 8, 12, 14])
        a, b = g * rng.choice([3, 4, 5]), g * rng.choice([6, 7, 8])
        r = math.gcd(a, b)
        return mk("operasi", lv, f"Seorang pegawai membagi {a} buku tulis dan {b} pulpen menjadi paket-paket yang isinya sama banyak, tanpa sisa. "
                  f"Banyak paket paling banyak yang bisa dibuat adalah …", r, [r * 2, a // r + b // r, lcm(a, b) // 10, r + 2],
                  f"Jumlah paket terbanyak = FPB({a}, {b}) = {r}. Tiap paket berisi {a // r} buku dan {b // r} pulpen.",
                  "“Paling banyak paket yang sama rata” = FPB. “Kejadian berulang bersamaan” = KPK.", rng)
    kpk, fpb = rng.choice([(36, 6), (48, 8), (72, 12), (60, 5)])
    a = fpb * rng.choice([2, 3])
    other = kpk * fpb // a
    return mk("operasi", lv, f"KPK dua bilangan adalah {kpk} dan FPB-nya {fpb}. Jika salah satu bilangan itu {a}, bilangan yang lain adalah …",
              other, [kpk // a, kpk, a * fpb, other + fpb],
              f"Hasil kali dua bilangan = KPK × FPB. {a} × x = {kpk} × {fpb} = {kpk * fpb}, sehingga x = {other}.",
              "Rumus pintas: a × b = KPK × FPB. Cukup satu pembagian.", rng)


@reg("operasi")
def op_habis_dibagi(lv, rng):
    ks = {1: [3, 9], 2: [4, 6, 8], 3: [7, 11, 12]}[lv]
    k = rng.choice(ks)
    rule = {
        3: "habis dibagi 3 jika jumlah digitnya habis dibagi 3",
        9: "habis dibagi 9 jika jumlah digitnya habis dibagi 9",
        4: "habis dibagi 4 jika dua digit terakhir habis dibagi 4",
        8: "habis dibagi 8 jika tiga digit terakhir habis dibagi 8",
        6: "habis dibagi 6 jika genap dan jumlah digitnya habis dibagi 3",
        7: "habis dibagi 7: kurangi (2 × digit satuan) dari bilangan di depannya, ulangi, hasil kelipatan 7",
        11: "habis dibagi 11: selisih jumlah digit posisi ganjil dan genap adalah 0 atau kelipatan 11",
        12: "habis dibagi 12 jika habis dibagi 3 dan 4",
    }[k]
    while True:
        nums = [rng.randint(1000, 99999) for _ in range(5)]
        ok = [n for n in nums if n % k == 0]
        if not ok:
            nums[0] = k * rng.randint(1000 // k + 1, 99999 // k)
            ok = [nums[0]]
        if len(ok) == 1 and len(set(nums)) == 5:
            break
    rng.shuffle(nums)
    jawab = ok[0]
    fmt = lambda n: str(n)
    exp = f"Aturan: bilangan {rule}. Yang memenuhi hanya {jawab} (sisa bagi 0), sedangkan lainnya bersisa."
    return mk("operasi", lv, f"Manakah bilangan berikut yang habis dibagi {k}?", fmt(jawab), [fmt(n) for n in nums if n != jawab],
              exp, f"Jangan dibagi panjang. Pakai aturan: {rule}.", rng)


@reg("operasi")
def op_eksponen_akar(lv, rng):
    if lv == 1:
        a = rng.choice([2, 3, 5])
        m, n, p = rng.randint(3, 6), rng.randint(2, 5), rng.randint(1, 3)
        ans = a ** (m + n - p)
        return mk("operasi", lv, f"Nilai dari ({a}^{m} × {a}^{n}) ÷ {a}^{p} adalah …", ans,
                  [a ** (m + n + p), a ** (m * n - p), a ** (m + n) // 1, a ** (m - n + p)],
                  f"Pangkat dijumlah saat dikali dan dikurang saat dibagi: {a}^({m}+{n}−{p}) = {a}^{m + n - p} = {ans}.",
                  "Basis sama: kali → jumlahkan pangkat, bagi → kurangkan pangkat. Hitung nilainya di akhir.", rng)
    if lv == 2:
        c, d = rng.choice([(3, 2), (5, 3), (2, 7), (4, 5)])
        e = rng.randint(2, 6)
        s = (c + e)
        ans = f"{s}√{d}"
        return mk("operasi", lv, f"Bentuk sederhana dari {c}√{d} + {e}√{d} adalah …", ans,
                  [f"{c * e}√{d}", f"{s}√{d * 2}", f"√{d * s}", f"{s + 1}√{d}", f"{s - 1}√{d}", f"{s + 2}√{d}"],
                  f"Akar sejenis (√{d}) dijumlah koefisiennya: ({c} + {e})√{d} = {s}√{d}.",
                  "Akar sejenis boleh dijumlah/dikurang koefisiennya. Akar tak sejenis dibiarkan.", rng)
    k, root = rng.choice([(36, 6), (49, 7), (25, 5), (64, 8)])
    n = rng.choice([2, 3, 5])
    v = k * n
    ans = f"{root}√{n}"
    return mk("operasi", lv, f"Bentuk paling sederhana dari √{v} adalah …", ans,
              [f"{n}√{k}", f"{root + 1}√{n}", f"√{v - 1}", f"{root * 2}√{n}"],
              f"{v} = {k} × {n} dan {k} adalah kuadrat sempurna ({root}²). Maka √{v} = {root}√{n}.",
              "Cari faktor kuadrat sempurna terbesar (4, 9, 16, 25, 36, 49, 64), keluarkan akarnya.", rng)


@reg("operasi", (2, 3))
def op_urut_pecahan(lv, rng):
    while True:
        vals = []
        forms = []
        for _ in range(5):
            kind = rng.choice(["frac", "dec", "pct"] if lv == 3 else ["frac", "dec"])
            if kind == "frac":
                d = rng.choice([2, 3, 4, 5, 6, 8, 10])
                nn = rng.randint(1, d - 1)
                v = Fraction(nn, d)
                forms.append(f"{nn}/{d}")
            elif kind == "dec":
                x = rng.randint(1, 9) / 10 + rng.choice([0, 0.05])
                v = Fraction(str(round(x, 2)))
                forms.append(dc(round(x, 2)))
            else:
                p = rng.choice([15, 25, 35, 45, 60, 75, 85])
                v = Fraction(p, 100)
                forms.append(f"{p}%")
            vals.append(v)
        if len(set(vals)) == 5:
            break
    mode = rng.choice(["terkecil", "terbesar"])
    target = min(vals) if mode == "terkecil" else max(vals)
    idx = vals.index(target)
    ans = forms[idx]
    exp = "Samakan bentuknya ke desimal: " + "; ".join(f"{f} = {dc(round(float(v), 3))}" for f, v in zip(forms, vals)) + f". Yang {mode} adalah {ans}."
    return mk("operasi", lv, f"Manakah bilangan yang nilainya {mode}?", ans, [f for i, f in enumerate(forms) if i != idx], exp,
              "Ubah semua ke desimal (1/4 = 0,25; 1/8 = 0,125; 3/8 = 0,375) lalu bandingkan. Hafal tabel pecahan dasar.", rng)


# =====================================================================
# 2. PERSAMAAN DAN PERTIDAKSAMAAN
# =====================================================================
def _det2(a, b, c, d):
    return a * d - b * c


@reg("persamaan")
def pers_spldv(lv, rng):
    if lv <= 2:
        while True:
            x, y = rng.randint(2, 20) * 100, rng.randint(2, 20) * 100
            a, b, c, d = rng.randint(2, 5), rng.randint(2, 5), rng.randint(2, 5), rng.randint(2, 5)
            if _det2(a, b, c, d) != 0 and a != c:
                break
        e1, e2 = a * x + b * y, c * x + d * y
        item = rng.choice([("bungkus mi instan", "kaleng susu"), ("buah apel", "buah jeruk"), ("buku tulis", "pulpen")])
        stem = (f"Ibu A membeli {a} {item[0]} dan {b} {item[1]} seharga {rp(e1)}. Ibu B membeli {c} {item[0]} dan {d} {item[1]} seharga {rp(e2)}. "
                f"Harga satu {item[0]} adalah …")
        ans = rp(x)
        dis = [rp(y), rp(x + 100), rp(x - 100), rp(e1 // (a + b))]
        k = _det2(a, b, c, d)
        exp = (f"Misal {item[0]} = x dan {item[1]} = y. Persamaan: {a}x + {b}y = {e1} dan {c}x + {d}y = {e2}. "
               f"Eliminasi y: kalikan persamaan 1 dengan {d} dan persamaan 2 dengan {b}, lalu kurangkan: {k}x = {d * e1 - b * e2}, sehingga x = {x}.")
        trick = "Eliminasi satu variabel dengan menyamakan koefisien (kali silang), lalu substitusi. Cek jawaban ke salah satu persamaan."
        return mk("persamaan", lv, stem, ans, dis, exp, trick, rng)
    while True:
        M, J, A = (rng.randint(2, 9) * 5000 for _ in range(3))
        c1 = (2, 2, 1)
        c2 = (1, 2, 2)
        c3 = (2, 2, 3)
        if len({M, J, A}) == 3:
            break
    e = [c[0] * M + c[1] * J + c[2] * A for c in (c1, c2, c3)]
    stem = (f"Harga 2 kg mangga, 2 kg jeruk, dan 1 kg anggur adalah {rp(e[0])}. Harga 1 kg mangga, 2 kg jeruk, dan 2 kg anggur adalah {rp(e[1])}. "
            f"Harga 2 kg mangga, 2 kg jeruk, dan 3 kg anggur adalah {rp(e[2])}. Harga 1 kg jeruk adalah …")
    exp = (f"Persamaan 3 − persamaan 1: 2A = {e[2] - e[0]}, jadi A = {A}. Persamaan 1 − persamaan 2: M − A = {e[0] - e[1]}, jadi M = {M}. "
           f"Substitusi ke persamaan 1: 2·{M} + 2J + {A} = {e[0]}, sehingga J = {J}.")
    return mk("persamaan", lv, stem, rp(J), [rp(M), rp(A), rp(J + 5000), rp(J - 5000)], exp,
              "Cari dua persamaan yang bedanya hanya satu variabel (persamaan 3 dan 1 hanya beda anggur). Kurangkan, variabel itu langsung ketemu.", rng)


@reg("persamaan")
def pers_kuadrat(lv, rng):
    r1, r2 = rng.sample(range(-6, 9), 2)
    while r1 == 0 or r2 == 0 or r1 + r2 == 0:
        r1, r2 = rng.sample(range(-6, 9), 2)
    S, P = r1 + r2, r1 * r2

    def eq(s, p):
        t1 = "x²"
        t2 = "" if s == 0 else (f" − {s}x" if s > 0 else f" + {-s}x")
        t3 = "" if p == 0 else (f" + {p}" if p > 0 else f" − {-p}")
        return f"{t1}{t2}{t3} = 0"
    if lv == 1:
        mode = rng.choice(["jumlah", "hasil kali"])
        ans = S if mode == "jumlah" else P
        wr = P if mode == "jumlah" else S
        return mk("persamaan", lv, f"Jika x₁ dan x₂ adalah akar-akar persamaan {eq(S, P)}, maka {mode} akar-akarnya adalah …", ans,
                  [wr, -ans, ans + 2, ans - 2],
                  f"Untuk x² + bx + c = 0: x₁ + x₂ = −b dan x₁·x₂ = c. Di sini jumlah = {S} dan hasil kali = {P}.",
                  "Tidak perlu mencari akarnya. Jumlah = −b/a, hasil kali = c/a.", rng)
    if lv == 2:
        ans = S * S - 2 * P
        return mk("persamaan", lv, f"Jika x₁ dan x₂ akar-akar persamaan {eq(S, P)}, nilai x₁² + x₂² adalah …", ans,
                  [S * S, S * S + 2 * P, P * P, S * S - P],
                  f"x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂ = {S}² − 2({P}) = {S * S} − ({2 * P}) = {ans}.",
                  "Bentuk simetris akar selalu diubah ke jumlah dan hasil kali: x₁² + x₂² = (x₁+x₂)² − 2x₁x₂.", rng)
    ns, np_ = 2 * S, 4 * P
    ans = eq(ns, np_)
    dis = [eq(S, 2 * P), eq(ns, 2 * P), eq(-ns, np_), eq(ns, P), eq(S, np_), eq(ns, 2 * np_)]
    return mk("persamaan", lv, f"Akar-akar persamaan {eq(S, P)} adalah x₁ dan x₂. Persamaan kuadrat baru yang akar-akarnya 2x₁ dan 2x₂ adalah …", ans, dis,
              f"Jumlah baru = 2(x₁+x₂) = {ns}. Hasil kali baru = 4·x₁x₂ = {np_}. Persamaan baru: x² − ({ns})x + ({np_}) = 0.",
              "Akar dikali k: jumlah dikali k, hasil kali dikali k². Susun x² − (jumlah)x + (hasil kali) = 0.", rng)


@reg("persamaan")
def pers_pertidaksamaan(lv, rng):
    if lv == 1:
        a, c = rng.randint(2, 6), rng.randint(1, 5)
        while a <= c:
            a += 1
        b, d = rng.randint(-8, 8), rng.randint(-8, 8)
        k = Fraction(d - b, a - c)
        ans = f"x > {k}" if k.denominator == 1 else f"x > {k.numerator}/{k.denominator}"
        def f(t):
            return f"x > {t}"
        stem = f"Himpunan penyelesaian dari {a}x {'+' if b >= 0 else '−'} {abs(b)} > {c}x {'+' if d >= 0 else '−'} {abs(d)} adalah …"
        kk = int(k) if k.denominator == 1 else None
        if kk is None:
            return pers_pertidaksamaan(lv, rng)
        return mk("persamaan", lv, stem, f(kk), [f"x < {kk}", f"x > {-kk}", f"x < {-kk}", f"x > {kk + 1}"],
                  f"Pindahkan suku x ke kiri dan konstanta ke kanan: ({a} − {c})x > {d} − ({b}), sehingga x > {kk}.",
                  "Pindah ruas = ganti tanda. Tanda pertidaksamaan hanya berbalik jika dikali atau dibagi bilangan negatif.", rng)
    if lv == 2:
        return _ineq_neg(lv, rng)
    p, q = sorted(rng.sample(range(-6, 9), 2))
    if q - p < 3:
        q = p + 4
    jml = q - p - 1
    ans = f"{p} < x < {q}"
    stem = f"Pertidaksamaan (x − ({p}))(x − {q}) < 0 mempunyai himpunan penyelesaian …"
    return mk("persamaan", lv, stem, ans, [f"x < {p} atau x > {q}", f"{q} < x < {p}", f"x < {p}", f"x > {q}"],
              f"Pembuat nol: x = {p} dan x = {q}. Tanda “<” (negatif) berada di antara kedua akar: {p} < x < {q}.",
              "Kuadrat positif (a > 0): “<” → di antara akar; “>” → di luar akar. Gambar garis bilangan.", rng)


def _ineq_neg(lv, rng):
    a = rng.randint(2, 5)
    k = rng.randint(2, 9)
    b = rng.randint(1, 9)
    c = -a * k + b
    ans = f"x < {k}"
    stem = f"Himpunan penyelesaian dari −{a}x + {b} > {c} adalah …"
    return mk("persamaan", lv, stem, ans, [f"x > {k}", f"x < {-k}", f"x > {-k}", f"x < {k + 1}"],
              f"−{a}x > {c} − {b} = {c - b}. Dibagi −{a} (negatif) tanda berbalik: x < {k}.",
              "Dibagi atau dikali bilangan negatif → tanda pertidaksamaan berbalik. Ini jebakan paling sering.", rng)


# =====================================================================
# 3. GEOMETRI
# =====================================================================
@reg("geometri")
def geo_persegi_panjang(lv, rng):
    if lv == 1:
        p = rng.randint(30, 90)
        l = rng.randint(20, 60)
        K = 2 * (p + l)
        return mk("geometri", lv, f"Sebuah papan tulis berbentuk persegi panjang dengan keliling {K} cm. Jika panjang salah satu sisinya {p} cm, luasnya adalah … cm².",
                  p * l, [p * (K // 2), (K // 2 - p) * 2 * p // 1, p * p, p * l + p], f"Setengah keliling = {K // 2}, jadi sisi lainnya = {K // 2} − {p} = {l}. Luas = {p} × {l} = {p * l} cm².",
                  "Keliling = 2(p + l) → p + l = K ÷ 2. Cari sisi lain dulu, baru kalikan.", rng)
    if lv == 2:
        l = rng.randint(6, 14)
        k = rng.choice([2, 3])
        p = l * k
        L = p * l
        return mk("geometri", lv, f"Panjang sebuah persegi panjang {k} kali lebarnya dan luasnya {L} cm². Keliling persegi panjang itu adalah … cm.",
                  2 * (p + l), [p + l, 2 * p * l, 2 * (p + l) + 2, 4 * p],
                  f"Misal lebar = l, maka {k}l × l = {L} → l² = {L // k} → l = {l}. Panjang = {p}. Keliling = 2({p} + {l}) = {2 * (p + l)}.",
                  "Soal “k kali”: misalkan lebar l, panjang kl. Luas jadi kl², selesaikan akarnya.", rng)
    a, w = rng.randint(20, 40), rng.randint(2, 4)
    L = (a + 2 * w) ** 2 - a * a
    return mk("geometri", lv, f"Sebuah kolam persegi dengan sisi {a} m dikelilingi jalan setapak selebar {w} m di semua sisinya. Luas jalan setapak adalah … m².",
              L, [4 * a * w, (a + w) ** 2 - a * a, 4 * w * w, L + 2 * w],
              f"Luas total = ({a} + 2·{w})² = {(a + 2 * w) ** 2}. Luas kolam = {a * a}. Selisih = {L} m².",
              "Luas bingkai = luas besar − luas dalam. Jangan menjumlah 4 persegi panjang kecuali sudut dihitung.", rng)


@reg("geometri")
def geo_lingkaran(lv, rng):
    r = rng.choice([7, 14, 21, 28, 35])
    if lv == 1:
        n = rng.randint(3, 6)
        K = 2 * 22 * r // 7
        return mk("geometri", lv, f"Fahmi berlari mengitari lapangan berbentuk lingkaran sebanyak {n} kali putaran. Jika jari-jari lapangan {r} m, Fahmi berlari sejauh … m (π = 22/7).",
                  n * K, [n * K // 2, n * K * 2, n * r * r * 22 // 7, n * K + K],
                  f"Keliling = 2πr = 2 × 22/7 × {r} = {K} m. {n} putaran = {n} × {K} = {n * K} m.", "Pilih r kelipatan 7 saat π = 22/7: bagi 7 dulu. Keliling = 2πr, bukan πr².", rng)
    if lv == 2:
        n = rng.randint(100, 500)
        d = 2 * r
        K = 22 * d // 7
        jarak = n * K
        return mk("geometri", lv, f"Roda sepeda berdiameter {d} cm berputar sebanyak {n} kali. Jarak yang ditempuh sepeda adalah … cm (π = 22/7).",
                  jarak, [n * K // 2, n * d, jarak * 2, jarak + K], f"Satu putaran = keliling = πd = 22/7 × {d} = {K} cm. {n} putaran = {jarak} cm.",
                  "Satu putaran roda = satu keliling = πd. Jarak = banyak putaran × keliling.", rng)
    V = 22 * r * r * 10 // 7
    tinggi = 10
    liter_stem = f"Sebuah tangki berbentuk tabung berisi air setinggi {tinggi} cm dengan volume {V} cm³ (π = 22/7). Jari-jari tangki itu adalah … cm."
    return mk("geometri", lv, liter_stem, r, [r // 2, r * 2, r + 7, 2 * r + 7],
              f"V = πr²t → {V} = 22/7 × r² × {tinggi} → r² = {V} × 7 ÷ ({22} × {tinggi}) = {r * r} → r = {r} cm.",
              "V = πr²t. Kalikan silang 7 dan 22, lalu akarkan. Pilih opsi yang kuadratnya cocok.", rng)


@reg("geometri", (2, 3))
def geo_perubahan(lv, rng):
    if lv == 2:
        t, a = rng.choice([(10, 15), (20, 10), (25, 20), (10, 20)])
        f = Fraction(100 + t, 100) * Fraction(100 - a, 100)
        d = (f - 1) * 100
        ans = f"naik {dc(float(d))}%" if d > 0 else (f"turun {dc(float(-d))}%" if d < 0 else "tetap")
        stem = f"Tinggi sebuah segitiga naik {t}% dan alasnya turun {a}%. Luas segitiga berubah sebesar …"
        w = [f"naik {dc(float(abs(t - a)))}%", f"turun {dc(float(abs(t - a)))}%", f"naik {t}%", f"turun {a}%", "tetap"]
        return mk("geometri", lv, stem, ans, w, f"Luas ∝ alas × tinggi. Faktor = {100 + t}% × {100 - a}% = {dc(float(f * 100))}%, jadi {ans}.",
                  "Perubahan dua dimensi: kalikan faktornya. Jangan menjumlah +10% dan −15%.", rng)
    a, b = rng.choice([(20, 10), (25, 20), (50, 20)])
    f = (Fraction(100 + a, 100) ** 2) * Fraction(100 - b, 100)
    d = (f - 1) * 100
    ans = f"naik {dc(float(d))}%" if d > 0 else f"turun {dc(float(-d))}%"
    return mk("geometri", lv, f"Rusuk sebuah balok dengan alas persegi bertambah {a}% pada kedua sisi alasnya, sedangkan tingginya berkurang {b}%. Volumenya berubah menjadi …",
              ans, [f"naik {a - b}%", f"turun {abs(a - b)}%", "tetap", f"naik {a}%", f"naik {dc(float(d) + 4)}%"],
              f"Volume ∝ p × l × t. Faktor = {1 + a / 100:.2f} × {1 + a / 100:.2f} × {1 - b / 100:.2f} = {float(f):.3f} → {ans}.",
              "Tiap dimensi punya faktor sendiri; kalikan semuanya. Bangun 3 dimensi: tiga faktor.", rng)


@reg("geometri", (2, 3))
def geo_pythagoras(lv, rng):
    if lv == 2:
        a, b, c = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)])
        k = rng.choice([1, 2, 3])
        a, b, c = a * k, b * k, c * k
        return mk("geometri", lv, f"Tangga sepanjang {c} m disandarkan pada dinding. Jarak ujung bawah tangga ke dinding {a} m. Tinggi dinding yang dicapai tangga adalah … m.",
                  b, [a + 1, c - a, c + a, b + 2], f"Pythagoras: t² = {c}² − {a}² = {c * c - a * a} → t = {b} m.",
                  "Hafal tripel: 3-4-5, 5-12-13, 8-15-17, 7-24-25 dan kelipatannya. Kenali, jangan hitung.", rng)
    p, l, t, d = rng.choice([(1, 2, 2, 3), (2, 3, 6, 7), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (2, 10, 11, 15)])
    k = rng.choice([1, 2])
    p, l, t, d = p * k, l * k, t * k, d * k
    return mk("geometri", lv, f"Sebuah balok berukuran {p} cm × {l} cm × {t} cm. Panjang diagonal ruangnya adalah … cm.", d,
              [d + 1, d - 1, p + l + t, int(math.sqrt(p * p + l * l)) + t],
              f"Diagonal ruang = √(p² + l² + t²) = √({p * p} + {l * l} + {t * t}) = √{p * p + l * l + t * t} = {d} cm.",
              "Diagonal ruang balok = √(p²+l²+t²). Kuadrupel yang sering muncul: (1,2,2,3), (2,3,6,7), (4,4,7,9), (2,6,9,11).", rng)


@reg("geometri", (3,))
def geo_kubus_selisih(lv, rng):
    b = rng.randint(4, 12)
    d = rng.choice([2, 3, 4])
    a = b + d
    S = 6 * (a * a - b * b)
    return mk("geometri", lv, f"Dua kubus mempunyai panjang rusuk yang berselisih {d} cm dan luas permukaannya berselisih {S} cm². Panjang rusuk kubus yang lebih besar adalah … cm.",
              a, [b, a + 1, a - 2, (a + b)],
              f"Misal rusuk a dan b. a − b = {d}; 6(a² − b²) = {S} → a² − b² = {S // 6} → (a − b)(a + b) = {S // 6} → a + b = {S // 6 // d}. Maka a = ({S // 6 // d} + {d})/2 = {a}.",
              "Selisih kuadrat: a² − b² = (a − b)(a + b). Dari situ a + b langsung ketemu, lalu jumlah dan selisih memberi a.", rng)


# =====================================================================
# 4. ARITMATIKA SOSIAL DAN BARISAN DAN DERET
# =====================================================================
@reg("aritsos")
def as_bruto_tara(lv, rng):
    bruto = rng.choice([100, 200, 50, 80])
    tara = rng.choice([2, 5, 4])
    neto = bruto * (100 - tara) // 100
    jual = rng.choice([12000, 14000, 15000, 16000])
    beli = rng.randint(7, 11) * 100000
    if lv == 1:
        untung = jual * neto - beli
        stem = f"Seorang pedagang membeli satu karung gula pasir bruto {bruto} kg, tara {tara}%, dengan harga {rp(beli)}. Semua gula dijual Rp{jual:,} per kg (berat neto). Keuntungannya adalah …".replace(",", ".")
        return mk("aritsos", lv, stem, rp(untung), [rp(jual * bruto - beli), rp(untung + jual), rp(untung - jual), rp(beli - jual * neto)],
                  f"Neto = {bruto} − {tara}% × {bruto} = {neto} kg. Hasil jual = {neto} × {jual} = {rp(jual * neto)}. Untung = {rp(jual * neto)} − {rp(beli)} = {rp(untung)}.",
                  "Bruto = tara + neto. Yang dijual dihitung dari NETO, bukan bruto. Untung = hasil jual − harga beli.", rng)
    persen = rng.choice([20, 25, 40])
    modal = rng.randint(2, 9) * 100000
    jualtotal = modal * (100 + persen) // 100
    return mk("aritsos", lv, f"Pedagang membeli barang seharga {rp(modal)} dan menjualnya dengan laba {persen}% dari harga beli. Harga jualnya adalah …",
              rp(jualtotal), [rp(modal + persen * 100), rp(modal * (100 - persen) // 100), rp(jualtotal + 20000), rp(modal * persen // 100)],
              f"Harga jual = {100 + persen}% × {rp(modal)} = {rp(jualtotal)}.", "Laba L% dari harga beli: jual = beli × (1 + L%). Rugi: kali (1 − L%).", rng)


@reg("aritsos", (2, 3))
def as_diskon(lv, rng):
    if lv == 2:
        a, b = rng.choice([(30, 40), (20, 10), (25, 20), (10, 10), (50, 20)])
        H = rng.randint(2, 10) * 100000
        f = (100 - a) * (100 - b) / 100
        return mk("aritsos", lv, f"Sebuah toko memberi diskon {a}% lalu diskon lagi {b}% untuk sebuah baju seharga {rp(H)}. Total potongan harga adalah …",
                  rp(H * (100 - f) / 100), [rp(H * (a + b) / 100), rp(H * a / 100), rp(H * f / 100), rp(H * (100 - f + 5) / 100)],
                  f"Faktor harga = {100 - a}% × {100 - b}% = {f:g}%. Diskon gabungan = {100 - f:g}%. Potongan = {100 - f:g}% × {rp(H)} = {rp(H * (100 - f) / 100)}.",
                  "Diskon bertahap: kalikan faktor sisanya, bukan jumlahkan diskonnya. Diskon gabungan = 100% − (faktor1 × faktor2).", rng)
    D, e, x = rng.choice([(32, 20, 15), (40, 20, 25), (19, 10, 10), (44, 30, 20), (52, 20, 40)])
    stem = (f"Sebuah celana didiskon {D}%. Sebuah baju didiskon x% lalu didiskon lagi {e}%. Jika total diskon baju sama dengan diskon celana, nilai x adalah …")
    return mk("aritsos", lv, stem, x, [D - e, e, x + 5, x - 5], f"Faktor sisa baju = (100 − x)% × {100 - e}% = {100 - D}% → (100 − x)% = {100 - D}/{100 - e} = {(100 - x) / 100:g} → x = {x}.",
              "Samakan faktor sisa: (1 − x)(1 − e) = 1 − D. Cari faktor yang belum diketahui dengan membagi.", rng)


@reg("aritsos", (2, 3))
def as_bunga_tunggal(lv, rng):
    M = rng.randint(2, 20) * 1000000
    p = rng.choice([6, 8, 10, 12])
    n = rng.choice([6, 9, 12, 18])
    bunga = M * p * n // 1200
    if lv == 2:
        return mk("aritsos", lv, f"Ani menabung {rp(M)} dengan bunga tunggal {p}% per tahun. Setelah {n} bulan, jumlah tabungan Ani adalah …", rp(M + bunga),
                  [rp(bunga), rp(M + bunga * 12 // n), rp(M + M * p // 100), rp(M + bunga + M // 100)],
                  f"Bunga = {rp(M)} × {p}% × {n}/12 = {rp(bunga)}. Total = {rp(M + bunga)}.", "Bunga tunggal: M × p% × (bulan/12). Jangan lupa menambahkan modal awal.", rng)
    return mk("aritsos", lv, f"Setelah ditabung {n} bulan dengan bunga tunggal {p}% per tahun, tabungan Budi menjadi {rp(M + bunga)}. Tabungan awal Budi adalah …", rp(M),
              [rp(M + bunga - bunga), rp(M + bunga // 2), rp(M - 1000000), rp(M + 1000000)],
              f"Faktor total = 1 + {p}% × {n}/12 = {1 + p * n / 1200:.3f}. Awal = {rp(M + bunga)} ÷ {1 + p * n / 1200:.3f} = {rp(M)}.",
              "Mundur dari saldo akhir: modal = saldo ÷ (1 + p% × t). Cek dengan menghitung maju.", rng)


@reg("aritsos")
def as_aritmatika(lv, rng):
    a = rng.randint(2, 12)
    b = rng.randint(2, 7)
    if lv == 1:
        n = rng.randint(10, 25)
        return mk("aritsos", lv, f"Suku pertama barisan aritmatika adalah {a} dan bedanya {b}. Suku ke-{n} adalah …", a + (n - 1) * b,
                  [a + n * b, a + (n - 2) * b, a * b * n, a + (n - 1) * b + b], f"Un = a + (n − 1)b = {a} + {n - 1} × {b} = {a + (n - 1) * b}.",
                  "Un = a + (n−1)b. Banyaknya loncatan b adalah n−1, bukan n.", rng)
    if lv == 2:
        n = rng.randint(10, 30)
        S = n * (2 * a + (n - 1) * b) // 2
        return mk("aritsos", lv, f"Jumlah {n} suku pertama deret aritmatika dengan suku pertama {a} dan beda {b} adalah …", S,
                  [S + n, S - n, n * (a + (n - 1) * b), S + a * n], f"Sn = n/2 (2a + (n − 1)b) = {n}/2 × ({2 * a} + {(n - 1) * b}) = {S}.",
                  "Sn = n/2 (a + Un). Hitung Un dulu, lalu rata-rata suku pertama dan terakhir dikali n.", rng)
    n = rng.choice([21, 25, 33])
    a = rng.randint(3, 9)
    un = a + 2 * rng.randint(5, 12)
    Sn = n * (a + un) // 2
    return mk("aritsos", lv, f"Jumlah {n} suku pertama deret aritmatika adalah {Sn}. Jika suku pertamanya {a}, suku ke-{n} adalah …", un,
              [un - 2, un + 2, Sn // n, 2 * Sn // n], f"Sn = n/2 (a + Un) → {Sn} = {n}/2 ({a} + U) → ({a} + U) = {2 * Sn // n} → U = {un}.",
              "Dari Sn = n/2 (a + Un): (a + Un) = 2Sn/n. Satu pembagian, kurangi a.", rng)


@reg("aritsos", (2, 3))
def as_geometri(lv, rng):
    if lv == 2:
        a = rng.choice([2, 3, 5])
        r = rng.choice([2, 3])
        n = rng.choice([4, 5, 6])
        S = a * (r ** n - 1) // (r - 1)
        return mk("aritsos", lv, f"Jumlah {n} suku pertama deret geometri {a} + {a * r} + {a * r * r} + … adalah …", S,
                  [a * r ** (n - 1), a * r ** n, S - a, S + a], f"Sn = a(rⁿ − 1)/(r − 1) = {a}({r}^{n} − 1)/({r} − 1) = {S}.",
                  "r > 1: Sn = a(rⁿ − 1)/(r − 1). Jika diminta Un: a·rⁿ⁻¹ (pangkat n−1).", rng)
    n = rng.randint(14, 28)
    pecah = rng.choice([(2, "setengah"), (4, "seperempat"), (8, "seperdelapan")])
    # bakteri membelah 2 tiap hari; setengah penuh hari n → penuh hari n+1
    sebelum = {"setengah": 0, "seperempat": 1, "seperdelapan": 2}[pecah[1]]
    ans = n - sebelum
    return mk("aritsos", lv, f"Sejenis bakteri membelah diri menjadi 2 setiap hari. Wadah berisi setengah penuh pada hari ke-{n}. Pada hari keberapa wadah itu berisi {pecah[1]} penuh?",
              f"Hari ke-{ans}", [f"Hari ke-{n // 2}", f"Hari ke-{n - 1 if sebelum != 1 else n - 2}", f"Hari ke-{n + 1}", f"Hari ke-{n - 3}"],
              f"Jumlah bakteri berlipat dua tiap hari, jadi tiap hari mundur membuat isi wadah setengahnya. Setengah di hari {n} → seperempat di hari {n - 1} → seperdelapan di hari {n - 2}. Maka {pecah[1]} di hari {ans}.",
              "Berlipat dua tiap hari: mundur 1 hari = dibagi 2. Jangan memakai rumus deret, cukup mundur hari.", rng)


@reg("aritsos", (3,))
def as_kelipatan(lv, rng):
    k = rng.choice([3, 4, 6, 7])
    lo = rng.choice([100, 50, 200])
    hi = lo + rng.choice([100, 120, 150])
    first = ((lo // k) + 1) * k
    last = (hi // k) * k if hi % k else (hi // k) * k - k
    n = (last - first) // k + 1
    S = n * (first + last) // 2
    return mk("aritsos", lv, f"Jumlah semua bilangan di antara {lo} dan {hi} yang habis dibagi {k} adalah …", S, [S + k, S - k, S + first, n * (lo + hi) // 2],
              f"Suku pertama {first}, suku terakhir {last}, banyak suku = ({last} − {first})/{k} + 1 = {n}. Sn = {n}/2 ({first} + {last}) = {S}.",
              "Cari kelipatan pertama dan terakhir yang benar-benar di dalam batas (di antara, bukan termasuk batas). Lalu rumus Sn.", rng)


@reg("aritsos", (3,))
def as_sisip(lv, rng):
    m = rng.choice([9, 11, 14])
    a = rng.randint(2, 9) * 2
    b = a + (m + 1) * rng.randint(2, 6)
    S = (m + 2) * (a + b) // 2
    return mk("aritsos", lv, f"Antara bilangan {a} dan {b} disisipkan {m} bilangan sehingga bersama kedua bilangan semula membentuk deret hitung. Jumlah deret hitung itu adalah …",
              S, [S + a, S - b, (m + 1) * (a + b) // 2, m * (a + b) // 2], f"Banyak suku = {m} + 2 = {m + 2}. Sn = {m + 2}/2 × ({a} + {b}) = {S}.",
              "Penyisipan tidak mengubah suku pertama dan terakhir. Banyak suku = bilangan sisipan + 2.", rng)


# =====================================================================
# 5. SUDUT DAN HIMPUNAN
# =====================================================================
def _norm(x):
    x = abs(x)
    return 360 - x if x > 180 else x


@reg("sudut", (2, 3))
def sd_jam(lv, rng):
    h = rng.randint(1, 11)
    m = rng.choice([10, 20, 30, 40, 50]) if lv == 2 else rng.randint(1, 59)
    pendek = 30 * h + 0.5 * m
    panjang = 6 * m
    d = _norm(pendek - panjang)
    ans = f"{dc(d)}°"
    w = [f"{dc(_norm(30 * h - 6 * m))}°", f"{dc(_norm(pendek + panjang))}°", f"{dc(360 - d)}°", f"{dc(d + 5)}°"]
    return mk("sudut", lv, f"Besar sudut terkecil yang dibentuk jarum pendek dan jarum panjang pada pukul {h:02d}.{m:02d} adalah …", ans, w,
              f"Jarum pendek bergerak 30° per jam dan 0,5° per menit: {h}×30 + {m}×0,5 = {dc(pendek)}°. Jarum panjang 6° per menit: {m}×6 = {panjang}°. Selisih = {dc(d)}°.",
              "Sudut jam = |30h − 5,5m|. Jika > 180°, ambil 360° dikurangi hasil.", rng)


@reg("sudut")
def sd_garis(lv, rng):
    if lv == 1:
        a = rng.randint(20, 70)
        return mk("sudut", lv, f"Dua sudut saling berpelurus. Jika salah satunya {a}°, sudut yang lain adalah …", f"{180 - a}°",
                  [f"{90 - a}°" if a < 90 else f"{a}°", f"{a}°", f"{360 - a}°", f"{180 - a + 10}°"], f"Berpelurus berjumlah 180°: 180° − {a}° = {180 - a}°.",
                  "Berpelurus 180°, berpenyiku 90°. Hafal pasangan itu.", rng)
    if lv == 2:
        return _sudut_penyiku(rng)
    while True:
        A = rng.choice([8, 10, 12, 15])
        x = rng.randint(3, 9)
        B = rng.choice([3, 4, 5, 6])
        y = rng.randint(10, 30)
        theta = A * x
        if theta < 150 and A * x + x + B * y == 180:
            break
        for yy in range(5, 60):
            if A * x + x + B * yy == 180:
                y = yy
                break
        else:
            continue
        theta = A * x
        if theta < 150:
            break
    ans = f"{x}° dan {y}°"
    return mk("sudut", lv, f"Dua garis sejajar dipotong oleh sebuah garis. Sudut sehadap dengan sudut {theta}° besarnya (x·{A})° dan sudut yang berpelurus dengannya besarnya (x + {B}y)°. "
              f"Nilai x dan y adalah …", ans,
              [f"{x + 1}° dan {y}°", f"{x}° dan {y + 2}°", f"{x - 1}° dan {y + 3}°", f"{x + 2}° dan {y - 1}°"],
              f"Sudut sehadap sama besar: {A}x = {theta} → x = {x}. Berpelurus berjumlah 180°: {A}x + (x + {B}y) = 180 → {theta} + {x} + {B}y = 180 → {B}y = {180 - theta - x} → y = {y}.",
              "Pakai sifat sudut (sehadap/bertolak belakang = sama; berpelurus = 180°) untuk mendapat satu variabel dulu, lalu substitusi untuk variabel kedua.", rng)


def _sudut_penyiku(rng):
    a = rng.randint(10, 40)
    k = rng.choice([2, 3, 4])
    x = 90 // (k + 1)
    while 90 % (k + 1):
        k = rng.choice([2, 3, 4, 5])
        x = 90 // (k + 1) if 90 % (k + 1) == 0 else 0
    big = k * x
    return mk("sudut", 2, f"Dua sudut saling berpenyiku dan sudut yang besar {k} kali sudut yang kecil. Besar sudut yang kecil adalah …", f"{x}°",
              [f"{big}°", f"{x + 5}°", f"{90 // k}°", f"{x - 3}°"], f"x + {k}x = 90° → {k + 1}x = 90° → x = {x}°.",
              "Berpenyiku 90°: jumlahkan koefisien (1 + k) lalu bagi 90 dengan jumlah itu.", rng)


@reg("sudut")
def sd_himpunan(lv, rng):
    if lv == 1:
        S = rng.choice([60, 80, 100, 120, 143])
        A = rng.randint(S // 3, S // 2)
        B = rng.randint(S // 3, S // 2)
        AB = rng.randint(S // 10, min(A, B) - 1)
        tidak = S - (A + B - AB)
        if tidak < 3:
            return sd_himpunan(lv, rng)
        return mk("sudut", lv, f"Dari {S} siswa, {A} siswa senang matematika, {B} siswa senang fisika, dan {AB} siswa senang keduanya. Banyak siswa yang tidak senang keduanya adalah …",
                  tidak, [A + B - AB, S - A - B, tidak + AB, tidak + 4], f"n(A ∪ B) = {A} + {B} − {AB} = {A + B - AB}. Tidak keduanya = {S} − {A + B - AB} = {tidak}.",
                  "n(A∪B) = n(A) + n(B) − n(A∩B). Yang di luar = semesta − gabungan.", rng)
    S = rng.choice([80, 100, 120])
    A = rng.randint(25, 40)
    AB = rng.randint(5, 15)
    luar = rng.randint(20, 35)
    B = S - luar - A + AB
    if lv == 2:
        return mk("sudut", lv, f"Dari {S} siswa, {A} gemar olahraga. Di antara penggemar olahraga, {AB} siswa juga gemar musik. Jika {luar} siswa tidak gemar keduanya, banyak penggemar musik seluruhnya adalah …",
                  B, [B - AB, B + AB, S - A - luar, A + AB], f"{S} = {A} + n(M) − {AB} + {luar} → n(M) = {S} − {A} + {AB} − {luar} = {B}.",
                  "Susun persamaan semesta, lalu cari yang belum diketahui. Gambar diagram Venn dua lingkaran.", rng)
    hanya = A - AB
    return mk("sudut", lv, f"Dari {S} siswa, {A} gemar olahraga, {B} gemar musik, dan {luar} siswa tidak gemar keduanya. Banyak siswa yang HANYA gemar musik adalah …",
              B - AB, [B, hanya, B - AB + 5, B - AB - 3], f"n(A∩M) = {A} + {B} + {luar} − {S} = {AB}. Hanya musik = {B} − {AB} = {B - AB}.",
              "Cari irisan dulu: n(A∩B) = n(A) + n(B) + luar − semesta. “Hanya satu” = total kelompok − irisan.", rng)
