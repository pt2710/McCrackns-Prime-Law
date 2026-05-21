from triadic_domains import TriadicDomains


def test_unity_even_odd_placements():
    domains = TriadicDomains([2, 3, 5, 7])

    assert domains.place(1).domain == "U"
    assert domains.place(1).axis == "U1"

    placed_even = domains.place(40)
    assert placed_even.domain == "E"
    assert placed_even.axis == "E3"
    assert placed_even.cofactor == 5

    placed_prime = domains.place(31)
    assert placed_prime.domain == "O"
    assert placed_prime.axis == "O1"
    assert placed_prime.kind == "odd-prime"


def test_odd_composites_are_lpf_axis_placed():
    domains = TriadicDomains([2, 3, 5, 7])

    expected = {
        9: ("O2", 3, 3),
        15: ("O2", 3, 5),
        21: ("O2", 3, 7),
        25: ("O3", 5, 5),
        27: ("O2", 3, 9),
        35: ("O3", 5, 7),
        49: ("O4", 7, 7),
    }

    for value, (axis, lpf, cofactor) in expected.items():
        placement = domains.place(value)
        assert placement.domain == "O"
        assert placement.kind == "odd-composite"
        assert placement.axis == axis
        assert placement.least_prime_factor == lpf
        assert placement.cofactor == cofactor


def test_axis_law_first_hole_examples():
    domains_after_3 = TriadicDomains([2, 3])
    assert domains_after_3.axis_law_successor_gap(3, limit=16) == (5, 2)
    assert domains_after_3.axis_law_successor_gap(5, limit=16) == (7, 2)
    assert domains_after_3.axis_law_successor_gap(7, limit=16) == (11, 4)

    domains_after_7 = TriadicDomains([2, 3, 5, 7])
    assert domains_after_7.axis_law_successor_gap(29, limit=64) == (31, 2)
    assert domains_after_7.place(31).axis == "O1"


def test_composite_stream_has_canonical_lpf_entries_without_duplicate_axes():
    domains = TriadicDomains([2, 3, 5, 7])
    placements = {p.value: p for p in domains.odd_composite_stream(50)}

    assert placements[15].axis == "O2"
    assert placements[15].least_prime_factor == 3
    assert placements[25].axis == "O3"
    assert placements[35].axis == "O3"
    assert placements[49].axis == "O4"
