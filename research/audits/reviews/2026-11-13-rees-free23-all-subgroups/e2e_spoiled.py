"""Route A end to end with UNCONDITIONED labels, plus explicit checks of Lemma S and Lemma C' (spoiled copies).
AI-written 2026-11-13, pending human review.  Finite check only (falsification).

This runs the second referee's exact simulation `e2e.py` (read-only import; true coset states, true labels, true
automorphism permutations, exact sampling of every outcome) with two additions, patched into Run.go:
  * Lemma S: in every run whose used supports contain a spoiled copy (lam'.e' = 0), the state before the final QFT
    is supported on exactly one line w* + F_p e', with amplitude ratio Psi(w* + tau e')/Psi(w*) = omega^(mu tau),
    mu = the public form of Lemma E at the true theta.  Counters: spoiled_runs_checked, line_fail, phase_fail.
    Unspoiled runs must have full support (full_support_fail).
  * Lemma C': for each level-2 state, whether D_l = 0, split by whether the state's support contains a spoiled copy
    (D0_spoiled / n_spoiled_states) or not (D0_clean / n_clean_states), and states whose every support triple is
    spoiled (n_allspoiled_states, D0_allspoiled).
Usage: python e2e_spoiled.py p n_attempts seed
"""
import sys, os, inspect, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-13-rees-free23-theorem-referee'))
import e2e
import numpy as np

src = textwrap.dedent(inspect.getsource(e2e.Run.go))
m1 = "        lines = set()\n"
m2 = "        Z = np.indices((p, p)).reshape(2, -1).T\n"
assert src.count(m1.strip()) == 1 and src.count(m2.strip()) == 1
ins1 = """        for st in states:
            fl = [any((int(fe.lam[0]) * int(etap[0]) + int(fe.lam[1]) * int(etap[1])) % p == 0 for fe in t['fes']) for t in st['T']]
            key = 'clean' if not any(fl) else 'spoiled'
            s.st['n_%s_states' % key] = s.st.get('n_%s_states' % key, 0) + 1
            s.st['D0_%s' % key] = s.st.get('D0_%s' % key, 0) + int(st['D'] % p == 0)
            if all(fl):
                s.st['n_allspoiled_states'] = s.st.get('n_allspoiled_states', 0) + 1
                s.st['D0_allspoiled'] = s.st.get('D0_allspoiled', 0) + int(st['D'] % p == 0)
"""
ins2 = """        e2v = np.array([int(etap[0]), int(etap[1])]) % p
        sup = np.argwhere(np.abs(Psi) > 1e-9)
        spoiled_used = any((int(lam[0]) * int(etap[0]) + int(lam[1]) * int(etap[1])) % p == 0 for l in act for lam in states[l]['supp_labs'])
        if spoiled_used:
            w0 = sup[0]
            dd = ((sup[:, 0] - w0[0]) * e2v[1] - (sup[:, 1] - w0[1]) * e2v[0]) % p
            line_ok = (not dd.any()) and len(sup) == p
            ph_ok = True
            for tau in range(p):
                w = (w0 + tau * e2v) % p
                ratio = Psi[w[0], w[1]] / Psi[w0[0], w0[1]]
                ph_ok &= bool(abs(ratio - F.om ** ((int(mu_true) * tau) % p)) < 1e-8)
            s.st['spoiled_runs_checked'] = s.st.get('spoiled_runs_checked', 0) + 1
            s.st['line_fail'] = s.st.get('line_fail', 0) + int(not line_ok)
            s.st['phase_fail'] = s.st.get('phase_fail', 0) + int(not ph_ok)
        else:
            s.st['full_support_fail'] = s.st.get('full_support_fail', 0) + int(len(sup) != p * p)
"""
m1, m2 = m1[4:], m2[4:]                       # dedent markers and inserts to the dedented method body
ins1 = ''.join(l[4:] + '\n' for l in ins1.splitlines()); ins2 = ''.join(l[4:] + '\n' for l in ins2.splitlines())
assert src.count(m1) == 1 and src.count(m2) == 1
src = src.replace(m1, ins1 + m1).replace(m2, ins2 + m2)
ns = dict(vars(e2e))
exec(src, ns)
e2e.Run.go = ns['go']

if __name__ == '__main__':
    e2e.main()
