"""Generator soal Numerikal bagian 2: perbandingan, jarak-kecepatan-waktu, peluang, statistika, deret."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from .model import dc, mk, rp
from .registry import reg


def hm(menit: int) -> str:
    return f"{(menit // 60) % 24:02d}.{menit % 60:02d}"


def lcm(a, b):
    return a * b // math.gcd(a, b)


# =====================================================================
# 6. PERBANDINGAN
# =====================================================================
@reg("banding")
def pb_senilai(lv, rng):
    if lv == 1:
        n1, n2 = rng.choice([(7, 2), (5, 3), (4, 6), (8, 3)])
        harga1 = n1 * rng.randint(10, 40) * 1000
        h2 = harga1 * n2 // n1
        stem = f"Siti membeli {n1} kg buah naga seharga {rp(harga1)}. Uang yang dibutuhkan untuk membeli {n2} kg buah naga di toko yang sama adalah …"
        return mk("banding", lv, stem, rp(h2), [rp(harga1 // n2), rp(h2 + 5000), rp(h2 - 5000), rp(harga1 - h2)],
                  f"Senilai: {n1}/{n2} = {rp(harga1)}/x → x = {rp(harga1)} × {n2} ÷ {n1} = {rp(h2)}.",
                  "Cari harga satuan dulu (harga ÷ berat), lalu kalikan. Senilai: makin banyak, makin mahal.", rng)
    skala = rng.choice([1000000, 2000000, 5000000, 10000000])
    km = rng.choice([140, 210, 350, 560])
    cm = km * 100000 / skala
    cm_s = dc(round(cm, 2))
    stem = f"Jarak dua kota sebenarnya {km} km. Pada peta dengan skala 1 : {skala:,}".replace(",", ".") + f", jarak kedua kota itu pada peta adalah … cm."
    return mk("banding", lv, stem, cm_s, [dc(round(cm * 10, 2)), dc(round(cm / 10, 2)), dc(round(cm + 1, 2)), dc(round(cm * 2, 2))],
              f"{km} km = {km * 100000} cm. Jarak peta = {km * 100000} ÷ {skala} = {cm_s} cm.",
              "Satu km = 100.000 cm. Jarak peta = jarak sebenarnya (cm) ÷ penyebut skala. Samakan satuan dulu.", rng)


@reg("banding")
def pb_berbalik(lv, rng):
    if lv == 1:
        w1, w2 = rng.choice([(10, 15), (8, 12), (6, 9), (12, 18), (20, 30)])
        hari = rng.choice([6, 12, 18, 24])
        ans = hari * w1 // w2 if (hari * w1) % w2 == 0 else None
        if ans is None:
            return pb_berbalik(lv, rng)
        return mk("banding", lv, f"Suatu pekerjaan dapat diselesaikan oleh {w1} pekerja dalam {hari} hari. Jika pekerjanya {w2} orang, pekerjaan selesai dalam … hari.", ans,
                  [hari * w2 // w1 if (hari * w2) % w1 == 0 else hari + 2, hari - 1, ans + 2, hari], f"Berbalik nilai: {w1} × {hari} = {w2} × x → x = {w1 * hari} ÷ {w2} = {ans} hari.",
                  "Pekerja lebih banyak → waktu lebih sedikit. Total beban (pekerja × hari) tetap.", rng)
    if lv == 2:
        return _jam_terlambat(rng, rng.choice([10, 8, 12, 15, 5, 6, 9, 20, 30]))
    D = rng.choice([60, 48, 40])
    for _ in range(200):
        d1 = rng.choice([10, 12, 15, 20])
        s = rng.choice([2, 3, 4, 5])
        W = rng.randint(10, 40)
        rem = D - d1 - s
        beban = (D - d1) * W
        if rem > 0 and beban % rem == 0 and beban // rem > W:
            break
    else:
        D, W, d1, s = 60, 27, 20, 4
        rem, beban = D - d1 - s, (D - d1) * W
    need = beban // rem
    ans = need - W
    return mk("banding", lv, f"Proyek ditargetkan selesai dalam {D} hari oleh {W} pekerja. Setelah {d1} hari proyek dihentikan {s} hari karena cuaca. Agar selesai tepat waktu, jumlah pekerja tambahan yang diperlukan adalah …",
              ans, [need, ans + 1, ans - 1, ans + 2], f"Sisa pekerjaan = ({D} − {d1}) × {W} = {beban} orang-hari. Sisa waktu = {D} − {d1} − {s} = {rem} hari. Pekerja perlu = {beban} ÷ {rem} = {need}. Tambahan = {need} − {W} = {ans}.",
              "Hitung sisa beban dalam “orang-hari”, bagi dengan sisa hari kerja yang benar-benar tersedia, lalu kurangi pekerja yang sudah ada.", rng)


def _jam_terlambat(rng, m):
    hari = 720 // m
    return mk("banding", 2, f"Sebuah jam dinding (12 jam) setiap hari terlambat {m} menit. Berapa hari yang diperlukan agar jam itu kembali menunjukkan waktu yang benar?", hari,
              [hari * 2, hari // 2, 1440 // (m * 2), hari + m], f"Jam 12 jam kembali tepat setelah terlambat satu putaran penuh = 12 jam = 720 menit. Hari = 720 ÷ {m} = {hari}.",
              "Kembali menunjuk waktu yang sama = terlambat satu putaran penuh jam. Jam 12 jam: 720 menit; jam 24 jam: 1440 menit.", rng)


@reg("banding", (2, 3))
def pb_campuran(lv, rng):
    if lv == 2:
        o1, p1, h1 = rng.choice([(5, 70, 16), (4, 60, 12), (6, 90, 10), (5, 100, 8)])
        o2 = rng.choice([40, 50, 30])
        rasio = Fraction(o2 * 2, 1)
        p2 = p1 * rng.choice([2, 3, 5])
        h2 = h1 // 2 if h1 % 2 == 0 else h1
        ans = Fraction(p2 * o1 * h1, p1 * h2)
        if ans.denominator != 1:
            return pb_campuran(lv, rng)
        a = int(ans)
        return mk("banding", lv, f"Sebuah konveksi punya {o1} karyawan yang dapat menyelesaikan {p1} pesanan baju dalam {h1} hari. Berapa karyawan yang diperlukan untuk {p2} pesanan yang harus selesai dalam {h2} hari?",
                  a, [a // 2 if a % 2 == 0 else a + 3, a + o1, a - 2, o1 * p2 // p1], f"Produk/(orang × hari) tetap: {p1}/({o1}×{h1}) = {p2}/(x×{h2}) → x = {p2}×{o1}×{h1} ÷ ({p1}×{h2}) = {a}.",
              "Perbandingan campuran: produk sebanding dengan orang × waktu. Tulis sebagai produk ÷ (orang × hari) = tetap.", rng)
    a, b = rng.choice([(5, 3), (3, 2), (7, 5)])
    pj, pq = rng.choice([(3, 8), (2, 5), (3, 4)])
    frac = Fraction(a, a + b) * Fraction(pj, pq)
    ans = f"{frac.numerator}/{frac.denominator}"
    return mk("banding", lv, f"Jumlah serangga berciri X dibanding berciri Y adalah {a} : {b}, dan {pj}/{pq} serangga berciri X adalah jantan. Dari seluruh serangga, proporsi serangga jantan berciri X adalah …",
              ans, [f"{a}/{a + b}", f"{pj}/{pq}", f"{Fraction(b, a + b) * Fraction(pj, pq)}", f"{Fraction(a, b) * Fraction(pj, pq)}", f"{pj}/{pq + a}", f"{a}/{pq + b}"],
              f"Bagian X dari seluruh = {a}/{a + b}. Jantan dari X = {pj}/{pq}. Proporsi = {a}/{a + b} × {pj}/{pq} = {ans}.",
              "Perbandingan a : b → bagian a = a/(a+b) dari seluruhnya. Pecahan dari pecahan: kalikan.", rng)


# =====================================================================
# 7. JARAK, KECEPATAN DAN WAKTU
# =====================================================================
@reg("jarak")
def jk_papasan(lv, rng):
    if lv == 1:
        v1, v2 = rng.choice([(52, 58), (40, 60), (45, 55), (60, 65)])
        t = rng.choice([1, 2, 3])
        S = (v1 + v2) * t
        mulai = rng.choice([7, 8, 9, 10]) * 60
        return mk("jarak", lv, f"Jarak rumah Andi dan Budi {S} km. Andi berkendara dari rumahnya pukul {hm(mulai)} dengan kecepatan {v1} km/jam menuju rumah Budi. Pada waktu yang sama Budi berkendara menuju rumah Andi dengan kecepatan {v2} km/jam. Mereka berpapasan pukul …",
                  hm(mulai + t * 60), [hm(mulai + t * 60 + 30), hm(mulai + t * 60 - 30), hm(mulai + (t + 1) * 60), hm(mulai + t * 30)],
                  f"Kecepatan gabungan = {v1} + {v2} = {v1 + v2} km/jam. Waktu = {S} ÷ {v1 + v2} = {t} jam. Pukul {hm(mulai)} + {t} jam = {hm(mulai + t * 60)}.",
                  "Berpapasan: kecepatan DIJUMLAH. Waktu = jarak ÷ jumlah kecepatan.", rng)
    if lv == 2:
        v1, v2 = rng.choice([(80, 60), (60, 90), (50, 70), (40, 60)])
        tunda = rng.choice([30, 60])
        t = rng.choice([1, 2])
        S = v1 * tunda // 60 + (v1 + v2) * t
        mulai = rng.choice([8, 9, 10]) * 60
        return mk("jarak", lv, f"Jarak rumah Arman dan Danu {S} km. Arman berangkat pukul {hm(mulai)} dengan {v1} km/jam menuju rumah Danu. Danu berangkat {tunda} menit kemudian dengan {v2} km/jam menuju rumah Arman. Mereka berpapasan pukul …",
                  hm(mulai + tunda + t * 60), [hm(mulai + t * 60), hm(mulai + tunda + t * 60 + 30), hm(mulai + tunda), hm(mulai + (t + 1) * 60 + tunda)],
                  f"Selisih jarak = {v1} × {tunda}/60 = {v1 * tunda // 60} km. Waktu berpapasan = ({S} − {v1 * tunda // 60}) ÷ ({v1} + {v2}) = {t} jam sejak Danu berangkat. Pukul {hm(mulai + tunda)} + {t} jam = {hm(mulai + tunda + t * 60)}.",
                  "Berangkat tidak bersamaan: kurangi jarak yang sudah ditempuh si pemberangkat awal, baru bagi dengan jumlah kecepatan. Waktu dihitung dari yang berangkat belakangan.", rng)
    v1, v2 = rng.choice([(60, 70), (40, 50), (50, 60), (30, 40)])
    sel = rng.choice([20, 30, 40])
    sjarak = v1 * sel / 60
    t = sjarak / (v2 - v1)
    if t != int(t) or t <= 0:
        return jk_papasan(lv, rng)
    mulai = rng.choice([6, 7]) * 60 + rng.choice([0, 20, 40])
    ans = hm(mulai + sel + int(t) * 60)
    return mk("jarak", lv, f"Lina berangkat pukul {hm(mulai)} dengan kecepatan {v1} km/jam. Leni berangkat {sel} menit kemudian dari tempat yang sama dengan kecepatan {v2} km/jam. Pukul berapa Leni menyusul Lina?",
              ans, [hm(mulai + sel), hm(mulai + int(t) * 60), hm(mulai + sel + int(t) * 60 + 30), hm(mulai + sel + int(t) * 60 - 20)],
              f"Jarak Lina saat Leni berangkat = {v1} × {sel}/60 = {sjarak:g} km. Waktu menyusul = {sjarak:g} ÷ ({v2} − {v1}) = {int(t)} jam. Pukul {hm(mulai + sel)} + {int(t)} jam = {ans}.",
              "Menyusul: kecepatan DIKURANGI. Waktu menyusul = jarak awal ÷ selisih kecepatan, dihitung sejak yang kedua berangkat.", rng)


@reg("jarak", (2, 3))
def jk_rata2(lv, rng):
    if lv == 2:
        s1, t1 = rng.choice([(600, 5), (400, 4), (900, 6)])
        s2, t2 = rng.choice([(900, 10), (1200, 8), (1100, 12)])
        s3, t3 = rng.choice([(750, 15), (800, 8), (1300, 20)])
        S, T = s1 + s2 + s3, t1 + t2 + t3
        ans = Fraction(S, T)
        a = dc(round(float(ans), 2)) if ans.denominator != 1 else str(ans.numerator)
        return mk("jarak", lv, f"Sebuah kendaraan menempuh {s1} m dalam {t1} menit, lalu {s2} m dalam {t2} menit, dan {s3} m dalam {t3} menit terakhir. Kecepatan rata-rata kendaraan itu adalah … m/menit.",
                  a, [dc(round((s1 / t1 + s2 / t2 + s3 / t3) / 3, 2)), dc(round(float(ans) + 5, 2)), dc(round(float(ans) - 5, 2)), dc(round(float(ans) * 2, 2))],
                  f"Rata-rata = jarak total ÷ waktu total = ({s1} + {s2} + {s3}) ÷ ({t1} + {t2} + {t3}) = {S} ÷ {T} = {a} m/menit.",
                  "Kecepatan rata-rata = jarak TOTAL ÷ waktu TOTAL. Bukan rata-rata dari kecepatan tiap ruas.", rng)
    v = rng.choice([35, 40, 45])
    berhenti = rng.choice([1, 2])
    lama = rng.choice([4, 5, 6])
    sj = v * lama
    mulai = 6 * 60 + 20
    tiba = mulai + (lama + berhenti) * 60
    return mk("jarak", lv, f"Dodi berangkat dari kota A pukul {hm(mulai)} dan tiba di kota B pukul {hm(tiba)}. Ia mengendarai mobil dengan kecepatan {v} km/jam dan berhenti selama {berhenti} jam di jalan. Jarak kota A ke B adalah … km.",
              sj, [v * (lama + berhenti), v * (lama - 1), v * (lama + 1), sj + v // 2],
              f"Waktu total = {lama + berhenti} jam. Dikurangi berhenti {berhenti} jam = {lama} jam berkendara. Jarak = {v} × {lama} = {sj} km.",
              "Waktu berhenti TIDAK dihitung untuk jarak. Waktu tempuh = waktu total − waktu berhenti.", rng)


@reg("jarak")
def jk_zona_dan_lebih_cepat(lv, rng):
    if lv == 1:
        s, t = rng.choice([(70, 2.5), (60, 2), (90, 3), (120, 2.5)])
        lebih = rng.choice([0.5, 0.75]) if s != 120 else 0.5
        v1 = s / t
        t2 = t - lebih
        v2 = s / t2
        if abs(v2 - round(v2)) > 1e-9 or abs(v1 - round(v1)) > 1e-9:
            return jk_zona_dan_lebih_cepat(lv, rng)
        d = int(round(v2 - v1))
        return mk("jarak", lv, f"Seseorang menempuh {s} km dalam {dc(t)} jam. Agar tiba {dc(lebih)} jam lebih cepat, ia harus menambah kecepatan rata-rata sebesar … km/jam.", d,
                  [int(v2), int(v1), d + 4, d - 3], f"v₁ = {s}/{dc(t)} = {int(v1)} km/jam. v₂ = {s}/{dc(t2)} = {int(v2)} km/jam. Tambahan = {int(v2)} − {int(v1)} = {d} km/jam.",
                  "Hitung dua kecepatan (lama dan baru), lalu kurangkan. Perhatikan yang ditanya: kecepatan baru atau selisihnya.", rng)
    beda = rng.choice([2, 3])
    mulai = rng.choice([4, 5, 6, 7]) * 60
    dur = rng.choice([3, 4, 5])
    if lv == 2:
        return mk("jarak", lv, f"Waktu di kota A adalah {beda} jam lebih cepat daripada di kota B. Sebuah pesawat berangkat dari kota A pukul {hm(mulai)} (waktu A) menuju kota B dan tiba {dur} jam kemudian. Pukul berapa (waktu B) pesawat itu tiba?",
                  hm(mulai + dur * 60 - beda * 60), [hm(mulai + dur * 60), hm(mulai + dur * 60 + beda * 60), hm(mulai - beda * 60), hm(mulai + dur * 60 - (beda + 1) * 60)],
                  f"Tiba menurut waktu A = {hm(mulai)} + {dur} jam = {hm(mulai + dur * 60)}. Waktu B lebih lambat {beda} jam, jadi {hm(mulai + dur * 60)} − {beda} jam = {hm(mulai + dur * 60 - beda * 60)}.",
                  "Kota yang waktunya “lebih cepat” memiliki jam yang lebih besar. Konversi ke waktu kota tujuan di akhir, bukan di awal.", rng)
    tiba_B = mulai + dur * 60 - beda * 60
    return mk("jarak", lv, f"Waktu di kota A adalah {beda} jam lebih cepat daripada di kota B. Sebuah pesawat berangkat dari kota A pukul {hm(mulai)} (waktu A) dan tiba di kota B pukul {hm(tiba_B)} (waktu B). Lama penerbangan adalah … jam.",
              dur, [dur - beda, dur + beda, dur + 1, dur - 1], f"Samakan zona: pukul {hm(tiba_B)} waktu B = {hm(tiba_B + beda * 60)} waktu A. Lama = {hm(tiba_B + beda * 60)} − {hm(mulai)} = {dur} jam.",
              "Soal zona waktu: ubah kedua waktu ke zona yang SAMA sebelum menghitung selisih.", rng)


@reg("jarak", (2, 3))
def jk_kerja_bersama(lv, rng):
    a, b, c, ans = rng.choice([(30, 45, 90, 15), (20, 30, 60, 10), (10, 15, 30, 5), (12, 18, 36, 6), (24, 48, 48, 12), (40, 60, 120, 20)])
    if lv == 2:
        return mk("jarak", lv, f"Andi dapat mengisi kolam ikan dalam {a} menit, Bedu dalam {b} menit, dan Catur dalam {c} menit. Jika mereka bekerja bersama, waktu yang dibutuhkan adalah … menit.",
                  ans, [(a + b + c) // 3, ans + 3, ans - 2, a // 2], f"Misal total = KPK = {lcm(lcm(a, b), c)} satuan. Laju: {lcm(lcm(a, b), c) // a} + {lcm(lcm(a, b), c) // b} + {lcm(lcm(a, b), c) // c} = {lcm(lcm(a, b), c) // ans}. Waktu = {lcm(lcm(a, b), c)} ÷ {lcm(lcm(a, b), c) // ans} = {ans} menit.",
                  "Tiga pekerja: misalkan total pekerjaan = KPK, hitung satuan per menit tiap orang, jumlahkan, bagi.", rng)
    return _bak(rng)


def _bak(rng):
    x, y = rng.choice([(3, 6), (4, 12), (6, 12), (10, 15), (12, 18), (4, 6), (8, 24)])
    L = lcm(x, y)
    net = L // x - L // y
    ans = L // net
    return mk("jarak", 3, f"Pipa A dapat mengisi bak air hingga penuh dalam {x} jam, sedangkan pipa B dapat menguras bak penuh dalam {y} jam. Jika bak kosong dan kedua pipa dibuka bersamaan, bak penuh dalam … jam.",
              ans, [x * y // (x + y) if (x * y) % (x + y) == 0 else y - x, y - x, ans + 2, ans - 2],
              f"Total = KPK = {L} satuan. Pengisian {L // x}/jam, penguras {L // y}/jam, bersih {net}/jam. Waktu = {L} ÷ {net} = {ans} jam.",
              "Pengisi dan penguras: laju dikurangi, bukan dijumlah. Rumus pintas: xy ÷ (y − x).", rng)


# =====================================================================
# 8. PELUANG, PERMUTASI DAN KOMBINASI
# =====================================================================
def _frac(n, d):
    f = Fraction(n, d)
    return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)


@reg("peluang")
def pl_dadu(lv, rng):
    if lv == 1:
        jml = rng.choice([4, 5, 6, 7, 8, 9, 10])
        cnt = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == jml)
        return mk("peluang", lv, f"Dua dadu dilempar bersamaan. Peluang munculnya jumlah kedua mata dadu sama dengan {jml} adalah …", _frac(cnt, 36),
                  [_frac(cnt + 1, 36), _frac(cnt, 12), _frac(cnt - 1 if cnt > 1 else cnt + 2, 36), _frac(1, 6), _frac(cnt + 2, 36), _frac(cnt + 3, 36), _frac(cnt, 6)],
                  f"Kejadian jumlah {jml}: " + ", ".join(f"({a},{b})" for a in range(1, 7) for b in range(1, 7) if a + b == jml) + f". n(A) = {cnt}, n(S) = 36. P = {_frac(cnt, 36)}.",
                  "Dua dadu: n(S) = 36. Daftar pasangannya urut, jangan lewatkan pasangan terbalik (1,5) dan (5,1).", rng)
    if lv == 2:
        k = rng.choice([8, 9, 10])
        cnt = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= k)
        return mk("peluang", lv, f"Dua dadu dilempar bersamaan. Peluang munculnya jumlah mata dadu paling sedikit {k} adalah …", _frac(cnt, 36),
                  [_frac(cnt + 1, 36), _frac(36 - cnt, 36), _frac(cnt, 18), _frac(cnt - 1, 36)],
                  f"Jumlah ≥ {k}: ada {cnt} pasangan. P = {cnt}/36 = {_frac(cnt, 36)}.", "“Paling sedikit k” artinya ≥ k. Hitung dari sisi yang pasangannya lebih sedikit.", rng)
    pB = rng.choice([Fraction(1, 4), Fraction(1, 5)])
    pb = 1 - pB
    k = rng.choice([2, 3])
    pA = k * pB
    ans = 1 - pA
    kand = [pA, pB, pb, Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5)]
    dis = [_frac(x.numerator, x.denominator) for x in kand if x != ans]
    return mk("peluang", lv, f"Dalam suatu kompetisi, peluang tim A menjadi juara {k} kali peluang tim B. Jika peluang tim B tidak menjadi juara adalah {pb.numerator}/{pb.denominator}, peluang tim A tidak menjadi juara adalah …",
              _frac(ans.numerator, ans.denominator), dis,
              f"P(B) = 1 − {pb} = {pB}. P(A) = {k} × {pB} = {pA}. P(A tidak juara) = 1 − {pA} = {ans}.", "Komplemen: P(A′) = 1 − P(A). Cari P yang dibutuhkan dulu lewat hubungan yang diberikan.", rng)


@reg("peluang")
def pl_permutasi(lv, rng):
    if lv == 1:
        n = rng.choice([4, 5, 6])
        r = 3
        ans = math.perm(n, r)
        return mk("peluang", lv, f"Nomor antrian terdiri atas {r} angka berbeda yang dibentuk dari angka 1 sampai {n}. Banyak nomor antrian yang dapat dibuat adalah …", ans,
                  [math.comb(n, r), n ** r, math.factorial(n), ans + n], f"Urutan berpengaruh: P({n},{r}) = {n}!/({n}−{r})! = {ans}.",
                  "Urutan berpengaruh (nomor, susunan) → permutasi. Tidak berpengaruh (memilih kelompok) → kombinasi.", rng)
    if lv == 2:
        n = rng.choice([5, 6, 7])
        ans = (n - 2) * math.factorial(n - 1) * 2 // 1
        jml = math.factorial(n) - 2 * math.factorial(n - 1)
        return mk("peluang", lv, f"{n} orang duduk berjajar di {n} kursi. Jika dua orang di antaranya (Adi dan Budi) tidak mau duduk berdampingan, banyak susunan duduk yang mungkin adalah …",
                  jml, [math.factorial(n), 2 * math.factorial(n - 1), jml + math.factorial(n - 1), jml - n], f"Total = {n}! = {math.factorial(n)}. Berdampingan = 2 × {n - 1}! = {2 * math.factorial(n - 1)}. Tidak berdampingan = {math.factorial(n)} − {2 * math.factorial(n - 1)} = {jml}.",
                  "“Tidak berdampingan” = total − berdampingan. Berdampingan: anggap keduanya satu blok, lalu kali 2 untuk urutan di dalam blok.", rng)
    d = rng.choice([[1, 2, 4, 6, 9], [1, 3, 4, 7, 9], [1, 2, 5, 7, 9]])
    ganjil = [x for x in d if x % 2 == 1]
    ans = len(ganjil) * math.factorial(len(d) - 1)
    return mk("peluang", lv, f"Banyak bilangan ganjil lima angka yang memuat semua angka {', '.join(map(str, d))} (tiap angka dipakai sekali) adalah …", ans,
              [math.factorial(len(d)), ans // 2, ans + 24, len(ganjil) * math.factorial(len(d))],
              f"Angka terakhir harus ganjil: ada {len(ganjil)} pilihan ({', '.join(map(str, ganjil))}). Empat posisi lain: 4! = 24. Total = {len(ganjil)} × 24 = {ans}.",
              "Isi posisi yang paling dibatasi dulu (satuan harus ganjil), baru sisanya dipermutasikan.", rng)


@reg("peluang", (2, 3))
def pl_kombinasi(lv, rng):
    if lv == 2:
        m, f, k = rng.choice([(5, 4, 3), (6, 4, 2), (5, 5, 3)])
        a, b = 2, 2
        ans = math.comb(m, a) * math.comb(f, b) * math.comb(k, 1)
        return mk("peluang", lv, f"Dari {m} buku matematika, {f} buku fisika, dan {k} buku kimia akan dipilih 2 buku matematika, 2 buku fisika, dan 1 buku kimia. Banyak cara memilihnya adalah …", ans,
                  [ans // 2 if ans % 2 == 0 else ans + 10, math.comb(m + f + k, 5), ans + 30, math.comb(m, 2) + math.comb(f, 2) + k],
                  f"C({m},2) × C({f},2) × C({k},1) = {math.comb(m, 2)} × {math.comb(f, 2)} × {k} = {ans}.", "Pilihan terpisah: kalikan kombinasi tiap kelompok. Kombinasi karena memilih tanpa memperhatikan urutan.", rng)
    n = rng.choice([10, 11, 12])
    k = rng.choice([5, 6])
    ans = math.comb(n, k) - math.comb(n - 2, k - 2)
    return mk("peluang", lv, f"Ani akan mengundang {k} dari {n} temannya, termasuk Citra dan Budi. Karena suatu masalah, Citra dan Budi tidak ingin bertemu di acara yang sama. Banyak cara Ani mengundang {k} orang adalah …",
              ans, [math.comb(n, k), math.comb(n - 2, k) + 2 * math.comb(n - 2, k - 1), math.comb(n - 2, k - 2), ans - math.comb(n - 2, k - 2)],
              f"Total = C({n},{k}) = {math.comb(n, k)}. Keduanya hadir = C({n - 2},{k - 2}) = {math.comb(n - 2, k - 2)}. Tidak bersama = {math.comb(n, k)} − {math.comb(n - 2, k - 2)} = {ans}.",
              "Syarat “tidak boleh bersama” = total − (keduanya bersama). Cara itu lebih singkat daripada menjumlahkan kasus.", rng)


@reg("peluang")
def pl_frekuensi(lv, rng):
    if lv == 1:
        n = rng.choice([36, 60, 120, 180])
        return mk("peluang", lv, f"Sebuah dadu dilempar sebanyak {n} kali. Frekuensi harapan munculnya mata dadu bernomor 3 adalah …", n // 6, [n // 3, n // 2, n // 6 + 3, n // 12],
                  f"Fh = n × P(A) = {n} × 1/6 = {n // 6}.", "Frekuensi harapan = banyak percobaan × peluang satu kejadian.", rng)
    if lv == 2:
        akhir = rng.choice([("N", 14, 3), ("M", 13, 3), ("Z", 26, 5)])
        huruf, jml, vok = akhir
        n = jml * rng.choice([6, 8, 10])
        ans = vok * n // jml
        return mk("peluang", lv, f"Sebuah kotak berisi kertas bertuliskan huruf A sampai {huruf} (satu kertas tiap huruf). Setiap kali pengambilan, kertas dikembalikan. Dari {n} pengambilan, frekuensi harapan terambilnya huruf vokal adalah …",
                  ans, [ans + vok, ans - vok, n // vok, n * vok // jml + 2], f"Huruf A–{huruf} ada {jml}; vokal ada {vok} (A, E, I{', O, U' if vok == 5 else ''}). P(vokal) = {vok}/{jml}. Fh = {vok}/{jml} × {n} = {ans}.",
                  "Hitung dulu peluang satu kejadian, baru kalikan dengan banyak percobaan. Hati-hati menghitung vokal yang termasuk dalam rentang huruf.", rng)
    h, p = rng.choice([(55, 60), (30, 40), (45, 60)])
    x = rng.choice([10, 15, 20, 25, 35])
    S = h + p
    P = Fraction(x, S + x)
    return mk("peluang", lv, f"Sebuah kantong berisi {h} kelereng hitam, {p} kelereng putih, dan beberapa kelereng abu-abu. Jika diambil satu kelereng, peluang terambilnya kelereng abu-abu adalah {P.numerator}/{P.denominator}. Banyak kelereng abu-abu adalah … butir.",
              x, [x + 5, x - 5, S, x * 2], f"Misal abu-abu = x. x/({S} + x) = {P.numerator}/{P.denominator} → {P.denominator}x = {P.numerator}({S} + x) → {P.denominator - P.numerator}x = {P.numerator * S} → x = {x}.",
              "Peluang pecahan dengan satu variabel: kalikan silang, kumpulkan x di satu ruas. Cek dengan memasukkan jawaban ke pecahan.", rng)


# =====================================================================
# 9. STATISTIKA
# =====================================================================
@reg("statistika", (1,))
def st_tunggal(lv, rng):
    n = rng.choice([9, 10, 11])
    data = sorted(rng.randint(2, 12) for _ in range(n))
    mean = Fraction(sum(data), n)
    med = data[n // 2] if n % 2 else Fraction(data[n // 2 - 1] + data[n // 2], 2)
    mode = max(set(data), key=lambda v: (data.count(v), -v))
    mode_cnt = data.count(mode)
    ties = [v for v in set(data) if data.count(v) == mode_cnt]
    if len(ties) > 1:
        return st_tunggal(lv, rng)
    which = rng.choice(["rata-rata", "median", "modus"])
    ans = {"rata-rata": mean, "median": med, "modus": mode}[which]
    f = lambda v: dc(float(v)) if isinstance(v, Fraction) and v.denominator != 1 else str(int(v))
    ws = {"rata-rata": [med, mode, mean + 1, mean - 1], "median": [mean, mode, med + 1, med - 1], "modus": [mean, med, mode + 1, mode - 1]}[which]
    return mk("statistika", lv, f"Diketahui data: {', '.join(map(str, rng.sample(data, n)))}. Nilai {which} data tersebut adalah …", f(ans), [f(Fraction(w).limit_denominator(100)) for w in ws] + [f(ans + Fraction(3, 2)), f(ans + 2)],
              f"Urutkan: {', '.join(map(str, data))}. n = {n}. Jumlah = {sum(data)}. Rata-rata = {f(mean)}; median = {f(med)}; modus = {mode}.",
              "Urutkan dulu data (untuk median dan modus). Median data ganjil = data ke-(n+1)/2; genap = rata-rata dua data tengah.", rng)


@reg("statistika", (2, 3))
def st_gabungan(lv, rng):
    if lv == 2:
        n1, m1 = rng.choice([(12, 80), (10, 70), (8, 75)])
        n2 = rng.choice([16, 20, 12])
        m2 = rng.choice([84, 78, 90])
        tot = n1 * m1 + n2 * m2
        ans = Fraction(tot, n1 + n2)
        a = dc(round(float(ans), 2)) if ans.denominator != 1 else str(ans.numerator)
        return mk("statistika", lv, f"Rata-rata nilai {n1} siswa laki-laki adalah {m1} dan rata-rata nilai {n2} siswa perempuan adalah {m2}. Rata-rata nilai seluruh siswa adalah …", a,
                  [dc(round((m1 + m2) / 2, 2)), dc(round(float(ans) + 1, 2)), dc(round(float(ans) - 1, 2)), dc(round(float(ans) + 2, 2))],
                  f"Total = {n1}×{m1} + {n2}×{m2} = {tot}. Rata-rata = {tot} ÷ {n1 + n2} = {a}.", "Rata-rata gabungan = total nilai ÷ total orang. Bukan rata-rata dari dua rata-rata.", rng)
    L, P = 12, 16
    rata = rng.choice([80, 78, 82])
    lama = rng.choice([[52, 56, 62, 66], [50, 54, 60, 64]])
    naik = rng.choice([6, 7, 8])
    rl = rng.choice([76, 78])
    tot_all = (L + P) * rata
    tot_L = L * rl
    tot_P = tot_all - tot_L
    sum_remedial_naik = naik * 4
    # setelah remedial, rata-rata laki-laki 'rl' dan sebelumnya 'rl - x' ; derive female avg
    new_avg_P = Fraction(tot_P, P)
    if new_avg_P.denominator != 1:
        tot_P = P * (tot_P // P)
        new_avg_P = Fraction(tot_P, P)
    ans = int(new_avg_P)
    return mk("statistika", lv, f"Dalam suatu kelas terdapat {L} murid laki-laki dan {P} murid perempuan. Rata-rata nilai seluruh murid adalah {rata}. Rata-rata nilai laki-laki adalah {rl}. Rata-rata nilai murid perempuan adalah …",
              ans, [ans + 2, ans - 2, rata, (rata + rl) // 2], f"Total seluruh = {L + P} × {rata} = {(L + P) * rata}. Total laki-laki = {L} × {rl} = {L * rl}. Total perempuan = {(L + P) * rata - L * rl}. Rata-rata = {(L + P) * rata - L * rl} ÷ {P} = {Fraction((L + P) * rata - L * rl, P)}.",
              "Cari total tiap kelompok, kurangkan, baru bagi dengan banyak orangnya. Selalu bekerja dengan total.", rng) if ((L + P) * rata - L * rl) % P == 0 else st_gabungan(lv, rng)


@reg("statistika", (2, 3))
def st_kelompok(lv, rng):
    batas = [(31, 40), (41, 50), (51, 60), (61, 70), (71, 80), (81, 90)]
    fr = [rng.randint(2, 12) for _ in batas]
    n = sum(fr)
    tabel = "| Nilai | Frekuensi |\n|---|---|\n" + "\n".join(f"| {a} – {b} | {f} |" for (a, b), f in zip(batas, fr))
    mids = [(a + b) / 2 for a, b in batas]
    mean = sum(m * f for m, f in zip(mids, fr)) / n
    if lv == 2:
        a = dc(round(mean, 2))
        return mk("statistika", lv, f"Perhatikan tabel berikut.\n\n{tabel}\n\nRata-rata nilai pada tabel tersebut adalah …", a,
                  [dc(round(mean + 1, 2)), dc(round(mean - 1.5, 2)), dc(round(mean + 2.5, 2)), dc(round(sum(mids) / len(mids), 2))],
                  f"Nilai tengah tiap kelas: {', '.join(dc(m) for m in mids)}. Σ f·x = {dc(sum(m * f for m, f in zip(mids, fr)))}. Rata-rata = {dc(sum(m * f for m, f in zip(mids, fr)))} ÷ {n} = {a}.",
                  "Data berkelompok: pakai nilai tengah tiap kelas, kalikan frekuensi, jumlahkan, bagi total frekuensi.", rng)
    # median
    cum = 0
    for i, f in enumerate(fr):
        if cum + f >= n / 2:
            break
        cum += f
    tb = batas[i][0] - 0.5
    p = 10
    med = tb + ((n / 2 - cum) / fr[i]) * p
    a = dc(round(med, 2))
    return mk("statistika", lv, f"Perhatikan tabel berikut.\n\n{tabel}\n\nMedian dari data pada tabel tersebut adalah …", a,
              [dc(round(med + 2, 2)), dc(round(med - 2, 2)), dc(round(tb, 2)), dc(round(med + 5, 2))],
              f"n = {n}, n/2 = {dc(n / 2)}. Kelas median: {batas[i][0]} – {batas[i][1]} (frekuensi kumulatif sebelumnya {cum}, frekuensi kelas {fr[i]}). Tepi bawah = {dc(tb)}. Median = {dc(tb)} + (({dc(n / 2)} − {cum})/{fr[i]}) × 10 = {a}.",
              "Median kelompok: cari kelas yang memuat data ke-n/2 lewat frekuensi kumulatif, lalu rumus tepi bawah + ((n/2 − fk)/f) × p.", rng)


@reg("statistika", (3,))
def st_ekstrem(lv, rng):
    if rng.random() < 0.5:
        n = rng.choice([15, 20])
        m = rng.choice([15, 20, 25])
        ans = n * m - (n - 2) * (n - 1) // 2
        return mk("statistika", lv, f"Jika rata-rata {n} bilangan bulat non-negatif yang berbeda adalah {m}, bilangan terbesar yang mungkin adalah …", ans,
                  [ans - n, ans + n, n * m, ans - 10], f"Jumlah = {n} × {m} = {n * m}. Agar satu bilangan sebesar mungkin, {n - 1} lainnya sekecil mungkin: 0, 1, …, {n - 2}, jumlahnya {(n - 2) * (n - 1) // 2}. Terbesar = {n * m} − {(n - 2) * (n - 1) // 2} = {ans}.",
                  "Maksimalkan satu bilangan = minimalkan yang lain: pakai deret berbeda terkecil (0, 1, 2, …). Kurangkan dari total.", rng)
    lo, hi = rng.choice([(20, 48), (10, 30), (15, 45)])
    mn = Fraction(3 * lo + hi, 4)
    mx = Fraction(lo + 3 * hi, 4)
    inside = [mn, (mn + mx) / 2, mx - 2, mx]
    out = rng.choice([mx + 3, mn - 3])
    opts_vals = [float(v) for v in inside] + [float(out)]
    opts_vals = sorted(set(round(v, 2) for v in opts_vals))
    if len(opts_vals) != 5:
        return st_ekstrem(lv, rng)
    fmtv = lambda v: dc(v)
    return mk("statistika", lv, f"Ada empat bilangan; yang terkecil {lo} dan yang terbesar {hi}. Rata-rata keempat bilangan itu tidak mungkin sebesar …", fmtv(round(float(out), 2)),
              [fmtv(v) for v in opts_vals if v != round(float(out), 2)],
              f"Rata-rata terkecil = ({lo}+{lo}+{lo}+{hi})/4 = {dc(float(mn))}. Rata-rata terbesar = ({lo}+{hi}+{hi}+{hi})/4 = {dc(float(mx))}. Jadi {dc(float(mn))} ≤ rata-rata ≤ {dc(float(mx))}; nilai di luar rentang itu mustahil.",
              "Batas rata-rata: ganti tiga bilangan lain dengan nilai minimum (lo) atau maksimum (hi). Rata-rata pasti berada di antaranya.", rng)


# =====================================================================
# 10. DERET ANGKA DAN HURUF
# =====================================================================
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]


def _stem(seq):
    return "Lanjutkan deret berikut: **" + ", ".join(map(str, seq)) + ", …**"


@reg("deret", (1,))
def dr_dasar(lv, rng):
    t = rng.randint(1, 6)
    if t == 1:
        a, d = rng.randint(2, 30), rng.randint(2, 9)
        seq = [a + i * d for i in range(5)]
        ans = a + 5 * d
        return mk("deret", lv, _stem(seq), ans, [ans + 1, ans - 1, ans + d, ans - d], f"Selisih tetap +{d}. {seq[-1]} + {d} = {ans}.", "Cek selisih dulu. Kalau tetap, cukup tambahkan.", rng)
    if t == 2:
        a, r = rng.randint(1, 6), rng.choice([2, 3])
        seq = [a * r ** i for i in range(5)]
        ans = a * r ** 5
        return mk("deret", lv, _stem(seq), ans, [seq[4] + seq[3], ans + r, ans - r, seq[4] * (r + 1)], f"Tiap suku dikali {r}: {seq[4]} × {r} = {ans}.", "Angka melonjak cepat: cek rasio (suku ÷ suku sebelumnya).", rng)
    if t == 3:
        a, b = rng.randint(1, 5), rng.randint(2, 7)
        seq = [a, b]
        for i in range(3):
            seq.append(seq[-1] + seq[-2])
        ans = seq[-1] + seq[-2]
        return mk("deret", lv, _stem(seq), ans, [ans + 1, ans - 1, seq[-1] * 2, ans + 2], f"Fibonacci: tiap suku = jumlah dua suku sebelumnya. {seq[-2]} + {seq[-1]} = {ans}.",
                  "Selisihnya menyerupai deret itu sendiri? Itu Fibonacci: jumlahkan dua suku sebelumnya.", rng)
    if t == 4:
        a, d1 = rng.randint(2, 6), rng.randint(2, 4)
        b = rng.randint(5, 15)
        d2 = rng.randint(2, 6)
        seq = [a, b, a + d1, b + d2, a + 2 * d1, b + 2 * d2]
        ans = a + 3 * d1
        return mk("deret", lv, _stem(seq), ans, [b + 3 * d2, ans + d1, ans - 1, ans + 1], f"Dua larik berselang-seling. Suku ganjil: {a}, {a + d1}, {a + 2 * d1} (+{d1}). Suku genap: {b}, {b + d2}, {b + 2 * d2} (+{d2}). Berikutnya dari larik ganjil: {ans}.",
                  "Larik: pisahkan suku ganjil dan genap, kerjakan masing-masing. Ini pola yang sangat sering muncul.", rng)
    if t == 5:
        a = rng.randint(2, 6)
        s1, s2 = rng.choice([(2, 3), (2, 4), (3, 4)])
        seq = [a]
        for i in range(5):
            seq.append(seq[-1] + (s1 if i % 3 != 2 else s2) * (1 if i < 2 else 1))
        # pola tingkat: +2, +2, +3, +2, +2, +3 …
        seq = [a]
        incs = [s1, s1, s2, s1, s1, s2, s1]
        for i in range(5):
            seq.append(seq[-1] + incs[i])
        ans = seq[-1] + incs[5]
        return mk("deret", lv, _stem(seq), ans, [ans + 1, ans - 1, seq[-1] + s1, ans + 2], f"Pola tingkat: tambah {s1}, {s1}, {s2}, lalu berulang. Setelah {seq[-1]} giliran +{incs[5]}: {ans}.",
                  "Tingkat: selisihnya sendiri berpola (misal 2, 2, 3, 2, 2, 3). Tulis selisih antar suku di bawahnya.", rng)
    n0, c = rng.randint(2, 6), rng.choice([-3, -2, -1, 1, 2, 3, 4])
    seq = [(n0 + i) ** 2 + c for i in range(5)]
    ans = (n0 + 5) ** 2 + c
    return mk("deret", lv, _stem(seq), ans, [ans + 2, ans - 2, (n0 + 5) ** 2, ans + 2 * (n0 + 5) + 1], f"Suku = n² {'+' if c >= 0 else '−'} {abs(c)}. Untuk n = {n0 + 5}: {(n0 + 5) ** 2} {'+' if c >= 0 else '−'} {abs(c)} = {ans}.",
              "Selisih naik 2, 4, 6 … dan angkanya dekat kuadrat sempurna: n² ± konstanta.", rng)


@reg("deret", (2,))
def dr_menengah(lv, rng):
    t = rng.randint(1, 6)
    if t == 1:
        n0, c = rng.randint(1, 4), rng.choice([-1, 0, 1, 2])
        seq = [(n0 + i) ** 3 + c for i in range(5)]
        ans = (n0 + 5) ** 3 + c
        return mk("deret", lv, _stem(seq), ans, [ans + 1, ans - 1, ans + 10, ans - 10], f"Suku = n³ {'+' if c >= 0 else '−'} {abs(c)}. n = {n0 + 5}: {(n0 + 5) ** 3} → {ans}.", "Hafal kubik 1–10: 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000.", rng)
    if t == 2:
        st = rng.randint(0, 8)
        seq = PRIMES[st:st + 5]
        ans = PRIMES[st + 5]
        return mk("deret", lv, _stem(seq), ans, [ans + 2, ans - 2, ans + 4, ans - 4], f"Bilangan prima berurutan; setelah {seq[-1]} adalah {ans}.", "Hafal prima sampai 70: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67.", rng)
    if t == 3:
        k0 = rng.randint(1, 5)
        T = lambda k: k * (k + 1) // 2
        seq = [T(k0 + i) for i in range(5)]
        ans = T(k0 + 5)
        return mk("deret", lv, _stem(seq), ans, [ans + 1, ans - 1, seq[-1] + k0 + 4, seq[-1] + k0 + 6], f"Selisih naik 1 tiap langkah: bilangan segitiga n(n+1)/2. {seq[-1]} + {k0 + 5} = {ans}.", "Selisih naik 1 tiap langkah → bilangan segitiga.", rng)
    if t == 4:
        t0, ad = rng.randint(2, 6), rng.randint(2, 5)
        s = [t0]
        ops = [lambda x: x + ad, lambda x: x * 2]
        for i in range(5):
            s.append(ops[i % 2](s[-1]))
        ans = ops[1](s[-1])
        return mk("deret", lv, _stem(s), ans, [s[-1] + ad, ans + ad, ans - ad, s[-1] * 3], f"Pola: +{ad}, ×2, +{ad}, ×2, … Suku terakhir {s[-1]} × 2 = {ans}.", "Dua operasi bergantian: uji dengan tiga suku pertama.", rng)
    if t == 5:
        a = rng.randint(1, 6)
        seq = [a, a + 1, a + 3, a + 7, a + 15]
        ans = a + 31
        return mk("deret", lv, _stem(seq), ans, [ans + 1, ans - 1, a + 23, a + 30], f"Selisih 1, 2, 4, 8: berlipat dua. Selanjutnya 16: {a + 15} + 16 = {ans}.", "Selisih berlipat dua tiap langkah: suku = a + (2ⁿ − 1).", rng)
    n0 = rng.randint(1, 5)
    seq = [(n0 + i) * (n0 + i + 1) for i in range(5)]
    ans = (n0 + 5) * (n0 + 6)
    return mk("deret", lv, _stem(seq), ans, [ans + 2, ans - 2, (n0 + 5) ** 2, (n0 + 6) ** 2], f"Suku = n(n+1): hasil kali dua bilangan berurutan. {n0 + 5} × {n0 + 6} = {ans}.", "Semua suku genap dan selisih naik 2: n(n+1).", rng)


@reg("deret", (3,))
def dr_sulit(lv, rng):
    t = rng.randint(1, 5)
    if t == 1:
        a = rng.randint(1, 3)
        seq = [a, a, 2 * a, 6 * a, 24 * a]
        ans = 120 * a
        return mk("deret", lv, _stem(seq), ans, [96 * a, 144 * a, ans + a, ans - a], f"Pengali naik: ×1, ×2, ×3, ×4, lalu ×5. {24 * a} × 5 = {ans}.", "Pengali yang ikut naik (×1, ×2, ×3, …) adalah faktorial.", rng)
    if t == 2:
        t0 = rng.randint(2, 5)
        s = [t0]
        ops = [lambda x: x + 2, lambda x: x * 3, lambda x: x - 1]
        for i in range(5):
            s.append(ops[i % 3](s[-1]))
        ans = ops[2](s[-1])
        return mk("deret", lv, _stem(s), ans, [s[-1] + 2, s[-1] * 3, ans + 2, ans - 2], f"Siklus tiga langkah: +2, ×3, −1. Setelah {s[-1]} giliran −1: {ans}.", "Pola tiga langkah berulang: lihat tiga perpindahan pertama, cek apakah berulang.", rng)
    if t == 3:
        while True:
            tb, tc = rng.randint(1, 3), rng.randint(2, 5)
            s = [1, tb, tc]
            for i in range(3):
                s.append(s[-1] + s[-2] + s[-3])
            d1 = [s[i + 1] - s[i] for i in range(5)]
            d2 = [d1[i + 1] - d1[i] for i in range(4)]
            d3 = [d2[i + 1] - d2[i] for i in range(3)]
            if len(set(d3)) > 1:  # hindari deret yang juga cocok sebagai deret selisih ketiga tetap (ambigu)
                break
        ans = s[-1] + s[-2] + s[-3]
        return mk("deret", lv, _stem(s), ans, [s[-1] + s[-2], ans + 1, ans - 1, s[-1] * 2], f"Tiap suku = jumlah tiga suku sebelumnya: {s[-3]} + {s[-2]} + {s[-1]} = {ans}.", "Fibonacci biasa meleset? Coba tiga suku sebelumnya (tribonacci).", rng)
    if t == 4:
        a = rng.randint(3, 8)
        u = [a]
        for i in range(1, 5):
            u.append(2 * u[i - 1] - i)
        ans = 2 * u[4] - 5
        return mk("deret", lv, _stem(u), ans, [2 * u[4], ans + 1, ans - 1, 2 * u[4] - 4], f"Suku = 2 × suku sebelumnya − n (n = 1, 2, 3, …). 2 × {u[4]} − 5 = {ans}.", "Hampir kali 2 tetapi meleset dengan angka yang ikut naik: pola 2t − n.", rng)
    D, s0, k = rng.randint(1, 3), rng.randint(1, 2), rng.randint(1, 2)
    df = [D]
    sd = []
    for i in range(5):
        sd.append(s0 + i * k)
        df.append(df[i] + sd[i])
    tv = rng.randint(1, 9)
    seq = [tv]
    for i in range(5):
        seq.append(seq[i] + df[i])
    ans = seq[5] + df[5]
    return mk("deret", lv, _stem(seq), ans, [seq[5] + df[4], ans + 1, ans - 1, ans + k], f"Selisih: {', '.join(map(str, df[:5]))}. Selisih kedua: {', '.join(map(str, sd[:4]))} (naik {k}). Selisih ketiga tetap {k}. Selisih berikutnya {df[5]}, jadi {seq[5]} + {df[5]} = {ans}.",
              "Selisih pertama dan kedua belum tetap? Hitung selisih ketiga lalu susun mundur.", rng)


ABJAD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@reg("deret", (1, 2, 3))
def dr_huruf(lv, rng):
    if lv == 1:
        st, step = rng.randint(0, 5), rng.randint(2, 4)
        seq = [ABJAD[st + i * step] for i in range(5)]
        idx = st + 5 * step
        ans = ABJAD[idx]
        dis = [ABJAD[idx + o] for o in (-1, 1, -2, 2, -3, 3, -4, 4, -5, 5) if 0 <= idx + o < 26]
        return mk("deret", lv, "Lanjutkan deret huruf: **" + ", ".join(seq) + ", …**", ans, dis, f"Ubah ke angka (A=1 … Z=26): " + ", ".join(str(ABJAD.index(c) + 1) for c in seq) + f". Loncat {step} tiap langkah, berikutnya {ans} ({idx + 1}).",
                  "Ubah huruf jadi angka (A=1 … Z=26); tulis jangkar E=5, J=10, O=15, T=20, Y=25 supaya cepat.", rng)
    if lv == 2:
        a0, d1 = rng.randint(0, 4), rng.randint(2, 3)
        b0, d2 = rng.randint(14, 18), rng.randint(1, 3)
        seq = [ABJAD[a0], ABJAD[b0], ABJAD[a0 + d1], ABJAD[b0 - d2], ABJAD[a0 + 2 * d1], ABJAD[b0 - 2 * d2]]
        idx = a0 + 3 * d1
        ans = ABJAD[idx]
        dis = [ABJAD[idx + o] for o in (-1, 1, -2, 2) if 0 <= idx + o < 26] + [ABJAD[b0 - 3 * d2]]
        return mk("deret", lv, "Lanjutkan deret huruf: **" + ", ".join(seq) + ", …**", ans, dis,
                  f"Dua larik. Larik ganjil: {ABJAD[a0]}, {ABJAD[a0 + d1]}, {ABJAD[a0 + 2 * d1]} (+{d1}). Larik genap: {ABJAD[b0]}, {ABJAD[b0 - d2]}, {ABJAD[b0 - 2 * d2]} (−{d2}). Suku ke-7 mengikuti larik ganjil: {ans}.",
                  "Huruf selang-seling naik dan turun? Pisahkan jadi dua larik, ubah ke angka.", rng)
    st = rng.randint(0, 2)
    kelompok = []
    for i in range(5):
        base = st + i * 3
        kelompok.append((ABJAD[base], ABJAD[base + 1], ABJAD[base + 2]))
    tampil = []
    for i, (x, y, z) in enumerate(kelompok[:-1]):
        tampil.append((z + y + x) if i % 2 == 0 else (x + y + z))
    nxt = kelompok[-1]
    ans = nxt[2] + nxt[1] + nxt[0] if (len(kelompok) - 1) % 2 == 0 else nxt[0] + nxt[1] + nxt[2]
    alt = nxt[0] + nxt[1] + nxt[2] if ans != nxt[0] + nxt[1] + nxt[2] else nxt[2] + nxt[1] + nxt[0]
    return mk("deret", lv, "Lanjutkan deret kelompok huruf: **" + ", ".join(tampil) + ", …**", ans,
              [alt, ABJAD[ABJAD.index(nxt[0]) + 1] + nxt[1] + nxt[2], nxt[0] + nxt[2] + nxt[1], ABJAD[ABJAD.index(nxt[2]) + 1] + nxt[1] + nxt[0], nxt[1] + nxt[0] + nxt[2]],
              f"Tiap kelompok berisi tiga huruf berurutan; kelompok bernomor ganjil ditulis terbalik (mis. {tampil[0]}), yang genap normal ({tampil[1]}). Kelompok berikutnya adalah {ans}.",
              "Kelompok huruf: cek dulu apakah tiga huruf berurutan, lalu apakah urutan ditulis terbalik berselang-seling.", rng)
