from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class SecureChannel:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.symmetric_key = Fernet.generate_key()
        self.fernet = Fernet(self.symmetric_key)

    def encrypt(self, message: bytes) -> bytes:
        return self.fernet.encrypt(message)

    def decrypt(self, encrypted_message: bytes) -> bytes:
        return self.fernet.decrypt(encrypted_message)

    def get_public_key(self) -> rsa.RSAPublicKey:
        return self.public_key

    def set_partner_public_key(self, partner_public_key: rsa.RSAPublicKey):
        self.partner_public_key = partner_public_key

    def exchange_symmetric_key(self) -> bytes:
        encrypted_symmetric_key = self.partner_public_key.encrypt(
            self.symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_symmetric_key

    def receive_symmetric_key(self, encrypted_symmetric_key: bytes):
        self.partner_symmetric_key = self.private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.partner_fernet = Fernet(self.partner_symmetric_key)
