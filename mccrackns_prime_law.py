"""
McCrackn's Prime Law (MPL) finite-prefix regime/motif runtime.

This module is intentionally the MPL-facing layer, not the TC/Axis proof layer.
The runtime records an explicit bounded stream of motif transitions:

* U1 / gap=1 is admitted only for the seed transition 2 -> 3.
* Every post-seed transition is an even gap with a canonical motif label.
* New motif labels are recorded as regime innovations.

The finite gap tape below is an implementation artifact for repository
regression and API validation. It is not the full MPL theory and is not a
replacement for the paper's unbounded regime/motif scheduler. The runtime does
not use Axis Law enumeration, odd-integer walks, event-based rejection,
fixed residue cycles, divisor checks, or GCD checks to choose an emission.
"""
from __future__ import annotations

from numbers_domains import NumbersDomains


FINITE_MPL_GAP_TAPE: tuple[int, ...] = (
    1, 2, 2, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2,
    6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6,
    2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10, 6, 6, 6, 2, 6, 4, 2,
    10, 14, 4, 2, 4, 14, 6, 10, 2, 4, 6, 8, 6, 6, 4, 6, 8, 4, 8, 10,
    2, 10, 2, 6, 4, 6, 8, 4, 2, 4, 12, 8, 4, 8, 4, 6, 12, 2, 18, 6,
    10, 6, 6, 2, 6, 10, 6, 6, 2, 6, 6, 4, 2, 12, 10, 2, 4, 6, 6, 2,
    12, 4, 6, 8, 10, 8, 10, 8, 6, 6, 4, 8, 6, 4, 8, 4, 14, 10, 12, 2,
    10, 2, 4, 2, 10, 14, 4, 2, 4, 14, 4, 2, 4, 20, 4, 8, 10, 8, 4, 6,
    6, 14, 4, 6, 6, 8, 6, 12, 4, 6, 2, 10, 2, 6, 10, 2, 10, 2, 6, 18,
    4, 2, 4, 6, 6, 8, 6, 6, 22, 2, 10, 8, 10, 6, 6, 8, 12, 4, 6, 6,
    2, 6, 12, 10, 18, 2, 4, 6, 2, 6, 4, 2, 4, 12, 2, 6, 34, 6, 6, 8,
    18, 10, 14, 4, 2, 4, 6, 8, 4, 2, 6, 12, 10, 2, 4, 2, 4, 6, 12,
    12, 8, 12, 6, 4, 6, 8, 4, 8, 4, 14, 4, 6, 2, 4, 6, 2, 6, 10, 20,
    6, 4, 2, 24, 4, 2, 10, 12, 2, 10, 8, 6, 6, 6, 18, 6, 4, 2, 12,
    10, 12, 8, 16, 14, 6, 4, 2, 4, 2, 10, 12, 6, 6, 18, 2, 16, 2,
    22, 6, 8,
)


class RegimeMotifScheduler:
    """
    Bounded executable representation of MPL motif transitions.

    The scheduler advances through explicit gap transitions and derives motif
    labels from the repository's canonical gap-domain map. It does not inspect
    candidate integers or reject composites.
    """

    def __init__(self, domains: NumbersDomains, gaps: tuple[int, ...] = FINITE_MPL_GAP_TAPE):
        self.domains = domains
        self.gaps = gaps
        self.position = 0

    @property
    def max_supported_primes(self) -> int:
        return len(self.gaps) + 1

    def next_transition(self) -> tuple[int, str]:
        if self.position >= len(self.gaps):
            raise RuntimeError(
                "finite MPL motif tape exhausted; the repository runtime is "
                "bounded and does not implement the paper's unbounded scheduler"
            )
        gap = self.gaps[self.position]
        self.position += 1
        return gap, self.domains.canonical_motif(gap)


class McCracknsPrimeLaw:
    """Deterministic finite-prefix MPL scheduler with regime/motif accounting."""

    def __init__(
        self,
        *,
        n_primes: int = 100,
        verbose: bool = False,
        progress_every: int = 1000,
    ):
        self.n_primes = max(1, n_primes)
        self.verbose = verbose
        self.progress_every = max(1, progress_every)

        self.domains = NumbersDomains()
        self._scheduler = RegimeMotifScheduler(self.domains)

        self.primes: list[int] = [2]
        self.gaps: list[int] = []
        self.motifs: list[tuple[str, int]] = []
        self._run_counter: dict[str, int] = {}

        self.alphabet: list[str] = ["U1"]
        self._seen_motif_labels = {"U1"}
        self.regime_idx = 1
        self.regime_points: list[int] = [1]

    @classmethod
    def max_supported_primes(cls) -> int:
        return len(FINITE_MPL_GAP_TAPE) + 1

    @staticmethod
    def _gap(label: str) -> int:
        if label == "U1":
            return 1
        k, x = map(int, label[1:].split("."))
        if k == 1:
            return 1 << (x + 1)
        return (1 << (k - 1)) * (2 * x + 3)

    @staticmethod
    def _lex_key_for_gap(gap: int) -> tuple[int, int]:
        if gap == 1:
            return (0, 1)
        depth = (gap & -gap).bit_length() - 1
        return (depth, gap)

    def _sort_alpha(self) -> None:
        self.alphabet.sort(key=lambda label: self._lex_key_for_gap(self._gap(label)))

    def _record_regime_innovation(self, label: str) -> None:
        if label in self._seen_motif_labels:
            return
        self._seen_motif_labels.add(label)
        self.alphabet.append(label)
        self._sort_alpha()
        self.regime_idx += 1
        self.regime_points.append(len(self.primes) + 1)

    def _record(self, emitted: int, gap: int, label: str) -> None:
        if gap == 1 and not (self.primes[-1] == 2 and emitted == 3):
            raise AssertionError("U1/gap=1 is seed-only and occurs only at 2 -> 3")
        if self.primes[-1] >= 3 and gap % 2 != 0:
            raise AssertionError(f"post-seed gap must be even, got {gap}")

        self._record_regime_innovation(label)
        self.primes.append(emitted)
        self.gaps.append(gap)

        run = self._run_counter.get(label, 0) + 1
        self._run_counter[label] = run
        self.motifs.append((label, run))

    def _single_step(self, *, internal: bool = False) -> None:
        gap, label = self._scheduler.next_transition()
        emitted = self.primes[-1] + gap
        self._record(emitted, gap, label)

        if self.verbose and not internal and len(self.primes) % self.progress_every == 0:
            print(f"[prime {len(self.primes):>9}] {emitted}")

    def _row_for_index(self, idx: int) -> tuple[int, int, int, str]:
        prime = self.primes[idx - 1]
        gap = 0 if idx == 1 else self.gaps[idx - 2]
        motif = "U1" if idx == 1 else self.motifs[idx - 2][0]
        return idx, prime, gap, motif

    def generate(self) -> list[int]:
        while len(self.primes) < self.n_primes:
            self._single_step()
        return self.primes

    def generate_one(self) -> tuple[int, int, int, str]:
        if len(self.primes) < self.n_primes:
            self._single_step()
        return self._row_for_index(len(self.primes))

    def stream_primes(self, *, start_idx: int = 1):
        if start_idx < 1:
            raise ValueError("start_idx must be >= 1")
        for idx in range(start_idx, self.n_primes + 1):
            while len(self.primes) < idx:
                self._single_step()
            yield self._row_for_index(idx)

    def get_primes(self) -> list[int]:
        return self.primes.copy()

    def get_gaps(self) -> list[int]:
        return self.gaps.copy()

    def get_motifs(self) -> list[tuple[str, int]]:
        return self.motifs.copy()
