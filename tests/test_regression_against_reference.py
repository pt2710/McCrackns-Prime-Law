"""
Verified regression test for McCrackn's Prime Law (MPL).

Purpose
-------
1. Generate first N primes using MPL (assert-only GCD mode).
2. Generate first N primes using independent reference implementation
   (classical deterministic trial division).
3. Compare sequences element-wise.
4. Abort immediately on first mismatch.

This ensures MPL is not accidentally relying on structural filtering
or hidden primality assumptions.
"""

from math import isqrt
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


def test_regression_first_1000():
    N = 1000

    mpl = McCracknsPrimeLaw(n_primes=N)
    mpl_primes = mpl.generate()

    ref_primes = reference_primes(N)

    assert len(mpl_primes) == len(ref_primes)

    for i, (a, b) in enumerate(zip(mpl_primes, ref_primes), start=1):
        assert a == b, (
            f"Mismatch at index {i}: MPL={a}, REF={b}"
        )


def test_regression_first_5000():
    N = 5000

    mpl = McCracknsPrimeLaw(n_primes=N)
    mpl_primes = mpl.generate()

    ref_primes = reference_primes(N)

    assert mpl_primes == ref_primes
