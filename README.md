
# McCrackn’s Prime Law
[![CI](https://github.com/pt2710/McCrackns-Prime-Law/actions/workflows/ci.yml/badge.svg)](https://github.com/pt2710/McCrackns-Prime-Law/actions/workflows/ci.yml)

_Repository slug:_ `mccrackns_prime_law`  
**Status:** non‑profit · community‑maintained · volunteer‑run

---

## Abstract
**McCrackn’s Prime Law** is a deterministic, recursive rule that derives every prime directly from its predecessor—no sieves, randomness, or empirical tables required.  
The method is accompanied by mathematical proofs and validation up to \(n = 10^{7}\).

*Read the full manuscript:* [`McCrackns_prime_law.pdf`](./McCrackns_prime_law.pdf)

---

## Table of Contents
- [Abstract](#abstract)
- [Quick Start](#quick-start)
- [Programmatic Usage](#programmatic-usage)
- [Repository Layout](#repository-layout)
- [Reproducibility & Open Science](#reproducibility--open-science)
- [Community & Governance](#community--governance)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)
- [Authors & Credits](#authors--credits)

---

## Quick Start

> **Note:** The large pre‑computed dataset `motifs_10m.csv` is stored with **Git LFS**.  
> Install LFS once via `git lfs install` *before* cloning or pulling.

```bash
# 1 · Clone & enter
git clone https://github.com/pt2710/McCrackns-Prime-Law.git
cd McCrackns-Prime-Law

# 2 · Ensure Git LFS is enabled (one‑time per machine)
git lfs install

# 3 · Create isolated Python env (3.9+)
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate.bat   # Windows (PowerShell users: Activate.ps1)

# 4 · Install runtime deps
pip install -r requirements.txt

# 5 · Verify the theorem for the first 10⁵ primes
python test_mccrackns_prime_law.py
```

The script prints prime indices, local regimes, motifs and gap statistics.  
Add `--plot` to create histograms of prime gaps and motif frequencies.

---

## Programmatic Usage

```python
from mccrackns_prime_law import McCracknsPrimeLaw

mpl = McCracknsPrimeLaw(n_primes=20)
mpl.generate()
print(mpl.get_primes())
```

---

## Repository Layout

```
mccrackns_prime_law/
├── .github/
│   └── workflows/ci.yml         # Continuous‑integration pipeline
├── .gitattributes               # Git LFS tracking rules
├── configs/
│   └── default.yaml             # Tunable parameters
├── figures/                     # Paper‑ready plots (static)
├── figures_visible/             # Interactive PNGs & CSVs (large files in LFS)
├── src/                         # Library code (importable)
│   ├── __init__.py
│   ├── prime_utils.py
│   └── your_module.py
├── tests/                       # Unit / regression tests
│   └── test_basic.py
├── McCrackns_prime_law.pdf      # Formal manuscript
├── mccrackns_prime_law.py       # Single‑file reference implementation
├── next_prime.py                # CLI helper
├── numbers_domains.py           # Support module
├── precompute_motifs.py         # Data‑generation script
├── LICENSE                      # MIT License
├── README.md                    # You are here
├── CONTRIBUTING.md              # How to propose changes
├── SECURITY.md                  # Responsible‑disclosure policy
├── requirements.txt             # Runtime dependencies
└── motifs_10m.csv               # Pre‑computed data set (LFS pointer)
```

---

## Reproducibility & Open Science
All code, data and figures are provided under an OSI‑approved license to foster independent verification.  
Run the notebooks, re‑plot the data, or extend the proofs—then open a Pull Request or Discussion to share your findings!

---

## Community & Governance
McCrackn’s Prime Law is **community‑maintained**. There is currently **no corporate backing and no single full‑time maintainer**.  
We rely on volunteers for everything from issue triage to peer‑review of new proofs. If you’d like to help, see **[`CONTRIBUTING.md`](./CONTRIBUTING.md)**.

---

## Contributing
Bug reports, feature requests and PRs of any size are welcome.  
Please read the guidelines in [`CONTRIBUTING.md`](./CONTRIBUTING.md) before you start hacking.

---

## Security
If you believe you have found a vulnerability, **do not open a public Issue**.  
Instead, follow the private process in [`SECURITY.md`](./SECURITY.md).

---

## License
This project is released under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

## Authors & Credits
Created by **Budd McCrackn** and extended by a growing community of mathematicians, coders and prime‑enthusiasts.  
See `AUTHORS.md` (or the GitHub contributions graph) for a full list of contributors.

---

_Last updated: 2025‑06‑17_
