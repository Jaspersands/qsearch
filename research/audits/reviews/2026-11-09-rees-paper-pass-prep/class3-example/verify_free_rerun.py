"""Re-run of the two checks of verify_free.py whose EXPECTATIONS were wrong in the first run
(the mathematics was fine; the expected values in the script were miscomputed by hand):
  F1e: Z(A) is span(tu, tw, t2u, t2w, t3u, t3w) (t2u, t2w are central too), not span(tu,tw,t3u,t3w);
  F5h: psi_theta(x) also has a w-term (theta^2 - theta^3) w.
verify_free.py has been corrected; this script runs just these two checks with the corrected code.
"""
import numpy as np
import verify_free as vf

vf.f1(5)
p = 5
phi = np.array([[1, 0, 1, 1, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, p-1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype=np.int64)
TL = vf.L_tensor(p)


def is_aut(Mx):
    for i in range(vf.M):
        for j in range(i+1, vf.M):
            k = vf.L_BR.get((i, j))
            rhs = Mx[k[0]] if k else np.zeros(vf.M, dtype=np.int64)
            if not np.array_equal(vf.br(TL, Mx[i], Mx[j], p), rhs % p):
                return False
    return round(np.linalg.det(Mx.astype(float))) % p != 0


phinv = np.round(np.linalg.inv(phi.astype(float))).astype(np.int64) % p
good = is_aut(phi)
for th in range(1, p):
    D = np.diag([th, th, th**2 % p, th**3 % p, th**3 % p])
    Cm = (phinv @ D @ phi) % p
    formula = np.array([[th, 0, (th-th**2) % p, (th-th**3) % p, (th**2-th**3) % p], [0, th, 0, 0, 0],
                        [0, 0, th**2 % p, 0, (th**3-th**2) % p], [0, 0, 0, th**3 % p, 0],
                        [0, 0, 0, 0, th**3 % p]], dtype=np.int64)
    r = (np.array(vf.V_MAIN) @ Cm) % p
    good &= np.array_equal(Cm, formula) and is_aut(Cm) and vf.rank([vf.V_MAIN, r], p) == 1 \
        and np.array_equal(Cm[3:, 3:], (th**3 % p) * np.eye(2, dtype=np.int64))
vf.check("F5h", good, f"p={p}: psi_theta = phi delta_theta phi^-1: x -> theta x + (theta-theta^2) z + (theta-theta^3) u "
                      f"+ (theta^2-theta^3) w, y -> theta y, z -> theta^2 z + (theta^3-theta^2) w, u -> theta^3 u, "
                      f"w -> theta^3 w; an automorphism preserving h, central scalar theta^3, every theta")
print("FAILURES:", vf.FAILS if vf.FAILS else "none")
