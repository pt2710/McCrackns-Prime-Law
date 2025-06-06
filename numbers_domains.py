# -----------------------------------------------------------------------------
# numbers_domains.py
# -----------------------------------------------------------------------------
"""Domain classifier for McCrackn’s Prime Law."""

class NumbersDomains:
    __slots__ = ()

    @staticmethod
    def evens(gap: int):
        return gap // 6 if gap % 6 == 0 else None

    @staticmethod
    def odds(gap: int):
        r = gap % 6
        if r in (2, 4):
            return (gap - r) // 6 + 7
        return None
