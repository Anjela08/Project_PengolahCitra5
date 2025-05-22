import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

DATA_FILE = "data/informasi.txt"


def simpan_berita():
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
    isi = berita_entry.get("1.0", "end").strip()

    if not isi:
        messagebox.showerror("Error", "Berita tidak boleh kosong!")
        return

    with open(DATA_FILE, "a") as file:
        file.write(f"{tanggal} | {isi}\n")

    berita_entry.delete("1.0", "end")
    tampilkan_berita()
    messagebox.showinfo("Berhasil", "Berita disimpan!")


def tampilkan_berita():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            semua_berita = file.read()
        berita_text.config(state="normal")
        berita_text.delete("1.0", "end")
        berita_text.insert("1.0", semua_berita)
        berita_text.config(state="disabled")
    else:
        berita_text.insert("1.0", "Belum ada berita.")


# GUI
root = tk.Tk()
root.title("Informasi Penting")
root.geometry("600x600")
root.configure(bg="white")

tk.Label(root, text="Tambah Berita Penting", font=("Arial", 18), bg="white").pack(pady=10)

berita_entry = tk.Text(root, height=5, width=60)
berita_entry.pack(pady=10)

tk.Button(root, text="Simpan Berita", command=simpan_berita, bg="lightblue").pack(pady=5)

tk.Label(root, text="📢 Semua Berita:", font=("Arial", 14), bg="white").pack(pady=10)

berita_text = tk.Text(root, height=20, width=70, state="disabled", bg="#f9f9f9")
berita_text.pack(pady=5)

tampilkan_berita()

root.mainloop()
