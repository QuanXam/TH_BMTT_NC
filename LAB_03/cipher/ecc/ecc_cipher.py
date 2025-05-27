import ecdsa
import os

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        # Tạo khóa riêng tư
        sk = ecdsa.SigningKey.generate()
        # Lấy khóa công khai từ khóa riêng
        vk = sk.get_verifying_key()

        with open('cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())

        with open('cipher/ecc/keys/publicKey.pem', 'wb') as p:
            p.write(vk.to_pem())

    def load_keys(self):
        with open('cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())

        with open('cipher/ecc/keys/publicKey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())

        return sk, vk

    def sign(self, message, private_key):
        # Ký dữ liệu bằng khóa riêng tư
        return private_key.sign(message.encode('ascii'))

    def verify(self, message, signature, public_key):
        # Xác thực chữ ký bằng khóa công khai
        try:
            return public_key.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            return False
