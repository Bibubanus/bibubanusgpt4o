#!/usr/bin/env bash
set -euo pipefail

# 1) Тесты/сборка из корня (prod‑пакет)
PYTHONPATH=. python tests/run_tests.py
PYTHONPATH=. python scripts/generate_graph.py --input data/seeds.json --output build/graph/graph.json
PYTHONPATH=. python scripts/dump_report.py --graph build/graph/graph.json --output build/report/report.md

# 2) Готовим Pages
mkdir -p public/graph public/report
cp -f build/graph/graph.json public/graph/
[ -f build/graph/graph.png ] && cp -f build/graph/graph.png public/graph/
[ -f build/graph/graph.png.txt ] && cp -f build/graph/graph.png.txt public/graph/
cp -f build/report/report.md public/report/
[ -f public/index.md ] || printf "ULTIMAI Reasoning Artifacts\n\n- Graph: ./graph/\n- Report: ./report/report.md\n" > public/index.md

# 3) (опционально) вычистить старую копию
if [ -d ULTIMAI ]; then
  git rm -r ULTIMAI
fi

git add .
git commit -m "ULTIMAI: prod-ready apply; tests green; build & Pages artifacts prepared"
git push origin main
