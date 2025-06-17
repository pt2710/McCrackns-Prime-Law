from collections import defaultdict
import os
import time
import gc

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

import mccrackns_prime_law
from mccrackns_prime_law import McCracknsPrimeLaw

# Directories
PKG_DIR     = os.path.dirname(mccrackns_prime_law.__file__)
FIGURES_DIR = os.path.join(PKG_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Reference primes for testing
REFERENCE_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71
]

def print_prime_summary(primes, show=10):
    n = len(primes)
    half = show * 2
    # Case 1: small list—print all
    if n <= half:
        for i, p in enumerate(primes, 1):
            print(f"  Prime #{i}: {p}")
        return

    # Case 2: large list—print head, ellipsis, tail
    head = primes[:show]
    tail = primes[-show:]
    for i, p in enumerate(head, 1):
        print(f"  Prime #{i}: {p}")
    print("  ...")
    start = n - show + 1
    for offset, p in enumerate(tail, start):
        print(f"  Prime #{offset}: {p}")


def test_first_n_primes(n=50):
    print("="*50)
    print(f"TEST: Compare first {n} deterministic primes to reference sequence:")

    # 1) generate
    t0 = time.perf_counter()
    mcc = McCracknsPrimeLaw(n_primes=n, verbose=True)
    mcc.generate()
    dt = time.perf_counter() - t0
    print(f"[generation] Completed in {dt:.2f}s")

    # 2) summary & verify
    primes = mcc.get_primes()
    print("\nPrime summary:")
    print_prime_summary(primes)
    for idx, want in enumerate(REFERENCE_PRIMES, 1):
        got = primes[idx-1]
        assert got == want, f"Mismatch at idx={idx}: got {got}, expected {want}"

    print(f"\n✔ All first {len(REFERENCE_PRIMES)} primes match reference.")
    print("="*50)


def test_innovation_points():
    print("="*50)
    print("TEST: Regime/motif innovation points (Nk) and offset check:")

    t0 = time.perf_counter()
    mcc = McCracknsPrimeLaw(n_primes=40)
    mcc.generate()
    dt = time.perf_counter() - t0
    print(f"[generation] Completed in {dt:.2f}s")

    pts    = set(mcc.regime_points)
    primes = mcc.get_primes()
    motifs = mcc.get_motifs()

    print(f"Regime points (Nk): {sorted(pts)}")
    for nk in sorted(pts):
        if nk < len(primes):
            print(f"  n={nk}: prime={primes[nk]}, motif={motifs[nk-1]}")
    print("✔ Innovation points look correct.")
    print("="*50)

def test_no_duplicate_motifs():
    print("="*50)
    print("TEST: Ensure each (domain, run) motif is unique up to n=100:")

    t0 = time.perf_counter()
    motifs = McCracknsPrimeLaw(n_primes=100).generate() or McCracknsPrimeLaw(n_primes=100).get_motifs()
    dt = time.perf_counter() - t0
    print(f"[generation] Completed in {dt:.2f}s")

    seen = set()
    for i, motif in enumerate(motifs, 1):
        if motif in seen:
            raise AssertionError(f"Duplicate motif at idx={i}: {motif}")
        seen.add(motif)

    print("✔ No duplicate motifs.")
    print("="*50)


def test_error_handling():
    print("="*50)
    print("TEST: n_primes=1 should not crash:")

    t0 = time.perf_counter()
    primes = McCracknsPrimeLaw(n_primes=1).generate() or McCracknsPrimeLaw(n_primes=1).get_primes()
    dt = time.perf_counter() - t0
    print(f"[generation] Completed in {dt:.2f}s")

    assert primes[0] == 2, f"First prime should be 2, got {primes[0]}"
    print(f"✔ Handled n_primes=1 without crashing; got seed primes {primes}")
    print("="*50)


def main_gap_and_motif_analysis(n=100_000):
    start_all = time.perf_counter()

    mcc = McCracknsPrimeLaw(n_primes=n)
    mcc.generate()
    primes = mcc.get_primes()
    motifs = mcc.get_motifs()
    regime_points = set(mcc.regime_points)

    # Include p1=2 as the first prime, and ensure all lists match in length
    # For motifs: first is always "U1", run=1 (for p1=2)
    motif_list = ["U1"] + [m[0] for m in motifs]
    run_list   = [1]    + [m[1] for m in motifs]
    gaps       = [1]    + mcc.get_gaps()  # First gap for p1=2 is 1 by convention
    domains    = [m.split('.')[0] for m in motif_list]

    n_full = len(primes)
    index = np.arange(1, n_full + 1)

    # Build regime column: "R1", "R2", ... at regime innovation points (rest are "")
    regime_points_sorted = sorted(regime_points)
    regime_col = [""] * n_full
    for k, rp in enumerate(regime_points_sorted, 1):
        df_idx = rp - 1  # p6 (rp=6) is at row 5, since index=1 is row 0
        if 0 <= df_idx < len(regime_col):
            regime_col[df_idx] = f"R{k}"

    df = pd.DataFrame({
        "index": index,
        "prime": primes,
        "regime": regime_col,
        "motif": motif_list,
        "run":   run_list,
        "gap":   gaps,
        "domain": domains,
    })



    # Actual plotting functions
    def plot_gap_evolution():
        plt.figure(figsize=(12,6))
        ax = plt.gca()
        sns.scatterplot(data=df, x="index", y="gap", hue="domain",
                        palette="tab10", s=10, ax=ax, legend="brief")
        for rp in regime_points:
            ax.axvline(rp, color="grey", lw=1, ls="--", alpha=0.7)
        ax.set(title="Prime Gap Evolution (colored by domain)\nwith regime-innovation lines",
               xlabel="Prime index n", ylabel="Gap = pₙ₊₁ − pₙ")
        ax.legend(title="Domain", bbox_to_anchor=(1.02,1), loc="upper left")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "gap_evolution_domains.png"))
        plt.close()

    def plot_gap_vs_run():
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=df, x="run", y="gap", hue="domain",
                        palette="tab10", s=15, alpha=0.7)
        plt.title("Gap size vs. motif run index, colored by domain")
        plt.xlabel("Motif run index")
        plt.ylabel("Gap size")
        plt.legend(title="Domain", bbox_to_anchor=(1.02,1), loc="upper left")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "gap_vs_run.png"))
        plt.close()

    def plot_cumulative_motifs():
        cum = (
            df
            .groupby(["domain", "index"], observed=False)
            .size()
            .groupby(level=0, observed=False)
            .cumsum()
            .reset_index(name="cum_count")
        )
        plt.figure(figsize=(12,6))
        sns.lineplot(data=cum, x="index", y="cum_count", hue="domain", palette="tab10")
        plt.title("Cumulative motif innovations by domain")
        plt.xlabel("Prime index n")
        plt.ylabel("Cumulative count of motifs")
        plt.legend(title="Domain", bbox_to_anchor=(1.02,1), loc="upper left")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "cumulative_motifs.png"))
        plt.close()



    def plot_gap_boxplot():
        plt.figure(figsize=(10,6))
        order = df["domain"].value_counts().index
        sns.boxplot(data=df, x="domain", y="gap", order=order)
        plt.title("Distribution of prime gaps by domain")
        plt.xlabel("Domain")
        plt.ylabel("Gap size")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "gap_boxplot_by_domain.png"))
        plt.close()

    def plot_innovations_by_regime():
        new_by_regime = []
        seen_motifs = set()
        prev_idx = 1

        # collect all new motifs by regime
        for rp in regime_points:
            chunk = df.iloc[prev_idx : rp-1]
            for motif in chunk["motif"].unique():
                if motif not in seen_motifs:
                    seen_motifs.add(motif)
                    new_by_regime.append({"regime": rp, "domain": motif.split(".")[0]})
            prev_idx = rp-1

        # build DataFrame
        regdf = pd.DataFrame(new_by_regime)

        # group with observed=False to silence the FutureWarning
        reg_counts = (
            regdf
            .groupby(["regime", "domain"], observed=False)
            .size()
            .reset_index(name="count")
        )

        fig, ax = plt.subplots(figsize=(8,5))
        sns.barplot(
            data=reg_counts,
            x="regime",
            y="count",
            hue="domain",
            palette="tab10",
            ax=ax
        )
        ax.set(
            title="New motif innovations at each regime expansion",
            xlabel="Regime point Nk",
            ylabel="Number of new motifs",
        )
        ax.legend(title="Domain", bbox_to_anchor=(1.02,1), loc="upper left")
        fig.tight_layout()
        fig.savefig(os.path.join(FIGURES_DIR, "innovations_by_regime.png"))
        plt.close(fig)

    def plot_alphabet_growth():
        # 1) find first index for hver unik motif
        first_idx = (
            df
            .groupby("motif", observed=False)["index"]
            .min()
        )
        # 2) for hver regime-punkt, tæl hvor mange motiver debuterer <= rp
        alpha_sizes = [
            {"regime": rp, "alphabet_size": int((first_idx <= rp).sum())}
            for rp in regime_points
        ]
        adf = pd.DataFrame(alpha_sizes)

        # 3) Tegn det med log‐skala
        fig, ax = plt.subplots(figsize=(8,5))
        sns.lineplot(data=adf, x="regime", y="alphabet_size", marker="o", ax=ax)
        ax.set(
            title="Motif alphabet size at each regime expansion",
            xlabel="Regime point Nk",
            ylabel="Count of unique motifs so far"
        )
        ax.set_xscale("log", base=2)

        # --- robustify the xticks call ---
        # if regime_points is a single int, wrap it in a list
        try:
            ticks = list(regime_points)
        except TypeError:
            ticks = [regime_points]
        ax.set_xticks(ticks)

        # format them nicely
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"{int(x):,}")
        )

        fig.tight_layout()
        fig.savefig(os.path.join(FIGURES_DIR, "alphabet_growth.png"))
        plt.close(fig)


    # Replace placeholders with actual functions
    plot_funcs = [
        plot_gap_evolution, plot_gap_vs_run, plot_cumulative_motifs,
        plot_gap_boxplot, plot_innovations_by_regime, plot_alphabet_growth
    ]

    total_steps = len(plot_funcs) + 1  # +1 for CSV save
    times = []

    # Execute plotting steps with logging
    for idx, func in enumerate(plot_funcs, start=1):
        step_name = func.__name__
        print(f"[{idx}/{total_steps}] Starting: {step_name}")
        t0 = time.perf_counter()
        func()
        duration = time.perf_counter() - t0
        times.append(duration)
        avg = sum(times) / len(times)
        eta = avg * (total_steps - idx)
        print(f"[{idx}/{total_steps}] Completed: {step_name} in {duration:.2f}s | ETA {eta:.2f}s")
        gc.collect()

    # Save raw motif+gap data
    print(f"[{total_steps}/{total_steps}] Saving motif data CSV")
    t0 = time.perf_counter()
    df.to_csv(os.path.join(FIGURES_DIR, "motif_data.csv"), index=False)
    duration = time.perf_counter() - t0
    print(f"[{total_steps}/{total_steps}] Saved CSV in {duration:.2f}s")

    total_time = time.perf_counter() - start_all
    print(f"🔖 All steps completed in {total_time:.2f}s. Figures & data under {FIGURES_DIR}/")

if __name__ == "__main__":
    test_first_n_primes(10000000)
    test_innovation_points()
    test_no_duplicate_motifs()
    test_error_handling()
    main_gap_and_motif_analysis(n=10000000)

