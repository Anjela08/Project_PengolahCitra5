import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os

DATA_PATH = "data/kegiatan.txt"
FOLDER_GAMBAR = "images/kegiatan/"

# Pastikan folder kegiatan ada
os.makedirs(FOLDER_GAMBAR, exist_ok=True)

def show_kegiatan(root):
    # hapus tampilan sebelumnya
    for widget in root.winfo_children():
        widget.destroy()



def upload_gambar():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        nama_file = os.path.basename(file_path)
        simpan_path = os.path.join(FOLDER_GAMBAR, nama_file)
        with open(file_path, "rb") as src, open(simpan_path, "wb") as dst:
            dst.write(src.read())
        gambar_var.set(nama_file)
        preview_gambar(simpan_path)


def preview_gambar(path):
    img = Image.open(path).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    gambar_label.config(image=img_tk)
    gambar_label.image = img_tk


def simpan_kegiatan():
    tanggal = datetime.now().strftime("%Y-%m-%d")
    gambar = gambar_var.get()
    deskripsi = deskripsi_entry.get("1.0", "end").strip()

    if not gambar or not deskripsi:
        messagebox.showerror("Error", "Gambar dan deskripsi harus diisi!")
        return

    with open(DATA_PATH, "a") as file:
        file.write(f"{tanggal}|{gambar}|{deskripsi}\n")
    messagebox.showinfo("Berhasil", "✅ Kegiatan disimpan.")
    deskripsi_entry.delete("1.0", "end")
    gambar_var.set("")
    gambar_label.config(image="")


# GUI
root = tk.Tk()
root.title("Kegiatan")
root.geometry("500x600")
root.configure(bg="white")

tk.Label(root, text="Upload Kegiatan", font=("Arial", 18), bg="white").pack(pady=10)

gambar_var = tk.StringVar()

gambar_label = tk.Label(root, bg="white")
gambar_label.pack()

tk.Button(root, text="Upload Gambar", command=upload_gambar).pack(pady=10)

tk.Label(root, text="Deskripsi Kegiatan:", bg="white").pack()
deskripsi_entry = tk.Text(root, height=5, width=50)
deskripsi_entry.pack(pady=5)

tk.Button(root, text="Simpan", command=simpan_kegiatan, bg="lightgreen").pack(pady=20)


root.mainloop()
