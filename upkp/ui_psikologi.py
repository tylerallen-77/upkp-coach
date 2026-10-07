"""Halaman Streamlit untuk subtes psikologi non-pilihan ganda: DISC, karakteristik pribadi, skala penilaian diri, Pauli."""
from __future__ import annotations

import random
import time

import streamlit as st

from . import content_psikologi as cp


def _catatan():
    st.info("Format subtes ini **perkiraan** (halaman buku belum tersedia) dan **tidak ada jawaban benar/salah**. "
            "Hasilnya bukan alat ukur psikologi yang tervalidasi; gunanya hanya membiasakan format dan melatih konsistensi.")


def halaman_disc():
    _catatan()
    if "disc_set" not in st.session_state:
        st.session_state.disc_set = cp.disc_kelompok(random.Random(), 8)
    kelompok = st.session_state.disc_set
    st.write("Pada tiap kelompok, pilih satu kata yang **paling** menggambarkan Anda dan satu yang **paling tidak** menggambarkan Anda.")
    pilihan = []
    valid = True
    for i, item in enumerate(kelompok):
        kata = [k for _, k in item]
        peta = {k: t for t, k in item}
        c1, c2 = st.columns(2)
        p = c1.selectbox(f"{i + 1}. Paling sesuai", ["—"] + kata, key=f"disc_p{i}")
        k = c2.selectbox(f"{i + 1}. Paling tidak sesuai", ["—"] + kata, key=f"disc_k{i}")
        if p == "—" or k == "—" or p == k:
            valid = False
        else:
            pilihan.append((peta[p], peta[k]))
    c1, c2 = st.columns(2)
    if c1.button("Lihat hasil", disabled=not valid, type="primary"):
        skor = cp.hitung_disc(pilihan)
        st.session_state.disc_hasil = skor
    if c2.button("Ganti kelompok kata"):
        for key in [k for k in st.session_state if str(k).startswith("disc_")]:
            del st.session_state[key]
        st.rerun()
    if not valid:
        st.caption("Lengkapi semua kelompok dan pastikan pilihan “paling sesuai” dan “paling tidak sesuai” berbeda.")
    if "disc_hasil" in st.session_state:
        skor = st.session_state.disc_hasil
        st.subheader("Profil Anda (latihan)")
        st.bar_chart({t: [v] for t, v in skor.items()})
        urut = sorted(skor.items(), key=lambda kv: -kv[1])
        st.write(f"Kecenderungan tertinggi: **{urut[0][0]}**. " + cp.DISC_PENJELASAN[urut[0][0]])
        st.write(f"Kedua: **{urut[1][0]}**. " + cp.DISC_PENJELASAN[urut[1][0]])
        st.caption("Skor = berapa kali tipe dipilih paling sesuai dikurangi dipilih paling tidak sesuai.")


def halaman_karakter():
    _catatan()
    st.write("Nilai seberapa sesuai pernyataan dengan diri Anda: 1 = sangat tidak sesuai, 5 = sangat sesuai.")
    nilai = []
    for i, (_, teks, _) in enumerate(cp.KARAKTER):
        nilai.append(st.radio(f"{i + 1}. {teks}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"kar_{i}"))
    if st.button("Lihat hasil", disabled=any(v is None for v in nilai), type="primary"):
        hasil, kons = cp.hitung_karakter(nilai)
        st.subheader("Hasil latihan")
        st.bar_chart(hasil)
        st.write(f"Indeks konsistensi: **{kons:.0%}**. Butir yang maknanya berkebalikan seharusnya dijawab berkebalikan pula.")
        if kons < 0.7:
            st.warning("Jawaban Anda kurang konsisten antar-butir berkebalikan. Di tes sesungguhnya, ini bisa terbaca sebagai jawaban tidak jujur atau tidak teliti.")
        else:
            st.success("Jawaban Anda cukup konsisten.")


def halaman_skala():
    _catatan()
    st.write("Nilai kemampuan diri Anda: 1 = sangat rendah, 5 = sangat tinggi. Pikirkan satu contoh nyata sebelum memberi nilai tinggi.")
    nilai = []
    for i, teks in enumerate(cp.SKALA):
        nilai.append(st.radio(f"{i + 1}. {teks}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"skl_{i}"))
    if st.button("Lihat hasil", disabled=any(v is None for v in nilai), type="primary"):
        rata = sum(nilai) / len(nilai)
        st.metric("Rata-rata penilaian diri", f"{rata:.2f} / 5")
        if len(set(nilai)) == 1:
            st.warning("Semua butir sama. Jawaban yang seragam di semua butir bisa terlihat tidak reflektif.")
        elif rata >= 4.6:
            st.warning("Rata-rata sangat tinggi. Pastikan Anda bisa memberi contoh nyata untuk tiap butir.")
        else:
            st.success("Sebaran jawaban wajar.")


def halaman_pauli():
    _catatan()
    st.write("Jumlahkan **dua angka berurutan** dalam kolom, lalu tulis **angka satuan** hasilnya. Contoh: 7 dan 8 → 15 → tulis 5. "
             "Ketik semua jawaban berurutan tanpa spasi.")
    if "pauli" not in st.session_state:
        d, k = cp.pauli_kolom(random.Random(), 26)
        st.session_state.pauli = {"d": d, "k": k, "t0": time.time(), "hasil": None}
    p = st.session_state.pauli
    st.code("   ".join(str(x) for x in p["d"][:13]) + "\n" + "   ".join(str(x) for x in p["d"][13:]), language=None)
    st.caption("Baca baris pertama dari kiri ke kanan, lalu baris kedua. Jumlahkan tiap pasangan yang berdekatan (angka ke-1 dan ke-2, ke-2 dan ke-3, dan seterusnya).")
    isi = st.text_input(f"Jawaban ({len(p['k'])} digit)", max_chars=len(p["k"]) + 5, key="pauli_isi")
    c1, c2 = st.columns(2)
    if c1.button("Kumpulkan", type="primary"):
        dur = time.time() - p["t0"]
        benar, salah, kosong = cp.nilai_pauli(isi, p["k"])
        p["hasil"] = (benar, salah, kosong, dur)
    if c2.button("Ganti soal"):
        for key in ("pauli", "pauli_isi"):
            st.session_state.pop(key, None)
        st.rerun()
    if p["hasil"]:
        benar, salah, kosong, dur = p["hasil"]
        st.subheader("Hasil latihan")
        a, b, c, d = st.columns(4)
        a.metric("Benar", benar)
        b.metric("Salah", salah)
        c.metric("Kosong", kosong)
        d.metric("Waktu", f"{dur:.0f} dtk")
        cepat = (benar + salah) / max(dur, 1) * 60
        st.write(f"Kecepatan: **{cepat:.0f} jawaban/menit**. Ketelitian: **{benar / max(benar + salah, 1):.0%}**.")
        st.caption("Di tes sesungguhnya, nilai dihitung dari kecepatan, ketelitian, ketahanan (tidak melambat), dan konsistensi sepanjang kolom.")
        if salah + kosong:
            st.write("Kunci jawaban: " + "".join(str(x) for x in p["k"]))
