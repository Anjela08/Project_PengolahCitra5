import tkinter as tk
import subprocess

def buka_absensi():
    subprocess.Popen(["python", "absensi.py"])

def buka_profil():
    subprocess.Popen(["python", "profil.py"])

def buka_kegiatan():
    subprocess.Popen(["python", "kegiatan.py"])

def buka_informasi():
    subprocess.Popen(["python", "informasi.py"])

def keluar():
    root.destroy()

# GUI Launcher
root = tk.Tk()
root.title("Dashboard Aplikasi Absensi")
root.geometry("400x400")
root.configure(bg="lightblue")

tk.Label(root, text="📋 Menu Utama", font=("Arial", 18), bg="lightblue").pack(pady=20)

tk.Button(root, text="📅 Absensi", width=30, command=buka_absensi).pack(pady=5)
tk.Button(root, text="👤 Profil", width=30, command=buka_profil).pack(pady=5)
tk.Button(root, text="📸 Kegiatan", width=30, command=buka_kegiatan).pack(pady=5)
tk.Button(root, text="📰 Informasi", width=30, command=buka_informasi).pack(pady=5)

tk.Button(root, text="🚪 Keluar", width=30, bg="red", fg="white", command=keluar).pack(pady=20)

root.mainloop()
