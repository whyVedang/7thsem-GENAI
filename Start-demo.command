#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
    echo "Missing .venv/bin/python. Create a Python 3.11 virtual environment first (see DEMO-NOTES.md)." >&2
    exit 1
fi

exec .venv/bin/python -m streamlit run app.py "$@"
