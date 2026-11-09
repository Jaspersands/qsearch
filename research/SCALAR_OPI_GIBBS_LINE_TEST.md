# Scalar OPI: A Native Gibbs Field-Line Test

2026-11-06. Written analytical falsifier, independently reviewed against the
actual text by the parent research agent. The reviewer rederived the weighted
MDS variance, two-symbol affinity, change of law and self-loop mixing bound.
This is automated mathematical review, not human validation or a novelty claim.
No implementation, experiment, general classical lower bound, or first-witness
hitting claim. This tests one proposed sampler, not OPI search.

## Question and exact scope

Use the ORIGINAL full-table source: q=2^t>=4, m=q-1, the [m,k]
Reed-Solomon evaluation code C, 1<=k<=m, and independent uniform
q/2-element accepted sets S_i. All tables and the field are explicit.
Let H_S(c) count accepted coordinates, fix a real beta>0 independent of
the tables, and define

    Z_S=sum_(c in C) exp(beta H_S(c)),
    pi_S(c)=exp(beta H_S(c))/Z_S.

The candidate was to match an interior known DQI score by setting
theta=exp(beta)/(1+exp(beta)) to that score and sampling this Gibbs law
with polynomially many line updates. This would be a classical competitor,
not a new quantum algorithm. The promised output is one native polynomial
whose score is checked by Horner evaluation on the explicit tables.
Polynomial worst-start mixing was the proposed proof obligation; the
calculation below falsifies it for the specified update family. It does
not decide a different initialization or first-witness strategy.

Let D be any nonzero PUBLIC codeword. The exact field-line heat bath is

    K_D(c,c+uD)=exp(beta H_S(c+uD))
                  /sum_(v in Fq) exp(beta H_S(c+vD)).

This is an ideal heat-bath kernel; granting exact real weights only makes
the tested sampler stronger. It costs O(mq) table inspections plus public
arithmetic to evaluate the scores on a line;
no conditional-count oracle is assumed. Each K_D is reversible for pi_S.
A standard random-scan chain chooses D from a nonempty public catalog
of M directions with fixed positive scan probabilities. The catalog and
probabilities depend only on public code parameters, not tables or the
current state. This note does NOT analyze adaptively constructed directions,
satisfied-anchor selection, annealing schedules, or Algorithm H.
For the mixing statement, assume the catalog spans C, so irreducibility
is not the obstruction.

The published systematic-basis annealer is a STRONGER surviving baseline:
[2610.06753v1, Sections C.3 and D.1](https://arxiv.org/html/2610.06753v1)
updates its basis after moves, can pivot onto newly satisfied rows, and
changes beta during the run. It is outside this fixed-public-catalog,
fixed-temperature theorem. No result below rejects that published method.

Put tau=tanh(beta/2), d_*=m-k+1, and

    v_beta=(1+tau^2)^m/q^k,
    delta_beta=(1/2)*sqrt(v_beta),
    rho_beta=(q-2+q*sech(beta/2))/(2(q-1)),
    epsilon=M*(q-1)*rho_beta^d_*+delta_beta.

The native stationary expectation of the MAXIMUM exit probability over
the public catalog is at most epsilon. Consequently, for fixed R in (0,1),
k=floor(Rm), fixed beta>0 and M<=q^A for a fixed A, it is exp(-Omega(m)).
The specified random-scan sampler has exponential worst-start mixing time
with probability tending to one over the ORIGINAL tables. The proof and
its limitations follow.

## 1. Weighted partition variance and a paid planted comparison

Write a_beta=(1+exp(beta))/2 and W_S=Z_S/(q^k a_beta^m). Clearly E_S W_S=1.
For two codewords whose difference has z zero coordinates, independence
between rows and exact balanced-table two-symbol probabilities give

    E_S W_S^2=E_(D uniform C) A^z B^(m-z),
    A=1+tau^2, B=1-tau^2/(q-1).

For every set J of j coordinates, the MDS property gives
Pr[D_J=0]=q^(-min(j,k)). Expanding A^z B^(m-z) as a sum over such J,
and subtracting (B+(A-B)/q)^m=1, proves EXACTLY

    Var(W_S)=sum_(j=k+1)^m binom(m,j) B^(m-j) (A-B)^j
                                      *(q^(-k)-q^(-j))
            <= A^m/q^k=v_beta<=2^m/q^k.

This is the weighted version of the same MDS second-moment calculation in
SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md, derived here directly. It does not
assume independence among all codewords or supply a counting algorithm.

Let P0 be the original table law. Compare two JOINT laws on (S,c):

    Q(S,c)=P0(S)*exp(beta H_S(c))/Z_S,
    Pstar(S,c)=P0(S)*exp(beta H_S(c))/(q^k a_beta^m).

Q means original tables followed by a stationary Gibbs word. Pstar is a
PROOF-ONLY tilt: c is uniform in C and, conditional on c, the tables are
independent, with each original row law tilted by exp(beta*1[c_i in S_i]).
In particular the current hit bits are IID Bernoulli
theta=exp(beta)/(1+exp(beta)) under Pstar. Summing over c gives the exact
native-versus-planted identity

    TV(Q,Pstar)=(1/2)*E_(S~P0)|1-W_S|<=delta_beta.

No planted instance is supplied to an algorithm. This identity is what
pays the change of law; ignoring its normalization would be invalid.

## 2. Exact two-symbol affinity bounds the line exit

For two DISTINCT symbols in one uniformly balanced row, their acceptance
bits X,Y obey

    Pr[X=Y=0]=Pr[X=Y=1]=(q-2)/(4(q-1)),
    Pr[X=0,Y=1]=Pr[X=1,Y=0]=q/(4(q-1)).

Under the planted tilt at the current symbol, therefore,

    E_star exp(beta*(Y-X)/2)
      = E_0 exp(beta*(X+Y)/2)/a_beta
      = rho_beta < 1.

For a fixed nonzero u and public D, c_i and c_i+uD_i are distinct at
exactly wt(D) rows. Conditional on c the rows remain independent under
Pstar, so

    E_star exp(beta*(H_S(c+uD)-H_S(c))/2)=rho_beta^wt(D).

The exit probability e_D(S,c)=1-K_D(c,c) satisfies

    e_D <= sum_(u!=0) min(1,exp(beta*(H_S(c+uD)-H_S(c))))
         <= sum_(u!=0) exp(beta*(H_S(c+uD)-H_S(c))/2).

Hence E_star e_D<=(q-1)rho_beta^wt(D). Since wt(D)>=d_*, a union bound
over the public catalog, followed by the TV comparison for the bounded
function max_D e_D in [0,1], gives

    E_(S~P0) E_(c~pi_S) max_D e_D(S,c) <= epsilon.

No independence between the q-1 alternatives, or between catalog lines,
is used. For a fixed mixture one can omit M by averaging, but the stated
bound also controls all catalog exits simultaneously at typical states.

## 3. Consequence and the search boundary

Let L_S=E_(c~pi_S) max_D e_D. Markov gives
Pr[L_S>sqrt(epsilon)]<=sqrt(epsilon). Also Chebyshev gives
Pr[Z_S<(1/2)q^k a_beta^m]<=4v_beta. On their common good event,

    max_c pi_S(c)<=2*(2theta)^m/q^k.

For fixed positive R and beta this tends to zero, while
rho_beta tends to (1+sech(beta/2))/2<1. Thus epsilon=exp(-Omega(m))
for every polynomial public catalog. Eventually max_c pi_S(c)<=1/4.
Since L_S<=sqrt(epsilon), some state c has max_D e_D(S,c)<=2sqrt(epsilon).
For the fixed random-scan chain, starting at this c and taking
T=floor(1/(8sqrt(epsilon))) steps leaves probability at least3/4 of never
leaving c, by the union bound. Its distance from stationarity is therefore
at least1/2. This proves an exponential WORST-START mixing lower bound,
on a native-instance event of probability at least
1-sqrt(epsilon)-4v_beta. No spectral-gap assumption was used.

The existing all-bit-pattern count theorem also shows that, on its native
high-probability event, the Gibbs hit pattern is close to IID Bernoulli
theta after exponential tilting. Thus a finite beta can target a desired
constant score below1, including an interior DQI score. Having the desired
stationary mean does not pay sampling it by these field-line updates.

Crucially, slow mixing does NOT imply slow first attainment of a target
score from a uniform or Prange start. The obstructing stationary states
can already be successful witnesses. No conclusion here covers classical
OPI search, a full-input adaptive direction optimizer, another block
sampler, or the published quantum algorithm. No larger line-search sweep
is justified by this calculation.

Prior-work checks: corpus been-tried/baselines, SCALAR_OPI_NATIVE_PRIORITY.md,
SCALAR_OPI_SOFT_DECODING.md, SCALAR_OPI_FOURIER_ELIMINATION.md, and the
random-table list-sampler note above. The corpus also returned earlier
heat-bath traps on DIFFERENT sources; none was imported as a native bound.
No tests were run: all claims above are symbolic identities and inequalities,
reviewed as above, not finite evidence or an asymptotic approximation claim
inferred from experiments.
