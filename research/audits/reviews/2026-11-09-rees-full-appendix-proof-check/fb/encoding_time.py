"""fb check 8: cost of the generator's Encoding(p) (theorems/rees_circuit_general.Encoding), which
every backend Config builds; tests the scope sentence of appendix-backends.tex:45 ("its classical
generator ... is not shown to run in time polynomial in log p").  Run from the repo root, read-only."""
import sys, time
sys.path.insert(0, '.')
import theorems.rees_circuit_general as G
prev = None
for p in [31, 61, 127, 251]:
    t0 = time.process_time(); G.Encoding(p); t = time.process_time() - t0
    ratio = "" if prev is None else f"  ratio to previous {t/prev[1]:.1f} (p ratio {p/prev[0]:.2f}, cubed {(p/prev[0])**3:.1f})"
    print(f"p={p}: Encoding {t:.2f} s CPU{ratio}", flush=True)
    prev = (p, t)
