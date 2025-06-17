# mccrackns_prime_law.py

from collections import defaultdict
from numbers_domains import NumbersDomains

class McCracknsPrimeLaw:
    __slots__ = (
        "n_primes",
        "domains",
        "primes",
        "gaps",
        "domain_run_counts",
        "label_run_counts",
        "motif_history",
        "verbose",
        "regime_points",
        "regime_set",
        "_prime_cache",
        "_next_index"
    )

    N0 = 6
    # prebuilt once for all instances
    GAP_CANDIDATES = tuple(range(2, 10_000, 2))

    def __init__(self, n_primes=100, domain_classifier=None, verbose=False):
        self.n_primes          = n_primes
        self.domains           = domain_classifier or NumbersDomains()
        # seed arrays
        self.primes            = [2, 3, 5, 7, 11, 13]
        self.gaps              = [1, 2, 2, 4, 2]
        # motif bookkeeping
        self.domain_run_counts = defaultdict(int)
        self.label_run_counts  = defaultdict(int)
        self.motif_history     = []
        self.verbose           = verbose

        # regime‐innovation points
        self.regime_points     = self._compute_regime_points(n_primes)
        self.regime_set        = set(self.regime_points)

        # internal cache
        self._prime_cache      = {}

        # initialize motif_history from the seed gaps
        self._initialize_motifs()

        # streaming index: next prime to generate is at this index
        self._next_index       = len(self.primes)

    def _compute_regime_points(self, n_primes):
        pts = []
        w = self.N0
        while w < n_primes:
            pts.append(w)
            w <<= 1
        return pts

    def _initialize_motifs(self):
        drc = self.domain_run_counts
        lrc = self.label_run_counts
        mh  = self.motif_history

        for g in self.gaps:
            label = self.domains.canonical_motif(g)
            raw   = label.split(".", 1)[0]
            drc[raw] += 1
            lrc[label] += 1
            mh.append((label, lrc[label]))

    def _is_prime(self, n: int) -> bool:
        """Default trial‐division primality (6k±1)."""
        cache = self._prime_cache
        if n in cache:
            return cache[n]

        if n < 2:
            res = False
        elif n < 4:
            res = True
        elif n % 6 not in (1, 5):
            res = False
        else:
            res = True
            limit = int(n**0.5)
            i = 5
            while i <= limit:
                if n % i == 0 or n % (i+2) == 0:
                    res = False
                    break
                i += 6

        cache[n] = res
        return res

    def generate_step(self):
        """
        Stream exactly one more prime/gap/motif.
        Must be called repeatedly until _next_index == n_primes.
        """
        idx  = self._next_index
        last = self.primes[-1]

        # find minimal legal gap
        for g in self.GAP_CANDIDATES:
            cand = last + g
            if self._is_prime(cand):
                # record prime & gap
                self.primes.append(cand)
                self.gaps.append(g)

                # motif bookkeeping
                label = self.domains.canonical_motif(g)
                raw   = label.split(".", 1)[0]
                self.domain_run_counts[raw] += 1

                self.label_run_counts[label] += 1
                run = self.label_run_counts[label]
                self.motif_history.append((label, run))

                if self.verbose:
                    print(f"[STEP {idx}] Prime: {last}, Motif: '{label}', Gap: {g}, Next prime: {cand}")

                break

        # advance stream index
        self._next_index += 1

    def generate(self):
        """Generate all remaining primes/motifs in one go."""
        while self._next_index < self.n_primes:
            self.generate_step()

    def get_primes(self):
        return self.primes

    def get_gaps(self):
        return self.gaps

    def get_motifs(self):
        return self.motif_history
