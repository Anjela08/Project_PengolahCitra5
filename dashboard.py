import tkinter as tk
from PIL import Image, ImageTk
import os
PHOTO_PATH = "images/foto_pengguna.png"
DEFAULT_PHOTO = "images/default_photo.png"

# ...
# Di bagian tampilan profil:

if os.path.exists(PHOTO_PATH):
    foto_img = Image.open(PHOTO_PATH).resize((100, 100))
else:
    foto_img = Image.open(DEFAULT_PHOTO).resize((100, 100))

foto_tk = ImageTk.PhotoImage(foto_img)
tk.Label( image=foto_tk, bg="#1f3a56").pack(side="left", padx=20)

# Paths
LOGO_PATH = "images/logo.png"
PHOTO_PATH = "images/foto_pengguna.png"
DEFAULT_PHOTO = "images/default_photo.png"
ICONS = {
    "Absensi": "images/absensi_icon.png",
    "Profil": "images/profil_icon.png",
    "Kegiatan": "images/kegiatan_icon.png",
    "Informasi": "images/informasi_icon.png"
}


# Fungsi buka modul (sementara hanya print)
def buka_menu(menu):
    print(f"Membuka {menu}")


# Setup GUI
root = tk.Tk()
root.title("Dashboard Absensi")
root.geometry("800x600")
root.configure(bg="white")

# ================= Header ==================
header_frame = tk.Frame(root, bg="white")
header_frame.pack(pady=10)

logo_img = Image.open(LOGO_PATH).resize((100, 100))
logo_tk = ImageTk.PhotoImage(logo_img)
tk.Label(header_frame, image=logo_tk, bg="white").pack(side="left", padx=10)

tk.Label(header_frame,
         text="CV. DESAIN KREASI SUPPLIER\nGENERAL SUPPLIER, HEAVY EQUIPMENT,\nMANPOWER SUPPLY, RENTAL SCAFFOLDING",
         font=("Arial", 14, "bold"), bg="white", fg="purple", justify="left").pack(side="left")

# ================= Judul ==================
tk.Label(root, text="ABSENSI", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

# ================= Profil ==================
profil_frame = tk.Frame(root, bg="#1f3a56", padx=20, pady=20)
profil_frame.pack(pady=10, fill="x")

# Foto profil
if os.path.exists(PHOTO_PATH):
    foto_img = Image.open(PHOTO_PATH).resize((100, 100))
else:
    foto_img = Image.open(DEFAULT_PHOTO).resize((100, 100))
foto_tk = ImageTk.PhotoImage(foto_img)
tk.Label(profil_frame, image=foto_tk, bg="#1f3a56").pack(side="left", padx=20)

# Data user
tk.Label(profil_frame, text="Prof. Ir. Dr. H. joko widodo", font=("Arial", 14, "bold"),
         fg="white", bg="#1f3a56").pack(anchor="w")
tk.Label(profil_frame, text="Mantan presiden indonesia", font=("Arial", 12),
         fg="white", bg="#1f3a56").pack(anchor="w")
tk.Label(profil_frame, text="Solo, indonesia", font=("Arial", 12),
         fg="white", bg="#1f3a56").pack(anchor="w")

# ================= Menu Icons ==================
menu_frame = tk.Frame(root, bg="white")
menu_frame.pack(pady=30)

for idx, (menu, icon_path) in enumerate(ICONS.items()):
    icon_img = Image.open(icon_path).resize((80, 80))
    icon_tk = ImageTk.PhotoImage(icon_img)


    def make_command(m=menu):
        return lambda: buka_menu(m)


    btn = tk.Button(menu_frame, image=icon_tk, bd=0, command=make_command(), bg="white", activebackground="white")
    btn.image = icon_tk  # simpan referensi
    btn.grid(row=0, column=idx, padx=20)

    tk.Label(menu_frame, text=menu, bg="white", font=("Arial", 10, "bold")).grid(row=1, column=idx)

root.mainloop()
