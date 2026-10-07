from __future__ import annotations
import random
from .model import Q, mk, mk_svg_opts

INK="#111827"; BG="#ffffff"; GRID="#cbd5e1"

def _set_meta(q:Q,skill:str,archetype:str)->Q:
    q.skill=skill;q.archetype=archetype;return q

def _svg_frame(inner:str,size=100)->str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="100" height="100"><rect x="1" y="1" width="98" height="98" rx="8" fill="{BG}" stroke="{GRID}"/>{inner}</svg>'

def _shape(kind:str,rot:int=0,filled:bool=False,dot:int=0,inner:bool=False)->str:
    fill=INK if filled else BG
    if kind=="tri": pts="50,18 82,76 18,76"
    elif kind=="diamond": pts="50,14 84,50 50,86 16,50"
    else: pts="22,22 78,22 78,78 22,78"
    poly=f'<polygon points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="3" transform="rotate({rot} 50 50)"/>'
    dots=[(50,30),(70,50),(50,70),(30,50)];dx,dy=dots[dot%4]
    mark=f'<circle cx="{dx}" cy="{dy}" r="5" fill="{BG if filled else INK}" stroke="{INK}" stroke-width="1"/>'
    extra=f'<circle cx="50" cy="50" r="10" fill="none" stroke="{INK}" stroke-width="2"/>' if inner else ''
    return _svg_frame(poly+mark+extra)

def _matrix(cells:list[str])->str:
    coords=[(0,0),(108,0),(0,108)]
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 208 208" width="300" height="300">']
    for c,(x,y) in zip(cells,coords):
        inner=c.split('>',1)[1].rsplit('</svg>',1)[0]
        out.append(f'<g transform="translate({x},{y})">{inner}</g>')
    out.append('<g transform="translate(108,108)"><rect x="1" y="1" width="98" height="98" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="6 5"/><text x="50" y="66" text-anchor="middle" font-size="44" font-family="sans-serif" fill="#64748b">?</text></g></svg>')
    return ''.join(out)

def _fmt_rp(n:int)->str:return "Rp"+f"{int(n):,}".replace(",",".")

def _percent_q(d:int,rng:random.Random)->Q:
    v=rng.randrange(3)
    if v==0:
        base=rng.choice([240,320,400,480,600])*1000;up=rng.choice([20,25,30,40]);down=rng.choice([10,15,20,25])
        final=round(base*(1+up/100)*(1-down/100))
        q=mk("banding",d,f"Harga suatu barang {_fmt_rp(base)} naik {up}% lalu mendapat diskon {down}% dari harga setelah kenaikan. Harga akhirnya adalah…",final,
             [round(base*(1+(up-down)/100)),base,round(final*1.05),round(base*(1-down/100))],
             f"Kalikan faktor beruntun: {1+up/100:.2f} × {1-down/100:.2f} × harga awal.","Persentase beruntun = faktor × faktor, bukan selisih persen.",rng,waktu=58)
        return _set_meta(q,"numerik.multi_step_percent","percent_up_then_discount")
    if v==1:
        listed=rng.choice([300,400,500,600])*1000;disc=rng.choice([10,20,25]);tax=rng.choice([10,11])
        final=round(listed*(1-disc/100)*(1+tax/100))
        q=mk("banding",d,f"Harga label {_fmt_rp(listed)} didiskon {disc}%, kemudian dikenai pajak {tax}% dari harga setelah diskon. Total yang dibayar adalah…",final,
             [round(listed*(1-disc/100+tax/100)),listed,round(listed*(1+tax/100)),round(final*.95)],
             f"Harga bayar = harga label × {1-disc/100:.2f} × {1+tax/100:.2f}.","Urutan persen penting; tiap persen bekerja pada basis saat itu.",rng,waktu=60)
        return _set_meta(q,"numerik.multi_step_percent","percent_discount_then_tax")
    original=rng.choice([200,250,300,400])*1000;up=rng.choice([20,25,40]);new=round(original*(1+up/100));back=100*up/(100+up)
    corr=f"{back:.2f}%".replace(".",",")
    dis=[f"{up:.2f}%".replace(".",","),f"{100*up/100:.2f}%".replace(".",","),f"{back+5:.2f}%".replace(".",","),f"{back-5:.2f}%".replace(".",",")]
    q=mk("banding",d,f"Sebuah nilai naik {up}% dari {_fmt_rp(original)} menjadi {_fmt_rp(new)}. Agar kembali tepat ke nilai awal, nilai baru harus turun sebesar berapa persen?",corr,dis,
         f"Penurunan dihitung terhadap basis baru: selisih/original baru = {new-original}/{new} = {back:.2f}%.","Reverse percentage: gunakan basis baru, bukan mengulang persen kenaikan.",rng,waktu=58)
    return _set_meta(q,"numerik.multi_step_percent","percent_reverse_to_original")

def _weighted_q(d:int,rng:random.Random)->Q:
    if rng.random()<.5:
        n1=rng.choice([20,24,30,32]);n2=rng.choice([10,16,20,24]);a=rng.choice([68,70,72,75]);b=rng.choice([80,82,84,85])
        correct=(n1*a+n2*b)/(n1+n2);corr=f"{correct:.1f}".replace(".",",")
        q=mk("statistika",d,f"Kelompok A terdiri dari {n1} orang dengan rata-rata {a}. Kelompok B terdiri dari {n2} orang dengan rata-rata {b}. Rata-rata gabungan adalah…",corr,
             [f"{(a+b)/2:.1f}".replace(".",","),f"{correct+2:.1f}".replace(".",","),f"{correct-2:.1f}".replace(".",","),f"{correct+1:.1f}".replace(".",",")],
             f"Total nilai = {n1}×{a} + {n2}×{b}; bagi {n1+n2}.","Weighted mean: mean → total → gabungkan → bagi total orang.",rng,waktu=58)
        return _set_meta(q,"numerik.weighted_average","weighted_merge_groups")
    n1=rng.choice([20,25,30]);n2=rng.choice([10,15,20]);a=rng.choice([70,72,75]);combined=rng.choice([74,76,78]);b=((n1+n2)*combined-n1*a)/n2
    corr=f"{b:.1f}".replace(".",",")
    q=mk("statistika",d,f"Rata-rata {n1} peserta pertama adalah {a}. Setelah {n2} peserta lain digabung, rata-rata seluruh {n1+n2} peserta menjadi {combined}. Rata-rata kelompok tambahan adalah…",corr,
         [str(combined),str(a),f"{b+3:.1f}".replace(".",","),f"{b-3:.1f}".replace(".",",")],
         "Cari total gabungan lalu kurangi total kelompok awal; hasilnya dibagi jumlah peserta tambahan.","Missing-group mean: total gabungan − total lama = total kelompok baru.",rng,waktu=62)
    return _set_meta(q,"numerik.weighted_average","weighted_missing_group")

def _data_q(d:int,rng:random.Random,skill:str)->Q:
    v=rng.randrange(3)
    names=["Unit A","Unit B","Unit C","Unit D"]
    if v==0:
        base=[rng.randrange(80,151,5) for _ in names];growth=rng.sample([8,10,12,15,20,25],4);nxt=[round(a*(1+g/100)) for a,g in zip(base,growth)]
        table="| Unit | Tahun 1 | Tahun 2 |\n|---|---:|---:|\n"+"\n".join(f"| {n} | {a} | {b} |" for n,a,b in zip(names,base,nxt))
        rates=[(b-a)/a for a,b in zip(base,nxt)];idx=max(range(4),key=lambda i:rates[i]);correct=names[idx]
        q=Q(f"adv-data-{d}-{rng.randrange(10**9):09d}","statistika",d,table+"\n\nUnit manakah yang mengalami kenaikan persentase TERBESAR dari Tahun 1 ke Tahun 2?",names+["Semua sama"],idx,
            "Bandingkan kenaikan relatif: (Tahun 2 − Tahun 1) / Tahun 1, bukan selisih absolut.","Data interpretation: denominator yang benar lebih penting daripada selisih terbesar.",waktu=70,skill="numerik.data_interpretation",archetype="table_largest_percentage_growth");return q
    if v==1:
        target=[rng.randrange(90,141,5) for _ in names];done=[rng.randrange(55,96,5) for _ in names]
        actual=[round(t*p/100) for t,p in zip(target,done)]
        table="| Unit | Target | Realisasi |\n|---|---:|---:|\n"+"\n".join(f"| {n} | {t} | {a} |" for n,t,a in zip(names,target,actual))
        pct=[a/t for a,t in zip(actual,target)];idx=max(range(4),key=lambda i:pct[i])
        q=Q(f"adv-target-{d}-{rng.randrange(10**9):09d}","statistika",d,table+"\n\nUnit mana yang memiliki tingkat pencapaian target tertinggi?",names+["Tidak dapat ditentukan"],idx,
            "Hitung Realisasi/Target untuk tiap unit.","Jangan bandingkan realisasi absolut jika target tiap unit berbeda.",waktu=68,skill="numerik.data_interpretation",archetype="table_target_attainment");return q
    # combined inference across two columns
    base=[rng.randrange(100,181,10) for _ in names];cost=[rng.randrange(40,91,5) for _ in names];benefit=[rng.randrange(70,151,10) for _ in names]
    table="| Program | Biaya | Manfaat |\n|---|---:|---:|\n"+"\n".join(f"| {n} | {c} | {b} |" for n,c,b in zip(names,cost,benefit))
    ratios=[b/c for b,c in zip(benefit,cost)];idx=max(range(4),key=lambda i:ratios[i])
    q=Q(f"adv-ratio-{d}-{rng.randrange(10**9):09d}","statistika",d,table+"\n\nJika efisiensi didefinisikan sebagai Manfaat/Biaya, program mana yang paling efisien?",names+["Semua sama"],idx,
        "Bandingkan rasio Manfaat/Biaya, bukan manfaat tertinggi atau biaya terendah secara terpisah.","Saat definisi metrik diberikan, hitung tepat metrik itu dan abaikan angka yang tidak relevan.",waktu=72,skill="numerik.data_interpretation",archetype="table_benefit_cost_ratio");return q

def _logic_order_q(d:int,rng:random.Random)->Q:
    if rng.random()<.5:
        stem=("Lima orang duduk berurutan dari kiri ke kanan. Bima harus di kiri Citra. Deni tepat di kanan Ari. Eka tidak boleh di ujung. Manakah susunan yang mungkin?")
        opts=["Bima – Citra – Ari – Deni – Eka","Ari – Deni – Eka – Bima – Citra","Eka – Ari – Deni – Citra – Bima","Citra – Bima – Ari – Deni – Eka","Ari – Eka – Deni – Bima – Citra"]
        return Q(f"adv-log-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,1,"Opsi B memenuhi seluruh constraint.","Eliminasi opsi per constraint; jangan susun semua permutasi.",waktu=62,skill="logika.constraint_ordering",archetype="ordering_possible_sequence")
    stem=("Empat presentasi P, Q, R, S dijadwalkan berurutan. P harus sebelum R. Q tidak boleh pertama. S harus tepat setelah Q. Pernyataan mana yang PASTI benar?")
    opts=["P selalu pertama","R selalu terakhir","Q selalu sebelum S","S selalu terakhir","P selalu sebelum Q"]
    return Q(f"adv-order2-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,2,"Karena S harus tepat setelah Q, Q pasti berada sebelum S pada semua susunan valid.","Untuk 'pasti benar', cari aturan yang langsung diwajibkan oleh constraint, bukan posisi yang hanya mungkin.",waktu=62,skill="logika.constraint_ordering",archetype="ordering_must_be_true")

def _assignment_q(d:int,rng:random.Random)->Q:
    if rng.random()<.5:
        stem=("Empat proyek P, Q, R, S dibagikan kepada empat analis A, B, C, D, masing-masing satu proyek. A tidak boleh menangani P. B harus menangani Q atau R. Jika C menangani P, maka D harus menangani S. Manakah pembagian yang MUNGKIN?")
        opts=["A-P, B-Q, C-R, D-S","A-S, B-R, C-P, D-Q","A-Q, B-P, C-R, D-S","A-R, B-S, C-P, D-Q","A-Q, B-R, C-P, D-S"]
        return Q(f"adv-assign-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,4,"Opsi E memenuhi semua syarat.","Coret opsi yang melanggar syarat paling restriktif dahulu.",waktu=70,skill="logika.assignment_constraints",archetype="assignment_possible")
    stem=("Empat proyek P, Q, R, S dibagikan kepada A, B, C, D, masing-masing satu proyek. A tidak boleh menangani P. B harus menangani Q atau R. Jika C menangani P, maka D harus menangani S. Jika diketahui A menangani Q dan B menangani R, pembagian dua proyek yang tersisa yang memenuhi seluruh aturan adalah…")
    opts=["C-P, D-S","C-S, D-P","C-Q, D-P","C-R, D-S","C-S, D-Q"]
    return Q(f"adv-assign2-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,0,"Setelah A=Q dan B=R, tersisa P dan S untuk C dan D. Jika C=P, aturan memaksa D=S; itulah pembagian yang konsisten.","Kunci assignment: tetapkan informasi yang sudah pasti, coret slot terisi, baru terapkan conditional constraint.",waktu=64,skill="logika.assignment_constraints",archetype="assignment_conditional_remaining")

def _critical_q(d:int,rng:random.Random)->Q:
    v=rng.randrange(3)
    if v==0:
        stem=("Sebuah unit menerapkan sistem baru. Setelah tiga bulan, waktu penyelesaian rata-rata turun 18%, tetapi volume pekerjaan pada periode yang sama juga turun 12%. Kesimpulan yang PALING dapat dipertanggungjawabkan adalah…")
        opts=["Sistem baru pasti meningkatkan produktivitas 18%.","Penurunan waktu membuktikan kualitas layanan meningkat.","Ada perbaikan waktu penyelesaian, tetapi data belum cukup untuk mengisolasi pengaruh sistem baru.","Turunnya volume pasti menjadi satu-satunya penyebab.","Sistem baru tidak berdampak karena volume turun."]
        return Q(f"adv-ver-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,2,"Dua variabel berubah bersamaan; kausalitas tunggal belum terisolasi.","Bedakan observasi dari sebab-akibat.",waktu=68,skill="verbal.critical_inference",archetype="verbal_causality_limit")
    if v==1:
        stem=("Survei terhadap 120 pegawai sukarela menunjukkan 78% responden menyukai metode pelatihan baru. Kesimpulan mana yang paling tepat?")
        opts=["78% seluruh pegawai pasti menyukai metode baru.","Mayoritas responden survei menyukai metode baru, tetapi generalisasi ke seluruh pegawai memerlukan kehati-hatian.","Metode baru pasti lebih efektif.","Pegawai yang tidak menjawab pasti tidak menyukai metode baru.","Hasil survei tidak memberi informasi apa pun."]
        return Q(f"adv-sample-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,1,"Sampel sukarela dapat memiliki selection bias; hasil menggambarkan responden, bukan otomatis seluruh populasi.","Perhatikan siapa yang diukur sebelum menggeneralisasi.",waktu=64,skill="verbal.critical_inference",archetype="verbal_sample_generalization")
    stem=("Semua laporan yang terlambat menerima notifikasi. Beberapa laporan yang menerima notifikasi ternyata tidak terlambat. Pernyataan mana yang didukung informasi?")
    opts=["Semua laporan bernotifikasi terlambat.","Notifikasi hanya diberikan pada laporan terlambat.","Ada penyebab notifikasi selain keterlambatan.","Tidak ada laporan terlambat yang menerima notifikasi.","Semua laporan tepat waktu menerima notifikasi."]
    return Q(f"adv-inf-{d}-{rng.randrange(10**9):09d}","analisis",d,stem,opts,2,"Karena sebagian laporan bernotifikasi tidak terlambat, notifikasi dapat muncul karena alasan lain.","Jangan membalik implikasi: terlambat→notifikasi tidak berarti notifikasi→terlambat.",waktu=58,skill="verbal.critical_inference",archetype="verbal_inverse_inference")

def _onlyif_q(d:int,rng:random.Random)->Q:
    if rng.random()<.5:
        stem=("Sebuah dokumen dapat diterbitkan hanya jika telah diverifikasi dan memiliki persetujuan akhir. Dokumen X telah diterbitkan. Pernyataan yang pasti benar adalah…")
        opts=["Dokumen X hanya diverifikasi","Dokumen X hanya memiliki persetujuan akhir","Dokumen X telah diverifikasi dan memiliki persetujuan akhir","Setiap dokumen yang diverifikasi pasti diterbitkan","Tidak dapat ditentukan"]
        return Q(f"adv-if-{d}-{rng.randrange(10**9):09d}","silogisme",d,stem,opts,2,"Diterbitkan hanya jika V dan A berarti Diterbitkan → (V dan A).","P hanya jika Q = P→Q.",waktu=48,skill="logika.only_if",archetype="only_if_conjunction")
    stem=("Pegawai boleh mengakses sistem khusus hanya jika telah mengikuti pelatihan. Rani belum mengikuti pelatihan. Apa yang pasti benar?")
    opts=["Rani tidak boleh mengakses sistem khusus","Rani pasti bukan pegawai","Semua yang mengikuti pelatihan pasti mengakses sistem","Rani boleh mengakses jika mendapat izin lisan","Tidak dapat disimpulkan"]
    return Q(f"adv-if2-{d}-{rng.randrange(10**9):09d}","silogisme",d,stem,opts,0,"Akses → Pelatihan. Tidak Pelatihan → Tidak Akses (modus tollens).","Only-if memberi syarat perlu; negasi syarat meniadakan akibat.",waktu=44,skill="logika.only_if",archetype="only_if_modus_tollens")

def _figural_q(d:int,rng:random.Random)->Q:
    v=rng.randrange(3);kind=rng.choice(["tri","diamond","square"]);r0=rng.choice([0,90,180,270]);dot=rng.randrange(4);fill=rng.choice([False,True])
    if v==0:
        A=_shape(kind,r0,fill,dot);B=_shape(kind,(r0+90)%360,not fill,dot);C=_shape(kind,(r0+180)%360,fill,(dot+1)%4);correct=_shape(kind,(r0+270)%360,not fill,(dot+1)%4)
        distract=[_shape(kind,(r0+180)%360,not fill,(dot+1)%4),_shape(kind,(r0+270)%360,fill,(dot+1)%4),_shape(kind,(r0+270)%360,not fill,dot),_shape(kind,(r0+90)%360,not fill,(dot+2)%4)]
        q=mk_svg_opts("analogifig",d,"Lengkapi matriks 2×2 berikut.",[correct]+distract,0,"Horizontal: rotasi +90° dan fill berganti. Vertikal: rotasi +180° dan titik bergeser satu posisi.","Pisahkan aturan baris dan kolom; jawaban harus memenuhi keduanya.",rng,svg=_matrix([A,B,C]),waktu=72)
        return _set_meta(q,"figural.matrix_transform","matrix_rotation_fill_dot")
    if v==1:
        kinds=["tri","square","diamond"];k0=rng.randrange(3)
        A=_shape(kinds[k0],r0,False,dot);B=_shape(kinds[(k0+1)%3],r0,False,(dot+1)%4);C=_shape(kinds[(k0+1)%3],(r0+90)%360,True,dot);correct=_shape(kinds[(k0+2)%3],(r0+90)%360,True,(dot+1)%4)
        distract=[_shape(kinds[k0],(r0+90)%360,True,(dot+1)%4),_shape(kinds[(k0+2)%3],r0,True,(dot+1)%4),_shape(kinds[(k0+2)%3],(r0+90)%360,False,(dot+1)%4),_shape(kinds[(k0+1)%3],(r0+180)%360,True,dot)]
        q=mk_svg_opts("analogifig",d,"Lengkapi matriks 2×2 berikut.",[correct]+distract,0,"Horizontal: jenis bentuk maju satu dan titik bergeser. Vertikal: rotasi +90° dan fill berubah menjadi hitam.","Cari perubahan atribut yang independen: bentuk, titik, orientasi, fill.",rng,svg=_matrix([A,B,C]),waktu=74)
        return _set_meta(q,"figural.matrix_transform","matrix_shape_cycle_rotation")
    A=_shape(kind,r0,False,dot,False);B=_shape(kind,r0,False,(dot+2)%4,True);C=_shape(kind,(r0+180)%360,True,dot,False);correct=_shape(kind,(r0+180)%360,True,(dot+2)%4,True)
    distract=[_shape(kind,(r0+180)%360,False,(dot+2)%4,True),_shape(kind,r0,True,(dot+2)%4,True),_shape(kind,(r0+180)%360,True,dot,True),_shape(kind,(r0+90)%360,True,(dot+1)%4,True)]
    q=mk_svg_opts("analogifig",d,"Lengkapi matriks 2×2 berikut.",[correct]+distract,0,"Horizontal: titik pindah ke sisi berlawanan dan lingkaran tengah ditambahkan. Vertikal: bentuk diputar 180° dan fill dibalik.","Gunakan decomposition per atribut; jangan menebak bentuk keseluruhan.",rng,svg=_matrix([A,B,C]),waktu=76)
    return _set_meta(q,"figural.matrix_transform","matrix_opposite_dot_inner_mark")

def generate(skill:str,difficulty:int,rng:random.Random)->Q|None:
    d=max(4,min(5,int(difficulty)))
    if skill=="numerik.multi_step_percent":return _percent_q(d,rng)
    if skill=="numerik.weighted_average":return _weighted_q(d,rng)
    if skill in ("numerik.data_interpretation","numerik.rate_change_table"):return _data_q(d,rng,skill)
    if skill=="logika.constraint_ordering":return _logic_order_q(d,rng)
    if skill=="logika.assignment_constraints":return _assignment_q(d,rng)
    if skill=="verbal.critical_inference":return _critical_q(d,rng)
    if skill=="logika.only_if":return _onlyif_q(d,rng)
    if skill=="figural.matrix_transform":return _figural_q(d,rng)
    return None

ADVANCED_SKILLS=["numerik.multi_step_percent","numerik.weighted_average","numerik.data_interpretation","numerik.rate_change_table","logika.constraint_ordering","logika.assignment_constraints","verbal.critical_inference","logika.only_if","figural.matrix_transform"]
