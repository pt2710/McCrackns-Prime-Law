from collections import defaultdict
from numbers_domains import NumbersDomains

class McCracknsPrimeLaw:
    __slots__ = (
        "n_primes", "domains", "primes", "gaps",
        "domain_run_counts", "label_run_counts", "motif_history",
        "offset_applied", "verbose", "regime_points", "regime_set",
        "_prime_cache"
    )

    N0 = 6
    # Prebuilt once for all instances
    GAP_CANDIDATES = tuple(range(2, 10_000, 2))

    def __init__(self, n_primes=100, domain_classifier=None, verbose=False):
        self.n_primes          = n_primes
        self.domains           = domain_classifier or NumbersDomains()
        self.primes            = [2, 3, 5, 7, 11, 13]
        self.gaps              = [1, 2, 2, 4, 2]
        self.domain_run_counts = defaultdict(int)
        self.label_run_counts  = defaultdict(int)
        self.motif_history     = []
        self.offset_applied    = False
        self.verbose           = verbose

        # Precompute regime points and set for O(1) checks
        self.regime_points     = self._compute_regime_points(n_primes)
        self.regime_set        = set(self.regime_points)

        # Internal cache for primality tests
        self._prime_cache      = {}

        # Seed the motif history from the initial gaps
        self._initialize_motifs()

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
        """Default trial-division primality with 6k±1 optimization."""
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
                if n % i == 0 or n % (i + 2) == 0:
                    res = False
                    break
                i += 6

        cache[n] = res
        return res

    def generate(self):
        primes        = self.primes
        gaps          = self.gaps
        regime_set    = self.regime_set
        is_prime      = self._is_prime
        canonical     = self.domains.canonical_motif
        dom_counts    = self.domain_run_counts
        lab_counts    = self.label_run_counts
        history       = self.motif_history
        verbose       = self.verbose
        offset_flag   = self.offset_applied
        target        = self.n_primes

        # ensure seed
        if not primes:
            primes.append(2)

        start_idx = len(primes)
        for idx in range(start_idx, target):
            last = primes[-1]

            if verbose and idx in regime_set:
                print(f"[REGIME] innovation at n={idx}")

            for d in self.GAP_CANDIDATES:
                # single "-2" offset at the 6th prime
                g = (d - 2) if (idx == 6 and not offset_flag) else d
                if g <= 0:
                    continue

                cand = last + g

                # skip 15 but still update domain run count
                if cand == 15:
                    if verbose:
                        print("[SKIP] 15")
                    raw = canonical(g).split(".", 1)[0]
                    dom_counts[raw] += 1
                    continue

                if is_prime(cand):
                    if idx == 6 and not offset_flag:
                        offset_flag = True
                        if verbose:
                            print("[OFFSET] -2 at p=13")

                    primes.append(cand)
                    gaps.append(g)

                    label = canonical(g)
                    raw   = label.split(".", 1)[0]
                    dom_counts[raw] += 1

                    lab_counts[label] += 1
                    history.append((label, lab_counts[label]))

                    if verbose:
                        print(f"[STEP {idx}] Prime: {last}, Motif: '{label}', Gap: {g}, Next prime: {cand}")
                    break

        # commit the one‐time offset change
        self.offset_applied = offset_flag

    def get_primes(self):
        return self.primes

    def get_gaps(self):
        return self.gaps

    def get_motifs(self):
        return self.motif_history
