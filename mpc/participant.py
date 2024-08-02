from abc import ABC, abstractmethod
from typing import List
from security.secure_channel import SecureChannel

class MPCParticipant(ABC):
    def __init__(self, id: int, num_participants: int, shared_prime: int):
        self.id = id
        self.num_participants = num_participants
        self.shared_prime = shared_prime
        self.shares: List[int] = []
        self.secure_channel = SecureChannel()

    @abstractmethod
    def generate_shares(self, secret: int) -> List[int]:
        pass

    @abstractmethod
    def reconstruct_secret(self, shares: List[int]) -> int:
        pass