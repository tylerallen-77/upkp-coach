"""Soal Verbal: padanan kata, pengelompokan kata, silogisme, penalaran analisis.

Sebagian soal berasal dari bank buatan sendiri (`bank_statis.json`), sebagian ditulis baru
mengikuti jenis soal di buku (hlm. 1-22). Tidak ada soal yang disalin dari buku.
"""
from __future__ import annotations

import json
from pathlib import Path

from .model import Q, mk
from .registry import GENS, reg

_BANK = json.loads((Path(__file__).parent / "bank_statis.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------------
# Soal pengelompokan kata (buku hlm. 7-9): cari kata yang tidak sekelompok
# [kata yang berbeda, 4 anggota kelompok, alasan kelompok, tingkat]
# ---------------------------------------------------------------------
KELOMPOK = [
    ("Harimau", ["Sapi", "Kambing", "Kuda", "Kelinci"], "pemakan tumbuhan (herbivora)", 1),
    ("Kubus", ["Persegi", "Lingkaran", "Trapesium", "Segitiga"], "bangun datar (kubus adalah bangun ruang)", 1),
    ("Bogor", ["Bandung", "Semarang", "Surabaya", "Medan"], "ibu kota provinsi (Bogor adalah kota, bukan ibu kota provinsi)", 1),
    ("Laut Jawa", ["Samudra Pasifik", "Samudra Atlantik", "Samudra Hindia", "Samudra Arktik"], "samudra (Laut Jawa adalah laut)", 1),
    ("Segitiga", ["Ungu", "Hijau", "Biru", "Kuning"], "warna (segitiga adalah bentuk)", 1),
    ("Emas", ["Perunggu", "Kuningan", "Baja", "Solder"], "logam paduan (emas adalah unsur logam murni)", 2),
    ("Bangladesh", ["Laos", "Kamboja", "Myanmar", "Brunei Darussalam"], "negara anggota ASEAN", 2),
    ("Mohammad Hatta", ["Soekarno", "Soeharto", "B.J. Habibie", "Abdurrahman Wahid"], "Presiden Republik Indonesia (Hatta adalah Wakil Presiden)", 2),
    ("OJK", ["Direktorat Jenderal Anggaran", "Direktorat Jenderal Perimbangan Keuangan", "Direktorat Jenderal Pengelolaan Pembiayaan dan Risiko", "Inspektorat Jenderal"],
     "unit eselon I Kementerian Keuangan (OJK adalah lembaga independen)", 2),
    ("39", ["29", "31", "37", "41"], "bilangan prima (39 = 3 × 13)", 2),
    ("Tinggi – Rendah", ["Cantik – Elok", "Besar – Raya", "Pintar – Pandai", "Cepat – Laju"], "pasangan sinonim (tinggi–rendah adalah pasangan antonim)", 3),
    ("Juni", ["Januari", "Maret", "Mei", "Juli"], "bulan yang berjumlah 31 hari (Juni 30 hari)", 3),
    ("Sinergi", ["Akuntabel", "Kompeten", "Harmonis", "Loyal"], "nilai dasar ASN BerAKHLAK (sinergi adalah nilai Kementerian Keuangan)", 3),
    ("Harmonis", ["Integritas", "Profesionalisme", "Pelayanan", "Kesempurnaan"], "nilai-nilai Kementerian Keuangan (harmonis adalah nilai dasar ASN BerAKHLAK)", 3),
]
KELOMPOK_TRICK = {
    1: "Cari satu ciri umum 4 kata (jenis, fungsi, asal, tempat). Kata yang tidak punya ciri itu adalah jawabannya.",
    2: "Rangkai jadi kalimat: “… adalah ___”. Kalau satu kata tidak cocok dengan kalimat yang sama, itu jawabannya. Cek juga awalan dan akhiran.",
    3: "Soal tingkat tinggi memakai kategori yang mirip. Tentukan kategori yang lebih spesifik (contoh: bukan sekadar “nilai”, tetapi “nilai milik instansi mana”).",
}

# ---------------------------------------------------------------------
# Silogisme tambahan (buku hlm. 10-16): konversi, obversi, aturan quantifier
# [stem, jawab, 4 pengecoh, pembahasan, cara cepat, tingkat]
# ---------------------------------------------------------------------
SILOGISME_BARU = [
    ("Premis: **Semua dosen adalah peneliti.** Menurut aturan konversi, kesimpulan langsung yang benar adalah …", "Sebagian peneliti adalah dosen",
     ["Semua peneliti adalah dosen", "Tidak ada dosen yang peneliti", "Semua dosen bukan peneliti", "Sebagian peneliti bukan dosen"],
     "Konversi menukar subjek dan predikat. Dari “Semua S adalah P” hanya sah menyimpulkan “Sebagian P adalah S”.",
     "Konversi “semua” menjadi “sebagian”. Jangan menukar tanpa mengubah “semua” (itu kesalahan klasik).", 1),
    ("Premis: **Semua ikan dapat berenang.** Obversinya adalah …", "Tak satu pun ikan yang tidak dapat berenang",
     ["Semua yang dapat berenang adalah ikan", "Sebagian ikan tidak dapat berenang", "Tak satu pun ikan dapat berenang", "Sebagian yang dapat berenang adalah ikan"],
     "Obversi mengubah kualitas (positif ↔ negatif) dan menegasikan predikat, tanpa mengubah makna.",
     "Obversi: ubah kata kerja positif/negatif, negasikan predikat. “Semua S adalah P” ≡ “Tak satu pun S yang bukan P”.", 1),
    ("Premis: **Tidak ada pegawai yang tidak disiplin.** Obversinya adalah …", "Semua pegawai disiplin",
     ["Sebagian pegawai disiplin", "Semua pegawai tidak disiplin", "Tidak ada pegawai yang disiplin", "Sebagian pegawai tidak disiplin"],
     "Dua negasi saling menghapus: tak ada yang tidak disiplin sama dengan semua disiplin.", "Dua negatif = positif. “Tak ada S yang bukan P” = “Semua S adalah P”.", 1),
    ("Semua pejabat adalah PNS. Semua PNS wajib menaati disiplin. Kesimpulan yang benar adalah …", "Semua pejabat wajib menaati disiplin",
     ["Semua PNS adalah pejabat", "Sebagian PNS tidak wajib menaati disiplin", "Sebagian pejabat bukan PNS", "Tidak ada pejabat yang menaati disiplin"],
     "Quantifier: semua + semua = semua. Subjek dari premis minor, predikat dari premis mayor.", "Dua premis “semua” → kesimpulan “semua”. Coret term tengah (PNS).", 1),
    ("Berdasarkan aturan quantifier silogisme, dua premis yang sama-sama berbunyi “sebagian …” menghasilkan kesimpulan …", "tidak dapat disimpulkan",
     ["sebagian …", "semua …", "tidak ada …", "semua … bukan …"],
     "Sebagian + sebagian = tidak dapat disimpulkan, karena term tengah belum tentu diikat oleh bagian yang sama.", "Hafalkan: semua+semua = semua/sebagian; sebagian+semua = sebagian; sebagian+sebagian = tidak dapat disimpulkan.", 2),
    ("Semua laporan keuangan memuat neraca. Sebagian laporan keuangan diaudit. Kesimpulan yang tepat adalah …", "Sebagian laporan yang memuat neraca diaudit",
     ["Semua laporan yang memuat neraca diaudit", "Tidak ada laporan yang memuat neraca diaudit", "Semua laporan yang diaudit tidak memuat neraca", "Semua laporan diaudit"],
     "Laporan keuangan yang diaudit pasti memuat neraca, jadi ada laporan yang memuat neraca dan diaudit. Karena ada “sebagian”, kesimpulannya “sebagian”.", "Premis “semua” + premis “sebagian” = kesimpulan “sebagian”.", 2),
    ("Tidak ada polisi yang berprofesi tentara. Tidak ada tentara yang berprofesi guru. Kesimpulan yang tepat adalah …", "Tidak dapat disimpulkan",
     ["Tidak ada polisi yang berprofesi guru", "Semua polisi berprofesi guru", "Sebagian polisi berprofesi guru", "Semua guru bukan polisi"],
     "Dua premis negatif tidak menghasilkan kesimpulan: polisi dan guru bisa saja beririsan atau tidak.", "Kedua premis negatif → tidak dapat disimpulkan (hukum silogisme).", 3),
    ("Semua mahasiswa kampus X adalah calon PNS. Semua calon PNS mengikuti diklat. Kesimpulan yang pasti benar adalah …", "Semua mahasiswa kampus X mengikuti diklat",
     ["Semua yang mengikuti diklat adalah mahasiswa kampus X", "Sebagian calon PNS bukan mahasiswa kampus X", "Tidak ada calon PNS yang mahasiswa", "Semua calon PNS adalah mahasiswa kampus X"],
     "Rantai: mahasiswa X → calon PNS → mengikuti diklat. Kesimpulan tidak boleh lebih umum dari premis (jangan dibalik).", "Rantai lingkaran dalam lingkaran. Jawaban hanya boleh mengikuti arah dari yang kecil ke yang besar.", 3),
]

# ---------------------------------------------------------------------
# Penalaran analisis tambahan (buku hlm. 17-21): urutan, penjadwalan, posisi, implikasi
# ---------------------------------------------------------------------
ANALISIS_BARU = [
    ("Harga buku lebih mahal daripada pensil. Harga pulpen lebih mahal daripada buku. Harga penggaris lebih murah daripada pensil. Dari keterangan itu dapat disimpulkan bahwa …",
     "Penggaris paling murah di antara keempatnya",
     ["Pensil lebih mahal daripada pulpen", "Buku lebih murah daripada penggaris", "Pulpen lebih murah daripada pensil", "Penggaris lebih mahal daripada buku"],
     "Urutan dari termahal: pulpen > buku > pensil > penggaris. Jadi penggaris paling murah.", "Tulis rantai dengan tanda “>”. Ujung kiri paling mahal, ujung kanan paling murah.", 1),
    ("Lima pegawai (A, B, C, D, E) masing-masing mendapat satu hari piket Senin sampai Jumat. A tidak piket Senin dan Jumat. B piket sehari sebelum C. D piket setelah A. E piket hari Jumat. Siapa yang piket hari Selasa?",
     "C", ["A", "B", "D", "E"],
     "E = Jumat. A bisa Selasa, Rabu, atau Kamis. Jika A = Selasa atau Kamis, pasangan (B, C) yang berurutan tidak muat. Jadi A = Rabu, (B, C) = (Senin, Selasa), D = Kamis. Hari Selasa: C.",
     "Buat tabel hari. Isi yang pasti (E = Jumat), lalu cek kemungkinan tiap hari untuk pegawai paling terbatas (A).", 2),
    ("Lima toko berjajar dari kiri ke kanan: toko obat, buku, roti, sepatu, dan pakaian. Toko obat berada di ujung kiri. Toko roti tepat di sebelah kanan toko obat. Toko buku bersebelahan dengan toko sepatu. Toko pakaian tidak bersebelahan dengan toko roti. Toko sepatu tidak bersebelahan dengan toko roti. Toko yang berada di tengah (urutan ke-3) adalah …",
     "Toko buku", ["Toko obat", "Toko roti", "Toko sepatu", "Toko pakaian"],
     "Obat (1), roti (2). Pakaian tidak di 3, jadi pakaian ada di 4 atau 5. Buku dan sepatu harus bersebelahan, jadi pakaian di 5, buku dan sepatu di 3 dan 4. Sepatu tidak di 3, jadi buku di 3, sepatu di 4.",
     "Pasang yang pasti dulu (ujung dan “tepat di sebelah”), lalu coret posisi yang dilarang untuk sisanya.", 2),
    ("Seorang siswa memilih tiga dari lima ekstrakurikuler: Basket, Catur, Drama, Futsal, dan Musik. Aturannya: (1) Jika memilih Drama, tidak boleh memilih Futsal. (2) Jika memilih Musik, harus memilih Catur. (3) Jika memilih Basket, harus memilih Futsal. Pilihan yang diperbolehkan adalah …",
     "Catur, Futsal, dan Musik",
     ["Basket, Drama, dan Musik", "Basket, Catur, dan Drama", "Drama, Futsal, dan Musik", "Basket, Drama, dan Futsal"],
     "Cek tiap opsi: Basket tanpa Futsal melanggar (3); Drama bersama Futsal melanggar (1). Hanya Catur, Futsal, Musik yang memenuhi semua aturan (Musik disertai Catur).",
     "Coret opsi yang melanggar aturan, satu aturan per pass. Mulai dari aturan yang paling mudah dicek.", 3),
    ("Lima kota P, Q, R, S, T dihubungkan jalur pesan satu arah: P ke Q, Q ke R, Q ke T, S ke R, dan R ke T. Pesan hanya bisa diteruskan sesuai jalur. Jika kota Q rusak, semua pengiriman berikut tetap bisa dilakukan KECUALI …",
     "dari P ke T", ["dari S ke R", "dari R ke T", "dari S ke T", "dari S ke R lalu ke T"],
     "Dari P satu-satunya jalur keluar lewat Q. Q rusak, jadi P tidak bisa mengirim ke mana pun, termasuk ke T. Jalur S → R → T tidak melewati Q.",
     "Gambar panah. Tandai simpul yang rusak lalu telusuri apakah masih ada jalur alternatif.", 3),
]


# ---------------------------------------------------------------------
# Pembangun soal dari data statis
# ---------------------------------------------------------------------
def _bangun_statis(bab: str, kunci: str, idx: int, item: dict, rng) -> Q:
    stem = item["q"]
    return mk(bab, item["lv"], stem, item["a"], item["d"], item["exp"], item["trick"], rng, id=f"{bab}-{kunci}-{idx}", waktu=0)


def _statis_generator(bab: str, kunci: str, sumber: str):
    daftar = [(i, it) for i, it in enumerate(_BANK[sumber])]

    def gen(lv, rng):
        pool = [(i, it) for i, it in daftar if it["lv"] == lv]
        if not pool:
            raise KeyError(f"tidak ada soal {bab}/{sumber} tingkat {lv}")
        i, it = rng.choice(pool)
        return _bangun_statis(bab, kunci, i, it, rng)
    gen.__name__ = f"statis_{bab}_{sumber}"
    levels = tuple(sorted({it["lv"] for it in _BANK[sumber]}))
    GENS.setdefault(bab, []).append((gen, levels))


for _bab, _sumber in [("padanan", "sinonim"), ("padanan", "antonim"), ("padanan", "analogi"),
                      ("silogisme", "silogisme"), ("silogisme", "bersyarat"), ("analisis", "urutan")]:
    _statis_generator(_bab, _sumber, _sumber)


def _daftar_generator(bab: str, kunci: str, data: list):
    def gen(lv, rng):
        pool = [(i, d) for i, d in enumerate(data) if d[-1] == lv]
        if not pool:
            raise KeyError(f"tidak ada soal {bab}/{kunci} tingkat {lv}")
        i, d = rng.choice(pool)
        stem, jawab, dis, exp, trick, tlv = d
        return mk(bab, lv, stem, jawab, dis, exp, trick, rng, id=f"{bab}-{kunci}-{i}")
    gen.__name__ = f"daftar_{bab}_{kunci}"
    GENS.setdefault(bab, []).append((gen, tuple(sorted({d[-1] for d in data}))))


_daftar_generator("silogisme", "baru", SILOGISME_BARU)
_daftar_generator("analisis", "baru", ANALISIS_BARU)


def _gen_kelompok(lv, rng):
    pool = [(i, d) for i, d in enumerate(KELOMPOK) if d[3] == lv]
    i, (aneh, grup, alasan, _) = rng.choice(pool)
    stem = "Pilihlah kata yang **tidak termasuk** dalam kelompoknya!"
    exp = f"Empat kata lain termasuk: {alasan}. Kata yang berbeda adalah **{aneh}**."
    return mk("kelompok", lv, stem, aneh, grup, exp, KELOMPOK_TRICK[lv], rng, id=f"kelompok-{i}")


GENS.setdefault("kelompok", []).append((_gen_kelompok, (1, 2, 3)))
