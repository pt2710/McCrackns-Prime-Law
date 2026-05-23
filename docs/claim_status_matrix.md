# MPL/TC V3 Claim Status Matrix

This repository document aligns implementation support with the attached V3 paper
(`10.5281/zenodo.20343409`).  It is an implementation-status map, not a
replacement for the paper.  When this document and code disagree, code is the
source of truth for what is implemented; when repository language and the V3
paper disagree, the V3 paper is the theory source of truth.

The current repository state includes the original bounded executable prefix / regression harness,
finite-prefix TC/Axis validation, and an executable derivation-level unbounded
lagged TC certificate-frontier scheduler.  PR #5 merged that scheduler into
`master` at `25421497ec8b4dfd2e33e9b5b135a93d2e6f6368` from implementation
commit `09157d77ae26baab8e942a18253ad537f5ac07b4`.

Final-paper layer order:

```text
TC -> Axis / First-Hole -> derivation-level lagged scheduler
   -> MPL regime-motif / Lex-Min readout
   -> MPL-normalized symbolic O(1)
```

Implementation boundary: the repository implements the derivation-level
frontier scheduler and finite-prefix regression evidence.  The paper's O(1)
claim is scoped to MPL-normalized motif-to-motif symbolic transition cost.  The
repository does not prove concrete data-structure O(1), bit-complexity O(1),
expanded integer output O(1), explicit certificate-frontier materialization
O(1), bounded lagged-closure compression, asymptotic runtime, or the full
theorem complex.

## Status Categories

- A: Fully implemented and tested.
- B: Finite-prefix implemented and tested.
- C: Partially implemented.
- D: Paper-only mathematical claim.
- E: Unsupported / unsafe to claim.
- F: Requires proof obligation before implementation can be claimed.

## Claim Matrix

| Claim | Repository support | Evidence | Status |
|---|---|---|---|
| U1 / gap = 1 is seed-only at `2 -> 3` | Runtime assertion and pytest coverage | `mccrackns_prime_law.py`, `tests/test_mpl_tc_architecture.py` | A - supported |
| Post-seed prime gaps are even | Runtime assertion and pytest coverage over bounded prefix | `mccrackns_prime_law.py`, `tests/test_mpl_tc_architecture.py` | A - supported |
| Bounded MPL prefix equals an independent reference prefix | Bounded finite tape is compared to a reference-only prime list | `tests/test_regression_against_reference.py` | B - finite-prefix validated |
| No GCD generator or GCD filter in MPL runtime | Runtime has no `gcd` call; tests guard against active use | `mccrackns_prime_law.py`, `tests/test_mpl_tc_architecture.py` | A - supported |
| No wheel, sieve, trial division, candidate scanning, frontier/event rejection as MPL runtime | Negative tests scan the MPL runtime; current runtime reads explicit motif transitions | `mccrackns_prime_law.py`, `tests/test_mpl_tc_architecture.py` | A - supported for current runtime |
| TC Unity / Even / Odd placement | Finite-prefix structural placement utility | `triadic_domains.py`, `tests/test_triadic_domains.py` | B - finite-prefix validated |
| O1 prime/free odd-axis | Odd realized primes are placed on `O1` | `triadic_domains.py`, `tests/test_triadic_domains.py` | B - finite-prefix validated |
| O2/O3/O4 lpf-strata for odd composites | Least-prime-factor placement for realized odd axes | `triadic_domains.py`, `tests/test_triadic_domains.py` | B - finite-prefix validated |
| Axis Law / First-Hole bridge examples | Finite realized-axis first-hole checks | `triadic_domains.py`, `tests/test_triadic_domains.py` | B - finite-prefix validated |
| MPL successor equals Axis Law successor for a finite prefix | Dedicated finite bridge verifier compares bounded MPL emissions to first-hole outputs | `verify_axis_bridge.py`, `tests/test_axis_bridge_consistency.py` | B - finite-prefix validated |
| Derivation-level lagged TC certificate-frontier scheduler | Executable scheduler with generated values, allowed/forbidden derivations, activation cohorts, active multipliers, known targets, delayed obstruction horizons, canonical value certificates, and prime buffers | `lagged_certificate_frontier.py`, `tests/test_lagged_certificate_frontier.py` | C - implemented with finite-prefix regression coverage |
| MPL regime-motif / Lex-Min readout of the TC frontier | Paper-level readout layer; bounded motif/regime harness remains for regression | `mccrackns_prime_law.py`, this matrix | C/D - implemented as bounded harness plus paper-level readout |
| Full compressed unbounded MPL regime-motif runtime | Not implemented as a standalone compressed symbolic runtime. Current MPL-facing runtime is `FINITE_MPL_GAP_TAPE` plus `RegimeMotifScheduler`; the implemented unbounded object is the derivation-level frontier scheduler. | `mccrackns_prime_law.py`, `lagged_certificate_frontier.py`, `docs/unbounded_scheduler_proof_obligations.md` | F - proof/implementation obligation |
| MPL-normalized motif-to-motif symbolic O(1) | Paper-level symbolic cost model. Repository documentation preserves the scope and exclusions. | `docs/unbounded_scheduler_proof_obligations.md`, `docs/theorem_implementation_map.md`, `cost_model.py` | D/F - paper claim plus repository claim-boundary tests |
| Concrete derivation-level scheduler runtime | Deterministic and check-free, but data-structure-dependent; tests do not assert O(1) runtime | `lagged_certificate_frontier.py`, `tests/test_lagged_certificate_frontier.py` | C - implemented with finite-prefix regression coverage |
| TC iff MPL bridge | Finite-prefix verifier exists; full equivalence remains paper-level unless formal obligations are discharged in code/proofs. | `verify_axis_bridge.py`, `docs/theorem_implementation_map.md` | D/F - paper claim with finite validation |
| Full theorem-complex support | Mapped, but not implemented as a formal proof system. | `docs/theorem_implementation_map.md` | C/F - partial map plus obligations |
| GCD sentinel status | Documentation and tests keep GCD as falsification/diagnostic only if ever introduced. | `README.md`, `tests/test_mpl_tc_architecture.py` | A - supported as policy |
| Repository implementation status | Bounded executable prefix / regression harness, finite TC/Axis validation, and derivation-level unbounded lagged scheduler with finite-prefix tests | `README.md`, this matrix, `tests/test_lagged_certificate_frontier.py` | C - implementation plus finite regression status |

## Terminology Alignment With V3 Paper

- Unity seed `U1`: `1` is structurally separated as the TC Unity seed and
  monoid identity.  In the MPL gap stream, `U1` labels the single seed
  transition `2 -> 3`.
- Pure dyadic powers / pure even lifts / even unity-sets: values
  `2, 4, 8, 16, ...` are pure lifts from Unity along the 2-axis.  This
  terminology does not make pure dyadic powers conventional primes.
- `O1` / first-order odd unity-sets: conventional odd primes
  `3, 5, 7, 11, ...` occupy the prime/free odd-axis `O1`.
- lpf-stratified odd composites: odd composites are placed by least prime
  factor: `O2` for lpf `3`, `O3` for lpf `5`, `O4` for lpf `7`, and so on.
  This is the canonical duplicate-free odd-composite representation.
- Mixed even composites `2^k m`: for `k >= 1` and odd `m > 1`, these are
  dyadic lifts of odd-domain factors.
- First-Hole language is reserved for the Axis Law relative to
  `M_j = <{2} union P_j>` and realized smooth-monoid coverage.  The
  repository must not make "holes" the primary name for conventional odd
  primes.

## Safe Repository Claim

The repository may safely claim that it provides a bounded executable
prefix/regression harness for MPL-facing motif transitions, finite-prefix
TC/U/E/O placement, finite Axis Law bridge checks, an executable
derivation-level lagged certificate-frontier scheduler, forbidden-mechanism
regression tests, and implementation-support audit scaffolding.  The paper may
cite PR #5 as repository support for the derivation-level scheduler and finite
R2/R3/R4/R10/first-20 regression contracts.

It may not claim that repository tests establish O(1), finite-prefix tests
establish asymptotic complexity, the repository supplies the paper proof,
concrete data structures are O(1), bit-complexity is O(1), or explicit
frontier materialization is O(1).

False claim to avoid: O(1) unit-cost theorem has been implemented or proved by tests.
