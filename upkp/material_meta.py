"""Presentation/source metadata for learning materials.
This does not replace the source text; it makes provenance/freshness explicit in the UI.
"""
MATERIAL_META = {
    "etika":{"status":"needs_book_crosscheck","status_label":"Perlu cross-check buku","verified":"Okt 2026","note":"Basis regulasi/pengetahuan resmi; halaman buku bab belum tersedia."},
    "wawasan":{"status":"needs_verification","status_label":"Perlu verifikasi","verified":"","note":"Ringkasan berbasis pengetahuan umum; cocokkan dengan buku/sumber resmi terbaru."},
    "nilai":{"status":"official_plus_crosscheck","status_label":"Sumber resmi + cross-check","verified":"Okt 2026","note":"Mengacu materi nilai Kemenkeu dan dokumen terkait; cocokkan redaksi dengan buku."},
    "kepegawaian":{"status":"verified_regulation","status_label":"Regulasi diverifikasi","verified":"Okt 2026","note":"Regulasi dapat berubah; tanggal verifikasi ditampilkan agar freshness eksplisit."},
    "keuangan":{"status":"core_law","status_label":"UU pokok","verified":"","note":"Ringkasan tiga paket UU keuangan negara; perlu cross-check dengan materi ujian."},
    "struktur":{"status":"verified_dynamic","status_label":"Diverifikasi · cepat berubah","verified":"Okt 2026","note":"Struktur organisasi bersifat dinamis; cek regulasi terbaru sebelum ujian."},
}

def metadata(code, source_type):
    if code in MATERIAL_META:
        return MATERIAL_META[code]
    if source_type=="buku":
        return {"status":"book_anchored","status_label":"Berbasis buku","verified":"","note":"Ringkasan ditulis ulang dari pokok bahasan buku Anak UPKP."}
    return {"status":"general","status_label":"Basis umum","verified":"","note":"Perlu validasi terhadap sumber ujian terbaru."}
