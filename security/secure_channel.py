import logging
from typing import Optional
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

logger = logging.getLogger(__name__)

class SecureChannel:
    """
    Secure communication channel between participants.
    
    This class provides encryption, decryption, and key exchange functionality
    for secure communication between participants using RSA for asymmetric
    encryption and Fernet for symmetric encryption.
    """
    
    def __init__(self):
        """Initialize a secure channel with fresh cryptographic keys."""
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        
        # Generate symmetric key for efficient encryption
        self.symmetric_key = Fernet.generate_key()
        self.fernet = Fernet(self.symmetric_key)
        
        # Partner keys will be set during key exchange
        self.partner_public_key: Optional[rsa.RSAPublicKey] = None
        self.partner_symmetric_key: Optional[bytes] = None
        self.partner_fernet: Optional[Fernet] = None
        
        logger.debug("Secure channel initialized with new cryptographic keys")

    def encrypt(self, message: bytes) -> bytes:
        """
        Encrypt a message using symmetric encryption.
        
        Args:
            message: The plaintext message to encrypt
            
        Returns:
            The encrypted message
        """
        if not isinstance(message, bytes):
            raise TypeError("Message must be bytes")
            
        return self.fernet.encrypt(message)

    def decrypt(self, encrypted_message: bytes) -> bytes:
        """
        Decrypt a message using symmetric encryption.
        
        Args:
            encrypted_message: The encrypted message to decrypt
            
        Returns:
            The decrypted plaintext message
            
        Raises:
            cryptography.fernet.InvalidToken: If the message is invalid or corrupted
        """
        if not isinstance(encrypted_message, bytes):
            raise TypeError("Encrypted message must be bytes")
            
        try:
            return self.fernet.decrypt(encrypted_message)
        except Exception as e:
            logger.error(f"Failed to decrypt message: {str(e)}")
            raise

    def get_public_key(self) -> rsa.RSAPublicKey:
        """
        Get this channel's public key for sharing with other participants.
        
        Returns:
            The RSA public key
        """
        return self.public_key

    def set_partner_public_key(self, partner_public_key: rsa.RSAPublicKey) -> None:
        """
        Set the partner's public key for secure communication.
        
        Args:
            partner_public_key: The partner's RSA public key
        """
        self.partner_public_key = partner_public_key
        logger.debug("Partner public key set")

    def exchange_symmetric_key(self) -> bytes:
        """
        Encrypt this channel's symmetric key with the partner's public key.
        
        Returns:
            The encrypted symmetric key
            
        Raises:
            ValueError: If partner's public key hasn't been set yet
        """
        if not self.partner_public_key:
            raise ValueError("Partner public key not set. Call set_partner_public_key first.")
            
        # Encrypt our symmetric key with the partner's public key
        encrypted_symmetric_key = self.partner_public_key.encrypt(
            self.symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        logger.debug("Symmetric key encrypted for secure exchange")
        return encrypted_symmetric_key

    def receive_symmetric_key(self, encrypted_symmetric_key: bytes) -> None:
        """
        Decrypt the partner's symmetric key using this channel's private key.
        
        Args:
            encrypted_symmetric_key: The encrypted symmetric key from the partner
            
        Raises:
            ValueError: If the decryption fails
        """
        try:
            # Decrypt the partner's symmetric key
            self.partner_symmetric_key = self.private_key.decrypt(
                encrypted_symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            # Create a Fernet instance with the partner's key
            self.partner_fernet = Fernet(self.partner_symmetric_key)
            logger.debug("Partner's symmetric key received and decrypted successfully")
        except Exception as e:
            logger.error(f"Failed to decrypt partner's symmetric key: {str(e)}")
            raise ValueError(f"Failed to decrypt partner's symmetric key: {str(e)}")
            
    def encrypt_for_partner(self, message: bytes) -> bytes:
        """
        Encrypt a message using the partner's symmetric key.
        
        Args:
            message: The plaintext message to encrypt
            
        Returns:
            The encrypted message
            
        Raises:
            ValueError: If partner's symmetric key hasn't been received yet
        """
        if not self.partner_fernet:
            raise ValueError("Partner's symmetric key not set. Call receive_symmetric_key first.")
            
        return self.partner_fernet.encrypt(message)
        
    def decrypt_from_partner(self, encrypted_message: bytes) -> bytes:
        """
        Decrypt a message using the partner's symmetric key.
        
        Args:
            encrypted_message: The encrypted message from the partner
            
        Returns:
            The decrypted plaintext message
            
        Raises:
            ValueError: If partner's symmetric key hasn't been received yet
            cryptography.fernet.InvalidToken: If the message is invalid or corrupted
        """
        if not self.partner_fernet:
            raise ValueError("Partner's symmetric key not set. Call receive_symmetric_key first.")
            
        try:
            return self.partner_fernet.decrypt(encrypted_message)
        except Exception as e:
            logger.error(f"Failed to decrypt message from partner: {str(e)}")
            raise
