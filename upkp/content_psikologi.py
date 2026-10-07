"""Tes Psikologi: pemahaman, number logic, block pattern, DISC, karakteristik pribadi, skala penilaian diri, Pauli.

PENTING: halaman buku bagian ini (hlm. 196 dst.) belum tersedia. Format di bawah adalah PERKIRAAN dari judul
subtes pada daftar isi dan dari format tes psikologi seleksi pada umumnya. Ganti dengan format buku saat
halamannya tersedia. DISC, karakteristik pribadi, dan skala penilaian diri TIDAK punya jawaban benar/salah.
"""
from __future__ import annotations

import random

from .model import Q, mk, mk_svg_opts
from .registry import GENS, reg
from . import figural as _fig  # noqa: F401  (memakai _frame)

# ---------------------------------------------------------------------
# 1. PEMAHAMAN YANG DIBERIKAN (format perkiraan: memahami bacaan/instruksi)
# ---------------------------------------------------------------------
PEMAHAMAN = [
    ("Bacalah teks berikut.\n\n> Kantor pelayanan menerapkan jam kerja pukul 07.30 sampai 16.00. Pegawai yang tiba lebih dari 15 menit setelah jam masuk tercatat terlambat. "
     "Pegawai yang terlambat wajib mengisi formulir keterlambatan.\n\nPegawai yang tiba pukul 07.50 …", "tercatat terlambat dan wajib mengisi formulir",
     ["tidak terlambat karena tiba sebelum pukul 08.00", "tercatat terlambat tetapi tidak perlu mengisi formulir", "wajib pulang pukul 16.30", "tercatat terlambat hanya jika tiba setelah pukul 08.00"],
     "Batas toleransi: 07.30 + 15 menit = 07.45. Pukul 07.50 melewati batas, jadi tercatat terlambat dan wajib mengisi formulir.", "Hitung batas dulu (jam masuk + toleransi), baru bandingkan.", 1),
    ("Bacalah teks berikut.\n\n> Rapat evaluasi dilaksanakan setiap Senin minggu pertama dan Kamis minggu ketiga setiap bulan. Bila hari rapat jatuh pada hari libur nasional, rapat dimajukan satu hari kerja.\n\n"
     "Jika Kamis minggu ketiga jatuh pada hari libur nasional, rapat dilaksanakan pada hari …", "Rabu minggu ketiga", ["Jumat minggu ketiga", "Senin minggu keempat", "Selasa minggu ketiga", "Kamis minggu keempat"],
     "“Dimajukan satu hari kerja” berarti ke hari kerja sebelumnya: dari Kamis menjadi Rabu.", "Dimajukan = lebih awal. Diundurkan = lebih akhir.", 1),
    ("Bacalah instruksi berikut.\n\n> Dari daftar bilangan 4, 7, 12, 15, 18, 21, pilih bilangan yang genap dan habis dibagi 3, lalu jumlahkan.\n\nHasilnya adalah …", "30", ["12", "18", "33", "36"],
     "Genap dan habis dibagi 3: 12 dan 18. Jumlah = 30.", "Terapkan semua syarat sekaligus (genap DAN habis dibagi 3). Baru jumlahkan.", 2),
    ("Bacalah teks berikut.\n\n> Pegawai yang mengikuti pelatihan mendapat nilai akhir dari tiga komponen: ujian tertulis (50%), praktik (30%), dan kehadiran (20%). Seorang peserta mendapat 80 pada ujian tertulis, 70 pada praktik, dan 100 pada kehadiran.\n\nNilai akhir peserta adalah …",
     "81", ["83", "80", "85", "78"], "Nilai = 0,5 × 80 + 0,3 × 70 + 0,2 × 100 = 40 + 21 + 20 = 81.", "Rata-rata berbobot: kali bobot masing-masing, jumlahkan. Bobot harus berjumlah 100%.", 2),
    ("Bacalah teks berikut.\n\n> Tidak semua pegawai yang mengikuti pelatihan lolos sertifikasi. Semua pegawai yang lolos sertifikasi mendapat tunjangan tambahan. Rina mengikuti pelatihan.\n\nPernyataan yang PASTI benar adalah …",
     "Jika Rina lolos sertifikasi, Rina mendapat tunjangan tambahan", ["Rina lolos sertifikasi", "Rina tidak mendapat tunjangan tambahan", "Semua yang mendapat tunjangan mengikuti pelatihan", "Rina tidak lolos sertifikasi"],
     "Hanya hubungan “lolos → tunjangan” yang pasti. Tidak ada informasi apakah Rina lolos.", "Pilih pernyataan bersyarat yang selalu benar, bukan yang menebak fakta.", 3),
]


def _gen_pemahaman(lv, rng):
    pool = [(i, d) for i, d in enumerate(PEMAHAMAN) if d[-1] == lv]
    i, (stem, jawab, dis, exp, trick, _) = rng.choice(pool)
    return mk("pemahaman", lv, stem, jawab, dis, exp, trick, rng, id=f"pemahaman-{i}")


GENS.setdefault("pemahaman", []).append((_gen_pemahaman, (1, 2, 3)))


# ---------------------------------------------------------------------
# 2. NUMBER LOGIC (format perkiraan: pola hubungan antar-angka)
# ---------------------------------------------------------------------
RULES = {
    1: [("a + b", lambda a, b: a + b), ("a × b", lambda a, b: a * b), ("a − b", lambda a, b: a - b)],
    2: [("a × b − a", lambda a, b: a * b - a), ("2a + b", lambda a, b: 2 * a + b), ("a² + b", lambda a, b: a * a + b), ("a + 2b", lambda a, b: a + 2 * b)],
    3: [("a² − b²", lambda a, b: a * a - b * b), ("(a + b) × 2 − a", lambda a, b: (a + b) * 2 - a), ("a × b + a + b", lambda a, b: a * b + a + b), ("a² + b² ", lambda a, b: a * a + b * b)],
}
SEMUA = [r for lvr in RULES.values() for r in lvr]


def _gen_numlogic(lv, rng):
    for _ in range(300):
        nama, f = rng.choice(RULES[lv])
        if lv == 1:
            pairs = [(rng.randint(2, 9), rng.randint(2, 9)) for _ in range(4)]
        else:
            pairs = [(rng.randint(3, 9), rng.randint(2, 8)) for _ in range(4)]
        # semua aturan yang cocok dengan 3 contoh harus tepat satu (aturan yang dipakai)
        cocok = [n for n, g in SEMUA if all(g(a, b) == f(a, b) for a, b in pairs[:3])]
        if len(set(cocok)) == 1 and all(f(a, b) > 0 for a, b in pairs):
            break
    a4, b4 = pairs[3]
    jawab = f(a4, b4)
    contoh = "\n".join(f"- ({a}, {b}) → **{f(a, b)}**" for a, b in pairs[:3])
    stem = f"Perhatikan hubungan angka berikut.\n\n{contoh}\n- ({a4}, {b4}) → **?**\n\nAngka yang menggantikan tanda tanya adalah …"
    exp = f"Aturan yang cocok dengan ketiga contoh: c = {nama.strip()}. Untuk ({a4}, {b4}): {jawab}."
    trick = "Uji aturan sederhana dulu (jumlah, kali, selisih) pada contoh pertama, lalu pastikan aturan itu juga cocok di contoh kedua dan ketiga. Jangan berhenti pada satu contoh."
    dis = [jawab + 1, jawab - 1, jawab + b4, jawab - a4, jawab + 2]
    return mk("numlogic", lv, stem, jawab, dis, exp, trick, rng)


GENS.setdefault("numlogic", []).append((_gen_numlogic, (1, 2, 3)))


# ---------------------------------------------------------------------
# 3. BLOCK PATTERN (format perkiraan: rotasi dan cermin pola kotak)
# ---------------------------------------------------------------------
def _grid_svg(g, warna="#1f3a8f"):
    n = len(g)
    sz = 100 // n
    inner = "".join(
        f'<rect x="{c * sz + 6}" y="{r * sz + 6}" width="{sz - 2}" height="{sz - 2}" fill="{warna if g[r][c] else "#fff"}" stroke="#555" stroke-width="1"/>'
        for r in range(n) for c in range(n)
    )
    return _fig._frame(f'<g transform="translate(-3,-3) scale(0.9)">{inner}</g>')


def _rot(g):  # 90° searah jarum jam
    n = len(g)
    return [[g[n - 1 - c][r] for c in range(n)] for r in range(n)]


def _cermin(g):
    return [row[::-1] for row in g]


def _gen_blockpattern(lv, rng):
    n = 3 if lv == 1 else 4
    for _ in range(500):
        g = [[rng.random() < 0.45 for _ in range(n)] for _ in range(n)]
        variants = [g, _rot(g), _rot(_rot(g)), _rot(_rot(_rot(g))), _cermin(g), _cermin(_rot(g)), _cermin(_rot(_rot(g))), _cermin(_rot(_rot(_rot(g))))]
        keys = {tuple(map(tuple, v)) for v in variants}
        k = rng.choice([1, 2, 3]) if lv >= 2 else 1
        if len(keys) == 8 and 5 <= sum(map(sum, g)) <= n * n - 4:
            break
    target = g
    for _ in range(k):
        target = _rot(target)
    if lv == 3:
        # pilihan benar = pola awal diputar k kali; pengecoh termasuk cermin
        pass
    deg = 90 * k
    benar = target
    kand = [_cermin(target)]
    for j in (1, 2, 3):
        if j != k:
            r = g
            for _ in range(j):
                r = _rot(r)
            kand.append(r)
    ubah = [row[:] for row in target]
    rr, cc = rng.randrange(n), rng.randrange(n)
    ubah[rr][cc] = not ubah[rr][cc]
    kand.append(ubah)
    keys = {tuple(map(tuple, benar))}
    opts = [_grid_svg(benar)]
    for cnd in kand:
        key = tuple(map(tuple, cnd))
        if key not in keys:
            keys.add(key)
            opts.append(_grid_svg(cnd))
        if len(opts) == 5:
            break
    exp = f"Putar pola {deg}° searah jarum jam: baris pertama menjadi kolom terakhir (dibaca dari bawah ke atas). Pengecoh berupa cermin, putaran yang berbeda, atau satu kotak yang berubah."
    trick = "Lacak satu sudut berwarna (pojok kiri atas) untuk melihat arah putarannya, lalu cek satu baris. Cermin membalik kiri-kanan, putaran tidak."
    return mk_svg_opts("blockpattern", lv, f"Pola kotak berikut diputar {deg}° searah jarum jam. Pola manakah yang dihasilkan?", opts, 0, exp, trick, rng, svg=_grid_svg(g))


GENS.setdefault("blockpattern", []).append((_gen_blockpattern, (1, 2, 3)))


# ---------------------------------------------------------------------
# 4. DISC (kuesioner pilihan paksa; tidak ada jawaban benar/salah)
# ---------------------------------------------------------------------
DISC_KATA = {
    "D": ["Tegas", "Berani mengambil risiko", "Kompetitif", "Langsung ke pokok", "Menuntut hasil", "Mandiri", "Cepat memutuskan", "Berorientasi target"],
    "I": ["Ramah", "Antusias", "Meyakinkan orang lain", "Optimis", "Mudah bergaul", "Ekspresif", "Menyukai suasana ramai", "Mudah memotivasi"],
    "S": ["Sabar", "Setia", "Tenang", "Pendengar yang baik", "Mudah bekerja sama", "Konsisten", "Menjaga keharmonisan", "Dapat diandalkan"],
    "C": ["Teliti", "Analitis", "Rapi", "Hati-hati", "Patuh pada aturan", "Mengutamakan akurasi", "Sistematis", "Kritis terhadap detail"],
}
DISC_PENJELASAN = {
    "D": "Dominance: tegas, berorientasi hasil, mengambil keputusan cepat. Waspadai kesan terlalu menekan.",
    "I": "Influence: ramah, persuasif, mudah memotivasi. Waspadai kurang rinci dan kurang tuntas.",
    "S": "Steadiness: sabar, stabil, kooperatif. Waspadai lambat beradaptasi pada perubahan mendadak.",
    "C": "Conscientiousness: teliti, analitis, patuh prosedur. Waspadai terlalu lama menimbang.",
}


def disc_kelompok(rng: random.Random, n=8):
    """Kembalikan n kelompok; tiap kelompok memuat satu kata dari tiap tipe (D, I, S, C)."""
    idx = {t: rng.sample(range(8), n) for t in "DISC"}
    out = []
    for i in range(n):
        item = [(t, DISC_KATA[t][idx[t][i]]) for t in "DISC"]
        rng.shuffle(item)
        out.append(item)
    return out


def hitung_disc(jawaban):
    """jawaban: list of (paling_sesuai_tipe, paling_tidak_sesuai_tipe). Hasil: skor tipe (P - K)."""
    skor = {t: 0 for t in "DISC"}
    for p, k in jawaban:
        skor[p] += 1
        skor[k] -= 1
    return skor


# ---------------------------------------------------------------------
# 5. KARAKTERISTIK PRIBADI dan 6. SKALA PENILAIAN DIRI
# ---------------------------------------------------------------------
KARAKTER = [
    ("Teliti", "Saya memeriksa ulang pekerjaan sebelum menyerahkannya.", False),
    ("Teliti", "Saya sering melewatkan detail kecil dalam pekerjaan saya.", True),
    ("Tanggung jawab", "Saya menyelesaikan tugas tepat waktu walau tidak diawasi.", False),
    ("Tanggung jawab", "Saya cenderung menunda pekerjaan sampai mendekati batas waktu.", True),
    ("Kerja sama", "Saya senang membantu rekan yang kesulitan.", False),
    ("Kerja sama", "Saya lebih suka bekerja sendiri daripada dalam tim.", True),
    ("Ketenangan", "Saya tetap tenang saat menghadapi tekanan.", False),
    ("Ketenangan", "Saya mudah cemas ketika banyak tugas datang bersamaan.", True),
    ("Adaptasi", "Saya cepat menyesuaikan diri dengan aturan atau lingkungan baru.", False),
    ("Adaptasi", "Saya sulit menerima perubahan cara kerja.", True),
    ("Integritas", "Saya mengakui kesalahan saya meskipun tidak ada yang mengetahuinya.", False),
    ("Integritas", "Saya kadang menyesuaikan laporan agar terlihat lebih baik.", True),
]

SKALA = [
    "Saya mampu bekerja di bawah tenggat waktu yang ketat.",
    "Saya mampu menjelaskan sesuatu dengan jelas kepada orang lain.",
    "Saya mampu menerima kritik tanpa tersinggung.",
    "Saya mampu mengambil keputusan dengan data yang tersedia.",
    "Saya mampu bekerja sama dengan orang yang pendapatnya berbeda.",
    "Saya mampu mempelajari hal baru dengan cepat.",
    "Saya mampu menjaga kerahasiaan informasi pekerjaan.",
    "Saya mampu menyelesaikan masalah tanpa menunggu perintah.",
]


def hitung_karakter(nilai: list[int]):
    """nilai: skor 1-5 per butir (urut KARAKTER). Butir negatif dibalik. Kembalikan skor per aspek dan indeks konsistensi."""
    per = {}
    selisih = []
    for (aspek, _, balik), v in zip(KARAKTER, nilai):
        s = 6 - v if balik else v
        per.setdefault(aspek, []).append(s)
    for aspek, lst in per.items():
        if len(lst) == 2:
            selisih.append(abs(lst[0] - lst[1]))
    hasil = {a: sum(l) / len(l) for a, l in per.items()}
    konsisten = 1 - (sum(selisih) / (4 * len(selisih)))
    return hasil, konsisten


# ---------------------------------------------------------------------
# 7. PAULI (kolom angka: jumlahkan dua angka berurutan, tulis angka satuannya)
# ---------------------------------------------------------------------
def pauli_kolom(rng: random.Random, panjang=26):
    d = [rng.randint(0, 9) for _ in range(panjang)]
    jawab = [(d[i] + d[i + 1]) % 10 for i in range(panjang - 1)]
    return d, jawab


def nilai_pauli(masukan: str, jawab: list[int]):
    """Bandingkan masukan (string digit) dengan kunci. Kembalikan (benar, salah, kosong)."""
    s = "".join(ch for ch in masukan if ch.isdigit())
    benar = salah = 0
    for i, k in enumerate(jawab):
        if i < len(s):
            if int(s[i]) == k:
                benar += 1
            else:
                salah += 1
    return benar, salah, len(jawab) - min(len(s), len(jawab))
