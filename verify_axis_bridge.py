"""
Finite-prefix Axis Law bridge verifier.

This module compares the bounded MPL prefix against the TC/Axis first-hole
identity for small realized-axis prefixes.  It is a validation/proof-layer tool,
not the MPL runtime.  First-Hole language here is always relative to
M_j = <{2} union P_j> and realized smooth-monoid coverage.
"""
from __future__ import annotations

from dataclasses import dataclass

from mccrackns_prime_law import McCracknsPrimeLaw
from triadic_domains import TriadicDomains


@dataclass(frozen=True)
class AxisBridgeResult:
    """One finite-prefix comparison between MPL and Axis Law output."""

    stage: int
    realized_axes: tuple[int, ...]
    current_prime: int
    mpl_next_prime: int
    axis_next_prime: int
    mpl_gap: int
    axis_gap: int

    @property
    def matches(self) -> bool:
        return self.mpl_next_prime == self.axis_next_prime and self.mpl_gap == self.axis_gap


def verify_axis_bridge_prefix(n_primes: int = 10) -> list[AxisBridgeResult]:
    """
    Compare bounded MPL successors with finite Axis Law first-hole successors.

    The verifier checks stages `1..n_primes-1`.  At stage `j`, realized axes are
    exactly the bounded MPL prefix primes through `p_j`, and the Axis check is
    performed by `TriadicDomains` over a finite smooth-monoid prefix.
    """
    if n_primes < 2:
        raise ValueError("n_primes must be at least 2")
    if n_primes > McCracknsPrimeLaw.max_supported_primes():
        raise ValueError("n_primes exceeds the bounded MPL prefix")

    law = McCracknsPrimeLaw(n_primes=n_primes)
    primes = law.generate()
    gaps = law.get_gaps()

    results: list[AxisBridgeResult] = []
    for stage in range(1, n_primes):
        current = primes[stage - 1]
        expected_next = primes[stage]
        domains = TriadicDomains(primes[:stage])
        bound = max(current * current, expected_next + 1)
        axis_next, axis_gap = domains.axis_law_successor_gap(current, limit=bound)
        results.append(
            AxisBridgeResult(
                stage=stage,
                realized_axes=tuple(primes[:stage]),
                current_prime=current,
                mpl_next_prime=expected_next,
                axis_next_prime=axis_next,
                mpl_gap=gaps[stage - 1],
                axis_gap=axis_gap,
            )
        )
    return results


def assert_axis_bridge_prefix(n_primes: int = 10) -> None:
    """Raise an AssertionError if any finite-prefix bridge comparison fails."""
    mismatches = [result for result in verify_axis_bridge_prefix(n_primes) if not result.matches]
    if mismatches:
        raise AssertionError(f"Axis bridge mismatch: {mismatches[0]}")
