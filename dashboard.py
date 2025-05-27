import tkinter as tk
import os
from PIL import Image, ImageTk

DATA_PATH = "data/profil.txt"
PHOTO_PATH = "images/foto_pengguna.png"
DEFAULT_PHOTO = "images/default_photo.png"

def baca_profil():
    profil = {}
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            for baris in f:
                if ": " in baris:
                    key, value = baris.strip().split(": ", 1)
                    profil[key] = value
    return profil

def show_dashboard(root):
    # Hapus tampilan lama
    for widget in root.winfo_children():
        widget.destroy()

    profil = baca_profil()

    # ===== HEADER =====
    tk.Label(root, text="CV. DESAIN KREASI SUPPLIER", font=("Arial", 18, "bold"), fg="purple", bg="white").pack(pady=10)
    tk.Label(root, text="GENERAL SUPPLIER, HEAVY EQUIPMENT, MANPOWER SUPPLY, RENTAL SCAFFOLDING", font=("Arial", 10), bg="white").pack()
    tk.Label(root, text="ABSENSI", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

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

    # ===== MENU KOSONG (bisa diisi nanti) =====
    tk.Label(root, text="Silakan pilih menu di sebelah kiri", bg="white", font=("Arial", 12)).pack(pady=30)
