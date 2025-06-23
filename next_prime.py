"""
Deterministically compute the next prime \( p_{n+1} \) from a given \( p_n \)
according to McCrackn’s Prime Law.

Examples
--------
# Provide explicit p_n
python next_prime.py --P 97 --n 25      # returns 101

# Mersenne form 2^e − 1 (e.g. 2^5 − 1 = 31)
python next_prime.py --exp 5 --n 11     # returns 37

This script reconstructs the motif structure up to index `n`, inserts the known
prime `p_n`, then computes the next deterministic prime according to the law's motif logic.
"""

import argparse
import time
from mccrackns_prime_law import McCracknsPrimeLaw


def build_law_with_prefix(p_n: int, n: int) -> McCracknsPrimeLaw:
    """
    Construct a McCrackn’s Prime Law instance with prefix ending in p_n at index n.

    Parameters:
        p_n (int): The known n-th prime.
        n   (int): The 1-based index of p_n in the prime sequence.

    Returns:
        McCracknsPrimeLaw: Law instance preloaded up to p_n with its motif state.
    """
    law = McCracknsPrimeLaw(n_primes=n + 1, verbose=False)

    # Step until we have generated enough primes to safely set p_n
    for _ in range(len(law.primes), n - 1):
        law.generate_one()

    # Replace or append p_n at index n−1
    if len(law.primes) >= n:
        law.primes[n - 1] = p_n
    else:
        law.primes.append(p_n)

    return law


def main() -> None:
    """
    Parse CLI args and compute p_{n+1} from p_n using motif logic.
    """
    pa = argparse.ArgumentParser(description="Compute p_{n+1} from p_n.")
    grp = pa.add_mutually_exclusive_group(required=True)
    grp.add_argument("--P",   type=int,
                     help="Known prime p_n (decimal)")
    grp.add_argument("--exp", type=int,
                     help="If p_n = 2^e − 1 (Mersenne prime), supply e instead")
    pa.add_argument("--n", type=int, required=True,
                    help="Index n (1-based) of the given prime p_n")
    args = pa.parse_args()

    # Decode p_n from either direct input or exponent form
    p_n = args.P if args.P is not None else (1 << args.exp) - 1
    n   = args.n

    # Build law instance ending at p_n
    law = build_law_with_prefix(p_n, n)

    # Advance one prime deterministically
    law.generate_one()
    p_np1 = law.primes[n]

    print(f"p_{n+1} = {p_np1}")


if __name__ == "__main__":
    print("🔍  Deterministic next-prime computation")
    t0 = time.perf_counter()
    main()
    print(f"⏱  {time.perf_counter() - t0:.2f}s")
