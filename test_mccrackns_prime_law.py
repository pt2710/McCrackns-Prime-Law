from mccrackns_prime_law import McCracknsPrimeLaw
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

REFERENCE_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71
]

def load_gap_lookup(csv_folder):
    import os
    import glob
    import pandas as pd
    gap_lookup = {}
    for path in glob.glob(os.path.join(csv_folder, "gap_sequence_E*.csv")):
        basename = os.path.basename(path)
        try:
            num = int(basename.split("_E")[1].split(".")[0])
            key = f"E{num}"
            seq = pd.read_csv(path)['gap'].astype(int).tolist()
            gap_lookup[key] = seq
        except Exception as e:
            print(f"Warning: could not process {basename}: {e}")
    print(f"Loaded gap_lookup domains: {sorted(gap_lookup.keys())}")
    return gap_lookup

def print_prime_summary(primes, show=10):
    n = len(primes)
    if n <= show * 2:
        # If small, print all
        for i, p in enumerate(primes):
            print(f"  Prime #{i+1}: {p}")
    else:
        # First `show`
        for i in range(show):
            print(f"  Prime #{i+1}: {primes[i]}")
        print("  ...")
        # Last `show`
        for i in range(n - show, n):
            print(f"  Prime #{i+1}: {primes[i]}")

def test_first_n_primes(n=20, gap_lookup=None):
    print("="*50)
    print(f"TEST: Compare first {n} deterministic primes to reference sequence:")
    mcc = McCracknsPrimeLaw(n_primes=n, gap_lookup=gap_lookup)
    mcc.generate()
    primes = mcc.get_primes()
    print("\nPrime summary:")
    print_prime_summary(primes, show=10)
    # Only compare up to length of REFERENCE_PRIMES if n > len(REFERENCE_PRIMES)
    n_ref = min(n, len(REFERENCE_PRIMES))
    for i, (p1, p2) in enumerate(zip(primes[:n_ref], REFERENCE_PRIMES[:n_ref])):
        if p1 != p2:
            raise AssertionError(
                f"Prime mismatch at index {i} (n={i+1}): generated={p1}, reference={p2}"
            )
    print("\nAll values match the reference prime sequence (up to provided reference)!")
    print("="*50)

def test_innovation_points(gap_lookup=None):
    print("="*50)
    print("TEST: Regime/motif innovation points (Nk) and offset check:")
    mcc = McCracknsPrimeLaw(n_primes=40, gap_lookup=gap_lookup)
    mcc.generate()
    regime_points = mcc.regime_points
    primes = mcc.get_primes()
    motifs = mcc.get_motifs()
    print(f"Regime points (Nk): {regime_points}")
    print("Primes and motifs at regime innovation points:")
    for nk in regime_points:
        if nk < len(primes):
            print(f"  n={nk}: p={primes[nk]}, motif={motifs[nk-1]}")
    print("="*50)

def test_no_duplicate_motifs(gap_lookup=None):
    print("="*50)
    print("TEST: Ensure each (domain, run) motif is unique in the sequence:")
    mcc = McCracknsPrimeLaw(n_primes=100, gap_lookup=gap_lookup)
    mcc.generate()
    used = set()
    duplicates = []
    for i, motif in enumerate(mcc.get_motifs()):
        if motif in used:
            duplicates.append((i+1, motif))
        used.add(motif)
    if duplicates:
        print("Duplicate motifs found (index, motif):")
        for idx, m in duplicates:
            print(f"  {idx}: {m}")
    else:
        print("No duplicates – all motifs are unique!")
    print("="*50)

def test_error_handling(gap_lookup=None):
    print("="*50)
    print("TEST: Error handling for extremely small n_primes (should not fail):")
    try:
        mcc = McCracknsPrimeLaw(n_primes=1, gap_lookup=gap_lookup)
        mcc.generate()
        print("OK (no crash for n_primes=1)")
        print(f"Primes generated: {mcc.get_primes()}")
    except Exception as e:
        print("Error:", e)
    print("="*50)

def save_gap_histogram(primes, out_dir="figures", out_dir_gaps="gaps", bins=50):
    os.makedirs(out_dir, exist_ok=True)
    gaps = np.diff(primes)
    plt.figure(figsize=(10, 6))
    sns.histplot(gaps, bins=bins, kde=True)
    plt.xlabel("Prime Gap")
    plt.ylabel("Count")
    plt.title("Prime Gap Histogram (First N Primes)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "prime_gaps_histogram.png"), dpi=300)
    plt.close()
    # Save gap data for reference
    pd.DataFrame({"gap": gaps}).to_csv(os.path.join(out_dir_gaps, "prime_gaps.csv"), index=False)
    print(f"Saved gap histogram and data to {out_dir_gaps}/")

def save_gap_evolution(primes, out_dir="figures"):
    os.makedirs(out_dir, exist_ok=True)
    gaps = np.diff(primes)
    plt.figure(figsize=(12, 6))
    plt.plot(range(2, len(primes)+1), gaps, lw=0.6)
    plt.xlabel("n (prime index)")
    plt.ylabel("Gap (p_{n+1} - p_n)")
    plt.title("Prime Gap Evolution (First N Primes)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "prime_gaps_evolution.png"), dpi=300)
    plt.close()
    print(f"Saved gap evolution plot to {out_dir}/")

def save_motif_stats(motifs, out_dir="figures"):
    os.makedirs(out_dir, exist_ok=True)
    # Motif as tuple: (domain, run)
    motifs_df = pd.DataFrame(motifs, columns=["domain", "run"])
    # Histogram by domain
    plt.figure(figsize=(10, 5))
    sns.countplot(y=motifs_df["domain"], order=motifs_df["domain"].value_counts().index)
    plt.xlabel("Count")
    plt.ylabel("Domain")
    plt.title("Motif Innovation Count by Domain")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "motif_innovation_histogram.png"), dpi=300)
    plt.close()
    # Histogram of run indices (across all domains)
    plt.figure(figsize=(8, 4))
    sns.histplot(motifs_df["run"], bins=40, kde=False)
    plt.xlabel("Run Index")
    plt.ylabel("Frequency")
    plt.title("Distribution of Motif Run Indices")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "motif_run_histogram.png"), dpi=300)
    plt.close()
    # Save motif data for reference
    motifs_df.to_csv(os.path.join(out_dir, "motif_innovation.csv"), index=False)
    print(f"Saved motif histograms and CSV to {out_dir}/")

def main_gap_and_motif_analysis(n=100000, gap_lookup=None, out_dir="figures"):
    mcc = McCracknsPrimeLaw(n_primes=n, gap_lookup=gap_lookup)
    mcc.generate()
    primes = mcc.get_primes()
    motifs = mcc.get_motifs()
    save_gap_histogram(primes, out_dir=out_dir)
    save_gap_evolution(primes, out_dir=out_dir)
    save_motif_stats(motifs, out_dir=out_dir)

if __name__ == "__main__":
    gap_lookup = load_gap_lookup("./gaps")  # Path to your gap_sequence_E*.csv files
    try:
        test_first_n_primes(10000000, gap_lookup)
    except AssertionError as e:
        print(f"ERROR: {e}")
        import sys; sys.exit(1)
    print()
    test_innovation_points(gap_lookup)
    print()
    test_no_duplicate_motifs(gap_lookup)
    print()
    test_error_handling(gap_lookup)
    print()

    main_gap_and_motif_analysis(n=10000000, gap_lookup=gap_lookup, out_dir="figures")
