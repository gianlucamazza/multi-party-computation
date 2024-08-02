import logging
from typing import Tuple
from ecdsa import SigningKey, SECP256k1
from mpc.shamir_secret_sharing import ShamirSecretSharingParticipant
from utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

class MPCSigningProtocol:
    def __init__(self, num_participants: int, threshold: int):
        self.num_participants = num_participants
        self.threshold = threshold
        self.curve = SECP256k1
        self.shared_prime = self.curve.order
        logger.info(f"Using shared prime (curve order) for all participants: {self.shared_prime}")
        self.participants = [ShamirSecretSharingParticipant(i, num_participants, self.shared_prime) for i in range(num_participants)]
        logger.info(f"MPC Signing Protocol initialized with {num_participants} participants, threshold {threshold}, using SECP256k1 curve")
        self.private_key = None
        self.public_key = None

    def setup_secure_channels(self):
        # In a real implementation, this would involve network communication
        for i, participant in enumerate(self.participants):
            for j, other_participant in enumerate(self.participants):
                if i != j:
                    participant.secure_channel.set_partner_public_key(other_participant.secure_channel.get_public_key())
                    encrypted_key = participant.secure_channel.exchange_symmetric_key()
                    other_participant.secure_channel.receive_symmetric_key(encrypted_key)

    def generate_key_shares(self) -> None:
        logger.info("Generating and distributing key shares")
        # Generate a private key using ECDSA
        self.private_key = SigningKey.generate(curve=self.curve)
        private_key_int = self.private_key.privkey.secret_multiplier
        self.public_key = self.private_key.get_verifying_key()
        logger.info(f"Generated ECDSA private key: {private_key_int}")
        logger.info(f"Corresponding public key: {self.public_key.to_string().hex()}")
        
        key_shares = self.participants[0].generate_shares(private_key_int)
        for i, share in enumerate(key_shares):
            encrypted_share = self.participants[i].secure_channel.encrypt(str(share).encode())
            self.participants[i].shares = [encrypted_share]
            logger.debug(f"Participant {i} received encrypted key share")

    def sign_message(self, message: str) -> Tuple[int, int]:
        logger.info(f"Signing message: '{message}'")
        if not self.private_key:
            raise ValueError("Private key not available. Generate key shares first.")
        
        # In a real threshold signature scheme, this would involve a distributed signing process
        # For simplicity, we're using the full private key here
        signature = self.private_key.sign(message.encode())
        r, s = signature[:32], signature[32:]  # Split the signature into r and s
        r_int = int.from_bytes(r, 'big')
        s_int = int.from_bytes(s, 'big')
        logger.info(f"Generated signature: (r: {r_int}, s: {s_int})")
        return r_int, s_int

    def verify_signature(self, message: str, signature: Tuple[int, int]) -> bool:
        if not self.public_key:
            raise ValueError("Public key not available. Generate key shares first.")
        r, s = signature
        try:
            r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')
            s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
            signature_bytes = r_bytes + s_bytes
            self.public_key.verify(signature_bytes, message.encode())
            logger.info("Signature verified successfully!")
            return True
        except:
            logger.warning("Signature verification failed!")
            return False
        