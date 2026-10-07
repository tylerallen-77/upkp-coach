"""Ringkasan materi per bab. Ditulis ulang dengan kata sendiri dari pokok bahasan buku (hlm. 1-82).
Bab TSKKWK dan Psikologi: halaman buku belum tersedia, isi bersifat umum dan harus dicocokkan dengan buku.
"""

MATERI = {}

MATERI["padanan"] = """
### Tiga jenis soal
**Sinonim** (persamaan kata), **antonim** (lawan kata), dan **analogi** (hubungan antar-pasangan kata). Intinya mengukur perbendaharaan kata.

### Cara cepat
- **Ganti dengan kata yang paling umum:** jika kata pilihan tidak dikenal, masukkan ke kalimat sehari-hari dan lihat mana yang pas.
- **Antonim punya jebakan:** salah satu opsi sering sinonim kata soal. Sebut lawan kata dulu di kepala, baru cocokkan.
- **Analogi:** ubah pasangan pertama jadi satu kalimat (“A adalah alat untuk B”), lalu uji ke tiap opsi. Hubungan yang sering muncul: profesi–tempat, alat–fungsi, sebab–akibat, bagian–keseluruhan, bahan–hasil, tingkatan.
- **Pecah kata serapan:** re- (kembali), ek-/ekstra- (luar), in- (dalam/tidak), hetero- (berbeda), homo- (sama), kontra- (melawan).
- Tambah kosakata tiap hari dengan membaca KBBI daring.

### Contoh
*Relatif* bersinonim dengan *nisbi*. *Pindai* bermakna melihat dengan cermat dan lama, jadi sinonimnya *mencermati*.
"""

MATERI["kelompok"] = """
### Cara kerja
Dari lima kata, **empat memiliki satu ciri yang sama**, satu tidak. Cari kata yang tidak sekelompok.

### Cara cepat
1. Perhatikan seluruh kata. Jika ada kata yang tidak dikenal, lewati ke yang lain; sering kata itu adalah jawabannya.
2. **Awalan atau akhiran yang sama** bisa menjadi petunjuk kelompok (dan kata tanpa awalan itu yang berbeda).
3. Rangkai jadi kalimat: “… adalah ___ (kategori)”. Kata yang tidak cocok adalah jawabannya.
4. Perluas pengetahuan umum: lembaga negara, tokoh, geografi, sains dasar, unit Kemenkeu.

### Jebakan umum
Kategori yang terlalu luas (misal “makhluk hidup”) membuat semua kata cocok. Cari kategori **yang paling spesifik** yang masih memuat empat kata.
"""

MATERI["silogisme"] = """
### Proposisi kategoris
Terdiri dari **quantifier** (semua/sebagian/tidak ada) + subjek + kopula (adalah/bukan) + predikat.
- Universal: *semua, setiap*. Partikular: *sebagian, beberapa, ada*.
- Positif: *adalah*. Negatif: *bukan, tidak*.

### Penarikan kesimpulan langsung
- **Konversi:** “Semua S adalah P” → “Sebagian P adalah S”. “Sebagian S adalah P” → “Sebagian P adalah S”.
- **Obversi:** ubah kualitas dan negasikan predikat. “Semua S adalah P” ≡ “Tak satu pun S yang bukan P”.

### Penarikan kesimpulan tak langsung (dua premis)
Coret **term tengah**. Aturan quantifier: semua+semua = semua/sebagian; sebagian+semua = sebagian; **sebagian+sebagian = tidak dapat disimpulkan**.
Aturan kopula: positif+positif = positif; positif+negatif = negatif; negatif+positif = negatif; **negatif+negatif = tidak dapat disimpulkan**.

### Proposisi kondisional
- Implikasi P → Q ≡ **kontraposisi** ¬Q → ¬P ≡ ¬P ∨ Q.
- **Modus ponens:** P → Q, P ⟹ Q. **Modus tollens:** P → Q, ¬Q ⟹ ¬P. **Silogisme hipotetis:** P → Q, Q → R ⟹ P → R (di buku tertulis P → Q; yang benar P → R).
- **Jebakan:** Q benar tidak berarti P benar (afirmasi konsekuen), dan P salah tidak berarti Q salah.
- Negasi implikasi: ¬(P → Q) ≡ P ∧ ¬Q.

### Cara cepat
Gambar lingkaran (Venn): “semua A adalah B” = lingkaran A di dalam B. Jika ada “sebagian”, kesimpulan hanya “sebagian” atau “tidak dapat disimpulkan”.
"""

MATERI["analisis"] = """
### Struktur soal
**Pengantar** (situasi) → **pembatas** (aturan yang harus dipenuhi) → **soal** (pertanyaan yang mengikuti aturan).

### Tiga jenis
1. **Urutan:** kualitas (pakai tanda >, <, =) atau kuantitas (hitung nilainya dulu, urutkan).
2. **Kombinatoris:** *penjadwalan* (buat tabel hari/jam, tempatkan variabel), *posisi* (gambar skema: berjajar, berhadapan, melingkar).
3. **Implikasi:** aturan “jika … maka …”. Coret dulu jawaban yang melanggar aturan.

### Cara cepat
- Tulis semua informasi sebagai satu rantai atau tabel; jangan mengandalkan ingatan.
- Mulai dari informasi yang paling pasti (di ujung, “tepat di sebelah”).
- Jawaban yang “mungkin” berbeda dari yang “pasti”: baca kata tanyanya (pasti benar, mungkin, KECUALI).
- Pada soal implikasi, uji tiap opsi terhadap tiap aturan lalu coret yang melanggar.
"""

MATERI["operasi"] = """
### Bilangan
Bulat, cacah, asli, pecahan, rasional (bisa ditulis a/b), irasional (π, √2: desimal tak berhenti dan tak berpola), real, imajiner, kompleks.

### Eksponen
aᵐ·aⁿ = aᵐ⁺ⁿ; aᵐ÷aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; (ab)ⁿ = aⁿbⁿ; a⁰ = 1; a⁻ⁿ = 1/aⁿ; ⁿ√(aᵐ) = a^(m/n).

### Bentuk akar
a√c + b√c = (a+b)√c; √a·√b = √(ab); √a·√a = a. Sederhanakan dengan faktor kuadrat sempurna (√72 = 6√2).

### KPK dan FPB
- KPK: faktor prima berbeda dengan **pangkat tertinggi**. FPB: faktor prima sama dengan **pangkat terkecil**.
- a × b = KPK × FPB.
- “Berulang bersamaan” → KPK. “Dibagi sama rata dan paling banyak” → FPB.

### Habis dibagi
2: satuan genap. 3: jumlah digit habis dibagi 3. 4: dua digit terakhir. 5: satuan 0 atau 5. 6: genap dan habis dibagi 3. 8: tiga digit terakhir. 9: jumlah digit habis dibagi 9. 10: satuan 0.
7: kurangi 2× satuan dari bilangan di depannya, ulangi. 11: selisih jumlah digit posisi ganjil dan genap.

### Cara cepat
Ubah pecahan, persen, desimal ke satu bentuk sebelum membandingkan. Hafal: 1/8 = 0,125; 1/6 ≈ 0,167; 3/8 = 0,375; 5/8 = 0,625.
"""

MATERI["persamaan"] = """
### Persamaan kuadrat ax² + bx + c = 0
- Akar: faktorisasi, melengkapkan kuadrat, atau rumus x = (−b ± √D)/2a dengan **D = b² − 4ac**.
- D > 0: dua akar real berbeda. D = 0: akar kembar. D < 0: tidak real.
- Jumlah akar x₁ + x₂ = −b/a; hasil kali x₁·x₂ = c/a; x₁² + x₂² = (x₁+x₂)² − 2x₁x₂.
- Persamaan baru dari akar x₁, x₂: x² − (jumlah)x + (hasil kali) = 0.
- a > 0 memiliki nilai minimum; a < 0 memiliki nilai maksimum. Titik ekstrem: (−b/2a, −D/4a).

### Pertidaksamaan
- Sifat: tambah/kurang kedua ruas tidak mengubah tanda. Kali/bagi bilangan **positif** tidak mengubah tanda; kali/bagi bilangan **negatif membalik** tanda.
- Kuadrat: cari akar x₁ < x₂. Tanda “>” → x < x₁ atau x > x₂ (di luar). Tanda “<” → x₁ < x < x₂ (di antara).

### SPLDV dan SPLTV
Eliminasi (samakan koefisien lalu kurangkan), substitusi, atau keduanya. Pada tiga variabel, cari **dua persamaan yang bedanya hanya satu variabel**.
"""

MATERI["geometri"] = """
### Sudut dan garis
Berpelurus = 180°; berpenyiku = 90°; bertolak belakang sama besar; pada dua garis sejajar yang dipotong: sehadap sama, dalam berseberangan sama, dalam sepihak berjumlah 180°.

### Bangun datar
Segitiga L = ½at; persegi L = s²; persegi panjang L = pl, K = 2(p+l); jajar genjang L = at; belah ketupat L = ½d₁d₂; trapesium L = ½(a+b)t; lingkaran K = 2πr, L = πr² (π = 22/7 jika r kelipatan 7). Pythagoras: c² = a² + b².

### Bangun ruang
Kubus V = s³, L = 6s²; balok V = plt, L = 2(pl+pt+lt); tabung V = πr²t; kerucut V = ⅓πr²t; bola V = 4/3 πr³, L = 4πr². Diagonal ruang balok = √(p²+l²+t²).

### Cara cepat
- Tripel Pythagoras: 3-4-5, 5-12-13, 8-15-17, 7-24-25 dan kelipatannya.
- Perubahan dimensi: kalikan faktor tiap dimensi (naik 10%, turun 15% → 1,10 × 0,85 = 0,935 → turun 6,5%).
- 1 liter = 1000 cm³. Samakan satuan sebelum menghitung.
"""

MATERI["aritsos"] = """
### Aritmatika sosial
- Untung = HJ − HB; %U = U/HB × 100%. Rugi = HB − HJ.
- **Diskon bertahap:** kalikan faktor sisanya. Diskon 30% lalu 40% → 0,7 × 0,6 = 0,42 → diskon gabungan 58%, bukan 70%.
- **Bruto = tara + neto.** Yang dijual dihitung dari neto.
- **Bunga tunggal:** T = Mₒ + (p% × n × Mₒ), dengan n dalam tahun.

### Barisan dan deret aritmatika
Uₙ = a + (n−1)b; Sₙ = n/2 (a + Uₙ) = n/2 (2a + (n−1)b). Mencari kelipatan di antara dua bilangan: cari kelipatan pertama dan terakhir, hitung banyak suku, pakai Sₙ.

### Barisan dan deret geometri
Uₙ = a·rⁿ⁻¹; Sₙ = a(rⁿ−1)/(r−1) untuk r > 1; Sₙ = a(1−rⁿ)/(1−r) untuk r < 1; deret tak hingga S∞ = a/(1−r).

### Cara cepat
Pertumbuhan berlipat dua tiap hari: untuk “setengah penuh di hari n”, “seperempat penuh” adalah hari n − 1. Tidak perlu rumus deret.
"""

MATERI["sudut"] = """
### Sudut jarum jam
Jarum pendek bergerak 30° per jam dan 0,5° per menit. Jarum panjang 6° per menit.
**Sudut = |30h − 5,5m|**. Jika lebih dari 180°, pakai 360° − hasil.

### Sifat sudut
Berpelurus 180°, berpenyiku 90°. Garis sejajar dipotong garis lain: sudut sehadap, berseberangan, dan bertolak belakang sama besar; sudut dalam/luar sepihak berjumlah 180°.

### Himpunan
- Irisan A ∩ B: anggota keduanya. Gabungan A ∪ B: anggota salah satunya.
- **n(S) = n(A) + n(B) − n(A ∩ B) + n(di luar A dan B)**.

### Cara cepat
Gambar diagram Venn. Isi irisan lebih dulu, baru bagian “hanya A” dan “hanya B”. “Hanya A” = n(A) − n(A ∩ B).
"""

MATERI["banding"] = """
### Perbandingan senilai
Makin banyak, makin banyak: x₁/x₂ = y₁/y₂. **Skala** = jarak sebenarnya / jarak di peta (satuan cm).

### Perbandingan berbalik nilai
Ada unsur waktu dan subjek: x₁·y₁ = x₂·y₂. Contoh: pekerja lebih banyak → hari lebih sedikit.

### Kecepatan berbeda
1/a + 1/b + … = 1/(waktu bersama).

### Perbandingan campuran
produk A / (subjek A × waktu A) = produk B / (subjek B × waktu B).
Proyek yang terhenti: hitung sisa pekerjaan dalam **orang-hari**, bagi dengan sisa hari kerja yang tersedia.

### Cara cepat
Tentukan dulu senilai atau berbalik dengan satu pertanyaan: “jika yang satu naik, yang lain naik atau turun?”. Samakan satuan sebelum menghitung.
"""

MATERI["jarak"] = """
### Rumus dasar
s = v × t; v = s/t; t = s/v. Ubah menit ke jam (÷ 60) sebelum menghitung.

### Berpapasan
- Berangkat bersamaan: **t = S / (V₁ + V₂)**.
- Berangkat tidak bersamaan: t = (S − selisih jarak) / (V₁ + V₂), dengan selisih jarak = V₁ × selisih waktu.

### Menyusul
**t = selisih jarak / (V₂ − V₁)**, dihitung sejak yang kedua berangkat.

### Kecepatan rata-rata
= **jarak total ÷ waktu total**. Bukan rata-rata dari kecepatan tiap ruas. Pulang-pergi berjarak sama: 2ab/(a+b).

### Cara cepat
- Berpapasan: kecepatan dijumlah. Menyusul: kecepatan dikurangi.
- Waktu berhenti tidak dihitung untuk jarak.
- Zona waktu: ubah kedua waktu ke zona yang sama dulu.
- Kerja bersama: 1/a + 1/b + 1/c = 1/t. Pakai KPK sebagai total pekerjaan.
"""

MATERI["peluang"] = """
### Peluang
P(A) = n(A)/n(S). Komplemen: P(A′) = 1 − P(A). Frekuensi harapan: **Fh = n × P(A)**.
Dua dadu: n(S) = 36. Jumlah 6: 5 pasangan → 5/36.

### Permutasi (urutan penting)
P(n,k) = n!/(n−k)!. Unsur sama: n!/(n₁!n₂!…). **Siklik: (n−1)!**.

### Kombinasi (urutan tidak penting)
C(n,k) = n!/((n−k)! k!).

### Cara cepat
- “Tidak boleh berdampingan” = total − berdampingan. Berdampingan: anggap satu blok (2·(n−1)!).
- “Dua orang tidak mau bertemu” = total − (keduanya hadir).
- Bilangan ganjil dari digit tertentu: isi **satuan dulu** (harus ganjil), baru sisanya.
- Pilihan kelompok terpisah: kalikan kombinasi tiap kelompok.
"""

MATERI["statistika"] = """
### Data tunggal
Mean = jumlah/banyak data. Median = nilai tengah setelah diurutkan (ganjil: data ke-(n+1)/2; genap: rata-rata dua data tengah). Modus = data yang paling sering muncul.

### Rata-rata gabungan
(n₁x̄₁ + n₂x̄₂ + …) / (n₁ + n₂ + …). Selalu bekerja dengan **total**.

### Data berkelompok
- Mean = Σ(fᵢ·xᵢ) / Σfᵢ, xᵢ = nilai tengah kelas.
- Median = Tb + ((n/2 − fk)/f) × p. Tb = tepi bawah, fk = frekuensi kumulatif sebelum kelas median.
- Modus = Tb + (d₁/(d₁+d₂)) × p.

### Cara cepat
- Mengecilkan/menambah satu data: gunakan total (rata-rata × banyak data).
- Bilangan terbesar yang mungkin dengan rata-rata tertentu: buat bilangan lain sekecil mungkin (0, 1, 2, …).
- Batas rata-rata: ganti tiga bilangan lain dengan nilai minimum atau maksimum.
"""

MATERI["deret"] = """
### Pola deret angka
1. **Fibonacci:** tiap suku = jumlah dua suku sebelumnya.
2. **Larik:** dua (atau tiga) deret bergantian. Pisahkan suku ganjil dan genap.
3. **Tingkat:** selisihnya sendiri berpola (+2, +2, +3, …). Tulis selisih di bawah deret.
4. **Kombinasi:** campuran pola di atas. Hitung selisih bertingkat.
Pola lain: aritmatika, geometri, kuadrat, kubik, bilangan prima, segitiga, n(n+1), faktorial, tribonacci.

### Deret huruf
Ubah huruf jadi angka (A=1 … Z=26) lalu perlakukan sebagai deret angka. **Jangkar ingatan: E=5, J=10, O=15, T=20, Y=25.**
Beberapa deret huruf memakai kelompok yang dibalik (WXY ditulis YXW).

### Cara cepat
Cek berurutan: selisih tetap → selisih berpola → kali/bagi tetap → Fibonacci → larik. Angka naik pelan = selisih; melonjak = kali atau kuadrat; naik-turun = larik.
"""

MATERI["deretfig"] = """
### Jenis soal
**Deret figural:** temukan pola perubahan bentuk, jumlah elemen, simbol, putaran, atau gabungannya, lalu tentukan gambar berikutnya. **Beda figural:** satu gambar berbeda dari yang lain.

### Istilah penting
Arah mata angin (utara, timur laut, timur, tenggara, selatan, barat daya, barat, barat laut) dan arah putaran (searah/berlawanan arah jarum jam).

### Cara cepat
1. Baca instruksi. 2. Lacak **satu atribut per langkah** (arah, jumlah titik, warna). 3. Hitung elemen dengan membagi gambar menjadi kuadran. 4. Pada beda figural, jangan terkecoh putaran: putaran tidak mengubah bentuk, tetapi **cermin** mengubahnya.
"""

MATERI["analogifig"] = """
### Cara kerja
Dua gambar pertama punya hubungan tertentu. Terapkan hubungan yang sama pada gambar ketiga untuk mendapat gambar keempat.

### Jenis perubahan yang sering muncul
Putaran (90°, 180°), pembalikan warna, penambahan atau pengurangan sisi, pertukaran posisi luar-dalam, perpindahan elemen kecil, penggandaan lalu penghapusan sebagian, dan penggabungan dua gambar.

### Cara cepat
1. Bandingkan gambar 1 dan 2 **satu atribut demi satu** dan daftarkan perubahannya.
2. Terapkan daftar itu pada gambar 3.
3. Coret opsi yang gagal pada atribut pertama yang diperiksa. Biasanya dua atau tiga opsi gugur dengan sekali cek warna atau bentuk.
"""

# ---- TSKKWK: isi umum, bukan dari buku
MATERI["etika"] = """
> **Catatan:** halaman buku bab ini belum tersedia. Ringkasan ini dari sumber umum; cocokkan dengan buku.

### Nilai dasar ASN: BerAKHLAK
**Ber**orientasi pelayanan, **A**kuntabel, **K**ompeten, **H**armonis, **L**oyal, **A**daptif, **K**olaboratif.

### Hal yang sering diuji
- Dasar hukum: UU 20/2023 tentang ASN; kode etik dan kode perilaku menjabarkan nilai dasar.
- Gratifikasi: pemberian terkait jabatan → tolak dan laporkan.
- Netralitas, menjaga rahasia jabatan, tidak menyalahgunakan wewenang, tidak menyebarkan hoaks.
- Etika bermedia sosial dan berhubungan dengan pihak yang dilayani.

### Cara cepat
Pada soal kasus, pilih jawaban yang (1) mematuhi aturan, (2) menjaga kepentingan publik, (3) menyampaikan lewat jalur resmi, bukan yang paling nyaman atau paling cepat.
"""

MATERI["wawasan"] = """
> **Catatan:** halaman buku bab ini belum tersedia. Ringkasan ini dari pengetahuan umum; cocokkan dengan buku.

### Pokok bahasan
- **Pancasila:** 1 Ketuhanan Yang Maha Esa; 2 Kemanusiaan yang Adil dan Beradab; 3 Persatuan Indonesia; 4 Kerakyatan yang Dipimpin oleh Hikmat Kebijaksanaan dalam Permusyawaratan/Perwakilan; 5 Keadilan Sosial bagi Seluruh Rakyat Indonesia.
- **UUD 1945:** Pembukaan (alinea 4 memuat dasar negara), empat kali amandemen (1999–2002), Pasal 1 ayat (2) tentang kedaulatan rakyat.
- **Empat pilar:** Pancasila, UUD NRI 1945, NKRI, Bhinneka Tunggal Ika.
- Nasionalisme, bela negara, wawasan nusantara, ketahanan nasional, hak dan kewajiban warga negara, ancaman dan tantangan kebangsaan.

### Cara cepat
Hafal urutan sila dengan lambang (bintang, rantai, beringin, banteng, padi dan kapas). Kaitkan butir pengamalan dengan sila asalnya.
"""

MATERI["nilai"] = """
### IProSPeK
Nilai-Nilai Kementerian Keuangan: **I**ntegritas, **Pro**fesionalisme, **S**inergi, **Pe**layanan, **K**esempurnaan (KMK 312/KMK.01/2011). Kode etik dan kode perilaku: PMK 190/PMK.01/2018.

| Nilai | Makna ringkas | Kata kunci perilaku utama |
|---|---|---|
| Integritas | berpikir, berkata, berperilaku, bertindak baik dan benar; memegang teguh kode etik dan prinsip moral | jujur, tulus, dapat dipercaya, transparan, menjaga martabat |
| Profesionalisme | bekerja tuntas dan akurat atas dasar kompetensi terbaik dengan tanggung jawab dan komitmen tinggi | ahli, efisien dan efektif, cerdas, cepat, tuntas |
| Sinergi | membangun kerja sama internal yang produktif dan kemitraan harmonis dengan pemangku kepentingan | sangka baik, saling percaya, menghormati, terbuka |
| Pelayanan | melayani demi kepuasan pemangku kepentingan dengan sepenuh hati, transparan, cepat, akurat, aman | berorientasi kepuasan, ramah, adil |
| Kesempurnaan | senantiasa melakukan upaya perbaikan di segala bidang untuk menjadi dan memberikan yang terbaik | perbaikan berkelanjutan, inovasi |

> Sumber: laman resmi Kemenkeu dan DJPb. Cocokkan dengan buku bila ada perbedaan redaksi.

### Cara cepat
Kata kunci → nilai: tuntas/akurat → Profesionalisme; jujur/transparan → Integritas; kerja sama → Sinergi; kepuasan pemangku kepentingan → Pelayanan; perbaikan terus-menerus → Kesempurnaan.
"""

MATERI["kepegawaian"] = """
> **Catatan:** halaman buku bab ini belum tersedia. Ringkasan di bawah dari sumber umum dan resmi (diverifikasi Oktober 2026); peraturan bisa berubah.

### Dasar hukum
- **UU 20/2023 tentang ASN** (menggantikan UU 5/2014).
- **PP 94/2021 tentang Disiplin PNS** (menggantikan PP 53/2010). Memuat kewajiban, larangan, dan hukuman disiplin.
- PMK 123/2023 (tata cara pemeriksaan pelanggaran disiplin di lingkungan Kemenkeu).

### Hukuman disiplin (PP 94/2021)
- **Ringan:** teguran lisan, teguran tertulis, pernyataan tidak puas secara tertulis.
- **Sedang:** pemotongan tunjangan kinerja dengan jangka waktu tertentu.
- **Berat:** penurunan jabatan, pembebasan dari jabatan, pemberhentian dengan hormat tidak atas permintaan sendiri, pemberhentian tidak dengan hormat.

### Cara cepat
Hukuman makin berat jika melanggar larangan berat atau berulang. Jenis dan tingkat selalu berurutan: ringan → sedang → berat.
"""

MATERI["keuangan"] = """
> **Catatan:** halaman buku bab ini belum tersedia. Ringkasan dari sumber umum.

### Tiga paket UU keuangan negara
- **UU 17/2003** tentang Keuangan Negara.
- **UU 1/2004** tentang Perbendaharaan Negara.
- **UU 15/2004** tentang Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara.

### Pokok
- Keuangan negara: semua hak dan kewajiban negara yang dapat dinilai dengan uang, serta segala sesuatu yang dapat dijadikan milik negara.
- Presiden memegang kekuasaan pengelolaan keuangan negara, dikuasakan kepada **Menteri Keuangan** (pengelola fiskal dan wakil pemerintah dalam kepemilikan kekayaan negara yang dipisahkan) dan **menteri/pimpinan lembaga** (pengguna anggaran/barang).
- Tahun anggaran = Januari–Desember. RAPBN diajukan Agustus tahun sebelumnya.
- Pemeriksa eksternal: **BPK**. Pengawas internal: Inspektorat dan BPKP.

### Cara cepat
Urutan siklus APBN: perencanaan → penyusunan → pembahasan DPR → pelaksanaan → pengawasan → pertanggungjawaban (laporan keuangan diperiksa BPK).
"""

MATERI["struktur"] = """
> **Catatan:** halaman buku bab ini belum tersedia. Struktur organisasi bisa berubah; ini diverifikasi dari pemberitaan dan siaran resmi (Perpres 158/2024 dan PMK 124/2024). Cek aturan terbaru.

### Unit eselon I utama
Sekretariat Jenderal; Inspektorat Jenderal; **DJA** (Anggaran); **DJP** (Pajak); **DJBC** (Bea dan Cukai); **DJPb** (Perbendaharaan); **DJKN** (Kekayaan Negara); **DJPK** (Perimbangan Keuangan); **DJPPR** (Pengelolaan Pembiayaan dan Risiko); **BPPK** (Pendidikan dan Pelatihan Keuangan).

### Perubahan terbaru
- **Badan Kebijakan Fiskal (BKF) dihapus** dari susunan organisasi.
- Dibentuk **Direktorat Jenderal Strategi Ekonomi dan Fiskal**, **Direktorat Jenderal Stabilitas dan Pengembangan Sektor Keuangan**, dan **Badan Teknologi, Informasi, dan Intelijen Keuangan**.
- Juga ada Staf Ahli Menteri.

### Cara cepat
Hafal fungsi dengan kata kunci: pajak (DJP), bea dan cukai (DJBC), anggaran (DJA), kas dan perbendaharaan (DJPb), aset dan lelang (DJKN), transfer ke daerah (DJPK), utang dan SBN (DJPPR), diklat (BPPK).
"""

# ---- Psikologi: format perkiraan
MATERI["pemahaman"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan.

Subtes ini umumnya menguji kemampuan memahami teks atau instruksi lalu menerapkannya dengan tepat.
- Baca instruksi **sampai selesai** sebelum menjawab.
- Tandai syarat (DAN, ATAU, KECUALI, paling sedikit, paling banyak).
- Hitung hal numerik langkah demi langkah dan cek satuan.
- Untuk pernyataan logis, bedakan “pasti benar” dan “mungkin benar”.
"""

MATERI["numlogic"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan.

Number logic menguji penalaran angka: temukan aturan hubungan dari beberapa contoh, lalu terapkan pada contoh baru.
- Uji aturan sederhana dulu (jumlah, kali, selisih), baru yang lebih rumit (kuadrat, kombinasi).
- Aturan yang benar harus cocok dengan **semua** contoh, bukan satu.
- Pola yang sering muncul: a + b, a × b, a² ± b, 2a + b, a² − b².
"""

MATERI["blockpattern"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan.

Block pattern menguji persepsi ruang: menyusun, memutar, atau mencerminkan pola kotak.
- Lacak **satu pojok** berwarna untuk memastikan arah putaran.
- Putaran searah jarum jam 90°: baris pertama menjadi kolom terakhir.
- Cermin membalik kiri-kanan (atau atas-bawah) dan **tidak bisa** didapat dari putaran saja.
"""

MATERI["disc"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan. **Tidak ada jawaban benar atau salah.**

DISC mengelompokkan kecenderungan perilaku: **D**ominance, **I**nfluence, **S**teadiness, **C**onscientiousness. Pada soal pilihan paksa, Anda memilih kata yang paling dan paling tidak menggambarkan diri Anda.
- Jawab jujur dan **konsisten**; profil yang dibuat-buat mudah terlihat dari ketidakkonsistenan.
- Tidak ada profil “terbaik” untuk semua posisi.
- Latihan di aplikasi ini hanya untuk membiasakan format, bukan alat ukur psikologi yang tervalidasi.
"""

MATERI["karakter"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan. **Tidak ada jawaban benar atau salah.**

Subtes karakteristik pribadi biasanya berupa pernyataan yang dinilai sesuai/tidak sesuai dengan diri Anda.
- Butir yang maknanya berkebalikan dipakai untuk mengecek konsistensi.
- Jangan menebak “jawaban ideal”: jawaban yang terlalu sempurna di semua butir dapat tampak tidak jujur.
- Jawab berdasarkan perilaku nyata, bukan niat.
"""

MATERI["skala"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan. **Tidak ada jawaban benar atau salah.**

Skala penilaian diri meminta Anda menilai kemampuan atau perilaku diri sendiri pada skala (misal 1–5).
- Pakai seluruh rentang skala sesuai kenyataan.
- Berikan contoh nyata di kepala sebelum memilih angka tinggi.
- Waspadai kecenderungan memilih jawaban tengah atau ekstrem di semua butir.
"""

MATERI["pauli"] = """
> **Catatan:** halaman buku bab ini belum tersedia; format di bawah perkiraan.

Tes Pauli menguji kecepatan, ketelitian, ketahanan, dan konsistensi kerja. Biasanya Anda menjumlahkan dua angka berurutan dalam kolom dan menulis **angka satuan** hasilnya, terus-menerus dalam waktu tertentu.
- Contoh: 7 dan 8 → 15 → tulis **5**.
- Jaga irama yang stabil; kecepatan yang naik-turun menurunkan nilai konsistensi.
- Jangan berhenti menghapus kesalahan, lanjutkan saja.
"""


MATERI["etika"] += """

### Dasar hukum (diverifikasi Oktober 2026)
- **PP 42/2004** tentang Pembinaan Jiwa Korps dan Kode Etik PNS.
- **PMK 190/PMK.01/2018** tentang Kode Etik dan Kode Perilaku PNS di Lingkungan Kementerian Keuangan.
- **SE-12/MK.1/2018** tentang Penerapan Nilai-Nilai Kementerian Keuangan dan Kode Etik sebagai *Early Warning System*.
"""

MATERI["nilai"] += """

### Program Budaya (KMK 127/KMK.01/2013, 3 April 2013)
| Program | Maksud |
|---|---|
| Satu Informasi Setiap Hari | mencari informasi positif dan membaginya (sharing) dengan pegawai lain |
| Dua Menit Sebelum Jadual | hadir di tempat rapat dua menit sebelum rapat dimulai, melatih kedisiplinan |
| Tiga Salam Setiap Hari | memberi salam sesuai waktu: selamat pagi, siang, dan sore |
| Rencanakan, Kerjakan, Monitor dan Tindaklanjuti | etos kerja dan prinsip manajemen (PDCA) |
| Ringkas, Rapi, Resik, Rawat, Rajin (5R) | penataan ruang kantor dan dokumen kerja yang nyaman |

**Cara cepat:** angka 1-2-3 untuk tiga program pertama (Satu informasi, Dua menit, Tiga salam), lalu PDCA dan 5R.

### Dokumen terkait
- **SE-12/MK.1/2018**: penerapan nilai-nilai dan kode etik sebagai *early warning system*.
- **KMK 429/KMK.01/2022**: Penguatan Budaya di Lingkungan Kementerian Keuangan.
"""

MATERI["kepegawaian"] += """

### Peraturan kepegawaian pada daftar Anda (diverifikasi Oktober 2026)
| Peraturan | Isi |
|---|---|
| PP 11/2017 dan PP 17/2020 | Manajemen PNS dan perubahannya |
| Peraturan BKN 24/2017 (diubah Peraturan BKN 7/2021) | Tata cara pemberian cuti PNS |
| SE-15/MK.1/2018 | Pelaksanaan cuti PNS di lingkungan Kemenkeu |
| SE-4/MK.1/2019 | Mekanisme cuti secara online di lingkungan Kemenkeu |
| PMK 224/PMK.01/2020 | Manajemen karier di lingkungan Kemenkeu (berlaku 30 Maret 2021) |
| PMK 216/PMK.01/2018 | Manajemen pengembangan SDM di lingkungan Kemenkeu |
| KMK 942/KMK.01/2019 | Pengelolaan keamanan informasi di lingkungan Kemenkeu |

**Perlu dicocokkan dengan buku:** PP 94/2021 (disiplin) tidak ada di daftar Anda, padahal PP 53/2010 yang digantikannya ada. Lihat menu **Regulasi**.

**Cuti (pengetahuan umum, cocokkan dengan buku):** cuti tahunan 12 hari kerja; cuti besar paling lama 3 bulan.
"""

MATERI["struktur"] += """

### Dasar hukum (diverifikasi Oktober 2026)
- **Perpres 158/2024** tentang Kementerian Keuangan, dirinci dengan **PMK 124/2024** (penataan organisasi dan tata kerja).
- **Perpres 140/2024** tentang Organisasi Kementerian Negara (di daftar Anda tertulis “PP 140/2024”, yang tepat Perpres).
- **UU 39/2008** tentang Kementerian Negara (pengetahuan umum).
- **UU 4/2023** tentang Pengembangan dan Penguatan Sektor Keuangan (P2SK).
"""
