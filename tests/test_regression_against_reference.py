"""
Extended Verified Regression & Structural Validation Suite for MPL

This suite now:
1. Verifies the bounded MPL runtime against an independent reference prefix
2. Measures performance
3. Confirms structural invariants
"""

from math import isqrt
import time
from mccrackns_prime_law import McCracknsPrimeLaw


def reference_primes(n: int):
    primes = []
    candidate = 2

    while len(primes) < n:
        is_prime = True
        limit = isqrt(candidate)
        for p in primes:
            if p > limit:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1

    return primes


def test_regression_bounded_finite_prefix():
    N = McCracknsPrimeLaw.max_supported_primes()

    start_mpl = time.perf_counter()
    mpl = McCracknsPrimeLaw(n_primes=N)
    mpl_primes = mpl.generate()
    mpl_time = time.perf_counter() - start_mpl

    start_ref = time.perf_counter()
    ref_primes = reference_primes(N)
    ref_time = time.perf_counter() - start_ref

    assert mpl_primes == ref_primes, "Bounded MPL prefix regression mismatch"

    print("\n--- Performance Report ---")
    print(f"MPL time: {mpl_time:.4f} seconds")
    print(f"Reference time: {ref_time:.4f} seconds")
    print(f"Speed ratio (MPL / REF): {mpl_time/ref_time:.4f}")

    # Structural invariant check: only one odd gap (2→3)
    gaps = [b - a for a, b in zip(mpl_primes, mpl_primes[1:])]
    odd_gaps = [g for g in gaps if g % 2 != 0]

    assert odd_gaps == [1], "Unexpected odd gap detected"

    print("Structural validation passed: Only one odd gap (2→3).")
