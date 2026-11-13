# Weak product phase: full Born sampling admission

2026-11-14. One bounded constructive classical challenge selected after
independent hidden-field, arithmetic and physical comparisons. Full213-line
selection/source review parent-read at
`audits/reviews/2026-11-14-independent-physical-selection.md`.
No new quantum mechanism or speedup is claimed.

## Native endpoint and reason for selection

Input: a finite open square lattice of N listed qubits, rational complex
Hermitian 4x4 edge matrices h_e with ||h_e||<=1, binary rational lambda>=0,
and error epsilon. H=-sum Z_i+lambda sum h_e. Fix 0<=lambda<=2^-24,
independent of N and epsilon. Here Delta=2,d<=4,J<=1, so BDL's
lambda_0>=2^-19; this explicit choice also lies within its stronger
two-site-observable window lambda_0/[2(d+1)]. Any proposed full sampler
may prove a smaller explicit constant window, but must state that scope.
Output a sample
within TV epsilon of the unique ground state's computational-basis Born
law, in poly(N,input bits,1/epsilon) time with capped failure probability.
No amplitudes, ground energy, inverse source or conditional probabilities
are supplied. Complex signs are permitted. Full spin snapshots are a
physical output distinct from already tractable local expectations.

The quantum mechanism is ALREADY KNOWN: a uniform gap along the product
Hamiltonian interpolation pays ordinary adiabatic preparation and readout.
BDL's fixed-coupling gap theorem suffices for this quantum upper bound;
there is no need to assume the dissipative compiler as a free operation.
The independently interesting dissipative theorem pays all-start
logarithmic mixing in its OWN fixed weak window, with a qualitative tail
repair below. No claim that 2^-24 lies inside that unspecified window is
needed or made. Potential asymptotic advantage over a general classical full sampler
is UNKNOWN, not inferred. This pass asks whether that native readout has
a classical polynomial counterpart, before any quantum implementation.

Compared alternatives: exact hidden-field Jacobi readout fails; retaining
its phases supplies no decoder. Explicit diagonal cubic recovery is
classical; CSA minimal modules are already closed written. Choi spectral
response repeats a screened simulation/QPE operation. This concrete
normalization/sampling obligation can resolve a meaningful physical output
and is selected over those duplicate or receiver-free alternatives.

## Actual source and classical-baseline gates

Corpus snapshots and four primary PDF/text/provenance bundles are retained
in `audits/sources/dissipative_selection/` (snapshots pending final freeze).

- Bravyi--DiVincenzo--Loss0707.1894: bounded-degree two-site interactions,
  Delta=min onsite gap, J=max interaction norm, lambda_0=2^-18 Delta/(dJ).
  Theorem1 gives unique gap>=Delta/2 for |lambda|<=2lambda_0. Theorems2--4
  pay ground energy/two-site observables, not full occupation prefixes.
  Theorem3 and linked-cluster proof compute creation coefficients through
  order k in N exp(O(k)) work for fixed degree. No positive coefficients.
- Mann--Waite2601.21140v2: Theorems1/5 genuinely sample the full diagonal
  Gibbs law, but |lambda|<=exp(-2r beta)/(e^4 beta Delta_graph 2^r).
  This does not cover fixed lambda at ground-state temperature. The
  abstract's arbitrary-temperature phrase cannot replace this inequality.
- Helmuth--Mann2201.06533v2: Theorem15 gives a low-temperature partition
  FPTAS under stable-phase/Peierls/pure spatial-boundary conditions. It
  supplies no arbitrary imaginary-time-slice occupation-prefix theorem.
- Zhan et al2503.15827v3 (published DOI10.1103/wzb3-dbg9): filtered
  K_i=integral f(t)exp(itH)X_i exp(-itH)dt, source Eq4; Theorem8 all-start
  trace-norm error<=8N exp(-t/4) in a fixed weak window. H17 has a
  stretched-exponential Gevrey tail; its summed tail is NOT O(2^-r) as
  later printed. H26 needs only sum_m(m+1)^(2D+2)Gamma(m)<infinity:
  choose a fixed cutoff with tail<1/8, then lambda small enough for the
  near-field term<1/8. This repairs qualitative fixed-locality contraction,
  not the source's displayed radius/coupling asymptotics. The known
  adiabatic bound above bypasses any new compiler/source-clock obligation.

Tensor-network truncation alone supplies no uniform bond/error bound.
Ordinary local expectations do not give the rare-prefix chain rule for
free. No classical impossibility follows from these source-scope limits.

## Positive representation lemma, with its remaining blocker

BDL gives u=exp(-C)|0>, C=sum_M C(M)a_M^dagger, commuting nilpotent
creation monomials. ||C||_1=max_i sum_(M contains i)|C(M)|. Lemma5 bounds
the order-p coefficient norm by 2^-15/(2lambda_0)^p. At lambda<=lambda_0,
let C_k be the degree-k truncation and D=C-C_k. Then

    ||D|| <= sum_M |D(M)| <= N ||D||_1 <= N 2^-15 2^-k.

Because C_k commutes with D, v=exp(-C_k)|0>=exp(D)u. Thus
||v-u||/||u|| <= exp(||D||)-1; normalizing u and v costs at most twice
this Euclidean error. Their Born laws are at most that far apart in TV.
Choose k=ceil(log2(8N/epsilon)). Polynomially many rational coefficients
therefore give a succinct creation-exponential representation within the
requested global state error. The independent addendum pays rational BIT
cost explicitly: Q=48 q_h q_lambda lcm(1,...,k+1), where q_h multiplies
all real/imaginary entry denominators. The recurrence divides only by
2|M| and j!, j<=4; order-p support has |M|<=p+1. Every lambda^p C_p(M)
has denominator dividing Q^p. Numerator bounds follow from Lemma5, so
intermediate and output bit lengths are polynomial. Rounding T retained
coefficients to epsilon/(32T) adds at most epsilon/32 operator error and
the SAME commuting argument pays its normalized global error. No vacuum
overlap lower bound is required. Full independent addendum parent-checked.

This is a representation/error statement, NOT a sampler: exp(-C_k) still
contains exponentially many amplitudes, and no normalization or conditional
evaluation oracle has been supplied. A useful construction must contract
this representation with output-bit projectors, or avoid tiny-prefix
division with a proved whole-distribution error bound.

## Cheapest exact falsifiers of proposed shortcuts

1. Hamiltonian compression is not output conditioning. For
   H=-Z1-Z2+lambda X1X2 and P=|1><1|_1, the true ground probability is
   (1-2/sqrt(4+lambda^2))/2>0. PHP on its range has energies0,2; its
   partition function divided by the full partition function tends0 as
   beta grows. Tr(P exp(-beta H)) cannot be replaced by Tr exp(-beta PHP).
   The same example has exact zero Born probabilities at01 and10.
2. A naive connected paired-cover polymer is not a probability. Take
   C1=C2=a,C12=a^2; exp(-C)|00>=[1,-a,-a,0]. Its connected two-site norm
   activity is a^4-2a^4=-a^4. This is native even at arbitrarily weak
   coupling: s=1+2a^2,E=-2/s,psi=[1,-a,-a,0],w=(H0-E)psi,
   V=-(w psi^T+psi w^T)/s with H0=diag(-2,0,0,2). Then Hpsi=Epsi,
   ||V||=sqrt(8)a/s<=3a. With lambda=4a,h=V/lambda has norm<1 and
   rational entries; for small a, Weyl's bound proves psi unique ground.
   This refutes only the positive-connected-activity interpretation.
3. Finite-time amplitude damping is not a mixture containing a positive
   exact reset fraction. After subtracting theta times reset, a Choi
   principal minor is [[1-theta,sqrt(eta)],[sqrt(eta),eta]], determinant
   -theta eta<0 for eta,theta>0. An entanglement-breaking reset argument
   cannot simply be imported into this zero-temperature dynamics.
4. Gap alone does not imply cooling: the torus Ising model in the review
   has unique ground, gap2, and all-down is dark for strictly downward
   filtered couplings supported on fewer than N sites. This does not
   refute the weak-interaction theorem or a fixed-source preparation.

## Final disposition and reopening condition

PARKED after one bounded constructive counterpart attempt. Claude/high
request78557 ended truncated/EMPTY, response0bytes, terminal/reapedexit1;
input23021/output48000tokens, runner estimate1.052084USD. No report,
scientific finding or completed review is inferred; no retry or paidOpenAI.
Exact packet/provenance: audits/api_inputs/2026-11-14-weak-born/;
terminal bundle: audits/claude_runs/2026-11-14-weak-born/.
The local1.5USD guard is not actual billing, a balance or a provider cap.

One exact Sage control at audits/controls/weak_born_shortcuts/ checked the
specified two-site identities and Choi minor once, terminal/reaped0,
session79436; full result and core script parent-read. At a=1/32 the
connected weight is -1/1048576 and gap1022/513; the ALL-a proof above
supplies the arbitrarily weak family (the fixture is not asserted to lie
in BDL's tiny window). No extra size sweep or sampler test is justified.

Established: polynomial-BIT succinct global state approximation in a
fixed weak window, and exact scoped failures of three shortcut operations.
The normalized full Born sampler remains UNKNOWN. Neither the source
scope gap nor the empty paid response is hardness or a general no-go.
No new quantum algorithm, speedup, novelty, full classical match,
coherent-state simulation or quantum execution is claimed.

Reopen only for a concrete positive sampling/contraction representation
that handles arbitrary rational signs and error with a bounded clock,
or an actual primary theorem covering this SAME full-output input model.
The next cheap acceptance test remains the exact two-site pinning and
negative-activity families, followed by the all-input TV/bit proof.
Do not continue generic prefix-condition analysis or increase the paid
request budget. Next pass starts from STATE/TRAPS and compares independent
constructive directions by external value.
