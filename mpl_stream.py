"""Streaming prime generator used for benchmarking."""

from typing import List
from src.prime_utils import is_prime


class MPLStream:
    """Generate ``n_primes`` primes lazily."""

    def __init__(self, n_primes: int):
        self.target = n_primes
        self.primes: List[int] = []


    def generate(self) -> None:
        """Populate :pyattr:`primes` with prime numbers."""
        candidate = 2
        while len(self.primes) < self.target:
            if is_prime(candidate):
                self.primes.append(candidate)
            candidate += 1 if candidate == 2 else 2
