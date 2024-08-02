import secrets
import logging
from typing import List, Tuple
from mpc.participant import MPCParticipant
from utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

class ShamirSecretSharingParticipant(MPCParticipant):
    def _mod_inverse(self, a: int, m: int) -> int:
        def egcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            else:
                g, y, x = egcd(b % a, a)
                return g, x - (b // a) * y, y

        g, x, _ = egcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    def generate_shares(self, secret: int) -> List[int]:
        logger.info(f"Participant {self.id} generating shares for secret")
        coefficients = [secret] + [secrets.randbelow(self.shared_prime) for _ in range(self.num_participants - 1)]
        shares = []
        for i in range(1, self.num_participants + 1):
            share = sum(coeff * pow(i, j, self.shared_prime) for j, coeff in enumerate(coefficients)) % self.shared_prime
            shares.append(share)
            logger.debug(f"Participant {self.id} generated share {i}: {share}")
        return shares

    def reconstruct_secret(self, shares: List[int]) -> int:
        logger.info(f"Participant {self.id} reconstructing secret from shares")
        x_values = list(range(1, len(shares) + 1))
        secret = 0
        for i, share in enumerate(shares):
            numerator, denominator = 1, 1
            for j, x in enumerate(x_values):
                if i != j:
                    numerator = (numerator * (-x_values[j])) % self.shared_prime
                    denominator = (denominator * (x_values[i] - x_values[j])) % self.shared_prime
            lagrange = (share * numerator * self._mod_inverse(denominator, self.shared_prime)) % self.shared_prime
            secret = (secret + lagrange) % self.shared_prime
        logger.debug(f"Participant {self.id} reconstructed secret: {secret}")
        return secret
    