"""Daftar dasar hukum TSKKWK dari daftar pengguna, beserta hasil pengecekan (Oktober 2026).

status:
  "ok"       : ditemukan di sumber resmi/tepercaya pada pengecekan ini
  "memori"   : berdasarkan pengetahuan umum, BELUM dicek pada pengecekan ini
  "koreksi"   : penulisan di daftar tampaknya keliru; ini koreksinya
  "belum"    : TIDAK ditemukan; perlu dicari sendiri
  "dicabut"  : ada, tetapi sudah digantikan
"""
from __future__ import annotations

REGULASI = [
    # (nomor di daftar pengguna, nomor yang benar, judul/isi, status, catatan, bab terkait)
    ("UU 22/2023", "UU 20/2023", "Aparatur Sipil Negara (ASN)", "koreksi",
     "UU 22/2023 adalah pengesahan Treaty on the Prohibition of Nuclear Weapons, bukan ASN. Kemungkinan salah ketik dari UU 20/2023 (sudah ada di daftar).", "kepegawaian"),
    ("PP 42/2004", "PP 42/2004", "Pembinaan Jiwa Korps dan Kode Etik PNS", "ok", "Muncul sebagai dasar kode etik PNS pada sumber 2026. Cek status berlakunya setelah UU 20/2023.", "etika"),
    ("SE 44/MK.01/2017", "SE-44/MK.1/2017 (?)", "Belum diketahui", "belum",
     "Tidak ditemukan dengan format SE-44/MK.1/2017 maupun SE-44/MK.01/2017. Ditemukan SE-44/MK.1/2020 (Pelaksanaan Konseling Pegawai); cek apakah tahunnya keliru.", "kepegawaian"),
    ("SE 12/MK.01/2019", "SE-12/MK.1/2019 (?)", "Belum diketahui", "belum",
     "Tidak ditemukan. Ditemukan SE-12/MK.1/2018 (nilai-nilai dan kode etik sebagai early warning system) dan SE-12/MK.1/2021 (COVID-19). Cek tahun atau nomor.", "kepegawaian"),
    ("PMK 190/PMK.01/2018", "PMK 190/PMK.01/2018", "Kode Etik dan Kode Perilaku PNS di Lingkungan Kementerian Keuangan", "ok", "Dikonfirmasi di laman DJPb.", "etika"),
    ("PP 53/2010", "PP 53/2010", "Disiplin PNS (lama)", "dicabut", "Digantikan PP 94/2021. PP 94/2021 tidak ada di daftar Anda.", "kepegawaian"),
    ("PMK 190/PMK.1/2018", "PMK 190/PMK.01/2018", "Kode Etik dan Kode Perilaku PNS Kemenkeu", "koreksi", "Duplikat dengan baris PMK 190/PMK.01/2018 (penulisan nomor berbeda).", "etika"),
    ("KMK 942/KMK.01/2019", "KMK 942/KMK.01/2019", "Pengelolaan Keamanan Informasi di Lingkungan Kementerian Keuangan", "ok", "Dikonfirmasi di beberapa laman Kemenkeu/DJPb/DJKN.", "kepegawaian"),
    ("UU 20/2023", "UU 20/2023", "Aparatur Sipil Negara", "ok", "Menggantikan UU 5/2014.", "kepegawaian"),
    ("KMK 127/KMK.01/2013", "KMK 127/KMK.01/2013", "Program Budaya di Lingkungan Kementerian Keuangan Tahun 2013", "ok",
     "Lima program budaya: Satu Informasi Setiap Hari; Dua Menit Sebelum Jadual; Tiga Salam Setiap Hari; Rencanakan, Kerjakan, Monitor dan Tindaklanjuti; Ringkas, Rapi, Resik, Rawat, Rajin. Ditetapkan 3 April 2013.", "nilai"),
    ("SE 12/MK.1/2018", "SE-12/MK.1/2018", "Penerapan Nilai-Nilai Kementerian Keuangan dan Kode Etik sebagai Early Warning System di Lingkungan Kementerian Keuangan", "ok", "Judul dikonfirmasi lewat surat penyampaian DJPb dan artikel DJPb.", "nilai"),
    ("KMK 429/KMK.01/2022", "KMK 429/KMK.01/2022", "Penguatan Budaya di Lingkungan Kementerian Keuangan", "ok", "Dikonfirmasi di laman DJPb dan dokumen KMK lain yang merujuknya.", "nilai"),
    ("PP 17/2020", "PP 17/2020", "Perubahan atas PP 11/2017 tentang Manajemen PNS", "ok", "Dirujuk dalam PMK 224/PMK.01/2020.", "kepegawaian"),
    ("PP 11/2017", "PP 11/2017", "Manajemen Pegawai Negeri Sipil", "ok", "Dirujuk dalam Peraturan BKN 24/2017 dan PMK 216/PMK.01/2018.", "kepegawaian"),
    ("UU 5/2014", "UU 5/2014", "Aparatur Sipil Negara (lama)", "dicabut", "Digantikan UU 20/2023.", "kepegawaian"),
    ("PMK 224/PMK.01/2020", "PMK 224/PMK.01/2020", "Manajemen Karier di Lingkungan Kementerian Keuangan", "ok", "Berlaku 30 Maret 2021; mencabut PMK 75/PMK.01/2008 dan PMK 39/PMK.01/2009. Dikonfirmasi di JDIH Kemenkeu dan JDIH BPK.", "kepegawaian"),
    ("PMK 216/PMK.01/2018", "PMK 216/PMK.01/2018", "Manajemen Pengembangan Sumber Daya Manusia di Lingkungan Kementerian Keuangan", "ok", "Berlaku 31 Desember 2018. Dikonfirmasi di JDIH BPK dan JDIH Kemenkeu.", "kepegawaian"),
    ("Peraturan Kepala BKN 24/2017", "Peraturan BKN 24/2017", "Tata Cara Pemberian Cuti Pegawai Negeri Sipil", "ok", "Diubah dengan Peraturan BKN 7/2021. (Catatan: tebakan saya sebelumnya, “pemberhentian PNS”, keliru.)", "kepegawaian"),
    ("SE-15/MK.1/2018", "SE-15/MK.1/2018", "Pelaksanaan Cuti bagi Pegawai Negeri Sipil di Lingkungan Kementerian Keuangan", "ok", "Dikonfirmasi di artikel DJKN.", "kepegawaian"),
    ("SE-4/MK.1/2019", "SE-4/MK.1/2019", "Mekanisme Cuti secara Online di Lingkungan Kementerian Keuangan", "ok", "Sumber salinan dokumen kurang resmi (Studocu); judul konsisten dengan isinya. Cocokkan dengan dokumen aslinya.", "kepegawaian"),
    ("UU 17/2003", "UU 17/2003", "Keuangan Negara", "memori", "Pengetahuan umum; belum dicek pada pengecekan ini. UU 1/2004 dan UU 15/2004 belum ada di daftar.", "keuangan"),
    ("UU 4/2023", "UU 4/2023", "Pengembangan dan Penguatan Sektor Keuangan (P2SK)", "ok", "Terdaftar di basis data peraturan BPK. Muncul dua kali di daftar Anda.", "struktur"),
    ("PP 158/2024", "Perpres 158/2024", "Kementerian Keuangan", "koreksi", "Ini Peraturan Presiden, bukan PP. Menjadi dasar susunan organisasi Kemenkeu. Muncul dua kali di daftar Anda.", "struktur"),
    ("PMK 124/2024", "PMK 124/2024", "Penataan organisasi dan tata kerja Kementerian Keuangan", "ok", "Perincian dari Perpres 158/2024. Muncul dua kali di daftar Anda.", "struktur"),
    ("UU 39/2008", "UU 39/2008", "Kementerian Negara", "memori", "Pengetahuan umum; belum dicek pada pengecekan ini.", "struktur"),
    ("PP 140/2024", "Perpres 140/2024", "Organisasi Kementerian Negara", "koreksi", "Tidak ada PP 140/2024 dengan topik ini. Yang ada Peraturan Presiden 140/2024 tentang Organisasi Kementerian Negara (21 Oktober 2024).", "struktur"),
]

STATUS_LABEL = {"ok": "terverifikasi", "memori": "dari pengetahuan umum", "koreksi": "perlu dikoreksi", "belum": "tidak ditemukan", "dicabut": "sudah digantikan"}

DAFTAR_TAMBAHAN = [
    ("PP 94/2021", "Disiplin PNS (menggantikan PP 53/2010). Tidak ada di daftar Anda."),
    ("UU 1/2004 dan UU 15/2004", "Perbendaharaan Negara dan Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara; pasangan UU 17/2003."),
    ("KMK 312/KMK.01/2011", "Nilai-Nilai Kementerian Keuangan (IProSPeK). Tidak ada di daftar Anda."),
    ("PMK 123/2023", "Tata cara pemeriksaan pelanggaran disiplin di lingkungan Kemenkeu (disebut di laman DJPb; belum jelas masuk cakupan)."),
]
