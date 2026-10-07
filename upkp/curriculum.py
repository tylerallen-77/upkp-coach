"""Daftar bab mengikuti DAFTAR ISI buku "Anak UPKP" (29 bab, 3 bagian besar).

`sumber` menunjukkan asal isi:
  - "buku"   : pola, rumus, dan jenis soal dibaca dari halaman buku yang diunggah (hlm. 1-82).
  - "umum"   : halaman buku belum tersedia; isi disusun dari pengetahuan umum dan sumber resmi
               yang bisa dicek. WAJIB dicocokkan dengan buku saat halamannya tersedia.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Bab:
    kode: str
    judul: str
    bagian: str      # Tes Potensi / TSKKWK / Tes Psikologi
    subtes: str
    halaman: str
    sumber: str      # "buku" atau "umum"
    mode: str = "pg"  # "pg" pilihan ganda, "pauli", "diri" (kuesioner tanpa kunci)


BAB = [
    # ---- TES POTENSI: SUBTES VERBAL
    Bab("padanan", "Padanan Kata", "Tes Potensi", "Verbal", "1", "buku"),
    Bab("kelompok", "Pengelompokan Kata", "Tes Potensi", "Verbal", "7", "buku"),
    Bab("silogisme", "Silogisme", "Tes Potensi", "Verbal", "10", "buku"),
    Bab("analisis", "Penalaran Analisis", "Tes Potensi", "Verbal", "17", "buku"),
    # ---- TES POTENSI: SUBTES NUMERIKAL
    Bab("operasi", "Operasi Bilangan", "Tes Potensi", "Numerikal", "23", "buku"),
    Bab("persamaan", "Persamaan dan Pertidaksamaan", "Tes Potensi", "Numerikal", "29", "buku"),
    Bab("geometri", "Geometri", "Tes Potensi", "Numerikal", "34", "buku"),
    Bab("aritsos", "Aritmatika Sosial dan Barisan dan Deret", "Tes Potensi", "Numerikal", "39", "buku"),
    Bab("sudut", "Sudut dan Himpunan", "Tes Potensi", "Numerikal", "44", "buku"),
    Bab("banding", "Perbandingan", "Tes Potensi", "Numerikal", "48", "buku"),
    Bab("jarak", "Jarak, Kecepatan dan Waktu", "Tes Potensi", "Numerikal", "53", "buku"),
    Bab("peluang", "Peluang, Permutasi dan Kombinasi", "Tes Potensi", "Numerikal", "58", "buku"),
    Bab("statistika", "Statistika", "Tes Potensi", "Numerikal", "62", "buku"),
    Bab("deret", "Deret Angka dan Huruf", "Tes Potensi", "Numerikal", "68", "buku"),
    # ---- TES POTENSI: SUBTES FIGURAL
    Bab("deretfig", "Deret Figural", "Tes Potensi", "Figural", "72", "buku"),
    Bab("analogifig", "Analogi Figural", "Tes Potensi", "Figural", "78", "buku"),
    # ---- TSKKWK
    Bab("etika", "Etika PNS", "TSKKWK", "TSKKWK", "83", "umum"),
    Bab("wawasan", "Wawasan Kebangsaan", "TSKKWK", "TSKKWK", "97", "umum"),
    Bab("nilai", "Nilai-Nilai Kementerian Keuangan", "TSKKWK", "TSKKWK", "119", "umum"),
    Bab("kepegawaian", "Tata Aturan Kepegawaian", "TSKKWK", "TSKKWK", "133", "umum"),
    Bab("keuangan", "Pengelolaan Keuangan Negara", "TSKKWK", "TSKKWK", "168", "umum"),
    Bab("struktur", "Struktur Kementerian Keuangan Terbaru", "TSKKWK", "TSKKWK", "184", "umum"),
    # ---- TES PSIKOLOGI
    Bab("pemahaman", "Subtes Pemahaman yang Diberikan", "Tes Psikologi", "Psikologi", "196", "umum"),
    Bab("numlogic", "Subtes Number Logic", "Tes Psikologi", "Psikologi", "200", "umum"),
    Bab("blockpattern", "Subtes Block Pattern", "Tes Psikologi", "Psikologi", "203", "umum"),
    Bab("disc", "Subtes DISC", "Tes Psikologi", "Psikologi", "209", "umum", "diri"),
    Bab("karakter", "Subtes Karakteristik Pribadi", "Tes Psikologi", "Psikologi", "21x", "umum", "diri"),
    Bab("skala", "Subtes Skala Penilaian Diri", "Tes Psikologi", "Psikologi", "23x", "umum", "diri"),
    Bab("pauli", "Subtes Pauli", "Tes Psikologi", "Psikologi", "24x", "umum", "pauli"),
]

BAB_BY_KODE = {b.kode: b for b in BAB}
BAGIAN = ["Tes Potensi", "TSKKWK", "Tes Psikologi"]
SUBTES = {
    "Tes Potensi": ["Verbal", "Numerikal", "Figural"],
    "TSKKWK": ["TSKKWK"],
    "Tes Psikologi": ["Psikologi"],
}


def bab_di(bagian: str, subtes: str | None = None):
    return [b for b in BAB if b.bagian == bagian and (subtes is None or b.subtes == subtes)]
