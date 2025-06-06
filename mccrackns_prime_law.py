# -----------------------------------------------------------------------------
# mccrackns_prime_law.py
# -----------------------------------------------------------------------------
"""Simple prime generator used for repository examples."""

from typing import List
from src.prime_utils import is_prime


class McCracknsPrimeLaw:
    """Generate prime numbers using straightforward trial division."""

    def __init__(self, n_primes: int):
        self.target = n_primes
        self.primes: List[int] = []
        self.gaps: List[int] = []

    def generate(self) -> None:
        """Fill :pyattr:`primes` with the first ``n`` prime numbers."""
        candidate = 2
        last_prime = None
        while len(self.primes) < self.target:
            if is_prime(candidate):
                self.primes.append(candidate)
                if last_prime is not None:
                    self.gaps.append(candidate - last_prime)
                last_prime = candidate
            candidate += 1 if candidate == 2 else 2

    def get_gaps(self) -> List[int]:
        """Return the list of gaps between generated primes."""
        return self.gaps

    def get_primes(self) -> List[int]:
        """Return the list of generated primes."""
        return self.primes
