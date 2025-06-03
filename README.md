# McCrackn's Prime Law

_Repository slug:_ `mccrackns_prime_law`

---

## Abstract

This project implements **McCrackn's Prime Law**—an explicit, recursive, and deterministic equation for the generation of the prime sequence.

---

## Installation

```bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## Usage

To run all scientific tests and generate publication-grade figures (histograms/statistics):

```bash
python test_mccrackn_conjector.py
```

All output (CSV data, PNGs) will be saved in `figures/`.

---

## Project Structure

mccrackns_prime_law/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── mccrackn_conjector.py
├── numbers_domains.py
├── test_mccrackn_conjector.py
├── motif_innovation.csv
├── prime_gaps.csv
├── figures/
│   ├── prime_gaps_histogram.png
│   ├── prime_gaps_evolution.png
│   ├── motif_innovation_histogram.png
│   ├── motif_run_histogram.png
│   └── ...
├── gaps/
│   └── gap_sequence_E*.csv
├── src/
│   └── your_module.py
├── configs/
│   └── default.yaml
├── tests/
│   └── test_basic.py
└── .github/
    └── workflows/
        └── ci.yml

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
