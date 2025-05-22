import tkinter as tk
import os
from PIL import Image, ImageTk
from typing import Any

photo: Any = ImageTk


# Lokasi file data dan foto
DATA_PATH = "data/profil.txt"
PHOTO_PATH = "images/foto_pengguna.png"
DEFAULT_PHOTO = "images/default_photo.png"

# Fungsi baca profil dengan format key-value
def baca_profil():
    profil = {}
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            for baris in f:
                if ": " in baris:
                    key, value = baris.strip().split(": ", 1)
                    profil[key] = value
    return profil

# Fungsi buka file lain
def buka_file(nama_file):
    os.system(f"python {nama_file}")

# Fungsi untuk menampilkan dashboard
def tampilkan_dashboard():
    profil = baca_profil()

    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("800x600")

    # ===== HEADER =====
    tk.Label(root, text="CV. DESAIN KREASI SUPPLIER", font=("Arial", 18, "bold"), fg="purple").pack(pady=10)
    tk.Label(root, text="GENERAL SUPPLIER, HEAVY EQUIPMENT, MANPOWER SUPPLY, RENTAL SCAFFOLDING", font=("Arial", 10)).pack()
    tk.Label(root, text="ABSENSI", font=("Arial", 14, "bold")).pack(pady=10)

    # ===== PROFIL KOTAK =====
    frame = tk.Frame(root, bg="#1e3a5f", padx=20, pady=20)
    frame.pack(pady=10)

    try:
        image = Image.open(profil.get("Foto", DEFAULT_PHOTO)).resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        label_foto = tk.Label(frame, image=photo)
        label_foto.image = photo
        label_foto.grid(row=0, column=0, rowspan=3, padx=10)
    except:
        label_foto = tk.Label(frame, text="No Image", bg="#ccc", width=12, height=6)
        label_foto.grid(row=0, column=0, rowspan=3, padx=10)

    tk.Label(frame, text=profil.get("Nama", "Belum diisi"), font=("Arial", 14, "bold"), fg="white", bg="#1e3a5f").grid(row=0, column=1, sticky="w")
    tk.Label(frame, text=profil.get("Jabatan", "Belum diisi"), font=("Arial", 10), fg="white", bg="#1e3a5f").grid(row=1, column=1, sticky="w")
    tk.Label(frame, text=profil.get("Lokasi", "Belum diisi"), font=("Arial", 10), fg="white", bg="#1e3a5f").grid(row=2, column=1, sticky="w")

    # ===== MENU =====
    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=20)

    def buat_menu(icon_path, label, command):
        icon = Image.open(icon_path).resize((64, 64))
        icon_tk = ImageTk.PhotoImage(icon)
        btn_frame = tk.Frame(menu_frame)
        btn_frame.pack(side="left", padx=20)

        btn = tk.Button(btn_frame, image=icon_tk, command=command, bd=0)
        btn.image = icon_tk  # agar gambar tidak hilang
        btn.pack()

        tk.Label(btn_frame, text=label).pack()

    # Buat tombol menu
    buat_menu("images/absensi_icon.png", "Absensi", lambda: buka_file("absensi.py"))
    buat_menu("images/profil_icon.png", "Profil", lambda: buka_file("profil.py"))
    buat_menu("images/kegiatan_icon.png", "Kegiatan", lambda: buka_file("kegiatan.py"))
    buat_menu("images/informasi_icon.png", "Informasi", lambda: buka_file("informasi.py"))

    root.mainloop()

# Jalankan hanya jika file ini langsung dijalankan
if __name__ == "__main__":
    tampilkan_dashboard()
