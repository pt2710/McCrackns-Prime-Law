from pathlib import Path

from mccrackns_prime_law import McCracknsPrimeLaw


ROOT = Path(__file__).resolve().parents[1]


def test_u1_gap_is_seed_only_and_post_seed_gaps_are_even():
    law = McCracknsPrimeLaw(n_primes=200)
    law.generate()

    gaps = law.get_gaps()
    motifs = [label for label, _run in law.get_motifs()]

    assert gaps[0] == 1
    assert gaps.count(1) == 1
    assert motifs[0] == "U1"
    assert "U1" not in motifs[1:]
    assert all(gap % 2 == 0 for gap in gaps[1:])


def test_mpl_file_is_not_wheel_or_fixed_early_schedule():
    source = (ROOT / "mccrackns_prime_law.py").read_text(encoding="utf-8")
    lowered = source.lower()

    forbidden_markers = [
        "wheel(30)",
        "wheel_30",
        "hardcoded early schedule",
        "early_minimal_schedule",
        "gcd filter",
        "gcd filtering",
        "trial division",
        "sieve",
        "candidate scanning",
        "wheel",
    ]

    for marker in forbidden_markers:
        assert marker not in lowered


def test_gcd_is_not_active_in_mpl_generator():
    source = (ROOT / "mccrackns_prime_law.py").read_text(encoding="utf-8").lower()

    assert "from math import gcd" not in source
    assert "gcd(" not in source
