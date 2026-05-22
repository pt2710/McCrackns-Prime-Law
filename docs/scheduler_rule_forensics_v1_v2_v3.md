# Scheduler Rule Forensics Across V1, V2, and V3

This document audits whether the attached paper versions contain enough
executable information to implement the actual unbounded MPL regime-motif
scheduler without forbidden runtime mechanisms.

Sources inspected:

- V1: `McCrackns_prime_law_v1.pdf`, DOI `10.5281/zenodo.15696112`.
- V2: `McCrackns_prime_law_v2.pdf`, DOI `10.5281/zenodo.19131458`.
- V3: `McCrackns_prime_law_v3.pdf`, DOI `10.5281/zenodo.20343409`.

## Executive Conclusion

Implementable now: **no**.

Combined V1/V2/V3 is not sufficient to implement the actual unbounded MPL
regime-motif scheduler under the repository guardrails.  V1 contains the most
direct pseudocode, but its executable definitions use gcd/coprimality and
minimal-legal-gap readout.  V2 and V3 improve layer separation and repeatedly
state that gcd, sieves, candidate scanning, and Axis first-hole logic are not
runtime mechanisms, but the concrete rules still defer to undefined motif
compatibility, `G_j` / `G_n(beta)` legal-gap sets, `M_j` non-membership,
scheduled stream emissions that are not specified as data structures, or
proof-normal gcd ledgers.

Final classification: **not READY**.  The missing rules must be formalized in
the paper before a non-substitute implementation can proceed.

## Cross-Version Table

| Rule | V1 evidence | V2 evidence | V3 evidence | Executable? | Blocker |
|---|---|---|---|---|---|
| `A_k` construction | p.3 Definition 2.2 defines `A_k` by legal gaps modulo `P_k` and `gcd(p_n + a_alpha, P_k) = 1`; p.8 Definition 5.2 defines `A_k := {alpha in D : gcd(p_n + a_{n,alpha}, P_k) = 1}`. | p.20 Definition 2.2 defines `A_k` as legal residues and says an increment is legal iff `gcd(p_j+a,P_k)=1`; p.23 Definition 3.2 uses nonempty legal residue classes under the motif predicate. | p.20 Definition 2.2 describes a proof-normal gcd ledger and says runtime consumes a realized motif schedule; p.23 Definition 3.2 says `A_k` is labels whose legal residue classes are nonempty under Definition 26.22. | No | V1 is forbidden/gcd-based. V2/V3 are proof-layer or assume a realized schedule; no check-free construction of `A_k` is given. |
| Motif compatibility | p.9 Definition 5.4 uses `(alpha, g) motif-compatible` but does not define the predicate. | p.27 Definition 3.9 and p.28 Theorem 3.14 use `(beta,g) motif-compatible`; p.152 Section 16.1 defines legal gaps with compatibility but does not define how to compute it. | p.27 Definition 3.9, p.28 Theorem 3.14, and p.146 Section 16.1 use `(beta,g) compatible`; p.146 says it is a Boolean predicate, but the predicate itself is not made executable. | No | Compatibility is assumed/parameterized. No formula for `m_beta`, the motif gate, or compatibility from scheduler state is supplied without residue/gcd/Axis filtering. |
| Legal gap readout | p.9 Definition 5.4 defines `G_n(alpha)` by gcd and compatibility; p.24 Algorithm 2 computes `min G_n(alpha)`. | p.27 Definition 3.9 uses `p_n+g notin M_j`; p.152 Section 16.1 uses `gcd(p_n+g,P_k)=1`; p.375 Definition 26.23 assumes the mechanically defined `G_j`. | p.27 Definition 3.9 uses `p_n+g notin M_j`; p.146 Section 16.1 uses `gcd(p_n+g,P_k)=1`; p.367 Definition 26.23 assumes `G_j`. | No | Readout is gcd/coprimality, Axis/smooth-monoid first-hole, or least-witness over a legal set. The scheduled merge/compare/multiply structure is not specified concretely enough to implement as runtime. |
| Lex-min selection | p.9 Definition 5.5 defines the motif order, but selection depends on `G_n(alpha)` from Definition 5.4. | p.20 Definition 2.3 and p.28 Theorem 3.14 define order/selection after legal sets exist; p.375-376 Definition 26.23 / Lemma 26.25 prove Lex=>Min assuming `G_j`. | p.27 Definition 3.13 defines motif order; p.28 Theorem 3.14 and p.367-368 Definition 26.23 / Lemma 26.25 prove order properties assuming `G_j`. | Partial | The order is executable, but not sufficient. It selects among motifs or legal gaps only after legality/readout has already been supplied. |
| Regime rebuild / innovation | p.3 Definition 2.3 and p.24 Algorithms 1/2 bump and rebuild, but Algorithm 1 calls `minimal legal gap`; V1 p.24 also requires a motif universe `A` without check-free construction. | p.23 Definition 3.2 says consume one pass then rebuild `A_{k+1}`; p.57 Algorithms 1/2 call minimal legal gap and rebuild under new `P_k`. | p.23 Definition 3.2 says consume one pass then rebuild `A_{k+1}`; p.37 Definition 6.5 says bump after all motifs used; p.53 Algorithms 1/2 call minimal legal gap and rebuild under new `P_k`. | No | Rebuild is specified procedurally but depends on undefined/forbidden construction of the next alphabet and minimal legal gap. |
| Successor emission | p.3 Definition 2.3 and p.9 Definition 5.3 emit `p_{n+1}=p_n+a_{n,alpha(n)}`. | p.27 Definition 3.9 and p.28 Theorem 3.14 emit after `a_mech` is obtained. | p.27 Definition 3.9 and p.28 Theorem 3.14 emit after `a_mech` is obtained. | Partial | Addition is executable, but the emitted gap is not produced by a READY check-free rule. |
| Runtime separation from forbidden mechanisms | p.1 and p.11 claim no divisibility/trial division/sieve/search; however p.3/p.8/p.9 use gcd/coprimality for the executable rule. | V2 strongly separates runtime from proof ledgers, but concrete readouts still use `M_j`, stream emissions, or gcd in proof-normal forms. | V3 states the repository is bounded and separates runtime from proof ledgers, but concrete readouts still use `M_j`, stream emissions, or gcd in proof-normal forms. | No | Separation is asserted, but no complete substitute executable rule is provided. |

## Target Decisions

### Target 1 - `A_k` Construction

Decision: **FORBIDDEN in V1, PARTIAL/MISSING in V2/V3**.

V1 fixes none of the previous blocker.  It gives a direct construction, but it
is gcd-based:

- V1 p.3, Definition 2.2: motifs satisfy `gcd(p_n + a_alpha, P_k) = 1`.
- V1 p.8, Definition 5.2: `A_k := {alpha in D : gcd(p_n + a_{n,alpha}, P_k) = 1}`.

V2 and V3 do not replace this with an executable check-free construction:

- V2 p.20, Definition 2.2: legal increments are tied to `gcd(p_j+a,P_k)=1`.
- V2 p.23, Definition 3.2: `A_k` contains labels whose legal residue classes
  are nonempty under a motif predicate.
- V3 p.20, Definition 2.2: the gcd ledger is called certification and the
  runtime consumes a realized motif schedule.
- V3 p.23, Definition 3.2: `A_k` is labels whose legal residue classes are
  nonempty under Definition 26.22.

No version gives a check-free algorithm that constructs `A_k` from the prior
MPL scheduler state.

### Target 2 - Motif Compatibility

Decision: **MISSING / PARTIAL**.

All versions use compatibility as a predicate but do not provide an executable
runtime definition:

- V1 p.9, Definition 5.4: `G_n(alpha)` includes `(alpha,g) motif-compatible`.
- V2 p.27, Definition 3.9: `G_n^mech(beta)` includes `(beta,g) motif-compatible`.
- V2 p.152, Section 16.1: legal gaps intersect coprimality with
  `(beta,g) motif-compatible`.
- V3 p.27, Definition 3.9 and p.146, Section 16.1: same structure.

The papers state or assume periodic compatibility, but do not define a runtime
function that computes compatibility, its period `m_beta`, or its mask from
regime state without falling back to residue/gcd/Axis membership machinery.

### Target 3 - Legal Gap Generation / Readout

Decision: **FORBIDDEN or PROOF-LAYER ONLY**.

V1 is explicitly gcd-based:

- V1 p.9, Definition 5.4: `G_n(alpha) = {g in 2N : gcd(p_n+g,P_k)=1, ...}`,
  and `a_{n,alpha(n)} := min G_n(alpha(n))`.
- V1 p.24, Algorithm 2: `Compute a_{n,alpha(n)} <- min G_n(alpha)`.

V2/V3 replace the direct runtime story with layer separation, but still do not
provide a concrete check-free data structure:

- V2 p.27, Definition 3.9: operational readout uses `p_n+g notin M_j`; this is
  Axis/first-hole membership unless the stream implementation is specified.
- V2 p.152, Section 16.1: `G_n(beta)` uses `gcd(p_n+g,P_k)=1`.
- V3 p.27, Definition 3.9: operational readout uses `p_n+g notin M_j`.
- V3 p.146, Section 16.1: `G_n(beta)` uses `gcd(p_n+g,P_k)=1`.

Scheduled stream operations (`merge/compare/multiply`) are named in V2/V3, but
not specified with enough state, queues, invariants, and update rules to code a
runtime without turning it into Axis first-hole enumeration or event/frontier
composite rejection.

### Target 4 - Lex-Min Selection

Decision: **PARTIAL**.

The motif order itself is executable:

- V1 p.9, Definition 5.5 gives the lexicographic motif order.
- V2 p.28, Theorem 3.14 gives `alpha(n) := min R_k(n)`.
- V3 p.27, Definition 3.13 gives `U1 < E1.0 < E1.1 < E2.0 < ...`;
  p.28, Theorem 3.14 gives `alpha(n) := min R_k(n)`.

But lex-min does not solve legality/readout:

- V2 p.375-376 and V3 p.367-368 prove Lex=>Min only after `G_j` is already
  mechanically defined and satisfies admissibility invariants.
- The ordered alphabet does not produce `a_{n,beta}` without the missing or
  forbidden legal-gap rule.

### Target 5 - Regime Rebuild / Regime Innovation

Decision: **PARTIAL / MISSING**.

All versions describe when to bump regimes, but not how to rebuild the next
runtime alphabet check-free:

- V1 p.3, Definition 2.3: bump to `k+1` and rebuild `A_{k+1}` after all motifs
  are used.
- V1 p.24, Algorithm 1: `M_k <- min(A \\ A_{k-1})`, `A_k <- A_{k-1} union {M_k}`;
  Algorithm 2 rebuilds under new `P_k`.
- V2 p.23 and V3 p.23, Definition 3.2: consume one pass, bump, and rebuild
  `A_{k+1}`.
- V3 p.37, Definition 6.5: bump after all motifs in `A_k` are used.

The rebuild operation depends on a motif universe and minimal legal gaps whose
construction remains undefined or forbidden.

## Implementation-Readiness Classification

| Component | Classification | Reason |
|---|---|---|
| `A_k` construction | MISSING / FORBIDDEN | V1 uses gcd; V2/V3 assume realized schedules or legal residue classes. |
| Motif compatibility | MISSING | `(beta,g) compatible` is a predicate parameter, not an executable definition. |
| Legal gap readout | PROOF-LAYER ONLY / FORBIDDEN | Uses gcd, `M_j` non-membership, or least-witness/minimum over legal gaps. |
| Lex-min selection | PARTIAL | Order is executable, but only after legality/readout exists. |
| Regime rebuild | PARTIAL | Bump timing is specified; check-free rebuild is not. |
| Successor emission | PARTIAL | Addition is executable; gap production is not. |
| Runtime separation proof | PARTIAL | Separation is asserted, but the replacement executable rules are absent. |

## Implementation Decision

The actual unbounded scheduler is **not implemented** from this audit.

Reason: not all five runtime rules are READY.  Implementing now would require
one of the forbidden substitutions: finite tape, gcd/coprimality ledger, wheel
residue logic, candidate scanning, Axis first-hole enumeration, or an invented
compatibility/readout rule.

## Required Paper Additions Before Implementation

### Executable Motif Compatibility Definition

Intended location: V3 Section 3.8 or Section 16.1 before legal-gap readout.

Required content:

- Define the motif object `beta` and its period `m_beta`.
- Give a finite, state-based function `compatible(beta, g, state) -> bool`.
- Prove that evaluating compatibility does not call gcd, primality tests,
  candidate scanning, `M_j` membership, wheel residues, or first-hole logic.

Why needed: every legal-gap definition uses `(beta,g) compatible`, but no
version defines this predicate executably.

### Check-Free `A_k` Construction Theorem

Intended location: V3 Section 3.2 / Definition 6.4.

Required content:

- Give an algorithm that constructs `A_k` and `A_{k+1}` from scheduler state.
- Avoid gcd/coprimality ledgers, residue sieves, prime tables, known gap data,
  candidate scanning, and Axis first-hole membership.
- Prove the constructed alphabet is finite, nonempty, complete for the regime,
  and duplicate-free.

Why needed: V1 constructs `A_k` with gcd; V2/V3 assume legal residue classes or
realized schedules.

### Scheduler Readout Theorem

Intended location: V3 Section 16.1 or Definition 26.22.

Required content:

- Give a direct runtime function that maps `(state, beta)` to the next gap
  `a_{n,beta}`.
- Define the data structures for any claimed stream operations
  (`merge/compare/multiply`), including initialization, update, and bounded
  operation counts.
- Prove it is not Axis first-hole enumeration, candidate scanning, or
  event/frontier composite rejection.

Why needed: current readout is `min G_n(beta)`, `p_n+g notin M_j`, or gcd
proof-normal readout.

### Lex-Min Runtime Realization Lemma

Intended location: V3 Section 3.8 / Definition 26.25.

Required content:

- Prove lex-min can be evaluated using only the constructed active motif
  alphabet and the check-free readout.
- Show it does not require precomputing the legal gap set `G_j`.

Why needed: the existing Lex=>Min proofs assume `G_j` already exists.

### Regime Rebuild Recursion

Intended location: V3 Section 6.6 / Appendix C.

Required content:

- Define exactly when and how `A_{k+1}` is rebuilt.
- Define the motif universe used by Algorithm 1 without empirical known gaps.
- Prove rebuild preserves legality, completeness, and non-forbidden runtime
  status.

Why needed: all versions describe the bump but leave rebuild dependent on
undefined or forbidden construction of the next alphabet.

## Safe Repository Action

Until the above definitions/theorems exist, the repository should keep the
bounded runtime, TC/Axis verifier, cost scaffolding, and proof-obligation
documents.  It should not introduce `mpl_unbounded_scheduler.py` or claim a
completed unbounded implementation.
