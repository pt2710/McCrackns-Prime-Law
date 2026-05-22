from verify_axis_bridge import verify_axis_bridge_prefix


def test_axis_bridge_matches_bounded_mpl_prefix():
    results = verify_axis_bridge_prefix(n_primes=12)

    assert len(results) == 11
    assert all(result.matches for result in results)


def test_axis_bridge_uses_expected_realized_axis_prefixes():
    results = verify_axis_bridge_prefix(n_primes=5)

    assert results[1].realized_axes == (2, 3)
    assert results[1].current_prime == 3
    assert results[1].axis_next_prime == 5

    assert results[2].realized_axes == (2, 3, 5)
    assert results[2].current_prime == 5
    assert results[2].axis_next_prime == 7

    assert results[3].realized_axes == (2, 3, 5, 7)
    assert results[3].current_prime == 7
    assert results[3].axis_next_prime == 11
