"""Exact stabilizers of single ISS-template factors, and of twisted products
(AI-written, pending human review).

For a factor psi (built in twist_check.state) and a twist parameter s, the factor
contributes to the product procedure g -> (psi . delta_s(g)) the stabilizer
  Stab_s = { g in G : psi . delta_s(g) is a scalar multiple of psi } = delta_s^{-1}(Stab(psi)).
By the tensor lemma the product procedure hides the intersection of the Stab_{s_i}
over the copies with s_i != 0.  We compute Stab(psi) by testing every g in G, then the
intersections for two distinct twist values, and report the order and whether it
contains H.
"""
import json
import numpy as np
from twist_check import Grp, state, right_mult_ratio, layer_positions

def stab(G, S, E):
    return np.array([g for g in range(G.n) if right_mult_ratio(G, S, E, g)[0] is not None])

def dil_inv_set(G, St, s):
    sinv = pow(s, -1, G.p)
    return set(int(G.enc(G.dil(G.coords[g], sinv))) for g in St)   # delta_s^{-1}(St)

def one(name, p, eta, u_gamma2, lam_top, s_pair, rng):
    G = Grp(name, p); cls = int(G.grades.max())
    eta = np.array(eta); a = int(rng.integers(G.n))
    Hset = set(int(G.enc(t * eta)) for t in range(p))
    out = {"alg": name, "p": p, "eta": eta.tolist()}
    for tag, Npos, lab in (("A_gamma2", layer_positions(G, 2), u_gamma2),
                           ("B_top", layer_positions(G, cls), lam_top)):
        S, E = state(G, a, eta, Npos, np.array(lab))
        St = stab(G, S, E)
        Sts = [dil_inv_set(G, St, s) for s in s_pair]
        inter = Sts[0] & Sts[1]
        out[tag] = {"label": lab, "stab_order": int(len(St)),
                    "stab_contains_H": Hset <= set(map(int, St)),
                    "twisted_stab_orders": [len(x) for x in Sts],
                    "s_pair": list(s_pair),
                    "intersection_order": len(inter),
                    "intersection_contains_H_or_a_dilate": any(
                        set(int(G.enc(G.dil(t * eta, pow(s, -1, p)))) for t in range(p)) <= inter
                        for s in range(1, p))}
    return out

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    runs = [
        ("filiform4", 5, [1, 0, 1, 0], [0, 1], [1], (2, 3)),   # h = exp(x1 + x3)
        ("filiform4", 5, [1, 0, 1, 0], [1, 0], [1], (2, 3)),   # u3 = 0: route A eigen
        ("filiform4", 5, [1, 0, 0, 1], [0, 1], [1], (2, 3)),   # v2 = 0: route B fine
        ("free23", 5, [1, 0, 1, 0, 0], [0, 1, 0], [1, 0], (2, 3)),  # h = exp(x + z)
        ("free23", 5, [1, 2, 3, 4, 1], [1, 2, 3], [2, 3], (2, 4)),
    ]
    for r in runs:
        print(json.dumps(one(*r, rng)), flush=True)
