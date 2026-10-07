"""Verifikasi mandiri: hitung ulang jawaban soal numerik dari teks soalnya (bukan dari kode generator)."""
import math
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from upkp import numerik_a, numerik_b  # noqa: F401
from upkp.registry import generate


def num(s):
    s = s.replace("Rp", "").replace("°", "").replace("%", "").strip()
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        return int(s.replace(".", ""))
    return float(s.replace(",", "."))


def hm2m(t):
    h, m = t.split(".")
    return int(h) * 60 + int(m)


def opt(q):
    return q.opts[q.ans]


fails, checked = [], {}


def check(tag, q, expect, tol=1e-6):
    checked[tag] = checked.get(tag, 0) + 1
    got = opt(q)
    ok = False
    try:
        ok = abs(num(got) - expect) <= tol
    except Exception:
        ok = str(got) == str(expect)
    if not ok:
        fails.append((tag, q.stem[:150], got, expect))


def run(bab, lv, n=300):
    for i in range(n):
        q = generate(bab, lv, random.Random(i * 97 + lv))
        t = q.stem
        m = None
        # ---------------- operasi
        if (m := re.match(r"FPB dari (\d+) dan (\d+)", t)):
            check("fpb", q, math.gcd(int(m[1]), int(m[2])))
        elif (m := re.match(r"Manakah bilangan berikut yang habis dibagi (\d+)", t)):
            k = int(m[1])
            div = [o for o in q.opts if int(o) % k == 0]
            checked["habis"] = checked.get("habis", 0) + 1
            if len(div) != 1 or div[0] != opt(q):
                fails.append(("habis", t, opt(q), div))
        elif (m := re.match(r"Bentuk paling sederhana dari √(\d+)", t)):
            v = int(m[1])
            a, b = re.match(r"(\d+)√(\d+)", opt(q)).groups()
            checked["akar"] = checked.get("akar", 0) + 1
            if int(a) ** 2 * int(b) != v:
                fails.append(("akar", t, opt(q), v))
        elif (m := re.match(r"Nilai dari \((\d+)\^(\d+) × \d+\^(\d+)\) ÷ \d+\^(\d+)", t)):
            a, mm, n2, p = map(int, m.groups())
            check("eksp", q, a ** (mm + n2 - p))
        elif (m := re.match(r"KPK dua bilangan adalah (\d+) dan FPB-nya (\d+)\. Jika salah satu bilangan itu (\d+)", t)):
            check("kpkfpb", q, int(m[1]) * int(m[2]) / int(m[3]))
        # ---------------- persamaan
        elif (m := re.match(r"Ibu A membeli (\d+) .* dan (\d+) .* seharga (Rp\d{1,3}(?:\.\d{3})*)\. Ibu B membeli (\d+) .* dan (\d+) .* seharga (Rp\d{1,3}(?:\.\d{3})*)\. Harga satu", t)):
            a, b, e1, c, d, e2 = int(m[1]), int(m[2]), num(m[3]), int(m[4]), int(m[5]), num(m[6])
            x = (d * e1 - b * e2) / (a * d - b * c)
            check("spldv2", q, x)
        elif (m := re.search(r"akar-akar persamaan x²( [−+] \d+x)?( [−+] \d+)? = 0, maka (jumlah|hasil kali)", t)):
            b = m[1]; c = m[2]
            S = 0 if not b else (int(re.search(r"\d+", b)[0]) * (1 if "−" in b else -1) * -1)
            S = 0 if not b else (int(re.search(r"\d+", b)[0]) if "−" in b else -int(re.search(r"\d+", b)[0]))
            P = 0 if not c else (int(re.search(r"\d+", c)[0]) if "+" in c else -int(re.search(r"\d+", c)[0]))
            check("kuadrat1", q, S if m[3] == "jumlah" else P)
        elif (m := re.match(r"Himpunan penyelesaian dari (\d+)x ([+−]) (\d+) > (\d+)x ([+−]) (\d+) adalah", t)):
            a, sb, b, c, sd, d = int(m[1]), m[2], int(m[3]), int(m[4]), m[5], int(m[6])
            b = b if sb == "+" else -b
            d = d if sd == "+" else -d
            k = Fraction(d - b, a - c)
            checked["ineq"] = checked.get("ineq", 0) + 1
            if opt(q) != f"x > {k}":
                fails.append(("ineq", t, opt(q), k))
        # ---------------- geometri
        elif (m := re.match(r"Fahmi berlari .* sebanyak (\d+) kali putaran\. Jika jari-jari lapangan (\d+) m", t)):
            n2, r = int(m[1]), int(m[2])
            check("lintasan", q, n2 * 2 * 22 * r / 7)
        elif (m := re.match(r"Roda sepeda berdiameter (\d+) cm berputar sebanyak (\d+) kali", t)):
            check("roda", q, int(m[2]) * 22 * int(m[1]) / 7)
        elif (m := re.match(r"Sebuah tangki .* volume (\d+) cm³ \(π = 22/7\)", t)):
            V = int(m[1]); r = math.sqrt(V * 7 / (22 * 10))
            check("tabung", q, r)
        elif (m := re.match(r"Dua kubus .* berselisih (\d+) cm dan luas permukaannya berselisih (\d+) cm²", t)):
            d, S = int(m[1]), int(m[2])
            s2 = S / 6 / d
            check("kubus", q, (s2 + d) / 2)
        elif (m := re.match(r"Sebuah balok berukuran (\d+) cm × (\d+) cm × (\d+) cm", t)):
            p, l, tt = map(int, m.groups())
            check("diagruang", q, math.sqrt(p * p + l * l + tt * tt))
        elif (m := re.match(r"Tangga sepanjang (\d+) m .* dinding (\d+) m", t)):
            check("tangga", q, math.sqrt(int(m[1]) ** 2 - int(m[2]) ** 2))
        # ---------------- aritsos
        elif (m := re.match(r"Suku pertama barisan aritmatika adalah (\d+) dan bedanya (\d+)\. Suku ke-(\d+)", t)):
            a, b, n2 = map(int, m.groups()); check("un", q, a + (n2 - 1) * b)
        elif (m := re.match(r"Jumlah (\d+) suku pertama deret aritmatika dengan suku pertama (\d+) dan beda (\d+)", t)):
            n2, a, b = map(int, m.groups()); check("sn", q, n2 * (2 * a + (n2 - 1) * b) / 2)
        elif (m := re.match(r"Jumlah (\d+) suku pertama deret aritmatika adalah (\d+)\. Jika suku pertamanya (\d+)", t)):
            n2, S, a = map(int, m.groups()); check("un_dari_sn", q, 2 * S / n2 - a)
        elif (m := re.match(r"Jumlah (\d+) suku pertama deret geometri (\d+) \+ (\d+)", t)):
            n2, a, a2 = map(int, m.groups()); r = a2 // a; check("sngeo", q, a * (r ** n2 - 1) / (r - 1))
        elif (m := re.match(r"Jumlah semua bilangan di antara (\d+) dan (\d+) yang habis dibagi (\d+)", t)):
            lo, hi, k = map(int, m.groups()); check("kelipatan", q, sum(x for x in range(lo + 1, hi) if x % k == 0))
        elif (m := re.match(r"Antara bilangan (\d+) dan (\d+) disisipkan (\d+) bilangan", t)):
            a, b, k = map(int, m.groups()); check("sisip", q, (k + 2) * (a + b) / 2)
        elif (m := re.match(r"Ani menabung (Rp\d{1,3}(?:\.\d{3})*) dengan bunga tunggal (\d+)% per tahun\. Setelah (\d+) bulan", t)):
            M, p, n2 = num(m[1]), int(m[2]), int(m[3]); check("bunga", q, M * (1 + p * n2 / 1200))
        elif (m := re.match(r"Setelah ditabung (\d+) bulan dengan bunga tunggal (\d+)% per tahun, tabungan Budi menjadi (Rp\d{1,3}(?:\.\d{3})*)", t)):
            n2, p, S = int(m[1]), int(m[2]), num(m[3]); check("bunga_mundur", q, S / (1 + p * n2 / 1200))
        elif (m := re.match(r"Seorang pedagang membeli satu karung gula pasir bruto (\d+) kg, tara (\d+)%, dengan harga (Rp\d{1,3}(?:\.\d{3})*)\. Semua gula dijual Rp([\d.]+) per kg", t)):
            br, tr, H, J = int(m[1]), int(m[2]), num(m[3]), num(m[4]); check("brutotara", q, br * (100 - tr) / 100 * J - H)
        # ---------------- sudut
        elif (m := re.match(r"Besar sudut terkecil yang dibentuk jarum pendek dan jarum panjang pada pukul (\d+)\.(\d+)", t)):
            h, mi = int(m[1]), int(m[2]); d = abs(30 * h - 5.5 * mi); d = 360 - d if d > 180 else d
            check("jam", q, d)
        elif (m := re.match(r"Dari (\d+) siswa, (\d+) siswa senang matematika, (\d+) siswa senang fisika, dan (\d+) siswa senang keduanya", t)):
            S, A, B, AB = map(int, m.groups()); check("venn1", q, S - (A + B - AB))
        elif (m := re.match(r"Dari (\d+) siswa, (\d+) gemar olahraga\. Di antara penggemar olahraga, (\d+) siswa juga gemar musik\. Jika (\d+) siswa tidak", t)):
            S, A, AB, L = map(int, m.groups()); check("venn2", q, S - A + AB - L)
        elif (m := re.match(r"Dari (\d+) siswa, (\d+) gemar olahraga, (\d+) gemar musik, dan (\d+) siswa tidak gemar keduanya", t)):
            S, A, B, L = map(int, m.groups()); AB = A + B + L - S; check("venn3", q, B - AB)
        # ---------------- banding
        elif (m := re.match(r"Siti membeli (\d+) kg buah naga seharga (Rp\d{1,3}(?:\.\d{3})*)\. .* (\d+) kg", t)):
            n1, h, n2 = int(m[1]), num(m[2]), int(m[3]); check("senilai", q, h * n2 / n1)
        elif (m := re.match(r"Suatu pekerjaan dapat diselesaikan oleh (\d+) pekerja dalam (\d+) hari\. Jika pekerjanya (\d+) orang", t)):
            w1, d, w2 = map(int, m.groups()); check("berbalik", q, w1 * d / w2)
        elif (m := re.match(r"Sebuah jam dinding \(12 jam\) setiap hari terlambat (\d+) menit", t)):
            check("jam_terlambat", q, 720 / int(m[1]))
        elif (m := re.match(r"Proyek ditargetkan selesai dalam (\d+) hari oleh (\d+) pekerja\. Setelah (\d+) hari proyek dihentikan (\d+) hari", t)):
            D, W, d1, s = map(int, m.groups()); check("proyek", q, (D - d1) * W / (D - d1 - s) - W)
        elif (m := re.match(r"Jarak dua kota sebenarnya (\d+) km\. Pada peta dengan skala 1 : ([\d.]+)", t)):
            km, sk = int(m[1]), int(m[2].replace(".", "")); check("skala", q, km * 100000 / sk, 0.01)
        # ---------------- jarak
        elif (m := re.match(r"Jarak rumah Andi dan Budi (\d+) km\. Andi berkendara .* pukul (\d+\.\d+) dengan kecepatan (\d+) km/jam .* (\d+) km/jam\. Mereka", t)):
            S, t0, v1, v2 = int(m[1]), hm2m(m[2]), int(m[3]), int(m[4]); ans = t0 + S / (v1 + v2) * 60
            checked["papasan1"] = checked.get("papasan1", 0) + 1
            if hm2m(opt(q)) != round(ans): fails.append(("papasan1", t, opt(q), ans))
        elif (m := re.match(r"Jarak rumah Arman dan Danu (\d+) km\. Arman berangkat pukul (\d+\.\d+) dengan (\d+) km/jam .* Danu berangkat (\d+) menit kemudian dengan (\d+) km/jam", t)):
            S, t0, v1, d, v2 = int(m[1]), hm2m(m[2]), int(m[3]), int(m[4]), int(m[5]); ans = t0 + d + (S - v1 * d / 60) / (v1 + v2) * 60
            checked["papasan2"] = checked.get("papasan2", 0) + 1
            if hm2m(opt(q)) != round(ans): fails.append(("papasan2", t, opt(q), ans))
        elif (m := re.match(r"Lina berangkat pukul (\d+\.\d+) dengan kecepatan (\d+) km/jam\. Leni berangkat (\d+) menit kemudian .* kecepatan (\d+) km/jam", t)):
            t0, v1, sel, v2 = hm2m(m[1]), int(m[2]), int(m[3]), int(m[4]); ans = t0 + sel + (v1 * sel / 60) / (v2 - v1) * 60
            checked["menyusul"] = checked.get("menyusul", 0) + 1
            if hm2m(opt(q)) != round(ans): fails.append(("menyusul", t, opt(q), ans))
        elif (m := re.match(r"Andi dapat mengisi kolam ikan dalam (\d+) menit, Bedu dalam (\d+) menit, dan Catur dalam (\d+) menit", t)):
            a, b, c = map(int, m.groups()); check("kolam", q, 1 / (1 / a + 1 / b + 1 / c))
        elif (m := re.match(r"Pipa A dapat mengisi bak air hingga penuh dalam (\d+) jam, sedangkan pipa B dapat menguras bak penuh dalam (\d+) jam", t)):
            x, y = int(m[1]), int(m[2]); check("bak", q, 1 / (1 / x - 1 / y))
        elif (m := re.match(r"Dodi berangkat dari kota A pukul (\d+\.\d+) dan tiba di kota B pukul (\d+\.\d+)\. .* kecepatan (\d+) km/jam dan berhenti selama (\d+) jam", t)):
            a, b, v, h = hm2m(m[1]), hm2m(m[2]), int(m[3]), int(m[4]); check("berhenti", q, v * ((b - a) / 60 - h))
        elif (m := re.match(r"Seseorang menempuh (\d+) km dalam ([\d,]+) jam\. Agar tiba ([\d,]+) jam lebih cepat", t)):
            s, t1, l = int(m[1]), num(m[2]), num(m[3]); check("lebihcepat", q, s / (t1 - l) - s / t1)
        # ---------------- peluang
        elif (m := re.match(r"Dua dadu dilempar bersamaan\. Peluang munculnya jumlah kedua mata dadu sama dengan (\d+) adalah", t)):
            k = int(m[1]); c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == k); f = Fraction(c, 36)
            checked["dadu"] = checked.get("dadu", 0) + 1
            if opt(q) != (f"{f.numerator}/{f.denominator}"): fails.append(("dadu", t, opt(q), f))
        elif (m := re.match(r"Nomor antrian terdiri atas (\d+) angka berbeda .* sampai (\d+)\.", t)):
            check("perm", q, math.perm(int(m[2]), int(m[1])))
        elif (m := re.match(r"(\d+) orang duduk berjajar di \d+ kursi\. Jika dua orang", t)):
            n2 = int(m[1]); check("tdkdampingan", q, math.factorial(n2) - 2 * math.factorial(n2 - 1))
        elif (m := re.match(r"Ani akan mengundang (\d+) dari (\d+) temannya", t)):
            k, n2 = int(m[1]), int(m[2]); check("undang", q, math.comb(n2, k) - math.comb(n2 - 2, k - 2))
        elif (m := re.match(r"Dari (\d+) buku matematika, (\d+) buku fisika, dan (\d+) buku kimia", t)):
            a, b, c = map(int, m.groups()); check("buku", q, math.comb(a, 2) * math.comb(b, 2) * c)
        elif (m := re.match(r"Sebuah kantong berisi (\d+) kelereng hitam, (\d+) kelereng putih.* adalah (\d+)/(\d+)\. Banyak", t)):
            h, p, nu, de = map(int, m.groups()); x = Fraction(nu * (h + p), de - nu); check("abu", q, x)
        # ---------------- statistika
        elif (m := re.match(r"Diketahui data: ([\d, ]+)\. Nilai (rata-rata|median|modus)", t)):
            data = sorted(int(v) for v in m[1].split(", ")); n2 = len(data)
            mean = Fraction(sum(data), n2); med = Fraction(data[n2 // 2]) if n2 % 2 else Fraction(data[n2 // 2 - 1] + data[n2 // 2], 2)
            mode = max(set(data), key=data.count)
            v = {"rata-rata": mean, "median": med, "modus": Fraction(mode)}[m[2]]
            check("stat1", q, float(v), 0.01)
        elif (m := re.match(r"Rata-rata (\d+) bilangan bulat non-negatif yang berbeda adalah (\d+)", t)):
            n2, mm = int(m[1]), int(m[2]); check("terbesar", q, n2 * mm - sum(range(n2 - 1)))
        elif (m := re.match(r"Rata-rata nilai (\d+) siswa laki-laki adalah (\d+) dan rata-rata nilai (\d+) siswa perempuan adalah (\d+)", t)):
            n1, m1, n2, m2 = map(int, m.groups()); check("gabungan", q, (n1 * m1 + n2 * m2) / (n1 + n2), 0.01)
        # ---------------- tabel statistik, ganjil, zona waktu, komplemen
        elif t.startswith("Perhatikan tabel berikut.") and (("Rata-rata nilai pada tabel" in t) or ("Median dari data" in t)):
            rows = [(int(a), int(b), int(f)) for a, b, f in re.findall(r"\| (\d+) – (\d+) \| (\d+) \|", t)]
            n2 = sum(f for _, _, f in rows)
            if "Rata-rata" in t:
                check("tabel_mean", q, sum((a + b) / 2 * f for a, b, f in rows) / n2, 0.01)
            else:
                cum = 0
                for a, b, f in rows:
                    if cum + f >= n2 / 2:
                        check("tabel_median", q, (a - 0.5) + ((n2 / 2 - cum) / f) * 10, 0.01)
                        break
                    cum += f
        elif (m := re.match(r"Banyak bilangan ganjil lima angka yang memuat semua angka ([\d, ]+) \(", t)):
            d = [int(x) for x in m[1].split(", ")]; check("ganjil5", q, sum(1 for x in d if x % 2) * math.factorial(len(d) - 1))
        elif (m := re.match(r"Waktu di kota A adalah (\d+) jam lebih cepat daripada di kota B\. Sebuah pesawat berangkat dari kota A pukul (\d+\.\d+) \(waktu A\) dan tiba di kota B pukul (\d+\.\d+) \(waktu B\)", t)):
            d, x, y = int(m[1]), hm2m(m[2]), hm2m(m[3]); check("zona_durasi", q, (y + d * 60 - x) / 60)
        elif (m := re.match(r"Waktu di kota A adalah (\d+) jam lebih cepat daripada di kota B\. Sebuah pesawat berangkat dari kota A pukul (\d+\.\d+) \(waktu A\) .* tiba (\d+) jam kemudian", t)):
            d, x, dur = int(m[1]), hm2m(m[2]), int(m[3]); checked["zona_tiba"] = checked.get("zona_tiba", 0) + 1
            if hm2m(opt(q)) != x + dur * 60 - d * 60: fails.append(("zona_tiba", t, opt(q), x + dur * 60 - d * 60))
        elif (m := re.match(r"Dalam suatu kompetisi, peluang tim A menjadi juara (\d+) kali peluang tim B\. Jika peluang tim B tidak menjadi juara adalah (\d+)/(\d+)", t)):
            k, nu, de = map(int, m.groups()); f = 1 - k * (1 - Fraction(nu, de)); checked["komplemen"] = checked.get("komplemen", 0) + 1
            if opt(q) != f"{f.numerator}/{f.denominator}": fails.append(("komplemen", t, opt(q), f))
        # ---------------- pemeriksaan tambahan
        elif (m := re.match(r"Di sebuah taman, (.*)\. Pukul (\d+\.\d+) semua lampu menyala bersamaan\. .* untuk (pertama kali|kedua kalinya)", t)):
            sets = [int(x) for x in re.findall(r"tiap (\d+) menit", m[1])]
            L = 1
            for x in sets:
                L = L * x // math.gcd(L, x)
            kali = 1 if m[3] == "pertama kali" else 2
            checked["kpklampu"] = checked.get("kpklampu", 0) + 1
            if hm2m(opt(q)) != hm2m(m[2]) + kali * L:
                fails.append(("kpklampu", t, opt(q), hm2m(m[2]) + kali * L))
        elif (m := re.match(r"Manakah bilangan yang nilainya (terkecil|terbesar)\?", t)):
            pass
        elif (m := re.search(r"akar-akar persamaan x²( [−+] \d+x)?( [−+] \d+)? = 0, nilai x₁² \+ x₂²", t)):
            b = m[1]; c = m[2]
            S = 0 if not b else (int(re.search(r"\d+", b)[0]) if "−" in b else -int(re.search(r"\d+", b)[0]))
            P = 0 if not c else (int(re.search(r"\d+", c)[0]) if "+" in c else -int(re.search(r"\d+", c)[0]))
            check("kuadrat2", q, S * S - 2 * P)
        elif (m := re.match(r"Harga 2 kg mangga, 2 kg jeruk, dan 1 kg anggur adalah (Rp\d{1,3}(?:\.\d{3})*)\. Harga 1 kg mangga, 2 kg jeruk, dan 2 kg anggur adalah (Rp\d{1,3}(?:\.\d{3})*)\. Harga 2 kg mangga, 2 kg jeruk, dan 3 kg anggur adalah (Rp\d{1,3}(?:\.\d{3})*)", t)):
            e1, e2, e3 = num(m[1]), num(m[2]), num(m[3])
            A = (e3 - e1) / 2; M = e1 - e2 + A; J = (e1 - 2 * M - A) / 2
            check("spltv", q, J)
        elif (m := re.match(r"Pertidaksamaan \(x − \((-?\d+)\)\)\(x − (-?\d+)\) < 0", t)):
            p1, p2 = int(m[1]), int(m[2]); checked["ineqkuad"] = checked.get("ineqkuad", 0) + 1
            if opt(q) != f"{min(p1, p2)} < x < {max(p1, p2)}": fails.append(("ineqkuad", t, opt(q), (p1, p2)))
        elif (m := re.match(r"Sebuah papan tulis .* keliling (\d+) cm\. Jika panjang salah satu sisinya (\d+) cm", t)):
            K, a = int(m[1]), int(m[2]); check("luas_pp", q, a * (K // 2 - a))
        elif (m := re.match(r"Panjang sebuah persegi panjang (\d+) kali lebarnya dan luasnya (\d+) cm²", t)):
            k, L = int(m[1]), int(m[2]); l = math.sqrt(L / k); check("keliling_pp", q, 2 * (k * l + l))
        elif (m := re.match(r"Sebuah kolam persegi dengan sisi (\d+) m dikelilingi jalan setapak selebar (\d+) m", t)):
            a, w = int(m[1]), int(m[2]); check("jalan", q, (a + 2 * w) ** 2 - a * a)
        elif (m := re.match(r"Sebuah toko memberi diskon (\d+)% lalu diskon lagi (\d+)% untuk sebuah baju seharga (Rp\d{1,3}(?:\.\d{3})*)", t)):
            a, b, H = int(m[1]), int(m[2]), num(m[3]); check("diskon2", q, H * (1 - (1 - a / 100) * (1 - b / 100)))
        elif (m := re.match(r"Sejenis bakteri membelah diri menjadi 2 setiap hari\. Wadah berisi setengah penuh pada hari ke-(\d+)\. .* berisi (setengah|seperempat|seperdelapan) penuh", t)):
            n2 = int(m[1]); k = {"setengah": 0, "seperempat": 1, "seperdelapan": 2}[m[2]]; checked["bakteri"] = checked.get("bakteri", 0) + 1
            if opt(q) != f"Hari ke-{n2 - k}": fails.append(("bakteri", t, opt(q), n2 - k))
        elif (m := re.match(r"Dua dadu dilempar bersamaan\. Peluang munculnya jumlah mata dadu paling sedikit (\d+) adalah", t)):
            k = int(m[1]); c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= k); f = Fraction(c, 36); checked["dadu2"] = checked.get("dadu2", 0) + 1
            if opt(q) != f"{f.numerator}/{f.denominator}": fails.append(("dadu2", t, opt(q), f))
        elif (m := re.match(r"Sebuah dadu dilempar sebanyak (\d+) kali\. Frekuensi harapan", t)):
            check("fh_dadu", q, int(m[1]) / 6)
        elif (m := re.match(r"Sebuah kotak berisi kertas bertuliskan huruf A sampai ([A-Z]) .* Dari (\d+) pengambilan", t)):
            akhir = ord(m[1]) - 64; vok = sum(1 for ch in "AEIOU" if ord(ch) - 64 <= akhir); check("vokal", q, vok * int(m[2]) / akhir)
        elif (m := re.match(r"Sebuah konveksi punya (\d+) karyawan yang dapat menyelesaikan (\d+) pesanan baju dalam (\d+) hari\. .* untuk (\d+) pesanan yang harus selesai dalam (\d+) hari", t)):
            o1, p1, h1, p2, h2 = map(int, m.groups()); check("konveksi", q, p2 * o1 * h1 / (p1 * h2))
        elif (m := re.match(r"Sebuah kendaraan menempuh (\d+) m dalam (\d+) menit, lalu (\d+) m dalam (\d+) menit, dan (\d+) m dalam (\d+) menit terakhir", t)):
            a1, b1, a2, b2, a3, b3 = map(int, m.groups()); check("ratarata_seg", q, (a1 + a2 + a3) / (b1 + b2 + b3), 0.01)
        elif (m := re.match(r"Ada empat bilangan; yang terkecil (\d+) dan yang terbesar (\d+)\.", t)):
            lo, hi = int(m[1]), int(m[2]); mn, mx = (3 * lo + hi) / 4, (lo + 3 * hi) / 4
            vals = [num(o) for o in q.opts]; keluar = [v for v in vals if v < mn - 1e-9 or v > mx + 1e-9]
            checked["rentang"] = checked.get("rentang", 0) + 1
            if len(keluar) != 1 or abs(keluar[0] - num(opt(q))) > 1e-9: fails.append(("rentang", t, opt(q), (mn, mx, vals)))
        elif (m := re.match(r"Dua garis sejajar dipotong oleh sebuah garis\. Sudut sehadap dengan sudut (\d+)° besarnya \(x·(\d+)\)° dan sudut yang berpelurus dengannya besarnya \(x \+ (\d+)y\)°", t)):
            th, A, B = map(int, m.groups()); x = th / A; y = (180 - th - x) / B
            checked["sudut_sejajar"] = checked.get("sudut_sejajar", 0) + 1
            if opt(q) != f"{int(x)}° dan {int(y)}°" or abs(x - int(x)) > 1e-9 or abs(y - int(y)) > 1e-9: fails.append(("sudut_sejajar", t, opt(q), (x, y)))



def run_all(n=300):
    for bab in ["operasi", "persamaan", "geometri", "aritsos", "sudut", "banding", "jarak", "peluang", "statistika", "deret"]:
        for lv in (1, 2, 3):
            try:
                run(bab, lv, n)
            except KeyError:
                pass
    return checked, fails


if __name__ == "__main__":
    c, f = run_all()
    print("diperiksa:", dict(sorted(c.items())))
    print("GAGAL:", len(f))
    for x in f[:25]:
        print(x)
