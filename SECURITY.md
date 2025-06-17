# SECURITY POLICY  
(for **McCrackn’s Prime Law** – a **non-profit, community-maintained, volunteer-run** research project)

McCrackn’s Prime Law is built and cared for by a small, all-volunteer community led by its original author, **Budd McCrackn**.  
There is **no commercial sponsorship** and contributors work in their spare time.  
Even so, every good-faith security report is taken seriously and coordinated fixes are released as volunteer availability permits.  
Thank you for practising *responsible disclosure* and helping keep the community safe.

---

## Which Code Gets Patches?

Because the project does **not** follow formal Semantic Versioning, releases stay intentionally simple and rely on the community to help test patches:

| Track | Where to find it | Patch policy |
|-------|------------------|--------------|
| **Stable** | latest GitHub **Release** (ZIP/TAR) | Receives fixes once the community has reviewed and tested them |
| **Development** | `main` branch (default) | Always contains the newest code; fixes appear here first |
| **Older tags / archives** | any commit or release more than 12 months old | *End-of-life* – please upgrade or cherry-pick a patch yourself |

If absolute reproducibility is critical for your research, pin to a specific commit hash or the latest Release tag.

---

## How to Report a Vulnerability

| Step | Details |
|------|---------|
| **1. Keep it private first** | Please **do not** open a public GitHub Issue or PR for security matters. |
| **2. Preferred channel** | Use the GitHub **Security Advisory** form: <https://github.com/pt2710/McCrackns-Prime-Law/security/advisories/new> |
| **3. If the form is unavailable** | Open a *very low-detail* issue titled “Request secure disclosure channel” and a maintainer will respond with an alternative private contact (for example a temporary e-mail alias or encrypted paste). |
| **4. Helpful information** | When possible, include reproduction steps, affected commit or release date, OS / Python details, and (optionally) a CVSS 3.1 vector. |

---

## Community Workflow & Target Timelines *(best effort)*

| Phase | Target time | What happens |
|-------|-------------|--------------|
| Acknowledge | ≤ 5 calendar days | A volunteer replies and assigns an internal tracking ID. |
| Triage | ≤ 14 days | Issue reproduced, impact estimated, fix strategy agreed. |
| Patch & testing | ≤ 45 days for critical; best-effort otherwise | Patch on a private branch, peer review by volunteers, minimal CI. |
| Public release | Coordinated | Patched **Release** plus signed advisory (GHSA/CVE). |
| Credit | At release | Name or pseudonym (opt-in). |

If limited volunteer availability delays these targets, you will receive a status update with a revised estimate.

---

## Severity Mapping (CVSS 3.1 → GitHub levels)

| CVSS Base | GitHub level | Typical impact |
|-----------|--------------|----------------|
| ≥ 9.0 | Critical | Remote code execution, privilege escalation, silent data corruption |
| 7.0 – 8.9 | High | DoS halting computations, sensitive data leak |
| 4.0 – 6.9 | Medium | Limited DoS, weak entropy, integrity bypass |
| < 4.0 | Low | Information disclosure, minor timing channels |

---

## Scope

| In scope | Out of scope |
|----------|--------------|
| Logic or math errors in **`src/`** that break correctness or safety | Vulnerabilities *in third-party dependencies* (report upstream) |
| Dependency confusion / malicious package takeover | Mis-configuration in downstream forks or private deployments |
| Leakage of workflow secrets, tampering with GitHub Releases | Example notebooks, documentation, unit-test helpers |

---

## Tips for Users

* **Pin explicitly:** clone the repo and check out a commit hash, or use the latest Release archive.  
* **Isolate heavy computations:** run prime searches inside Docker/LXC containers or unprivileged VMs.  
* **Verify signatures & hashes:** each Release is GPG-signed; checksums in `SHA256SUMS`.  
* **Stay informed:** click **Watch → Security alerts** on GitHub or subscribe to the Releases RSS feed.

---

## Gratitude

We salute every researcher or community member who follows coordinated disclosure.  
Valid reporters (with consent) will be listed here and receive a digital *Prime Law Hall of Fame* badge.

---

*Last updated: 2025-06-17*
