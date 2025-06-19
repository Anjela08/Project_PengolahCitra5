import pickle
import os

ENCODINGS_FILE = "encodings.pkl"

if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
        if data:
            print(f"✅ Jumlah wajah terdaftar: {len(data)}")
            for i, d in enumerate(data):
                print(f"{i+1}. Data: {d}")  # Ganti ke print isi asli d
        else:
            print("❌ Tidak ada data wajah terdaftar.")
else:
    print("❌ File tidak ditemukan.")
