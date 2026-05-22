from pathlib import Path

import pytest

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
        "axiseventscheduler",
        "events.pop",
        "_reschedule",
        "event table",
        "first-hole",
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


def test_mpl_runtime_uses_regime_motif_scheduler_not_axis_events():
    source = (ROOT / "mccrackns_prime_law.py").read_text(encoding="utf-8")

    assert "class RegimeMotifScheduler" in source
    assert "AxisEventScheduler" not in source
    assert "frontier" not in source


def test_gcd_is_not_active_in_mpl_generator():
    source = (ROOT / "mccrackns_prime_law.py").read_text(encoding="utf-8").lower()

    assert "from math import gcd" not in source
    assert "gcd(" not in source


def test_stream_primes_yields_seed_when_starting_at_one():
    rows = list(McCracknsPrimeLaw(n_primes=4).stream_primes(start_idx=1))

    assert rows == [
        (1, 2, 0, "U1"),
        (2, 3, 1, "U1"),
        (3, 5, 2, "E1.0"),
        (4, 7, 2, "E1.0"),
    ]


def test_stream_primes_start_idx_two_starts_at_second_prime():
    rows = list(McCracknsPrimeLaw(n_primes=4).stream_primes(start_idx=2))

    assert rows[0] == (2, 3, 1, "U1")


def test_bounded_runtime_reports_prefix_exhaustion():
    law = McCracknsPrimeLaw(n_primes=McCracknsPrimeLaw.max_supported_primes() + 1)

    with pytest.raises(RuntimeError, match="finite MPL motif tape exhausted"):
        law.generate()
