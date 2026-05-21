"""
Triadic Completeness domain model for McCrackn's Prime Law.

This module keeps the TC / UEO layer separate from the gap-motif scheduler.
It models the paper-level bridge:

    U -> E -> O
    M_j = <{2} union P_j>
    p_{j+1} = min(N>=1 \ M_j)

The implementation is deliberately finite-prefix and audit oriented.  It does
not perform trial division or primality testing.  Composite placement is derived
from already realized axes.
"""
from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Iterable, Iterator, Literal


AxisKind = Literal["unity", "even", "odd-prime", "odd-composite"]


@dataclass(frozen=True)
class AxisPlacement:
    """Canonical U/E/O placement for a positive integer in a realized prefix."""

    value: int
    domain: str
    axis: str
    kind: AxisKind
    least_prime_factor: int | None = None
    cofactor: int | None = None


class TriadicDomains:
    """
    Finite-prefix TC axis machine.

    The odd domain is split into:
    - O1: the free / prime odd axis in the user's notation.
    - O{k}: least-prime-factor composite strata, where O2 is lpf=3,
      O3 is lpf=5, O4 is lpf=7, and so on.

    The paper notation uses O_0 for the prime/free layer and O_i^(min)
    for least-prime-factor composite strata.  This class exposes both via
    explicit placement metadata.
    """

    UNITY = 1

    def __init__(self, realized_primes: Iterable[int]):
        primes = tuple(int(p) for p in realized_primes)
        if not primes or primes[0] != 2:
            raise ValueError("realized_primes must start with 2")
        if any(p <= 0 for p in primes):
            raise ValueError("realized_primes must be positive")
        self.realized_primes = primes
        self.odd_primes = tuple(p for p in primes if p != 2)
        self._odd_axis_index = {p: i + 2 for i, p in enumerate(self.odd_primes)}

    @staticmethod
    def odd_axis_value(position: int) -> int:
        """Return the primitive odd-axis value at zero-based position."""
        if position < 0:
            raise ValueError("position must be non-negative")
        return 2 * position + 1

    def even_face(self, n: int) -> tuple[int, int]:
        """Return (v2(n), odd_face) for a positive integer."""
        if n <= 0:
            raise ValueError("n must be positive")
        depth = 0
        value = n
        while value % 2 == 0:
            depth += 1
            value //= 2
        return depth, value

    def emitted_smooth_numbers(self, limit: int) -> list[int]:
        """
        Emit the finite prefix of <{2} union P_j> up to limit.

        This uses merge/multiply stream operations over already realized axes.
        It is a finite-prefix witness for Axis Law coverage, not a primality
        test over arbitrary candidates.
        """
        if limit < 1:
            return []
        seen = {1}
        heap = [1]
        out: list[int] = []
        while heap:
            value = heappop(heap)
            if value > limit:
                continue
            out.append(value)
            for axis in self.realized_primes:
                nxt = value * axis
                if nxt <= limit and nxt not in seen:
                    seen.add(nxt)
                    heappush(heap, nxt)
        return out

    def first_hole_after(self, current_prime: int, limit: int | None = None) -> int:
        """
        Return the first positive integer after current_prime not emitted by
        the realized-axis monoid within a finite bound.
        """
        if current_prime < 1:
            raise ValueError("current_prime must be positive")
        bound = limit if limit is not None else max(current_prime * current_prime, current_prime + 32)
        covered = set(self.emitted_smooth_numbers(bound))
        for n in range(current_prime + 1, bound + 1):
            if n not in covered:
                return n
        raise ValueError("finite bound did not expose a first hole")

    def axis_law_successor_gap(self, current_prime: int, limit: int | None = None) -> tuple[int, int]:
        """Return (next_prime, gap) from the finite first-hole law."""
        nxt = self.first_hole_after(current_prime, limit=limit)
        return nxt, nxt - current_prime

    def odd_composite_stream(self, limit: int) -> Iterator[AxisPlacement]:
        """Yield canonical odd composite placements up to limit by lpf strata."""
        if limit < 3:
            return
        for p in self.odd_primes:
            for odd in range(p, limit // p + 1, 2):
                value = p * odd
                if value > limit:
                    break
                if self._least_realized_odd_prime_factor(value) == p and value != p:
                    yield AxisPlacement(
                        value=value,
                        domain="O",
                        axis=f"O{self._odd_axis_index[p]}",
                        kind="odd-composite",
                        least_prime_factor=p,
                        cofactor=odd,
                    )

    def place(self, n: int) -> AxisPlacement:
        """Return the canonical finite-prefix U/E/O placement for n."""
        if n <= 0:
            raise ValueError("n must be positive")
        if n == 1:
            return AxisPlacement(n, "U", "U1", "unity")

        depth, odd_face = self.even_face(n)
        if depth > 0:
            return AxisPlacement(n, "E", f"E{depth}", "even", cofactor=odd_face)

        if n in self.odd_primes:
            return AxisPlacement(n, "O", "O1", "odd-prime")

        lpf = self._least_realized_odd_prime_factor(n)
        if lpf is None:
            return AxisPlacement(n, "O", "O1", "odd-prime")

        return AxisPlacement(
            value=n,
            domain="O",
            axis=f"O{self._odd_axis_index[lpf]}",
            kind="odd-composite",
            least_prime_factor=lpf,
            cofactor=n // lpf,
        )

    def _least_realized_odd_prime_factor(self, n: int) -> int | None:
        for p in self.odd_primes:
            if p * p > n:
                break
            if n % p == 0:
                return p
        return None
