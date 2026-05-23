"""
Operation-count scaffolding for MPL/TC implementation support.

This module does not prove the V3 O(1) theorem.  It records a bounded-prefix
unit-cost accounting framework for the current finite motif tape runtime and
keeps arithmetic bit complexity, Python data-structure costs, and the paper's
unbounded scheduler proof obligations separate.
"""
from __future__ import annotations

from dataclasses import dataclass

from mccrackns_prime_law import McCracknsPrimeLaw


UNIT_COST_ASSUMPTIONS: tuple[str, ...] = (
    "A scheduler-level tape transition read is counted as one symbolic step.",
    "A motif-label lookup is counted as one symbolic step.",
    "A successor addition is counted as one symbolic step.",
    "Seed/parity guard evaluation is counted as one symbolic step.",
    "Motif/regime bookkeeping is counted as one symbolic step.",
    "Arithmetic bit complexity, printing, Python sorting/cache overhead, and wall-clock timing are outside this count.",
)


@dataclass(frozen=True)
class TransitionCost:
    """Symbolic operation count for one bounded-prefix transition."""

    index: int
    emitted_prime: int
    gap: int
    motif: str
    unit_scheduler_steps: int


@dataclass(frozen=True)
class CostAuditReport:
    """Summary of bounded-prefix operation-count instrumentation."""

    transition_costs: tuple[TransitionCost, ...]
    assumptions: tuple[str, ...]
    bounded_prefix_only: bool
    proves_o1: bool
    limitation: str

    @property
    def max_unit_scheduler_steps(self) -> int:
        return max((cost.unit_scheduler_steps for cost in self.transition_costs), default=0)

    @property
    def min_unit_scheduler_steps(self) -> int:
        return min((cost.unit_scheduler_steps for cost in self.transition_costs), default=0)

    @property
    def constant_within_prefix(self) -> bool:
        return self.max_unit_scheduler_steps == self.min_unit_scheduler_steps


def audit_bounded_prefix_cost(n_primes: int = 20) -> CostAuditReport:
    """
    Count symbolic scheduler operations for the bounded MPL prefix.

    The count is intentionally conservative and explanatory.  It can show that
    this instrumentation uses a fixed symbolic count on the implemented prefix;
    it cannot prove the paper's unbounded O(1) theorem.
    """
    if n_primes < 2:
        raise ValueError("n_primes must be at least 2")
    if n_primes > McCracknsPrimeLaw.max_supported_primes():
        raise ValueError("n_primes exceeds the bounded MPL prefix")

    law = McCracknsPrimeLaw(n_primes=n_primes)
    rows = list(law.stream_primes(start_idx=2))
    costs = tuple(
        TransitionCost(
            index=index,
            emitted_prime=prime,
            gap=gap,
            motif=motif,
            unit_scheduler_steps=5,
        )
        for index, prime, gap, motif in rows
    )
    return CostAuditReport(
        transition_costs=costs,
        assumptions=UNIT_COST_ASSUMPTIONS,
        bounded_prefix_only=True,
        proves_o1=False,
        limitation=(
            "This audit covers the bounded finite motif tape only. It does not "
            "discharge the formal unbounded scheduler, invariant, amortization, "
            "or bit-complexity obligations required for the V3 O(1) claim."
        ),
    )
