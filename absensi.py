import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import cv2

# Path file dan Haar Cascade
DATA_ABSEN_PATH = "data/absensi.txt"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fungsi Check-in Manual
def check_in_manual(status_label):
    now = datetime.now()
    with open(DATA_ABSEN_PATH, "a") as file:
        file.write(f"{now.strftime('%Y-%m-%d')},{now.strftime('%H:%M:%S')},Manual\n")
    status_label.config(text="✅ Anda sudah Check-in Manual")

# Fungsi Check-in Face ID
def check_in_faceid(status_label):
    cap = cv2.VideoCapture(0)
    success = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Gambar kotak di wajah
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            success = True

        cv2.imshow('Deteksi Wajah - Tekan Q untuk Check-in', frame)

        # Tekan Q untuk keluar dan simpan absensi
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if success:
        now = datetime.now()
        with open(DATA_ABSEN_PATH, "a") as file:
            file.write(f"{now.strftime('%Y-%m-%d')},{now.strftime('%H:%M:%S')},FaceID\n")
        status_label.config(text="✅ Anda sudah Check-in dengan Face ID")
        messagebox.showinfo("Berhasil", "Check-in dengan Face ID berhasil!")
    else:
        messagebox.showwarning("Gagal", "Wajah tidak terdeteksi!")

# Fungsi Lihat Riwayat
def lihat_riwayat():
    if os.path.exists(DATA_ABSEN_PATH):
        with open(DATA_ABSEN_PATH, "r") as file:
            return file.readlines()
    else:
        return ["Belum ada riwayat absensi."]

# Fungsi utama GUI absensi
def tampilkan_absensi():
    root = tk.Tk()
    root.title("Absensi")
    root.geometry("400x450")

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    status_label = tk.Label(frame, text="Status: Belum Check-in", font=("Arial", 12), bg="#f0f0f0")
    status_label.pack(pady=10)

    btn_manual = tk.Button(frame, text="Check-in Manual", command=lambda: check_in_manual(status_label))
    btn_manual.pack(pady=10)

    btn_faceid = tk.Button(frame, text="Check-in Face ID", command=lambda: check_in_faceid(status_label))
    btn_faceid.pack(pady=10)

    def tampilkan_riwayat():
        data = lihat_riwayat()
        riwayat_window = tk.Toplevel(root)
        riwayat_window.title("Riwayat Absensi")
        text_area = tk.Text(riwayat_window, width=50, height=15)
        text_area.pack(padx=10, pady=10)
        for baris in data:
            text_area.insert(tk.END, baris)

    btn_riwayat = tk.Button(frame, text="Lihat Riwayat", command=tampilkan_riwayat)
    btn_riwayat.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    tampilkan_absensi()
