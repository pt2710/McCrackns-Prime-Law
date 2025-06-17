#!/usr/bin/env python3
"""
Resumeable precompute of McCrackn’s motif table, with progress reporting
every 0.3% of the remaining primes.

Usage:
    python precompute_motifs.py --n 100000000 --csv motifs_62m.csv --state state.json
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
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            existing_history = [(label, None) for (_, label) in reader]
        M = len(existing_history)
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        print(f"[RESUME]  Found {M} motifs in {csv_path}, loaded state from {state_path}", flush=True)
        return M, state, existing_history
    else:
        print(f"[START]   No existing CSV/state; will begin fresh and write to {csv_path}", flush=True)
        return 0, None, []

def save_state(law: McCracknsPrimeLaw, state_path: str):
    st = {
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
    p.add_argument("--csv",   type=str, default="motifs_62m.csv",
                   help="Path to motifs CSV (will append/resume here)")
    p.add_argument("--state", type=str, default="state.json",
                   help="Path to JSON resume‐state file")
    args = p.parse_args()

    N          = args.n
    csv_path   = args.csv
    state_path = args.state

    # 1) patch in fast primality
    McCracknsPrimeLaw._is_prime = staticmethod(fast_is_prime)

    # 2) load progress
    M, saved_state, existing_history = load_progress(csv_path, state_path)

    # 3) instantiate the law
    law = McCracknsPrimeLaw(n_primes=N, verbose=False)

    # 4) restore counts & history
    if saved_state:
        law.regime_points     = saved_state["regime_points"]
        law.regime_set        = set(law.regime_points)
        law.domain_run_counts = defaultdict(int, saved_state["domain_run_counts"])
        law.label_run_counts  = defaultdict(int, saved_state["label_run_counts"])
        # overwrite its motif_history so far:
        law.motif_history     = existing_history[:]
        # advance its internal pointer
        law._next_index       = len(law.primes) + M  # must match how many steps done

    # 5) generate the rest
    start_idx   = law._next_index
    total_to_do = N - start_idx
    report_every = max(int(total_to_do * 0.003), 1)

    print(f"[1/2] Generating motifs {start_idx+1}..{N} (engine=gmpy2)", flush=True)
    t0 = time.perf_counter()
    for i in range(start_idx, N):
        law.generate_step()
        done = i - start_idx + 1
        if done % report_every == 0 or i == N - 1:
            elapsed = time.perf_counter() - t0
            pct     = done / total_to_do * 100
            eta     = (elapsed * (total_to_do - done) / done) if done else 0.0
            print(f"[PROGRESS] {done}/{total_to_do} ({pct:.1f}%) — "
                  f"Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s",
                  flush=True)
    dt = time.perf_counter() - t0
    print(f"[DONE]    Generated motifs up to {N} in {dt:.1f}s", flush=True)

    # 6) append *only* the newly generated tail
    full_history = law.get_motifs()
    if len(full_history) < M:
        raise RuntimeError(f"Something went backwards: got only {len(full_history)} motifs but {M} existed")

    new_tail = full_history[M:]
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for idx, (label, _) in enumerate(new_tail, start=M+1):
            writer.writerow([idx, label])
    print(f"[2/2]    Appended motifs {M+1}..{M+len(new_tail)} to {csv_path}", flush=True)

    # 7) save updated state
    save_state(law, state_path)
    print(f"✅ Completed in {dt:.1f}s — motifs now up to {len(full_history)}", flush=True)

if __name__ == "__main__":
    main()
