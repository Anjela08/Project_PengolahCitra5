import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

DATA_PATH = "data/profil.txt"
PHOTO_PATH = "images/foto_pengguna.png"

def show_profil(root):
    def simpan_data():
        nama = nama_var.get()
        jabatan = jabatan_var.get()
        lokasi = lokasi_var.get()

        with open(DATA_PATH, "w") as file:
            file.write(f"Nama: {nama}\n")
            file.write(f"Jabatan: {jabatan}\n")
            file.write(f"Lokasi: {lokasi}\n")
            file.write(f"Foto: {PHOTO_PATH if os.path.exists(PHOTO_PATH) else ''}\n")

        status_label.config(text="✅ Data berhasil disimpan")

    def upload_foto():
        file_path = filedialog.askopenfilename(title="Pilih Foto", filetypes=[("Image Files", "*.jpg *.png")])
        if file_path:
            image = Image.open(file_path)
            image.save(PHOTO_PATH)
            load_foto()
            status_label.config(text="✅ Foto berhasil di-upload")

    def load_data():
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r") as file:
                for line in file:
                    if line.startswith("Nama:"):
                        nama_var.set(line.split(":", 1)[1].strip())
                    elif line.startswith("Jabatan:"):
                        jabatan_var.set(line.split(":", 1)[1].strip())
                    elif line.startswith("Lokasi:"):
                        lokasi_var.set(line.split(":", 1)[1].strip())
        load_foto()

    def load_foto():
        try:
            img = Image.open(PHOTO_PATH).resize((150, 150))
        except:
            img = Image.open("images/default_photo.png").resize((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        foto_label.config(image=img_tk)
        foto_label.image = img_tk  # biar gambar ga kehapus

    # Hapus tampilan sebelumnya
    for widget in root.winfo_children():
        widget.destroy()

    nama_var = tk.StringVar()
    jabatan_var = tk.StringVar()
    lokasi_var = tk.StringVar()

    tk.Label(root, text="Profil", font=("Arial", 20), bg="white").pack(pady=10)

    foto_label = tk.Label(root, bg="white")
    foto_label.pack(pady=10)

    tk.Button(root, text="Upload Foto", command=upload_foto).pack()

    tk.Label(root, text="Nama", bg="white").pack(pady=5)
    tk.Entry(root, textvariable=nama_var).pack()

    tk.Label(root, text="Jabatan", bg="white").pack(pady=5)
    tk.Entry(root, textvariable=jabatan_var).pack()

    tk.Label(root, text="Lokasi", bg="white").pack(pady=5)
    tk.Entry(root, textvariable=lokasi_var).pack()

    tk.Button(root, text="Simpan Data", command=simpan_data).pack(pady=20)

    status_label = tk.Label(root, text="", bg="white", fg="green")
    status_label.pack()

    load_data()
