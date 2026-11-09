"""OSC(B) test at kappa = 5 (and kappa = 4 for validation): fast separable-type enumerator.

Object: F(U, V) of ../types/orbit_types_fast.py (labelled (S, T, z) mod PGL_2, (S, T) in (C1)).
Kernel osc_kernel.c (ctypes, threads): unlabelled S mod PGL_2 (lexicographic-minimum normal form,
weighted by orbit size, V re-symmetrised over S_k here), T not enumerated (multisets of U-values
per (S, z, bucket) with binomial weights, U re-labelled here with prod n_a!).

Statistics (definitions of ../types-proof/REPORT.md and ../types-proof/cert_check.py):
  Rees = F(-iota, -iota) (as orbit_types_fast), PW (as orbit_types_fast), PW_pair (cert_check (V)),
  N1 = Fhat(0)/k^2 (= C1tot of sep_types), mu1 = T1 k^-(k-1)^2, T1 = (p-2)_{k-2} (p-k)_k,
  B_L  = max over rho != 0, rho not a pair class, m = |supp r| + |supp c| <= 5 of n|Fh|/(k Fh0)
  B_H  = max over rho != 0, not pair, m >= 6 of |Fh| / (sqrt(m/N1) Fh0)
  and the cert_check versions B_L_cc (min support <= 2, incl. pairs, p|Fh|/(k Fh0)) and
  B_H_cc (min support >= 3).
Usage: python osc_k5.py k p1 [p2 ...] [--threads N] [--validate]
  --validate: also run ../types/orbit_types_fast.run (k = 5) or ../types/sep_types.run (k = 4)
  and compare F arrays exactly.
"""
import sys, os, math, itertools, time, json, ctypes
from concurrent.futures import ThreadPoolExecutor
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
lib = ctypes.CDLL(os.path.join(HERE, 'osc_kernel.so'))
lib.init_bin.restype = None
lib.init_bin()
P_u8 = ctypes.POINTER(ctypes.c_uint8)
P_i32 = ctypes.POINTER(ctypes.c_int32)
P_i8 = ctypes.POINTER(ctypes.c_int8)
P_i16 = ctypes.POINTER(ctypes.c_int16)
P_u64 = ctypes.POINTER(ctypes.c_uint64)
P_i64 = ctypes.POINTER(ctypes.c_int64)
lib.run_chunk.restype = ctypes.c_int
lib.run_chunk.argtypes = [ctypes.c_int, ctypes.c_int, P_u8, P_i32, P_i8, ctypes.c_int, P_i16,
                          ctypes.c_int, ctypes.c_int, P_u64, P_i64]


def primroot(p):
    fac, n, d = [], p - 1, 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g


def comps_of(k):
    return [n for n in itertools.product(range(k + 1), repeat=k) if sum(n) == k]


def enumerate_acc(k, p, nthreads=4, nchunks=None):
    assert (p - 1) % k == 0
    g = primroot(p)
    ind = np.full(p, 255, dtype=np.uint8)
    x = 1
    for e in range(p - 1):
        ind[x] = e % k
        x = x * g % p
    inv = np.zeros(p, dtype=np.int32)
    for a in range(1, p):
        inv[a] = pow(a, p - 2, p)
    perms = np.array(list(itertools.permutations(range(k))), dtype=np.int8)
    comps = comps_of(k)
    code2idx = np.full((k + 1) ** k, -1, dtype=np.int16)
    for i, n in enumerate(comps):
        code2idx[sum(n[a] * (k + 1) ** a for a in range(k))] = i
    KV = k ** (k - 1)
    nchunks = nchunks or 8 * nthreads
    accs = [np.zeros(len(comps) * KV, dtype=np.uint64) for _ in range(nchunks)]
    infos = [np.zeros(4, dtype=np.int64) for _ in range(nchunks)]

    def work(i):
        r = lib.run_chunk(k, p, ind.ctypes.data_as(P_u8), inv.ctypes.data_as(P_i32), perms.ctypes.data_as(P_i8),
                          len(perms), code2idx.ctypes.data_as(P_i16), i, nchunks, accs[i].ctypes.data_as(P_u64),
                          infos[i].ctypes.data_as(P_i64))
        if r != 0:
            raise RuntimeError('kernel error %d' % r)
        return r

    with ThreadPoolExecutor(nthreads) as ex:
        list(ex.map(work, range(nchunks)))
    acc = sum(a.astype(object) for a in accs)  # exact
    info = np.array([sum(int(inf[j]) for inf in infos) for j in range(3)] + [max(int(inf[3]) for inf in infos)])
    acc = np.array([int(v) for v in acc], dtype=np.uint64).reshape(len(comps), KV)
    return acc, info, int(ind[p - 1])


def build_F(k, acc):
    """Ft[U_0..U_{k-1}, V_0..V_{k-1}] exactly as orbit_types_fast (float64)."""
    comps = comps_of(k)
    cidx = {n: i for i, n in enumerate(comps)}
    K = k ** k
    KV = k ** (k - 1)
    kf = math.factorial(k)
    allw = np.array([[(i // k ** j) % k for j in range(k)] for i in range(K)], dtype=np.int64)  # allw[idx][j]
    pw = k ** np.arange(k, dtype=np.int64)
    compU = np.array([cidx[tuple(int((w == a).sum()) for a in range(k))] for w in allw])
    factU = np.array([math.prod(math.factorial(int((w == a).sum())) for a in range(k)) for w in allw], dtype=np.float64)
    compUa = [compU[((allw + a) % k) @ pw] for a in range(k)]
    # V symmetrisation over S_k (S was unlabelled)
    Gs = np.zeros((len(comps), K), dtype=np.float64)
    accf = acc.astype(np.float64)
    for tau in itertools.permutations(range(k)):
        Vt = allw[:, list(tau)]
        Vc = (Vt[:, 1:] - Vt[:, :1]) % k
        vidx = (Vc * pw[:k - 1]).sum(1)
        Gs += accf[:, vidx]
    Gs /= kf
    F2 = np.zeros((K, K), dtype=np.float64)
    for a in range(k):
        F2 += Gs[compUa[a]]
    F2 *= factU[:, None]
    resid = np.abs(F2 - np.round(F2)).max()
    F2 = np.round(F2)
    Ft = F2.reshape((k,) * k + (k,) * k)
    Ft = np.transpose(Ft, list(range(k - 1, -1, -1)) + list(range(2 * k - 1, k - 1, -1)))
    return np.ascontiguousarray(Ft), resid


def perm_weights(k):
    allr = np.array(list(itertools.product(range(k), repeat=k)))
    P = np.zeros(len(allr), dtype=complex)
    for sg in itertools.permutations(range(k)):
        Us = np.array([(-sg[i]) % k for i in range(k)])
        P += np.exp(2j * np.pi * ((allr * Us).sum(1) % k) / k)
    return P.reshape((k,) * k)


def stats(k, p, Ft):
    n = p + 1 - 2 * k
    kf = math.factorial(k)
    Fh = np.fft.fftn(Ft)
    F0 = Fh.flat[0].real
    sh = (k,) * k
    idx = np.indices(sh)
    rs1 = (idx.sum(0) % k == 0)
    m1 = (idx != 0).sum(0)
    del idx
    full = (k,) * (2 * k)
    supp = (rs1.reshape(sh + (1,) * k) & rs1.reshape((1,) * k + sh))
    mr = np.broadcast_to(m1.reshape(sh + (1,) * k), full)
    mc = np.broadcast_to(m1.reshape((1,) * k + sh), full)
    nz = supp.copy()
    nz.flat[0] = False
    leak = np.abs(Fh[~supp]).max() / F0
    absF = np.abs(Fh)
    Pc = perm_weights(k)
    Pa = np.abs(Pc)
    absPP = Pa.reshape(sh + (1,) * k) * Pa.reshape((1,) * k + sh)
    PW = (absF * absPP)[nz].sum() / (F0 * kf ** 2)
    pairr = (m1 == 2)
    S_pair = Pc[pairr].sum().real
    pair1 = nz & (((mr == 0) & (mc == 2)) | ((mc == 0) & (mr == 2)))
    corr2 = np.where(pair1, np.abs(Fh + k * F0 / n), absF)
    den2 = F0 * kf ** 2 - 2 * k * F0 * kf * S_pair / n
    contrib = corr2 * absPP
    PWp = contrib[nz].sum() / den2
    N1 = F0 / k ** 2
    T1 = math.prod(range(p - k + 1, p - 1)) * math.prod(range(p - 2 * k + 1, p - k + 1))
    mu1 = T1 * float(k) ** (-(k - 1) ** 2)
    mtot = mr + mc
    Lset = nz & ~pair1 & (mtot <= 5)
    Hset = nz & ~pair1 & (mtot >= 6)
    B_L = (n * absF[Lset] / (k * F0)).max()
    B_H = (absF[Hset] * math.sqrt(N1) / (np.sqrt(mtot[Hset]) * F0)).max() if Hset.any() else float('nan')
    Lcc = nz & (np.minimum(mr, mc) <= 2)
    Hcc = nz & (np.minimum(mr, mc) >= 3)
    B_L_cc = (p * absF[Lcc] / (k * F0)).max()
    B_H_cc = (absF[Hcc] / (k * np.sqrt(mtot[Hcc] * F0))).max() if Hcc.any() else float('nan')
    # PW_pair split: share from L classes, H classes, pair classes
    sh_pair = contrib[pair1].sum() / den2
    sh_L = contrib[Lset].sum() / den2
    sh_H = contrib[Hset].sum() / den2
    iota = tuple((-i) % k for i in range(k))
    Rees = Ft[iota + iota]
    classes = []
    sq = math.sqrt(p)
    for a in range(k + 1):
        for b in range(k + 1):
            sel = nz & (mr == a) & (mc == b)
            if not sel.any():
                continue
            m = a + b
            vals = n * Fh[sel] / F0
            row = dict(r=a, c=b, num=int(sel.sum()), max_n_absF=float(np.abs(vals).max()),
                       weil=(m - 2) * sq + 2 * k - m,
                       max_H=float((absF[sel] * math.sqrt(N1) / (math.sqrt(m) * F0)).max()),
                       pwpair_share=float(contrib[sel].sum() / den2))
            if m <= 4:
                mv = vals.mean()
                row['mean_nFh'] = [float(mv.real), float(mv.imag)]
            classes.append(row)
    return dict(k=k, p=p, Rees=float(Rees), PW=float(PW), PW_pair=float(PWp), N1=float(N1), mu1=float(mu1),
                N1_mu1=float(N1 / mu1), lam=p / k ** (k - 1), B_L=float(B_L), B_H=float(B_H), B_L_cc=float(B_L_cc),
                B_H_cc=float(B_H_cc), share_pair=float(sh_pair), share_L=float(sh_L), share_H=float(sh_H),
                leak=float(leak), classes=classes)


def validate(k, p, Ft):
    sys.path.insert(0, os.path.join(HERE, '..', 'types'))
    cap = {}
    orig = np.fft.fftn

    def fftn(a, *x, **kw):
        cap['Ft'] = np.array(a)
        return orig(a, *x, **kw)
    np.fft.fftn = fftn
    try:
        if k == 5:
            import orbit_types_fast as ref
        else:
            import sep_types as ref
        t0 = time.time()
        d = ref.run(k, p)
    finally:
        np.fft.fftn = orig
    Fr = cap['Ft']
    return dict(ref=ref.__name__, ref_time=time.time() - t0, ref_Rees=float(d['Rees']), ref_PW=float(d['PW']),
                max_abs_diff=float(np.abs(Fr - Ft).max()), ref_total=float(Fr.sum()),
                ref_C1=float(d['C1']) if 'C1' in d else None)


if __name__ == '__main__':
    args = sys.argv[1:]
    nthreads = 4
    do_val = False
    if '--threads' in args:
        i = args.index('--threads')
        nthreads = int(args[i + 1])
        del args[i:i + 2]
    if '--validate' in args:
        args.remove('--validate')
        do_val = True
    k = int(args[0])
    for p in map(int, args[1:]):
        t0 = time.time()
        c0 = time.process_time()
        acc, info, eps = enumerate_acc(k, p, nthreads)
        t1 = time.time()
        c1 = time.process_time()
        np.save(os.path.join(HERE, 'acc_k%d_p%d.npy' % (k, p)), acc)
        Ft, resid = build_F(k, acc)
        st = stats(k, p, Ft)
        st.update(nrep=int(info[0]), sum_orbit=int(info[1]), labelled_nf=(p - 2) * (p - 3) if k == 5 else p - 2,
                  N1_from_kernel=int(info[2]) * math.factorial(k), maxbucket=int(info[3]), int_resid=float(resid),
                  enum_wall=t1 - t0, enum_cpu=c1 - c0, total_wall=time.time() - t0)
        if do_val:
            st['validate'] = validate(k, p, Ft)
        cl = st.pop('classes')
        print(json.dumps(st), flush=True)
        for row in cl:
            print('   CLASS', json.dumps(row), flush=True)
