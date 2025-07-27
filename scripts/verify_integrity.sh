#!/bin/bash
# Verify the integrity of the ULTIMAI reasoning infrastructure by running tests.

set -e
python tests/run_tests.py
echo "All tests passed."