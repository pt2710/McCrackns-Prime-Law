class NumbersDomains:
    """
    Class for classifying integer gap values into conceptual domains.
    Provides canonical motif labeling as (Ek.x).
    """
    __slots__ = ("prime_cache", "_motif_cache")

    def __init__(self):
        # cache for primality tests and motif lookups
        self.prime_cache = {}
        self._motif_cache = {}

    def canonical_motif(self, g: int) -> str:
        """
        Return the canonical domain.subclass label for the given gap.
        - If gap == 1: returns 'U1'
        - If pure 2^k: returns 'E1.(k-1)'
        - If g = 2^k * m, m odd >= 3: returns 'E{k+1}.((m-3)//2)'
        """
        cache = self._motif_cache
        if g in cache:
            return cache[g]

        if g == 1:
            label = "U1"
        elif g & 1:
            raise ValueError(f"Gap {g} is not classifiable in canonical_motif.")
        else:
            # count trailing zeros in g
            k = (g & -g).bit_length() - 1
            m = g >> k
            if m == 1:
                # pure power of two
                label = f"E1.{k-1}"
            else:
                # mixed 2-adic
                x = (m - 3) // 2
                label = f"E{k+1}.{x}"

        cache[g] = label
        return label

    def _is_prime(self, n: int) -> bool:
        """
        Miller–Rabin–style 6k±1 trial division with caching.
        """
        cache = self.prime_cache
        if n in cache:
            return cache[n]

        if n < 2:
            result = False
        elif n < 4:
            result = True
        elif n % 6 not in (1, 5):
            result = False
        else:
            # test divisors of form 6k±1 up to sqrt(n)
            limit = int(n**0.5)
            result = True
            i = 5
            while i <= limit:
                if n % i == 0 or n % (i + 2) == 0:
                    result = False
                    break
                i += 6

        cache[n] = result
        return result
