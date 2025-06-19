import streamlit as st
from PIL import Image
import os
import absensi

DATA_PATH = "data/profil.txt"
DEFAULT_PHOTO = "images/default_photo.png"

def baca_profil():
    profil_data = {}
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            for baris in f:
                if ": " in baris:
                    key, value = baris.strip().split(": ", 1)
                    profil_data[key] = value
    return profil_data

def tampilkan_dashboard():
    profil_data = baca_profil()

    # Logo perusahaan diperbesar otomatis
    st.image("images/Logo.png", use_container_width=True)
    st.divider()

    # Profil pengguna
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            image_path = profil_data.get("Foto", DEFAULT_PHOTO)
            img = Image.open(image_path)
            st.image(img, width=120)
        except:
            st.warning("Foto tidak tersedia.")
    with col2:
        with st.container():
            st.subheader(profil_data.get('Nama Lengkap', 'Belum diisi'))
            st.write("**Jabatan:**", profil_data.get('Jabatan', 'Belum diisi'))
            st.write("**Lokasi:**", profil_data.get('Lokasi', 'Belum diisi'))

    st.divider()

    # Menu interaktif
    st.subheader("Menu Utama")
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        st.image("images/absensi_icon.png", width=60)
        if st.button("Absensi"):
            import absensi
            absensi.tampilkan_absensi()

    with col4:
        st.image("images/profil_icon.png", width=60)
        if st.button("Profil"):
            import profil
            profil.tampilkan_profil()

    with col5:
        st.image("images/kegiatan_icon.png", width=60)
        if st.button("Kegiatan"):
            import kegiatan
            kegiatan.tampilkan_kegiatan()

    with col6:
        st.image("images/informasi_icon.png", width=60)
        if st.button("Informasi"):
            import informasi
            informasi.tampilkan_informasi()

    st.divider()
    st.button("🚪 Logout")
