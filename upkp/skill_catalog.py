from __future__ import annotations
import re

SKILLS = {
    "numerik.operasi_bilangan": {"label":"Operasi bilangan", "chapter":"operasi", "section":"numerical"},
    "numerik.persamaan": {"label":"Persamaan & pertidaksamaan", "chapter":"persamaan", "section":"numerical"},
    "numerik.geometri": {"label":"Geometri", "chapter":"geometri", "section":"numerical"},
    "numerik.aritmatika_sosial": {"label":"Aritmatika sosial", "chapter":"aritsos", "section":"numerical"},
    "numerik.sudut_himpunan": {"label":"Sudut & himpunan", "chapter":"sudut", "section":"numerical"},
    "numerik.reverse_percentage": {"label":"Reverse percentage", "chapter":"banding", "section":"numerical"},
    "numerik.work_rate": {"label":"Work rate", "chapter":"banding", "section":"numerical"},
    "numerik.ratio": {"label":"Rasio & perbandingan", "chapter":"banding", "section":"numerical"},
    "numerik.jarak_kecepatan_waktu": {"label":"Jarak · kecepatan · waktu", "chapter":"jarak", "section":"numerical"},
    "numerik.peluang_kombinasi": {"label":"Peluang & kombinasi", "chapter":"peluang", "section":"numerical"},
    "numerik.statistika": {"label":"Statistika & data interpretation", "chapter":"statistika", "section":"numerical"},
    "numerik.deret_alternating": {"label":"Deret · alternating operations", "chapter":"deret", "section":"numerical"},
    "numerik.deret_difference": {"label":"Deret · difference pattern", "chapter":"deret", "section":"numerical"},
    "numerik.deret_multiply": {"label":"Deret · multiply ± k", "chapter":"deret", "section":"numerical"},
    "numerik.weighted_average": {"label":"Weighted average", "chapter":"statistika", "section":"numerical"},
    "numerik.multi_step_percent": {"label":"Multi-step percentage", "chapter":"banding", "section":"numerical"},
    "numerik.data_interpretation": {"label":"Data interpretation", "chapter":"statistika", "section":"numerical"},
    "numerik.rate_change_table": {"label":"Rate change from table", "chapter":"statistika", "section":"numerical"},

    "verbal.padanan_relasi": {"label":"Padanan kata · relation", "chapter":"padanan", "section":"verbal"},
    "verbal.pengelompokan": {"label":"Pengelompokan kata", "chapter":"kelompok", "section":"verbal"},
    "verbal.critical_inference": {"label":"Verbal critical inference", "chapter":"analisis", "section":"verbal"},

    "logika.silogisme_quantifier": {"label":"Silogisme · quantifier", "chapter":"silogisme", "section":"logical"},
    "logika.only_if": {"label":"Conditional logic · if / only if", "chapter":"silogisme", "section":"logical"},
    "logika.penalaran_analitis": {"label":"Penalaran analitis", "chapter":"analisis", "section":"logical"},
    "logika.constraint_ordering": {"label":"Constraint ordering", "chapter":"analisis", "section":"logical"},
    "logika.assignment_constraints": {"label":"Assignment constraints", "chapter":"analisis", "section":"logical"},

    "figural.deret": {"label":"Figural · deret", "chapter":"deretfig", "section":"figural"},
    "figural.analogi": {"label":"Figural · analogi", "chapter":"analogifig", "section":"figural"},
    "figural.matrix_transform": {"label":"Figural · matrix transform", "chapter":"analogifig", "section":"figural"},

    "substansi.etika": {"label":"Etika PNS", "chapter":"etika", "section":"substansi"},
    "substansi.wawasan": {"label":"Wawasan Kebangsaan", "chapter":"wawasan", "section":"substansi"},
    "substansi.nilai_kemenkeu": {"label":"Nilai-Nilai Kementerian Keuangan", "chapter":"nilai", "section":"substansi"},
    "substansi.kepegawaian": {"label":"Tata Aturan Kepegawaian", "chapter":"kepegawaian", "section":"substansi"},
    "substansi.keuangan_negara": {"label":"Pengelolaan Keuangan Negara", "chapter":"keuangan", "section":"substansi"},
    "substansi.struktur_kemenkeu": {"label":"Struktur Kementerian Keuangan", "chapter":"struktur", "section":"substansi"},
}

CHAPTER_DEFAULT = {
    "padanan":"verbal.padanan_relasi", "kelompok":"verbal.pengelompokan",
    "silogisme":"logika.silogisme_quantifier", "analisis":"logika.penalaran_analitis",
    "operasi":"numerik.operasi_bilangan", "persamaan":"numerik.persamaan",
    "geometri":"numerik.geometri", "aritsos":"numerik.aritmatika_sosial",
    "sudut":"numerik.sudut_himpunan", "banding":"numerik.ratio",
    "jarak":"numerik.jarak_kecepatan_waktu", "peluang":"numerik.peluang_kombinasi",
    "statistika":"numerik.statistika", "deret":"numerik.deret_difference",
    "deretfig":"figural.deret", "analogifig":"figural.analogi",
    "etika":"substansi.etika", "wawasan":"substansi.wawasan",
    "nilai":"substansi.nilai_kemenkeu", "kepegawaian":"substansi.kepegawaian",
    "keuangan":"substansi.keuangan_negara", "struktur":"substansi.struktur_kemenkeu",
}

SECTION_LABELS = {
    "verbal":"Verbal Mastery",
    "numerical":"Numerikal Mastery",
    "logical":"Logical Mastery",
    "figural":"Figural Mastery",
    "substansi_etika":"Etika PNS Mastery",
    "substansi_wawasan":"Wawasan Kebangsaan Mastery",
    "substansi_nilai":"Nilai Kemenkeu Mastery",
    "substansi_kepegawaian":"Kepegawaian Mastery",
    "substansi_keuangan":"Keuangan Negara Mastery",
    "substansi_struktur":"Struktur Kemenkeu Mastery",
}

BADGE_SKILLS = {
    "verbal":["verbal.padanan_relasi","verbal.pengelompokan","verbal.critical_inference","logika.silogisme_quantifier","logika.only_if","logika.penalaran_analitis","logika.constraint_ordering","logika.assignment_constraints"],
    "numerical":[
        "numerik.operasi_bilangan","numerik.persamaan","numerik.aritmatika_sosial",
        "numerik.ratio","numerik.reverse_percentage","numerik.work_rate",
        "numerik.jarak_kecepatan_waktu","numerik.statistika",
        "numerik.deret_difference","numerik.deret_alternating",
        "numerik.data_interpretation","numerik.multi_step_percent",
    ],
    "logical":["logika.silogisme_quantifier","logika.only_if","logika.penalaran_analitis","logika.constraint_ordering","logika.assignment_constraints"],
    "figural":["figural.deret","figural.analogi","figural.matrix_transform"],
    "substansi_etika":["substansi.etika"],
    "substansi_wawasan":["substansi.wawasan"],
    "substansi_nilai":["substansi.nilai_kemenkeu"],
    "substansi_kepegawaian":["substansi.kepegawaian"],
    "substansi_keuangan":["substansi.keuangan_negara"],
    "substansi_struktur":["substansi.struktur_kemenkeu"],
}

def label(skill: str) -> str:
    return SKILLS.get(skill, {}).get("label", skill.split('.',1)[-1].replace('_',' ').title())

def chapter(skill: str) -> str | None:
    return SKILLS.get(skill, {}).get("chapter")

def section(skill: str) -> str:
    return SKILLS.get(skill, {}).get("section","unknown")

def classify_legacy(q: dict) -> str:
    bab = str(q.get("bab", ""))
    text = " ".join(str(q.get(k, "")) for k in ("stem","exp","trick")).lower()
    explicit=str(q.get("skill") or "")
    if explicit:return explicit
    if bab == "banding":
        if "%" in text and any(x in text for x in ("lebih tinggi","lebih besar","lebih rendah","lebih kecil","dibanding","persen")):
            return "numerik.reverse_percentage"
        if any(x in text for x in ("pekerja","orang","hari","pekerjaan","selesai")):
            return "numerik.work_rate"
        return "numerik.ratio"
    if bab == "aritsos" and any(x in text for x in ("pekerja","orang","hari","pekerjaan")):
        return "numerik.work_rate"
    if bab == "deret":
        if any(x in text for x in ("bergantian","selang-seling","alternat")):
            return "numerik.deret_alternating"
        if re.search(r"(?:×|x|kali)\s*\d", text) or "dikali" in text:
            return "numerik.deret_multiply"
        return "numerik.deret_difference"
    if bab == "silogisme":
        if "hanya jika" in text or ("jika" in text and any(x in text for x in ("modus","implikasi","maka"))):
            return "logika.only_if"
    return CHAPTER_DEFAULT.get(bab, f"bab.{bab or 'unknown'}")

def tag_question(q):
    if not getattr(q, "skill", ""):
        q.skill = classify_legacy(q.to_dict())
    return q
