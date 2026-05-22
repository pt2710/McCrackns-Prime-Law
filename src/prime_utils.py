"""Reference-only utilities for tests and diagnostics."""

def is_prime(n: int) -> bool:
    """Return ``True`` for primes by direct divisor checks.

    This helper is not used by the MPL successor.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(n ** 0.5) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False
    return True
