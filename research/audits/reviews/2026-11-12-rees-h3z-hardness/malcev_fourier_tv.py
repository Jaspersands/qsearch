"""Single-copy abelian Fourier sampling in Mal'cev coordinates for H = <h>.

Run: nice -n 19 /opt/anaconda3/bin/python malcev_fourier_tv.py
Finite check only (TRAPS 7).

Box: g = x^a y^b z^t with 0 <= a, b < R, 0 <= t < T (coordinates (a, b, t)).
Standard Fourier sampling: query f on the uniform box state, measure f,
QFT over Z_R x Z_R x Z_T, measure xi.  Its law is
    p(xi) = |Box|^{-2} sum_d K(d) e(xi . d),
K(d) = #{(g, g') in Box^2 : same left H-coset, coord(g') - coord(g) = d mod (R,R,T)}.
For H = 1, p is uniform.  We print TV(p_H, uniform), and the same quantity for
the abelian control: Z^3 with hidden lattice <(v1, v2, c)> on the same box.
"""
import numpy as np

def mul(g, h):
    return (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])

def law(R, T, step_fn):
    """step_fn(a, b, t, j) -> (a', b', t') for the j-th coset neighbour."""
    a, b, t = np.meshgrid(np.arange(R), np.arange(R), np.arange(T), indexing="ij")
    a = a.ravel(); b = b.ravel(); t = t.ravel()
    K = np.zeros((R, R, T))
    K[0, 0, 0] = a.size
    for j in list(range(1, 4 * R)) + [-j for j in range(1, 4 * R)]:
        a2, b2, t2 = step_fn(a, b, t, j)
        ok = (a2 >= 0) & (a2 < R) & (b2 >= 0) & (b2 < R) & (t2 >= 0) & (t2 < T)
        if not ok.any():
            continue
        np.add.at(K, ((a2[ok] - a[ok]) % R, (b2[ok] - b[ok]) % R, (t2[ok] - t[ok]) % T), 1)
    N = R * R * T
    p = np.real(np.fft.fftn(K)) / N ** 2
    return p, N

def tv_uniform(p, N):
    return 0.5 * np.abs(p - 1.0 / N).sum()

def heis_step(h):
    v1, v2, c = h
    def f(a, b, t, j):
        # g = x^a y^b z^t = (a, b, ab + t); g h^j in matrix coords
        hj = (j * v1, j * v2, j * c + (j * (j - 1) // 2) * v1 * v2)
        A = a + hj[0]; B = b + hj[1]; C = (a * b + t) + hj[2] + a * hj[1]
        return A, B, C - A * B
    return f

def abel_step(h):
    v1, v2, c = h
    return lambda a, b, t, j: (a + j * v1, b + j * v2, t + j * c)

if __name__ == "__main__":
    print("TV distance of single-copy Fourier-sampling law from uniform (H = 1)")
    print(f"{'R':>3} {'T':>5} {'h':>12} {'Heisenberg <h>':>15} {'abelian <(v,c)>':>16}")
    for R, T in [(8, 64), (12, 144), (16, 256)]:
        for h in [(1, 0, 0), (1, 1, 0), (1, 2, 1), (2, 3, 1), (3, 1, 2)]:
            pH, N = law(R, T, heis_step(h))
            pA, _ = law(R, T, abel_step(h))
            print(f"{R:>3} {T:>5} {str(h):>12} {tv_uniform(pH, N):>15.4f} {tv_uniform(pA, N):>16.4f}")
    # mass at small central frequency for the Heisenberg law
    print("\nShare of TV(H=<h>) carried by central frequencies |gamma| <= T/R:")
    for R, T in [(8, 64), (12, 144), (16, 256)]:
        h = (1, 2, 1)
        pH, N = law(R, T, heis_step(h))
        dev = np.abs(pH - 1.0 / N)
        g = np.arange(T); small = (np.minimum(g, T - g) <= T // R)
        share = dev[:, :, small].sum() / dev.sum()
        print(f"R={R:>3} T={T:>4} h={h}: share {share:.3f} (these frequencies are {small.mean():.3f} of all)")
