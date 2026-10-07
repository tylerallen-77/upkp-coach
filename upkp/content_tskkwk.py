"""Soal TSKKWK (Tes Substansi Kemenkeu dan Wawasan Kebangsaan).

PENTING: halaman buku bagian ini (hlm. 83 dst.) belum tersedia. Isi disusun dari pengetahuan umum dan
sumber resmi yang diverifikasi Oktober 2026 (lihat `SUMBER`). Peraturan dan struktur organisasi bisa
berubah. Cocokkan dengan buku dan peraturan terbaru sebelum dipakai sebagai patokan ujian.
"""
from __future__ import annotations

from .model import mk
from .registry import GENS

SUMBER = {
    "struktur": "Perpres 158/2024 tentang Kementerian Keuangan; PMK 124/2024 (penataan organisasi dan tata kerja Kemenkeu); Perpres 140/2024 (Organisasi Kementerian Negara); UU 39/2008; UU 4/2023. "
                "BKF dihapus; dibentuk DJ Strategi Ekonomi dan Fiskal, DJ Stabilitas dan Pengembangan Sektor Keuangan, dan Badan Teknologi, Informasi, dan Intelijen Keuangan. Cek aturan yang lebih baru.",
    "nilai": "KMK 312/KMK.01/2011 (IProSPeK); PMK 190/PMK.01/2018; KMK 127/KMK.01/2013 (Program Budaya); SE-12/MK.1/2018; KMK 429/KMK.01/2022 (Penguatan Budaya).",
    "kepegawaian": "UU 20/2023; PP 94/2021; PP 11/2017 dan PP 17/2020; Peraturan BKN 24/2017 (cuti); SE-15/MK.1/2018 dan SE-4/MK.1/2019 (cuti Kemenkeu); PMK 216/PMK.01/2018; PMK 224/PMK.01/2020; KMK 942/KMK.01/2019.",
    "keuangan": "UU 17/2003 Keuangan Negara; UU 1/2004 Perbendaharaan Negara; UU 15/2004 Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara.",
    "wawasan": "UUD 1945 dan pengetahuan umum kebangsaan.",
    "etika": "UU 20/2023; PP 94/2021; PP 42/2004; PMK 190/PMK.01/2018; BerAKHLAK.",
}

# [stem, jawab, 4 pengecoh, pembahasan, cara cepat, tingkat]
BANK = {
    "etika": [
        ("Nilai dasar ASN yang disingkat BerAKHLAK terdiri atas …", "Berorientasi Pelayanan, Akuntabel, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif",
         ["Berintegritas, Akuntabel, Kreatif, Harmonis, Loyal, Adaptif, Kolaboratif", "Berorientasi Pelayanan, Akuntabel, Kompeten, Harmonis, Loyal, Aktif, Kolaboratif",
          "Berorientasi Pelayanan, Amanah, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif", "Berorientasi Pelayanan, Akuntabel, Kompeten, Hormat, Loyal, Adaptif, Kreatif"],
         "BerAKHLAK: Berorientasi Pelayanan, Akuntabel, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif.", "Hafal akronim: B-er-A-K-H-L-A-K → Berorientasi, Akuntabel, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif.", 1),
        ("Seorang PNS menerima bingkisan dari pihak yang sedang mengurus layanan di kantornya. Sikap yang sesuai kode etik adalah …", "Menolak dan melaporkannya sebagai gratifikasi kepada unit pengendali gratifikasi",
         ["Menerima karena tidak diminta", "Menerima lalu membagikannya ke rekan kerja", "Menyimpannya dan melapor bila diperiksa", "Menerima jika nilainya kecil"],
         "Pemberian terkait jabatan berpotensi gratifikasi. Sikap yang benar: menolak, dan melaporkan sesuai ketentuan.", "Pemberian yang berhubungan dengan jabatan dan layanan = tolak, laporkan. Nilai kecil tidak menghapus potensi gratifikasi.", 2),
        ("Penggunaan media sosial yang sesuai etika ASN adalah …", "Menyampaikan informasi resmi yang benar dan tidak menyebarkan ujaran kebencian atau hoaks",
         ["Mengunggah dokumen internal yang belum dipublikasikan", "Mengkritik atasan secara terbuka dengan nama lengkap", "Menyebarkan berita yang belum terverifikasi agar cepat diketahui", "Memberi komentar bernada dukungan terhadap salah satu calon pada pemilihan umum"],
         "ASN wajib menjaga rahasia jabatan, netralitas, dan tidak menyebarkan hoaks atau ujaran kebencian.", "Tiga cek sebelum unggah: rahasia jabatan? netral? benar dan terverifikasi?", 2),
        ("Seorang atasan meminta bawahannya mengubah angka laporan agar target terlihat tercapai. Sikap bawahan yang paling tepat adalah …", "Menolak, menjelaskan alasannya, dan menyampaikan data yang sebenarnya melalui jalur yang berwenang",
         ["Mengikuti perintah karena atasan bertanggung jawab", "Mengubah sedikit saja agar tidak mencolok", "Mengikuti perintah lalu menyimpan bukti pribadi", "Diam dan tidak mengerjakan laporannya"],
         "Integritas dan akuntabilitas menolak manipulasi data. Perintah yang melanggar aturan tidak wajib dilaksanakan; sampaikan lewat jalur resmi.", "Perintah melanggar aturan: tolak dengan santun, jelaskan, lapor lewat jalur resmi.", 3),
    ],
    "wawasan": [
        ("Pancasila sebagai dasar negara tercantum dalam …", "Pembukaan UUD 1945 alinea keempat",
         ["Pasal 1 UUD 1945", "Pembukaan UUD 1945 alinea pertama", "Penjelasan Pasal 33", "Pasal 29 UUD 1945"], "Rumusan Pancasila tercantum pada alinea keempat Pembukaan UUD 1945.", "Alinea 4 memuat tujuan negara dan dasar negara (Pancasila).", 1),
        ("Sila ketiga Pancasila adalah …", "Persatuan Indonesia", ["Kemanusiaan yang Adil dan Beradab", "Kerakyatan yang Dipimpin oleh Hikmat Kebijaksanaan dalam Permusyawaratan/Perwakilan", "Ketuhanan Yang Maha Esa", "Keadilan Sosial bagi Seluruh Rakyat Indonesia"],
         "Urutan sila: 1 Ketuhanan, 2 Kemanusiaan, 3 Persatuan, 4 Kerakyatan, 5 Keadilan sosial.", "Hafal dengan lambang: bintang, rantai, pohon beringin, kepala banteng, padi dan kapas.", 1),
        ("Semboyan “Bhinneka Tunggal Ika” memiliki makna …", "Berbeda-beda tetapi tetap satu",
         ["Satu nusa, satu bangsa, satu bahasa", "Bersatu kita teguh bercerai kita runtuh", "Gotong royong membangun negeri", "Kesatuan dalam keseragaman"], "Bhinneka Tunggal Ika dari Kakawin Sutasoma: berbeda-beda tetapi tetap satu.", "Bhinneka = beragam, tunggal = satu, ika = itu.", 1),
        ("Empat konsensus dasar (pilar) kebangsaan Indonesia adalah …", "Pancasila, UUD 1945, NKRI, dan Bhinneka Tunggal Ika",
         ["Pancasila, UUD 1945, Sumpah Pemuda, dan Proklamasi", "Pancasila, NKRI, Pembukaan UUD, dan Garuda", "UUD 1945, Sumpah Pemuda, NKRI, dan Bhinneka Tunggal Ika", "Pancasila, Proklamasi, TAP MPR, dan NKRI"], "Empat pilar: Pancasila, UUD NRI 1945, NKRI, Bhinneka Tunggal Ika.", "Sebut PUNB: Pancasila, UUD, NKRI, Bhinneka.", 2),
        ("UUD 1945 telah diamandemen sebanyak … kali.", "4 (empat)", ["2 (dua)", "3 (tiga)", "5 (lima)", "6 (enam)"],
         "Amandemen terjadi pada 1999, 2000, 2001, dan 2002 (empat kali).", "Empat amandemen, tahun 1999-2002, berurutan setiap tahun.", 2),
        ("Menurut UUD 1945, kedaulatan berada di tangan rakyat dan dilaksanakan menurut …", "Undang-Undang Dasar", ["Ketetapan MPR", "Peraturan Presiden", "Keputusan DPR", "Peraturan Pemerintah"],
         "Pasal 1 ayat (2) UUD 1945: kedaulatan berada di tangan rakyat dan dilaksanakan menurut Undang-Undang Dasar.", "Pasal 1 ayat (2): kedaulatan rakyat dilaksanakan menurut UUD.", 3),
    ],
    "nilai": [
        ("Nilai-Nilai Kementerian Keuangan terdiri atas …", "Integritas, Profesionalisme, Sinergi, Pelayanan, dan Kesempurnaan",
         ["Integritas, Profesionalisme, Sinergi, Kolaborasi, dan Kesempurnaan", "Integritas, Profesionalisme, Akuntabel, Pelayanan, dan Kesempurnaan", "Integritas, Kompeten, Sinergi, Pelayanan, dan Kesempurnaan", "Loyalitas, Profesionalisme, Sinergi, Pelayanan, dan Kesempurnaan"],
         "Nilai-nilai Kemenkeu disingkat IProSPeK.", "IProSPeK: Integritas, Profesionalisme, Sinergi, Pelayanan, Kesempurnaan.", 1),
        ("“Bekerja tuntas dan akurat atas dasar kompetensi terbaik dengan penuh tanggung jawab dan komitmen yang tinggi” merupakan definisi nilai …", "Profesionalisme",
         ["Integritas", "Sinergi", "Pelayanan", "Kesempurnaan"], "Definisi itu merujuk pada nilai Profesionalisme.", "Kata kunci “tuntas, akurat, kompetensi” → Profesionalisme.", 1),
        ("Nilai Kementerian Keuangan yang berarti senantiasa melakukan upaya perbaikan di segala bidang untuk menjadi dan memberikan yang terbaik adalah …", "Kesempurnaan",
         ["Integritas", "Profesionalisme", "Sinergi", "Pelayanan"], "Kesempurnaan = perbaikan terus-menerus untuk menjadi dan memberikan yang terbaik.", "“Perbaikan terus-menerus” → Kesempurnaan.", 1),
        ("Perilaku utama nilai Sinergi adalah …", "Memiliki sangka baik, saling percaya, dan saling menghormati",
         ["Bertindak transparan dan konsisten", "Bekerja cerdas, cepat, dan tuntas", "Melayani dengan berorientasi pada kepuasan pemangku kepentingan", "Melakukan perbaikan dalam segala bidang"],
         "Sinergi menekankan hubungan kerja sama internal yang produktif: sangka baik, saling percaya, saling menghormati.", "Sinergi → kerja sama. Transparan → Integritas; cerdas, cepat, tuntas → Profesionalisme; kepuasan → Pelayanan.", 2),
        ("Kaidah perilaku utama Nilai-Nilai Kementerian Keuangan ditetapkan dalam …", "Keputusan Menteri Keuangan Nomor 312/KMK.01/2011",
         ["Peraturan Menteri Keuangan Nomor 190/PMK.01/2018", "Undang-Undang Nomor 20 Tahun 2023", "Peraturan Pemerintah Nomor 94 Tahun 2021", "Keputusan Presiden Nomor 1 Tahun 2011"],
         "KMK 312/KMK.01/2011 mengatur Nilai-Nilai Kemenkeu, sedangkan PMK 190/PMK.01/2018 mengatur Kode Etik dan Kode Perilaku PNS Kemenkeu.", "KMK 312 = nilai-nilai; PMK 190 = kode etik dan kode perilaku.", 3),
    ],
    "kepegawaian": [
        ("Undang-undang yang saat ini menjadi dasar utama pengaturan Aparatur Sipil Negara adalah …", "Undang-Undang Nomor 20 Tahun 2023 tentang ASN",
         ["Undang-Undang Nomor 5 Tahun 2014 tentang ASN", "Undang-Undang Nomor 43 Tahun 1999", "Undang-Undang Nomor 8 Tahun 1974", "Undang-Undang Nomor 17 Tahun 2003"],
         "UU 20/2023 menggantikan UU 5/2014 sebagai UU ASN.", "ASN: UU 8/1974 → UU 43/1999 → UU 5/2014 → UU 20/2023.", 1),
        ("Peraturan Pemerintah yang mengatur Disiplin PNS adalah …", "PP Nomor 94 Tahun 2021", ["PP Nomor 53 Tahun 2010", "PP Nomor 11 Tahun 2017", "PP Nomor 30 Tahun 2019", "PP Nomor 42 Tahun 2004"],
         "PP 94/2021 menggantikan PP 53/2010 tentang disiplin PNS.", "Disiplin PNS: PP 94/2021.", 1),
        ("Berdasarkan PP 94/2021, hukuman disiplin PNS dibagi menjadi tiga tingkat, yaitu …", "ringan, sedang, dan berat", ["lisan, tertulis, dan pemecatan", "ringan, berat, dan sangat berat", "teguran, penundaan, dan penurunan", "administratif, pidana, dan perdata"],
         "Tingkat hukuman disiplin: ringan, sedang, berat.", "Ringan → teguran/pernyataan tidak puas; sedang → pemotongan tunjangan; berat → penurunan jabatan sampai pemberhentian.", 1),
        ("Teguran lisan, teguran tertulis, dan pernyataan tidak puas secara tertulis termasuk hukuman disiplin tingkat …", "ringan", ["sedang", "berat", "administratif", "pidana"],
         "Ketiganya adalah jenis hukuman disiplin ringan.", "Ringan = teguran/pernyataan tidak puas, tanpa potongan.", 2),
        ("Nilai dasar ASN BerAKHLAK diterapkan dalam …", "kode etik dan kode perilaku ASN dalam pelaksanaan tugas", ["hanya saat pelantikan", "hanya oleh pejabat struktural", "hanya dalam pengadaan barang", "hanya saat penilaian kinerja tahunan"],
         "Nilai dasar diimplementasikan dan dijabarkan dalam kode etik dan kode perilaku ASN.", "Nilai dasar → kode etik → perilaku sehari-hari.", 2),
        ("Berikut yang BUKAN merupakan kewajiban PNS menurut aturan disiplin adalah …", "Menyalahgunakan wewenang untuk kepentingan pribadi",
         ["Menaati ketentuan jam kerja", "Melaksanakan tugas kedinasan dengan penuh pengabdian", "Menjaga rahasia jabatan", "Bekerja dengan jujur, tertib, cermat, dan bersemangat"],
         "Menyalahgunakan wewenang adalah larangan. Opsi lain adalah kewajiban.", "Kata “menyalahgunakan”, “menerima hadiah”, “memiliki saham”: larangan. Selain itu umumnya kewajiban.", 3),
    ],
    "keuangan": [
        ("Keuangan negara menurut UU Nomor 17 Tahun 2003 adalah …", "semua hak dan kewajiban negara yang dapat dinilai dengan uang, serta segala sesuatu yang dapat dijadikan milik negara berhubung dengan pelaksanaan hak dan kewajiban tersebut",
         ["hanya uang yang tercatat di APBN", "hanya penerimaan pajak dan bukan pajak", "semua kekayaan pemerintah daerah", "semua uang milik BUMN dan BUMD"],
         "Definisi tersebut ada pada Pasal 1 UU 17/2003.", "Kata kunci: hak, kewajiban, dinilai dengan uang, dapat dijadikan milik negara.", 2),
        ("Undang-undang yang mengatur Perbendaharaan Negara adalah …", "UU Nomor 1 Tahun 2004", ["UU Nomor 17 Tahun 2003", "UU Nomor 15 Tahun 2004", "UU Nomor 20 Tahun 2023", "UU Nomor 25 Tahun 2004"],
         "Tiga paket keuangan negara: UU 17/2003 (Keuangan Negara), UU 1/2004 (Perbendaharaan Negara), UU 15/2004 (Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara).", "Urutan tahun: 17/2003, 1/2004, 15/2004.", 1),
        ("Menurut UU Keuangan Negara, Presiden sebagai Kepala Pemerintahan memegang kekuasaan pengelolaan keuangan negara sebagai bagian dari kekuasaan pemerintahan. Kekuasaan itu dikuasakan kepada …", "Menteri Keuangan sebagai pengelola fiskal dan wakil pemerintah dalam kepemilikan kekayaan negara yang dipisahkan, serta menteri/pimpinan lembaga sebagai pengguna anggaran/pengguna barang",
         ["Hanya Menteri Keuangan untuk seluruh pengelolaan", "Hanya DPR sebagai pemegang hak anggaran", "Gubernur Bank Indonesia", "Ketua Badan Pemeriksa Keuangan"],
         "Kekuasaan dikuasakan kepada Menteri Keuangan (pengelola fiskal) dan menteri/pimpinan lembaga (pengguna anggaran/barang).", "Pengelola fiskal = Menkeu; pengguna anggaran/barang = menteri/pimpinan lembaga.", 3),
        ("Pemeriksa eksternal atas pengelolaan dan tanggung jawab keuangan negara adalah …", "Badan Pemeriksa Keuangan (BPK)", ["Inspektorat Jenderal", "Badan Pengawasan Keuangan dan Pembangunan (BPKP)", "Direktorat Jenderal Perbendaharaan", "Kejaksaan Agung"],
         "BPK adalah lembaga pemeriksa eksternal yang bebas dan mandiri. Inspektorat jenderal dan BPKP adalah pengawas internal pemerintah.", "Eksternal = BPK. Internal = APIP (Inspektorat, BPKP).", 1),
        ("Tahun anggaran Anggaran Pendapatan dan Belanja Negara (APBN) berlangsung dari …", "1 Januari sampai 31 Desember", ["1 April sampai 31 Maret", "1 Juli sampai 30 Juni", "1 Oktober sampai 30 September", "1 Februari sampai 31 Januari"],
         "Tahun anggaran sama dengan tahun takwim.", "Tahun anggaran = tahun takwim (Januari–Desember).", 1),
        ("Rancangan APBN diajukan Presiden kepada DPR paling lambat pada bulan …", "Agustus (bersama pidato kenegaraan dan nota keuangan)", ["Januari", "Maret", "Oktober", "Desember"],
         "RUU APBN disampaikan pada Agustus tahun sebelumnya, disertai nota keuangan.", "Agustus: RAPBN diajukan. Oktober: biasanya disahkan.", 2),
    ],
    "struktur": [
        ("Menurut Perpres 158 Tahun 2024, unit eselon I baru di Kementerian Keuangan yang dibentuk adalah …", "Direktorat Jenderal Strategi Ekonomi dan Fiskal, Direktorat Jenderal Stabilitas dan Pengembangan Sektor Keuangan, dan Badan Teknologi, Informasi, dan Intelijen Keuangan",
         ["Badan Kebijakan Fiskal dan Direktorat Jenderal Pajak Baru", "Direktorat Jenderal Pendapatan Negara dan Badan Anggaran", "Direktorat Jenderal Teknologi dan Badan Intelijen Negara", "Hanya Badan Teknologi, Informasi, dan Intelijen Keuangan"],
         "Perpres 158/2024 dan PMK 124/2024 mengubah struktur Kemenkeu: BKF dihapus dan dua ditjen serta satu badan baru dibentuk (menurut pemberitaan resmi Menkeu).", "Ingat 2+1: dua Ditjen (Strategi Ekonomi dan Fiskal; Stabilitas dan Pengembangan Sektor Keuangan) + satu Badan (Teknologi, Informasi, dan Intelijen Keuangan).", 2),
        ("Unit di bawah Kementerian Keuangan yang menangani penerimaan pajak adalah …", "Direktorat Jenderal Pajak", ["Direktorat Jenderal Anggaran", "Direktorat Jenderal Perbendaharaan", "Direktorat Jenderal Kekayaan Negara", "Direktorat Jenderal Perimbangan Keuangan"],
         "DJP mengelola penerimaan pajak. DJBC mengelola bea dan cukai.", "Pajak → DJP; bea dan cukai → DJBC; anggaran → DJA; perbendaharaan → DJPb; lelang dan aset → DJKN.", 1),
        ("Direktorat Jenderal yang bertugas mengelola kekayaan negara, piutang negara, dan lelang adalah …", "Direktorat Jenderal Kekayaan Negara (DJKN)", ["Direktorat Jenderal Anggaran (DJA)", "Direktorat Jenderal Perbendaharaan (DJPb)", "Direktorat Jenderal Bea dan Cukai (DJBC)", "Direktorat Jenderal Perimbangan Keuangan (DJPK)"],
         "DJKN: kekayaan negara, piutang negara, lelang, dan penilaian.", "Aset, lelang, piutang → DJKN.", 1),
        ("Direktorat Jenderal yang mengelola hubungan keuangan antara pemerintah pusat dan daerah (transfer ke daerah) adalah …", "Direktorat Jenderal Perimbangan Keuangan (DJPK)", ["Direktorat Jenderal Anggaran (DJA)", "Direktorat Jenderal Kekayaan Negara (DJKN)", "Direktorat Jenderal Perbendaharaan (DJPb)", "Direktorat Jenderal Pajak (DJP)"],
         "DJPK: perimbangan keuangan pusat dan daerah.", "Pusat–daerah → DJPK.", 2),
        ("Badan Pendidikan dan Pelatihan Keuangan (BPPK) bertugas …", "menyelenggarakan pendidikan, pelatihan, dan pengembangan SDM keuangan negara", ["mengelola utang negara", "memeriksa laporan keuangan kementerian", "menyusun APBN", "mengelola barang milik negara"],
         "BPPK adalah unit eselon I yang menangani pengembangan SDM di bidang keuangan negara.", "BPPK = pendidikan dan pelatihan.", 2),
        ("Direktorat Jenderal Pengelolaan Pembiayaan dan Risiko (DJPPR) bertugas di bidang …", "pengelolaan utang, surat berharga negara, pembiayaan, dan risiko", ["pemungutan pajak", "pengawasan intern", "pelayanan lelang", "pengelolaan hibah daerah"],
         "DJPPR mengelola pembiayaan dan risiko, termasuk surat berharga negara dan utang.", "Utang dan SBN → DJPPR.", 2),
    ],
}


# ---- Tambahan setelah verifikasi daftar regulasi pengguna (Oktober 2026). Lihat upkp/regulasi.py
BANK["etika"] += [
    ("Peraturan Pemerintah Nomor 42 Tahun 2004 mengatur tentang …", "Pembinaan Jiwa Korps dan Kode Etik Pegawai Negeri Sipil",
     ["Disiplin Pegawai Negeri Sipil", "Manajemen Pegawai Negeri Sipil", "Penilaian Kinerja Pegawai Negeri Sipil", "Gaji Pegawai Negeri Sipil"],
     "PP 42/2004 mengatur pembinaan jiwa korps dan kode etik PNS. Disiplin PNS diatur PP 94/2021 (sebelumnya PP 53/2010); manajemen PNS diatur PP 11/2017.", "42 → jiwa korps dan kode etik. 94 → disiplin. 11 → manajemen.", 2),
    ("Kode etik dan kode perilaku PNS di lingkungan Kementerian Keuangan diatur dalam …", "PMK Nomor 190/PMK.01/2018",
     ["PMK Nomor 224/PMK.01/2020", "PMK Nomor 216/PMK.01/2018", "KMK Nomor 942/KMK.01/2019", "KMK Nomor 127/KMK.01/2013"],
     "PMK 190/PMK.01/2018 mengatur Kode Etik dan Kode Perilaku PNS di lingkungan Kemenkeu.", "190 → kode etik; 224 → karier; 216 → pengembangan SDM; 942 → keamanan informasi; 127 → program budaya.", 1),
]
BANK["nilai"] += [
    ("Program Budaya Kementerian Keuangan menurut KMK 127/KMK.01/2013 terdiri atas lima program. Yang BUKAN termasuk adalah …", "Satu Hari Satu Laporan",
     ["Satu Informasi Setiap Hari", "Dua Menit Sebelum Jadual", "Tiga Salam Setiap Hari", "Ringkas, Rapi, Resik, Rawat, Rajin"],
     "Lima program: Satu Informasi Setiap Hari; Dua Menit Sebelum Jadual; Tiga Salam Setiap Hari; Rencanakan, Kerjakan, Monitor dan Tindaklanjuti; Ringkas, Rapi, Resik, Rawat, Rajin.", "Hafal 1-2-3: Satu informasi, Dua menit, Tiga salam; lalu PDCA dan 5R.", 2),
    ("Program budaya “Dua Menit Sebelum Jadual” dimaksudkan untuk melatih kedisiplinan pegawai dengan …", "hadir di ruang rapat dua menit sebelum rapat dimulai sesuai jadwal",
     ["mengirim laporan dua menit sebelum tenggat", "memulai rapat dua menit lebih awal dari jadwal", "membatasi durasi rapat paling lama dua menit", "membaca laporan harian selama dua menit tiap pagi"],
     "KMK 127/KMK.01/2013: hadir di tempat rapat 2 menit sebelum rapat dimulai, supaya rapat efektif dan efisien.", "“Dua menit” = datang lebih awal, bukan rapat dipercepat.", 1),
    ("Program budaya “Tiga Salam Setiap Hari” mendorong pegawai memberi salam …", "selamat pagi, selamat siang, dan selamat sore sesuai waktunya",
     ["tiga kali sehari kepada atasan saja", "sebelum rapat, saat makan, dan saat pulang", "kepada tamu, atasan, dan bawahan", "salam agama, salam nasional, dan salam kantor"],
     "Tujuannya membiasakan pelayanan terbaik dan sikap sopan santun dengan memberi salam sesuai waktu.", "Tiga salam = pagi, siang, sore.", 1),
    ("Program budaya “Rencanakan, Kerjakan, Monitor dan Tindaklanjuti” mencerminkan prinsip manajemen …", "Plan–Do–Check–Action (PDCA)",
     ["Analisis SWOT", "Balanced Scorecard", "Matriks Eisenhower", "Diagram Pareto"],
     "Rencanakan = Plan; Kerjakan = Do; Monitor = Check; Tindaklanjuti = Action.", "Cocokkan kata kerja: rencana-kerja-monitor-tindak lanjut = PDCA.", 1),
    ("Program “Ringkas, Rapi, Resik, Rawat, Rajin” (5R) mendorong kepedulian pegawai pada …", "penataan ruang kantor dan dokumen kerja yang ringkas, rapi, dan bersih",
     ["pengelolaan anggaran kantor", "penghematan listrik dan air", "penampilan dan seragam pegawai", "pengamanan data elektronik"],
     "5R bertujuan menciptakan lingkungan kerja yang nyaman guna meningkatkan etos kerja dan semangat berkarya.", "5R = tata ruang dan dokumen.", 2),
    ("Program budaya “Satu Informasi Setiap Hari” mendorong pegawai untuk …", "mencari informasi yang positif dan membaginya kepada pegawai lain",
     ["menyampaikan satu laporan tiap hari kepada atasan", "membaca satu peraturan baru tiap hari", "mencatat satu kesalahan rekan tiap hari", "mengadakan satu rapat tiap hari"],
     "KMK 127/KMK.01/2013: mencari informasi positif dan berbagi (sharing) untuk pengetahuan bersama.", "Kata kunci: positif dan sharing.", 2),
    ("Surat Edaran Menteri Keuangan Nomor SE-12/MK.1/2018 mengatur tentang …", "penerapan nilai-nilai Kementerian Keuangan dan kode etik sebagai early warning system",
     ["pelaksanaan cuti bagi PNS di lingkungan Kementerian Keuangan", "mekanisme cuti secara online", "pengelolaan keamanan informasi", "manajemen karier pegawai"],
     "SE-12/MK.1/2018 menekankan penerapan nilai dan kode etik sebagai sistem peringatan dini.", "SE-12/2018 → nilai dan kode etik; SE-15/2018 → cuti; SE-4/2019 → cuti online.", 3),
    ("Keputusan Menteri Keuangan Nomor 429/KMK.01/2022 mengatur tentang …", "Penguatan Budaya di Lingkungan Kementerian Keuangan",
     ["Program Budaya Tahun 2013", "Pengelolaan Keamanan Informasi", "Manajemen Karier", "Manajemen Pengembangan SDM"],
     "KMK 429/KMK.01/2022 mengatur penguatan budaya. KMK 127/2013 adalah program budaya tahun 2013.", "Budaya: 127/2013 (program 2013) lalu 429/2022 (penguatan).", 3),
]
BANK["kepegawaian"] += [
    ("Peraturan Pemerintah Nomor 11 Tahun 2017 mengatur tentang …", "Manajemen Pegawai Negeri Sipil",
     ["Disiplin Pegawai Negeri Sipil", "Penilaian Kinerja Pegawai Negeri Sipil", "Jiwa Korps dan Kode Etik Pegawai Negeri Sipil", "Peraturan Gaji Pegawai Negeri Sipil"],
     "PP 11/2017 mengatur manajemen PNS, diubah dengan PP 17/2020.", "11/2017 → manajemen; 94/2021 → disiplin; 30/2019 → penilaian kinerja.", 1),
    ("Peraturan Pemerintah Nomor 17 Tahun 2020 adalah …", "perubahan atas PP Nomor 11 Tahun 2017 tentang Manajemen PNS",
     ["perubahan atas PP Nomor 94 Tahun 2021 tentang Disiplin PNS", "pencabut PP Nomor 53 Tahun 2010", "peraturan pelaksana UU Nomor 17 Tahun 2003", "pengganti UU Nomor 20 Tahun 2023"],
     "PP 17/2020 mengubah PP 11/2017 dan dirujuk sebagai dasar pengaturan ulang manajemen karier di Kemenkeu (PMK 224/PMK.01/2020).", "PP 17/2020 = revisi PP 11/2017.", 2),
    ("Peraturan Badan Kepegawaian Negara Nomor 24 Tahun 2017 mengatur tentang …", "Tata Cara Pemberian Cuti Pegawai Negeri Sipil",
     ["Tata Cara Pemberhentian PNS", "Penilaian Kinerja PNS", "Disiplin PNS", "Formasi dan Pengadaan PNS"],
     "Peraturan BKN 24/2017 mengatur tata cara pemberian cuti PNS. Diubah dengan Peraturan BKN 7/2021.", "BKN 24/2017 = cuti.", 2),
    ("Surat Edaran Menteri Keuangan Nomor SE-15/MK.1/2018 mengatur tentang …", "pelaksanaan cuti bagi PNS di lingkungan Kementerian Keuangan",
     ["penerapan nilai-nilai dan kode etik sebagai early warning system", "manajemen karier pegawai", "pengelolaan keamanan informasi", "jam kerja pada bulan Ramadan"],
     "SE-15/MK.1/2018 adalah ketentuan pelaksanaan cuti PNS Kemenkeu.", "SE-15/2018 → cuti.", 2),
    ("Mekanisme pengajuan cuti secara online di lingkungan Kementerian Keuangan diatur dalam …", "SE-4/MK.1/2019",
     ["SE-15/MK.1/2018", "SE-12/MK.1/2018", "KMK 942/KMK.01/2019", "PMK 224/PMK.01/2020"],
     "SE-4/MK.1/2019 tentang Mekanisme Cuti secara Online (sumber salinan kurang resmi; cocokkan dengan dokumen aslinya).", "Online → SE-4/2019; ketentuan cuti umum → SE-15/2018.", 3),
    ("Peraturan Menteri Keuangan Nomor 224/PMK.01/2020 mengatur tentang …", "Manajemen Karier di Lingkungan Kementerian Keuangan",
     ["Manajemen Pengembangan SDM", "Kode Etik dan Kode Perilaku", "Penguatan Budaya", "Pengelolaan Keamanan Informasi"],
     "PMK 224/PMK.01/2020 berlaku sejak 30 Maret 2021 dan mencabut PMK 75/PMK.01/2008 serta PMK 39/PMK.01/2009.", "224/2020 → karier; 216/2018 → pengembangan SDM.", 2),
    ("Peraturan Menteri Keuangan Nomor 216/PMK.01/2018 mengatur tentang …", "Manajemen Pengembangan Sumber Daya Manusia di Lingkungan Kementerian Keuangan",
     ["Manajemen Karier", "Kode Etik dan Kode Perilaku", "Pelaksanaan Cuti", "Organisasi dan Tata Kerja"],
     "PMK 216/PMK.01/2018 berlaku sejak 31 Desember 2018 dan merujuk PP 11/2017 tentang manajemen PNS.", "216/2018 → pengembangan SDM.", 2),
    ("Keputusan Menteri Keuangan Nomor 942/KMK.01/2019 mengatur tentang …", "Pengelolaan Keamanan Informasi di Lingkungan Kementerian Keuangan",
     ["Pengembangan Sistem Informasi", "Manajemen Risiko", "Tata Kelola Data", "Program Budaya"],
     "KMK 942/KMK.01/2019 menjadi dasar keamanan informasi, termasuk pembentukan KEMENKEU-CSIRT dan ketentuan akun/kata sandi.", "942/2019 → keamanan informasi.", 3),
    ("Cuti tahunan PNS diberikan paling lama … hari kerja dalam satu tahun.", "12 (dua belas)", ["10 (sepuluh)", "14 (empat belas)", "15 (lima belas)", "20 (dua puluh)"],
     "Cuti tahunan PNS adalah 12 hari kerja (menurut PP 11/2017; angka ini dari pengetahuan umum, cocokkan dengan buku). Ketentuan pelaksanaan di Kemenkeu: SE-15/MK.1/2018.", "Cuti tahunan 12 hari kerja; cuti besar paling lama 3 bulan.", 1),
    ("Cuti besar PNS diberikan paling lama …", "3 (tiga) bulan", ["1 (satu) bulan", "2 (dua) bulan", "6 (enam) bulan", "12 (dua belas) bulan"],
     "Cuti besar paling lama 3 bulan (ringkasan SE-15/MK.1/2018 dan PP 11/2017). Syarat masa kerja: cocokkan dengan buku.", "Besar = 3 bulan.", 2),
]
BANK["struktur"] += [
    ("Peraturan Presiden Nomor 158 Tahun 2024 mengatur tentang …", "Kementerian Keuangan",
     ["Organisasi Kementerian Negara", "Badan Kebijakan Fiskal", "Penataan Organisasi dan Tata Kerja Kemenkeu", "Kementerian Negara"],
     "Perpres 158/2024 mengatur susunan organisasi Kemenkeu. Perincian ada pada PMK 124/2024.", "Perpres 158/2024 = Kemenkeu; Perpres 140/2024 = organisasi semua kementerian.", 2),
    ("Peraturan Presiden Nomor 140 Tahun 2024 mengatur tentang …", "Organisasi Kementerian Negara",
     ["Kementerian Keuangan", "Kementerian Negara", "Aparatur Sipil Negara", "Keuangan Negara"],
     "Perpres 140/2024 (ditetapkan 21 Oktober 2024) mengatur organisasi kementerian negara.", "Bukan PP: Perpres.", 3),
    ("Perincian dari Perpres 158/2024 mengenai organisasi dan tata kerja Kementerian Keuangan terdapat pada …", "PMK Nomor 124 Tahun 2024",
     ["PMK Nomor 190/PMK.01/2018", "PMK Nomor 224/PMK.01/2020", "KMK Nomor 429/KMK.01/2022", "UU Nomor 39 Tahun 2008"],
     "PMK 124/2024 mengatur penataan organisasi dan tata kerja Kemenkeu sebagai perincian Perpres 158/2024.", "Perpres 158 → dirinci PMK 124.", 2),
    ("Undang-Undang Nomor 39 Tahun 2008 mengatur tentang …", "Kementerian Negara", ["Aparatur Sipil Negara", "Keuangan Negara", "Pengembangan dan Penguatan Sektor Keuangan", "Perbendaharaan Negara"],
     "UU 39/2008 adalah dasar pengaturan kementerian negara (berdasarkan pengetahuan umum, cocokkan dengan buku).", "39/2008 → kementerian negara.", 1),
    ("Undang-Undang Nomor 4 Tahun 2023 mengatur tentang …", "Pengembangan dan Penguatan Sektor Keuangan", ["Aparatur Sipil Negara", "Kementerian Negara", "Keuangan Negara", "Perbendaharaan Negara"],
     "UU 4/2023 dikenal sebagai UU P2SK.", "4/2023 = P2SK; 20/2023 = ASN.", 2),
]


def _daftar(bab, data):
    def gen(lv, rng):
        pool = [(i, d) for i, d in enumerate(data) if d[-1] == lv]
        if not pool:
            raise KeyError(f"tidak ada soal {bab} tingkat {lv}")
        i, d = rng.choice(pool)
        stem, jawab, dis, exp, trick, _ = d
        return mk(bab, lv, stem, jawab, dis, exp, trick, rng, id=f"{bab}-{i}")
    gen.__name__ = f"tskkwk_{bab}"
    GENS.setdefault(bab, []).append((gen, tuple(sorted({d[-1] for d in data}))))


for _b, _d in BANK.items():
    _daftar(_b, _d)
