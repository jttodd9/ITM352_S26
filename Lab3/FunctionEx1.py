# Lab3/FunctionEx1.py
# This script encrypts and decrypts a user-provided message using the Fernet symmetric encryption method.
# Justin Todd
# date: Jan 29, 2026

from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher = Fernet(key)

# Get message from user
message = input("Enter a message to encrypt: ")

# Encode, encrypt, decrypt, and decode
encoded = message.encode('utf-8')
encrypted = cipher.encrypt(encoded)
decrypted = cipher.decrypt(encrypted)
final_message = decrypted.decode('utf-8')

# Display results
print(f"\nOriginal message: {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted message: {final_message}")