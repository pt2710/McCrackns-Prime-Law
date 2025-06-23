# mccrackns_prime_law.py

from math import gcd
from numbers_domains import NumbersDomains

class McCracknsPrimeLaw:

    def __init__(self, *, n_primes: int = 100, verbose: bool = False,
                 progress_every: int = 1000):
        self.n_primes       = max(2, n_primes)
        self.verbose        = verbose
        self.progress_every = max(1, progress_every)

        seed_primes = [2, 3, 5, 7, 11, 13]
        self.primes = seed_primes[:self.n_primes]
        seed_gaps   = [1, 2, 2, 4, 2] 
        seed_labels = ["U1", "E1.0", "E1.0", "E1.1", "E1.0"]

        self.gaps   = seed_gaps[:len(self.primes)-1]
        self.motifs = [("U1", 1)]
        self._run_counter = {"U1": 1, "E1.0": 0, "E1.1": 0}
        for lbl in seed_labels[:len(self.primes)-1]:
            run = self._run_counter.get(lbl, 0) + 1
            self._run_counter[lbl] = run
            self.motifs.append((lbl, run))

        self.domains      = NumbersDomains()
        self.regime_idx   = 1
        self.primorial    = 2 * 3
        self.alphabet     = ["U1", "E1.0"]
        self._sort_alpha()
        self.used_motifs  = set(self.alphabet)
        self.regime_points = []

        if len(self.primes) >= 6:
            self._bump_regime()

    @staticmethod
    def _gap(label: str) -> int:
        if label == "U1":
            return 1
        k, x = map(int, label[1:].split("."))
        if k == 1:
            return 1 << (x + 1)
        return (1 << (k - 1)) * (2 * x + 3)

    def _sort_alpha(self):
        self.alphabet.sort(
            key=lambda lbl: (self._gap(lbl),) + tuple(map(int, lbl[1:].split(".")))
        )

    def _next_motif(self) -> str:
        g = self._gap(self.alphabet[-1]) + 2
        while True:
            lbl = self.domains.canonical_motif(g)
            if lbl != "U1" and lbl not in self.alphabet:
                return lbl
            g += 2

    def _bump_regime(self):
        self.regime_points.append(len(self.primes))

        self.alphabet.append(self._next_motif())
        self._sort_alpha()

        self.regime_idx += 1
        while len(self.primes) <= self.regime_idx:
            self._single_step(internal=True)
        self.primorial *= self.primes[self.regime_idx]

        self.used_motifs.clear()

    def _record(self, cand: int, gap: int, label: str):
        self.primes.append(cand)
        self.gaps.append(gap)
        run = self._run_counter.get(label, 0) + 1
        self._run_counter[label] = run
        self.motifs.append((label, run))

        self.used_motifs.add(label)
        if len(self.used_motifs) == len(self.alphabet):
            self._bump_regime()

   
    def _single_step(self, *, internal: bool = False):
        
        if len(self.primes) < 6:
            return

        while True:
            p_curr = self.primes[-1]
            P      = self.primorial 

            for lbl in self.alphabet:
                gap  = self._gap(lbl)
                cand = p_curr + gap

                if gcd(cand, P) != 1:
                    continue 

                while cand >= self.primes[self.regime_idx] ** 2:
                    self._bump_regime() 
                    P = self.primorial
                    if gcd(cand, P) != 1:
                        break  
                else:
                    self._record(cand, gap, lbl)

                    if self.verbose and not internal and \
                       len(self.primes) % self.progress_every == 0:
                        print(f"[prime {len(self.primes):>9}] {cand}")
                    return 

            self.alphabet.append(self._next_motif())
            self._sort_alpha()

    def generate(self):
        while len(self.primes) < self.n_primes:
            self._single_step()
        return self.primes
    
    def generate_one(self):
        """Advance by exactly **one** prime and return (index, prime, gap, motif)."""
        if len(self.primes) < self.n_primes:
            self._single_step()
        idx  = len(self.primes)
        p    = self.primes[-1]
        gap  = 0 if idx == 1 else self.gaps[-1]
        motif = "U1" if idx == 1 else self.motifs[-1][0]
        return idx, p, gap, motif


    def stream_primes(self, *, start_idx=1):
        """Yield (idx, prime, gap, motif) indefinitely up to n_primes."""
        while len(self.primes) < self.n_primes:
            self._single_step()
            idx = len(self.primes)
            if idx >= start_idx:
                p    = self.primes[-1]
                gap  = 0 if idx == 1 else self.gaps[-1]
                motif = "U1" if idx == 1 else self.motifs[-1][0]
                yield idx, p, gap, motif

    def get_primes(self):
        return self.primes.copy()

    def get_gaps(self):
        return self.gaps.copy()

    def get_motifs(self):
        return self.motifs[1:].copy() 
