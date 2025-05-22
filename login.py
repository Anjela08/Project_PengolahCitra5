# login.py
import tkinter as tk
from tkinter import messagebox
import dashboard

def validasi_login(username, password):
    try:
        with open("data/akun.txt", "r") as file:
            for baris in file:
                user, pw = baris.strip().split(",")
                if username == user and password == pw:
                    return True
    except FileNotFoundError:
        messagebox.showerror("Error", "File akun tidak ditemukan.")
    return False

def tampilkan_login():
    window = tk.Tk()
    window.title("Login")
    window.geometry("300x200")

    tk.Label(window, text="Username").pack(pady=5)
    entry_username = tk.Entry(window)
    entry_username.pack()

    tk.Label(window, text="Password").pack(pady=5)
    entry_password = tk.Entry(window, show="*")
    entry_password.pack()

    def proses_login():
        user = entry_username.get()
        pw = entry_password.get()
        if validasi_login(user, pw):
            window.destroy()
            dashboard.tampilkan_dashboard(user)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    tk.Button(window, text="Login", command=proses_login).pack(pady=20)

    window.mainloop()
