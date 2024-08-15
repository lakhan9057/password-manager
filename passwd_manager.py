from cryptography.fernet import Fernet
import secrets
import string
import os
import json

def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher = Fernet(key)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

def save_password(site, password):
    encrypted_password = cipher.encrypt(password.encode())
    data = {}
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
    data[site] = encrypted_password.decode()
    with open("passwords.json", "w") as file:
        json.dump(data, file)

def retrieve_password(site):
    if not os.path.exists("passwords.json"):
        return "No passwords stored."
    with open("passwords.json", "r") as file:
        data = json.load(file)
    encrypted_password = data.get(site)
    if encrypted_password:
        return cipher.decrypt(encrypted_password.encode()).decode()
    return "No password found for this site."

def main():
    while True:
        choice = input("Choose an option: [1] Save Password [2] Retrieve Password [3] Generate Password [4] Exit: ")
        if choice == '1':
            site = input("Enter the site name: ")
            password = input("Enter the password: ")
            save_password(site, password)
            print("Password saved successfully.")
        elif choice == '2':
            site = input("Enter the site name: ")
            print("Password:", retrieve_password(site))
        elif choice == '3':
            length = int(input("Enter the password length: "))
            print("Generated Password:", generate_password(length))
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

