#!/usr/bin/env bash
# Regenerate every report the paper cites into a fresh directory, then compare each
# number in numbers_map.json with the committed value.
#
#   docs/papers/classical-competitors/reproduce.sh [OUT]       # OUT defaults to a temp dir
#   PYTHON=/path/to/python docs/papers/classical-competitors/reproduce.sh
#
# Needs python-flint, sympy, numpy, scipy and cvxpy, and stops at once if any is missing
# (without cvxpy the circuit search would silently drop its PPT bounds). The qsearch-classical
# package lists only the first three; scipy and cvxpy are for the DCP circuit search. The
# modules run from the vendored source in packages/qsearch_classical/src, put on PYTHONPATH,
# so an installed copy of the package is not what this exercises. The two Jacobi modules are
# not run: no number in the paper comes from them. The prime-character Morse attack and the
# N = 32768 polar design take minutes each. The rediscovery-audit numbers are not
# regenerated here: they come from committed judgements, and `python tools/audit/rediscovery.py
# report` rebuilds them deterministically.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
OUT="${1:-$(mktemp -d)}"
PY="${PYTHON:-python3}"

"$PY" - <<'EOF'
import importlib.util
import sys

needed = {"flint": "python-flint", "sympy": "sympy", "numpy": "numpy", "scipy": "scipy", "cvxpy": "cvxpy"}
missing = [name for module, name in needed.items() if importlib.util.find_spec(module) is None]
if missing:
    sys.exit(f"reproduce.sh: missing {', '.join(missing)}; install with: pip install {' '.join(missing)}")
EOF

export PYTHONPATH="$REPO/packages/qsearch_classical/src"
export QSEARCH_CLASSICAL_ROOT="$OUT"
mkdir -p "$OUT/research/classical_baselines" "$OUT/research/audits"
echo "regenerating into $OUT"

# Order matters: finite_readout reads the OPI report from the same root.
for module in prime_character_opi prime_character_norm_attack prime_character_morse_attack \
              prime_character_exterior_bound prime_character_capacity_source prime_character_finite_readout \
              polar_conditional_sampler polar_source_design; do
  echo "== $module"
  "$PY" -m "qsearch_classical.$module" --write > /dev/null
done
echo "== polar_source_design N=32768"
"$PY" -m qsearch_classical.polar_source_design --write --length 32768 --grid 256 --power 3 > /dev/null

echo "== circuit search"
unset PYTHONPATH
"$PY" "$REPO/tools/circuit_search/dcp_readout.py" --out "$OUT/research/audits/circuit_search_dcp_readout.json" > /dev/null

echo "== compare"
"$PY" "$HERE/make_numbers.py" --compare "$OUT"
