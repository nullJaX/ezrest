#!/usr/bin/env bash
set -e
# CLEAR ENV
git checkout master
git pull

PYTHONS=("12" "11" "10" "9" "8")
for version in ${PYTHONS[@]}; do
  # INIT ENV
  rm -rf .pytest_cache .ruff_cache .venv build dist *.egg-info
  pyenv local 3.$version
  pyenv version
  pyenv exec python -m venv .venv
  source .venv/bin/activate
  python -V
  pip -V
  read -p "Press any key to resume ..."
  # INSTALL BUILD & TEST DEPS
  pip install -e .[dev]
  # LINT
  ruff format --check
  ruff check
  # TEST
  pytest
  # BUILD
  python -m build
done