# Direct Quaternion Quotient Readout

30 October 2026. Dewey the 2nd proposed and analyzed this concrete receiver
during the six-agent direction challenge. The parent checked the source
contract, norm-one unit factor and classical comparison. This is a narrow
receiver filter, not a lower bound for the compact quaternion problem.

## Exact Contract

Use the public order O and promised left ideal I=O*alpha, nrd(alpha)=q,
of QUATERNION_COMPACT_ORBIT_SOURCE.md. Let P_O,P_I be the ACTUAL finite
sequential Gaussian-bin laws of that note, and prepare independently

```
|C_O> = sum_x sqrt(P_O(x)) |x>,
|C_I> = sum_y sqrt(P_I(y)) |y>.
```

These are separately preparable coefficient states. We do NOT assert a
unitary that extracts pure coefficients from arbitrary nonorthogonal
physical packets while erasing their remaining state. The exact finite
laws, rather than untruncated ideal Gaussian approximations, are analyzed.

For x!=0 compute gamma=x^-1*y reversibly, retaining x. Nonzero x is
invertible because B is a division algebra. The x=0 branch is an abort,
not a discarded free conditioning step. Apply a finite Fourier transform
to the x-label register, with injective finite encoding and size M. Its
full record has probability

```
p(gamma,k) = (1/M) * |sum_(x!=0, x in O, x*gamma in I)
                    sqrt(P_O(x)*P_I(x*gamma))*chi_k(x)|^2.
```

Support conditions and zero probabilities are retained. Any nontrivial
arithmetic/encoding approximation needs its own error budget.

## Direct Success Bound

The direct decoder accepts the reported gamma precisely when
O*gamma=I and nrd(gamma)=q. These generators are H*alpha, H=O^1.
Indeed gamma*alpha^-1 belongs to O and has norm one; conversely every
h*alpha is a valid generator. Parseval over ALL Fourier outcomes gives

```
p_good = sum_(x!=0) P_O(x) * sum_(h in H) P_I(x*h*alpha)
       <= |H| * max_y P_I(y).
```

For fixed nonzero x the points x*h*alpha are distinct. In coordinate i,
the bin-integrated Gaussian has density at most 1/r_i and its retained
window has probability at least 1-beta_tail. Consequently every
conditional bin probability is at most 1/(r_i*(1-beta_tail)), and

```
p_good <= |H| / ((1-beta_tail)^N * product_i r_i).
```

This uses the sequential conditional law; independence of coordinates
is not assumed. The general bound |H|<=max(120,16d^2), N=4d, has a
separate proof in the source note. At fixed source error, its chosen
r_min>=C*N/epsilon_source^2 and beta_tail=O(1/N) give
p_good<=N^(-Omega(N)). Ordinary amplitude amplification of THIS marked
event still requires Omega(1/sqrt(p_good)) invocations for constant
success. This is worse in its N dependence than the comparator below.

For an actual prepared joint state within trace distance tau of the
specified finite state, retain p_good_actual<=p_good+tau. A constant
preparation error alone does NOT preserve the exponentially small bound.
The statement is about the specified source and direct marked event,
not arbitrary approximate preparations or arbitrary algorithms.

Classical independent sampling of x,y reproduces the gamma marginal
exactly, including abort. It does not reproduce the full k record. Using
k and nongenerator gamma to reconstruct a NEW answer is outside this
filter. Such records retain weighted intersection-lattice sums on
O intersect I*gamma^-1; a fast contraction and decoder remain missing.

## Matched Classical Comparator

On the same promised norm-exact input, the positive rational quadratic
form Q_q(x)=Tr_(F/Q)(nrd(x)/q) on I has minimum d. For nonzero x in I,
nrd(x)/q is a totally positive algebraic integer, so AM--GM gives Q_q>=d.
Equality forces every conjugate to be one, hence nrd(x)=q. A promised
generator attains equality; any shortest vector therefore supplies one.
The public field arithmetic determines this rational Gram form.

The [Aggarwal--Dadush--Regev--Stephens-Davidowitz exact SVP algorithm](https://arxiv.org/abs/1412.7994)
has randomized 2^(N+o(N)) time AND space, with input arithmetic charged.
The exponential memory is not omitted. This is an asymptotic comparator,
not an implemented PIP backend or a polynomial classical solver when d
grows. Constant-degree fixtures remain classical calibrations.

## Decision

Do not build a direct-quotient receiver backend or promote its rare good
branches. Re-entry requires a concrete decoder using the full weighted
records, or a different source/measurement with its own paid proof. The
finite controls in test_quaternion_pip_scope.py check quotient orientation,
the complete Parseval marginal, and the cyclotomic numerical factor;
they do not prove asymptotic performance or sample a quantum device.
