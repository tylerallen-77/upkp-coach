"""TPA enrichment layer.

This is original instructional content inspired by common cognitive-assessment
constructs (numerical, verbal, deductive, inductive, perceptual/spatial), not
copied questions. The uploaded UPKP material remains the relevance anchor.
"""
SOURCES = [
    {"name":"SHL Ability Tests","url":"https://www.shl.hu/en/tests-tools/ability-tests","use":"numerical, deductive, inductive, verbal critical reasoning"},
    {"name":"SHL Practice Tests","url":"https://www.shlglobal.cn/en/shldirect/en/practice-tests/","use":"table/data interpretation and inference formats"},
    {"name":"Aon Online Assessment Practice","url":"https://www.aon.com/en/capabilities/talent-and-rewards/prepare-for-your-online-assessment","use":"numerical, verbal, inductive and deductive reasoning archetypes"},
    {"name":"Thomas GIA","url":"https://www.thomas.co/assessments/general-intelligence-assessment-gia","use":"reasoning, perceptual speed, number speed/accuracy, word meaning, spatial visualization"},
]

ENRICHMENT = {
"padanan": """Fokus tambahan:
• functional relation: alat→fungsi, profesi→hasil, bagian→keseluruhan
• directionality: relasi harus bekerja dalam arah yang sama
• abstraction: pilih relasi inti, bukan asosiasi permukaan

Shortcut: ubah pasangan menjadi satu kalimat relasi pendek, lalu terapkan kalimat itu ke opsi.""",
"kelompok": """Fokus tambahan:
• semantic category vs functional category
• odd-one-out dengan atribut paling spesifik
• hierarchical grouping dan shared property

Shortcut: cari satu atribut yang menjelaskan 4 opsi sekaligus; jangan mulai dari opsi yang terasa asing.""",
"silogisme": """Fokus tambahan:
• quantifier: semua / sebagian / tidak ada
• modus ponens & modus tollens
• converse / inverse trap
• 'P hanya jika Q' = P→Q

Shortcut: simbolkan premis sebelum menilai opsi. Jangan menguatkan kesimpulan melebihi premis.""",
"analisis": """Fokus tambahan:
• constraint ordering
• scheduling & assignment
• necessary vs possible conclusion
• verbal critical inference

Shortcut: tulis constraint sebagai rantai/slot, lalu eliminasi opsi; jangan membangun semua kemungkinan dari nol.""",
"operasi": """Fokus tambahan:
• compensation dekat 10/100/1000
• factorization dan difference of squares
• estimasi untuk eliminasi opsi
• number speed & accuracy

Shortcut: cari bentuk yang bisa diubah, bukan langsung hitung panjang.""",

"persamaan": """Fokus tambahan:
• isolasi variabel dan substitusi cepat
• persamaan proporsional
• sistem dua variabel sederhana
• eliminasi opsi dengan back-solving

Shortcut: bila pilihan jawaban numerik, sering lebih cepat substitusi opsi daripada menyelesaikan aljabar penuh.""",
"geometri": """Fokus tambahan:
• luas/keliling sebagai relasi, bukan hafalan lepas
• perubahan skala: panjang k× → luas k²×
• Pythagoras triplet umum
• visual decomposition

Shortcut: sebelum hitung, cari apakah soal cukup diselesaikan dengan rasio skala atau bentuk standar.""",
"aritsos": """Fokus tambahan:
• untung-rugi dan margin vs markup
• diskon bertingkat
• bunga/pertumbuhan sederhana
• work-rate sebagai total work

Shortcut: tentukan basis persen dulu; banyak jebakan datang dari denominator yang berbeda.""",
"sudut": """Fokus tambahan:
• sudut garis sejajar
• jumlah sudut segitiga/poligon
• himpunan dan inklusi-eksklusi
• membaca diagram sebelum menghitung

Shortcut: tandai sudut yang pasti sama/berpelurus; untuk dua himpunan gunakan A∪B=A+B−irisan.""",
"jarak": """Fokus tambahan:
• distance = speed × time
• average speed dari total jarak/total waktu
• relative speed berlawanan/searah
• target-total reasoning

Shortcut: jangan merata-ratakan kecepatan secara langsung kecuali durasinya sama.""",
"peluang": """Fokus tambahan:
• complement probability
• kombinasi vs permutasi
• independent events
• counting sebelum probability

Shortcut: 'setidaknya satu' sering paling cepat lewat 1 − P(tidak ada).""",
"banding": """Fokus tambahan:
• direct/inverse ratio
• reverse percentage
• multi-step percentage
• work-rate equivalence

Shortcut: persen balik arah → basis 100; pekerjaan tetap → tenaga×waktu konstan.""",
"statistika": """Fokus tambahan:
• weighted average
• perubahan mean/total
• interpretasi tabel dan data
• memilih angka relevan di tengah informasi noise

Shortcut: rata-rata selalu bisa diubah menjadi total = n×mean.""",
"deret": """Fokus tambahan:
• first/second difference
• alternating operations
• interleaved sequences
• ×n ± k
• recursive / position-dependent patterns

Shortcut: cek selisih → rasio → alternating → interleaving, dalam urutan itu.""",
"deretfig": """Fokus tambahan:
• perubahan jumlah, posisi, rotasi, shading
• dua aturan simultan
• pola alternating/interleaving visual

Shortcut: pisahkan atribut gambar (jumlah, orientasi, isi, posisi) dan cari aturan per atribut.""",
"analogifig": """Fokus tambahan:
• transformasi rotasi/refleksi
• add/remove element
• position mapping
• relational composition

Shortcut: sebutkan transformasi A→B secara eksplisit, lalu terapkan ke C.""",
}
