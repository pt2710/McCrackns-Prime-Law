#!/usr/bin/env python3
"""
Precompute McCrackn’s prime‐law motif table up to the first N primes,
with accurate, count‐based progress updates and ETA.

Usage:
    python precompute_motifs.py --n 10000000 --out motifs.csv [--engine sympy|gmpy2] [--interval 5]
"""

import argparse
import csv
import time
import threading
import json

from mccrackns_prime_law import McCracknsPrimeLaw

def main():
    parser = argparse.ArgumentParser(description="Precompute McCrackn's motif table")
    parser.add_argument("--n", type=int, required=True,
                        help="Number of primes to generate (N)")
    parser.add_argument("--out", type=str, default="motifs.csv",
                        help="Output CSV file for motifs")
    parser.add_argument("--engine", choices=["sympy", "gmpy2"], default="sympy",
                        help="Primality test backend (default: sympy)")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="Seconds between progress reports")
    args = parser.parse_args()

    # Patch primality test
    if args.engine == "sympy":
        from sympy import isprime
        McCracknsPrimeLaw._is_prime = staticmethod(isprime)
    else:
        import gmpy2
        McCracknsPrimeLaw._is_prime = staticmethod(lambda n: bool(gmpy2.is_prime(n)))

    N = args.n
    out_file = args.out
    interval = args.interval

    print(f"[START] Generating {N} motifs with engine={args.engine}")

    # start generation in background
    mcc = McCracknsPrimeLaw(n_primes=N, verbose=False)
    thread = threading.Thread(target=mcc.generate, daemon=True)
    t_start = time.perf_counter()
    thread.start()

    # progress loop
    last_report = 0.0
    while thread.is_alive():
        time.sleep(interval)
        elapsed = time.perf_counter() - t_start
        done = len(mcc.primes)
        rate = done / elapsed if elapsed > 0 else 0
        remaining = max(N - done, 0)
        eta = remaining / rate if rate > 0 else float('inf')
        pct = done / N * 100
        print(f"[PROGRESS] {done}/{N} primes ({pct:.1f}%) — "
              f"Elapsed: {elapsed:.1f}s, ETA: {eta:.1f}s")

    # ensure finished
    thread.join()
    total_time = time.perf_counter() - t_start
    print(f"[DONE] Generated {N} motifs in {total_time:.1f}s")

    # write CSV
    print(f"[WRITE] Saving to {out_file} …")
    t0 = time.perf_counter()
    motifs = mcc.get_motifs()
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "motif"])
        for i, (label, run) in enumerate(motifs, 1):
            w.writerow([i, label])
    dt = time.perf_counter() - t0
    print(f"[WRITE] Done in {dt:.1f}s — File: {out_file}")

    # collect all domains seen (deduplicated in lex‐order of first appearance)
    motif_domains = [lbl.split(".")[0] for lbl, _ in mcc.get_motifs()]

    # build motif_alphabet: each domain, in order of first seen
    seen = set()
    motif_alphabet = []
    for d in motif_domains:
        if d not in seen:
            seen.add(d)
            motif_alphabet.append(d)

    # next run_counts: one past the last run for each domain
    run_counts = {d: motif_domains.count(d) + 1 for d in motif_alphabet}

    state = {
        "offset_applied":    mcc.offset_applied,
        "regime_points":     mcc.regime_points,
        "domain_run_counts": dict(mcc.domain_run_counts),
        "label_run_counts":  dict(mcc.label_run_counts),
        "motif_domains":     motif_domains,
        "motif_alphabet":    motif_alphabet,
        "run_counts":        run_counts
    }

    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    print("✅ Saved full Law state (including motif_alphabet) to state.json")


if __name__ == "__main__":
    main()

