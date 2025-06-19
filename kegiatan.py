import streamlit as st
from PIL import Image
import os
from datetime import datetime

# Folder dan file data
DATA_PATH = "data/kegiatan.txt"
FOLDER_GAMBAR = "images/kegiatan/"
os.makedirs(FOLDER_GAMBAR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# ------------------- Fungsi Hapus Kegiatan ------------------- #
def hapus_kegiatan(line_to_delete, path_gambar):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line for line in lines if line.strip() != line_to_delete.strip()]
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    if os.path.exists(path_gambar):
        os.remove(path_gambar)

# ------------------- Fungsi Utama ------------------- #
def tampilkan_kegiatan():
    st.title("📸 KEGIATAN CV DESAIN KREASI SUPPLIER")

    st.subheader("📝 Upload Kegiatan Baru")
    uploaded_file = st.file_uploader("Pilih Gambar", type=["jpg", "jpeg", "png"])
    deskripsi = st.text_area("Deskripsi Kegiatan")

    if st.button("✅ Simpan Kegiatan"):
        if uploaded_file and deskripsi.strip():
            tanggal = datetime.now().strftime("%A, %d %B %Y")
            nama_file = uploaded_file.name
            simpan_path = os.path.join(FOLDER_GAMBAR, nama_file)

            with open(simpan_path, "wb") as f:
                f.write(uploaded_file.read())

            with open(DATA_PATH, "a", encoding="utf-8") as f:
                f.write(f"{tanggal}|{nama_file}|{deskripsi.strip()}\n")

            st.success("✔️ Kegiatan berhasil disimpan.")
        else:
            st.error("⚠️ Gambar dan deskripsi harus diisi!")

    st.markdown("---")
    st.subheader("📂 Riwayat Kegiatan")

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in reversed(lines):
            try:
                tanggal, gambar, deskripsi = line.strip().split("|", 2)
                path_gambar = os.path.join(FOLDER_GAMBAR, gambar)
                if os.path.exists(path_gambar):
                    cols = st.columns([1, 4])
                    with cols[0]:
                        st.image(path_gambar, width=120)
                    with cols[1]:
                        st.markdown(f"**{tanggal}**")
                        st.write(deskripsi)
                        if st.button(f"🗑 Hapus - {gambar}"):
                            hapus_kegiatan(line, path_gambar)
                            st.rerun()
            except:
                continue
    else:
        st.info("Belum ada kegiatan yang tercatat.")
