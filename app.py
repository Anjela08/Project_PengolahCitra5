import streamlit as st
st.set_page_config(page_title="CV DESAIN KREASI SUPLIER", layout="wide")  # WAJIB PALING ATAS

import dashboard
import absensi
import profil
import kegiatan
import informasi
import auth

# ------------------- Login Multi-User ------------------- #
if "user" not in st.session_state or "role" not in st.session_state:
    auth.tampilkan_auth()
else:
    st.sidebar.title(f"👤 {st.session_state['user']} | CV DESAIN KREASI SUPLIER")

    # Menu navigasi
    menu = st.sidebar.radio("📁 Navigasi", [
        "Dashboard", "Absensi", "Profil", "Kegiatan", "Informasi", "Logout"])

    if menu == "Dashboard":
        dashboard.tampilkan_dashboard()
    elif menu == "Absensi":
        absensi.tampilkan_absensi()
    elif menu == "Profil":
        profil.tampilkan_profil()
    elif menu == "Kegiatan":
        kegiatan.tampilkan_kegiatan()
    elif menu == "Informasi":
        informasi.tampilkan_informasi()
    elif menu == "Logout":
        # Bersihkan session state tanpa rerun
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.stop()
