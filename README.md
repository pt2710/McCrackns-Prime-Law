# McCrackn’s Prime Law

_Repository slug:_ `mccrackns_prime_law`

---

## Abstract

This project implements **McCrackn’s Prime Law**—an explicit, recursive, and deterministic equation for generating the prime sequence.  
Unlike all previous approaches, this law generates each next prime **directly from the previous prime, without any search, randomness, or empirical lookup tables**.  
It is supported by rigorous proofs, large-scale computational validation (up to \( n = 10^7 \)), and open, reproducible code.

**Full manuscript:**  
[deterministic_equation_of_primes.pdf](https://github.com/pt2710/McCrackns-Prime-Law/blob/main/deterministic_equation_of_primes.pdf)

---

## Scientific Significance

Prime numbers have long been regarded as the archetype of unpredictability in mathematics.  
McCrackn’s Prime Law addresses a centuries-old challenge by providing a constructive, closed-form process for prime generation.  
If validated by the community, this breakthrough stands to reshape the foundations of analytic number theory.

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
python test_mccrackns_prime_law.py
```

All generated output (CSV data, PNGs) will be saved in the `figures/` directory.

To generate the prime sequence up to a specified limit, for example \(10^7\):

```bash
python mccrackns_prime_law.py --limit 10000000
```

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
│   ├── prime_gaps.csv
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
```

* **mccrackn_conjector.py**: Core implementation of McCrackn’s Prime Law.  
* **numbers_domains.py**: Domain classification utilities for primes.  
* **test_mccrackn_conjector.py**: Unit tests and scientific validation scripts.  
* **motif_innovation.csv**, **prime_gaps.csv**: Example datasets used by the implementation.  
* **figures/**: Generated plots (e.g., prime gaps histogram, evolution).  
* **gaps/**: CSV files tracking gap sequences under various regimes.  
* **src/**: Auxiliary modules (e.g., helper functions).  
* **configs/**: YAML configuration files.  
* **tests/**: Basic unit tests.  
* **.github/workflows/ci.yml**: Continuous Integration configuration.

---

## Reproducibility & Open Science

> **This repository and its contents are shared openly for transparent verification, discussion, and critique by the mathematical community.**  
> Advancement in mathematics requires collective scrutiny and constructive debate.  
> All serious questions, challenges, or feedback are welcome.

* All code, data, and results are provided to enable full reproducibility.  
* Validation scripts and reference comparisons are included for independent testing.

If you are a professional mathematician interested in collaborating, providing feedback, or offering peer review, please contact the author below.

---

## Preprint & Submission History

* **Full manuscript:** [deterministic_equation_of_primes.pdf](https://github.com/pt2710/McCrackns-Prime-Law/blob/main/deterministic_equation_of_primes.pdf)  

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Budd McCrackn**  
Contact: \[[ptxboxone@gmail.com](mailto:ptxboxone@gmail.com)]

---

*Last updated: 2025-06-05*
