# Unbounded MPL Scheduler Proof Obligations

The current paper states a derivation-level unbounded lagged TC
certificate-frontier scheduler and then reads MPL as the regime-motif /
Lex-Min readout of that TC certificate frontier.  The repository now implements
the derivation-level scheduler through PR #5 on `master`
(`25421497ec8b4dfd2e33e9b5b135a93d2e6f6368`, from implementation commit
`09157d77ae26baab8e942a18253ad537f5ac07b4`).  The older
`mccrackns_prime_law.py` runtime remains a bounded executable prefix /
regression harness.

This document still tracks the remaining obligations before replacing the
bounded regime/motif harness with a compressed unbounded motif scheduler or
claiming the concrete derivation-level frontier representation has O(1)
runtime.  The paper's O(1) claim is scoped to MPL-normalized motif-to-motif
symbolic transition cost; it is not a claim about bit-complexity, expanded
integer output, explicit certificate-frontier materialization, whole-regime
materialization, concrete data-structure runtime, repository tests, or
finite-prefix implementation evidence.  The bounded lagged-closure compression theorem remains open.

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
   Preserve the final paper's MPL-normalized motif-to-motif symbolic O(1)
   scope while providing any additional invariant reasoning needed before a
   compressed implementation can claim constant or amortized scheduler steps.
   Keep this separate from arithmetic bit costs, expanded integer output,
   explicit frontier materialization, whole-regime materialization, Python
   data-structure overhead, and finite-prefix timing.

9. Validation plan:
   Define finite-prefix tests against independent references and bridge
   verification without turning the reference oracle or Axis Law verifier into
   the MPL runtime.

## Current Decision

The repository should continue to describe `mccrackns_prime_law.py` as a
bounded executable prefix / regression harness until these obligations are
discharged by code, tests, and proof artifacts.  The new
`lagged_certificate_frontier.py` module is the paper-level frontier scheduler,
with deterministic check-free behavior and data-structure-dependent concrete
cost.  Repository tests are finite-prefix regression guardrails, not proof that
finite-prefix tests establish asymptotic complexity, concrete O(1), bounded
lagged-closure compression, or the full theorem complex.
