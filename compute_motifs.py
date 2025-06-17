#!/usr/bin/env python3
"""
Resumeable, streaming compute of McCrackn’s motif table,
writing each new motif to CSV as soon as it’s generated.

Usage:
    python compute_motifs.py --n 100000000 \
        --csv motifs_62m.csv --state state.json
"""
import argparse, csv, json, os, time
from collections import defaultdict

from gmpy2 import is_prime
from mccrackns_prime_law import McCracknsPrimeLaw

def fast_is_prime(n: int) -> bool:
    return is_prime(n)

def load_progress(csv_path, state_path):
    if os.path.exists(csv_path) and os.path.exists(state_path):
        # count already‐written motifs
        with open(csv_path, newline="", encoding="utf-8") as f:
            M = sum(1 for _ in f) - 1
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        print(f"[RESUME]  Found {M} motifs in {csv_path}, loaded state from {state_path}", flush=True)
        return M, state
    else:
        print(f"[START]   No existing CSV/state; starting fresh -> {csv_path}", flush=True)
        return 0, None

def save_state(law: McCracknsPrimeLaw, state_path):
    st = {
        "regime_points":     law.regime_points,
        "domain_run_counts": dict(law.domain_run_counts),
        "label_run_counts":  dict(law.label_run_counts),
    }
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    print(f"[STATE]   Saved resume state to {state_path}", flush=True)

def main():
    p = argparse.ArgumentParser(description="Streaming resumeable motif compute")
    p.add_argument("--n",   type=int, required=True, help="Total primes to generate (N)")
    p.add_argument("--csv", type=str, required=True, help="Path to motifs CSV")
    p.add_argument("--state", type=str, required=True, help="Path to resume-state JSON")
    args = p.parse_args()

    N          = args.n
    csv_path   = args.csv
    state_path = args.state

    # patch primality test
    McCracknsPrimeLaw._is_prime = staticmethod(fast_is_prime)

    # figure out how many already done
    M, saved_state = load_progress(csv_path, state_path)

    # instantiate law up to N
    law = McCracknsPrimeLaw(n_primes=N, verbose=False)

    # restore counts & pointer
    if saved_state:
        law.regime_points     = saved_state["regime_points"]
        law.regime_set        = set(law.regime_points)
        law.domain_run_counts = defaultdict(int, saved_state["domain_run_counts"])
        law.label_run_counts  = defaultdict(int, saved_state["label_run_counts"])
        law._next_index       = len(law.primes) + M  # pick up after M steps

    start_idx   = law._next_index
    total_to_do = N - start_idx
    report_every = max(int(total_to_do * 0.003), 1)

    # open CSV for append (or write header if new)
    is_new = not os.path.exists(csv_path)
    csvf   = open(csv_path, "a", newline="", encoding="utf-8")
    writer = csv.writer(csvf)
    if is_new:
        writer.writerow(["index","motif"])
    print(f"[1/2] Generating motifs {start_idx+1}..{N}", flush=True)

    t0 = time.perf_counter()
    for i in range(start_idx, N):
        label, run = law.generate_step()
        idx        = i + 1
        writer.writerow([idx, label])

        done = i - start_idx + 1
        if done % report_every == 0 or i == N-1:
            elapsed = time.perf_counter() - t0
            pct     = done/total_to_do*100
            eta     = elapsed*(total_to_do-done)/done if done else 0.0
            print(f"[PROGRESS] {done}/{total_to_do} ({pct:.1f}%) — "
                  f"Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s",
                  flush=True)
    csvf.close()

    dt = time.perf_counter() - t0
    print(f"[DONE]    Generated motifs up to {N} in {dt:.1f}s", flush=True)

    # save resume-state
    save_state(law, state_path)
    print(f"✅ Completed — motifs up to {N} written to {csv_path}", flush=True)

if __name__=="__main__":
    main()
