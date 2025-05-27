import tkinter as tk
from dashboard import show_dashboard
from profil import show_profil
from absensi import show_absensi
from kegiatan import show_kegiatan
from informasi import show_informasi

def main():
    root = tk.Tk()
    root.title("Aplikasi Absensi")
    root.geometry("900x600")
    root.configure(bg="white")

    # Frame untuk navigasi samping
    nav_frame = tk.Frame(root, bg="#f0f0f0", width=200)
    nav_frame.pack(side="left", fill="y")

    # Frame untuk konten utama
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side="right", expand=True, fill="both")

    # Fungsi wrapper biar bisa switch halaman
    def tampilkan_dashboard():
        show_dashboard(content_frame)

    def tampilkan_profil():
        show_profil(content_frame)

    def tampilkan_absensi():
        show_absensi(content_frame)

    def tampilkan_kegiatan():
        show_kegiatan(content_frame)

    def tampilkan_informasi():
        show_informasi(content_frame)

    # Tombol navigasi
    tk.Button(nav_frame, text="Dashboard", width=20, command=tampilkan_dashboard).pack(pady=10)
    tk.Button(nav_frame, text="Profil", width=20, command=tampilkan_profil).pack(pady=10)
    tk.Button(nav_frame, text="Absensi", width=20, command=tampilkan_absensi).pack(pady=10)
    tk.Button(nav_frame, text="Kegiatan", width=20, command=tampilkan_kegiatan).pack(pady=10)
    tk.Button(nav_frame, text="Informasi", width=20, command=tampilkan_informasi).pack(pady=10)

    # Tampilkan halaman pertama
    tampilkan_dashboard()

    root.mainloop()

if __name__ == "__main__":
    main()
