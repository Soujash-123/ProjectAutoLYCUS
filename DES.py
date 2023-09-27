from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def generate_des_encryption(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))
    return ciphertext.hex()

# Example usage
plaintext = b'This is a secret message'
key = get_random_bytes(8)  # DES key size is 8 bytes
encryption = generate_des_encryption(plaintext, key)
print("DES Encryption:", encryption)
