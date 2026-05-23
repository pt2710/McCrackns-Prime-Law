# V3 Theorem And Implementation Map

This theorem map records repository support for selected V3 claims.

This map links major V3 paper claims to repository support.  It is not a proof
assistant transcript and does not claim full formalization of the theorem
complex.

| V3 theorem / lemma / claim | Mathematical claim | Implementation object | Test object | Status | Notes |
|---|---|---|---|---|---|
| Lemma 6.15, U1 seed-only parity constraint | Gap `1` occurs only at `2 -> 3`; later gaps are even | `McCracknsPrimeLaw._record` | `tests/test_mpl_tc_architecture.py` | implemented | Runtime assertion plus bounded-prefix test |
| TC Unity domain | `1` is Unity seed / monoid identity, structurally separated from Odd | `TriadicDomains.place` | `tests/test_triadic_domains.py` | finite-prefix validated | `place(1)` returns `U` / `U1` |
| Even-domain dyadic placement | Even numbers decompose by dyadic depth and odd face | `TriadicDomains.even_face`, `TriadicDomains.place` | `tests/test_triadic_domains.py` | finite-prefix validated | Covers pure dyadic powers and mixed even composites structurally |
| Theorem 5.3, Odd-domain completeness by least prime factor | Odd values are O1 primes or unique lpf composite strata | `TriadicDomains.place`, `odd_composite_stream` | `tests/test_triadic_domains.py` | finite-prefix validated | O2/O3/O4 examples are tested |
| Corollary 5.4, O-axis notation and lpf strata | O1 is prime/free; O2/O3/O4 are lpf strata | `TriadicDomains` | `tests/test_triadic_domains.py` | finite-prefix validated | Avoids duplicate raw-axis placement such as `15` in two rows |
| Theorem 6.6, Axis Law iff MPL outcomes | MPL successor equals `min(N >= 1 \\ M_j)` in proof layer | `verify_axis_bridge.py` | `tests/test_axis_bridge_consistency.py` | finite-prefix validated | Full equivalence remains paper-level |
| Lemma 6.12, Sentinel non-generativity | GCD/assertions, if present, are falsification-only | Policy in docs; no GCD in runtime | `tests/test_mpl_tc_architecture.py` | implemented as absence/policy | No active GCD selector is present |
| Bounded MPL regime/motif prefix | Repository emits a finite prefix with motif labels and regime accounting | `mccrackns_prime_law.py` | `tests/test_regression_against_reference.py` | finite-prefix validated | Uses `FINITE_MPL_GAP_TAPE`; not the full theory |
| Section 6.5, Derivation-level lagged TC certificate-frontier scheduler | Deterministic derivation scheduler with generated values, allowed/forbidden derivations, activation cohorts, active multipliers, known targets, prime buffers, and delayed obstruction horizons | `lagged_certificate_frontier.py` | `tests/test_lagged_certificate_frontier.py` | implemented with finite-prefix regression coverage | Concrete runtime is data-structure-dependent |
| Full unbounded MPL scheduler | Deterministic check-free scheduler for all primes | `lagged_certificate_frontier.py` for the derivation-level certificate-frontier form; compressed regime/motif form not implemented | `tests/test_lagged_certificate_frontier.py`, `docs/unbounded_scheduler_proof_obligations.md` | partial / proof obligation | Must not be claimed as compressed or O(1) |
| Theorem 6.22 / 6.27 / 6.33, frontier completeness and conditional O(1) compression | Derivation-level construction is check-free; constant-step compression is conditional | `lagged_certificate_frontier.py`, `cost_model.py` framework | `tests/test_lagged_certificate_frontier.py`, `tests/test_cost_model_instrumentation.py` | implemented / proof obligation | The implementation validates finite-prefix regression contracts but does not prove the bounded lagged-closure compression theorem |
| TC iff MPL bridge | Structural TC coverage and MPL successor agree globally | Finite verifier only | `tests/test_axis_bridge_consistency.py` | paper-only with finite validation | TC alone is not used as a prime generator |
| U/E/O terminology | Unity seed, even unity-sets, first-order odd unity-sets, lpf odd composites, mixed even composites | `docs/claim_status_matrix.md`, `triadic_domains.py` | `tests/test_claim_status_docs.py` | documented | Terminology is aligned to V3 and does not alter arithmetic |

## Safe Citation Boundary

The paper may cite this repository as support for a bounded executable prefix /
regression harness, finite TC/Axis validation, bridge-verifier scaffolding,
claim-status auditing, and an executable derivation-level lagged TC
certificate-frontier scheduler.  It should not cite the repository as a
computational proof of the O(1) theorem or the bounded lagged-closure
compression theorem.
The O(1) unit-cost successor claim remains a proof obligation outside the
concrete frontier implementation.
