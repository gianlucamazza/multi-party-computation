from abc import ABC, abstractmethod
from typing import List, Any
from security.secure_channel import SecureChannel

class MPCParticipant(ABC):
    """
    Abstract base class for Multi-Party Computation participants.
    
    This class defines the interface for participants in secure multi-party
    computation protocols, providing methods for share generation and secret
    reconstruction.
    """
    
    def __init__(self, id: int, num_participants: int, shared_prime: int, threshold: int = None):
        """
        Initialize a multi-party computation participant.
        
        Args:
            id: Unique identifier for this participant
            num_participants: Total number of participants in the protocol
            shared_prime: Prime modulus for the finite field operations
            threshold: Minimum number of shares needed for reconstruction (defaults to num_participants)
        """
        self.id = id
        self.num_participants = num_participants
        self.shared_prime = shared_prime
        # Set threshold to num_participants if not specified
        self.threshold = threshold if threshold is not None else num_participants
        self.shares: List[Any] = []
        self.secure_channel = SecureChannel()

    @abstractmethod
    def generate_shares(self, secret: int) -> List[int]:
        """
        Generate shares for a secret value.
        
        Args:
            secret: The secret value to be shared
            
        Returns:
            List of shares, one for each participant
        """
        pass

    @abstractmethod
    def reconstruct_secret(self, shares: List[int]) -> int:
        """
        Reconstruct the original secret from a set of shares.
        
        Args:
            shares: List of share values to use for reconstruction
            
        Returns:
            The reconstructed secret
        """
        pass