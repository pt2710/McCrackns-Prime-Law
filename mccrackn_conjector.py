from collections import defaultdict
from numbers_domains import NumbersDomains

class McCracknConjector:
    N0 = 6  # Initial regime boundary

    def __init__(self, n_primes=100, domain_classifier=None, gap_lookup=None, verbose=False):
        self.n_primes = n_primes
        self.domains = domain_classifier if domain_classifier else NumbersDomains()
        self.gap_lookup = gap_lookup  # Dict: {"E1": [2,4,8,...], ...}
        self.primes = [2, 3, 5, 7, 11, 13]
        self.gaps = [1, 2, 2, 4, 2]
        self.motif_history = []
        self.domain_run_counts = defaultdict(int)
        self.offset_applied = False
        self.motif_alphabet = []
        self.regime_points = self._compute_regime_points(self.n_primes)
        self._initialize_motifs()
        self.verbose = verbose
        if self.verbose:
            print(f"[INIT] Seeded with primes {self.primes}")
            print(f"[INIT] Initial motifs: {self.motif_alphabet}")

    def _compute_regime_points(self, n_primes):
        regime_pts = []
        win = self.N0
        while win < n_primes:
            regime_pts.append(win)
            win *= 2
        return regime_pts

    def _domain(self, gap):
        if gap == 1:
            return 'U1'
        # After prime 3, only even gaps are allowed
        if self.primes[-1] > 3 and gap % 2 != 0:
            raise ValueError(f"Odd gap {gap} after 3 is not allowed!")
        evens_code = self.domains.evens(gap)
        if evens_code is not None:
            return f'E{evens_code}'
        # O-domain logic (should only be used for initial motifs/gaps)
        odds_code = self.domains.odds(gap)
        if odds_code is not None:
            return f'O{odds_code-7}'
        raise ValueError(f"Gap {gap} is not classified.")

    def _initialize_motifs(self):
        initial_gaps = [1, 2, 2, 4, 2]
        motif_seq = []
        for g in initial_gaps:
            domain = self._domain(g)
            self.domain_run_counts[domain] += 1
            motif = (domain, self.domain_run_counts[domain])
            motif_seq.append(motif)
            if motif not in self.motif_alphabet:
                self.motif_alphabet.append(motif)
        self.motif_history = motif_seq.copy()

    def generate(self):
        n = len(self.primes)
        while len(self.primes) < self.n_primes:
            if n in self.regime_points and self.verbose:
                print(f"[REGIME] Regime innovation at n={n}")
            motif, gap = self._next_motif_gap()
            if not self.offset_applied and len(self.primes) == 6:
                gap -= 2
                self.offset_applied = True
                if self.verbose:
                    print(f"[OFFSET] Offset -2 applied at n=6 (p=13)")
            candidate = self.primes[-1] + gap
            if candidate == 15:
                if self.verbose:
                    print(f"[SKIP] Candidate 15 is not prime, skipping this motif.")
                self.domain_run_counts[motif[0]] += 1
                continue
            assert self._is_prime(candidate), f"Generated candidate {candidate} is not prime!"
            if self.verbose:
                print(f"[STEP {len(self.primes)}] Prime: {self.primes[-1]}, Motif: {motif}, Gap: {gap}, Next prime: {candidate}")
            self.primes.append(candidate)
            self.gaps.append(gap)
            self.domain_run_counts[motif[0]] += 1
            self.motif_history.append(motif)
            n += 1

    def _next_motif_gap(self):
        """
        Deterministically select the lexicographically first available (domain, run) motif,
        dynamically expanding the domain list as needed.
        """
        # Expand E- and O-domains up to any order needed
        possible_domains = set()
        max_even_k = 1
        for d in self.domain_run_counts:
            if d.startswith("E"):
                try:
                    k = int(d[1:])
                    if k > max_even_k:
                        max_even_k = k
                except Exception:
                    continue
        for k in range(1, max_even_k + 4):
            possible_domains.add(f"E{k}")
        for k in range(1, 8):
            possible_domains.add(f"O{k}")
        possible_domains.add("U1")

        for d in sorted(possible_domains, key=lambda x: (x[0], int(x[1:]))):
            run = self.domain_run_counts[d] + 1
            motif = (d, run)
            gap = self._get_minimal_gap(d, run)
            if gap is not None:
                return motif, gap
        raise RuntimeError("No legal motif could be assigned!")

    def _get_minimal_gap(self, domain, run):
        """
        Deterministically pick the 'run'th gap from the domain's sequence,
        using gap_lookup if present. Otherwise, do slow search.
        """
        if self.gap_lookup and domain in self.gap_lookup:
            seq = self.gap_lookup[domain]
            if run - 1 < len(seq):
                return seq[run - 1]
        # Fallback: slow search
        g = 1
        last_prime = self.primes[-1]
        while g < 10000:
            candidate = last_prime + g
            try:
                domain_name = self._domain(g)
            except Exception:
                g += 1
                continue
            if self._is_prime(candidate) and domain_name == domain:
                return g
            g += 1
        return None

    def _is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for d in range(3, int(n**0.5) + 1, 2):
            if n % d == 0:
                return False
        return True

    def get_primes(self):
        return self.primes

    def get_gaps(self):
        return self.gaps

    def get_motifs(self):
        return self.motif_history
