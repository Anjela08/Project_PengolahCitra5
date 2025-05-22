import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os
import cv2

# Load Haar Cascade buat deteksi wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def check_in_manual():
    now = datetime.now()
    with open("data/absensi.txt", "a") as file:
        file.write(f"{now.strftime('%Y-%m-%d')},{now.strftime('%H:%M:%S')},Manual\n")
    status_label.config(text="✅ Anda sudah Check-in Manual")

def lihat_riwayat():
    if os.path.exists("data/absensi.txt"):
        with open("data/absensi.txt", "r") as file:
            data = file.read()
        riwayat = tk.Toplevel(root)
        riwayat.title("Riwayat Absen")
        tk.Label(riwayat, text=data).pack()
    else:
        status_label.config(text="❌ Belum ada data absensi.")

def registrasi_wajah():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            nama_file = filedialog.asksaveasfilename(initialdir="faces", defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
            if nama_file:
                cv2.imwrite(nama_file, frame)
                status_label.config(text="✅ Wajah berhasil diregistrasi.")
        else:
            status_label.config(text="❌ Tidak ada wajah terdeteksi.")
    else:
        status_label.config(text="❌ Kamera gagal terbuka.")
    cam.release()
    cv2.destroyAllWindows()

def check_in_face_id():
    # Ambil wajah dari webcam
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        status_label.config(text="❌ Gagal membuka kamera.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        # Misal kita anggap berhasil karena ada wajah terdeteksi
        now = datetime.now()
        with open("data/absensi.txt", "a") as file:
            file.write(f"{now.strftime('%Y-%m-%d')},{now.strftime('%H:%M:%S')},FaceID\n")
        status_label.config(text="✅ Check-in Face ID berhasil.")
        cv2.imshow("Wajah Terdeteksi", frame)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    else:
        status_label.config(text="❌ Tidak ditemukan wajah.")
        cv2.imshow("Tidak Ada Wajah", frame)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

def logout():
    root.destroy()
    import main
    main.tampilkan_login()  # pastikan login kamu pakai fungsi ini

# GUI
root = tk.Tk()
root.title("Menu Absensi")
root.geometry("800x500")
root.configure(bg="lightblue")

hari = datetime.now().strftime("%A, %d %B %Y")
jam = datetime.now().strftime("%H:%M")

tk.Label(root, text=f"{hari} | {jam}", font=("Helvetica", 16), bg="lightblue").pack(pady=10)

tk.Button(root, text="✅ Check-in Manual", width=30, command=check_in_manual).pack(pady=5)
tk.Button(root, text="👤 Registrasi Wajah", width=30, command=registrasi_wajah).pack(pady=5)
tk.Button(root, text="🤳 Check-in dengan Face ID", width=30, command=check_in_face_id).pack(pady=5)
tk.Button(root, text="📊 Lihat Riwayat Absen", width=30, command=lihat_riwayat).pack(pady=5)
tk.Button(root, text="🚪 Logout", width=30, command=logout, bg="red", fg="white").pack(pady=10)

status_label = tk.Label(root, text="", font=("Helvetica", 12), bg="lightblue")
status_label.pack(pady=10)

root.mainloop()
