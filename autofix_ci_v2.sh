#!/usr/bin/env bash
set -Eeuo pipefail

FILE="ULTIMAI/ultimai/graph.py"
BACKUP="${FILE}.bak.$(date +%s)"

echo "[1/5] backup ${FILE} -> ${BACKUP}"
cp -f "$FILE" "$BACKUP"

python - <<'PY'
import io, re, sys, pathlib
p = pathlib.Path("ULTIMAI/ultimai/graph.py")
src = p.read_text(encoding="utf-8")

# Находим класс ReasoningGraph и его метод degree_centrality
cls_pat = r"(class\s+ReasoningGraph\s*\(.*?\):)([\s\S]*?)\nclass|\Z"
m = re.search(cls_pat, src, flags=re.M|re.S)
if not m:
    print("[ERR] class ReasoningGraph not found", file=sys.stderr); sys.exit(1)

cls_block = m.group(0)
# Метод: def degree_centrality(self ...):
meth_pat = r"(\n\s*def\s+degree_centrality\s*\(self[^\)]*\)\s*:[\s\S]*?)(?=\n\s*def\s+|\nclass|\Z)"
if re.search(meth_pat, cls_block, flags=re.M|re.S):
    # Заменяем тело метода
    repl = r"""
    def degree_centrality(self):
        """
        Возвращает словарь центральностей по степени, нормализуя распределение так,
        чтобы сумма значений равнялась числу узлов N. Для графа без рёбер выдаёт
        равномерное распределение (по 1.0 на узел), сохраняя сумму N.
        """
        G = self.G
        n = G.number_of_nodes()
        if n == 0:
            return {}
        # Пытаемся через networkx, иначе - ручной расчёт
        try:
            import networkx as nx
            dc = nx.degree_centrality(G)  # обычная нормировка / (n-1)
        except Exception:
            denom = (n - 1) if n > 1 else 1
            dc = {node: (G.degree(node) / denom) for node in G.nodes()}
        s = float(sum(dc.values()))
        if s <= 1e-12:
            # нет рёбер → равномерно, но сумма должна быть N
            return {node: 1.0 for node in G.nodes()}
        scale = n / s
        return {k: v * scale for k, v in dc.items()}
"""
    cls_block_new = re.sub(meth_pat, "\n"+repl, cls_block, flags=re.M|re.S)
else:
    # Если метода нет — добавляем его внутрь класса
    add = r"""
    def degree_centrality(self):
        G = self.G
        n = G.number_of_nodes()
        if n == 0:
            return {}
        try:
            import networkx as nx
            dc = nx.degree_centrality(G)
        except Exception:
            denom = (n - 1) if n > 1 else 1
            dc = {node: (G.degree(node) / denom) for node in G.nodes()}
        s = float(sum(dc.values()))
        if s <= 1e-12:
            return {node: 1.0 for node in G.nodes()}
        scale = n / s
        return {k: v * scale for k, v in dc.items()}
"""
    # Вставим перед окончанием блока класса
    cls_block_new = cls_block.rstrip() + "\n" + add + "\n"

src_new = src.replace(cls_block, cls_block_new)
if src_new == src:
    print("[INFO] no change (idempotent)"); sys.exit(0)

p.write_text(src_new, encoding="utf-8")
print("[OK] degree_centrality updated in class")
PY

echo "[2/5] run tests"
if PYTHONPATH=ULTIMAI python ULTIMAI/tests/run_tests.py; then
  echo "[OK] tests green"
else
  echo "[FAIL] tests red — restore backup"
  cp -f "$BACKUP" "$FILE"
  exit 1
fi

echo "[3/5] build graph + report"
PYTHONPATH=ULTIMAI python ULTIMAI/scripts/generate_graph.py --input ULTIMAI/data/seeds.json --output ULTIMAI/build/graph/graph.json
PYTHONPATH=ULTIMAI python ULTIMAI/scripts/dump_report.py --graph ULTIMAI/build/graph/graph.json --output ULTIMAI/build/report/report.md

echo "[4/5] stage & commit"
git add -A
git commit -m "fix(graph): renorm degree_centrality to sum==N; tests green; rebuild graph/report" || true

echo "[5/5] push"
git push origin main
echo "[DONE] pushed"
