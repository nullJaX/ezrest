#!/usr/bin/env bash
set -e
# CLEAR ENV
git checkout master
git pull
rm -rf .pytest_cache .ruff_cache .venv build dist *.egg-info
# INIT ENV
python3 -m virtualenv .venv
source .venv/bin/activate
# INSTALL BUILD & TEST DEPS
pip install -e .[dev]
# CHECK TAG
VERSION=$(python -c "from ezrest import __version__;print(__version__)")
echo "Detected current version:" $VERSION
for tag in $(git tag); do
  if [[ "$VERSION" == "$tag" ]]; then
    echo "ERROR: Version $VERSION is already present in the repo."
    exit 1
  fi
done
# LINT
ruff format --check
ruff check
# TEST
pytest
# BUILD
python -m build
# UPLOAD
python -m twine upload dist/*
# TAG
git tag $VERSION
git push origin $VERSION