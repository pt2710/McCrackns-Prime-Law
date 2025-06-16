# McCrackn’s Prime Law
[![CI](https://github.com/pt2710/McCrackns-Prime-Law/actions/workflows/ci.yml/badge.svg)](https://github.com/pt2710/McCrackns-Prime-Law/actions/workflows/ci.yml)

_Repository slug:_ `mccrackns_prime_law`

---

## Abstract

This project demonstrates **McCrackn’s Prime Law** – a deterministic and recursive rule that generates each prime directly from its predecessor. The approach removes the need for search, randomization or empirical tables and is accompanied by proofs and validation up to $n=10^7$.

**Full manuscript:** [McCrackns_prime_law.pdf](https://github.com/pt2710/McCrackns-Prime-Law/blob/main/McCrackns_prime_law.pdf)

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
index,prime,gap,motif,run,domain
2,3,1,U1,1,U1
3,5,2,E1.0,1,E1
4,7,2,E1.0,2,E1
5,11,4,E1.1,1,E1
6,13,2,E1.0,3,E1
7,17,4,E1.1,2,E1
8,19,2,E1.0,4,E1
9,23,4,E1.1,3,E1
10,29,6,E2.0,1,E2
11,31,2,E1.0,5,E1
12,37,6,E2.0,2,E2
13,41,4,E1.1,4,E1
14,43,2,E1.0,6,E1
15,47,4,E1.1,5,E1
16,53,6,E2.0,3,E2
17,59,6,E2.0,4,E2
18,61,2,E1.0,7,E1
19,67,6,E2.0,5,E2
20,71,4,E1.1,6,E1
21,73,2,E1.0,8,E1
```

---

## Generating primes programmatically

```python
from mccrackns_prime_law import McCracknsPrimeLaw

m = McCracknsPrimeLaw(n_primes=20)
m.generate()
print(m.get_primes())
```

---

## Repository layout

```
mccrackns_prime_law/
├── LICENSE                  
├── README.md                
├── requirements.txt         
├── mccrackns_prime_law.py   
├── precompute_motifs.py 
├── next_prime.py 
├── numbers_domains.py       
├── test_mccrackns_prime_law.py
├── src/                     
│   └── your_module.py
├── configs/                 
│   └── default.yaml
├── tests/                  
│   └── test_basic.py
├── .github/workflows/ci.yml 
└── figures_visible/
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
