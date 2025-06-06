"""Benchmark MPL prime generation against a simple sieve."""

import time
import math
from mpl_stream import MPLStream

def sieve(n: int):
    """Return the first ``n`` primes using a basic sieve."""
    lim = 15 if n < 6 else int(n*(math.log(n)+math.log(math.log(n))))+10
    while True:
        b = bytearray(b"\x01")*(lim+1); b[:2]=b"\x00\x00"
        for p in range(2,int(lim**0.5)+1):
            if b[p]: b[p*p:lim+1:p]=b"\x00"*(((lim-p*p)//p)+1)
        primes=[i for i,f in enumerate(b) if f][:n]
        if len(primes)==n: return primes
        lim*=2

def bench(n: int):
    """Run one benchmark iteration for ``n`` primes."""
    t0=time.perf_counter(); g=MPLStream(n); g.generate(); t_fast=time.perf_counter()-t0
    t0=time.perf_counter(); sieve(n);       t_sieve=time.perf_counter()-t0
    print(f"\n=== n = {n:,} ===")
    print("First 20:", g.primes[:20])
    print("Last  20:", g.primes[-20:])
    print(f"mpl_stream {t_fast:.6f}s   sieve {t_sieve:.6f}s   speed-up {t_sieve/t_fast:5.1f}×")

if __name__ == "__main__":
    for N in (10_000, 100_000, 1_000_000, 1_000_000_0):
        bench(N)
