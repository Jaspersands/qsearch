# Scalar OPI anchor-plane admission

6 November 2026. A paid classical batching operation and exact invariants,
not a new quantum mechanism or an asymptotically competitive solver.
Independent derivation and actual-note core/addendum reviews accepted.

## Question and source admission

Can a polynomial-time classical algorithm match the known DQI score on
the ORIGINAL full-table scalar OPI distribution? As in
`SCALAR_OPI_NATIVE_PRIORITY.md`, q=2^t, m=q-1 nonzero evaluation points,
k=floor(Rm), and independent uniform q/2-element accepted sets S_i are
supplied in full. Output a degree<k polynomial and verify every row.
Assume k>=2 below. Input reading and arithmetic are charged; no compact
predicate, planted secret or privileged good direction is supplied.

At fixed rate the paid known Johnson-list quantum comparator has score
1/2+sqrt(a(1-a)), a=min(1/2,1-sqrt(1-R)); at R=1/4 this is about0.840625.
This is prior art, not a repository quantum algorithm or separation.
The desired falsifier is a classical polynomial full-input algorithm
reaching that quality with a paid success probability on the same source.

Corpus been-tried and baselines lookups preceded this calculation. Actual
[Mazumder--Niroula, arXiv:2610.06753v1, Appendix C.3](https://arxiv.org/html/2610.06753v1)
already allows systematic-basis pivots after codeword-line moves. For an
information set T, L=G G_T^-1; replacing row j by i with L_ij nonzero is
legal even when the current codeword does not change. Satisfied rows can
be preserved by those pivots. Appendix D counts adaptive moves and their
costs. Its numerical comparisons and Gaussian extrapolations are not
asymptotic complexity bounds.

For A of k-1 satisfied rows, D_A(X)=product_(i in A)(X-a_i). This is a
systematic basis column up to a nonzero scalar, using T=A union {b}.
An anchor exchange followed by choosing a different column therefore
uses the existing direction family. EXHAUSTIVELY choosing the exchange
by its resulting line maximum is a stronger policy than the paper
explicitly describes; the source does not establish that policy's
performance or say its experiments executed it.

Strong comparators remain best-of-N Prange, the published adaptive line
search/annealer, and the retained Algorithm H Fourier elimination. The
last has a failed predeclared q512 persistence test, not an asymptotic
upper bound. Neither the restricted Prange theorem nor the fixed-public-
catalog mixing theorem covers the present adaptive policy.

## Exact two-dimensional batching operation

Fix any input tables, a current codeword c and a satisfied anchor set A.
Remove one anchor a, leaving C of size k-2. Let d_i=D_C(a_i), and for
i outside C put g_i(z)=1_S_i(c_i+d_i z). Every g_i is balanced. The
degree<k plane has exact score

    F(u,v) = |C| + sum_(i outside C) g_i(a_i u+v),  (u,v) in F_q^2.

Use trace characters chi(z)=(-1)^Tr(z) and UNNORMALIZED transforms.
Summing first over v and then u gives

    Fhat(xi,eta) = q^2 |C| 1_(xi=eta=0)
                + q sum_(i outside C) 1_(xi=a_i eta) ghat_i(eta).

Indeed setting z=a_i u+v leaves sum_u chi((xi-a_i eta)u), which is q
exactly when xi=a_i eta. Distinct evaluation points give disjoint
NONZERO frequency lines. The zero-frequency contributions must all be
added. Inverse transformation divides by q^2 and returns integer scores.

Precompute all row Walsh transforms in O(mq log q) integer operations.
For d_i nonzero, change of variables gives

    ghat_i(eta) = chi(-eta c_i/d_i) hhat_i(eta/d_i), h_i=1_S_i.

Populate the plane spectrum in O(mq), then invert its length-q^2 Walsh
transform in O(q^2 log q). Field trace coordinates require a dual basis;
an ordinary binary dot-product basis must not silently replace them.
Construction of D_C evaluations costs at most O(mk) field operations.
Thus one plane costs O(mk+mq+q^2 log q), with O(q^2) stored integers
and polynomial bit costs. Transform integers have O(log(mq^2)) bits.
There is no floating-point precision or sampling-law normalization debt.

For a replacement anchor b in S(c) minus C, where S(c) is the HIT-INDEX
set of c, the allowed nonzero line points are (u,v)=(u,-a_b u), u!=0.
Include (0,0) for the incumbent if the objective includes it. Exclude
roots in C, the absent evaluation point0, and the direction at infinity
u=0,v!=0 when claiming EXACT equivalence to anchor swaps. The latter
points are valid degree<k polynomials, but preserve only k-2 anchors.
Scanning all choices of removed anchor costs O(k q^2 log q) plus field
work, not one plane's cost.

This transform is also a restriction of the exact Fourier objective in
`SCALAR_OPI_FOURIER_ELIMINATION.md`. It is a paid batching improvement,
not a new transform, decoder or source of quantum advantage.

## Every-table invariants and the missing drift

For EVERY input, c and satisfied A, averaging over its full line gives

    E_u H(c+uD_A) = (m+k-1)/2.

If h=H(c), the nonzero-parameter average is exactly

    mu = [q(m+k-1)/2 - h]/(q-1).

It is independent of A, including adaptively selected anchors. For the
full plane, uniform (u,v) makes each g_i a balanced Bernoulli variable.
Two distinct evaluation forms (a_i u+v,a_j u+v) are jointly uniform,
since their 2x2 matrix is invertible. Consequently

    E F = (m+k-2)/2,       Var F = (m-k+2)/4.

These are deterministic identities for complete tables, not fresh-table
heuristics. Mean or plane variance therefore cannot supply the proposed
anchor-selection gradient. Higher moments, tails and maxima CAN depend
on C; the identities do not bound adaptive maxima or first-witness time.

A precise restricted calculation is available. If c is table-independent,
or is ONE ordinary Prange completion with table-independent information
set and uniform accepted values there, conditioning on c and its hit
vector leaves rows independent and uniform subject to those hits. At a
different row value the acceptance probability is (q/2-b_i)/(q-1).
For L anchor sets chosen using only that hit vector, Hoeffding plus a
union bound over the L(q-1) nonzero points gives, with probability>=1-eta,

    max H <= max{h, mu + sqrt((m-k+1) log(L(q-1)/eta)/2)}.

Polynomial fresh lookahead has only a sublinear excess above the Prange
scale at fixed or inverse-polynomial eta. Selecting c or anchors using full tables destroys
this argument's conditioning hypothesis. It is NOT a bound on the
proposed repeated adaptive search or on Algorithm H.

A fully paid local policy can maximize P_c(A)=max_u H(c+uD_A) by scanning
all single-anchor exchanges and accepting only strict increases. With c
frozen, P_c is an integer in [0,m], so at most m increases occur; every
scan is polynomial. Its certified output is only an anchor-local maximum.
Including u=0 masks all line differences below h. Excluding u=0 removes
that masking and preserves the integer termination bound, but supplies
no proved quality guarantee either. Neither policy has a source-correct
adaptive drift theorem or a bound reaching the known quantum target.

## Control, independent comparison and disposition

One bounded Sage control completed on q8,k3, modulus z^3+z+1, with field
elements in integer-coordinate order. The seven native halfsets were
{0,2,4,6}, {1,2,6,7}, {0,2,3,6}, {2,3,4,7}, {0,2,3,4}, {0,2,5,7},
{4,5,6,7}, drawn by Python Random(3101). The fixed c=X²+X+1 has row
values [1,7,7,3,3,5,5] and five hits. C contains zero-based row1.
All64 Fourier identities matched direct native scoring. Plane mean4,
variance3/2 and all four allowed nonzero-line means31/7 agreed exactly;
the finite plane maximum was7. This is algebra/normalization evidence,
not an adaptive quality estimate. No optimization sweep or quantum run.
The first invocation reached the Fourier checks but failed on Sage's
unsupported QQ(n,d) call; QQ(n)/d corrected the control, not the theorem.
Temporary replay: `/opt/anaconda3/envs/qsearch-cas/bin/python
/tmp/qsearch_opi_anchor_plane_control.py`. The complete input above is
durable; no new reusable runner is introduced.

Independent comparison admitted no stronger mechanism:

- Scalar OPI anchor lookahead has the paid operation above, but no
  mechanism controlling the essential adaptive higher tails. No further
  annealing, parameter or finite-size sweep is justified by its invariants.
- Binary cubic phase-copy learning already has a separable measurement
  baseline: measure all but coordinate j in Z, then j in X, to obtain an
  exact quadratic derivative label. Classical F2 interpolation learns the
  nonconstant coefficients up to the unavoidable global phase. This is
  the known baseline in `POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md` and
  [Arunachalam et al., Section2.5.1 and Definition1](https://arxiv.org/html/2208.07851v2),
  whose actual text was checked this pass, not
  a new collective quantum receiver or a classical-input simulation.
- Unconditional complete class generation still lacks class coverage for
  the paid inverse-norm ideal sampler. Reusing it without that bound
  leaves the same unproved premise; no new subsystem is admitted.

The highest-value retained question remains a constructive first-witness
algorithm for original scalar OPI, but the pivot has no admitted run.
Re-entry requires a NEW operation or a source-correct adaptive quality
argument; input-independent tails, stationary mixing and invariant low
moments do not meet that gate. No general classical lower bound follows.
Before extending this line, compare independent high-upside mechanisms
again. The next read-only corpus query is recorded in the handoff.

Keep false: novelty, asymptotic DQI matching, classical hardness, quantum
speedup, efficient native first-witness search, and quantum execution.
No runner, registry or manuscript promotion is queued.
