
class NumbersDomains:

    __slots__ = ("_cache",)
    _CACHE_LIMIT = 1 << 20 

    def __init__(self):
        self._cache: dict[int, str] = {}

    def canonical_motif(self, g: int, *, use_cache: bool = True) -> str:

        if g == 1:
            return "U1"
        if g & 1:
            raise ValueError("gap must be 1 or an even integer")

        if use_cache and g <= self._CACHE_LIMIT and g in self._cache:
            return self._cache[g]

        if g & (g - 1) == 0:
            x = (g.bit_length() - 1) - 1
            lbl = f"E1.{x}"
        else:
    
            k = (g & -g).bit_length() - 1
            odd = g >> k
            if odd < 3 or odd % 2 == 0:
                raise ValueError("gap does not fit 2^k·(2x+3) form")
            x = (odd - 3) // 2
            lbl = f"E{k+1}.{x}"

        if use_cache and g <= self._CACHE_LIMIT:
            self._cache[g] = lbl
        return lbl
