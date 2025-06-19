import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

# Path dan konfigurasi awal
DATA_PATH = "data/profil.txt"
PHOTO_PATH = "images/foto_pengguna.png"
DEFAULT_PHOTO = "images/default_photo.png"

# Buat folder jika belum ada
os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Buat foto default jika belum ada
if not os.path.exists(DEFAULT_PHOTO):
    img = Image.new("RGB", (150, 150), color=(180, 200, 240))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = "No Photo"
    w, h = draw.textsize(text, font=font)
    draw.text(((150 - w) / 2, (150 - h) / 2), text, fill=(0, 0, 0), font=font)
    img.save(DEFAULT_PHOTO)

def tampilkan_profil():
    st.title("Profil Pengguna")

    # Status simpan
    status = st.empty()

    # Foto pengguna
    col1, col2 = st.columns([1, 2])
    with col1:
        foto_path = PHOTO_PATH if os.path.exists(PHOTO_PATH) else DEFAULT_PHOTO
        st.image(foto_path, width=150)
        uploaded_file = st.file_uploader("📸 Upload Foto", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                img = Image.open(uploaded_file).resize((150, 150))
                img.save(PHOTO_PATH)
                status.success("✅ Foto berhasil di-upload")
            except Exception as e:
                status.error(f"❌ Gagal memuat foto: {str(e)}")

    # Load data profil jika ada
    profil_data = {}
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            for line in file:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    profil_data[key] = value.strip()

    def input_field(label):
        return st.text_input(label, profil_data.get(label, ""))

    # Section: Informasi Pribadi
    st.subheader("1. Informasi Pribadi")
    nama = input_field("Nama Lengkap")
    ttl = input_field("Tempat, Tanggal Lahir")
    jk = input_field("Jenis Kelamin")
    alamat = input_field("Alamat")
    telepon = input_field("Nomor Telepon")
    email = input_field("Email")
    status_perkawinan = input_field("Status Perkawinan")
    kewarganegaraan = input_field("Kewarganegaraan")

    # Section: Pekerjaan
    st.subheader("2. Informasi Pekerjaan")
    jabatan = input_field("Jabatan")
    divisi = input_field("Departemen / Divisi")
    nik = input_field("Nomor Induk Karyawan (NIK)")
    tgl_masuk = input_field("Tanggal Masuk Kerja")
    status_karyawan = input_field("Status Karyawan")
    lokasi = input_field("Lokasi")

    # Section: Pendidikan
    st.subheader("3. Pendidikan")
    jenjang = input_field("Jenjang Pendidikan Terakhir")
    institusi = input_field("Nama Institusi")
    jurusan = input_field("Jurusan")
    lulus = input_field("Tahun Lulus")

    # Section: Pengalaman Kerja
    st.subheader("4. Pengalaman Kerja (jika ada)")
    perusahaan = input_field("Nama Perusahaan")
    jabatan_kerja = input_field("Jabatan (Pengalaman)")
    lama = input_field("Lama Bekerja")
    deskripsi = input_field("Deskripsi Pekerjaan")

    # Section: Keahlian
    st.subheader("5. Keterampilan / Keahlian")
    bahasa = input_field("Bahasa yang Dikuasai")
    keahlian = input_field("Keahlian Teknis")

    if st.button("💾 Simpan Data"):
        try:
            with open(DATA_PATH, "w", encoding="utf-8") as file:
                file.write(f"Nama Lengkap: {nama}\n")
                file.write(f"Tempat, Tanggal Lahir: {ttl}\n")
                file.write(f"Jenis Kelamin: {jk}\n")
                file.write(f"Alamat: {alamat}\n")
                file.write(f"Nomor Telepon: {telepon}\n")
                file.write(f"Email: {email}\n")
                file.write(f"Status Perkawinan: {status_perkawinan}\n")
                file.write(f"Kewarganegaraan: {kewarganegaraan}\n")
                file.write(f"Jabatan: {jabatan}\n")
                file.write(f"Departemen / Divisi: {divisi}\n")
                file.write(f"Nomor Induk Karyawan (NIK): {nik}\n")
                file.write(f"Tanggal Masuk Kerja: {tgl_masuk}\n")
                file.write(f"Status Karyawan: {status_karyawan}\n")
                file.write(f"Lokasi: {lokasi}\n")
                file.write(f"Jenjang Pendidikan Terakhir: {jenjang}\n")
                file.write(f"Nama Institusi: {institusi}\n")
                file.write(f"Jurusan: {jurusan}\n")
                file.write(f"Tahun Lulus: {lulus}\n")
                file.write(f"Nama Perusahaan: {perusahaan}\n")
                file.write(f"Jabatan (Pengalaman): {jabatan_kerja}\n")
                file.write(f"Lama Bekerja: {lama}\n")
                file.write(f"Deskripsi Pekerjaan: {deskripsi}\n")
                file.write(f"Bahasa yang Dikuasai: {bahasa}\n")
                file.write(f"Keahlian Teknis: {keahlian}\n")
                file.write(f"Foto: {PHOTO_PATH if os.path.exists(PHOTO_PATH) else DEFAULT_PHOTO}\n")
            status.success("✅ Data berhasil disimpan")
        except Exception as e:
            status.error(f"❌ Gagal menyimpan data: {str(e)}")
