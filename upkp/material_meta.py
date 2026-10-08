"""Source/freshness metadata for learning materials."""
MATERIAL_META = {
    "etika":{"status":"verified_regulation","status_label":"Sumber resmi diverifikasi","verified":"8 Okt 2026","note":"Anchor: UU 20/2023 dan PMK 190/PMK.01/2018."},
    "wawasan":{"status":"official_plus_crosscheck","status_label":"Konstitusional + perlu konteks ujian","verified":"8 Okt 2026","note":"Anchor konstitusional diverifikasi; cakupan detail TSKKWK tidak dipublikasikan sebagai blueprint resmi."},
    "nilai":{"status":"verified_regulation","status_label":"Sumber resmi diverifikasi","verified":"8 Okt 2026","note":"Nilai Kemenkeu IProSPeK dan kode perilaku masih digunakan pada laman resmi Kemenkeu."},
    "kepegawaian":{"status":"verified_regulation","status_label":"Regulasi diverifikasi","verified":"8 Okt 2026","note":"Anchor current: UU 20/2023, PP 94/2021, PMK 123/2023, dan aturan cuti BKN."},
    "keuangan":{"status":"verified_regulation","status_label":"UU pokok diverifikasi","verified":"8 Okt 2026","note":"Anchor: UU 17/2003, UU 1/2004, UU 15/2004."},
    "struktur":{"status":"verified_dynamic","status_label":"Struktur current · cepat berubah","verified":"8 Okt 2026","note":"Anchor current: PMK 124/2024 sebagaimana diubah PMK 117/2025."},
}
def metadata(code, source_type):
    if code in MATERIAL_META:
        return MATERIAL_META[code]
    if source_type=="buku":
        return {"status":"reference_anchored","status_label":"Referensi latihan tervalidasi","verified":"8 Okt 2026","note":"Konsep diperluas menjadi modul pembelajaran UPKP Coach; fokus pada kemampuan, bukan ringkasan sumber."}
    return {"status":"general","status_label":"Materi pembelajaran","verified":"","note":"Gunakan bersama evidence latihan dan sumber resmi terbaru bila regulasi dapat berubah."}
