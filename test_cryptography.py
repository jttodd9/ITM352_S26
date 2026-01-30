#!/usr/bin/env python3
"""Test script to verify that the cryptography library is installed correctly."""

from cryptography.fernet import Fernet

# Test 1: Generate a key
print("Test 1: Generating encryption key...")
key = Fernet.generate_key()
print(f"✓ Key generated successfully: {key[:20]}...")

# Test 2: Create a cipher and encrypt data
print("\nTest 2: Encrypting data...")
cipher = Fernet(key)
message = b"Hello, Cryptography!"
encrypted_message = cipher.encrypt(message)
print(f"✓ Original message: {message}")
print(f"✓ Encrypted message: {encrypted_message[:40]}...")

# Test 3: Decrypt data
print("\nTest 3: Decrypting data...")
decrypted_message = cipher.decrypt(encrypted_message)
print(f"✓ Decrypted message: {decrypted_message}")

# Verify decryption matches original
if decrypted_message == message:
    print("\n✓ SUCCESS: Cryptography library is working correctly!")
else:
    print("\n✗ FAILED: Decryption did not match original message")
