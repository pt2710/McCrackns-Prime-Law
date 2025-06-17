#!/usr/bin/env python3
"""
Compute the next prime via McCrackn’s Prime Law, given either:

  • --P <current_prime>   (as a decimal string, for arbitrary primes), or
  • --exp <e>             (for Mersenne primes P = 2^e − 1)

Usage:
    python next_prime.py --P 17 --n 7
    python next_prime.py --exp 82589933 --n 82589933
"""

import argparse
import time
from gmpy2 import is_prime
from mccrackns_prime_law import McCracknsPrimeLaw

def next_prime_after(P: int, n: int) -> int:
    # patch in fast primality
    McCracknsPrimeLaw._is_prime = staticmethod(is_prime)

    # build up to n+1
    law = McCracknsPrimeLaw(n_primes=n+1, verbose=False)

    # ensure seed list has exactly n entries, ending in P
    if len(law.primes) >= n:
        law.primes[n-1] = P
    else:
        law.primes = law.primes[:n-1] + [P]

    # now generate just one more
    law.generate()
    return law.get_primes()[n]  # index n is p_{n+1}

def main():
    parser = argparse.ArgumentParser(
        description="Compute p_{n+1} via McCrackn’s Prime Law"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--P",   type=str,
        help="Decimal of current prime p_n (can be huge)"
    )
    group.add_argument(
        "--exp", type=int,
        help="Exponent e if p_n is the Mersenne prime 2^e−1"
    )
    parser.add_argument(
        "--n", type=int, required=True,
        help="Index n of the current prime (p_n)"
    )
    args = parser.parse_args()

    # compute P
    if args.exp is not None:
        # for Mersennes: P = 2^e - 1
        P = pow(2, args.exp, None) - 1
    else:
        P = int(args.P)

    p_next = next_prime_after(P, args.n)
    print(f"Next prime p_{args.n+1} = {p_next}")

if __name__ == "__main__":
    # preserve exactly these start/end prints so you get timing feedback
    print("🔍 Starting next-prime computation…", flush=True)
    t0 = time.perf_counter()
    main()
    t1 = time.perf_counter()
    print(f"⏱ Total elapsed: {t1 - t0:.2f}s", flush=True)
