
# Contributing to **McCrackn’s Prime Law**

*Thank you* for considering a contribution!  
McCrackn’s Prime Law is a **non‑profit, community‑maintained, volunteer‑run** research project exploring prime‑number theory and algorithmic entropy.

> **TL;DR**  
> 1. Fork → clone → create a topic branch.  
> 2. Install **Git LFS** (`git lfs install`) once.  
> 3. Run `pre-commit run --all-files` and `pytest`.  
> 4. Keep changes small & focused.  
> 5. Open a Pull Request—template will guide you.  
> 6. Be excellent to each other (see `CODE_OF_CONDUCT.md`).  

---

## Table of Contents
1. [Before You Start](#before-you-start)  
2. [Ways to Contribute](#ways-to-contribute)  
3. [Development Environment](#development-environment)  
4. [Branching & Commit Style](#branching--commit-style)  
5. [Running Tests](#running-tests)  
6. [Documentation](#documentation)  
7. [Handling Large Files](#handling-large-files)  
8. [Pull Request Checklist](#pull-request-checklist)  
9. [Review Process](#review-process)  
10. [Security Issues](#security-issues)  
11. [License & DCO](#license--dco)  

---

## Before You Start
- **Install Git LFS**  
  ```bash
  git lfs install   # one‑time per machine
  ```
  The repository contains a 685 MB pre‑computed CSV (`motifs_10m.csv`) stored via LFS.
- **Read the [`README.md`](./README.md)** to understand the project scope.  
- **Search existing Issues / Discussions** to avoid duplicates.  
- **Respect the Code of Conduct.** We have a zero‑tolerance policy toward harassment.  
- For **security vulnerabilities**, **do *NOT* open a public issue**—see [`SECURITY.md`](./SECURITY.md).

---

## Ways to Contribute
| Type | Examples |
|------|----------|
| **Code** | Bug fixes, new algorithms, performance tweaks, refactors |
| **Research** | Proofs, theoretical notes, white‑papers in `docs/notes` |
| **Documentation** | Tutorials, API references, clarifying comments |
| **Testing** | New unit/integration tests, benchmark datasets |
| **DevOps** | CI speed‑ups, Docker images, conda recipes |
| **Community** | Issue triage, discussion moderation, translation, outreach |

---

## Development Environment

```bash
# Fork in the browser → then:
git clone https://github.com/<your-user>/McCrackns-Prime-Law.git
cd McCrackns-Prime-Law

git lfs install                    # make sure LFS pointers download correctly

python -m venv .venv               # Python ≥ 3.9
source .venv/bin/activate          # Win: .venv\Scripts\activate

pip install -r requirements-dev.txt

pre-commit install                 # black, isort, ruff, etc.
```

---

## Branching & Commit Style
- Branch off **`master`** (default):  
  ```bash
  git checkout -b feature/<short-topic>
  ```
- Keep PRs **small & focused** (< ~400 lines diff when possible).  
- Write **imperative** commit messages:
  ```
  fix: handle overflow in prime multiplication

  Details: ...
  ```
- Code style enforced by **Black** + **ruff** + **isort**.  
- Public APIs live under `src/mplaw/`; internal helpers under `src/_mplaw/`.

---

## Running Tests

```bash
pytest -q
```

Add or update tests alongside your code—*coverage should not fall*.  
Heavy numeric experiments belong in `tests/slow/` and are skipped by default (`-m "not slow"`).

---

## Documentation

- Docstrings follow **Google style** and render with **Sphinx**.  
- Build docs locally:
  ```bash
  make -C docs html
  open docs/_build/html/index.html
  ```
- New mathematical derivations or design docs belong in `docs/notes/` (Markdown or LaTeX).

---

## Handling Large Files

* **Git LFS required** – patterns are defined in `.gitattributes`.  
* **Do not commit raw files >100 MB**; GitHub will reject them.  
* If you need to add a new large dataset:  
  ```bash
  git lfs track "*.csv"
  git add .gitattributes big_dataset.csv
  ```
* Free tier: 1 GB storage, 1 GB/month bandwidth. Compress/split when practical.

---

## Pull Request Checklist

- [ ] Tests pass (`pytest`, `pre-commit run --all-files`).  
- [ ] Docstrings / docs updated.  
- [ ] Changes listed in `CHANGELOG.md` under **Unreleased**.  
- [ ] Any new externals added to `requirements*.txt`.  
- [ ] PR description explains **why** and **what** with references / benchmarks.  
- [ ] Linked to an Issue (if one exists) with `Fixes #<num>`.

---

## Review Process

| Stage | Typical Time | What Happens |
|-------|--------------|--------------|
| Triage | ≤ 7 days | Maintainer checks scope, labels PR |
| Community review | variable | Peers comment, request changes |
| Merge | when approvals & tests green | Maintainer squashes/merges |
| Release | batched periodically | Your commits ship in next GitHub Release |

Patience is appreciated—everyone here is a volunteer. 🙂

---

## Security Issues
Please follow the **private disclosure** procedure in [`SECURITY.md`](./SECURITY.md).  
Public Issues for security flaws will be closed and redirected.

---

## License & DCO
McCrackn’s Prime Law is licensed under the **MIT License** (see `LICENSE`).  
By submitting code, you agree your contribution is licensed under the same terms and you certify (via Developer Certificate of Origin) that you have the right to contribute it.

---

*May your primes be large and your proofs elegant—happy hacking!*  
