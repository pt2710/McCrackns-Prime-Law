from math import isqrt
from pathlib import Path

from lagged_certificate_frontier import LaggedCertificateFrontierScheduler


ROOT = Path(__file__).resolve().parents[1]


def reference_is_prime(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def derivation_keys(trace, *, allowed: bool) -> set[tuple[int, int, int]]:
    derivations = trace.allowed_derivations if allowed else trace.forbidden_derivations
    return {
        (derivation.left_factor, derivation.right_factor, derivation.value)
        for derivation in derivations
    }


def test_api_smoke():
    scheduler = LaggedCertificateFrontierScheduler()

    assert hasattr(scheduler, "step")
    assert hasattr(scheduler, "run_recursions")
    assert hasattr(scheduler, "generate_primes")
    assert hasattr(scheduler, "generate_prime_prefix")
    assert hasattr(scheduler, "current_state")
    assert hasattr(scheduler, "trace")


def test_r2_exact_behavior():
    scheduler = LaggedCertificateFrontierScheduler()
    trace = scheduler.step()

    assert trace.recursion_index == 2
    assert trace.emitted_prime == 5
    assert trace.generated_values == (9, 15)
    assert {25, 27, 45}.issubset(set(trace.forbidden_values))
    assert trace.certified_prime_buffer == (7, 11, 13)
    assert trace.active_multipliers_before == (3,)
    assert 9 not in trace.known_targets_before
    assert 15 not in trace.known_targets_before


def test_r3_generated_values_include_derivation_level_targets():
    scheduler = LaggedCertificateFrontierScheduler()
    scheduler.step()
    trace = scheduler.step()

    assert trace.recursion_index == 3
    assert trace.emitted_prime == 7
    assert {
        21, 25, 27, 33, 35, 39, 45, 55, 65, 75,
    }.issubset(set(trace.generated_values))
    assert 49 not in trace.generated_values
    assert 21 in scheduler.current_state().composite_certificates
    assert 21 not in scheduler.current_state().pending_prime_buffer


def test_r3_forbidden_value_and_forbidden_derivations():
    scheduler = LaggedCertificateFrontierScheduler()
    scheduler.run_recursions(2)
    trace = scheduler.trace()[1]

    forbidden = derivation_keys(trace, allowed=False)
    required_forbidden = {
        (3, 21, 63),
        (3, 25, 75),
        (3, 27, 81),
        (3, 33, 99),
        (3, 35, 105),
        (5, 21, 105),
        (3, 39, 117),
        (3, 45, 135),
        (5, 27, 135),
    }

    assert 49 in trace.forbidden_values
    assert 49 not in trace.generated_values
    assert required_forbidden.issubset(forbidden)
    assert (5, 15, 75) in derivation_keys(trace, allowed=True)
    assert 75 in trace.generated_values
    assert 75 not in trace.forbidden_values


def test_r3_prime_certification_horizon():
    scheduler = LaggedCertificateFrontierScheduler()
    scheduler.run_recursions(2)
    trace = scheduler.trace()[1]

    assert trace.delayed_obstruction_horizon == 49
    assert trace.certified_prime_buffer == (17, 19, 23, 29, 31, 37, 41, 43)
    assert 47 not in trace.certified_prime_buffer
    assert 53 not in trace.certified_prime_buffer
    assert {47, 53}.issubset(set(trace.not_certified_due_to_obstruction))


def test_canonical_duplicate_collapse_and_forbidden_aliases():
    scheduler = LaggedCertificateFrontierScheduler()
    scheduler.run_recursions(2)
    certificates = scheduler.current_state().composite_certificates

    certificate_45 = certificates[45]
    assert certificate_45.value == 45
    assert certificate_45.canonical_word == (3, 3, 5)
    assert set(certificate_45.aliases) == {(3, 15), (5, 9)}

    certificate_75 = certificates[75]
    assert certificate_75.value == 75
    assert certificate_75.canonical_word == (3, 5, 5)
    assert set(certificate_75.aliases) == {(5, 15)}
    assert (3, 25, 75) in {
        (d.left_factor, d.right_factor, d.value)
        for d in certificate_75.forbidden_derivations
    }


def test_r4_continuation_delayed_self_product_resolves():
    scheduler = LaggedCertificateFrontierScheduler()
    r2, r3, r4 = scheduler.run_recursions(3)

    assert 25 not in r2.generated_values
    assert 25 in r3.generated_values
    assert 49 not in r3.generated_values
    assert 49 in r4.generated_values
    assert 7 in r4.active_multipliers_before
    assert r4.emitted_prime == 11
    assert r4.delayed_obstruction_horizon == 121
    assert (11, 11, 121) in derivation_keys(r4, allowed=False)


def test_r10_continuation_and_prefix_primality_reference_only():
    scheduler = LaggedCertificateFrontierScheduler()
    scheduler.run_recursions(9)

    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    assert scheduler.current_state().emitted_primes == tuple(expected)
    assert all(reference_is_prime(value) for value in expected)

    for trace in scheduler.trace():
        assert trace.emitted_prime not in trace.active_multipliers_before
        for derivation in trace.allowed_derivations:
            assert derivation.left_factor in trace.active_multipliers_before
            assert derivation.right_factor in trace.known_targets_before


def test_prime_prefix_first_20():
    scheduler = LaggedCertificateFrontierScheduler()

    assert scheduler.generate_prime_prefix(20) == [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    ]


def test_production_source_avoids_forbidden_runtime_mechanisms():
    source = (ROOT / "lagged_certificate_frontier.py").read_text(encoding="utf-8")
    lowered = source.lower()

    forbidden = [
        "math.gcd",
        "gcd(",
        "is_prime",
        "isprime",
        "sympy",
        "trial_division",
        "trial division",
        "sieve",
        "wheel",
        "candidate % prime",
        "candidate % p",
        "finite_mpl_gap_tape",
        "finite gap tape",
        "hardcoded prime list",
        "hardcoded gap table",
    ]

    for marker in forbidden:
        assert marker not in lowered


def test_docs_do_not_overclaim_concrete_scheduler():
    docs = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8").lower(),
            (ROOT / "docs" / "claim_status_matrix.md").read_text(encoding="utf-8").lower(),
            (ROOT / "docs" / "theorem_implementation_map.md").read_text(encoding="utf-8").lower(),
            (ROOT / "docs" / "unbounded_scheduler_proof_obligations.md").read_text(encoding="utf-8").lower(),
        ]
    )

    required_safe = [
        "data-structure-dependent",
        "bounded lagged-closure compression theorem remains open",
        "finite-prefix regression",
    ]
    forbidden = [
        "concrete scheduler is o(1)",
        "repository proves o(1)",
        "repository proves bounded lagged-closure compression",
        "finite tests prove asymptotic complexity",
        "repository proves whole paper",
    ]

    for phrase in required_safe:
        assert phrase in docs
    for phrase in forbidden:
        assert phrase not in docs
