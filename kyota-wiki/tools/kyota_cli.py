#!/usr/bin/env python3
"""Compatibility shim for the installable KYOTA CLI package."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"

if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from kyota.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
