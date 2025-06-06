# -----------------------------------------------------------------------------
# numbers_domains.py
# -----------------------------------------------------------------------------
"""Domain classifier for McCrackn’s Prime Law."""

class NumbersDomains:
    """Utility methods for classifying gaps into domains."""
    __slots__ = ()

    @staticmethod
    def evens(gap: int):
        """Return k such that ``gap`` = 6*k if evenly divisible."""
        return gap // 6 if gap % 6 == 0 else None

    @staticmethod
    def odds(gap: int):
        """Return domain index for odd gaps or ``None`` if invalid."""
        r = gap % 6
        if r in (2, 4):
            return (gap - r) // 6 + 7
        return None
