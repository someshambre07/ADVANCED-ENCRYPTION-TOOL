import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes



def generate_key():
    #### Generate a random 32-byte key for AES-256 encryption. ####
    return get_random_bytes(32)



def encryption_func(file_path, key):
    #### Encrypt a file using AES-256 encryption. ####
    cipher = AES.new(key, AES.MODE_CBC)    
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)

    print(f"File encrypted successfully: {encrypted_file_path}")



def decryption_func(encrypted_file_path, key):
    #### Decrypt a file encrypted using AES-256 encryption.####
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    decrypted_file_path = encrypted_file_path.replace('.enc', '')
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    print(f"File decrypted successfully: {decrypted_file_path}")



def main():
    print("NEW AES-256 FILE ENCRYPTION TOOL")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Generate a new encryption key")

    choice = input("Enter your choice (1/2/3): ")

    match choice:
        case '1':
            #### select the file you want to encrypt for eg.example.txt
            file_path = input("Enter the path of the file to encrypt: ")
            key_path = input("Enter the path to the key file: ")
            if not os.path.exists(file_path):
                print("File not found!")
                return
            if not os.path.exists(key_path):
                print("Key file not found!")
                return
            with open(key_path, 'rb') as kf:
                key = kf.read()
            encryption_func(file_path, key)

        case '2':
            #### select the file you want to decrypt for eg.example.txt.enc
            encrypted_file_path = input("Enter the path of the file to decrypt: ")
            key_path = input("Enter the path to the key file: ")
            if not os.path.exists(encrypted_file_path):
                print("Encrypted file not found!")
                return
            if not os.path.exists(key_path):
                print("Key file not found!")
                return
            with open(key_path, 'rb') as kf:
                key = kf.read()
            decryption_func(encrypted_file_path, key)

        case '3':
            #### create a file with type ".key" for eg.generated_key.key
            try:
                key = generate_key()
                key_file_path = input("Enter the path to save the new key file for eg.generated_key.key: ")
                if not key_file_path.endswith('.key'):
                    raise ValueError("Invalid file type. Please provide a '.key' file.")
                with open(key_file_path, 'wb') as kf:
                    kf.write(key)

                print(f"New encryption key saved to: {key_file_path}")

            except (OSError, ValueError) as e:
                print(f"Error: {e}")
        case _:
            print("Invalid choice. Exiting.")



if __name__ == "__main__":
    main()
