import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass
from time import sleep

def display_banner():
    print(r"""
  ______ _       _               
 |  ____(_)     | |              
 | |__   _ _ __ | |__   ___ _ __ 
 |  __| | | '_ \| '_ \ / _ \ '__|
 | |    | | |_) | | | |  __/ |   
 |_|    |_| .__/|_| |_|\___|_|   
          | |                    
          |_|                    
    """)
    print("🔐 Fipher - Secure File & Message Encryption Tool")
    print("="*50)
    print("Created by: MD Farhan Uddin Jibon".center(50))
    print("="*50 + "\n")

def generate_key(password: str, salt: bytes = None) -> bytes:
    """Generate a Fernet key from a password using PBKDF2"""
    if salt is None:
        salt = os.urandom(16)  # Generate a random salt
    
    # Derive key from password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_message(message: str, password: str) -> tuple:
    """Encrypt a message with password protection"""
    key, salt = generate_key(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted, salt

def decrypt_message(encrypted: bytes, password: str, salt: bytes) -> str:
    """Decrypt a message with password and salt"""
    key, _ = generate_key(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return decrypted.decode()

def encrypt_file(input_path: str, output_path: str, password: str):
    """Encrypt a file with password protection"""
    with open(input_path, 'rb') as f:
        file_data = f.read()
    
    key, salt = generate_key(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(file_data)
    
    with open(output_path, 'wb') as f:
        f.write(salt + encrypted)  # Store salt with encrypted data

def decrypt_file(input_path: str, output_path: str, password: str):
    """Decrypt a file with password"""
    with open(input_path, 'rb') as f:
        data = f.read()
    
    salt = data[:16]  # First 16 bytes are the salt
    encrypted = data[16:]
    
    key, _ = generate_key(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    
    with open(output_path, 'wb') as f:
        f.write(decrypted)

def main():
    display_banner()
    
    while True:
        print("\n" + "="*50)
        print("MAIN MENU".center(50))
        print("="*50)
        print("1. 🔒 Encrypt a message")
        print("2. 🔓 Decrypt a message")
        print("3. 📁 Encrypt a file")
        print("4. 📂 Decrypt a file")
        print("5. 🚪 Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            print("\n" + "="*50)
            print("MESSAGE ENCRYPTION".center(50))
            print("="*50)
            message = input("\nEnter message to encrypt: ")
            password = getpass.getpass("Enter password: ")
            confirm_pass = getpass.getpass("Confirm password: ")
            
            if password != confirm_pass:
                print("\n⚠️ Passwords don't match! Please try again.")
                continue
                
            encrypted, salt = encrypt_message(message, password)
            print("\n" + "="*50)
            print("ENCRYPTION SUCCESSFUL".center(50))
            print("="*50)
            print(f"\n🔑 Encrypted message (base64):\n{base64.b64encode(encrypted).decode()}")
            print(f"\n🧂 Salt (required for decryption, base64):\n{base64.b64encode(salt).decode()}")
            print("\n⚠️ Please save both the encrypted message and salt securely!")
        
        elif choice == '2':
            print("\n" + "="*50)
            print("MESSAGE DECRYPTION".center(50))
            print("="*50)
            encrypted_b64 = input("\nEnter encrypted message (base64): ")
            salt_b64 = input("Enter salt (base64): ")
            password = getpass.getpass("Enter password: ")
            
            try:
                encrypted = base64.b64decode(encrypted_b64)
                salt = base64.b64decode(salt_b64)
                print("\nDecrypting...")
                sleep(1)
                decrypted = decrypt_message(encrypted, password, salt)
                print("\n" + "="*50)
                print("DECRYPTION SUCCESSFUL".center(50))
                print("="*50)
                print(f"\n📜 Decrypted message:\n{decrypted}")
            except Exception as e:
                print("\n" + "="*50)
                print("DECRYPTION FAILED".center(50))
                print("="*50)
                print(f"\n❌ Error: {e}\nWrong password or corrupted data.")
        
        elif choice == '3':
            print("\n" + "="*50)
            print("FILE ENCRYPTION".center(50))
            print("="*50)
            input_file = input("\nEnter input file path: ")
            output_file = input("Enter output file path: ")
            password = getpass.getpass("Enter password: ")
            confirm_pass = getpass.getpass("Confirm password: ")
            
            if password != confirm_pass:
                print("\n⚠️ Passwords don't match! Please try again.")
                continue
                
            try:
                print("\nEncrypting...")
                encrypt_file(input_file, output_file, password)
                sleep(1)
                print("\n" + "="*50)
                print("ENCRYPTION SUCCESSFUL".center(50))
                print("="*50)
                print(f"\n✅ File encrypted successfully to:\n{output_file}")
            except Exception as e:
                print("\n" + "="*50)
                print("ENCRYPTION FAILED".center(50))
                print("="*50)
                print(f"\n❌ Error: {e}")
        
        elif choice == '4':
            print("\n" + "="*50)
            print("FILE DECRYPTION".center(50))
            print("="*50)
            input_file = input("\nEnter encrypted file path: ")
            output_file = input("Enter output file path: ")
            password = getpass.getpass("Enter password: ")
            
            try:
                print("\nDecrypting...")
                decrypt_file(input_file, output_file, password)
                sleep(1)
                print("\n" + "="*50)
                print("DECRYPTION SUCCESSFUL".center(50))
                print("="*50)
                print(f"\n✅ File decrypted successfully to:\n{output_file}")
            except Exception as e:
                print("\n" + "="*50)
                print("DECRYPTION FAILED".center(50))
                print("="*50)
                print(f"\n❌ Error: {e}\nWrong password or corrupted file.")
        
        elif choice == '5':
            print("\n" + "="*50)
            print("THANK YOU FOR USING FIPHER".center(50))
            print("="*50)
            print("\nCreated by: MD Farhan Uddin Jibon")
            print("\nExiting...")
            sleep(1)
            break
        
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main()