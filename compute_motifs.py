#!/usr/bin/env python3
"""
Resumeable precompute of McCrackn’s motif table, with progress reporting
every 0.3% of the remaining primes.

Usage:
    python compute_motifs.py --n 1000000000 --csv motifs_100b.csv --state state.json
"""

import argparse
import csv
import json
import os
import time
from collections import defaultdict

from gmpy2 import is_prime
from mccrackns_prime_law import McCracknsPrimeLaw

def fast_is_prime(n: int) -> bool:
    return is_prime(n)

def load_progress(csv_path: str, state_path: str):
    if os.path.exists(csv_path) and os.path.exists(state_path):
        # Count already‐written motifs (minus header)
        with open(csv_path, "r", encoding="utf-8") as f:
            M = sum(1 for _ in f) - 1
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        print(f"[RESUME]  Found {M} motifs in {csv_path}, loaded state from {state_path}", flush=True)
        return M, state
    else:
        print(f"[START]   No existing CSV/state; will begin fresh and write to {csv_path}", flush=True)
        return 0, None

def save_state(law: McCracknsPrimeLaw, state_path: str):
    st = {
        # we no longer store offset_applied
        "regime_points":     law.regime_points,
        "domain_run_counts": dict(law.domain_run_counts),
        "label_run_counts":  dict(law.label_run_counts),
    }
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    print(f"[STATE]   Saved resume state to {state_path}", flush=True)

def main():
    p = argparse.ArgumentParser(
        description="Resumeable precompute of McCrackn’s motif table (0.3% progress)"
    )
    p.add_argument("--n",     type=int, required=True,
                   help="Total number of primes to generate (N)")
    p.add_argument("--csv",   type=str, required=True,
                   help="Path to motifs CSV (will append/resume here)")
    p.add_argument("--state", type=str, default="state.json",
                   help="Path to JSON resume‐state file")
    args = p.parse_args()

    N          = args.n
    csv_path   = args.csv
    state_path = args.state

    # patch in fast primality
    McCracknsPrimeLaw._is_prime = staticmethod(fast_is_prime)

    # figure out how many we've already done
    M, saved_state = load_progress(csv_path, state_path)
    if M >= N:
        print(f"[DONE]    Already have {M} ≥ {N} motifs in {csv_path}", flush=True)
        return

    # instantiate law up to N
    law = McCracknsPrimeLaw(n_primes=N, verbose=False)

    # restore counts & regime points if we have a saved state
    if saved_state:
        law.regime_points     = saved_state.get("regime_points", law.regime_points)
        law.regime_set        = set(law.regime_points)
        law.domain_run_counts = defaultdict(int, saved_state.get("domain_run_counts", {}))
        law.label_run_counts  = defaultdict(int, saved_state.get("label_run_counts", {}))

    # start generating from the built‐in seed
    start_idx   = len(law.primes)         # normally 6
    total_to_do = N - start_idx
    # report every 0.3%
    report_every = max(int(total_to_do * 0.003), 1)

    print(f"[1/2] Generating motifs {start_idx+1}..{N}  (engine=gmpy2)", flush=True)
    t0 = time.perf_counter()
    for i in range(start_idx, N):
        law.generate_step()

        done = i - start_idx + 1
        if done % report_every == 0 or i == N - 1:
            elapsed = time.perf_counter() - t0
            pct     = done / total_to_do * 100
            eta     = elapsed * (total_to_do - done) / done if done else 0.0
            print(f"[PROGRESS] {done}/{total_to_do} ({pct:.1f}%) — "
                  f"Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s",
                  flush=True)
    dt = time.perf_counter() - t0
    print(f"[DONE]    Generated motifs up to {N} in {dt:.1f}s", flush=True)

    # append new motifs to CSV
    all_motifs = law.get_motifs()
    is_new     = not os.path.exists(csv_path)
    mode       = "w" if is_new else "a"
    with open(csv_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["index", "motif"])
        for idx in range(M, N):
            label, _ = all_motifs[idx]
            writer.writerow([idx+1, label])
    print(f"[2/2]    Appended motifs {M+1}..{N} to {csv_path}", flush=True)

    # save updated run‐counts & regime points
    save_state(law, state_path)

    print(f"✅ Completed in {dt:.1f}s — motifs now up to {N}", flush=True)


if __name__ == "__main__":
    main()
