import streamlit as st
import sqlite3
import os
import face_recognition
import pickle

# === Konstanta path ===
DB_PATH = "users.db"
FACES_DIR = "faces"
ENCODINGS_FILE = "encodings.pkl"

# === Pastikan folder wajah ada ===
os.makedirs(FACES_DIR, exist_ok=True)

# === Buat tabel user jika belum ada ===
def create_user_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        face_image TEXT
    )''')
    conn.commit()
    conn.close()

# === Simpan user baru ===
def tambah_user(username, password, face_filename):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, face_image) VALUES (?, ?, ?)",
                  (username, password, face_filename))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# === Cek login ===
def cek_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

# === Simpan gambar wajah ke folder ===
def simpan_gambar_wajah(username, gambar):
    filepath = os.path.join(FACES_DIR, f"{username}.jpg")
    with open(filepath, "wb") as f:
        f.write(gambar.getbuffer())
    return os.path.basename(filepath)

# === Simpan encoding wajah ke file pickle ===
def simpan_encoding_wajah(username, path_gambar):
    image = face_recognition.load_image_file(path_gambar)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return False

    encoding = encodings[0]

    # Muat encoding sebelumnya jika ada
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
    else:
        data = {}

    data[username] = encoding

    # Simpan kembali encoding
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    return True

# ======================== HALAMAN LOGIN & REGISTER ======================== #
def tampilkan_auth():
    create_user_table()
    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if menu == "Login":
        st.title("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Masuk"):
            if username == "admin" and password == "admin123":
                st.session_state["user"] = "admin"
                st.session_state["role"] = "admin"
                st.success("Login sebagai Admin 👑")
                st.stop()
            else:
                user = cek_login(username, password)
                if user:
                    st.session_state["user"] = username
                    st.session_state["role"] = "user"
                    st.success(f"Selamat datang, {username} 👋")
                    st.stop()
                else:
                    st.error("❌ Username atau password salah!")

    elif menu == "Register":
        st.title("📝 Registrasi Pengguna")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        gambar_wajah = st.camera_input("Ambil Foto Wajah")

        if st.button("Daftar"):
            if not username or not password or not gambar_wajah:
                st.warning("⚠️ Semua kolom wajib diisi dan foto wajib diambil.")
            else:
                nama_file = simpan_gambar_wajah(username, gambar_wajah)
                path_lengkap = os.path.join(FACES_DIR, nama_file)

                if tambah_user(username, password, nama_file):
                    if simpan_encoding_wajah(username, path_lengkap):
                        st.success("✅ Registrasi & penyimpanan wajah berhasil. Silakan login.")
                    else:
                        st.warning("Registrasi berhasil, tapi wajah tidak bisa dikenali.")
                else:
                    st.error("❌ Username sudah terdaftar.")
