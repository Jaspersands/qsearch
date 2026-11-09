"""Deterministic Ivanyos-Santha Section 3 SDE solver (Rees Schedule 1).

Finds s != 0 in F_p^M with sum_i s_i^d lambda_i = 0 for arbitrary public
columns lambda_i in F_p^g, following arXiv:1503.09016v2 Section 3: the gcd
reduction to kappa = gcd(d, p-1), the Section 3.1 classification without
nonresidues (pi-parts, Pohlig-Hellman, whole-run restarts), Lemma 12 and
Theorem 11 (colliding representations), and the Section 3.3 accumulation.
Fact 2 is van de Woestijne's deterministic zero sum of kappa-th powers
(ISSAC 2005, Sections 5.2, 6.1, 6.2), with Selective Root Extraction built
from the same pi-part machinery. No randomness, nonresidue or field
enumeration. Every witness is verified exactly on the original columns.
This is a classical solver, not a quantum receiver or a novelty claim.
"""
from dataclasses import dataclass
from itertools import permutations
from math import gcd

from flint import fmpz


def _prime(prime):
    if type(prime) is not int or prime < 3 or not fmpz(prime).is_prime():
        raise ValueError("explicit odd prime integer required")


def _prime_divisors(n):
    out, f = [], 2
    while f*f <= n:
        if n % f == 0:
            out.append(f)
            while n % f == 0:
                n //= f
        f += 1
    return tuple(out+[n]) if n > 1 else tuple(out)


def _ceil_log2(n):
    return (n-1).bit_length()


def collision_arity(degree, rank):
    """G(d, a) = d^{d(d-1)/2} (a+1)^d of IS Theorem 11."""
    if type(degree) is not int or degree < 1 or type(rank) is not int or rank < 0:
        raise ValueError("integer degree>=1 and rank>=0 required")
    return degree**(degree*(degree-1)//2)*(rank+1)**degree


def is_arity(degree, rank):
    """B_d(a) = G(d, a)^ceil(log2(d+1)), the count main.tex (eq:is-arity) uses."""
    return collision_arity(degree, rank)**_ceil_log2(degree+1)


def reduced_degree(prime, degree):
    """kappa = gcd(d, p-1) and a positive t with t*d = kappa mod p-1 (IS Section 3)."""
    _prime(prime)
    if type(degree) is not int or degree < 1:
        raise ValueError("integer degree>=1 required")
    kappa = gcd(degree, prime-1)
    modulus = (prime-1)//kappa
    exponent = pow(degree//kappa, -1, modulus) if modulus > 1 else 1
    return kappa, exponent or modulus


class _Restart(Exception):
    def __init__(self, element):
        self.element = element


class _Found(Exception):
    def __init__(self, combination):
        self.combination = combination


class PiParts:
    """F_p^* = H_pi x H_pi' with pi the primes of d (IS Section 3.1)."""

    def __init__(self, prime, degree):
        self.p, self.d = prime, degree
        self.pi = _prime_divisors(degree)
        n_pi, rest = 1, prime-1
        for ell in self.pi:
            while rest % ell == 0:
                rest //= ell
                n_pi *= ell
        self.n_pi, self.n_rest = n_pi, rest
        self.e_pi = rest*pow(rest, -1, n_pi) % (prime-1) if n_pi > 1 else 0
        self.e_rest = n_pi*pow(n_pi, -1, rest) % (prime-1) if rest > 1 else 0
        self.root_rest = pow(degree, -1, rest) if rest > 1 else 0
        self.exponents = {}
        for ell in self.pi:
            power = 1
            while n_pi % (power*ell) == 0:
                power *= ell
            self.exponents[ell] = power

    def split(self, alpha):
        """alpha = gamma*gamma' with gamma in H_pi and gamma' in H_pi'."""
        p = self.p
        return pow(alpha, self.e_pi, p), pow(alpha, self.e_rest, p)

    def rest_root(self, gamma_rest):
        """The unique delta' in H_pi' with delta'^d = gamma'."""
        return pow(gamma_rest, self.root_rest, self.p)

    def order(self, x):
        n = self.n_pi
        for ell in self.pi:
            while n % ell == 0 and pow(x, n//ell, self.p) == 1:
                n //= ell
        return n

    def _component(self, x, ell):
        power = self.exponents[ell]
        other = self.n_pi//power
        return pow(x, other*pow(other, -1, power), self.p) if power > 1 else 1

    def join(self, eta, gamma):
        """A generator of <eta, gamma> inside the cyclic group H_pi."""
        out = 1
        for ell in self.pi:
            a, b = self._component(eta, ell), self._component(gamma, ell)
            out = out*(a if self.order(a) >= self.order(b) else b) % self.p
        return out

    def dlog(self, gamma, eta, order):
        """e with eta^e = gamma (Pohlig-Hellman), or None if gamma is not in <eta>."""
        p = self.p
        if pow(gamma, order, p) != 1:
            return None
        residues, moduli = [], []
        for ell in self.pi:
            power = 1
            while order % (power*ell) == 0:
                power *= ell
            if power == 1:
                continue
            cofactor = order//power
            h, target = pow(eta, cofactor, p), pow(gamma, cofactor, p)
            base = pow(h, power//ell, p)
            digits = {pow(base, j, p): j for j in range(ell)}
            x, scale = 0, 1
            while scale < power:
                c = pow(target*pow(h, -x, p) % p, power//(scale*ell), p)
                x += digits[c]*scale
                scale *= ell
            residues.append(x)
            moduli.append(power)
        e, m = 0, 1
        for r, q in zip(residues, moduli):
            e += m*((r-e)*pow(m, -1, q) % q)
            m *= q
        assert pow(eta, e, p) == gamma
        return e


class Classifier:
    """alpha = zeta_r beta^d with zeta_r = eta^r, r in 0..d-1 (IS Section 3.1).

    The zeta_r form a possibly redundant but complete system of coset
    representatives of <eta>^d in <eta>. An element whose pi-part escapes
    <eta> raises _Restart; the caller enlarges eta and reruns everything.
    """

    def __init__(self, parts, eta=1):
        self.parts, self.eta = parts, eta
        self.order = parts.order(eta)
        self.calls = 0

    def zeta(self, r):
        return pow(self.eta, r, self.parts.p)

    def classify(self, alpha):
        parts, p, d = self.parts, self.parts.p, self.parts.d
        self.calls += 1
        gamma, gamma_rest = parts.split(alpha)
        e = parts.dlog(gamma, self.eta, self.order)
        if e is None:
            raise _Restart(gamma)
        f, r = divmod(e, d)
        beta = pow(self.eta, f, p)*parts.rest_root(gamma_rest) % p
        assert alpha % p == self.zeta(r)*pow(beta, d, p) % p
        return r, beta


def _kernel_vector(prime, vectors, spread=False):
    """Nonzero alpha with sum_k alpha_k vectors[k] = 0 when len > dimension.

    Default: the basis vector of the first free column. `spread` sums the
    whole kernel basis instead; IS allow any nonzero kernel vector.
    """
    p, count = prime, len(vectors)
    dimension = len(vectors[0]) if vectors else 0
    rows = [[vectors[k][i] % p for k in range(count)] for i in range(dimension)]
    pivots, r = [], 0
    for col in range(count):
        pivot = next((i for i in range(r, dimension) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][col], -1, p)
        rows[r] = [x*inv % p for x in rows[r]]
        for i in range(dimension):
            if i != r and rows[i][col]:
                c = rows[i][col]
                rows[i] = [(x-c*y) % p for x, y in zip(rows[i], rows[r])]
        pivots.append(col)
        r += 1
    frees = [col for col in range(count) if col not in pivots]
    alpha = [0]*count
    for free in (frees if spread else frees[:1]):
        alpha[free] = 1
        for i, col in enumerate(pivots):
            alpha[col] = (alpha[col]-rows[i][free]) % p
    return alpha


def _combine(prime, vectors, coefficients, degree):
    out = [0]*len(vectors[0])
    for v, c in zip(vectors, coefficients):
        if c:
            w = pow(c, degree, prime)
            out = [(x+w*y) % prime for x, y in zip(out, v)]
    return tuple(out)


def _classified_kernel(classifier, vectors, target, spread=False):
    """Classified kernel coefficients, multiplied by zeta_target/zeta_r.

    The shift keeps each known form zeta_r' beta^d, rewritten as
    zeta_s (eta^q beta)^d with r'+target-r = d*q+s, instead of
    reclassifying: when ord(eta) < d a canonical class misses `target`.
    """
    p, d = classifier.parts.p, classifier.parts.d
    alpha = _kernel_vector(p, vectors, spread)
    classes = [classifier.classify(a) if a else None for a in alpha]
    r = next(c[0] for c in classes if c)
    out = []
    for a, c in zip(alpha, classes):
        if c is None:
            out.append(None)
            continue
        q, s = divmod(c[0]+target-r, d)
        beta = pow(classifier.eta, q, p)*c[1] % p
        assert a*classifier.zeta(target-r) % p == classifier.zeta(s)*pow(beta, d, p) % p
        out.append((s, beta))
    return out, [a*classifier.zeta(target-r) % p for a in alpha]


def lemma12(classifier, vectors, level, stats):
    """IS Lemma 12: from B_level(d, m) vectors, the d^level sets J_a.

    Returns {a: (support, w_a)} with support a tuple of (index, beta_i) and
    w_a = sum_{i in J_a} beta_i^d v_i, such that J_(0,...,level-1) != {} and
    sum_s zeta_s w_{a(j,s)} = 0 for every a and every position j.
    """
    p, d = classifier.parts.p, classifier.parts.d
    m = len(vectors[0][1])
    if level == 1:
        stats["kernels"] += 1
        classes, _ = _classified_kernel(classifier, [v for _, v in vectors], 0,
                                        stats.get("spread", False))
        out = {}
        for s in range(d):
            members = [(idx, v, c[1]) for (idx, v), c in zip(vectors, classes) if c and c[0] == s]
            vec = _combine(p, [v for _, v, _ in members], [b for _, _, b in members], d) \
                if members else (0,)*m
            out[(s,)] = (tuple((idx, b) for idx, _, b in members), vec)
        return out
    groups = d**(level-1)*(m+1)
    size = len(vectors)//groups
    children = [lemma12(classifier, vectors[k*size:(k+1)*size], level-1, stats)
                for k in range(groups)]
    keys = sorted(children[0])
    concatenated = [sum((child[a][1] for a in keys), ()) for child in children]
    stats["kernels"] += 1
    classes, _ = _classified_kernel(classifier, concatenated, level-1,
                                    stats.get("spread", False))
    out = {}
    for a in keys:
        for r in range(d):
            members = [(child, c[1]) for child, c in zip(children, classes) if c and c[0] == r]
            support = tuple((idx, gam*beta % p) for child, gam in members
                            for idx, beta in child[a][0])
            vec = (0,)*m
            for child, gam in members:
                w = pow(gam, d, p)
                vec = tuple((x+w*y) % p for x, y in zip(vec, child[a][1]))
            out[a+(r,)] = (support, vec)
    return out


def _sign(perm):
    sign, seen = 1, [False]*len(perm)
    for i in range(len(perm)):
        if not seen[i]:
            j, length = i, 0
            while not seen[j]:
                seen[j], j, length = True, perm[j], length+1
            sign *= -1 if length % 2 == 0 else 1
    return sign


def theorem11(classifier, vectors, stats):
    """IS Theorem 11: disjoint I != {} and J with sum_I g^d v = sum_J g^d v.

    `vectors` is a list of (index, vector) of length G(d, m). Returns
    (I, J, w) with I, J tuples of (index, gamma) and w the common value.
    """
    p, d = classifier.parts.p, classifier.parts.d
    sets = lemma12(classifier, vectors, d, stats)
    m = len(vectors[0][1])
    for a, (support, vec) in sets.items():
        for j in range(d):
            total = (0,)*m
            for s in range(d):
                b = a[:j]+(s,)+a[j+1:]
                z = classifier.zeta(s)
                total = tuple((x+z*y) % p for x, y in zip(total, sets[b][1]))
            assert not any(total), "Lemma 12 identity failed"
    even, odd, w_even, w_odd = [], [], (0,)*m, (0,)*m
    for perm in permutations(range(d)):
        support, vec = sets[perm]
        if _sign(perm) == 1:
            even.extend(support)
            w_even = tuple((x+y) % p for x, y in zip(w_even, vec))
        else:
            odd.extend(support)
            w_odd = tuple((x+y) % p for x, y in zip(w_odd, vec))
    assert even and w_even == w_odd, "sign identity (13) failed"
    return tuple(even), tuple(odd), w_even


def selective_root(prime, degree, values):
    """van de Woestijne Thm 5.1 on F_p: i < j and beta with values[i] = beta^d values[j].

    Realized with the IS Section 3.1 tools: eta generates the pi-parts of
    the inputs, and pigeonhole on eta-logarithms mod gcd(d, ord eta) picks
    i and j (eta^k is a d-th power in <eta> iff that gcd divides k). With
    fewer than d+1 values it may return None (no collision certified).
    """
    p, parts = prime, PiParts(prime, degree)
    if not values or any(v % p == 0 for v in values):
        raise ValueError("nonzero field elements required")
    split = [parts.split(v) for v in values]
    eta = 1
    for gamma, _ in split:
        eta = parts.join(eta, gamma)
    order = parts.order(eta)
    g = gcd(degree, order)
    seen = {}
    for j, (gamma, rest) in enumerate(split):
        e = parts.dlog(gamma, eta, order)
        if e % g in seen:
            i, ei = seen[e % g]
            k = (ei-e)//g
            x = k*pow(degree//g, -1, order//g) % (order//g) if order > g else 0
            beta = pow(eta, x, p)*parts.rest_root(split[i][1]*pow(rest, -1, p) % p) % p
            assert values[i] % p == pow(beta, degree, p)*values[j] % p
            return i, j, beta
        seen[e % g] = (j, e)
    return None


def _blocks(runs, count):
    """Split runs [(multiplicity, y)] into `count` consecutive nonempty blocks."""
    total = sum(k for k, _ in runs)
    q, extra = divmod(total, count)
    sizes = [q+1]*extra+[q]*(count-extra)
    blocks, current, need, queue = [], [], sizes[0], list(runs)
    while queue:
        k, y = queue.pop(0)
        take = min(k, need)
        current.append((take, y))
        need -= take
        if k > take:
            queue.insert(0, (k-take, y))
        if need == 0:
            blocks.append(current)
            current = []
            if len(blocks) < count:
                need = sizes[len(blocks)]
    return blocks


def zero_sum_of_powers(prime, degree, *, shorten=True):
    """Nonzero z_1, ..., z_t (2 <= t <= d+1) with sum z_j^d = 0 in F_p, d | p-1.

    van de Woestijne (ISSAC 2005): for odd d use 1 + (-1)^d = 0 (Section
    6.2). Otherwise write -1 as p-1 copies of 1^d and run the Section 6.1
    reduction with Selective Root Extraction until at most d terms remain,
    then move -1 back. With `shorten`, keep reducing while fewer than d+1
    terms still give a certified collision; this extra step is ours.
    """
    _prime(prime)
    p, d = prime, degree
    if (p-1) % d:
        raise ValueError("degree must divide p-1")
    if d % 2:
        return (1, p-1)
    runs = [(p-1, 1)]

    def value(block):
        return sum(k*pow(y, d, p) for k, y in block) % p

    while True:
        total = sum(k for k, _ in runs)
        if total <= 1 or (total <= d and not shorten):
            break
        blocks = _blocks(runs, min(d+1, total))
        prefix, s = [], 0
        for b in blocks:
            s = (s+value(b)) % p
            prefix.append(s)
        assert prefix[-1] == p-1
        zero = next((j for j, v in enumerate(prefix) if v == 0), None)
        if zero is not None:
            runs = [t for b in blocks[zero+1:] for t in b]
            continue
        hit = selective_root(p, d, prefix)
        if hit is None:
            break
        i, j, beta = hit
        scale = pow(beta, -1, p)
        runs = [(k, y*scale % p) for b in blocks[:i+1] for k, y in b]+[
            t for b in blocks[j+1:] for t in b]
    z = (1,)+tuple(y for k, y in runs for _ in range(k))
    assert len(z) <= d+1 and all(z) and sum(pow(x, d, p) for x in z) % p == 0
    return z


def _row_reduce(prime, columns):
    """Columns re-expressed in a basis of their row space (an equivalent system)."""
    p = prime
    g, M = len(columns[0]), len(columns)
    rows = [[columns[i][r] % p for i in range(M)] for r in range(g)]
    out, r = [], 0
    for col in range(M):
        pivot = next((i for i in range(r, g) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][col], -1, p)
        rows[r] = [x*inv % p for x in rows[r]]
        for i in range(g):
            if i != r and rows[i][col]:
                c = rows[i][col]
                rows[i] = [(x-c*y) % p for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == g:
            break
    return [tuple(rows[k][i] for k in range(r)) for i in range(M)], r


def _accumulate(classifier, columns, level, stats):
    """IS Section 3.3: one vector with 2^level disjoint d-th power representations.

    `columns` is a list of (index, vector) of length G^level. Returns
    (u, reps) with each rep a tuple of (index, c) and sum c^d v = u.
    Raises _Found when an intermediate common vector is zero, unless
    stats["early_exit"] is false: then accumulation continues through
    u = 0, whose J-side reps may be empty (they still sum to u), while
    reps[0] stays nonempty because I != {} at every level.
    """
    p, d = classifier.parts.p, classifier.parts.d
    if level == 0:
        (idx, v), = columns
        return v, (((idx, 1),),)
    size = len(columns)//stats["G"]
    children = [_accumulate(classifier, columns[k*size:(k+1)*size], level-1, stats)
                for k in range(stats["G"])]
    stats["theorem11"] += 1
    side_i, side_j, w = theorem11(classifier, [(k, u) for k, (u, _) in enumerate(children)], stats)
    if not any(w) and stats["early_exit"]:
        raise _Found(tuple((idx, c*gam % p) for k, gam in side_i for idx, c in children[k][1][0]))
    reps = []
    for side in (side_i, side_j):
        for r in range(len(children[0][1])):
            reps.append(tuple((idx, c*gam % p) for k, gam in side for idx, c in children[k][1][r]))
    return w, tuple(reps)


@dataclass(frozen=True)
class SDEWitness:
    s: tuple
    degree: int
    reduced_degree: int
    rank: int
    zero_sum: tuple
    levels: int
    columns_required: int
    columns_supplied: int
    restarts: int
    classifications: int
    kernel_calls: int
    theorem11_calls: int
    early_zero: bool
    collapsed: bool = False


def _anchor_split(parts, alpha):
    """Pi-parts of the anchor relation and a generator eta_1 of the group they span."""
    anchor = [(k, parts.split(a)) for k, a in enumerate(alpha) if a]
    eta = 1
    for _, (gamma, _) in anchor:
        eta = parts.join(eta, gamma)
    return anchor, eta


def _anchor_witness(parts, eta, anchor):
    """Collapse test of the `collapse` variant (2026-11-05 restarts note, Lemma 1).

    `anchor` lists (k, (gamma_k, gamma'_k)) for the nonzero coefficients
    alpha_k = gamma_k gamma'_k of a relation sum_k alpha_k v_k = 0, with every
    gamma_k in <eta>. If all gamma_k lie in one coset of <eta>^kappa, returns
    (k, u_k) with alpha_k = gamma_0 u_k^kappa for the first anchor entry's
    gamma_0, so that sum_k u_k^kappa v_k = 0; otherwise None.
    """
    p, kappa = parts.p, parts.d
    order = parts.order(eta)
    g = gcd(kappa, order)
    logs = [parts.dlog(gamma, eta, order) for _, (gamma, _) in anchor]
    assert None not in logs
    if any((e-logs[0]) % g for e in logs):
        return None
    out = []
    for (k, (_, rest)), e in zip(anchor, logs):
        x = (e-logs[0])//g % (order//g)
        x = x*pow(kappa//g, -1, order//g) % (order//g) if order > g else 0
        out.append((k, pow(eta, x, p)*parts.rest_root(rest) % p))
    base = anchor[0][1][0]
    assert all((gamma*rest - base*pow(u, kappa, p)) % p == 0
               for (_, (gamma, rest)), (_, u) in zip(anchor, out))
    return tuple(out)


def columns_required(prime, degree, rank, *, shorten=True):
    """Columns the deterministic run consumes: G(kappa, a)^L, L = ceil(log2 t) <= B_kappa(a).

    Pass the same `shorten` as to is_sde_solve; inputs with a zero column
    need only that column.
    """
    kappa, _ = reduced_degree(prime, degree)
    if kappa == 1 or rank == 0:
        return rank+1
    t = len(zero_sum_of_powers(prime, kappa, shorten=shorten))
    return collision_arity(kappa, rank)**_ceil_log2(t)


def verify(prime, degree, columns, s):
    if len(s) != len(columns) or not any(x % prime for x in s):
        return False
    g = len(columns[0])
    total = [0]*g
    for x, col in zip(s, columns):
        if x % prime:
            w = pow(x, degree, prime)
            total = [(a+w*b) % prime for a, b in zip(total, col)]
    return not any(total)


def is_sde_solve(prime, degree, columns, *, shorten=True, spread=False, early_exit=True,
                 collapse=False):
    """Deterministic nonzero s with sum_i s_i^degree columns[i] = 0 over F_p.

    Requires len(columns) >= columns_required(prime, degree, rank, shorten=shorten),
    which is at most B_kappa(rank) <= B_degree(rank), unless some column is
    zero (then e_i is returned at once). Raises ValueError otherwise.
    `spread` selects the other deterministic kernel vector (see
    _kernel_vector); the default one often ends Theorem 11 with J empty.
    `early_exit=False` is a diagnostic that skips the zero-vector exits so
    that every run reaches the full Section 3.3 accumulation and Fact 2.
    `collapse=True` (off by default) is the restart-collapsing variant of
    research/audits/reviews/2026-11-05-rees-is-restarts.md: the first
    level-1 kernel relation (on columns 0..rank, independent of eta) is kept
    as an anchor, eta starts at the generator of its pi-parts, and at every
    restart trigger the anchor is tested first; when its coefficients fall
    into one coset of <eta>^kappa it is returned as the witness (`collapsed`).
    For prime kappa this run never restarts; for kappa = l^e it makes at most e
    runs.
    """
    _prime(prime)
    p, d = prime, degree
    if type(d) is not int or d < 1:
        raise ValueError("integer degree>=1 required")
    if not columns or not columns[0] or len({len(c) for c in columns}) != 1:
        raise ValueError("nonempty columns of one positive length required")
    M = len(columns)
    kappa, exponent = reduced_degree(p, d)
    reduced, rank = _row_reduce(p, columns)
    zero = next((i for i, col in enumerate(columns) if not any(x % p for x in col)), None)
    if zero is not None:
        s = tuple(int(i == zero) for i in range(M))
        return SDEWitness(s=s, degree=d, reduced_degree=kappa, rank=rank, zero_sum=(1,),
                          levels=0, columns_required=1, columns_supplied=M, restarts=0,
                          classifications=0, kernel_calls=0, theorem11_calls=0,
                          early_zero=True)
    stats = dict(kernels=0, theorem11=0, G=collision_arity(kappa, rank), spread=spread,
                 early_exit=early_exit)
    restarts, calls, z, levels, early, collapsed = 0, 0, (1,), 0, False, False
    if kappa == 1:
        need = rank+1
        if M < need:
            raise ValueError(f"need {need} columns, got {M}")
        stats["kernels"] += 1
        y = _kernel_vector(p, reduced[:need])+[0]*(M-need)
    else:
        z = zero_sum_of_powers(p, kappa, shorten=shorten)
        levels = _ceil_log2(len(z))
        need = stats["G"]**levels
        if M < need:
            raise ValueError(f"need {need} columns, got {M}")
        parts, eta = PiParts(p, kappa), 1
        combination = None
        if collapse:
            anchor, eta = _anchor_split(parts, _kernel_vector(p, reduced[:rank+1], spread))
            combination = _anchor_witness(parts, eta, anchor)
            collapsed = combination is not None
        while combination is None:
            classifier = Classifier(parts, eta)
            stats.update(kernels=0, theorem11=0)
            try:
                _, reps = _accumulate(classifier, list(enumerate(reduced[:need])), levels, stats)
                combination = tuple(pair for zj, rep in zip(z, reps) for pair in
                                    ((idx, c*zj % p) for idx, c in rep))
            except _Found as found:
                combination, early = found.combination, True
            except _Restart as restart:
                calls += classifier.calls
                eta = parts.join(eta, restart.element)
                if collapse:
                    combination = _anchor_witness(parts, eta, anchor)
                    if combination is not None:
                        collapsed = True
                        break
                restarts += 1
                continue
            calls += classifier.calls
            break
        y = [0]*M
        for idx, c in combination:
            assert y[idx] == 0
            y[idx] = c
    s = tuple(pow(x, exponent, p) if x else 0 for x in y)
    if not verify(p, d, columns, s):
        raise ArithmeticError("returned witness failed exact verification")
    return SDEWitness(s=s, degree=d, reduced_degree=kappa, rank=rank, zero_sum=z,
                      levels=levels, columns_required=need, columns_supplied=M,
                      restarts=restarts, classifications=calls,
                      kernel_calls=stats["kernels"], theorem11_calls=stats["theorem11"],
                      early_zero=early, collapsed=collapsed)
