"""Official/current source anchors used to validate TSKKWK material.
The 2026 UPKP notice names TSKKWK as one exam category but does not publish
an official six-domain blueprint. These domains are therefore teaching domains.
"""
TSKKWK_SOURCES = {
  "etika":[
    {"name":"UU 20/2023 tentang ASN","url":"https://peraturan.bpk.go.id/Details/269470/uu-no20-tahun-2023"},
    {"name":"PMK 190/PMK.01/2018 — Kode Etik dan Kode Perilaku","url":"https://jdih.kemenkeu.go.id/dok/190-pmk-01-2018/overview"},
  ],
  "wawasan":[
    {"name":"UUD NRI Tahun 1945 — sumber konstitusional","url":"https://www.dpr.go.id/jdih/uu1945"},
  ],
  "nilai":[
    {"name":"Nilai-Nilai Kementerian Keuangan","url":"https://djpb.kemenkeu.go.id/kppn/barabai/id/profil/budaya-organisasi/nilai-nilai-kemenkeu.html"},
    {"name":"PMK 190/PMK.01/2018 — Kode Etik dan Kode Perilaku","url":"https://jdih.kemenkeu.go.id/dok/190-pmk-01-2018/overview"},
  ],
  "kepegawaian":[
    {"name":"UU 20/2023 tentang ASN","url":"https://peraturan.bpk.go.id/Details/269470/uu-no20-tahun-2023"},
    {"name":"PP 94/2021 tentang Disiplin PNS","url":"https://peraturan.bpk.go.id/Download/170383/PP%20Nomor%2094%20Tahun%202021.pdf"},
    {"name":"PMK 123/2023 — Pemeriksaan Pelanggaran Disiplin","url":"https://jdih.kemenkeu.go.id/dok/pmk-123-tahun-2023/view"},
    {"name":"Peraturan BKN 7/2021 — Cuti PNS","url":"https://www.bkn.go.id/layanan/cuti-asn/"},
  ],
  "keuangan":[
    {"name":"UU 17/2003 tentang Keuangan Negara","url":"https://peraturan.bpk.go.id/Details/43017/uu-no-17-tahun-2003"},
    {"name":"UU 1/2004 tentang Perbendaharaan Negara","url":"https://peraturan.bpk.go.id/Details/40446/uu-no-1-tahun-2004"},
    {"name":"UU 15/2004 tentang Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara","url":"https://peraturan.bpk.go.id/Details/40509/uu-no-15-tahun-2004"},
  ],
  "struktur":[
    {"name":"PMK 124/2024 — Organisasi dan Tata Kerja Kementerian Keuangan","url":"https://jdih.kemenkeu.go.id/dok/pmk-124-tahun-2024/view"},
    {"name":"PMK 117/2025 — Perubahan atas PMK 124/2024","url":"https://jdih.kemenkeu.go.id/dok/pmk-117-tahun-2025"},
  ],
}
UPKP_2026_PAGE = "https://sites.google.com/view/upkp2026/beranda"
UPKP_2026_JUKNIS_PAGE = "https://sites.google.com/view/upkp2026/petunjuk-teknis"
UPKP_2026_TPA_CONVERSION_PAGE = "https://sites.google.com/view/upkp2026/konversi-nilai-tpa"
TPA_OFFICIAL_SUBTESTS = ("Verbal", "Numerikal", "Figural")
# Topics explicitly listed in Section D of the UPKP 2026 portal page.
TSKKWK_OFFICIAL_CODES = ("etika", "nilai", "kepegawaian", "keuangan", "wawasan")
TSKKWK_OFFICIAL_TOPICS = (
    "Etika Pegawai Negeri Sipil",
    "Nilai-Nilai Kementerian Keuangan",
    "Tata Aturan Kepegawaian",
    "Pengelolaan Keuangan Negara",
    "Wawasan Kebangsaan",
)
# Retained as optional study enrichment; not included in official TSKKWK readiness.
TSKKWK_ENRICHMENT_CODES = ("struktur",)

VALIDATION = {
  "notice": "Portal UPKP 2026 menyebut Tes Potensi (Verbal, Numerikal, Figural) dan TSKKWK.",
  "tpa_scope": "Tiga kelompok Tes Potensi dikonfirmasi pada portal resmi; rincian topik per subtes dan bobot item belum dikonfirmasi dari Juknis yang dapat diakses.",
  "tskkwk_scope": "Portal resmi mencantumkan lima topik TSKKWK: Etika PNS, Nilai Kemenkeu, Tata Aturan Kepegawaian, Pengelolaan Keuangan Negara, dan Wawasan Kebangsaan. Struktur Kemenkeu dipertahankan sebagai pengayaan internal.",
  "portal_note": "Halaman berjudul UPKP 2026 memuat teks bagian D yang menyebut penyelenggaraan Tahun 2025. Karena tautan Petunjuk Teknis tidak dapat dibaca pada pemeriksaan ini, rincian topik/bobot perlu dikonfirmasi lagi dari dokumen Juknis.",
  "validated_at": "2026-11-09",
}
