"""Regulation-grounded TSKKWK deep dives.

These are teaching notes built from the currently validated regulation anchors.
They summarize study structure; they are not substitutes for the full legal text.
"""
DEEP_DIVES={
"etika":"""
## Deep dive regulasi
### UU 20/2023 tentang ASN
Fokus belajar: peran ASN, nilai dasar, kode etik/kode perilaku, profesionalitas, netralitas, sistem merit, dan orientasi pelayanan publik. UU ini menggantikan UU 5/2014.

### PMK 190/PMK.01/2018
Fokus belajar: kode etik dan kode perilaku PNS di lingkungan Kementerian Keuangan, mekanisme penjagaan martabat pegawai, dan konteks penanganan dugaan pelanggaran kode etik.

### Cara menghubungkan
Untuk soal kasus, mulai dari kewajiban/nilai ASN, lalu cek konteks khusus Kemenkeu. Hindari menghafal pasal tanpa memahami perilaku yang hendak dicegah atau diwajibkan.
""",
"kepegawaian":"""
## Deep dive regulasi
### UU 20/2023 — payung ASN
Kuasai struktur besar manajemen ASN, jenis pegawai ASN, jabatan, sistem merit, pengembangan talenta/kompetensi, serta nilai dasar dan perilaku ASN.

### PP 94/2021 — disiplin PNS
PP ini mengatur **kewajiban, larangan, hukuman disiplin, kewenangan pejabat yang menghukum, dan upaya administratif**. Belajar dengan matriks: *apa kewajiban/larangan → fakta pelanggaran → level hukuman → pejabat berwenang → hak pembelaan*.

### PMK 123/2023 — proses internal Kemenkeu
Gunakan untuk memahami **tata cara pemeriksaan pelanggaran disiplin dan penjatuhan hukuman** di lingkungan Kemenkeu. Bedakan aturan substansi disiplin dari prosedur pemeriksaannya.

### Cuti PNS
Anchor pada Peraturan BKN 24/2017 jo. Peraturan BKN 7/2021. Belajar per jenis cuti: tujuan, syarat umum, durasi/otoritas bila relevan, dan dokumen pendukung.

### Jembatan berpikir
**ATURAN → FAKTA → PROSES → PEJABAT → AKIBAT → UPAYA**.
""",
"keuangan":"""
## Deep dive regulasi
### UU 17/2003 — kerangka Keuangan Negara
Kuasai ruang lingkup keuangan negara, asas pengelolaan, kekuasaan pengelolaan, penyusunan/penetapan APBN dan APBD, pelaksanaan, serta pertanggungjawaban.

### UU 1/2004 — Perbendaharaan Negara
Materi pokok resminya mencakup pejabat perbendaharaan, pelaksanaan pendapatan/belanja, pengelolaan uang, piutang/utang, investasi, BMN/D, penatausahaan dan pertanggungjawaban, pengendalian intern, kerugian negara/daerah, serta BLU.

### UU 15/2004 — pemeriksaan
Fokuskan pada posisi BPK dan proses pemeriksaan pengelolaan serta tanggung jawab keuangan negara. Jangan campur fungsi pemeriksaan eksternal dengan pengendalian/pengawasan intern.

### Jembatan 17–1–15
**17 = KELOLA KERANGKA · 1 = BENDAHARA/LAKSANA · 15 = PERIKSA**.
""",
"struktur":"""
## Deep dive regulasi
### PMK 124/2024
Ini baseline Organisasi dan Tata Kerja Kementerian Keuangan yang mencabut PMK 118/2021 beserta perubahan-perubahannya.

### PMK 117/2025
Merupakan perubahan terbaru atas PMK 124/2024. Karena struktur organisasi dinamis, nama unit dan pembagian fungsi harus selalu dibaca sebagai satu paket: PMK 124/2024 **sebagaimana diubah** PMK 117/2025.

### Cara belajar yang lebih tahan perubahan
Jangan hafal daftar unit sebagai lagu kosong. Bentuk peta:
1. **Dukungan & governance**
2. **Pengawasan internal**
3. **Strategi/fiskal & anggaran**
4. **Penerimaan**
5. **Perbendaharaan & aset**
6. **Transfer/perimbangan**
7. **Pembiayaan & risiko**
8. **Sektor keuangan**
9. **Teknologi/data**
10. **Pembelajaran**

Jika soal memakai nama unit lama, cek fungsi yang dimaksud lalu bandingkan dengan nomenklatur current.
""",
"nilai":"""
## Deep dive perilaku IProSPeK
Jangan hafal hanya nama nilai. Bentuk pasangan **nilai → perilaku pembeda**:
- **Integritas**: benar, jujur, dapat dipercaya, menjaga martabat.
- **Profesionalisme**: kompeten, akurat, tuntas, bertanggung jawab.
- **Sinergi**: kolaborasi dan solusi bersama.
- **Pelayanan**: kebutuhan stakeholder, cepat, aman, akurat, proaktif.
- **Kesempurnaan**: continuous improvement, kreativitas, inovasi, kualitas lebih baik.

Pada soal kasus, cari *kata kerja dominan*; satu kasus bisa memuat beberapa nilai, tetapi biasanya ada satu nilai paling sentral.
""",
"wawasan":"""
## Deep dive kerangka kebangsaan
Materi ini lebih konseptual daripada satu PER spesifik. Gunakan empat jangkar: **Pancasila, UUD NRI 1945, NKRI, Bhinneka Tunggal Ika**.

Untuk setiap jangkar, belajar tiga lapis:
1. prinsip/definisi,
2. implikasi bagi warga negara/ASN,
3. penerapan pada kasus pelayanan publik, keberagaman, persatuan, hak-kewajiban, atau bela negara.

Jangan mengandalkan mnemonic tanpa bisa menjelaskan konteks penerapannya.
""",
}

def get(code):
    return DEEP_DIVES.get(code,"")
