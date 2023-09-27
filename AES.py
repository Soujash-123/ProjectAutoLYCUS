from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def generate_aes_encryption(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext.hex()

# Example usage
plaintext = b'This is a secret message'
key = get_random_bytes(16)  # AES-128
encryption = generate_aes_encryption(plaintext, key)
print("AES Encryption:", encryption)
