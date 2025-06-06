# McCrackn’s Prime Law
[![CI](https://github.com/pt2710/McCrackns-Prime-Law/actions/workflows/ci.yml/badge.svg)](https://github.com/pt2710/McCrackns-Prime-Law/actions/workflows/ci.yml)

_Repository slug:_ `mccrackns_prime_law`

---

## Abstract

This project demonstrates **McCrackn’s Prime Law** – a deterministic and recursive rule that generates each prime directly from its predecessor. The approach removes the need for search, randomization or empirical tables and is accompanied by proofs and validation up to $n=10^7$.

**Full manuscript:** [deterministic_equation_of_primes.pdf](https://github.com/pt2710/McCrackns-Prime-Law/blob/main/deterministic_equation_of_primes.pdf)

---

## Quick start

1. Clone the repository and create an isolated environment:

```bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

2. Run the main verification script:

```bash
python test_mccrackns_prime_law.py
```

The script validates the first few primes, reports regime innovation points and can optionally generate histograms of prime gaps and motif statistics.

Example output for the first 20 primes:

```
Prime #1: 2
Prime #2: 3
Prime #3: 5
Prime #4: 7
Prime #5: 11
Prime #6: 13
Prime #7: 17
Prime #8: 19
Prime #9: 23
Prime #10: 29
Prime #11: 31
Prime #12: 37
Prime #13: 41
Prime #14: 43
Prime #15: 47
Prime #16: 53
Prime #17: 59
Prime #18: 61
Prime #19: 67
Prime #20: 71
```

---

## Generating primes programmatically

```python
from mccrackns_prime_law import McCracknsPrimeLaw

m = McCracknsPrimeLaw(n_primes=20)
m.generate()
print(m.get_primes())
```

Output:

```
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
```

Gap sequences may be supplied through CSV files stored in the `gaps/` directory. When present they are loaded to accelerate generation.

---

## Benchmarks

Running `bench_stream.py` compares the streaming prime generator with a
traditional sieve implementation:

```bash
$ python bench_stream.py

=== n = 10,000 ===
First 20: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
Last  20: [104549, 104551, 104561, 104579, 104593, 104597, 104623, 104639, 104651, 104659, 104677, 104681, 104683, 104693, 104701, 104707, 104711, 104717, 104723, 104729]
mpl_stream 0.093s   sieve 0.007s   speed-up   0.1×

=== n = 100,000 ===
First 20: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
Last  20: [1299379, 1299437, 1299439, 1299449, 1299451, 1299457, 1299491, 1299499, 1299533, 1299541, 1299553, 1299583, 1299601, 1299631, 1299637, 1299647, 1299653, 1299673, 1299689, 1299709]
mpl_stream 3.32s   sieve 0.081s   speed-up   0.0×
```

These results were produced on the Codex test environment. In this configuration
the naive sieve remains faster than the simple streaming approach.

---

## Repository layout

```
mccrackns_prime_law/
├── LICENSE                  # MIT license text
├── README.md                # Project overview (this file)
├── requirements.txt         # Python dependencies
├── mccrackns_prime_law.py   # Core deterministic generator
├── numbers_domains.py       # Gap domain classification helpers
├── test_mccrackns_prime_law.py
├── src/                     # Auxiliary modules
│   └── your_module.py
├── configs/                 # Example configuration files
│   └── default.yaml
├── tests/                   # pytest based unit tests
│   └── test_basic.py
├── .github/workflows/ci.yml # Continuous integration setup
└── figures/ and gaps/       # Generated data and plots (optional)
```

---

## Reproducibility and open science

> This repository is provided for transparent examination by the mathematical community. All serious feedback is welcome.

The code, data sets and produced figures are open to facilitate independent replication. We encourage running the scripts and verifying the results locally. If you create new figures or discover interesting patterns, feel free to share them.

---

## Contributing

Issues and pull requests are encouraged. Please open a discussion first if you plan a larger change. For questions relating to the mathematics itself or potential collaborations, contact the author.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Budd McCrackn** – [ptxboxone@gmail.com](mailto:ptxboxone@gmail.com)

_Last updated: 2025-06-05_
