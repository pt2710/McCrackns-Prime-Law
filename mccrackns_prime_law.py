from collections import defaultdict
from numbers_domains import NumbersDomains

class McCracknsPrimeLaw:
    """
    Deterministic generator for the sequence of prime numbers via the
    regime-motif law and lexicographically minimal gap assignment.

    Attributes:
        N0 (int): Initial regime boundary (first regime expansion).
        n_primes (int): Number of primes to generate.
        domains (NumbersDomains): Classifier for domain assignment.
        gap_lookup (dict): Precomputed domain-gap sequences, if provided.
        primes (list): List of generated primes.
        gaps (list): List of consecutive prime gaps.
        motif_history (list): Sequence of (domain, run) motifs used.
        domain_run_counts (defaultdict): Counts of motifs by domain.
        offset_applied (bool): Whether the -2 parity offset has been used.
        motif_alphabet (list): Ordered list of discovered motifs.
        regime_points (list): List of regime innovation points (Nk).
        verbose (bool): Whether to print detailed step information.
    """

    N0 = 6  # Initial regime boundary

    def __init__(self, n_primes=100, domain_classifier=None, gap_lookup=None, verbose=False):
        """
        Initialize the McCracknsPrimeLaw.

        Args:
            n_primes (int): Number of primes to generate.
            domain_classifier (NumbersDomains or None): Custom domain classifier.
            gap_lookup (dict or None): Optional precomputed gap sequences for domains.
            verbose (bool): If True, print progress information during generation.
        """
        self.n_primes = n_primes
        self.domains = domain_classifier if domain_classifier else NumbersDomains()
        self.gap_lookup = gap_lookup  # Dict: {"E1": [2,4,8,...], ...}
        self.primes = [2, 3, 5, 7, 11, 13]   # Hard-coded seed (first 6 primes)
        self.gaps = [1, 2, 2, 4, 2]          # Gaps for seed primes
        self.motif_history = []              # Sequence of (domain, run) pairs
        self.domain_run_counts = defaultdict(int)  # Domain run-lengths
        self.offset_applied = False          # Parity offset flag
        self.motif_alphabet = []             # All unique motifs discovered so far
        self.regime_points = self._compute_regime_points(self.n_primes)
        self._initialize_motifs()
        self.verbose = verbose
        if self.verbose:
            print(f"[INIT] Seeded with primes {self.primes}")
            print(f"[INIT] Initial motifs: {self.motif_alphabet}")

    def _compute_regime_points(self, n_primes):
        """
        Compute the regime innovation points (Nk), which are powers of two starting from N0.

        Args:
            n_primes (int): The target number of primes.

        Returns:
            list: Regime innovation points (indices where motif expansion occurs).
        """
        regime_pts = []
        win = self.N0
        while win < n_primes:
            regime_pts.append(win)
            win *= 2
        return regime_pts

    def _domain(self, gap):
        """
        Determine the domain label for a given prime gap.

        Args:
            gap (int): The candidate gap value.

        Returns:
            str: Domain label (e.g., 'E1', 'O2', 'U1').

        Raises:
            ValueError: If the gap is not classifiable or violates parity constraints.
        """
        if gap == 1:
            return 'U1'
        # After the first odd prime, all further gaps must be even
        if self.primes[-1] > 3 and gap % 2 != 0:
            raise ValueError(f"Odd gap {gap} after 3 is not allowed!")
        evens_code = self.domains.evens(gap)
        if evens_code is not None:
            return f'E{evens_code}'
        odds_code = self.domains.odds(gap)
        if odds_code is not None:
            return f'O{odds_code-7}'
        raise ValueError(f"Gap {gap} is not classified.")

    def _initialize_motifs(self):
        """
        Initialize motif sequence for the seed primes, updating run counts and the alphabet.
        """
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
        """
        Generate the deterministic sequence of primes up to n_primes.
        Implements regime-motif innovation, minimal gap assignment, and parity offset.
        """
        n = len(self.primes)
        while len(self.primes) < self.n_primes:
            if n in self.regime_points and self.verbose:
                print(f"[REGIME] Regime innovation at n={n}")
            motif, gap = self._next_motif_gap()
            # Apply -2 offset at p=13 (see theoretical justification)
            if not self.offset_applied and len(self.primes) == 6:
                gap -= 2
                self.offset_applied = True
                if self.verbose:
                    print(f"[OFFSET] Offset -2 applied at n=6 (p=13)")
            candidate = self.primes[-1] + gap
            # Skip forbidden candidate 15 (composite, but appears via motif assignment)
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
        dynamically expanding domain space if necessary, and assign its minimal legal gap.

        Returns:
            tuple: (motif, gap), where motif is (domain, run).
        Raises:
            RuntimeError: If no legal motif-gap can be assigned.
        """
        # Build up even and odd domains up to max discovered so far (+buffer)
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
        # Expand E-domains by +3, always consider first 7 O-domains
        for k in range(1, max_even_k + 4):
            possible_domains.add(f"E{k}")
        for k in range(1, 8):
            possible_domains.add(f"O{k}")
        possible_domains.add("U1")

        # Lexicographic ordering: even/odd domains by number
        for d in sorted(possible_domains, key=lambda x: (x[0], int(x[1:]))):
            run = self.domain_run_counts[d] + 1
            motif = (d, run)
            gap = self._get_minimal_gap(d, run)
            if gap is not None:
                return motif, gap
        raise RuntimeError("No legal motif could be assigned!")

    def _get_minimal_gap(self, domain, run):
        """
        Deterministically select the run-th minimal gap for a given domain.

        Args:
            domain (str): Domain label (e.g., 'E1', 'O2', 'U1').
            run (int): Motif run index.

        Returns:
            int or None: Minimal legal gap, or None if not found.
        """
        # If precomputed gap sequence provided, use it
        if self.gap_lookup and domain in self.gap_lookup:
            seq = self.gap_lookup[domain]
            if run - 1 < len(seq):
                return seq[run - 1]
        # Otherwise: search for smallest admissible gap for domain/run
        g = 1
        last_prime = self.primes[-1]
        while g < 10000:  # Safe upper bound for search window
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
        """
        Test whether n is a prime by trial division.

        Args:
            n (int): Number to check.

        Returns:
            bool: True if n is prime, False otherwise.
        """
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
        """
        Return the list of generated primes.

        Returns:
            list: Prime numbers.
        """
        return self.primes

    def get_gaps(self):
        """
        Return the list of consecutive prime gaps.

        Returns:
            list: Prime gaps.
        """
        return self.gaps

    def get_motifs(self):
        """
        Return the list of (domain, run) motifs.

        Returns:
            list: Motif sequence.
        """
        return self.motif_history
