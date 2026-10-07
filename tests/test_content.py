"""Uji isi soal: format, keunikan opsi, kunci jawaban, teka-teki, dan verifikasi mandiri soal numerik."""
import itertools
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from upkp import engine  # noqa: E402
from upkp.curriculum import BAB  # noqa: E402


def test_semua_generator_valid():
    for b in BAB:
        if b.mode != "pg":
            continue
        for lv in engine.level_tersedia(b.kode):
            for i in range(120):
                q = engine.generate(b.kode, lv, random.Random(i * 13 + lv))
                n = len(q.opt_svgs) if q.opt_svgs else len(q.opts)
                assert n == 5, (b.kode, lv, q.stem[:60])
                assert 0 <= q.ans < n
                if not q.opt_svgs:
                    assert len(set(q.opts)) == 5, (b.kode, lv, q.opts)
                else:
                    assert len(set(q.opt_svgs)) == 5, (b.kode, lv, "opsi gambar kembar")
                assert q.exp and q.trick, (b.kode, lv)
                assert q.lv == lv, (b.kode, q.lv, lv)
                assert q.bab == b.kode


def test_tryout_id_unik():
    for paket in engine.PAKET:
        for lv in (0, 1, 2, 3):
            qs = engine.bangun_tryout(paket, lv, random.Random(7 + lv))
            ids = [q.id for q in qs]
            assert len(ids) == len(set(ids))
            assert len(qs) > 0


def test_teka_teki_jawaban_unik():
    # toko
    sol = []
    for p in itertools.permutations(["obat", "buku", "roti", "sepatu", "pakaian"]):
        pos = {n: i for i, n in enumerate(p)}
        if pos["obat"] != 0 or pos["roti"] != 1:
            continue
        if abs(pos["buku"] - pos["sepatu"]) != 1 or abs(pos["pakaian"] - pos["roti"]) == 1 or abs(pos["sepatu"] - pos["roti"]) == 1:
            continue
        sol.append(p)
    assert len(sol) == 1 and sol[0][2] == "buku"
    # piket
    sol = [p for p in itertools.permutations(range(5)) if p[0] not in (0, 4) and p[2] - p[1] == 1 and p[3] > p[0] and p[4] == 4]
    assert len(sol) == 1 and "ABCDE"[sol[0].index(1)] == "C"
    # ekstrakurikuler
    ok = lambda s: not ("D" in s and "F" in s) and ("M" not in s or "C" in s) and ("B" not in s or "F" in s)
    pil = {"Basket,Drama,Musik": {"B", "D", "M"}, "Catur,Futsal,Musik": {"C", "F", "M"}, "Basket,Catur,Drama": {"B", "C", "D"},
           "Drama,Futsal,Musik": {"D", "F", "M"}, "Basket,Drama,Futsal": {"B", "D", "F"}}
    assert [k for k, v in pil.items() if ok(v)] == ["Catur,Futsal,Musik"]


def test_jawaban_numerik_diverifikasi_mandiri():
    import verify_numerik
    checked, fails = verify_numerik.run_all(150)
    assert sum(checked.values()) > 1500
    assert not fails, fails[:5]


def test_deret_angka_tidak_ambigu():
    import verify_deret
    dicek, gagal, ambigu = verify_deret.run_all(300)
    assert dicek > 300
    assert not gagal, gagal[:3]
    assert not ambigu, ambigu[:3]


def test_regulasi_konsisten():
    from upkp import regulasi
    from upkp.curriculum import BAB_BY_KODE
    assert len(regulasi.REGULASI) >= 26
    for dft, benar, isi, status, cat, bab in regulasi.REGULASI:
        assert status in regulasi.STATUS_LABEL, (dft, status)
        assert bab in BAB_BY_KODE, (dft, bab)
        assert dft and benar and isi and cat


def test_tskkwk_semua_bab_punya_soal_tiap_tingkat():
    for kode in ["etika", "wawasan", "nilai", "kepegawaian", "keuangan", "struktur"]:
        assert engine.level_tersedia(kode) == [1, 2, 3], kode


if __name__ == "__main__":
    for nama, fn in list(globals().items()):
        if nama.startswith("test_"):
            fn()
            print("OK", nama)


# ---------------------------------------------------------------- pembangkit berbasis fakta
def test_fakta_pembangkit_valid_dan_banyak():
    import collections
    from upkp.registry import generate
    ids = collections.defaultdict(set)
    for bab in ["etika", "wawasan", "nilai", "kepegawaian", "keuangan", "struktur", "kelompok"]:
        for lv in (1, 2, 3):
            for i in range(250):
                q = generate(bab, lv, random.Random(i * 31 + lv))
                assert len(set(q.opts)) == 5 and q.lv == lv and q.exp and q.trick
                ids[bab].add(q.id)
    # soal unik yang dapat dibangkitkan (berdasarkan id) harus jauh lebih banyak daripada bank tulisan
    assert sum(len(v) for v in ids.values()) > 400, {k: len(v) for k, v in ids.items()}


def test_fakta_regulasi_konsisten_dengan_basis():
    import re
    from upkp import faktabase as fb
    from upkp.registry import generate
    judul_by_nomor = {r[1]: r[2] for r in fb.REGULASI_FAKTA}
    nomor_by_judul = {r[2]: r[1] for r in fb.REGULASI_FAKTA}
    cek = 0
    for bab in ["etika", "nilai", "kepegawaian", "keuangan", "struktur"]:
        for lv in (1, 2, 3):
            for i in range(300):
                q = generate(bab, lv, random.Random(i * 7 + lv))
                benar = q.opts[q.ans]
                m = re.match(r"\*\*(.+?)\*\* mengatur tentang …", q.stem)
                if m and m[1] in judul_by_nomor:
                    assert benar == judul_by_nomor[m[1]], (q.stem, benar)
                    cek += 1
                m = re.match(r"Peraturan yang berjudul/mengatur tentang “(.+?)” adalah …", q.stem)
                if m:
                    assert benar == nomor_by_judul[m[1]], (q.stem, benar)
                    # tidak boleh ada opsi lain yang judulnya saling memuat dengan judul benar
                    for o in q.opts:
                        if o != benar and o in judul_by_nomor:
                            j = judul_by_nomor[o]
                            assert m[1] not in j and j not in m[1], (q.stem, o)
                    cek += 1
    assert cek > 200


def test_fakta_nilai_dan_unit_konsisten():
    import re
    from upkp import faktabase as fb
    from upkp.registry import generate
    p2n = {p: n for n, d in fb.NILAI_KEMENKEU.items() for p in d["perilaku"]}
    for i in range(300):
        q = generate("nilai", 1, random.Random(i))
        m = re.match(r"Perilaku utama “\*\*(.+?)\*\*” termasuk", q.stem)
        if m:
            assert q.opts[q.ans] == p2n[m[1]]
        m = re.match(r"Berikut adalah perilaku utama nilai \*\*(.+?)\*\*, KECUALI", q.stem)
        if m:
            aneh = q.opts[q.ans]
            assert aneh not in fb.NILAI_KEMENKEU[m[1]]["perilaku"] and aneh in p2n
            assert all(o in fb.NILAI_KEMENKEU[m[1]]["perilaku"] for j, o in enumerate(q.opts) if j != q.ans)
    unit = {u[1]: u[2] for u in fb.UNIT}
    for i in range(300):
        q = generate("struktur", 2, random.Random(i))
        m = re.match(r"\*\*(.+?)\*\* bertugas di bidang …", q.stem)
        if m:
            assert q.opts[q.ans] == unit[m[1]]


def test_kategori_kelompok_tak_ambigu():
    from upkp import faktabase as fb
    from upkp.registry import generate
    for nama, lv, anggota, bukan in fb.KATEGORI:
        assert len(anggota) >= 4 and len(bukan) >= 1
        assert not set(anggota) & set(bukan), nama
    # anggota yang muncul pada sebuah soal selalu dari kategori yang sama, pengecoh bukan anggotanya
    import re
    for lv in (1, 2, 3):
        for i in range(300):
            q = generate("kelompok", lv, random.Random(i * 5 + lv))
            m = re.search(r"\*\*(.+?)\*\* bukan (.+?)\.", q.exp)
            if m:
                aneh, nama = m[1], m[2]
                kat = next(k for k in fb.KATEGORI if k[0] == nama)
                assert aneh == q.opts[q.ans] and aneh in kat[3]
                assert all(o in kat[2] for j, o in enumerate(q.opts) if j != q.ans)
