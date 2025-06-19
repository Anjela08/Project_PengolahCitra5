# ========================== FILE: utils.py ==========================
import os

DATA_USER = "data/users.txt"

# Contoh format users.txt:
# username1|password1
# username2|password2

def validasi_user(username, password):
    if not os.path.exists(DATA_USER):
        return False
    with open(DATA_USER, "r", encoding="utf-8") as f:
        for line in f:
            try:
                u, p = line.strip().split("|")
                if u == username and p == password:
                    return True
            except:
                continue
    return False
