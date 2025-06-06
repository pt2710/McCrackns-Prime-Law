# -----------------------------------------------------------------------------
# mccrackns_prime_law.py
# -----------------------------------------------------------------------------
"""Deterministic prime generator based on McCrackn's law."""

from collections import defaultdict
from typing import Dict, List

OFFSET_E = 0  # δₖ
OFFSET_O = 2  # εₖ
GAP_TABLE: Dict[str, List[int]] = {} 

class McCracknsPrimeLaw:
    N0 = 6

    def __init__(self, n_primes: int):
        """Initialize the generator for ``n_primes`` primes."""
        self.target = n_primes
        self.primes = [2, 3, 5, 7, 11, 13]
        self.gaps   = [1, 2, 2, 4, 2]
        self.run    = defaultdict(int, {"U1": 1, "E1": 0, "O1": 0})
        self.regime_k = 1
        self.next_regime_point = self.N0

    # ---------- public ----------
    def generate(self):
        """Generate primes up to the configured target."""
        while len(self.primes) < self.target:
            if len(self.primes) == self.next_regime_point:
                self._activate_next_regime()
            gap, dom = self._minimal_gap_next()
            self.primes.append(self.primes[-1] + gap)
            self.gaps.append(gap)
            self.run[dom] += 1

    def get_gaps(self):
        """Return the list of generated gaps."""
        return self.gaps

    # ---------- helpers ----------
    def _activate_next_regime(self):
        """Advance to the next regime level."""
        self.regime_k += 1
        k = self.regime_k
        self.run[f"E{k}"] = 0
        self.run[f"O{k}"] = 0
        self.next_regime_point *= 2

    def _minimal_gap_next(self):
        """Return the next minimal gap and its domain."""
        min_run = min(self.run[d] + 1 for d in self.run if d != "U1")
        domains = [f"E{k}" for k in range(1, self.regime_k + 1)] + \
                  [f"O{k}" for k in range(1, self.regime_k + 1)]
        for d in domains:
            if self.run[d] + 1 == min_run:
                return self._gap(d, min_run), d
        raise RuntimeError("No legal motif found – check tables/offsets")

    def _gap(self, domain: str, r: int) -> int:
        """Lookup or compute the gap size for ``domain`` at run ``r``."""
        tbl = GAP_TABLE.get(domain)
        if tbl and r <= len(tbl):
            return tbl[r - 1]
        if domain == "U1":
            return 1
        k = int(domain[1:])
        return 6 * k * r - OFFSET_E if domain[0] == "E" else 6 * k * r + OFFSET_O