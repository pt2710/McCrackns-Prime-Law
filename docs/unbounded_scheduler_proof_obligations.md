# Unbounded MPL Scheduler Proof Obligations

The current paper states a derivation-level unbounded lagged TC
certificate-frontier scheduler and a stronger compressed regime/motif
successor claim.  The repository now implements the Section 6.5
derivation-level scheduler.  The older `mccrackns_prime_law.py` runtime remains
a bounded executable prefix / regression harness.

This document still tracks the remaining obligations before replacing the
bounded regime/motif harness with a compressed unbounded motif scheduler or
claiming the concrete derivation-level frontier representation has O(1)
runtime.  The lagged certificate-frontier scheduler is implemented separately.
The bounded lagged-closure compression theorem remains open.

## Required Obligations Before Replacing The Bounded Runtime

1. Regime state:
   Define a concrete, serializable runtime state for regime index, active
   motif alphabet, motif usage, and regime transitions beyond the current
   bounded prefix.

2. Active motif alphabet construction:
   Provide an executable compressed construction of the legal motif alphabet
   `A_k` that does not query candidate primality, divisibility, `gcd`, wheel
   residues as a generator, or membership in `M_j`.

3. Lex-minimal motif selection:
   Specify how the least legal motif is selected in constant scheduler steps
   without scanning candidate integers or rejecting composites from an event
   table.

4. Regime innovation update:
   Define the update rule for motif innovations, regime bumps, and exhausted
   motif alphabets without falling back to a hardcoded gap schedule.

5. Successor emission:
   Prove that the emitted value `p_j + g` equals the next prime and that the
   implementation can execute this transition using the regime/motif state
   alone.

6. Axis Law equivalence:
   Prove that the runtime output agrees with
   `min(N >= 1 \\ M_j)` for `M_j = <{2} union P_j>` while keeping the
   First-Hole construction in the proof/validation layer, not the runtime.

7. Sentinel separation:
   If diagnostic assertions are present, prove they have no control edge into
   motif selection and cannot act as a generator, filter, sieve, primality test,
   or candidate-rejection mechanism.

8. Cost model:
   Provide a formal unit-cost model, invariant reasoning for constant or
   amortized scheduler steps, and a clear separation from arithmetic bit costs,
   printing costs, Python data-structure overhead, and finite-prefix timing.

9. Validation plan:
   Define finite-prefix tests against independent references and bridge
   verification without turning the reference oracle or Axis Law verifier into
   the MPL runtime.

## Current Decision

The repository should continue to describe `mccrackns_prime_law.py` as a
bounded executable prefix / regression harness until these obligations are
discharged by code, tests, and proof artifacts.  The new
`lagged_certificate_frontier.py` module is the paper-level frontier scheduler,
with data-structure-dependent concrete cost.
