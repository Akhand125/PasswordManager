from cryptography.fernet import Fernet
import os
import base64
import hashlib

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():

    return open("key.key", "rb").read()


if not os.path.exists("key.key"):
    write_key()


master_pwd = input("What is the master password? ")


key = load_key()


hashed_master_pwd = hashlib.sha256(master_pwd.encode()).digest()


combined_key = base64.urlsafe_b64encode(hashed_master_pwd[:16] + key[:16])
fer = Fernet(combined_key)

def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print("User: ", user, "| Password: ", fer.decrypt(passw.encode()).decode())
    except FileNotFoundError:
        print("No passwords file found. Please add some passwords first.")
    except Exception as e:
        print(f"An error occurred: {e}")

def add():
    name = input('Account Name: ')
    pwd = input("Password: ")

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue
