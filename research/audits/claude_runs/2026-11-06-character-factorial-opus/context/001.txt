# Native character Fourier features and the exact mask marginal

2026-11-06. Parent derivations, independent Codex actual-text review and
Claude targeted proof audit complete; review dispositions below. No new
end-to-end decoder is claimed.

## Scientific contract and choice

Input is an odd prime p, degree d and unknown monic squarefree Q over F_p.
The native copy source is p^(-1/2) sum_x F(x)|x>, with F a fixed sign table;
clean F(x)=lambda(Q(x)), lambda(0)=+1. The stronger chosen-BIT model supplies
F(x) on chosen classical inputs as well as coherent queries. These access
models are NOT interchangeable. The target is Q in poly(d,logp) time.

The existing uniform algorithm costs exp(O(d logd))*poly(logp), and its exact
consecutive-window Hankel readout has success<=1.5d^-d for irreducible Q
and every packet size 2d-1<=m<=p.
The candidate tested here was a decoder extracting imperfect-output Fourier
features or treating output labels as ideal moments plus independent public
mask noise. This might avoid waiting for a fully correct recurrence packet.
No new quantum subsystem is needed to test these hypotheses.

Prior work: corpus been-tried and baselines lookups (2026-11-06) supplied no
exact catalog match. Actual Russell--Shparlinski0212016 Theorem6 is an
O(d)-QUERY/POVM result, not an efficient decoder. Kopparty2601.07137 actual
Introduction and AlgorithmA/Theorem3.1 give a full-field-table classical
algorithm with polynomial field-size cost, under their degree/error bounds.
These are upper bounds, not hardness. The fixed-degree chosen-line
multivariate composition inherits the univariate cost. Independent new
superlattice DGS still uses exponential lists and has no paid clean inverse;
see SUPERLATTICE_CONDITIONAL_RECORD_AUDIT.md. These comparisons motivated
one focused test of a genuinely different decoder interface here.

## 1. Every additive Fourier mean has a matched classical estimator

Let m>=1, p>=m, V=F_p^(m+1), D=|V| and S the set of all degree-m squarefree
completely split polynomials with nonzero leading coefficient. Let
N=|S|=(p-1)binom(p,m). The paid source of the Hankel note is

 |S_F> = N^(-1/2) sum_{R in S} s_F(R)|R>,
 s_F(R)=chi(lead R)^d product_{x: R(x)=0} F(x).

Here d is the TARGET degree even if m differs. Coefficients are ascending.
Let P_F(y) be its normalized additive Fourier measurement law. Expanding
squared amplitudes and using character orthogonality proves, for every
public coefficient shift h in V,

 E_{y~P_F} exp(2*pi*i*<h,y>/p)
   = (1/N) sum_{R in S, R+h in S} s_F(R)s_F(R+h).             (1)

The source is real, so its Fourier law is even and the mean is real; a
choice of Fourier sign replaces h by-h without changing (1).

Classical algorithm in the chosen-BIT model: sample R uniformly in S by a
uniform leading coefficient and uniform m-subset of F_p. Form and factor
PUBLIC R+h. Return0 unless it has exact degree m, nonzero leading
coefficient and m distinct linear factors. Otherwise query the two root
sets (at most2m native signs), and return s_F(R)s_F(R+h). This bounded
random variable is an unbiased estimator of (1). Sampling a uniform subset,
public finite-field polynomial factorization and all field operations cost
randomized poly(m,logp). No split-event postselection is performed: failures
are zero observations, not expensive rejected samples. Q is never read.
Uniform subset sampling can use sequential sampling without replacement
with a finite-index map; it does not require a p-sized table.

For a fixed public upper bound K on adaptively chosen shifts and additive
accuracy epsilon, use
O(epsilon^-2 log(K/delta)) independent observations per query, with standard
bounded clocks for finite-field factoring and random-bit generation and
failure allocated within delta. A timed-out routine ABORTS the whole run;
it must not report a zero observation. Use Floyd's m-draw subset algorithm
and capped exact uniform draws. Split/squarefree membership itself is
deterministic by checking R+h divides X^p-X; only root extraction needs
randomized factorization. The conditional Hoeffding guarantee holds
for each query given the preceding transcript; union bound gives simultaneous
accuracy. Cost is poly(K,m,logp,epsilon^-1,log1/delta), including native sign
queries. The exact law holds for ANY fixed F, including a fixed corrupted
character table. It does not cover arbitrary amplitude-weighted sources.

Consequently a decoder whose guarantee holds for ANY epsilon-accurate
statistical-query answers to polynomially many additive Fourier means is
classically matched at inverse-polynomial epsilon in the chosen-BIT model.
Matching means alone does not reproduce finite-estimator randomness, joint
adaptive sample laws, or an algorithm exploiting those laws. It does not
sample P_F, simulate arbitrary functions of Fourier labels, recover Q, or
apply to a copy-only source. A successful decoder using this interface would
be a classical algorithm too, not an oracle separation in the chosen-BIT model.

This also covers the complete-syndrome score of any PUBLIC candidate: for
any supplied subspace B<=V and coset representative z, the projector identity
is 1_{y in z+B^perp}=E_{h uniform B} exp(2*pi*i*<h,y-z>/p).
Sample h from B and return cos(2*pi*<h,z>/p) times the estimator above.
Its expectation is P_F(z+B^perp), its magnitude is at most1, and its additive-
epsilon cost remains polynomial in the input basis size,m,logp,epsilon^-1.
Evaluate cosine to error<=epsilon/2 with polynomially many precision bits.
This scores a candidate to additive accuracy; it neither finds the unknown
candidate nor supplies relative accuracy for exponentially small scores.

## 2. Syndrome marginal is mask-only; the full law is not independent noise

Now restrict to CLEAN monic irreducible Q, degree d>=2, m>=d. Let
L:V->A=F_p[X]/Q, W=ker L, K0=|W|=p^(m+1-d), H=W^perp. On every residue
fiber S_v={R in S:R modQ=v}, s_F(R) is, up to one global sign, chi_A(v).
No split R is divisible by Q, so v!=0 on S.

Let |M>=N^(-1/2) sum_{R in S}|R> be the PUBLIC unsigned split mask, with
Fourier law P_M. For EVERY coset z+H, the Fourier projector gives

 P_F(z+H) = 1/(N*K0) sum_v
        |sum_{R in S_v} exp(2*pi*i*<z,R>/p)|^2
          = P_M(z+H).                                      (2)

The character phase cancels inside each fiber. Thus the complete syndrome
(y modulo H, equivalently all true-Q recurrences) has EXACTLY the public
mask's induced marginal. This is not just equality of the zero syndrome.
Computing that syndrome requires Q, so (2) supplies no native decoder or
simulator. The same fiber-phase proof in fact works for any root-free Q,
even reducible or non-squarefree, since the determinant of multiplication
by R in F_p[X]/Q still equals the resultant and never vanishes here.
The ideal uniform H\{0} law below, however, requires irreducibility.
For Q with rational roots, zero padding breaks this norm-phase argument;
(2) is not asserted in that case or for corrupted F.

A tempting stronger model takes independent T uniform on H\{0} (the ideal
irreducible norm-character Fourier law) and Z~P_M, then asserts y=T+Z.
It too has (2), but its FULL LABEL law is generally wrong: Fourier amplitudes
convolve coherently, and taking squares retains cross terms.

Cheapest exact counterexample REUSES the existing p5 irreducible control:
Q=X^2+2,d2,m3,N40,K0=25,D625. Existing exact residue counts give energy
sum_v |S_v|^2=72 and signed sum8. Therefore

 P_F(0)=8/3125,
 P_M(H)=9/125, P_M(0)=8/125,
 Pr[T+Z=0]=(P_M(H)-P_M(0))/(|H|-1)=1/3000.

These are unequal. Both models nevertheless have the SAME complete
true-Q syndrome law. A check of total mass on H or even every syndrome
would miss this error. This refutes this independent full-label noise
model, not all imperfect-outcome decoders. The zero label is singular for
Hankel decoding, but is a legitimate receiver outcome. Artifacts reused:
classical_baselines/hankel_resultant_control.json and the exact counting
calculation recorded in LEGENDRE_HANKEL_SUCCESS_BOUNDARY.md. No new FFT,
parameter sweep or quantum routine is needed for this falsifier.

The exact identity also fails throughout the large-prime regime for EVERY
odd d>=3, irreducible Q and nonempty split source m>=d. Scaling the leading
coefficient multiplies the actual source sign by chi(a)^d, so P_F(0)=0.
Write U=p^d-1 and C_v=|S_v|. C_0=0 and Cauchy--Schwarz give
sum C_v^2>=N^2/U. The proposed mixture instead has

 Pr[T+Z=0]=[sum C_v^2/(N*K0)-N/D]/U >= N/(D*U^2)>0,

using D=K0*p^d. This is an exact-identity counterexample under theorem-sized
primes too. The difference can be tiny: no useful total-variation lower
bound or rejection of a CONTROLLED APPROXIMATION follows from it.

## 3. Recurrence rows are not mostly correct

For m>=d, let s_i(y)=<X^i Q,y>, 0<=i<=m-d. The event s_i=0 is a Fourier
projector averaging over affine cosets of span(X^iQ), each of size p.
For i=0, two distinct split labels in one such coset share no root:
a shared root would be a root of cQ, impossible for root-free Q.
Thus each coset contains at most floor(p/m) split labels. For i>0, distinct
labels share no NONZERO root, and each has at least m-1 nonzero roots;
occupancy is at most floor((p-1)/(m-1)). Fiberwise Cauchy--Schwarz yields

 Pr(s_0=0)<=floor(p/m)/p<=1/m,
 Pr(s_i=0)<=floor((p-1)/(m-1))/p<1/(m-1), i>0.

This holds even for arbitrary weights and retained ancillary vectors on
S. Hence E[number of correct recurrence rows]
 <=1/m+(m-d)/(m-1)<=1.
At m=2d-1 it is <=1/2+1/(2d-1). This disproves a mostly-correct-row premise.
It does not exclude low-inlier-fraction robust regression, dense structured
errors, collective measurements or a different classical statistic. There
is no lower bound saying these upper bounds are attained.

## Disposition and remaining question

Established deductions: exact classical chosen-sign Fourier-mean estimator;
exact mask-only true-Q syndrome marginal; explicit failure of independent
full-label mask noise; failure of mostly-correct recurrence-row premise.
None establishes hardness, an impossibility for general measurements, a
new polynomial decoder, a speedup, novelty or quantum execution.

To escape this CHOSEN-BIT classical match, a quantum-specific improvement
must use more than this robust inverse-polynomial additive-mean interface,
for example the actual coherent within-coset law. A polynomial statistical-
query decoder would nevertheless be valuable: it would solve the chosen-BIT
problem classically and decode the copy source quantumly. It is not ruled
out or deprioritized merely because it would be classically matched.
Merely lengthening packets, adding estimators without a decoder, or assuming
an exact independent-noise law is not admitted. No new implementation or
larger sweep is queued. The next operation must be concrete and selected
against independent native problems, not another nearby boundary analysis.


## Review and validation record

Independent Codex review accepted the proof and repaired two scope errors:
the old all-window bound is for irreducible Q and 2d-1<=m<=p; a classically
matched SQ decoder would still be valuable. Both corrections are integrated.
Claude Opus/high audit completed in
`audits/claude_runs/2026-11-06-fourier-feature-review-opus/` (estimated
usage$0.41804). Parent checked its derivations and integrated explicit
whole-run ABORT on factoring/sampling timeout, a fixed K bound, public
subspace scoring and the root-free extension of the marginal identity.
Its proposed universal language about rational roots was NOT adopted:
failure of the norm-phase proof is not failure for every such polynomial.
It did not audit the source papers or the all-window theorem; these retain
their earlier scoped reviews. The exact odd-degree extension was checked
by parent and Codex after the Claude snapshot, not by that Claude report.

The earlier Fable/high constructive call ended with stop_reason=refusal and
zero output tokens, estimated input usage$0.15552. No reason or substantive
report was supplied, so it supplies no scientific finding. The distinct
Opus task above was a narrow proof audit, not an automatic retry.

A single exact Sage reuse of the EXISTING p5 case is saved in
`audits/controls/legendre_fourier_feature_match/p5_reuse.py` and `.json`.
It independently reproduced N40, energy72, signed_sum8 and the unequal zero
probabilities. Enumerating the classical estimator's40-element population
for six public shifts gave means1,0,1/20,-1/20,0,1/10; zero observations
are retained. This is an exact finite classical attack/control, not a Monte
Carlo confidence experiment, an all-parameter test, a new FFT or quantum
execution. The proof, not these values, establishes (1)--(2).
