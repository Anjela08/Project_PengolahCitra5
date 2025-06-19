import streamlit as st
import os
from datetime import datetime

# Konfigurasi halaman (pindahkan ini ke app.py jika gabung multi-modul)
# st.set_page_config(page_title="Informasi CV DESAIN KREASI SUPPLIER", layout="wide")

DATA_FILE = "data/informasi.txt"
os.makedirs("data", exist_ok=True)

# -------------------- Fungsi Baca Data -------------------- #
def baca_data_info():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    data_info = []
    for line in lines:
        try:
            tanggal, judul, isi = line.strip().split("|", 2)
            data_info.append({"tanggal": tanggal, "judul": judul, "isi": isi})
        except:
            continue
    return data_info

# -------------------- Fungsi Simpan Info -------------------- #
def simpan_info(judul, isi):
    tanggal = datetime.now().strftime("%A, %d %B %Y")
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(f"{tanggal}|{judul}|{isi}\n")

# -------------------- Tampilan Utama -------------------- #
def tampilkan_informasi():
    st.markdown("<h1 style='color:#0077B6;'>📢 Informasi Umum</h1>", unsafe_allow_html=True)
    st.markdown("💬 Berikut adalah pengumuman dan informasi penting perusahaan:")

    with st.expander("📝 Tambah Informasi Baru", expanded=False):
        with st.form("form_info"):
            judul_baru = st.text_input("🖋️ Judul Informasi")
            isi_baru = st.text_area("📄 Isi Informasi")
            submitted = st.form_submit_button("✅ Simpan")
            if submitted:
                if judul_baru.strip() and isi_baru.strip():
                    simpan_info(judul_baru.strip(), isi_baru.strip())
                    st.success("✅ Informasi berhasil ditambahkan dan akan tampil untuk semua user.")
                    st.experimental_rerun()
                else:
                    st.warning("⚠️ Judul dan isi tidak boleh kosong.")

    st.markdown("---")
    st.subheader("📂 Daftar Informasi Tersedia")

    data_info = baca_data_info()
    if not data_info:
        st.info("📭 Belum ada informasi yang tersedia.")
    else:
        for info in reversed(data_info):  # terbaru di atas
            with st.container():
                st.markdown(f"### 📰 {info['judul']}")
                st.caption(f"📅 {info['tanggal']}")
                st.write(info['isi'])
                st.markdown("---")
