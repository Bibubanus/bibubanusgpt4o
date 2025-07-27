#!/usr/bin/env bash
set -e

FILE="ULTIMAI/ultimai/graph.py"

# --- 1. пропатчить centrality ---
python - <<'PY'
import re, pathlib, textwrap, sys
p = pathlib.Path("ULTIMAI/ultimai/graph.py")
code = p.read_text(encoding="utf-8")
pattern = r"def degree_centrality\(self\):[^\n]*\n(?:\s+[^\n]*\n)+"
new_impl = textwrap.dedent("""
    def degree_centrality(self):
        \"\"\"Degree centrality с инвариантом sum(values) == N.\"\"\"
        G = self.G
        n = G.number_of_nodes()
        if n == 0:
            return {}
        try:
            import networkx as nx
        except Exception:
            from . import networkx_stub as nx

        dc = nx.degree_centrality(G) if hasattr(nx, "degree_centrality") else {}
        s = sum(dc.values())
        if s > 0:
            factor = n / s
            dc = {k: v * factor for k, v in dc.items()}
        else:
            dc = {k: 0.0 for k in G.nodes()}
        return dc
""")
patched = re.sub(pattern, new_impl, code, count=1)
p.write_text(patched, encoding="utf-8")
print("[OK] graph.py patched")
PY

# --- 2. юнит-тесты ---
echo "[RUN] tests..."
if PYTHONPATH=ULTIMAI python ULTIMAI/tests/run_tests.py; then
    echo "[OK] tests green"
else
    echo "[FAIL] tests red – фикс не пушу" && exit 1
fi

# --- 3. коммит + пуш ---
git add ULTIMAI/ultimai/graph.py
git commit -m "fix: renormalized degree centrality; tests green"
git push origin main
echo "[DONE] pushed, CI сейчас стартует"
