from cryptography.fernet import Fernet

# IMPORTANT: generate once and keep fixed
key = b'jnhk4Y_AixvgGIOodMMQaRqPkf8D4hJ36wNs6DhbTto='
cipher = Fernet(key)

def encrypt_card(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_card(data):
    return cipher.decrypt(data.encode()).decode()