import tkinter as tk
from tkinter import filedialog
import re
import getpass
from cryptography.fernet import Fernet
import base64
import hashlib
import os


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select file to encrypt/decrypt"
    )
    return file_path


def get_password_type():
    print("Choose password type:")
    print("1. Alphabetic")
    print("2. Numeric")
    print("3. Alphanumeric")
    while True:
        option = input("Enter option (1/2/3): ").strip()
        if option in ["1", "2", "3"]:
            return option
        print("Invalid option. Try again.")


def get_password(option):
    while True:
        pwd = getpass.getpass("Enter password: ")
        if option == "1" and re.fullmatch(r"[A-Za-z]+", pwd):
            return pwd
        elif option == "2" and re.fullmatch(r"\d+", pwd):
            return pwd
        elif option == "3" and re.fullmatch(r"[A-Za-z0-9]+", pwd):
            return pwd
        print("Invalid password format. Try again.")


def derive_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    out_path = file_path + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted)
    print(f"File encrypted: {out_path}")


def decrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)
    except Exception:
        print("Decryption failed. Wrong password or corrupted file.")
        return
    out_path = file_path.replace(".enc", ".dec")
    with open(out_path, "wb") as f:
        f.write(decrypted)
    print(f"File decrypted: {out_path}")


def main():
    print("Choose action:")
    print("1. Encrypt")
    print("2. Decrypt")
    action = input("Enter option (1/2): ").strip()
    if action not in ["1", "2"]:
        print("Invalid action.")
        return
    file_path = select_file()
    if not file_path:
        print("No file selected.")
        return
    pwd_type = get_password_type()
    password = get_password(pwd_type)
    key = derive_key(password)
    if action == "1":
        encrypt_file(file_path, key)
    else:
        decrypt_file(file_path, key)


if __name__ == "__main__":
    main()
