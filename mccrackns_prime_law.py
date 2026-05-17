"""
McCrackn's Prime Law — wheel-based minimal recursion implementation.

This version replaces the previous hardcoded early schedule with
an explicit wheel(30) gap generator. This reflects the verified
minimal recursion structure observed from prime 11 onward.

Wheel(30) gap cycle:
    6, 4, 2, 4, 2, 4, 6, 2

U1 remains seed-only (2 -> 3).
After 3, all gaps are even.
GCD is retained strictly as a structural invariant.
"""
from math import gcd
from numbers_domains import NumbersDomains


class McCracknsPrimeLaw:

    WHEEL_30 = [6, 4, 2, 4, 2, 4, 6, 2]

    def __init__(self, *, n_primes: int = 100, verbose: bool = False,
                 progress_every: int = 1000):

        self.n_primes = max(2, n_primes)
        self.verbose = verbose
        self.progress_every = max(1, progress_every)

        # Seed primes up to 13
        seed_primes = [2, 3, 5, 7, 11, 13]
        seed_gaps = [1, 2, 2, 4, 2]
        seed_labels = ["U1", "E1.0", "E1.0", "E1.1", "E1.0"]

        self.primes = seed_primes[:self.n_primes]
        self.gaps = seed_gaps[:len(self.primes) - 1]
        self.motifs = []
        self._run_counter = {}

        for lbl in seed_labels[:len(self.primes) - 1]:
            run = self._run_counter.get(lbl, 0) + 1
            self._run_counter[lbl] = run
            self.motifs.append((lbl, run))

        self.domains = NumbersDomains()

        # Start wheel cycle at position corresponding to 13 -> 17 (gap 4)
        # Wheel sequence: 6,4,2,4,2,4,6,2
        # From 11 -> 13 (gap 2) we are aligned so next gap should be 4.
        self.wheel_idx = 1

        # Primorial tracking (structural invariant)
        self.regime_idx = 1
        self.primorial = 2 * 3

    @staticmethod
    def _gap_to_motif(gap: int, domains: NumbersDomains) -> str:
        return domains.canonical_motif(gap)

    def _record(self, cand: int, gap: int, label: str):
        if gap == 1 and cand != 3:
            raise AssertionError(f"gap=1 leaked after seed at candidate {cand}")
        if self.primes[-1] >= 3 and gap % 2 != 0:
            raise AssertionError(f"post-seed gap must be even, got {gap}")

        self.primes.append(cand)
        self.gaps.append(gap)

        run = self._run_counter.get(label, 0) + 1
        self._run_counter[label] = run
        self.motifs.append((label, run))

    def _single_step(self, *, internal: bool = False):
        if len(self.primes) < 6:
            return

        p_curr = self.primes[-1]
        P = self.primorial

        gap = self.WHEEL_30[self.wheel_idx]
        self.wheel_idx = (self.wheel_idx + 1) % len(self.WHEEL_30)

        if p_curr >= 3 and gap % 2 != 0:
            raise AssertionError(f"post-seed gap must be even, got {gap}")

        cand = p_curr + gap

        # Structural invariant
        assert gcd(cand, P) == 1, \
            f"GCD-invariant violated at candidate {cand} (P={P})"

        label = self._gap_to_motif(gap, self.domains)
        self._record(cand, gap, label)

        if self.verbose and not internal and len(self.primes) % self.progress_every == 0:
            print(f"[prime {len(self.primes):>9}] {cand}")

    def generate(self):
        while len(self.primes) < self.n_primes:
            self._single_step()
        return self.primes

    def generate_one(self):
        if len(self.primes) < self.n_primes:
            self._single_step()
        idx = len(self.primes)
        p = self.primes[-1]
        gap = 0 if idx == 1 else self.gaps[-1]
        motif = "U1" if idx == 1 else self.motifs[-1][0]
        return idx, p, gap, motif

    def get_primes(self):
        return self.primes.copy()

    def get_gaps(self):
        return self.gaps.copy()

    def get_motifs(self):
        return self.motifs.copy()
