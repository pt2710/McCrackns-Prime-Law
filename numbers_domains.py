class NumbersDomains:
    """
    Class to handle motif domain calculations for prime gaps.

    This class provides functionality for calculating the canonical motif
    for a given gap size `g` according to McCrackn's motif-based prime law.
    The motifs are cached for efficiency up to a certain limit (`_CACHE_LIMIT`).
    """

    __slots__ = ("_cache",)  # Reduce memory usage by limiting instance attributes
    _CACHE_LIMIT = 1 << 20   # Limit cache to gaps less than 2^20

    def __init__(self):
        """
        Initializes the NumbersDomains class with an empty cache.
        """
        self._cache: dict[int, str] = {}  # Store motif labels for gaps in the cache

    def canonical_motif(self, g: int, *, use_cache: bool = True) -> str:
        """
        Computes the canonical motif label for a given gap size `g`.

        The motif is based on the formula `2^k * (2x + 3)` for even gaps.
        Special cases such as `g == 1` (U1) and power-of-two gaps are handled separately.
        Results are cached for efficiency if `use_cache` is True.

        Args:
            g (int): The gap size to compute the motif for.
            use_cache (bool): Whether to use cached results for gaps below the cache limit.

        Returns:
            str: The canonical motif label (e.g., "U1", "E1.0", "E2.1").

        Raises:
            ValueError: If the gap is not valid (odd or doesn't fit the expected form).
        """

        # Handle special case for gap 1
        if g == 1:
            return "U1"

        # Validate that the gap is even
        if g & 1:
            raise ValueError("gap must be 1 or an even integer")

        # Check cache if enabled and gap is within cache limit
        if use_cache and g <= self._CACHE_LIMIT and g in self._cache:
            return self._cache[g]

        # Handle powers of two (E1.x)
        if g & (g - 1) == 0:
            x = (g.bit_length() - 1) - 1  # Calculate x for E1.x (2^k form)
            lbl = f"E1.{x}"
        else:
            # General case: form 2^k * (2x + 3)
            k = (g & -g).bit_length() - 1  # Extract power-of-two factor
            odd = g >> k  # Odd factor from the remaining gap after dividing by 2^k
            if odd < 3 or odd % 2 == 0:
                raise ValueError("gap does not fit 2^k·(2x+3) form")
            x = (odd - 3) // 2  # Calculate x based on the odd factor
            lbl = f"E{k+1}.{x}"  # Label for the canonical motif

        # Cache the result if within cache limit
        if use_cache and g <= self._CACHE_LIMIT:
            self._cache[g] = lbl
        return lbl
