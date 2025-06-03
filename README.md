# McCrackn’s Prime Law

_Repository slug:_ `mccrackns_prime_law`

---

## Abstract

This project implements **McCrackn’s Prime Law**—an explicit, recursive, and deterministic equation for generating the prime sequence.

---

## Installation

```bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

## Usage

To run all scientific tests:

```bash
python test_mccrackn_conjector.py
```

All generated output (CSV data, PNGs) will be saved in the `figures/` directory.

---

## Project Structure

```
mccrackns_prime_law/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── mccrackn_conjector.py
├── numbers_domains.py
├── test_mccrackn_conjector.py
├── figures/
│   ├── prime_gaps_histogram.png
│   ├── prime_gaps_evolution.png
│   ├── motif_innovation_histogram.png
│   ├── motif_run_histogram.png
│   ├── motif_innovation.csv
│   └── ...
├── gaps/
│   ├── prime_gaps.csv
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
```

- **mccrackn_prime_law.py**: Core implementation of McCrackn’s Prime Law.
- **numbers_domains.py**: Domain classification utilities for primes.
- **test_mccrackn_prime_law.py**: Unit tests and scientific validation scripts.
- **motif_innovation.csv**, **prime_gaps.csv**: Example datasets used by the implementation.
- **figures/**: Generated plots (e.g., prime gaps histogram, evolution).
- **gaps/**: CSV files tracking gap sequences under various regimes.
- **src/**: Auxiliary modules (e.g., helper functions).
- **configs/**: YAML configuration files.
- **tests/**: Basic unit tests.
- **.github/workflows/ci.yml**: Continuous Integration configuration.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
```
