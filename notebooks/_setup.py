"""Path bootstrap for the lightweight notebooks.

Resolves `scripts/lakehouse.py` from the repo root regardless of where
Jupyter / Python was launched from. Used by all NB*/lite notebooks:

    import _setup  # noqa: F401  -- adds scripts/ to sys.path
    from lakehouse import path, reset

Why: the prior pattern `sys.path.insert(0, "../scripts")` is *cwd-relative*
and silently breaks if the notebook is run from the repo root or a CI
runner. Prefer `__file__` for a `.py` module, with a notebook-safe cwd
fallback when Jupyter does not define `__file__`.
"""
from __future__ import annotations

import sys
from pathlib import Path

_DOCKER = Path("/workspace/scripts")

try:
    _HERE = Path(__file__).resolve().parent
except NameError:
    # Jupyter executes cells without defining __file__.
    _HERE = Path.cwd()

_LOCAL = next(
    (
        candidate / "scripts"
        for candidate in (_HERE, *_HERE.parents)
        if (candidate / "scripts" / "lakehouse.py").exists()
    ),
    _HERE.parent / "scripts",
)

_TARGET = _DOCKER if _DOCKER.exists() else _LOCAL
sys.path.insert(0, str(_TARGET))
