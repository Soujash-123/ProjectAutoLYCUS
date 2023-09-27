from Crypto.Cipher import ARC4
from Crypto.Random import get_random_bytes
import random
def generate_arc4_encryption(plaintext, key):
    cipher = ARC4.new(key)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext.hex()

def generate_arc4_decryption(ciphertext, key):
    cipher = ARC4.new(key)
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return plaintext.decode()

# Example usage
plaintext = b'This is a secret message'
key = get_random_bytes(16)  # Key size can vary for ARC4
encryption = generate_arc4_encryption(plaintext, key)
print("ARC4 Encryption:", encryption)
print("Key:",key.hex())
'''attempt = 1
generated_key=""
while generated_key!=key:
    attempt+=1
    generated_key = get_random_bytes(16)
    print(f"Trying combination {attempt}...")
decryption = generate_arc4_decryption(encryption, generated_key)
print("ARC4 Decryption:", decryption)'''
