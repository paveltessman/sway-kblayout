#!/bin/bash
set -euxo pipefail

VERSION=$(cat version)

python3 -m venv .venv
pip install -r requirements-dev.txt

pyinstaller --name="sway-kbswitcher-${VERSION}" --onefile run.py
