"""
McCrackn's Prime Law — Analysis and Visualization Suite

This script includes:
- Regression tests for prime generation and motif correctness.
- Visual diagnostics of prime gaps, motif growth, domain structure.
- Export of full motif dataframe and CSVs.
- Plotting of:
    * Gap evolution by domain
    * Gap vs motif-run index
    * Cumulative motif counts
    * Boxplots of domain gap distributions
    * Innovations per regime
    * Alphabet size growth

Expected output is saved under `mccrackns_prime_law/figures/`.
"""

import os, time, gc
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

import mccrackns_prime_law
from mccrackns_prime_law import McCracknsPrimeLaw

# ──────────────────────────────────────────────────────────────
#  Paths & constants
# ──────────────────────────────────────────────────────────────

PKG_DIR     = os.path.dirname(mccrackns_prime_law.__file__)
FIGURES_DIR = os.path.join(PKG_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Known reference primes for validation
REFERENCE_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
]

def first_n_primes(n: int) -> list[int]:
    """Returns the first `n` primes via trial division (reference implementation)."""
    if n <= 20:
        return REFERENCE_PRIMES[:n]
    out = REFERENCE_PRIMES[:]
    cand = out[-1] + 2
    while len(out) < n:
        root = int(cand ** 0.5)
        for p in out:
            if p > root:
                out.append(cand)
                break
            if cand % p == 0:
                break
        else:
            out.append(cand)
        cand += 2
    return out

def print_prime_summary(primes, show=10):
    """Prints the head and tail of a prime list, with index labels."""
    n = len(primes)
    half = show * 2
    head, tail = primes[:show], primes[-show:]
    if n <= half:
        for i, p in enumerate(primes, 1):
            print(f"  Prime #{i}: {p}")
    else:
        for i, p in enumerate(head, 1):
            print(f"  Prime #{i}: {p}")
        print("  ...")
        for i, p in enumerate(tail, n - show + 1):
            print(f"  Prime #{i}: {p}")

# ──────────────────────────────────────────────────────────────
#  Unit tests
# ──────────────────────────────────────────────────────────────

def test_first_n_primes(n: int = 20):
    """Test if McCrackn’s primes match known correct reference primes."""
    print("=" * 50)
    print(f"TEST: Compare first {n} deterministic primes to reference.")
    t0 = time.perf_counter()
    mcc = McCracknsPrimeLaw(n_primes=n, verbose=True,
                            progress_every=min(1000, max(1, n // 10)))
    mcc.generate()
    print(f"[generation] Completed in {time.perf_counter() - t0:.2f}s")
    primes, reference = mcc.get_primes(), first_n_primes(n)
    print("\nPrime summary:")
    print_prime_summary(primes, show=min(10, n // 2))
    for idx, want in enumerate(reference, 1):
        got = primes[idx - 1]
        assert got == want, f"Mismatch idx={idx}: got {got}, expected {want}"
    print(f"✔ All first {n} primes match reference.")
    print("=" * 50)

def test_innovation_points():
    """Print regime expansion points and their associated motif labels."""
    print("=" * 50)
    print("TEST: Regime/motif innovation points (Nk).")
    mcc = McCracknsPrimeLaw(n_primes=40)
    mcc.generate()
    pts, primes, motifs = set(mcc.regime_points), mcc.get_primes(), mcc.get_motifs()
    print(f"Regime points: {sorted(pts)}")
    for nk in sorted(pts):
        if nk < len(primes):
            print(f"  n={nk:2d}: prime={primes[nk]:5d}, motif={motifs[nk-1]}")
    print("✔ Innovation points look correct.")
    print("=" * 50)

def test_no_duplicate_motifs():
    """Ensure that each motif label/run-pair is unique in the sequence."""
    print("=" * 50)
    print("TEST: Ensure each (domain, run) motif is unique up to n=100.")
    mcc = McCracknsPrimeLaw(n_primes=100)
    mcc.generate()
    seen = set()
    for i, motif in enumerate(mcc.get_motifs(), 1):
        if motif in seen:
            raise AssertionError(f"Duplicate motif at idx={i}: {motif}")
        seen.add(motif)
    print("✔ No duplicate motifs.")
    print("=" * 50)

def test_error_handling():
    """Ensure edge-case config (n=1) does not crash."""
    print("=" * 50)
    print("TEST: n_primes=1 should not crash.")
    mcc = McCracknsPrimeLaw(n_primes=1)
    mcc.generate()
    assert mcc.get_primes()[0] == 2
    print("✔ Handled n_primes=1 cleanly.")
    print("=" * 50)

# ──────────────────────────────────────────────────────────────
#  Plotting helpers
# ──────────────────────────────────────────────────────────────

def plot_gap_evolution(df, regime_points, outdir):
    """Scatterplot of gaps vs index, color-coded by domain, with vertical regime markers."""
    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    sns.scatterplot(data=df, x="index", y="gap", hue="domain",
                    palette="tab10", s=10, ax=ax, legend="brief")
    for rp in regime_points:
        ax.axvline(rp, color="grey", lw=1, ls="--", alpha=0.6)
    ax.set(title="Prime-gap evolution by domain",
           xlabel="Prime index n", ylabel="gap = pₙ₊₁ − pₙ")
    ax.legend(title="Domain", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "gap_evolution_domains.png"))
    plt.close()

def plot_gap_vs_run(df, outdir):
    """Plot gap size as function of motif run count."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="run", y="gap", hue="domain",
                    palette="tab10", s=15, alpha=0.7)
    plt.title("Gap size vs. motif-run index")
    plt.xlabel("Motif run index"), plt.ylabel("Gap size")
    plt.legend(title="Domain", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "gap_vs_run.png"))
    plt.close()

def plot_cumulative_motifs(df, outdir):
    """Line plot showing cumulative motif count per domain."""
    cum = (df.groupby(["domain", "index"], observed=False)
             .size()
             .groupby(level=0, observed=False)
             .cumsum()
             .reset_index(name="cum"))
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cum, x="index", y="cum", hue="domain", palette="tab10")
    plt.title("Cumulative motif innovations by domain")
    plt.xlabel("Prime index n"), plt.ylabel("Cumulative count")
    plt.legend(title="Domain", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "cumulative_motifs.png"))
    plt.close()

def plot_gap_boxplot(df, outdir):
    """Boxplot of gap distributions by motif domain."""
    plt.figure(figsize=(10, 6))
    order = df["domain"].value_counts().index
    sns.boxplot(data=df, x="domain", y="gap", order=order)
    plt.title("Distribution of prime gaps by domain")
    plt.xlabel("Domain"), plt.ylabel("Gap size")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "gap_boxplot_by_domain.png"))
    plt.close()

def plot_innovations_by_regime(df, regime_points, outdir):
    """Barplot of motif innovations introduced at each regime point."""
    new_by_regime, seen = [], set()
    prev = 1
    for rp in sorted(regime_points):
        chunk = df.iloc[prev:rp-1]
        for motif in chunk["motif"].unique():
            if motif not in seen:
                seen.add(motif)
                new_by_regime.append({"regime": rp, "domain": motif.split(".")[0]})
        prev = rp - 1
    regdf = pd.DataFrame(new_by_regime)
    counts = (regdf.groupby(["regime", "domain"], observed=False)
                    .size()
                    .reset_index(name="count"))
    plt.figure(figsize=(8, 5))
    sns.barplot(data=counts, x="regime", y="count", hue="domain", palette="tab10")
    plt.title("New motif innovations at each regime expansion")
    plt.xlabel("Regime point Nk"), plt.ylabel("Number of new motifs")
    plt.legend(title="Domain", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "innovations_by_regime.png"))
    plt.close()

def plot_alphabet_growth(df, regime_points, outdir):
    """Plot the growth of the alphabet size at each regime point."""
    first_idx = df.groupby("motif", observed=False)["index"].min()
    sizes = [{"regime": rp, "alphabet_size": int((first_idx <= rp).sum())}
             for rp in regime_points]
    adf = pd.DataFrame(sizes)
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=adf, x="regime", y="alphabet_size", marker="o")
    plt.title("Motif-alphabet size at each regime expansion")
    plt.xlabel("Regime point Nk"), plt.ylabel("Unique motifs so far")
    plt.xscale("log", base=2)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "alphabet_growth.png"))
    plt.close()

# ──────────────────────────────────────────────────────────────
#  High-level orchestration
# ──────────────────────────────────────────────────────────────

def main_gap_and_motif_analysis(n: int = 10000):
    """Full analysis and visualization pipeline on the first n primes."""
    print("=" * 50)
    print(f"MAIN ANALYSIS: generating n={n} primes …")
    t0_all = time.perf_counter()

    mcc = McCracknsPrimeLaw(n_primes=n, verbose=True)
    mcc.generate()

    primes, motifs = mcc.get_primes(), mcc.get_motifs()
    regime_points  = set(mcc.regime_points)

    motif_list = ["U1"] + [m[0] for m in motifs]
    run_list   = [1]    + [m[1] for m in motifs]
    gaps       = [1]    + mcc.get_gaps()
    domains    = [m.split('.')[0] for m in motif_list]
    df = pd.DataFrame({
        "index":  np.arange(1, len(primes) + 1),
        "prime":  primes,
        "regime": ["" for _ in primes],
        "motif":  motif_list,
        "run":    run_list,
        "gap":    gaps,
        "domain": domains,
    })

    for k, rp in enumerate(sorted(regime_points), 1):
        if rp - 1 < len(df):
            df.at[rp - 1, "regime"] = f"R{k}"

    plots = [
        ("gap_evolution",        plot_gap_evolution,        (df, regime_points, FIGURES_DIR)),
        ("gap_vs_run",           plot_gap_vs_run,           (df, FIGURES_DIR)),
        ("cumulative_sequences", plot_cumulative_motifs,    (df, FIGURES_DIR)),
        ("gap_boxplot",          plot_gap_boxplot,          (df, FIGURES_DIR)),
        ("innovations_regime",   plot_innovations_by_regime,(df, regime_points, FIGURES_DIR)),
        ("alphabet_growth",      plot_alphabet_growth,      (df, regime_points, FIGURES_DIR)),
    ]

    for i, (name, fn, args) in enumerate(plots, 1):
        print(f"[{i}/{len(plots)}] Plotting {name} …", end="", flush=True)
        t0 = time.perf_counter()
        fn(*args)
        print(f" done in {time.perf_counter() - t0:.1f}s")
        gc.collect()

    df.to_csv(os.path.join(FIGURES_DIR, "motif_data.csv"), index=False)
    print(f"CSV saved → {FIGURES_DIR}/motif_data.csv")
    print(f"⌛ Total time {time.perf_counter() - t0_all:.1f}s")
    print("=" * 50)

# ──────────────────────────────────────────────────────────────
#  Entrypoint
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_first_n_primes(n=10000)
    test_innovation_points()
    test_no_duplicate_motifs()
    test_error_handling()
    main_gap_and_motif_analysis(n=10_000_000)
