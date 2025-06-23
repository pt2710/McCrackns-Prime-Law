#!/usr/bin/env python3
"""
Streaming, resumable compute of McCrackn’s motif table (fast residue-based).

Usage:
    python compute_motifs.py --n 5000000 --csv motifs_5m.csv --state state.json
"""
import argparse, csv, json, os, time
from mccrackns_prime_law import McCracknsPrimeLaw


# ───────────────────────── helpers ──────────────────────────
def load_progress(csv_path: str, state_path: str):
    if os.path.exists(csv_path) and os.path.exists(state_path):
        with open(csv_path, encoding="utf-8") as f:
            written = sum(1 for _ in f) - 1       # minus header row
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)
        print(f"[RESUME] CSV rows={written} — state loaded.", flush=True)
        return written, state
    print(f"[START ] fresh run — creating {csv_path}", flush=True)
    return 0, None


def save_state(law: McCracknsPrimeLaw, state_path: str):
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "last_prime":    law.primes[-1],
                "regime_points": law.regime_points,
            },
            f,
            indent=2,
        )
    print(f"[STATE ] snapshot saved → {state_path}", flush=True)


# ───────────────────────── main ─────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Resumable motif-CSV generator")
    ap.add_argument("--n",     type=int, required=True, help="# primes to export")
    ap.add_argument("--csv",   type=str, required=True, help="output CSV file")
    ap.add_argument("--state", type=str, default="state.json",
                    help="JSON resume-state file")
    args = ap.parse_args()

    N, csv_path, state_path = args.n, args.csv, args.state
    done, saved = load_progress(csv_path, state_path)
    if done >= N:
        print(f"[DONE  ] already exported {done} ≥ requested {N}", flush=True)
        return

    law = McCracknsPrimeLaw(n_primes=N, verbose=False)

    # ---------- fast-forward if resuming ----------
    if saved:
        law.regime_points = saved.get("regime_points", [6])
        print(f"[CATCH ] fast-forwarding to idx={done} …", flush=True)
        t0 = time.perf_counter()
        for _ in range(len(law.primes), done):
            law.generate_one()
        print(f"[CATCH ] done in {time.perf_counter() - t0:.1f}s", flush=True)

    # ---------- streaming CSV output --------------
    new_file = not os.path.exists(csv_path)
    with open(csv_path, "a" if not new_file else "w",
              newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        if new_file:
            wr.writerow(["index", "prime", "gap", "motif"])

        total  = N - done
        every  = max(total // 200, 1)          # ~0.5 % progress prints
        start  = time.perf_counter()

        for idx, p, g, m in law.stream_primes(start_idx=done + 1):
            wr.writerow([idx, p, g, m])
            if idx % 1000 == 0:
                fh.flush()
            if (idx - done) % every == 0 or idx == N:
                elapsed = time.perf_counter() - start
                pct = (idx - done) / total * 100
                eta = elapsed * (total - (idx - done)) / max(idx - done, 1)
                print(f"[WRITE ] {idx}/{N} ({pct:5.1f} %) | "
                      f"elapsed {elapsed:6.1f}s | ETA {eta:6.1f}s",
                      flush=True)
            if idx >= N:
                break

    save_state(law, state_path)
    print(f"✅  CSV complete up to n={N}", flush=True)


if __name__ == "__main__":
    main()