from cost_model import audit_bounded_prefix_cost


def test_cost_model_reports_bounded_status_without_proving_o1():
    report = audit_bounded_prefix_cost(n_primes=12)

    assert report.bounded_prefix_only is True
    assert report.proves_o1 is False
    assert report.constant_within_prefix is True
    assert "bounded finite motif tape" in report.limitation
    assert "v3 mpl-normalized symbolic o(1) claim" in report.limitation.lower()


def test_cost_model_separates_symbolic_steps_from_bit_complexity():
    report = audit_bounded_prefix_cost(n_primes=4)
    assumptions = " ".join(report.assumptions).lower()

    assert "symbolic step" in assumptions
    assert "bit complexity" in assumptions
    assert "python sorting/cache overhead" in assumptions
