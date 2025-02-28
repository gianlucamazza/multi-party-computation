import secrets
import logging
from typing import List, Tuple, Optional
from mpc.participant import MPCParticipant

logger = logging.getLogger(__name__)

class ShamirSecretSharingParticipant(MPCParticipant):
    """
    Implementation of a participant in Shamir's Secret Sharing scheme.
    
    This class provides methods for generating polynomial-based secret shares
    and reconstructing secrets from a threshold number of shares.
    """
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """
        Calculate the modular multiplicative inverse of a under modulo m.
        
        Args:
            a: The number to find the modular inverse for
            m: The modulus
            
        Returns:
            The modular inverse of a under modulo m
            
        Raises:
            Exception: If the modular inverse does not exist
        """
        def egcd(a: int, b: int) -> Tuple[int, int, int]:
            """Extended Euclidean Algorithm to find gcd and coefficients."""
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
        """
        Generate shares for a secret using Shamir's Secret Sharing.
        
        This method creates a random polynomial of degree (threshold-1) with
        the secret as the constant term, then evaluates the polynomial at different
        points to create the shares.
        
        Args:
            secret: The secret value to be shared
            
        Returns:
            List of shares, one for each participant
        """
        if not 0 <= secret < self.shared_prime:
            raise ValueError(f"Secret must be in range [0, {self.shared_prime})")
            
        logger.info(f"Participant {self.id} generating shares for secret: {secret}")
        
        # Create a random polynomial f(x) = secret + a_1*x + a_2*x^2 + ... + a_(t-1)*x^(t-1)
        # where the secret is the constant term (a_0)
        # Note: For (t,n) threshold scheme, polynomial degree should be t-1
        coefficients = [secret]  # The constant term is the secret
        
        # Add random coefficients for terms x^1 through x^(threshold-1)
        for _ in range(self.threshold - 1):
            coefficients.append(secrets.randbelow(self.shared_prime))
        
        shares = []
        # Evaluate the polynomial at points (1, 2, ..., num_participants)
        for i in range(1, self.num_participants + 1):
            # Calculate f(i) = secret + a_1*i + a_2*i^2 + ... + a_(t-1)*i^(t-1)
            share = 0
            for j, coeff in enumerate(coefficients):
                term = (coeff * pow(i, j, self.shared_prime)) % self.shared_prime
                share = (share + term) % self.shared_prime
                
            shares.append(share)
            logger.debug(f"Participant {self.id} generated share {i}: {share}")
            
        return shares

    def reconstruct_secret(self, shares: List[int]) -> int:
        """
        Reconstruct the original secret from a set of shares.
        
        This method uses Lagrange interpolation to reconstruct the original
        polynomial and extract the constant term (the secret).
        
        Args:
            shares: List of share values to use for reconstruction
            
        Returns:
            The reconstructed secret
            
        Raises:
            ValueError: If insufficient shares are provided
        """
        # Ensure enough shares are provided for reconstruction
        t = len(shares)  # Number of shares provided
        if t < self.threshold:
            logger.warning(f"Only {t} shares provided, may not be enough for reconstruction")
            
        # For a polynomial of degree (t-1), we need exactly t points to reconstruct
        # In a threshold scheme, we need exactly 'threshold' shares
        
        # Only use the first 'threshold' shares if more are provided
        if t > self.threshold:
            shares = shares[:self.threshold]
            t = self.threshold
            
        logger.info(f"Participant {self.id} reconstructing secret from {t} shares")
        
        # The x-coordinates corresponding to each share (1, 2, ..., t)
        x_coords = list(range(1, t + 1))
        
        # Initialize the reconstructed secret to 0
        secret = 0
        
        # Use Lagrange interpolation to find f(0)
        for i in range(t):
            # Calculate the Lagrange basis polynomial L_i(0)
            numerator = 1
            denominator = 1
            
            for j in range(t):
                if i != j:
                    # For x=0: L_i(0) = Π[(0-x_j)/(x_i-x_j)] for j≠i
                    numerator = (numerator * (-x_coords[j])) % self.shared_prime
                    denominator = (denominator * (x_coords[i] - x_coords[j])) % self.shared_prime
            
            # Calculate the Lagrange coefficient
            inv_denominator = self._mod_inverse(denominator, self.shared_prime)
            lagrange_coef = (numerator * inv_denominator) % self.shared_prime
            
            # Multiply by the share value and add to the result
            term = (shares[i] * lagrange_coef) % self.shared_prime
            secret = (secret + term) % self.shared_prime
        
        logger.debug(f"Participant {self.id} reconstructed secret: {secret}")
        return secret
    