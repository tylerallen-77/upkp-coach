"""Pembangkit soal otomatis dari basis fakta (`faktabase.py`).

Satu fakta dapat menghasilkan banyak soal: tiap pembangkit memilih fakta, mengocok pengecoh dari fakta lain,
dan menyusun pembahasan dari fakta itu sendiri. Menambah fakta di `faktabase.py` otomatis menambah soal.
"""
from __future__ import annotations

import random

from . import faktabase as fb
from .model import mk
from .registry import reg


def _ambil(pool, k, rng, exclude=()):
    """Ambil k elemen berbeda dari pool (di luar `exclude`)."""
    cand = []
    for x in pool:
        if x not in exclude and x not in cand:
            cand.append(x)
    rng.shuffle(cand)
    return cand[:k]


def _dekat(items, lv, rng, kunci=lambda x: x):
    """Pilih elemen dengan tingkat sama; bila tak ada, pilih yang paling dekat."""
    ada = sorted({kunci(x) for x in items}, key=lambda t: abs(t - lv))
    sama = [x for x in items if kunci(x) == ada[0]]
    return rng.choice(sama)


# =====================================================================
# REGULASI
# =====================================================================
def _reg_bab(bab):
    return [r for r in fb.REGULASI_FAKTA if r[3] == bab]


def _reg_t1(bab):
    """Nomor peraturan → judul."""
    def gen(lv, rng):
        fakta = _reg_bab(bab)
        r = _dekat(fakta, lv, rng, lambda x: x[4])
        kunci, nomor, judul, _, _, sumber, _ = r
        # pengecoh: judul peraturan lain, tidak boleh mengandung/dikandung judul benar
        lain = [x[2] for x in fb.REGULASI_FAKTA if x[0] != kunci and judul not in x[2] and x[2] not in judul]
        sama_bab = [x[2] for x in fb.REGULASI_FAKTA if x[3] == bab and x[0] != kunci and judul not in x[2] and x[2] not in judul]
        dis = _ambil(sama_bab, 2, rng) + _ambil(lain, 4, rng, exclude=set())
        stem = f"**{nomor}** mengatur tentang …"
        exp = f"{nomor} mengatur {judul}." + (" (Isi dari pengetahuan umum; cocokkan dengan buku.)" if sumber == "umum" else "")
        return mk(bab, lv, stem, judul, dis, exp, "Hafal nomor bersama topiknya, bukan nomornya saja. Jenis peraturan (UU, PP, Perpres, PMK, KMK, SE) memberi petunjuk tingkat dan pembuatnya.", rng, id=f"{bab}-f-reg1-{kunci}")
    gen.__name__ = f"fakta_reg1_{bab}"
    return gen


def _reg_t2(bab):
    """Judul → nomor peraturan."""
    def gen(lv, rng):
        fakta = [r for r in _reg_bab(bab) if r[6]]
        r = _dekat(fakta, lv, rng, lambda x: x[4])
        kunci, nomor, judul, _, _, sumber, _ = r
        bentrok = lambda x: judul in x[2] or x[2] in judul  # judul yang saling memuat: kedua nomor bisa dianggap benar
        lain = [x[1] for x in fb.REGULASI_FAKTA if x[0] != kunci and not bentrok(x)]
        sama_bab = [x[1] for x in fb.REGULASI_FAKTA if x[3] == bab and x[0] != kunci and not bentrok(x)]
        dis = _ambil(sama_bab, 2, rng) + _ambil(lain, 4, rng)
        stem = f"Peraturan yang berjudul/mengatur tentang “{judul}” adalah …"
        exp = f"{judul} diatur dalam {nomor}." + (" (Isi dari pengetahuan umum; cocokkan dengan buku.)" if sumber == "umum" else "")
        return mk(bab, lv, stem, nomor, dis, exp, "Cari kata kunci topik (disiplin, cuti, karier, budaya) lalu cocokkan dengan peraturan yang kamu hafal untuk topik itu.", rng, id=f"{bab}-f-reg2-{kunci}")
    gen.__name__ = f"fakta_reg2_{bab}"
    return gen


for _b in ["kepegawaian", "etika", "nilai", "keuangan", "struktur"]:
    reg(_b, (1, 2, 3))(_reg_t1(_b))
    reg(_b, (1, 2, 3))(_reg_t2(_b))


@reg("kepegawaian", (2, 3))
def reg_supersesi(lv, rng):
    pool = [s for s in fb.SUPERSESI if s[3] <= lv] or fb.SUPERSESI
    lama, baru, topik, _ = rng.choice(pool)
    if rng.random() < 0.5:
        semua = [r[1] for r in fb.REGULASI_FAKTA if r[1] != baru] + [s[0] for s in fb.SUPERSESI if s[0] != lama]
        dis = _ambil(semua, 4, rng)
        stem = f"**{lama}** tentang {topik} telah digantikan oleh …"
        return mk("kepegawaian", lv, stem, baru, dis, f"{lama} dicabut dan digantikan {baru}.", "Hafal rantai: UU ASN 5/2014 → 20/2023; disiplin PNS 53/2010 → 94/2021.", rng, id=f"kepegawaian-f-sup1-{lama}")
    semua = [r[1] for r in fb.REGULASI_FAKTA if r[1] != lama and r[1] != baru] + [s[1] for s in fb.SUPERSESI if s[1] != baru]
    dis = _ambil(semua, 4, rng)
    stem = f"**{baru}** tentang {topik} menggantikan peraturan …"
    return mk("kepegawaian", lv, stem, lama, dis, f"{baru} menggantikan {lama}.", "Peraturan baru mencabut yang lama. Cek tahun: yang lebih baru adalah penggantinya.", rng, id=f"kepegawaian-f-sup2-{baru}")


@reg("kepegawaian", (3,))
def reg_pasangan_benar(lv, rng):
    """Pasangan peraturan–isi yang BENAR (pengecoh: isi ditukar)."""
    fakta = [r for r in fb.REGULASI_FAKTA if r[3] in ("kepegawaian", "etika", "nilai") and r[6]]
    benar, *salah_src = rng.sample(fakta, 5)
    opsi_salah = []
    for i, r in enumerate(salah_src):
        tukar = salah_src[(i + 1) % len(salah_src)]
        opsi_salah.append(f"{r[1]} – {tukar[2]}")
    stem = "Pasangan peraturan dan isinya yang **benar** adalah …"
    exp = f"{benar[1]} mengatur {benar[2]}. Pengecoh sengaja menukar isi antarperaturan."
    return mk("kepegawaian", lv, stem, f"{benar[1]} – {benar[2]}", opsi_salah, exp, "Cek satu peraturan yang paling kamu yakini, lalu coret opsi yang memasangkannya dengan isi lain.", rng, id=f"kepegawaian-f-pas-{benar[0]}-{rng.randrange(10**6)}")


_KEPEG = ["uu20-2023", "pp94-2021", "pp11-2017", "pp17-2020", "pp42-2004", "pmk190-2018", "bkn24-2017", "se15-2018", "se4-2019", "pmk224-2020", "pmk216-2018", "pmk123-2023"]
_ORG = ["perpres158-2024", "pmk124-2024", "perpres140-2024", "uu39-2008"]
_KEU = ["uu17-2003", "uu1-2004", "uu15-2004"]
_LAIN = {"kepegawaian": _ORG + _KEU + ["kmk942-2019"], "organisasi": _KEPEG + _KEU + ["kmk942-2019"]}


@reg("keuangan", (2, 3))
def reg_kelompok_bab(lv, rng):
    """Peraturan yang BUKAN bidang tertentu. Keanggotaan kelompok ditetapkan eksplisit agar tidak ambigu."""
    kelompok = rng.choice(["kepegawaian", "organisasi"])
    anggota_k = _KEPEG if kelompok == "kepegawaian" else _ORG
    peta = {r[0]: r for r in fb.REGULASI_FAKTA}
    four = [peta[k] for k in rng.sample(anggota_k, 4)]
    aneh = peta[rng.choice(_LAIN[kelompok])]
    nama = {"kepegawaian": "kepegawaian dan etika PNS", "organisasi": "organisasi kementerian"}[kelompok]
    fmt = lambda r: f"{r[1]} ({r[2][:48] + ('…' if len(r[2]) > 48 else '')})"
    stem = f"Peraturan berikut berkaitan dengan bidang **{nama}**, KECUALI …"
    exp = f"{aneh[1]} mengatur {aneh[2]}, yang termasuk bidang lain. Keempat lainnya berkaitan dengan {nama}."
    return mk("keuangan", lv, stem, fmt(aneh), [fmt(r) for r in four], exp, "Tentukan bidang tiap peraturan dari judulnya, lalu cari yang berbeda bidang.", rng, id=f"keuangan-f-kec-{aneh[0]}-{kelompok}-{rng.randrange(10**6)}")


# =====================================================================
# NILAI-NILAI KEMENKEU DAN PROGRAM BUDAYA
# =====================================================================
@reg("nilai", (1, 2))
def nilai_perilaku_ke_nilai(lv, rng):
    pasangan = [(p, n) for n, d in fb.NILAI_KEMENKEU.items() for p in d["perilaku"]]
    p, n = rng.choice(pasangan)
    dis = [x for x in fb.NILAI_KEMENKEU if x != n]
    stem = f"Perilaku utama “**{p}**” termasuk dalam nilai Kementerian Keuangan …"
    return mk("nilai", lv, stem, n, dis, f"“{p}” adalah perilaku utama nilai {n}.", "Cocokkan kata kunci perilaku: jujur, transparan → Integritas; cerdas, tuntas → Profesionalisme; sangka baik, saling percaya → Sinergi; kepuasan pemangku kepentingan → Pelayanan.", rng, id=f"nilai-f-p2n-{p}")


@reg("nilai", (1, 2, 3))
def nilai_definisi_ke_nilai(lv, rng):
    n = rng.choice(list(fb.NILAI_KEMENKEU))
    stem = f"“{fb.NILAI_KEMENKEU[n]['def']}” merupakan definisi nilai …"
    return mk("nilai", lv, stem, n, [x for x in fb.NILAI_KEMENKEU if x != n], f"Definisi tersebut adalah nilai {n}.", "Kata kunci definisi: kode etik/moral → Integritas; tuntas, akurat, kompetensi → Profesionalisme; kerja sama internal dan kemitraan → Sinergi; kepuasan pemangku kepentingan → Pelayanan; perbaikan → Kesempurnaan.", rng, id=f"nilai-f-d2n-{n}")


@reg("nilai", (2, 3))
def nilai_bukan_perilaku(lv, rng):
    n = rng.choice([x for x, d in fb.NILAI_KEMENKEU.items() if len(d["perilaku"]) >= 4])
    anggota = rng.sample(fb.NILAI_KEMENKEU[n]["perilaku"], 4)
    lain = [p for x, d in fb.NILAI_KEMENKEU.items() if x != n for p in d["perilaku"]]
    aneh = rng.choice(lain)
    asal = [x for x, d in fb.NILAI_KEMENKEU.items() if aneh in d["perilaku"]][0]
    stem = f"Berikut adalah perilaku utama nilai **{n}**, KECUALI …"
    return mk("nilai", lv, stem, aneh, anggota, f"“{aneh}” adalah perilaku utama nilai {asal}, bukan {n}.", "Tentukan dulu nilai yang ditanya, lalu cari perilaku yang kata kuncinya milik nilai lain.", rng, id=f"nilai-f-bukan-{n}-{aneh}")


@reg("nilai", (1, 2, 3))
def budaya_program(lv, rng):
    prog, maksud = rng.choice(fb.PROGRAM_BUDAYA)
    if rng.random() < 0.5:
        stem = f"Program budaya Kementerian Keuangan (KMK 127/KMK.01/2013) yang dimaksudkan untuk {maksud} adalah …"
        dis = [p for p, _ in fb.PROGRAM_BUDAYA if p != prog]
        return mk("nilai", lv, stem, prog, dis, f"Program “{prog}” bertujuan {maksud}.", "Ingat 1-2-3: Satu informasi, Dua menit, Tiga salam; lalu PDCA dan 5R.", rng, id=f"nilai-f-prog1-{prog}")
    stem = f"Program budaya “**{prog}**” dimaksudkan untuk …"
    dis = [m for p, m in fb.PROGRAM_BUDAYA if p != prog]
    return mk("nilai", lv, stem, maksud, dis, f"KMK 127/KMK.01/2013: “{prog}” bertujuan {maksud}.", "Terjemahkan nama program ke tujuannya: dua menit → tepat waktu; tiga salam → sopan santun; 5R → kantor rapi.", rng, id=f"nilai-f-prog2-{prog}")


# =====================================================================
# BerAKHLAK, PANCASILA
# =====================================================================
@reg("etika", (1, 2))
def berakhlak_definisi(lv, rng):
    n = rng.choice(list(fb.BERAKHLAK))
    if rng.random() < 0.5:
        stem = f"Nilai dasar ASN BerAKHLAK yang bermakna “{fb.BERAKHLAK[n]}” adalah …"
        dis = _ambil([x for x in fb.BERAKHLAK if x != n], 4, rng)
        return mk("etika", lv, stem, n, dis, f"“{fb.BERAKHLAK[n]}” adalah makna nilai {n} (pengetahuan umum; cocokkan dengan buku).", "Hafal tujuh nilai dengan kata kerja inti: melayani, bertanggung jawab, belajar, peduli, berdedikasi, berinovasi, bekerja sama.", rng, id=f"etika-f-ber1-{n}")
    stem = f"Menurut nilai dasar ASN BerAKHLAK, **{n}** berarti …"
    dis = _ambil([v for x, v in fb.BERAKHLAK.items() if x != n], 4, rng)
    return mk("etika", lv, stem, fb.BERAKHLAK[n], dis, f"{n}: {fb.BERAKHLAK[n]} (pengetahuan umum; cocokkan dengan buku).", "Hafal tujuh nilai dengan kata kerja inti.", rng, id=f"etika-f-ber2-{n}")


@reg("wawasan", (1, 2))
def pancasila_sila(lv, rng):
    i = rng.randrange(5)
    bunyi, lambang = fb.SILA[i]
    if rng.random() < 0.5:
        stem = f"Sila ke-{i + 1} Pancasila berbunyi …"
        dis = [b for j, (b, _) in enumerate(fb.SILA) if j != i]
        return mk("wawasan", lv, stem, bunyi, dis, f"Sila ke-{i + 1}: {bunyi}.", "Urutan sila: 1 Ketuhanan, 2 Kemanusiaan, 3 Persatuan, 4 Kerakyatan, 5 Keadilan sosial.", rng, id=f"wawasan-f-sila1-{i}")
    stem = f"Sila “{bunyi}” dilambangkan dengan …"
    dis = [l for j, (_, l) in enumerate(fb.SILA) if j != i]
    return mk("wawasan", lv, stem, lambang, dis, f"Lambang sila ke-{i + 1} adalah {lambang}.", "Lambang berurutan: bintang, rantai, pohon beringin, kepala banteng, padi dan kapas.", rng, id=f"wawasan-f-sila2-{i}")


@reg("wawasan", (3,))
def wawasan_lembaga(lv, rng):
    nama, _, anggota, bukan = next(k for k in fb.KATEGORI if k[0].startswith("lembaga negara"))
    four = rng.sample(anggota, 4)
    aneh = rng.choice(bukan)
    stem = "Berikut adalah lembaga negara yang disebut dalam UUD 1945, KECUALI …"
    return mk("wawasan", lv, stem, aneh, four, f"{aneh} bukan lembaga negara yang disebut dalam UUD 1945. Yang disebut: MPR, DPR, DPD, Presiden, BPK, MA, MK, dan KY.", "Hafal delapan lembaga negara hasil amandemen: MPR, DPR, DPD, Presiden, BPK, MA, MK, KY.", rng, id=f"wawasan-f-lembaga-{aneh}-{rng.randrange(10**6)}")


# =====================================================================
# DISIPLIN PNS
# =====================================================================
@reg("kepegawaian", (1, 2, 3))
def hukuman_tingkat(lv, rng):
    tingkat = {1: "ringan", 2: rng.choice(["ringan", "sedang"]), 3: rng.choice(["sedang", "berat"])}[lv]
    benar = rng.choice(fb.HUKUMAN[tingkat])
    lain = [h for t, hs in fb.HUKUMAN.items() if t != tingkat for h in hs]
    dis = _ambil(lain, 4, rng)
    stem = f"Berikut yang termasuk hukuman disiplin tingkat **{tingkat}** menurut PP 94/2021 adalah …"
    exp = f"“{benar}” termasuk hukuman disiplin {tingkat}. (Rincian sedang dan berat dari pengetahuan umum; cocokkan dengan buku.)"
    return mk("kepegawaian", lv, stem, benar, dis, exp, "Ringan = teguran dan pernyataan tidak puas. Sedang = potong tunjangan kinerja. Berat = turun jabatan, bebas jabatan, atau pemberhentian.", rng, id=f"kepegawaian-f-hk1-{benar}")


@reg("kepegawaian", (2, 3))
def hukuman_bukan(lv, rng):
    t = "berat"
    anggota = rng.sample(fb.HUKUMAN[t], 4)
    aneh = rng.choice(fb.HUKUMAN["ringan"] + fb.HUKUMAN["sedang"])
    stem = "Berikut adalah hukuman disiplin tingkat **berat** menurut PP 94/2021, KECUALI …"
    return mk("kepegawaian", lv, stem, aneh, anggota, f"“{aneh}” bukan hukuman berat. (Dari pengetahuan umum; cocokkan dengan buku.)", "Hukuman berat menyentuh status jabatan atau kepegawaian; pemotongan tunjangan dan teguran bukan.", rng, id=f"kepegawaian-f-hk2-{aneh}")


# =====================================================================
# UNIT ESELON I KEMENKEU
# =====================================================================
@reg("struktur", (1, 2))
def unit_singkatan(lv, rng):
    pool = [u for u in fb.UNIT if u[0]]
    sing, nama, _ = rng.choice(pool)
    dis = [u[1] for u in fb.UNIT if u[1] != nama]
    if rng.random() < 0.5:
        stem = f"**{sing}** adalah singkatan dari …"
        return mk("struktur", lv, stem, nama, dis, f"{sing} = {nama}.", "Hafal singkatan unit: DJP, DJBC, DJA, DJPb, DJKN, DJPK, DJPPR, DJSEF, DJSPSK, BPPK.", rng, id=f"struktur-f-sing1-{sing}")
    dis = [u[0] for u in fb.UNIT if u[0] and u[0] != sing]
    stem = f"Singkatan dari **{nama}** adalah …"
    return mk("struktur", lv, stem, sing, dis, f"{nama} disingkat {sing}.", "Perhatikan huruf besar-kecil: DJPb (perbendaharaan) berbeda dari DJP (pajak).", rng, id=f"struktur-f-sing2-{sing}")


@reg("struktur", (1, 2, 3))
def unit_fungsi(lv, rng):
    sing, nama, fungsi = rng.choice(fb.UNIT)
    if rng.random() < 0.5:
        stem = f"Unit eselon I Kementerian Keuangan yang bertugas di bidang {fungsi} adalah …"
        dis = [u[1] for u in fb.UNIT if u[1] != nama]
        return mk("struktur", lv, stem, nama, dis, f"{nama} bertugas di bidang {fungsi}.", "Kata kunci bidang → unit: pajak (DJP), bea cukai (DJBC), anggaran (DJA), perbendaharaan (DJPb), aset dan lelang (DJKN), pusat–daerah (DJPK), utang dan SBN (DJPPR), diklat (BPPK).", rng, id=f"struktur-f-fung1-{nama}")
    stem = f"**{nama}** bertugas di bidang …"
    dis = [u[2] for u in fb.UNIT if u[1] != nama]
    return mk("struktur", lv, stem, fungsi, dis, f"{nama} bertugas di bidang {fungsi}.", "Kenali kata kunci dalam nama unit (Pajak, Bea dan Cukai, Anggaran, Perbendaharaan, Kekayaan Negara, Perimbangan Keuangan, Pembiayaan dan Risiko).", rng, id=f"struktur-f-fung2-{nama}")


# =====================================================================
# KATA YANG TIDAK SEKELOMPOK (kategori + angka)
# =====================================================================
@reg("kelompok", (1, 2, 3))
def kelompok_kategori(lv, rng):
    kat = _dekat(fb.KATEGORI, lv, rng, lambda x: x[1])
    nama, _, anggota, bukan = kat
    four = rng.sample(anggota, 4)
    aneh = rng.choice(bukan)
    stem = "Pilihlah kata yang **tidak termasuk** dalam kelompoknya!"
    exp = f"Empat kata lain termasuk {nama}. **{aneh}** bukan {nama}."
    trick = {1: "Cari satu ciri umum 4 kata (jenis, fungsi, asal). Kata yang tidak punya ciri itu jawabannya.",
             2: "Rangkai kalimat “… adalah ___”. Kata yang tidak cocok dengan kalimat yang sama adalah jawabannya.",
             3: "Tentukan kategori yang paling spesifik, bukan yang terlalu luas (misal “nilai milik instansi mana”)."}[lv]
    return mk("kelompok", lv, stem, aneh, four, exp, trick, rng, id=f"kelompok-f-{nama}-{aneh}-{'-'.join(sorted(four))}")


@reg("kelompok", (1, 2, 3))
def kelompok_angka(lv, rng):
    def prima(n):
        return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))
    if lv == 1:
        nama = "bilangan genap"
        four = rng.sample(range(2, 60, 2), 4)
        aneh = rng.choice(range(1, 59, 2))
        exp = f"Empat bilangan lain genap (habis dibagi 2); {aneh} ganjil."
    elif lv == 2:
        nama = "kelipatan 7"
        four = rng.sample(range(14, 100, 7), 4)
        aneh = rng.choice([x for x in range(15, 99) if x % 7])
        exp = f"Empat bilangan lain kelipatan 7; {aneh} bukan kelipatan 7."
    else:
        if rng.random() < 0.5:
            nama = "bilangan prima"
            four = rng.sample([p for p in range(11, 90) if prima(p)], 4)
            aneh = rng.choice([x for x in range(21, 95, 2) if not prima(x)])
            exp = f"Empat bilangan lain prima; {aneh} habis dibagi bilangan selain 1 dan dirinya sendiri."
        else:
            nama = "kuadrat sempurna"
            four = rng.sample([k * k for k in range(4, 15)], 4)
            aneh = rng.choice([x for x in range(20, 200) if int(x ** 0.5) ** 2 != x])
            exp = f"Empat bilangan lain adalah kuadrat sempurna; {aneh} bukan."
    trick = "Uji tiap bilangan terhadap aturan yang sama; coret yang lolos."
    return mk("kelompok", lv, "Pilihlah bilangan yang **tidak termasuk** dalam kelompoknya!", aneh, four, exp, trick, rng, id=f"kelompok-n-{nama}-{aneh}-{'-'.join(map(str, sorted(four)))}")
