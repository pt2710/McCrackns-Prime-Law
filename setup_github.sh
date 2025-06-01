#!/usr/bin/env bash
set -euo pipefail

# Usage: ./prepare_github.sh [repo-slug] [public|private]
# Example: ./prepare_github.sh mccrackns_prime_law public

# 1. Parse arguments
REPO_SLUG=${1:-mccrackns_prime_law}
VISIBILITY=${2:-public}

# 2. Full human-readable title for README
FULL_TITLE="McCrackn's Prime Law"

echo "🔧 Scaffolding project for GitHub as '$REPO_SLUG' ($VISIBILITY)…"

# 3. Create necessary directories (figures for publication assets)
mkdir -p src configs tests figures .github/workflows gaps

# 4. Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
.env
venv/
*.log
.DS_Store
Thumbs.db
.vscode/
.idea/
figures/
gaps/
EOF

# 5. Create requirements.txt (if not present)
if [ ! -f requirements.txt ]; then
    pip freeze > requirements.txt
fi

# 6. Create README.md
cat > README.md << EOF
# $FULL_TITLE

_Repository slug:_ \`$REPO_SLUG\`

---

## Abstract

This project implements **McCrackn's Prime Law**—an explicit, recursive, and deterministic equation for the generation of the prime sequence. The framework is both mathematically rigorous and publication-ready, including motif innovation statistics and prime gap histograms for research dissemination.

---

## Installation

\`\`\`bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\\Scripts\\activate     # Windows
pip install -r requirements.txt
\`\`\`

---

## Usage

To run all scientific tests and generate publication-grade figures (histograms/statistics):

\`\`\`bash
python test_mccrackn_conjector.py
\`\`\`

All output (CSV data, PNGs) will be saved in \`figures/\`.

---

## Project Structure

$REPO_SLUG/
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

EOF

# 7. Create LICENSE (MIT)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Budd McCrackn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
EOF

# 8. Create src/your_module.py
cat > src/your_module.py << 'EOF'
def core_function(x):
    """
    Placeholder for core logic.
    """
    return 42
EOF

# 9. Create configs/default.yaml
cat > configs/default.yaml << 'EOF'
param1: 0.1
param2: 100
EOF

# 10. Create tests/test_basic.py
cat > tests/test_basic.py << 'EOF'
import pytest
from src.your_module import core_function

def test_core_function_returns_expected():
    assert core_function(0) == 42
EOF

# 11. Create GitHub Actions CI workflow
cat > .github/workflows/ci.yml << 'EOF'
name: Continuous Integration

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --maxfail=1 --disable-warnings -q
EOF

# 12. Initialize Git and make the first commit
if [ ! -d .git ]; then
  git init
fi
git add .
git commit -m "chore: initial scaffold for McCrackn's Prime Law – code, analysis, figures, CI"

# 13. Create GitHub repo & push (if gh CLI is available)
if command -v gh &> /dev/null; then
  echo "🔗 Creating GitHub repository '$REPO_SLUG' ($VISIBILITY)…"
  gh repo create "$REPO_SLUG" --"$VISIBILITY" --source=. --remote=origin --push
else
  echo "⚠️  GitHub CLI not found. Please manually create a repo named '$REPO_SLUG', then:"
  echo "    git remote add origin git@github.com:YOUR_USERNAME/$REPO_SLUG.git"
  echo "    git branch -M main"
  echo "    git push -u origin main"
fi

echo "✅ Project is now GitHub-ready for deterministic prime law research and publication graphics!"
