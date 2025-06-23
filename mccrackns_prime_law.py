"""
McCrackn’s Prime Law — Deterministic, recursive prime generator based on motif algebra.

This class implements a novel prime-generation algorithm using regime-based motif expansion
without trial division, sieving, or primality testing. Each new prime is derived from
canonical gap motifs constructed and sorted recursively.

Core concepts:
- Motifs: canonical gap encodings ("U1", "E1.0", etc.)
- Alphabet: active motifs used to construct candidates
- Regimes: expansion layers with motif innovation
- Primorial: dynamic modulator constraining valid candidates

The generator yields exact primes with metadata (gap, motif, regime) and supports both
stepwise and stream-based generation.

Dependencies:
- `numbers_domains.py` must provide `NumbersDomains.canonical_motif(gap: int) -> str`
"""
from math import gcd
from numbers_domains import NumbersDomains
class McCracknsPrimeLaw:
    """
    A deterministic prime generator using motif-regime logic.

    Args:
        n_primes (int): Number of primes to generate.
        verbose (bool): Whether to print progress.
        progress_every (int): Print progress every N primes if verbose is enabled.
    """

    def __init__(self, *, n_primes: int = 100, verbose: bool = False,
                 progress_every: int = 1000):
        # User configuration
        self.n_primes       = max(2, n_primes)
        self.verbose        = verbose
        self.progress_every = max(1, progress_every)

        # Seed primes and motifs
        seed_primes = [2, 3, 5, 7, 11, 13]
        self.primes = seed_primes[:self.n_primes]
        seed_gaps   = [1, 2, 2, 4, 2]
        seed_labels = ["U1", "E1.0", "E1.0", "E1.1", "E1.0"]

        self.gaps   = seed_gaps[:len(self.primes) - 1]
        self.motifs = [("U1", 1)]  # (motif_label, run_count)
        self._run_counter = {"U1": 1, "E1.0": 0, "E1.1": 0}
        for lbl in seed_labels[:len(self.primes) - 1]:
            run = self._run_counter.get(lbl, 0) + 1
            self._run_counter[lbl] = run
            self.motifs.append((lbl, run))

        self.domains        = NumbersDomains()
        self.regime_idx     = 1
        self.primorial      = 2 * 3
        self.alphabet       = ["U1", "E1.0"]  # active motif set
        self._sort_alpha()
        self.used_motifs    = set(self.alphabet)
        self.regime_points  = []

        if len(self.primes) >= 6:
            self._bump_regime()  # expand alphabet

    @staticmethod
    def _gap(label: str) -> int:
        """
        Decode a motif label into its numeric gap.

        Example:
            "E1.0" → 2
            "E2.0" → 6
        """
        if label == "U1":
            return 1
        k, x = map(int, label[1:].split("."))
        if k == 1:
            return 1 << (x + 1)  # 2^(x+1)
        return (1 << (k - 1)) * (2 * x + 3)

    def _sort_alpha(self):
        """Sort the current alphabet based on motif gap and label specificity."""
        self.alphabet.sort(
            key=lambda lbl: (self._gap(lbl),) + tuple(map(int, lbl[1:].split(".")))
        )

    def _next_motif(self) -> str:
        """
        Compute the next unused motif by scanning upward in gap size.
        """
        g = self._gap(self.alphabet[-1]) + 2
        while True:
            lbl = self.domains.canonical_motif(g)
            if lbl != "U1" and lbl not in self.alphabet:
                return lbl
            g += 2

    def _bump_regime(self):
        """
        Expand regime by adding a new motif to the alphabet.
        Update regime index, primorial, and ensure alignment with sequence length.
        """
        self.regime_points.append(len(self.primes))
        self.alphabet.append(self._next_motif())
        self._sort_alpha()

        self.regime_idx += 1
        while len(self.primes) <= self.regime_idx:
            self._single_step(internal=True)
        self.primorial *= self.primes[self.regime_idx]
        self.used_motifs.clear()

    def _record(self, cand: int, gap: int, label: str):
        """
        Finalize candidate as next prime and update all records.
        """
        self.primes.append(cand)
        self.gaps.append(gap)
        run = self._run_counter.get(label, 0) + 1
        self._run_counter[label] = run
        self.motifs.append((label, run))
        self.used_motifs.add(label)

        if len(self.used_motifs) == len(self.alphabet):
            self._bump_regime()

    def _single_step(self, *, internal: bool = False):
        """
        Attempt to generate the next prime candidate via motifs.
        If no valid candidate is found, extend alphabet (motif innovation).
        """
        if len(self.primes) < 6:
            return

        while True:
            p_curr = self.primes[-1]
            P      = self.primorial

            for lbl in self.alphabet:
                gap  = self._gap(lbl)
                cand = p_curr + gap

                if gcd(cand, P) != 1:
                    continue  # eliminate mod-primorial composites

                while cand >= self.primes[self.regime_idx] ** 2:
                    self._bump_regime()
                    P = self.primorial
                    if gcd(cand, P) != 1:
                        break  # candidate now disqualified
                else:
                    self._record(cand, gap, lbl)

                    if self.verbose and not internal and \
                       len(self.primes) % self.progress_every == 0:
                        print(f"[prime {len(self.primes):>9}] {cand}")
                    return  # candidate accepted

            # no candidate matched, extend motif alphabet
            self.alphabet.append(self._next_motif())
            self._sort_alpha()

    def generate(self):
        """
        Generate all primes up to `n_primes` limit.
        Returns:
            List[int]: list of primes.
        """
        while len(self.primes) < self.n_primes:
            self._single_step()
        return self.primes

    def generate_one(self):
        """
        Advance by exactly one prime.

        Returns:
            Tuple[int, int, int, str]: (index, prime, gap, motif label)
        """
        if len(self.primes) < self.n_primes:
            self._single_step()
        idx   = len(self.primes)
        p     = self.primes[-1]
        gap   = 0 if idx == 1 else self.gaps[-1]
        motif = "U1" if idx == 1 else self.motifs[-1][0]
        return idx, p, gap, motif

    def stream_primes(self, *, start_idx=1):
        """
        Generator that yields primes and their metadata from a given index.

        Yields:
            Tuple[int, int, int, str]: (index, prime, gap, motif label)
        """
        while len(self.primes) < self.n_primes:
            self._single_step()
            idx = len(self.primes)
            if idx >= start_idx:
                p     = self.primes[-1]
                gap   = 0 if idx == 1 else self.gaps[-1]
                motif = "U1" if idx == 1 else self.motifs[-1][0]
                yield idx, p, gap, motif

    def get_primes(self):
        """Returns: list of generated primes."""
        return self.primes.copy()

    def get_gaps(self):
        """Returns: list of prime gaps."""
        return self.gaps.copy()

    def get_motifs(self):
        """Returns: list of motifs (excluding seed)."""
        return self.motifs[1:].copy()
