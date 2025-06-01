"""
numbers_domains.py

Provides domain classification for gap values in prime-gap prediction.
Domains are divided into:
- Unity domain (gap == 1)
- Even domains based on 2-adic structure, matching Budd's explicit logic:
    - E1: All pure powers of 2 (2, 4, 8, 16, ...)
    - E2: 2 × odd ≥ 6  (e.g. 6, 10, 14, ...)
    - E3: 4 × odd ≥ 12 (e.g. 12, 20, 28, ...)
    - E4: 8 × odd ≥ 24 (e.g. 24, 40, 56, ...)
    - ... (generalized to any Ek: 2^k × odd, odd ≥ 3)
- Odd domains based on primality, perfect powers, and composite structure.
"""

class NumbersDomains:
    """
    Class for classifying integer gap values into conceptual domains.

    Methods
    -------
    unity(g)
        Classify gap == 1 as unity domain.
    evens(g)
        Classify even gaps into generalized 2-adic domains Ek.
    odds(g)
        Classify odd gaps into prime, power, or composite domains.
    """

    def __init__(self):
        """
        Initialize the NumbersDomains instance.

        Attributes
        ----------
        prime_cache : dict
            Cache for primality checks to avoid repeated computation.
        """
        self.prime_cache = {}

    def unity(self, g: int) -> int | None:
        """
        Classify the unity domain (gap == 1).

        Parameters
        ----------
        g : int
            Gap value to classify.

        Returns
        -------
        int or None
            Returns 1 for the unity domain, or None if g != 1.
        """
        return 1 if g == 1 else None

    def evens(self, g: int) -> int | None:
        """
        Classify even gap values into generalized 2-adic domains.

        For any even gap g ≥ 2:
          - Express as g = 2^k × odd, with odd ≥ 1, k ≥ 1.
          - If odd == 1 (i.e., g is a pure power of two), return domain 1 (E1).
          - Else, return domain (k), i.e., E2, E3, ... for k ≥ 2.

        Parameters
        ----------
        g : int
            Gap value to classify.

        Returns
        -------
        int or None
            Domain code (E1=1, E2=2, ...) for even gaps, or None otherwise.
        """
        if g < 2 or g % 2 != 0:
            return None

        n = g
        k = 0
        while n % 2 == 0:
            n //= 2
            k += 1
        if n == 1:
            return 1  # E1: pure power of two
        elif n % 2 == 1 and n >= 3:
            return k  # E2, E3, ..., Ek as needed
        else:
            return None  # Should never happen for valid evens

    def odds(self, g: int) -> int | None:
        """
        Classify odd gap values into five domains:

        Domains mapping:
          8: prime odds
          9: odd perfect powers b^k (k>=2)
          10: product of two distinct primes
          11: product q*p where q in {7,11,13,17,19}, p prime
          12: all other composite odds

        Parameters
        ----------
        g : int
            Gap value to classify.

        Returns
        -------
        int or None
            Domain code (8–12) for odd gaps, or None otherwise.
        """
        if g % 2 != 1:
            return None
        if self._is_prime(g):
            return 8
        if self._is_odd_power(g):
            return 9
        if self._is_product_of_two_primes(g):
            return 10
        for q in (7, 11, 13, 17, 19):
            if g % q == 0 and self._is_prime(g // q):
                return 11
        return 12

    def _is_prime(self, n: int) -> bool:
        """
        Check if n is prime using cached trial division.
        """
        if n in self.prime_cache:
            return self.prime_cache[n]
        if n <= 1:
            result = False
        elif n <= 3:
            result = True
        elif n % 2 == 0 or n % 3 == 0:
            result = False
        else:
            result = True
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    result = False
                    break
                i += 6
        self.prime_cache[n] = result
        return result

    def _is_odd_power(self, n: int) -> bool:
        """
        Detect if n is an odd perfect power b^k for k >= 2.
        """
        b = 2
        while b * b <= n:
            k = 2
            while b ** k <= n:
                if b ** k == n:
                    return True
                k += 1
            b += 1
        return False

    def _is_product_of_two_primes(self, n: int) -> bool:
        """
        Check if n is the product of two distinct prime numbers.
        """
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                j = n // i
                if i != j and self._is_prime(i) and self._is_prime(j):
                    return True
        return False
