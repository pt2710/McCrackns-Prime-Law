from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_scheduler_rule_forensics_document_exists_and_covers_targets():
    path = ROOT / "docs" / "scheduler_rule_forensics_v1_v2_v3.md"
    text = path.read_text(encoding="utf-8").lower()

    required = [
        "implementable now: **no**",
        "`a_k` construction",
        "motif compatibility",
        "legal gap readout",
        "lex-min selection",
        "regime rebuild",
        "executable motif compatibility definition",
        "check-free `a_k` construction theorem",
        "scheduler readout theorem",
        "lex-min runtime realization lemma",
        "regime rebuild recursion",
    ]

    for phrase in required:
        assert phrase in text
