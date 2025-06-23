#!/usr/bin/env python3
"""
Deterministically compute the next prime p_{n+1} from a given p_n
according to McCrackn’s Prime Law.

Examples
--------
# explicit p_n
python next_prime.py --P 97 --n 25      # returns 101

# Mersenne form 2^e − 1 (e.g. 2^5 − 1 = 31)
python next_prime.py --exp 5 --n 11     # returns 37
"""
import argparse, time
from mccrackns_prime_law import McCracknsPrimeLaw


def build_law_with_prefix(p_n: int, n: int) -> McCracknsPrimeLaw:
    """
    Return a McCracknsPrimeLaw instance whose first n primes end with p_n.

    Assumes p_n really *is* the deterministic n-th prime.
    """
    law = McCracknsPrimeLaw(n_primes=n + 1, verbose=False)

    for _ in range(len(law.primes), n - 1):
        law.generate_one()

    if len(law.primes) >= n:
        law.primes[n - 1] = p_n
    else:
        law.primes.append(p_n)

    return law


def main() -> None:
    pa = argparse.ArgumentParser(description="Compute p_{n+1} from p_n.")
    grp = pa.add_mutually_exclusive_group(required=True)
    grp.add_argument("--P",   type=int,
                     help="Known prime p_n (decimal)")
    grp.add_argument("--exp", type=int,
                     help="If p_n = 2^e − 1 (Mersenne prime), supply e instead")
    pa.add_argument("--n", type=int, required=True,
                    help="Index n (1-based) of the given prime p_n")
    args = pa.parse_args()

    p_n = args.P if args.P is not None else (1 << args.exp) - 1
    n   = args.n

    law = build_law_with_prefix(p_n, n)

    law.generate_one()
    p_np1 = law.primes[n]   

    print(f"p_{n+1} = {p_np1}")


if __name__ == "__main__":
    print("🔍  Deterministic next-prime computation")
    t0 = time.perf_counter()
    main()
    print(f"⏱  {time.perf_counter() - t0:.2f}s")
