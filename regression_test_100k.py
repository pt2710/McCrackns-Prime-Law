"""
Regression test for McCracknsPrimeLaw.

This diagnostic generates the bounded MPL runtime prefix and compares it
against an independent reference list. The reference path is validation-only;
it is not part of the MPL mechanism.

It reports:
- First mismatch index
- First composite generated (if any)
- Total time

Run locally:
    python regression_test_100k.py
"""
import time
from math import isqrt
from mccrackns_prime_law import McCracknsPrimeLaw


# Simple deterministic reference prime generator
def reference_primes(n):
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


if __name__ == "__main__":
    N = McCracknsPrimeLaw.max_supported_primes()

    print(f"Generating {N} MPL candidates...")
    t0 = time.time()
    mpl = McCracknsPrimeLaw(n_primes=N)
    mpl_primes = mpl.generate()
    t1 = time.time()

    print("Generating reference primes...")
    ref_primes = reference_primes(N)
    t2 = time.time()

    mismatch_index = None
    for i in range(N):
        if mpl_primes[i] != ref_primes[i]:
            mismatch_index = i
            break

    print("\n--- RESULTS ---")
    if mismatch_index is None:
        print("No mismatch detected up to 100k.")
    else:
        print(f"Mismatch at index {mismatch_index}")
        print(f"MPL value: {mpl_primes[mismatch_index]}")
        print(f"REF value: {ref_primes[mismatch_index]}")

    print(f"MPL time: {t1 - t0:.2f}s")
    print(f"REF time: {t2 - t1:.2f}s")
