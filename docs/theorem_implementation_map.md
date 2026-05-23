# V3 Theorem And Implementation Map

This theorem map records repository support for selected V3 claims.

This map links major final V3 paper claims to repository support.  It is not a
proof assistant transcript and does not claim full formalization of the theorem
complex.  It follows the paper's red thread:

```text
TC -> Axis / First-Hole -> derivation-level lagged scheduler
   -> MPL regime-motif / Lex-Min readout
   -> MPL-normalized symbolic O(1)
```

| V3 theorem / lemma / claim | Mathematical claim | Implementation object | Test object | Status | Notes |
|---|---|---|---|---|---|
| U1 seed-only parity constraint | Gap `1` occurs only at `2 -> 3`; later gaps are even | `McCracknsPrimeLaw._record` | `tests/test_mpl_tc_architecture.py` | implemented | Runtime assertion plus bounded-prefix test |
| TC Unity domain | `1` is Unity seed / monoid identity, structurally separated from Odd | `TriadicDomains.place` | `tests/test_triadic_domains.py` | finite-prefix validated | `place(1)` returns `U` / `U1` |
| Even-domain dyadic placement | Even numbers decompose by dyadic depth and odd face | `TriadicDomains.even_face`, `TriadicDomains.place` | `tests/test_triadic_domains.py` | finite-prefix validated | Covers pure dyadic powers and mixed even composites structurally |
| Odd-domain completeness by least prime factor | Odd values are O1 primes or unique lpf composite strata | `TriadicDomains.place`, `odd_composite_stream` | `tests/test_triadic_domains.py` | finite-prefix validated | O2/O3/O4 examples are tested |
| O-axis notation and lpf strata | O1 is prime/free; O2/O3/O4 are lpf strata | `TriadicDomains` | `tests/test_triadic_domains.py` | finite-prefix validated | Avoids duplicate raw-axis placement such as `15` in two rows |
| Axis / First-Hole bridge | The next free odd boundary is identified relative to `M_j = <{2} union P_j>` | `verify_axis_bridge.py` | `tests/test_axis_bridge_consistency.py` | finite-prefix validated | Full equivalence remains paper-level |
| Sentinel non-generativity | GCD/assertions, if present, are falsification-only | Policy in docs; no GCD in runtime | `tests/test_mpl_tc_architecture.py` | implemented as absence/policy | No active GCD selector is present |
| Bounded MPL regime/motif prefix | Repository emits a finite prefix with motif labels and regime accounting | `mccrackns_prime_law.py` | `tests/test_regression_against_reference.py` | finite-prefix validated | Uses `FINITE_MPL_GAP_TAPE`; not the full theory |
| Section 4 derivation-level lagged TC certificate-frontier scheduler | Deterministic, check-free frontier scheduler with generated values, allowed/forbidden derivations, activation cohorts, active multipliers, known targets, prime buffers, and delayed obstruction horizons | `lagged_certificate_frontier.py` | `tests/test_lagged_certificate_frontier.py` | implemented with finite-prefix regression coverage | PR #5 merged this support at `25421497ec8b4dfd2e33e9b5b135a93d2e6f6368`; implementation commit `09157d77ae26baab8e942a18253ad537f5ac07b4` |
| R2/R3/R4/R10 and first-20 scheduler contracts | Early recursion contracts, delayed obstruction horizon, derivation-level alias handling, and prefix continuation | `lagged_certificate_frontier.py` | `tests/test_lagged_certificate_frontier.py` | implemented and tested on finite prefixes | Includes R3 generation of `55`, `65`, `75`; `49` delayed; `47` and `53` withheld until the delayed obstruction clears |
| Section 5, MPL as regime-motif / Lex-Min readout of TC frontier | MPL is the regime-motif / Lex-Min readout of the TC certificate frontier | `mccrackns_prime_law.py`, docs | `tests/test_mpl_tc_architecture.py`, `tests/test_claim_status_docs.py` | bounded implementation plus paper-level claim | The compressed symbolic readout is not a concrete O(1) runtime claim |
| Section 5.10, MPL-normalized symbolic complexity | O(1) applies to motif-to-motif symbolic transition cost under the MPL-normalized cost model | `cost_model.py`, claim-status docs | `tests/test_cost_model_instrumentation.py`, `tests/test_claim_status_docs.py` | paper-level symbolic claim with repository boundary checks | Excludes bit complexity, expanded integer output, explicit frontier materialization, whole-regime materialization, concrete data-structure runtime, repository tests, and finite-prefix evidence; concrete runtime proof obligation remains separate |
| Concrete derivation-level runtime cost | Explicit certificate-frontier materialization has data-structure-dependent cost | `lagged_certificate_frontier.py`, `cost_model.py` | `tests/test_lagged_certificate_frontier.py`, `tests/test_cost_model_instrumentation.py` | implemented, not claimed O(1) | The implementation validates finite-prefix regression contracts but does not prove bounded lagged-closure compression |
| TC iff MPL bridge | Structural TC coverage and MPL successor agree globally | Finite verifier only | `tests/test_axis_bridge_consistency.py` | paper-only with finite validation | TC alone is not used as a prime generator |
| U/E/O terminology | Unity seed, even unity-sets, first-order odd unity-sets, lpf odd composites, mixed even composites | `docs/claim_status_matrix.md`, `triadic_domains.py` | `tests/test_claim_status_docs.py` | documented | Terminology is aligned to V3 and does not alter arithmetic |

## Safe Citation Boundary

The paper may cite this repository as support for TC/U/E/O finite-prefix
validation, Axis/First-Hole bridge verification, claim-status auditing, the
older bounded executable prefix / regression harness, and the PR #5
derivation-level unbounded lagged TC certificate-frontier scheduler.  It may
also cite the finite regression contracts for R2/R3/R4/R10 and the first 20
primes.

It should not cite the repository as a computational proof of concrete O(1),
bit-complexity O(1), explicit frontier materialization O(1), bounded
lagged-closure compression, asymptotic runtime, the full theorem complex, or
the full paper.
