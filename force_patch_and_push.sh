#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import pathlib
p = pathlib.Path("ULTIMAI/ultimai/graph.py")
src = p.read_text(encoding="utf-8")

tag = "# --- AUTO-PATCH: PATCH_ULIMAI_DC_V1 ---"
if tag not in src:
    patch = f"""

{tag}
def __ULTIMAI_patch_dc():
    def _dc(self):
        G = self.G
        n = G.number_of_nodes()
        if n == 0:
            return {}
        try:
            import networkx as nx
        except Exception:
            from . import networkx_stub as nx
        # базовая оценка + устойчивость к отсутствию networkx
        if hasattr(nx, 'degree_centrality'):
            try:
                dc = nx.degree_centrality(G)
            except Exception:
                dc = { { 'node': '(stub)' } }  # placeholder for f-string braces
                dc = {node: (G.degree(node)/(n-1) if n>1 else 0.0) for node in G.nodes()}
        else:
            dc = {node: (G.degree(node)/(n-1) if n>1 else 0.0) for node in G.nodes()}
        # ренормировка до суммы N
        s = sum(dc.values())
        if s <= 1e-12:
            return {node: 1.0 for node in G.nodes()}  # пустые рёбра → единичная масса
        factor = n / s
        return {k: v*factor for k,v in dc.items()}
    # привязать новый метод к классу после его объявления
    try:
        ReasoningGraph
    except NameError:
        return
    ReasoningGraph.degree_centrality = _dc

__ULTIMAI_patch_dc()
# --- END AUTO-PATCH ---
"""
    # почистим placeholder из-за вложенных фигурных скобок выше
    patch = patch.replace("{ { 'node': '(stub)' } }", "")
    p.write_text(src + patch, encoding="utf-8")
    print("[OK] appended post-class patch")
else:
    print("[SKIP] patch already present")
PY

echo "[RUN] tests..."
if PYTHONPATH=ULTIMAI python ULTIMAI/tests/run_tests.py; then
  echo "[OK] tests green"
  git add ULTIMAI/ultimai/graph.py
  git commit -m "fix(graph): override degree_centrality post-class; enforce sum==N invariant incl. edge-free graphs"
  git push origin main
  echo "[DONE] pushed — CI/Pages стартуют"
else
  echo "[FAIL] tests red — вывожу быстрый дебаг:"
  python - <<'PY'
from ultimai.graph import ReasoningGraph
rg = ReasoningGraph()
rg.add_node("a"); rg.add_node("b"); rg.add_node("c")
rg.add_edge("a","b"); rg.add_edge("b","c")
dc = rg.degree_centrality()
print("dc:", dc)
print("sum(dc)=", sum(dc.values()), "N=", len(dc))
PY
  exit 1
fi
