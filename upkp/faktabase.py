"""Basis fakta terstruktur untuk pembangkit soal otomatis (TSKKWK dan pengelompokan kata).

Aturan: hanya fakta yang jelas dan tidak ambigu yang masuk. Dua surat edaran yang belum ditemukan
(SE 44/MK.01/2017 dan SE 12/MK.01/2019) sengaja TIDAK dimasukkan.
Kolom `sumber`: "cek" = ditemukan di sumber resmi/tepercaya pada pengecekan Oktober 2026;
                "umum" = pengetahuan umum, cocokkan dengan buku.
"""
from __future__ import annotations

# --------------------------------------------------------------------- REGULASI
# kunci, nomor tepat, judul (persis), bab, tingkat, sumber, boleh_t2 (judul unik dipakai sebagai petunjuk)
REGULASI_FAKTA = [
    ("uu20-2023", "UU Nomor 20 Tahun 2023", "Aparatur Sipil Negara", "kepegawaian", 1, "cek", True),
    ("pp94-2021", "PP Nomor 94 Tahun 2021", "Disiplin Pegawai Negeri Sipil", "kepegawaian", 1, "cek", True),
    ("pp11-2017", "PP Nomor 11 Tahun 2017", "Manajemen Pegawai Negeri Sipil", "kepegawaian", 1, "cek", True),
    ("pp17-2020", "PP Nomor 17 Tahun 2020", "Perubahan atas PP Nomor 11 Tahun 2017 tentang Manajemen Pegawai Negeri Sipil", "kepegawaian", 2, "cek", False),
    ("pp42-2004", "PP Nomor 42 Tahun 2004", "Pembinaan Jiwa Korps dan Kode Etik Pegawai Negeri Sipil", "etika", 2, "cek", True),
    ("pmk190-2018", "PMK Nomor 190/PMK.01/2018", "Kode Etik dan Kode Perilaku Pegawai Negeri Sipil di Lingkungan Kementerian Keuangan", "etika", 1, "cek", True),
    ("bkn24-2017", "Peraturan BKN Nomor 24 Tahun 2017", "Tata Cara Pemberian Cuti Pegawai Negeri Sipil", "kepegawaian", 2, "cek", True),
    ("se15-2018", "SE-15/MK.1/2018", "Pelaksanaan Cuti bagi Pegawai Negeri Sipil di Lingkungan Kementerian Keuangan", "kepegawaian", 3, "cek", True),
    ("se4-2019", "SE-4/MK.1/2019", "Mekanisme Cuti secara Online di Lingkungan Kementerian Keuangan", "kepegawaian", 3, "cek", True),
    ("pmk224-2020", "PMK Nomor 224/PMK.01/2020", "Manajemen Karier di Lingkungan Kementerian Keuangan", "kepegawaian", 2, "cek", True),
    ("pmk216-2018", "PMK Nomor 216/PMK.01/2018", "Manajemen Pengembangan Sumber Daya Manusia di Lingkungan Kementerian Keuangan", "kepegawaian", 2, "cek", True),
    ("kmk942-2019", "KMK Nomor 942/KMK.01/2019", "Pengelolaan Keamanan Informasi di Lingkungan Kementerian Keuangan", "kepegawaian", 3, "cek", True),
    ("pmk123-2023", "PMK Nomor 123 Tahun 2023", "Tata Cara Pemeriksaan Pelanggaran Disiplin dan Penjatuhan Hukuman Disiplin di Lingkungan Kementerian Keuangan", "kepegawaian", 3, "cek", True),
    ("kmk312-2011", "KMK Nomor 312/KMK.01/2011", "Nilai-Nilai Kementerian Keuangan", "nilai", 1, "cek", True),
    ("kmk127-2013", "KMK Nomor 127/KMK.01/2013", "Program Budaya di Lingkungan Kementerian Keuangan Tahun 2013", "nilai", 2, "cek", True),
    ("se12-2018", "SE-12/MK.1/2018", "Penerapan Nilai-Nilai Kementerian Keuangan dan Kode Etik sebagai Early Warning System di Lingkungan Kementerian Keuangan", "nilai", 3, "cek", True),
    ("kmk429-2022", "KMK Nomor 429/KMK.01/2022", "Penguatan Budaya di Lingkungan Kementerian Keuangan", "nilai", 3, "cek", True),
    ("uu17-2003", "UU Nomor 17 Tahun 2003", "Keuangan Negara", "keuangan", 1, "umum", True),
    ("uu1-2004", "UU Nomor 1 Tahun 2004", "Perbendaharaan Negara", "keuangan", 1, "umum", True),
    ("uu15-2004", "UU Nomor 15 Tahun 2004", "Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara", "keuangan", 2, "umum", True),
    ("perpres158-2024", "Perpres Nomor 158 Tahun 2024", "Kementerian Keuangan", "struktur", 2, "cek", True),
    ("pmk124-2024", "PMK Nomor 124 Tahun 2024", "Penataan Organisasi dan Tata Kerja Kementerian Keuangan", "struktur", 3, "cek", True),
    ("perpres140-2024", "Perpres Nomor 140 Tahun 2024", "Organisasi Kementerian Negara", "struktur", 3, "cek", True),
    ("uu39-2008", "UU Nomor 39 Tahun 2008", "Kementerian Negara", "struktur", 2, "umum", True),
    ("uu4-2023", "UU Nomor 4 Tahun 2023", "Pengembangan dan Penguatan Sektor Keuangan", "struktur", 2, "cek", True),
]

# peraturan lama → peraturan yang menggantikan (lama, baru, topik)
SUPERSESI = [
    ("PP Nomor 53 Tahun 2010", "PP Nomor 94 Tahun 2021", "disiplin Pegawai Negeri Sipil", 2),
    ("UU Nomor 5 Tahun 2014", "UU Nomor 20 Tahun 2023", "Aparatur Sipil Negara", 1),
]

# --------------------------------------------------------------------- NILAI KEMENKEU
NILAI_KEMENKEU = {
    "Integritas": {
        "def": "Berpikir, berkata, berperilaku, dan bertindak dengan baik dan benar serta memegang teguh kode etik dan prinsip-prinsip moral",
        "perilaku": ["Bersikap jujur, tulus, dan dapat dipercaya", "Bertindak transparan dan konsisten", "Menjaga martabat dan tidak melakukan hal-hal tercela",
                     "Bertanggung jawab atas hasil kerja", "Bersikap obyektif"],
    },
    "Profesionalisme": {
        "def": "Bekerja tuntas dan akurat atas dasar kompetensi terbaik dengan penuh tanggung jawab dan komitmen yang tinggi",
        "perilaku": ["Mempunyai keahlian dan pengetahuan yang luas", "Memiliki kepercayaan diri yang tinggi", "Bekerja efisien dan efektif",
                     "Bekerja cerdas, cepat, dan tuntas", "Bekerja dengan hati"],
    },
    "Sinergi": {
        "def": "Membangun dan memastikan hubungan kerja sama internal yang produktif serta kemitraan yang harmonis dengan para pemangku kepentingan",
        "perilaku": ["Memiliki sangka baik, saling percaya, dan menghormati", "Berkomunikasi dengan sikap terbuka dan menghargai perbedaan",
                     "Menemukan dan melaksanakan solusi terbaik", "Berorientasi pada hasil yang memberikan nilai tambah"],
    },
    "Pelayanan": {
        "def": "Memberikan pelayanan untuk memenuhi kepuasan para pemangku kepentingan dengan sepenuh hati, transparan, cepat, akurat, dan aman",
        "perilaku": ["Melayani dengan berorientasi pada kepuasan pemangku kepentingan"],
    },
    "Kesempurnaan": {
        "def": "Senantiasa melakukan upaya perbaikan di segala bidang untuk menjadi dan memberikan yang terbaik",
        "perilaku": [],
    },
}

PROGRAM_BUDAYA = [
    ("Satu Informasi Setiap Hari", "mencari informasi yang positif dan membaginya dengan pegawai lain untuk pengetahuan bersama"),
    ("Dua Menit Sebelum Jadual", "melatih kedisiplinan dengan hadir di tempat rapat dua menit sebelum rapat dimulai"),
    ("Tiga Salam Setiap Hari", "membiasakan pelayanan terbaik dan sopan santun dengan memberi salam pagi, siang, dan sore"),
    ("Rencanakan, Kerjakan, Monitor dan Tindaklanjuti", "menerapkan etos kerja dan prinsip manajemen yang baik: merencanakan, mengerjakan hingga tuntas, memantau, dan menindaklanjuti"),
    ("Ringkas, Rapi, Resik, Rawat, Rajin", "menumbuhkan kepedulian pada penataan ruang kantor dan dokumen kerja yang ringkas, rapi, dan bersih"),
]

# --------------------------------------------------------------------- NILAI DASAR ASN (BerAKHLAK) — pengetahuan umum
BERAKHLAK = {
    "Berorientasi Pelayanan": "komitmen memberikan pelayanan prima demi kepuasan masyarakat",
    "Akuntabel": "bertanggung jawab atas kepercayaan yang diberikan",
    "Kompeten": "terus belajar dan mengembangkan kapabilitas",
    "Harmonis": "saling peduli dan menghargai perbedaan",
    "Loyal": "berdedikasi dan mengutamakan kepentingan bangsa dan negara",
    "Adaptif": "terus berinovasi dan antusias dalam menggerakkan ataupun menghadapi perubahan",
    "Kolaboratif": "membangun kerja sama yang sinergis",
}

# --------------------------------------------------------------------- PANCASILA
SILA = [
    ("Ketuhanan Yang Maha Esa", "bintang"),
    ("Kemanusiaan yang Adil dan Beradab", "rantai"),
    ("Persatuan Indonesia", "pohon beringin"),
    ("Kerakyatan yang Dipimpin oleh Hikmat Kebijaksanaan dalam Permusyawaratan/Perwakilan", "kepala banteng"),
    ("Keadilan Sosial bagi Seluruh Rakyat Indonesia", "padi dan kapas"),
]

# --------------------------------------------------------------------- UNIT ESELON I KEMENKEU
# singkatan (None bila belum baku), nama, fungsi
UNIT = [
    ("Setjen", "Sekretariat Jenderal", "pembinaan dan dukungan administrasi bagi seluruh unit Kementerian Keuangan"),
    ("Itjen", "Inspektorat Jenderal", "pengawasan intern di lingkungan Kementerian Keuangan"),
    ("DJA", "Direktorat Jenderal Anggaran", "perumusan dan pelaksanaan kebijakan di bidang penganggaran"),
    ("DJP", "Direktorat Jenderal Pajak", "perpajakan dan penerimaan pajak"),
    ("DJBC", "Direktorat Jenderal Bea dan Cukai", "kepabeanan dan cukai"),
    ("DJPb", "Direktorat Jenderal Perbendaharaan", "perbendaharaan negara, pengelolaan kas dan pelaksanaan anggaran"),
    ("DJKN", "Direktorat Jenderal Kekayaan Negara", "kekayaan negara, piutang negara, dan lelang"),
    ("DJPK", "Direktorat Jenderal Perimbangan Keuangan", "hubungan keuangan antara pemerintah pusat dan daerah"),
    ("DJPPR", "Direktorat Jenderal Pengelolaan Pembiayaan dan Risiko", "pengelolaan utang, surat berharga negara, pembiayaan, dan risiko"),
    ("DJSEF", "Direktorat Jenderal Strategi Ekonomi dan Fiskal", "kebijakan strategi ekonomi dan fiskal, melanjutkan pekerjaan Badan Kebijakan Fiskal"),
    ("DJSPSK", "Direktorat Jenderal Stabilitas dan Pengembangan Sektor Keuangan", "kebijakan sektor keuangan, profesi keuangan, dan kerja sama internasional"),
    (None, "Badan Teknologi, Informasi, dan Intelijen Keuangan", "teknologi informasi dan intelijen keuangan sebagai tulang punggung TI Kementerian Keuangan"),
    ("BPPK", "Badan Pendidikan dan Pelatihan Keuangan", "pendidikan, pelatihan, dan pengembangan SDM keuangan negara"),
]

# --------------------------------------------------------------------- HUKUMAN DISIPLIN (PP 94/2021) — cocokkan dengan buku
HUKUMAN = {
    "ringan": ["Teguran lisan", "Teguran tertulis", "Pernyataan tidak puas secara tertulis"],
    "sedang": ["Pemotongan tunjangan kinerja 25% selama 6 bulan", "Pemotongan tunjangan kinerja 25% selama 9 bulan", "Pemotongan tunjangan kinerja 25% selama 12 bulan"],
    "berat": ["Penurunan jabatan setingkat lebih rendah selama 12 bulan", "Pembebasan dari jabatan menjadi jabatan pelaksana selama 12 bulan",
              "Pemberhentian dengan hormat tidak atas permintaan sendiri", "Pemberhentian tidak dengan hormat sebagai PNS"],
}

# --------------------------------------------------------------------- KATEGORI untuk soal "kata yang tidak sekelompok"
# nama, tingkat, anggota (>= 4), bukan (pasti bukan anggota)
KATEGORI = [
    ("hewan pemakan tumbuhan (herbivora)", 1, ["Sapi", "Kambing", "Kuda", "Kelinci", "Kerbau", "Zebra", "Jerapah", "Domba"], ["Harimau", "Singa", "Serigala", "Elang", "Buaya", "Hiu"]),
    ("bangun datar", 1, ["Persegi", "Lingkaran", "Trapesium", "Segitiga", "Belah ketupat", "Jajar genjang", "Layang-layang"], ["Kubus", "Balok", "Tabung", "Kerucut", "Bola", "Limas"]),
    ("bangun ruang", 1, ["Kubus", "Balok", "Tabung", "Kerucut", "Bola", "Limas", "Prisma"], ["Persegi", "Lingkaran", "Segitiga", "Trapesium", "Jajar genjang"]),
    ("warna", 1, ["Merah", "Biru", "Hijau", "Kuning", "Ungu", "Jingga", "Cokelat"], ["Segitiga", "Persegi", "Lingkaran", "Kubus", "Jajar genjang"]),
    ("ibu kota provinsi", 1, ["Bandung", "Semarang", "Surabaya", "Medan", "Palembang", "Makassar", "Denpasar", "Pontianak", "Manado", "Jayapura", "Padang"], ["Bogor", "Malang", "Surakarta", "Bekasi", "Depok", "Cirebon"]),
    ("samudra", 1, ["Samudra Pasifik", "Samudra Atlantik", "Samudra Hindia", "Samudra Arktik"], ["Laut Jawa", "Laut Banda", "Laut Natuna", "Laut Merah", "Laut Arafura"]),
    ("logam paduan (aloi)", 2, ["Perunggu", "Kuningan", "Baja", "Solder"], ["Emas", "Perak", "Tembaga", "Seng", "Aluminium", "Timah"]),
    ("logam murni (unsur)", 2, ["Emas", "Perak", "Tembaga", "Seng", "Aluminium", "Timah"], ["Perunggu", "Kuningan", "Baja", "Solder"]),
    ("negara anggota ASEAN", 2, ["Indonesia", "Malaysia", "Singapura", "Thailand", "Filipina", "Brunei Darussalam", "Vietnam", "Laos", "Kamboja", "Myanmar"], ["Jepang", "India", "Bangladesh", "Tiongkok", "Korea Selatan", "Pakistan", "Australia"]),
    ("Presiden Republik Indonesia", 2, ["Soekarno", "Soeharto", "B.J. Habibie", "Abdurrahman Wahid", "Megawati Soekarnoputri", "Susilo Bambang Yudhoyono", "Joko Widodo", "Prabowo Subianto"],
     ["Mohammad Hatta", "Adam Malik", "Try Sutrisno", "Jusuf Kalla", "Boediono", "Hamzah Haz"]),
    ("planet dalam Tata Surya", 2, ["Merkurius", "Venus", "Bumi", "Mars", "Jupiter", "Saturnus", "Uranus", "Neptunus"], ["Bulan", "Matahari", "Pluto", "Sirius"]),
    ("unit eselon I Kementerian Keuangan", 2, ["Direktorat Jenderal Pajak", "Direktorat Jenderal Bea dan Cukai", "Direktorat Jenderal Anggaran", "Direktorat Jenderal Perbendaharaan",
                                                 "Direktorat Jenderal Kekayaan Negara", "Direktorat Jenderal Perimbangan Keuangan", "Inspektorat Jenderal", "Badan Pendidikan dan Pelatihan Keuangan"],
     ["Otoritas Jasa Keuangan", "Badan Pengawasan Keuangan dan Pembangunan", "Badan Pemeriksa Keuangan", "Bank Indonesia", "Badan Pusat Statistik", "Lembaga Penjamin Simpanan"]),
    ("bulan yang berjumlah 31 hari", 3, ["Januari", "Maret", "Mei", "Juli", "Agustus", "Oktober", "Desember"], ["April", "Juni", "September", "November"]),
    ("bulan yang berjumlah 30 hari", 3, ["April", "Juni", "September", "November"], ["Januari", "Maret", "Mei", "Juli", "Agustus", "Oktober", "Desember"]),
    ("nilai-nilai Kementerian Keuangan", 3, ["Integritas", "Profesionalisme", "Sinergi", "Pelayanan", "Kesempurnaan"], ["Akuntabel", "Kompeten", "Harmonis", "Loyal", "Adaptif", "Kolaboratif"]),
    ("nilai dasar ASN (BerAKHLAK)", 3, ["Berorientasi Pelayanan", "Akuntabel", "Kompeten", "Harmonis", "Loyal", "Adaptif", "Kolaboratif"], ["Integritas", "Profesionalisme", "Sinergi", "Kesempurnaan"]),
    ("lembaga negara menurut UUD 1945", 3, ["Majelis Permusyawaratan Rakyat", "Dewan Perwakilan Rakyat", "Dewan Perwakilan Daerah", "Badan Pemeriksa Keuangan", "Mahkamah Agung", "Mahkamah Konstitusi", "Komisi Yudisial"],
     ["Komisi Pemberantasan Korupsi", "Otoritas Jasa Keuangan", "Komisi Nasional Hak Asasi Manusia", "Ombudsman Republik Indonesia"]),
]
