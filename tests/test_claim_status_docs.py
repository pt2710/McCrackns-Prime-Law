from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_doc(path: str) -> str:
    return " ".join((ROOT / path).read_text(encoding="utf-8").lower().split())


def test_claim_status_matrix_exists_and_does_not_overclaim():
    text = read_doc("docs/claim_status_matrix.md")

    required_phrases = [
        "tc -> axis / first-hole -> derivation-level lagged scheduler",
        "mpl-normalized motif-to-motif symbolic transition cost",
        "repository does not prove concrete data-structure o(1)",
        "bit-complexity o(1)",
        "explicit certificate-frontier materialization",
        "25421497ec8b4dfd2e33e9b5b135a93d2e6f6368",
        "09157d77ae26baab8e942a18253ad537f5ac07b4",
        "bounded executable prefix / regression harness",
        "full compressed unbounded mpl regime-motif runtime",
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
        "mpl-normalized motif-to-motif symbolic transition cost",
        "bit-complexity",
        "expanded integer output",
        "explicit certificate-frontier materialization",
        "concrete data-structure runtime",
        "regime state",
        "active motif alphabet construction",
        "lex-minimal motif selection",
        "regime innovation update",
        "successor emission",
        "axis law equivalence",
        "sentinel separation",
        "cost model",
        "validation plan",
        "lagged_certificate_frontier.py",
        "bounded lagged-closure compression theorem remains open",
    ]

    for phrase in required_obligations:
        assert phrase in text


def test_theorem_map_marks_full_scheduler_and_o1_as_obligations():
    text = read_doc("docs/theorem_implementation_map.md")

    assert "section 5.10" in text
    assert "mpl-normalized symbolic complexity" in text
    assert "motif-to-motif symbolic transition cost" in text
    assert "explicit frontier materialization" in text
    assert "r2/r3/r4/r10" in text
    assert "25421497ec8b4dfd2e33e9b5b135a93d2e6f6368" in text
    assert "09157d77ae26baab8e942a18253ad537f5ac07b4" in text
    assert "proof obligation" in text
    assert "derivation-level lagged tc certificate-frontier scheduler" in text
    assert "tc alone is not used as a prime generator" in text


def test_readme_starts_from_tc_layer_and_keeps_final_cost_boundary():
    text = read_doc("README.md")

    required_phrases = [
        "triadic completeness (tc)",
        "mpl is the regime-motif / lex-min readout",
        "tc -> axis / first-hole -> derivation-level lagged scheduler",
        "mpl-normalized symbolic o(1)",
        "motif-to-motif symbolic",
        "not a claim about bit complexity",
        "concrete python data-structure runtime",
        "pr #5",
        "25421497ec8b4dfd2e33e9b5b135a93d2e6f6368",
        "09157d77ae26baab8e942a18253ad537f5ac07b4",
    ]

    forbidden_phrases = [
        "repository proves o(1)",
        "finite tests prove asymptotic complexity",
        "repository proves the paper",
        "concrete scheduler is o(1)",
    ]

    for phrase in required_phrases:
        assert phrase in text
    for phrase in forbidden_phrases:
        assert phrase not in text
