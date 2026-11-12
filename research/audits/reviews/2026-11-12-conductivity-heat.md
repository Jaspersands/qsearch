# Reviewed conductivity heat-kernel classical upper bound

2026-11-12. Independent mathematical review of
`PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md`, including the final whole-transcript
finite-bit repair. The truncated paid heat report was checked as advisory
material; its verdict is not evidence for the theorem. No tests, Git, network,
or API calls were made in this review. The bounded binary-binomial sampler
contract in `BINARY_FOCK_KERR_SAMPLING.md` section 3a is imported.

**Disposition: the stated classical upper bound closes with the finite-clock
and arithmetic repairs below.** For every Boolean coefficient circuit of size
B on the two-dimensional L=2^n torus, fixed rational contrast rho>1, additive
error epsilon, and failure probability delta, the SAME conductivity scalar has
a bounded classical randomized algorithm with cost

    poly(B,n,1/epsilon,log(1/delta),native scalar bitlength)
        * [n+loglog(e^2/epsilon)]^O_rho(log(1/epsilon)+1).

Thus fixed contrast AND fixed precision give polynomial time in B,n; at
epsilon=n^-a for any fixed a>0 the bound is
poly(B,log(1/delta),native scalar bitlength)*exp[O_rho,a(log^2 n)].
This does not establish a polynomial bound jointly in n and 1/epsilon,
hardness, separation, novelty, or a general dequantization theorem. No spatial
regularity, randomness, or correlation promise is added to the coefficient
circuit. Scalar input bitlength is charged in addition to its numeric accuracy.

## 1. The exact scalar and the signed row sampler

Use D_i=S_(+e_i)-I, D_j^*=S_(-e_j)-I, K0=D^*D, and
Pi=D K0^+ D^*. Let eta be the normalized constant direction-j field,
c=(rho+1)/2, z=(rho-1)/(rho+1), and a=c(I+z Sigma). The minimizing field
e=eta+u, u in ran(Pi), satisfies Pi a e=0 and Pi eta=0. Solving this
equation by the norm-convergent Neumann series gives exactly

    K_j=c[1+z mu-z^2 sum_(r>=0)(-z)^r T_r],
    mu=<eta,Sigma eta>,
    T_r=<eta,Sigma Pi(Sigma Pi)^r Sigma eta>.

Both Sigma and Pi are contractions, so |T_r|<=1; dropping r>=k costs at
most c z^(k+2)/(1-z). These are the original energy minimization and output,
not a replacement observable or normalized rare source.

The heat semigroup has the exact analysis law

    (exp(-tK0)f)(x)=E f(x+Y),
    Y_l=N_l^+-N_l^- mod L,  N_l^+,N_l^- independent Poisson(t).

Poisson integration by parts, E[N f(N)]=t E[f(N+1)], yields

    (D_i exp(-tK0) D_b^* f)(x)
      =E[(N_i^+/t-1)(N_b^-/t-1) f(x+Y)].

Here i is the current edge direction and b is the next direction: the
departing direction uses the PLUS count, and the arriving direction uses the
MINUS count. They are independent even when i=b, so the mark product has
second moment exactly 1/t^2. For i=b its operator is
2I-S_(+e_i)-S_(-e_i), with the correct positive diagonal sign. At small time
use the four shifts (e_i-e_b,e_i,-e_b,0) with signs (+,-,-,+). Coincident
shifts when i=b remain separate equally likely choices and cause no problem.

The exact projection is the integral of the full block operator
G(t)=D exp(-tK0) D^*. For L>=2,

    Pi_T=integral_0^T G(t) dt=V(I-exp(-TK0))V^*,
    ||Pi-Pi_T||<=exp(-16T/L^2).

This is an OPERATOR-NORM estimate; no corresponding l1 kernel estimate is
proved or needed. The trivial L=1 or rho=1 cases can be returned directly.

## 2. Finite time grid, operator error, and conditional second moment

Take 0<epsilon<=1 and 0<delta<=1/2; fix a local tolerance tau<1 below.
Choose T=2^J>=max(1,(L^2/16) ln(2/tau)), and a dyadic spacing
h=2^-m<=tau/(32T). Integer upper approximations to the logarithms suffice.
Use midpoint quadrature of spacing h on every interval of

    [0,1], [1,2], [2,4], ..., [2^(J-1),2^J].

Call the resulting full edge operator A. It is defined analytically by this
large grid; the algorithm only samples grid indices. Since ||K0||<=8 and
||D||^2<=8, ||G'(t)||<=64. The summed midpoint error is at most
64Th/4=16Th<=tau/2. Hence ||A-Pi||<=tau and ||A||<=1+tau.
The component estimate ||G'_(ib)||<=32 alone needs a factor d=2 when
converted to a full block norm. This is why h<=tau/(32T) is safe.
Only O(J+m) random bits are needed to choose a time-grid point, since each
interval contains a power-of-two number of points.

One ideal signed transition from (x,i) samples an interval uniformly among
J+1, a uniform midpoint t within it, and a next direction b uniformly among
d=2. Sample the four independent Poisson counts. On [0,1], also choose one
of the four shifts/signs uniformly, add its shift to Y, and use weight
4d(J+1) times its sign. On [2^ell,2^(ell+1)], use weight

    W=d(J+1) 2^ell (N_i^+/t-1)(N_b^-/t-1).

This is an unbiased sampler for the ROW action of A. Conditional on the
entire past, its second moment is bounded by

    E[W^2 | past] <= H^2 := 16d^2(J+1)^2 =64(J+1)^2.

Indeed the small-time weight has exactly this square; the large-time
conditional square is at most d^2(J+1)^2 because t>=2^ell. No dependence
on x or the material circuit occurs in this bound.

For moment r, start at a uniform node in direction j, multiply by Sigma
there, make r+1 independent transitions, multiply by Sigma at every newly
visited edge, and finish with the indicator of final direction j. Its mean
is T_r(A), obtained by replacing every Pi in T_r by A. Tower conditioning,
not independence of the successive material values, gives

    E[path_product^2] <= H^(2(r+1)).

Telescoping operator products gives
|T_r(A)-T_r|<=(r+1)tau(1+tau)^r. Consequently, if
tau<=(1-z)/2, the total weighted operator bias is at most

    c z^2 tau/[1-z(1+tau)]^2 <=4c tau/(1-z)^2.

## 3. A completely finite experiment and its error budget

The following conservative constants suffice. Choose k>=1 such that
c z^(k+2)/(1-z)<=epsilon/8, and set

    tau=epsilon(1-z)^2/(32c),
    a=epsilon(1-z)/(8c),   b=epsilon/(8c),
    s_r=ceil(8 H^(2(r+1))/a^2),  0<=r<k,
    g=8 ceil(log2(4k/delta))+1  (odd),
    s_mu=ceil(2 b^-2 ceil(log2(8/delta))).

For each r use g groups of s_r independent paths and take the median of
their group means. Chebyshev gives group error>a with probability<=1/8;
Hoeffding for the independent groups gives median error>a with probability
at most exp(-9g/32)<=delta/(4k). Estimate mu by s_mu exact uniform-node
samples; Hoeffding gives error<=b except with probability<=delta/4.

**Necessary arithmetic repair:** round each completed raw path product to
a common dyadic grid of spacing 2^-P<=a before accumulating it. Exact
rational accumulation over many independently sampled times does NOT
automatically have bitlength polynomial in log(number of paths): the odd
numerators of dyadic times become distinct rational denominators. Rounding
each completed product incurs at most a/2 absolute error per path, hence at
most a/2 in every group mean and median. Thus use 2a as the total moment
error bound. This deterministic rounding applies to both the ideal analysis
experiment and the implemented experiment.

With ideal Poisson draws, the assembled estimate

    Khat=c[1+z muhat-z^2 sum_(r<k)(-z)^r That_r]

has error at most

    epsilon/8 (series tail)
      +epsilon/8 (operator replacement)
      +epsilon/4 (moment statistics and rounding)
      +epsilon/8 (mean statistics)
    =5epsilon/8

except with probability at most delta/2. The reported answer can be clipped
to [1,rho], which cannot increase its error. No assertion about expectations
under approximate samplers is used below.

Define the exact, predetermined counts

    R=g sum_(r<k) s_r,
    U=g sum_(r<k) (r+1)s_r <=kR,
    F=4U,
    C_material=s_mu+g sum_(r<k)(r+2)s_r <=s_mu+(k+1)R.

U is the number of transitions and F the number of count draws; all can be
executed even if a path's product has already become zero. R counts paths,
not transitions. The material circuit is called exactly once at each visited
edge, including the initial edge. No random degree selection is needed.

**Uniform interval choices also need a finite clock.** For J+1 not a power
of two, propose ceil(log2(J+1)) fair bits and reject out-of-range integers.
Cap this at ceil(log2(16U/delta)) attempts and use a fixed interval on
timeout. Acceptance probability is at least 1/2, so the total variation
between all U such choices and exact uniforms is at most delta/16. J=0
is deterministic. Node, next-direction, small-shift, and time-grid choices
are exact bounded fair-bit draws.

**Whole-transcript Poisson replacement.** Put beta=delta/(16F) and use one
common power-of-two integer

    Q>=max(T,2T^2/beta).

For each sampled t, draw Binomial(Q,t/Q) with TV error at most beta/2 using
the imported bounded-clock binary-binomial lemma. The exact binomial is
within t^2/Q<=beta/2 of Poisson(t). One elementary proof couples Q
Bernoulli(p) variables to independent Poisson(p) variables: each pair's TV
is p(1-exp(-p))<=p^2; summing gives Qp^2=t^2/Q. This is an analysis
coupling, not an implementation with Q iterations.

Conditional on every previous matched transcript and the current sampled
t, the count-draw error is at most beta. Thus all F draws differ from the
ideal transcript with probability at most F beta=delta/16. Combining the
interval and count couplings, the IMPLEMENTED success event differs from
the ideal success event by at most delta/8. Its failure probability is
therefore at most 5delta/8<delta. Signed weights can be arbitrarily large
in the ideal law: equality of coupled transcripts still implies equality
of their final rounded outputs. No weighted-TV expectation estimate,
weight clipping, or variance assertion about the implemented distribution
is required. Exact Poisson sampling is never performed.

## 4. Bit lengths and runtime

J=O(n+loglog(e^2/tau)), m=O(J+log(1/tau)), and

    log Q=O(J+log F+log(1/delta)).

Every sampled t has numerator/denominator bitlength O(J+m), and t/Q is a
dyadic rational of polynomial bitlength. Every implemented count lies in
[0,Q]; reduce its displacement modulo L by binary arithmetic. Each rational
transition weight has polynomial bitlength in J,m,log Q,log(J+1); a product
of at most k weights has at most k times this size. Its absolute value is
bounded by Wmax^k, with

    Wmax=max(4d(J+1), d(J+1)T(Q+1)^2).

After path rounding, a group sum uses a common denominator 2^P and a
numerator with O(k log Wmax+P+log R) bits. Division by the known group size,
comparison for the median, and the final k-term rational combination all
use polynomial bitlength in these parameters and the native scalar bits.
This is the missing justification for the note's short claim about sums.

The binomial sampler uses polynomial BIT work in log Q, bitlength(t/Q),
and log(1/beta), including its own bounded random-bit clock. Time-grid
sampling, capped interval sampling, circuit evaluations, and weight
arithmetic have the same kind of bound. There is no loop of numerical size
T, Q, L, or the number of time-grid points. The only large explicit loops
are the charged R paths, U transitions, and s_mu mean samples.

Since H^2>=64,

    R <=g[k+16 a^-2 H^(2k)],
    log R=O(k log H+log(1/a)+log g+log(k+1)).

Multiplying the explicit call counts by the preceding polynomial BIT cost
proves the upper bound stated at the top. In particular delta is paid
through log(1/delta), not an uncharged repeat-until-success procedure.

## Review boundary

The original series, mark orientation, diagonal case, and ideal conditional
second-moment argument survive the attack. Four repairs must be retained:
operator-norm-only time truncation; the full-matrix quadrature constant;
finite interval selection; and common-denominator accumulation via path
rounding. The partial report's proposed l1 truncation assertion is rejected,
and its speculative row-l1 lower-bound discussion is not needed or promoted.
The fixed exact energy control remains a transcription control only. The
open scientific boundary is a classical polynomial bound jointly in n and
1/epsilon for ALL native coefficient circuits; this proof neither supplies
nor rules out such a bound.
