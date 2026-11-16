import json
import os
import hashlib
import base64
import getpass
from cryptography.fernet import Fernet

DATA_FILE = "vault.json"
KEY_FILE = "key.key"

def get_key(master_password):
    # Master password se key banayein
    hashed = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def load_vault(cipher):
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "rb") as f:
        encrypted_data = f.read()
        if not encrypted_data:
            return []
        try:
            decrypted = cipher.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except:
            print("\n[!] Wrong Master Password or Corrupted Vault!")
            exit()

def save_vault(cipher, data):
    encrypted = cipher.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)

def main():
    print("="*50)
    print("   SYNTECXHUB - Secure Password Manager")
    print("   Encrypted Local Storage | AES Encryption")
    print("="*50)
    master = getpass.getpass("Enter Master Password: ")
    key = get_key(master)
    cipher = Fernet(key)

    vault = load_vault(cipher)
    print(f"\n[+] Vault Unlocked! Total Entries: {len(vault)}")

    while True:
        print("\n--- MENU ---")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Search Entry")
        print("4. Delete Entry")
        print("5. Show All Sites")
        print("6. Exit")
        choice = input("Choose (1-6): ")

        if choice == "1":
            site = input("Website/App: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            vault.append({"site": site, "username": username, "password": password})
            save_vault(cipher, vault)
            print("[+] Entry Added & Encrypted Successfully!")

        elif choice == "2":
            site = input("Enter Website to Retrieve: ")
            found = False
            for entry in vault:
                if entry["site"].lower() == site.lower():
                    print(f"\nSite: {entry['site']}")
                    print(f"Username: {entry['username']}")
                    print(f"Password: {entry['password']}")
                    found = True
            if not found:
                print("[-] Not Found!")

        elif choice == "3":
            keyword = input("Search Keyword: ")
            for entry in vault:
                if keyword.lower() in entry["site"].lower():
                    print(f"Found -> {entry['site']} | User: {entry['username']}")

        elif choice == "4":
            site = input("Enter Website to Delete: ")
            new_vault = [e for e in vault if e["site"].lower() != site.lower()]
            if len(new_vault) != len(vault):
                vault = new_vault
                save_vault(cipher, vault)
                print("[+] Deleted Successfully!")
            else:
                print("[-] Not Found!")

        elif choice == "5":
            print("\n--- All Saved Sites ---")
            for entry in vault:
                print(f"- {entry['site']} | {entry['username']}")

        elif choice == "6":
            print("Vault Locked. Goodbye!")
            break
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()
