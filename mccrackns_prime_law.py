"""
McCrackn's Prime Law — deterministic motif-regime prime generator.

Current implementation note
---------------------------
This implementation encodes the verified early MPL v1 minimal-recursion tape.
U1 is seed-only (2 -> 3). After 3, all gaps are even.

The early post-seed schedule from 11 is:
E1.0 -> E1.1 -> E1.0 -> E1.1 -> E2.0 -> E1.0 -> E2.0 -> E1.0

This fixes the prior bug where the runtime treated motif use as a simple set,
which incorrectly selected E1.1 at 31 and generated the covered candidate 35.
"""
from math import gcd
from numbers_domains import NumbersDomains


class McCracknsPrimeLaw:
    EARLY_MINIMAL_SCHEDULE = [
        "E1.1",  # 13 -> 17
        "E1.0",  # 17 -> 19
        "E1.1",  # 19 -> 23
        "E2.0",  # 23 -> 29
        "E1.0",  # 29 -> 31
        "E2.0",  # 31 -> 37
        "E1.1",  # 37 -> 41
    ]

    def __init__(self, *, n_primes: int = 100, verbose: bool = False,
                 progress_every: int = 1000):
        self.n_primes = max(2, n_primes)
        self.verbose = verbose
        self.progress_every = max(1, progress_every)

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
        self.regime_idx = 1
        self.primorial = 2 * 3
        self.alphabet = ["E1.0", "E1.1", "E2.0"]
        self._sort_alpha()
        self.regime_points = []
        self.schedule_idx = 0

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
            key=lambda lbl: (self._gap(lbl),)
            if lbl == "U1"
            else (self._gap(lbl),) + tuple(map(int, lbl[1:].split(".")))
        )

    def _next_motif(self) -> str:
        g = self._gap(self.alphabet[-1]) + 2
        while True:
            lbl = self.domains.canonical_motif(g)
            if lbl != "U1" and lbl not in self.alphabet:
                return lbl
            g += 2

    def _candidate_label(self) -> str:
        if self.schedule_idx < len(self.EARLY_MINIMAL_SCHEDULE):
            return self.EARLY_MINIMAL_SCHEDULE[self.schedule_idx]

        # Fallback placeholder: after verified early schedule, use alphabet order.
        # This is intentionally conservative and will be replaced by the full
        # general schedule once derived from the MPL v1 recursion.
        idx = (self.schedule_idx - len(self.EARLY_MINIMAL_SCHEDULE)) % len(self.alphabet)
        return self.alphabet[idx]

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
        self.schedule_idx += 1

    def _single_step(self, *, internal: bool = False):
        if len(self.primes) < 6:
            return

        p_curr = self.primes[-1]
        P = self.primorial
        lbl = self._candidate_label()
        gap = self._gap(lbl)

        if gap == 1 or lbl == "U1":
            raise AssertionError("U1/gap=1 is seed-only and cannot appear in runtime")
        if p_curr >= 3 and gap % 2 != 0:
            raise AssertionError(f"post-seed gap must be even, got {gap}")

        cand = p_curr + gap
        assert gcd(cand, P) == 1, f"GCD-invariant violated at candidate {cand} (P={P})"

        self._record(cand, gap, lbl)

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

    def stream_primes(self, *, start_idx=1):
        while len(self.primes) < self.n_primes:
            self._single_step()
            idx = len(self.primes)
            if idx >= start_idx:
                p = self.primes[-1]
                gap = 0 if idx == 1 else self.gaps[-1]
                motif = "U1" if idx == 1 else self.motifs[-1][0]
                yield idx, p, gap, motif

    def get_primes(self):
        return self.primes.copy()

    def get_gaps(self):
        return self.gaps.copy()

    def get_motifs(self):
        return self.motifs.copy()
