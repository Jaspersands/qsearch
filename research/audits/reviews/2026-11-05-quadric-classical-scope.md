# Quadratic-character cone: classical and source scope

2026-11-05. Independent scoped audit; local primary sources and actual
baseline code inspected. No Git, network, external service, registry change,
or quantum execution. Scientific checks used
`/opt/anaconda3/envs/qsearch-cas/bin/python` and Sage finite fields.

## Native contract and prior-model distinctions

The proposed input is an unknown invertible symmetric A over an odd prime
field, odd n>=3, with padded sign F_A(x)=lambda(x^T A x), lambda(0)=+1.
The output is the projective class of A. Fresh pure global phase copies,
chosen BIT queries, raw phase queries, and full FIELD-VALUE queries are
different inputs; none is silently substituted for another.

Corpus `been-tried` and `baselines` searches were followed by actual code
inspection. `theorems/phase_state_workbench.py` function
`fp2_quadratic_algebraic_reconstruction_attack` subtracts exact residue
values of a KNOWN canonical quadratic and its translate. Its six-call
derivative solve does not recover an unknown A from character signs.
`CLASSICAL_VALUE_ACCESS_AUDIT.md` explicitly preserves this boundary.
The existing `classical_baselines/quadratic_legendre_birthday.py` assumes a
MONIC IRREDUCIBLE univariate quadratic; its sqrt(p) guarantee must not be
transferred verbatim to arbitrary padded line restrictions.

Local primary texts under `audits/sources/legendre_prf/` establish genuine
prior problem motivation but no novelty conclusion:

- Russell--Shparlinski, `russell_shparlinski_0212016.txt`, studies native
  character-only polynomial reconstruction and explicitly mentions its
  multivariate extension (lines94--98). Theorem6 supplies a POVM/query
  statement, not an efficient implementation of that measurement.
- Childs et al., `hidden_nonlinear_0705_2784.txt`, Section4.2 uses arbitrary
  INJECTIVE labels of polynomial level sets. Its separate hidden-radius
  lower bound concerns encrypted shifted-sphere oracles. Neither model is
  the two-sign character oracle here.
- `hidden_symmetry_1107_2189.txt`, Proposition5, already reduces quadratic
  HPP to O(n^2) univariate HQPP instances by coefficient ratios. Its HPP
  oracle satisfies f(x)=f(y) iff P(x)=P(y); this is not our sign oracle.
- Rotteler, `roetteler_quadratic_0911_4724.txt`, Section3, reconstructs a
  Boolean quadratic from phases (-1)^Q over F2. Such bits are full field
  values in F2, unlike Legendre signs of an odd-prime quadratic.

No audited source or code supplies a classical poly(n,log p) total-time
decoder for this exact sign-only problem. That is a scoped UNKNOWN, not
a hardness statement or an exhaustive priority search.

## Exact shifted-Legendre implication

Suppose a worst-case classical decoder recovers every promised A from
chosen F_A queries. For nonzero s, put

`Q_s(x)=x1*x2+s*x3^2+x4*x5+...+x_(n-1)*x_n`.

Its symmetric matrix is invertible. Given only L_s(t)=lambda(t+s), every
query is simulated with at most one original query: if x3!=0, return

`L_s((x1*x2+x4*x5+...+x_(n-1)*x_n)/x3^2)`;

if x3=0, evaluate the known remaining expression publicly. Multiplication
by x3^2 preserves lambda even at zero. Any returned projective matrix B
gives s=B33/(2B12). Public arithmetic is polynomial in n and log p.

The s=0 exception can be repaired without calling the decoder on a singular
matrix. Draw k independent uniform t in Fp*, comparing L_s(t) with public
chi(t). If every comparison agrees, return s=0. Otherwise s!=0 is CERTIFIED
and run the matrix decoder. For s=0 every comparison agrees. For s!=0,

`sum_(t!=0) lambda(t+s) chi(t) = -1+chi(-s)`,

so agreement probability is at most1/2 and false-zero probability at most
2^-k. Taking k=ceil(log2(2/eta)) and decoder error<=eta/2 covers every s.
Already n=3 with sufficiently large p meets any fixed p>=C*n^2 threshold.
This transfers a hypothetical classical total-time bound; it proves no
hardness, quantum separation, average-case claim, or copy-only reduction.

Exact F7 check: all6 nonzero shifts and all343 ternary x gave2058 successful
one-query simulations. All6 nonzero matrix scalars per shift gave36 correct
projective-ratio checks. These checks do not replace the displayed proof.

## Existing quantum oracle corollary and global-copy distinction

Let V consist of all e_i and e_i+e_j, i<j, so m=|V|=n(n+1)/2. Choose one
uniform u and restrict the oracle to x=t*u+v for each v in V. Write
Q(x)=x^T A x and B(u,v)=u^T A v. If Q(u)!=0 and

`D_v(u)=B(u,v)^2-Q(u)Q(v)!=0`,

the normalized restriction is a monic squarefree quadratic

`q_v(t)=t^2+2B(u,v)/Q(u)*t+Q(v)/Q(u)`.

For each nonzero v, D_v is a nonzero quadratic polynomial in u. If Q(v)=0,
it is the square of the nonzero linear functional B(-,v). Otherwise restrict
to v-perp: Q there is nondegenerate of dimension n-1, so D_v is not zero.
Schwartz--Zippel bounds each bad event by2/p. For odd n and nonsingular A,
Q has exactly p^(n-1) zeros; thus all restrictions are good with probability
at least1-(1+2m)/p. The weaker bound1-2(m+1)/p also suffices. A sufficiently
large absolute C makes p>=C*n^2 a constant-success genericity promise.

BIT or raw phase access prepares the chosen line phase state with one
query. Up to an irrelevant global sign chi(Q(u)), it differs from the monic
padded source only at at most2 roots. The independently reviewed fixed
corrupted-function degree2 decoder therefore applies, at its sufficient
prime threshold and with its paid error/copy bounds. Its already-proved
threshold can be absorbed into an absolute C. Amplify its failure to
O(eta/m) for all m calls. The constant coefficient of each decoded q_v
reveals Q(v)/Q(u); polarization recovers all entries of A/Q(u).

Consequently polynomial(n,log p) BIT/raw-phase reconstruction is already a
corollary of the reviewed univariate decoder. The oracle upper bound alone
is not the distinctive new operation. Fresh GLOBAL copies do not freely
prepare chosen line states: direct projection onto an affine line succeeds
with probability p^(1-n). This observation is not a general impossibility
theorem for converting or using global copies.

## Native O(n^2 p)-query classical moment algorithm

The same good-u line reduction gives a classical sign-only upper bound.
For a squarefree restriction, write

`g(t)=lambda(a*((t-h)^2-d)), a*d!=0, epsilon=chi(a), r in {0,2}`,

where r is its number of roots. Obtain epsilon once as F_A(u), under
Q(u)!=0. Query all p signs of a line and compute S0 as an INTEGER sum and
S1,S2 as field sums of t*g(t),t^2*g(t). Euler's criterion and finite-field
power sums give, for p>=5,

`S0=r-epsilon; S1=h*S0; M2=S2-h^2*S0=d*(r-epsilon/2)`.

The root-padding contribution is r to S0 and r*d to the centered second
moment; it must not be dropped. Recover r=S0+epsilon,
h=S1/S0, and d=M2/(r-epsilon/2), then q(t)=(t-h)^2-d. For p>=7 all
denominators are nonzero: S0 is in {-1,1,3}, and 2r-epsilon in {-1,1,3,5}.
The p5 nonsquare split case can have a zero second denominator and is
outside this formula's declared recovery scope.

Thus m line tables, one query at u, and polarization cost O(n^2*p) native
queries. Scalar moment accumulation also uses O(n^2*p) field operations;
explicitly assembling every n-coordinate query gives the safe total bound
O(n^3*p) field operations, with polynomial(log p) bit cost per operation.
No input-assembly savings or unit-cost n-coordinate serialization is assumed.
Genericity succeeds with the preceding constant probability. This is a
bounded-error upper bound; independent repetition and a majority of
canonically normalized projective outputs reduce error when C makes the
per-run success probability greater than1/2. No access to Q values or hidden coefficients
is used. In particular, when p=poly(n), this is already polynomial in the
input parameters. Any unresolved superpolynomial comparison must allow p
to grow superpolynomially in n. No sqrt(p) extension is asserted here.

The only new moment control enumerated all42 monic squarefree quadratics
over F7 and both leading-character signs. In all84 padded instances the
formulas recovered the correct monic polynomial, using exactly7 native
queries per instance, 588 total. Sage exact fields; zero failures.

## Native full-table baseline receipt

Before the parent's Fourier controls, one requested exact baseline used
p5,n3,A=I and its125 actual padded signs. Candidate coefficient order was
(x1^2,x2^2,x3^2,x1*x2,x1*x3,x2*x3), normalized by first nonzero coefficient1.
Sage determined nonsingularity; NumPy used bounded exact integer arithmetic
for table evaluations, not floating transforms or hidden value queries.

- 3906 projective candidates total;3100 nonsingular.
- Two scalar-character representatives {1,2}:6200 sign-table candidates.
- 775000 public candidate sign evaluations and775000 sign comparisons.
- Exactly one projective match and one scalar-class match: (1,1,1,0,0,0),
 scalar representative1.

The attack consumed only the125 source signs. This is a finite identifiability
and baseline receipt below the proposed theorem threshold, not a complexity
or separation theorem. No additional matrix scan was run.

Keep novelty, classical hardness, asymptotic separation, quantum execution,
mixed-source robustness, and free copy-to-oracle conversion claims false.

## Actual-text review of the cone receiver

After closing the preceding baseline checks, independently read the complete
`QUADRATIC_CHARACTER_CONE_READOUT.md` (355-line version supplied for review).
The written theorem is accepted under its exact stated source and parameter
promises. No mathematical correction was required.

The Fourier identities were rederived, including the padding term: use
chi(z)=G^-1 sum_(t!=0) chi(t)e_p(tz), then odd n cancels the multiplicative
character in the first transform. In the zero-indicator transform the
remaining character contributes chi(-q)G; G^2=chi(-1)p gives precisely the
note's epsilon. Thus equations(1)--(3) have the correct sign, normalization,
zero label and cancellation at chi(q)=+1. The exact cone mass and
alpha>=1-2/p bound also check.

The Witt-chart substitution C(1,-h,z) is a NONZERO polynomial unless C is
proportional to q: its five homogeneous degrees separately force precisely
that proportionality. Nondegeneracy and n>=3 ensure h!=0. The u!=0 chart's
Schwartz--Zippel bound and the u=0 chart's odd-dimensional zero count give
the stated uniform5/p intersection bound, including n=3. This proves the
full Veronese rank assertion rather than assuming generic samples.

The d=D-1 training cap, correct-prefix probability at least1-7/p, and
per-attempt success at least9/16 follow as written for p>=16n^2. Kernel
coefficients must indeed be halved off the diagonal before matrix inversion.
Fresh cone validation has correct probability at least1-2/p and wrong
probability at most7/p even when all noncone mass is credited to the wrong
candidate. Hence the Hoeffding constants, conditional-on-training guarantee,
fixed R,K schedule and ideal failure<=eta/2 are valid. Projective scaling
does not affect this test.

Finally, the at-most-L approximate QFTs have a stated event-probability
channel-error convention and a sufficient eta/(2L) hybrid budget. Standard
uniform approximate cyclic QFT circuits and field linear algebra have the
claimed polynomial cost. Exact fresh tensor copies are essential to the
independence and precision argument; no oracle inverse, selected-line
source, Gaussian phase estimate or unknown matrix inverse was imported.
This review accepts a written resource theorem, not executed quantum gates,
priority, hardness, separation, or any omitted source regime.
