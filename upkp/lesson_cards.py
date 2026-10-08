"""Structured teaching cards used by the lesson UI.

These cards are intentionally concise: they give learners a wide-angle map before
they enter the full explanation. They do not replace the lesson text.
"""
CARDS = {
 "silogisme":[
  {"kind":"concept","title":"Quantifier","body":"Semua / sebagian / tidak ada menentukan seberapa kuat kesimpulan boleh dibuat."},
  {"kind":"formula","title":"Implikasi","formula":"P → Q  ≡  ¬Q → ¬P","body":"Kontraposisi selalu ekuivalen; affirming the consequent tidak valid."},
  {"kind":"trap","title":"Jebakan klasik","body":"Q benar tidak membuktikan P benar."},
 ],
 "analisis":[
  {"kind":"method","title":"Constraint map","body":"Variabel → aturan absolut → blok → kemungkinan valid."},
  {"kind":"trap","title":"Pasti vs mungkin","body":"Pasti harus benar di semua konfigurasi; mungkin cukup benar di satu konfigurasi."},
 ],
 "operasi":[
  {"kind":"formula","title":"Pangkat","formula":"aᵐ·aⁿ = aᵐ⁺ⁿ","body":"Basis sama → pangkat dijumlah saat dikali."},
  {"kind":"formula","title":"Pangkat negatif","formula":"a⁻ⁿ = 1/aⁿ","body":"Ubah ke pecahan sebelum operasi lanjut."},
  {"kind":"shortcut","title":"25 × n","formula":"25n = 100n/4","body":"Gunakan pecahan benchmark untuk hitung mental."},
 ],
 "persamaan":[
  {"kind":"formula","title":"Diskriminan","formula":"D = b² − 4ac","body":"D menentukan jumlah akar real."},
  {"kind":"formula","title":"Vieta","formula":"x₁+x₂ = −b/a · x₁x₂ = c/a","body":"Sering lebih cepat daripada mencari akar satu per satu."},
  {"kind":"rule","title":"Pertidaksamaan","body":"Kali/bagi bilangan negatif → tanda pertidaksamaan dibalik."},
 ],
 "geometri":[
  {"kind":"formula","title":"Pythagoras","formula":"c² = a² + b²","body":"Cari tripel 3-4-5, 5-12-13, 8-15-17."},
  {"kind":"formula","title":"Lingkaran","formula":"K = 2πr · L = πr²","body":"Pastikan yang ditanya keliling atau luas."},
  {"kind":"formula","title":"Skala luas","formula":"faktor luas = k²","body":"Perubahan dimensi tidak dijumlah secara langsung."},
 ],
 "aritsos":[
  {"kind":"formula","title":"Untung","formula":"%U = (HJ−HB)/HB × 100%","body":"Denominator umum adalah harga beli."},
  {"kind":"formula","title":"Diskon bertahap","formula":"harga akhir = harga awal × ∏ faktor sisa","body":"20% lalu 10% = 0,8×0,9 = 0,72."},
  {"kind":"formula","title":"Deret aritmatika","formula":"Uₙ=a+(n−1)b · Sₙ=n/2(a+Uₙ)","body":"Bedakan suku ke-n dan jumlah n suku."},
 ],
 "sudut":[
  {"kind":"formula","title":"Sudut jam","formula":"|30h − 5,5m|","body":"Jika >180°, ambil 360°−hasil."},
  {"kind":"formula","title":"Gabungan himpunan","formula":"n(A∪B)=n(A)+n(B)−n(A∩B)","body":"Irisan dikurangkan karena terhitung dua kali."},
 ],
 "banding":[
  {"kind":"formula","title":"Berbalik nilai","formula":"x₁y₁ = x₂y₂","body":"Cocok untuk pekerja-waktu dan model sejenis."},
  {"kind":"formula","title":"Kerja bersama","formula":"1/a + 1/b = 1/t","body":"Yang dijumlah adalah rate pekerjaan."},
  {"kind":"formula","title":"Reverse percentage","formula":"awal = akhir / faktor perubahan","body":"Naik 25% → bagi 1,25 untuk kembali ke nilai awal."},
 ],
 "jarak":[
  {"kind":"formula","title":"Dasar","formula":"s = v × t","body":"Samakan satuan sebelum substitusi."},
  {"kind":"formula","title":"Berpapasan","formula":"t = S/(v₁+v₂)","body":"Relative speed dijumlah."},
  {"kind":"formula","title":"Menyusul","formula":"t = selisih jarak/(v₂−v₁)","body":"Relative speed dikurang."},
 ],
 "peluang":[
  {"kind":"formula","title":"Peluang","formula":"P(A)=n(A)/n(S)","body":"Ruang sampel harus benar dulu."},
  {"kind":"formula","title":"Kombinasi","formula":"C(n,k)=n!/[k!(n−k)!]","body":"Gunakan saat urutan tidak penting."},
  {"kind":"formula","title":"Permutasi","formula":"P(n,k)=n!/(n−k)!","body":"Gunakan saat urutan penting."},
 ],
 "statistika":[
  {"kind":"formula","title":"Mean","formula":"x̄ = Σx/n","body":"Sering lebih cepat berpikir lewat total = mean×n."},
  {"kind":"formula","title":"Weighted mean","formula":"x̄ = Σ(wx)/Σw","body":"Bobot masuk numerator dan denominator."},
  {"kind":"rule","title":"Median","body":"Urutkan data dulu; n genap → rata-rata dua posisi tengah."},
 ],
 "deret":[
  {"kind":"method","title":"Urutan diagnosis","body":"Selisih → selisih kedua → rasio → alternating → rekursif."},
  {"kind":"trap","title":"Timebox","body":"Jika pola belum terbaca setelah ±20 detik, parkir lalu kembali."},
 ],
 "deretfig":[
  {"kind":"method","title":"Lacak atribut","body":"Jumlah · posisi · orientasi · fill · ukuran · relasi."},
  {"kind":"trap","title":"Rotasi ≠ refleksi","body":"Rotasi mempertahankan handedness; cermin membaliknya."},
 ],
 "analogifig":[
  {"kind":"method","title":"Operator A→B","body":"Definisikan transformasi sebelum menerapkannya ke C."},
  {"kind":"shortcut","title":"Eliminasi cepat","body":"Cek atribut paling diskriminatif lebih dulu."},
 ],
 "padanan":[
  {"kind":"method","title":"Sinonim/antonim","body":"Definisikan kata dengan bahasa sendiri sebelum melihat opsi."},
  {"kind":"method","title":"Analogi","body":"Ubah pasangan pertama menjadi satu kalimat relasi."},
  {"kind":"trap","title":"Terkait ≠ sama makna","body":"Kata yang sering muncul bersama belum tentu sinonim."},
 ],
 "kelompok":[
  {"kind":"method","title":"Cari kategori tersempit","body":"Kategori harus memuat empat item dan mengecualikan satu."},
  {"kind":"trap","title":"Kategori terlalu luas","body":"Jika semua lima masih masuk, kategorinya belum cukup spesifik."},
 ],
 "etika":[
  {"kind":"concept","title":"Prinsip keputusan","body":"Aturan + kepentingan publik + transparansi + jalur resmi."},
  {"kind":"trap","title":"Konflik kepentingan","body":"Niat baik tidak menghapus conflict of interest."},
  {"kind":"method","title":"Soal kasus","body":"Identifikasi aktor, kepentingan, kewenangan, lalu tindakan yang paling defensible."},
 ],
 "wawasan":[
  {"kind":"concept","title":"Empat jangkar","body":"Pancasila · UUD NRI 1945 · NKRI · Bhinneka Tunggal Ika."},
  {"kind":"method","title":"Belajar dua arah","body":"Konsep → contoh perilaku dan kasus → prinsip."},
 ],
 "nilai":[
  {"kind":"concept","title":"IProSPeK","body":"Integritas · Profesionalisme · Sinergi · Pelayanan · Kesempurnaan."},
  {"kind":"method","title":"Cari perilaku dominan","body":"Semua opsi bisa positif; pilih nilai yang paling langsung menjelaskan tindakan."},
 ],
 "kepegawaian":[
  {"kind":"concept","title":"Peta regulasi","body":"UU 20/2023 · PP 94/2021 · PMK 123/2023 · aturan cuti BKN."},
  {"kind":"method","title":"Tiga lapis soal","body":"Pelanggaran → proses pemeriksaan → konsekuensi/kewenangan."},
 ],
 "keuangan":[
  {"kind":"concept","title":"Tiga pilar","body":"UU 17/2003 · UU 1/2004 · UU 15/2004."},
  {"kind":"method","title":"Siklus","body":"Perencanaan → penganggaran → pelaksanaan → pelaporan → pemeriksaan → tindak lanjut."},
  {"kind":"trap","title":"Jangan campur fungsi","body":"Pengelolaan, pengawasan internal, dan pemeriksaan eksternal berbeda."},
 ],
 "struktur":[
  {"kind":"concept","title":"Baseline current","body":"PMK 124/2024 sebagaimana diubah PMK 117/2025."},
  {"kind":"method","title":"Belajar per fungsi","body":"Nama unit → domain tugas → contoh isu → unit yang mirip."},
 ],
}

def cards(code):
    return CARDS.get(code, [])
