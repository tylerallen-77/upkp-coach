"""Study tools for UPKP Coach: reading lenses, formula handbook, and memory bridges.

Memory bridges are mnemonic aids created by UPKP Coach. They are never represented
as official wording from regulations.
"""

READING_LENS = {
"padanan":{"scan":"Tentukan dulu: sinonim, antonim, atau analogi?","model":"Ubah kata menjadi definisi sederhana; untuk analogi ubah A:B menjadi kalimat relasi.","attack":"Eliminasi opsi yang hanya 'terkait', lalu uji kandidat di konteks kalimat.","check":"Apakah hubungan dan arah relasinya tetap sama?"},
"kelompok":{"scan":"Cari empat item yang tampak membentuk kelompok paling kuat.","model":"Buat kategori tersempit yang memuat empat item.","attack":"Uji item kelima: apakah kategori juga memuatnya? Jika iya, kategorinya terlalu luas.","check":"Bisakah kamu menyelesaikan kalimat 'empat ini sama karena…'?"},
"silogisme":{"scan":"Lingkari quantifier: semua, sebagian, tidak ada, jika–maka.","model":"Ubah ke A/B/P/Q atau diagram himpunan kecil.","attack":"Tanya apakah kesimpulan pasti benar, bukan sekadar mungkin.","check":"Apakah kamu melakukan pembalikan implikasi atau generalisasi dari 'sebagian'?"},
"analisis":{"scan":"Cari semua aturan absolut: sebelum, sesudah, tepat, tidak boleh bersama.","model":"Ubah cerita menjadi slot/tabel/blok.","attack":"Gabungkan constraint paling mengunci lebih dulu.","check":"Untuk 'pasti', benar di semua konfigurasi? Untuk 'mungkin', ada minimal satu konfigurasi valid?"},
"operasi":{"scan":"Lihat struktur sebelum menghitung: faktor, pangkat, akar, pecahan, tanda.","model":"Cari bentuk yang bisa disederhanakan atau diestimasi.","attack":"Sederhanakan dulu, baru hitung presisi.","check":"Tanda, urutan operasi, dan orde besarnya masuk akal?"},
"persamaan":{"scan":"Identifikasi: linear, SPL, kuadrat, atau pertidaksamaan.","model":"Pilih eliminasi/substitusi/faktorisasi/Vieta/garis bilangan.","attack":"Gunakan metode terpendek yang sesuai bentuk.","check":"Substitusi balik atau cek tanda pertidaksamaan."},
"geometri":{"scan":"Tandai apa yang diketahui, ditanya, satuan, dan hubungan sudut/sisi.","model":"Cari segitiga siku-siku, kesebangunan, atau bentuk gabungan.","attack":"Pilih rumus hanya setelah hubungan gambar jelas.","check":"Apakah jawaban luas/keliling/volume dan satuannya benar?"},
"aritsos":{"scan":"Cari nilai awal, perubahan %, harga beli/jual, atau jenis barisan.","model":"Ubah persen ke faktor; bedakan U_n dan S_n.","attack":"Kerjakan dari basis/denominator yang benar.","check":"Perubahan bertahap sudah dikalikan, bukan dijumlah?"},
"sudut":{"scan":"Untuk jam: jam dan menit; untuk himpunan: total, A, B, irisan, luar.","model":"Jam → |30h−5,5m|; himpunan → diagram Venn.","attack":"Hitung komponen yang overlap dulu.","check":"Sudut sudah dibuat ≤180°? Irisan tidak dihitung dua kali?"},
"banding":{"scan":"Cari apakah hubungan senilai, berbalik nilai, work-rate, atau reverse percentage.","model":"Tentukan apa yang konstan: total, produk, rate, atau faktor.","attack":"Gunakan satu model saja sampai selesai.","check":"Jika pekerja bertambah, waktu seharusnya turun; cek arah hasil."},
"jarak":{"scan":"Tanya: mendekat, menjauh, menyusul, atau pergi-pulang?","model":"Gunakan relative speed yang tepat dan samakan satuan.","attack":"s=v×t; berpapasan jumlahkan v, menyusul kurangkan.","check":"Kecepatan rata-rata = total jarak/total waktu, bukan mean biasa."},
"peluang":{"scan":"Tentukan ruang sampel, urutan penting atau tidak, independen atau tidak.","model":"Pilih peluang langsung, komplemen, permutasi, atau kombinasi.","attack":"Hitung n(A) dan n(S) secara disiplin.","check":"Peluang harus 0–1 dan semua outcome relevan sudah dihitung."},
"statistika":{"scan":"Cari mean/median/modus/range/weighted mean atau interpretasi tabel.","model":"Untuk mean, pikirkan total = mean×n.","attack":"Kerjakan lewat total atau bobot; baca unit grafik.","check":"Ukuran kelompok dan bobot sudah diperhitungkan?"},
"deret":{"scan":"Jangan tebak pola kompleks: cek selisih, selisih kedua, rasio, alternating.","model":"Pisahkan posisi ganjil/genap jika perlu.","attack":"Ambil pola paling sederhana yang konsisten seluruh deret.","check":"Pola menjelaskan semua transisi, bukan hanya dua terakhir?"},
"deretfig":{"scan":"Lacak jumlah, posisi, orientasi, fill, ukuran, relasi.","model":"Tuliskan atribut yang berubah dan yang tetap.","attack":"Terapkan aturan per atribut ke frame berikut.","check":"Jangan samakan rotasi dengan refleksi."},
"analogifig":{"scan":"Fokus A→B: perubahan apa yang terjadi?","model":"Definisikan operator: rotate/reflect/move/add/remove/invert.","attack":"Terapkan operator yang sama ke C.","check":"Semua atribut penting ikut berubah konsisten?"},
"etika":{"scan":"Siapa aktor, apa kepentingan, ada konflik kepentingan atau tidak?","model":"Peta: aturan → risiko etik → jalur resmi → tindakan defensible.","attack":"Pilih opsi paling transparan, sah, dan melindungi kepentingan publik.","check":"Apakah pilihan tetap bisa dipertanggungjawabkan jika diaudit?"},
"wawasan":{"scan":"Kasus ini tentang nilai Pancasila, konstitusi, NKRI, keberagaman, atau bela negara?","model":"Hubungkan fakta kasus ke prinsip, bukan slogan.","attack":"Pilih prinsip yang paling langsung menjelaskan situasi.","check":"Apakah jawaban hanya hafalan kata atau benar-benar sesuai konteks?"},
"nilai":{"scan":"Cari kata kerja/perilaku dominan dalam kasus.","model":"Petakan ke IProSPeK berdasarkan perilaku inti.","attack":"Eliminasi nilai yang hanya muncul sebagai efek samping.","check":"Bisakah kamu menjelaskan satu kalimat mengapa nilai itu paling dominan?"},
"kepegawaian":{"scan":"Soal menguji aturan ASN umum, disiplin, proses pemeriksaan, hukuman, atau cuti?","model":"Pisahkan: substansi pelanggaran → proses → kewenangan/konsekuensi.","attack":"Gunakan regulasi yang tepat untuk lapisan yang ditanya.","check":"Jangan pakai aturan lama jika sudah diganti; cek level aturan dan konteks Kemenkeu."},
"keuangan":{"scan":"Identifikasi tahap siklus dan aktor: fiskal, pengguna anggaran, perbendaharaan, pemeriksa.","model":"Petakan ke UU 17/2003, UU 1/2004, atau UU 15/2004.","attack":"Bedakan mengelola, mengawasi internal, dan memeriksa eksternal.","check":"Aktor dan tahap siklus konsisten?"},
"struktur":{"scan":"Cari domain fungsi yang ditanya, bukan hanya singkatan unit.","model":"Isu → fungsi → unit organisasi current.","attack":"Eliminasi unit dengan domain paling jauh.","check":"Apakah nama unit masih current menurut PMK 124/2024 jo. PMK 117/2025?"},
}

FORMULAS = {
"operasi":[
("Urutan operasi","( ) → pangkat/akar → ×÷ → +−","Operasi setingkat dikerjakan kiri ke kanan."),
("Pangkat kali","a^m × a^n = a^(m+n)","Basis harus sama."),
("Pangkat bagi","a^m / a^n = a^(m−n)","a ≠ 0."),
("Pangkat dari pangkat","(a^m)^n = a^(mn)","Pangkat dikalikan."),
("Pangkat negatif","a^(−n)=1/a^n","Balik menjadi pecahan."),
("Pangkat nol","a^0=1","Untuk a ≠ 0."),
("Akar perkalian","√(ab)=√a·√b","Untuk nilai yang memenuhi domain real."),
("Akar pembagian","√(a/b)=√a/√b","b>0."),
("Rasionalisasi sederhana","1/√a = √a/a","Gunakan bila bentuk akar di penyebut."),
("FPB-KPK","FPB(a,b) × KPK(a,b) = a×b","Untuk dua bilangan positif."),
("Persen ke pecahan","p% = p/100","Gunakan benchmark mental."),
],
"persamaan":[
("Persamaan linear","ax+b=c → x=(c−b)/a","a ≠ 0."),
("Eliminasi SPL","samakan koefisien → kurangkan/jumlahkan","Cocok bila koefisien mudah disetarakan."),
("Substitusi SPL","isolasi satu variabel → substitusi","Cocok bila koefisien 1 atau sederhana."),
("Kuadrat","ax²+bx+c=0","Bentuk standar."),
("Rumus kuadrat","x=(-b±√(b²−4ac))/(2a)","Gunakan bila tidak mudah difaktorkan."),
("Diskriminan","D=b²−4ac","D>0 dua akar real; D=0 satu akar kembar; D<0 tidak ada akar real."),
("Vieta jumlah akar","x1+x2=−b/a","Lebih cepat jika hanya ditanya jumlah akar."),
("Vieta hasil kali","x1x2=c/a","Lebih cepat jika hanya ditanya hasil kali akar."),
("Titik puncak parabola","x_p=−b/(2a)","Substitusi untuk y_p."),
("Pertidaksamaan","kali/bagi bilangan negatif → balik tanda","Aturan wajib."),
],
"geometri":[
("Persegi","K=4s · L=s²","Diagonal=s√2."),
("Persegi panjang","K=2(p+l) · L=pl","Diagonal=√(p²+l²)."),
("Segitiga","L=½at","Jumlah sudut=180°."),
("Heron","L=√[s(s−a)(s−b)(s−c)]","s=½(a+b+c)."),
("Pythagoras","c²=a²+b²","Segitiga siku-siku."),
("Lingkaran","K=2πr · L=πr²","d=2r."),
("Panjang busur","s=(θ/360°)·2πr","θ sudut pusat."),
("Luas juring","L=(θ/360°)·πr²","θ sudut pusat."),
("Prisma","V=L_alas·t","Luas permukaan sesuai jaring-jaring."),
("Balok","V=plt","Diagonal ruang=√(p²+l²+t²)."),
("Kubus","V=s³","Luas permukaan=6s²; diagonal ruang=s√3."),
("Tabung","V=πr²t","Luas selimut=2πrt."),
("Kerucut","V=⅓πr²t","Garis pelukis s=√(r²+t²)."),
("Bola","V=4/3·πr³","Luas=4πr²."),
("Kesebangunan","sisi bersesuaian memiliki rasio sama","Luas berbanding kuadrat skala; volume kubik skala."),
],
"aritsos":[
("Persen perubahan","(baru−lama)/lama ×100%","Denominator = nilai lama."),
("Nilai setelah naik p%","akhir=awal(1+p)","p dalam desimal."),
("Nilai setelah turun p%","akhir=awal(1−p)","p dalam desimal."),
("Reverse percentage","awal=akhir/faktor perubahan","Jangan mengurangi persen dari nilai akhir."),
("Untung","U=HJ−HB","HJ harga jual; HB harga beli."),
("Persen untung","%U=U/HB×100%","Basis harga beli."),
("Rugi","R=HB−HJ","Saat HJ<HB."),
("Persen rugi","%R=R/HB×100%","Basis harga beli."),
("Diskon","harga akhir=harga label(1−d)","Diskon bertahap: kalikan faktor sisa."),
("Bunga sederhana","B=P·r·t","Pastikan unit waktu cocok dengan r."),
("Barisan aritmatika","U_n=a+(n−1)b","b beda tetap."),
("Jumlah aritmatika","S_n=n/2[2a+(n−1)b]","Atau n/2(a+U_n)."),
("Barisan geometri","U_n=ar^(n−1)","r rasio tetap."),
("Jumlah geometri","S_n=a(r^n−1)/(r−1)","r≠1."),
("Geometri tak hingga","S∞=a/(1−r)","Hanya |r|<1."),
],
"sudut":[
("Sudut jarum jam","θ=|30h−5,5m|","Jika >180°, gunakan 360°−θ."),
("Komplemen","A+B=90°","Dua sudut saling berpenyiku."),
("Suplemen","A+B=180°","Dua sudut berpelurus."),
("Jumlah sudut segitiga","A+B+C=180°",""),
("Jumlah sudut poligon","(n−2)180°","Jumlah sudut dalam."),
("Sudut dalam poligon beraturan","[(n−2)180°]/n",""),
("Gabungan 2 himpunan","n(A∪B)=n(A)+n(B)−n(A∩B)",""),
("Gabungan 3 himpunan","Σ tunggal − Σ irisan dua + irisan tiga","Inclusion–exclusion."),
("Komplemen himpunan","n(Aᶜ)=n(S)−n(A)",""),
],
"banding":[
("Rasio bagian","A:B=m:n → A=m/(m+n)·total","Untuk dua bagian."),
("Senilai","x1/y1=x2/y2","Naik-naik atau turun-turun."),
("Berbalik nilai","x1y1=x2y2","Satu naik, yang lain turun."),
("Rate kerja","r=1/t","Satu pekerjaan utuh."),
("Kerja bersama","1/T=1/a+1/b+…","Jumlahkan rate, bukan waktu."),
("Produktivitas","pekerjaan = rate × waktu × sumber daya","Gunakan bila jumlah pekerja berubah."),
("Reverse percentage","awal=akhir/(1±p)","Pilih + untuk kenaikan, − untuk penurunan."),
],
"jarak":[
("Dasar","s=v·t","s jarak, v kecepatan, t waktu."),
("Kecepatan","v=s/t",""),
("Waktu","t=s/v",""),
("Berpapasan","t=S/(v1+v2)","Arah saling mendekat."),
("Menyusul","t=gap/(v_cepat−v_lambat)","Arah sama."),
("Rata-rata kecepatan","v̄=total jarak/total waktu","Jangan rata-rata kecepatan begitu saja."),
("Jarak sama dua arah","v̄=2v1v2/(v1+v2)","Khusus jarak pergi-pulang sama."),
("Konversi","1 m/s = 3,6 km/jam","km/jam ÷3,6 = m/s."),
],
"peluang":[
("Peluang","P(A)=n(A)/n(S)","Outcome equiprobable."),
("Komplemen","P(Aᶜ)=1−P(A)","Sangat berguna untuk 'minimal satu'."),
("Gabungan","P(A∪B)=P(A)+P(B)−P(A∩B)",""),
("Independen","P(A∩B)=P(A)P(B)","Hanya jika independen."),
("Bersyarat","P(A|B)=P(A∩B)/P(B)","P(B)>0."),
("Faktorial","n!=n(n−1)…1","0!=1."),
("Permutasi","P(n,r)=n!/(n−r)!","Urutan penting."),
("Kombinasi","C(n,r)=n!/[r!(n−r)!]","Urutan tidak penting."),
("Permutasi unsur sama","n!/(a!b!…)","Untuk objek berulang."),
("Permutasi melingkar","(n−1)!","Jika rotasi dianggap sama."),
],
"statistika":[
("Mean","x̄=Σx/n",""),
("Total dari mean","Σx=x̄·n","Shortcut penting."),
("Weighted mean","x̄=Σ(wx)/Σw",""),
("Mean gabungan","(n1x̄1+n2x̄2)/(n1+n2)",""),
("Median posisi","(n+1)/2","Untuk data tunggal terurut, n ganjil."),
("Range","maks−min",""),
("Varians populasi","σ²=Σ(x−μ)²/N","Jika memang diuji."),
("Standar deviasi","σ=√σ²","Jika memang diuji."),
("Persentase bagian","bagian/total×100%","Untuk diagram/tabel."),
("Growth rate","(baru−lama)/lama×100%","Interpretasi data."),
],
"deret":[
("Aritmatika","U_n=a+(n−1)b","Selisih tetap."),
("Geometri","U_n=ar^(n−1)","Rasio tetap."),
("Selisih kedua","Δ² konstan → pola kuadrat","Gunakan sebagai diagnosis, bukan hafalan jawaban."),
("Fibonacci-type","U_n=U_(n−1)+U_(n−2)","Bisa memakai variasi koefisien."),
("Alternating","pisahkan posisi ganjil/genap","Sering menjadi dua deret interleaved."),
],
}

MNEMONICS = {
"etika":[
{"label":"Kaca Etik","mnemonic":"KON–PUB–TRANS–RESMI","meaning":"Konflik kepentingan → Kepentingan publik → Transparansi → Jalur resmi.","note":"Alat bantu UPKP Coach, bukan frasa regulasi."},
{"label":"BerAKHLAK","mnemonic":"Ber–A–K–H–L–A–K","meaning":"Berorientasi Pelayanan · Akuntabel · Kompeten · Harmonis · Loyal · Adaptif · Kolaboratif.","note":"Akronim resmi nilai dasar ASN."},
],
"wawasan":[
{"label":"Empat jangkar","mnemonic":"PA–UD–NK–BI","meaning":"Pancasila · UUD 1945 · NKRI · Bhinneka Tunggal Ika.","note":"Jembatan ingatan UPKP Coach."},
],
"nilai":[
{"label":"Nilai Kemenkeu","mnemonic":"I–PRO–SI–PE–K","meaning":"Integritas · Profesionalisme · Sinergi · Pelayanan · Kesempurnaan.","note":"IProSPeK mengikuti nama nilai Kementerian Keuangan."},
],
"kepegawaian":[
{"label":"Peta regulasi","mnemonic":"ASN–DIS–PERIKSA–CUTI","meaning":"UU ASN → disiplin PNS → proses pemeriksaan Kemenkeu → cuti PNS.","note":"Urutan belajar UPKP Coach."},
{"label":"Baca soal disiplin","mnemonic":"LANGGAR–PROSES–PEJABAT–AKIBAT","meaning":"Apa pelanggaran → bagaimana proses → siapa berwenang → apa konsekuensi.","note":"Kerangka analisis, bukan redaksi regulasi."},
],
"keuangan":[
{"label":"Tiga UU inti","mnemonic":"17–1–15 = KELOLA–BENDAHARA–PERIKSA","meaning":"UU 17/2003 Keuangan Negara → UU 1/2004 Perbendaharaan → UU 15/2004 Pemeriksaan.","note":"Jembatan ingatan UPKP Coach."},
{"label":"Siklus","mnemonic":"RENCANA–ANGGAR–LAKSANA–CATAT–LAPOR–PERIKSA–TINDAK","meaning":"Perencanaan → penganggaran → pelaksanaan → penatausahaan → pelaporan → pemeriksaan → tindak lanjut.","note":"Ringkasan alur belajar."},
],
"struktur":[
{"label":"Peta fungsi","mnemonic":"DUKUNG–AWAS–FISKAL–ANGGAR–TERIMA–BENDAHARA–ASET–TRANSFER–BIAYA–SEKTOR–DATA–BELAJAR","meaning":"Urutkan unit berdasarkan kelompok fungsi, bukan hafalan singkatan semata.","note":"Jembatan konseptual UPKP Coach; cek nama unit current pada sumber resmi."},
],
}

def reading_lens(code):
    return READING_LENS.get(code,{})

def hints(code):
    x=READING_LENS.get(code,{})
    return [x.get("scan"),x.get("model"),x.get("attack")] if x else []

def formulas(code):
    return [{"title":a,"formula":b,"note":c} for a,b,c in FORMULAS.get(code,[])]

def mnemonics(code):
    return MNEMONICS.get(code,[])
