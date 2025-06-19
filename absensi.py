import streamlit as st
from datetime import datetime
import face_recognition
import cv2
import pickle
import sqlite3
import os
import numpy as np
import pandas as pd

DB_FILE = "absensi.db"
ENCODINGS_FILE = "encodings.pkl"

# ------------------- Inisialisasi DB -------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            tanggal TEXT,
            waktu TEXT
        )
    """)
    conn.commit()
    return conn

# ------------------- Cek Sudah Absen Hari Ini -------------------
def sudah_absen_hari_ini(conn, username):
    today = datetime.now().strftime("%Y-%m-%d")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM absensi WHERE username=? AND tanggal=?", (username, today))
    return cursor.fetchone() is not None

# ------------------- Simpan Absensi -------------------
def simpan_absensi(conn, username):
    now = datetime.now()
    tanggal = now.strftime("%Y-%m-%d")
    waktu = now.strftime("%H:%M:%S")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO absensi (username, tanggal, waktu) VALUES (?, ?, ?)", (username, tanggal, waktu))
    conn.commit()

# ------------------- Scan Wajah Otomatis -------------------
def scan_wajah_otomatis():
    if not os.path.exists(ENCODINGS_FILE):
        return "❌ Data wajah belum tersedia."

    with open(ENCODINGS_FILE, "rb") as f:
        known_encodings = pickle.load(f)

    if not known_encodings:
        return "❌ Tidak ada data wajah yang terdaftar."

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "❌ Kamera tidak dapat diakses."

    stframe = st.empty()
    result = "❌ Gagal mendeteksi wajah."
    conn = init_db()
    detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            result = "❌ Gagal mengambil frame dari kamera."
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(list(known_encodings.values()), face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(list(known_encodings.values()), face_encoding)

            if True in matches:
                best_match_index = np.argmin(face_distances)
                username = list(known_encodings.keys())[best_match_index].strip()

                if not sudah_absen_hari_ini(conn, username):
                    simpan_absensi(conn, username)
                    result = f"✅ Absensi berhasil untuk {username}"
                else:
                    result = f"ℹ️ {username} sudah absen hari ini."

                st.session_state["username"] = username

                # Gambar kotak
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, username, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                stframe.image(frame, channels="BGR")
                detected = True
                break

        stframe.image(frame, channels="BGR")

        if detected:
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()
    return result

# ------------------- Tampilkan Riwayat Absensi Per User -------------------
def tampilkan_riwayat_user(username):
    st.subheader(f"👤 Pengguna: {username}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tanggal, MIN(waktu) as masuk, MAX(waktu) as pulang
        FROM absensi
        WHERE username=?
        GROUP BY tanggal
        ORDER BY tanggal DESC
    """, (username,))
    data = cursor.fetchall()
    conn.close()

    records = []
    for tanggal, masuk, pulang in data:
        tgl = tanggal.split("-")[-1]  # Ambil hari (DD)
        if masuk == pulang:
            pulang = "00:00:00"
        records.append({"TGL": tgl, "MASUK": masuk, "PULANG": pulang})

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)

# ------------------- Tampilan Utama -------------------
def tampilkan_absensi():
    st.title("📸 Absensi Face ID")

    # USER
    if st.session_state.get("role") != "admin":
        if st.button("✅ Mulai Absensi"):
            status = scan_wajah_otomatis()
            if status.startswith("✅"):
                st.success(status)
            elif status.startswith("ℹ️"):
                st.info(status)
            else:
                st.warning(status)

        if "username" in st.session_state:
            st.markdown("### 📜 Riwayat Absensi")
            tampilkan_riwayat_user(st.session_state["username"])
        else:
            st.markdown("👉 Lakukan absensi untuk melihat riwayat.")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.success("Berhasil logout.")

    # ADMIN
    else:
        tab1, tab2, tab3 = st.tabs(["📆 Hari Ini", "📈 Rekap Mingguan/Bulanan", "📥 Unduh Rekapan"])

        # Tab 1: Siapa saja yang absen hari ini
        with tab1:
            st.subheader("📆 Daftar Absensi Hari Ini")
            conn = sqlite3.connect(DB_FILE)
            today = datetime.now().strftime("%Y-%m-%d")
            df_today = pd.read_sql_query(
                "SELECT username, waktu FROM absensi WHERE tanggal = ?", conn, params=(today,)
            )
            conn.close()
            if df_today.empty:
                st.info("Belum ada yang absen hari ini.")
            else:
                st.dataframe(df_today, use_container_width=True)

        # Tab 2: Rekap mingguan / bulanan
        with tab2:
            st.subheader("📊 Rekap Absensi")
            conn = sqlite3.connect(DB_FILE)
            df_all = pd.read_sql_query("SELECT username, tanggal, waktu FROM absensi", conn)
            conn.close()

            if df_all.empty:
                st.info("Belum ada data absensi.")
            else:
                df_all["tanggal"] = pd.to_datetime(df_all["tanggal"])

                pilihan = st.radio("Lihat Berdasarkan:", ["Mingguan", "Bulanan"])
                if pilihan == "Mingguan":
                    df_all["minggu"] = df_all["tanggal"].dt.isocalendar().week
                    df_all["tahun"] = df_all["tanggal"].dt.year
                    df_grouped = df_all.groupby(["tahun", "minggu", "username"]).agg(
                        masuk=("waktu", "min"), pulang=("waktu", "max")).reset_index()
                else:
                    df_all["bulan"] = df_all["tanggal"].dt.month
                    df_all["tahun"] = df_all["tanggal"].dt.year
                    df_grouped = df_all.groupby(["tahun", "bulan", "username"]).agg(
                        masuk=("waktu", "min"), pulang=("waktu", "max")).reset_index()

                st.dataframe(df_grouped, use_container_width=True)

        # Tab 3: Unduh CSV
        with tab3:
            st.subheader("📥 Unduh Rekapan Absensi")
            conn = sqlite3.connect(DB_FILE)
            df_export = pd.read_sql_query("SELECT * FROM absensi", conn)
            conn.close()

            if not df_export.empty:
                csv = df_export.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", csv, "rekap_absensi.csv", "text/csv")
            else:
                st.info("Belum ada data untuk diunduh.")
