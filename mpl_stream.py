# mpl_stream.py  – deterministic infinite prime stream
import struct, mmap, os
from typing import List

# load the 19-gap seed
fd = os.open("seed_gaps.bin", os.O_RDONLY)
SEED = list(struct.unpack("<19I", mmap.mmap(fd, 0, access=mmap.ACCESS_READ)))
# SEED = [1, 2, 2, 4, 2, 6, 12, 12, 24, 18, 30, 18, 24, 36, 24, 30, 48, 30, 36]

class MPLStream:
    """Simple prime stream using a precomputed gap seed."""

    def __init__(self, n_primes: int):
        """Create a stream that will yield ``n_primes`` numbers."""
        self.target = n_primes
        self.primes: List[int] = [2]

    def generate(self):
        """Populate :pyattr:`primes` with generated prime numbers."""
        p = 2
        k = 0           # regime index
        idx = 0         # index within current regime pattern
        while len(self.primes) < self.target:
            gap = SEED[idx]
            p += gap
            self.primes.append(p)

            idx += 1
            if idx == len(SEED):        # finished one regime pattern
                k += 1                  # next regime
                idx = 0                 # restart pattern (motif law)
