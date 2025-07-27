"""Simple test runner for the ULTIMAI package.

This runner discovers modules in ``tests/`` whose names start with
``test_`` and executes all functions beginning with ``test_``.  It
injects a temporary directory for functions expecting a single
argument (``tmp_path``) and reports summary statistics.  The runner
exits with status 1 if any test fails.
"""

from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path
import pkgutil
import traceback
from tempfile import TemporaryDirectory


def run() -> None:
    tests_dir = Path(__file__).parent
    # Ensure package import works from this directory
    project_root = tests_dir.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    failed = 0
    total = 0
    for module_info in pkgutil.iter_modules([str(tests_dir)]):
        if not module_info.name.startswith('test_'):
            continue
        module_name = module_info.name
        try:
            module = importlib.import_module(module_name)
        except Exception:
            print(f"Failed to import {module_name}\n{traceback.format_exc()}")
            failed += 1
            continue
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith('test_'):
                continue
            total += 1
            try:
                if func.__code__.co_argcount == 0:
                    func()
                elif func.__code__.co_argcount == 1:
                    with TemporaryDirectory() as tmpdir:
                        func(Path(tmpdir))
                else:
                    raise ValueError(f"Unsupported signature for {name}")
                print(f"PASS {module_name}:{name}")
            except Exception:
                failed += 1
                print(f"FAIL {module_name}:{name}\n{traceback.format_exc()}")
    print(f"Executed {total} tests, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    run()