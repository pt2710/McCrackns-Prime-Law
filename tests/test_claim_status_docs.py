from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


def test_claim_status_matrix_exists_and_does_not_overclaim():
    text = read_doc("docs/claim_status_matrix.md")

    required_phrases = [
        "bounded executable prefix / regression harness",
        "full unbounded mpl regime-motif scheduler remains",
        "o(1) unit-cost theorem has been implemented or proved by tests",
        "gcd generator",
        "first-hole language is reserved for the axis law relative to",
        "m_j = <{2} union p_j>",
        "pure dyadic powers",
        "pure even lifts",
        "even unity-sets",
        "first-order odd unity-sets",
        "lpf-stratified odd composites",
        "mixed even composites",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_unbounded_scheduler_proof_obligations_are_explicit():
    text = read_doc("docs/unbounded_scheduler_proof_obligations.md")

    required_obligations = [
        "regime state",
        "active motif alphabet construction",
        "lex-minimal motif selection",
        "regime innovation update",
        "successor emission",
        "axis law equivalence",
        "sentinel separation",
        "cost model",
        "validation plan",
        "no experimental unbounded scheduler is added here",
    ]

    for phrase in required_obligations:
        assert phrase in text


def test_theorem_map_marks_full_scheduler_and_o1_as_obligations():
    text = read_doc("docs/theorem_implementation_map.md")

    assert "full unbounded mpl scheduler" in text
    assert "proof obligation" in text
    assert "theorem 6.17" in text
    assert "o(1) unit-cost successor" in text
    assert "tc alone is not used as a prime generator" in text
