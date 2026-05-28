#!/usr/bin/env bash
set -euo pipefail

# Create a virtual environment in .venv and install dependencies
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [ -d ".venv" ]; then
  echo ".venv already exists — skipping venv creation. To recreate remove .venv first."
else
  python3 -m venv .venv
  echo "Created virtual environment at .venv"
fi

# Activate and install
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Environment ready. Activate with: source .venv/bin/activate"
