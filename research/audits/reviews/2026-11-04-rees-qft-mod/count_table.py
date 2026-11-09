"""Gate counts of the generated circuits at the parameters of Corollary 8 (exact computation)."""
import json, math, sys, time
import sympy
from theorems.rees_qft_mod import params_for_eta, error_bound, qft_mod_ops, gate_counts, gate_bound
out = sys.argv[1]
rows = []
for b in (2, 4, 8, 16, 32, 64):
    N = sympy.prevprime(2**b) if b > 2 else 3
    for eta in (1e-3, 1e-6, 2.0**-40):
        t, r, tp = params_for_eta(N, eta)
        bd = error_bound(N, t, r, tp)
        t0 = time.time()
        ops, L, _ = qft_mod_ops(N, t, r, tp)
        c = gate_counts(ops)
        Lg = math.log2(1/eta)
        H, R = c.get('h', 0), c.get('r', 0)
        rows.append(dict(N=N, b=b, eta=eta, t=t, r=r, tp=tp, qubits=L.nq, total=c['total'], bound=gate_bound(b, t, r, tp),
                         toffoli=c.get('ccx', 0), h=H, r_single=R, cr=c.get('cr', 0), max_k=c['max_k'],
                         B=bd['B'], B_simple=bd['B_simple'], lead=420*b*b+187*b*Lg+4*Lg*Lg,
                         H_ok=H <= 4*t+3*b+6, R_ok=R <= (b+5)*tp+6, b_cubed=b**3))
        print(json.dumps(rows[-1]), round(time.time()-t0, 1), flush=True)
        json.dump(rows, open(out, 'w'), indent=1)
