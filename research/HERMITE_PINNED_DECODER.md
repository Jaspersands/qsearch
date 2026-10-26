# Pinned Differential Decoder For Streaming Hermite OPI

2026-10-21. Written derivation and exact classical controls; independent proof
and novelty review pending. No native quantum circuit has been executed.
No central claim admission, outreach, or preprint incorporation is authorized
by this note.

## Research Question

Can the exponential postprocessing in the near-optimal streaming Hermite-OPI
construction be replaced by polynomial-time decoding, while allowing
polynomial extra workspace? The proposed answer is constructive for growing
multiplicity. It does NOT preserve the tight linear workspace, solve ordinary
OPI, or establish an unrestricted-time Shor-level speedup.

The starting point is [Wu--Yang, 2610.01902v1](https://arxiv.org/html/2610.01902v1),
especially Section 5: a one-pass product source, an augmented syndrome carrying
random coordinates, and an exhaustive decoder. Their classical streaming
lower bound remains an external premise. Our proposed substitution is below.

The [fast multiplicity-decoding paper](https://arxiv.org/html/2311.17841v4)
uses differential interpolation and affine solution spaces, but its
near-capacity guarantee assumes characteristic larger than polynomial degree.
We cannot import its constant-dimensional kernel conclusion here.
[Kopparty--Ron-Zewi--Saraf--Wootters](https://arxiv.org/abs/1805.01498)
also supplies relevant affine-space pruning prior art. Neither interpolation
nor pruning is claimed as an invention of this repository.

More directly, [Guruswami--Wang, 1106.3951, Section 4.2 and Theorem 9](https://arxiv.org/pdf/1106.3951)
already uses noiseless derivative side information to avoid list enumeration,
under its large-characteristic hypotheses. This is an important antecedent,
not evidence that side-information decoding is a new paradigm here.

The potential contribution is their small-characteristic, **syndrome-only
and independently pinned** composition. Ordinary received-word pruning is
different: its sampled received values may be erroneous. The pins here are
actual coordinates of the error register retained in the augmented syndrome.
They must be paid for in the final score and quantum workspace.

## Problem And Claim Boundary

Let q be an odd prime, n=q-1, 1 <= ell < q, K=ell*n/2.
The code C consists of length-ell Hasse jets J_ell f(a), a in F_q^*, deg f<K.
Its scalar generator is G, with K rows and n*ell columns.
The input problem supplies explicit half-set membership tables as a classical
stream. N=(q-1)*q^ell counts entries, not a succinct-oracle input.

Choose constants 0<lambda<tau<1/2. Put d=floor(tau*n), Cguard=d+2.
The candidate decoder sees ONLY

    (G e, e_R), plus q, ell, a fixed differential order s and public R.

It does not see the actual e, its support, a planted polynomial, a list oracle,
or the original membership tables. Only the final equality herald compares
its returned vector with the existing source register.

Proposed asymptotic consequence, conditional on the checked composition:
for every fixed approximation target alpha<1, sufficiently large growing
multiplicity ell=floor(q^a), with fixed 0<a<1, admits polynomial(q,ell)
preprocessing, per-entry updating, postprocessing and reversible workspace.
Since q is polynomial in log N in this regime, these are polylog(N).
This sacrifices the sharper O(q*ell*log q) workspace.
It therefore does NOT settle the similar-space, fixed-multiplicity question
in the streaming paper's Section 1.4.

To retain a polynomial-N classical space/pass lower bound, a must also be
small enough for the published constant C_alpha. Do not supply an invented
numeric value for that constant. This is a restricted streaming improvement,
not a new general classical hardness theorem.

## 1. Explicit Syndrome-To-Jet Conversion

No dual-code transform is supplied as advice.
Let A(X)=(X^(q-1)-1)^ell. At a in F_q^*, define

    h_a(Z) = 1 / (A(a+Z)/Z^ell) mod Z^ell,
    (T_a)_(j,k) = [Z^(ell-1-j-k)] h_a(Z).

Negative-index coefficients are zero. Each T_a is symmetric and invertible:
its anti-diagonal is the nonzero constant h_a(0). Let T be block diagonal.
For deg f,deg g<K, the sum of residues of f*g/A is zero, because its
numerator degree is at most deg A-2. Expanding the residues gives

    (J f)^T T (J g) = 0.

The dimensions are half the ambient dimension, so ker G = T C.
The implementation independently checks G*T*G^T=0 and inverts every block.

Select e0(syndrome) by a FIXED right inverse of G, independent of R.
The first K scalar jet columns form a confluent Vandermonde information set.
Put y=-T^-1 e0. Every error of that syndrome is uniquely

    e=e0+T J f = T(J f-y).

Its block weight equals the block distance from J f to y. A retained error
block determines the true polynomial jet via J f(a)=y_a+T_a^-1 e_a.

## 2. Linear Hasse Interpolation

Choose 0<=s<ell<q. Seek a nonzero linear differential polynomial

    Q0(X) + sum_(j=0)^s Q_(j+1)(X) f^[j](X),

with deg Q0<=A+K-1 and deg Q_(j+1)<=A+j.
The unknown coefficient count is

    U=(s+2)A + K + (s+1)(s+2)/2.

At every point impose ell-s homogeneous linear constraints. For
0<=t<ell-s the constraint is

    Q0^[t](a)
      + sum_j sum_(u=0)^t Q_(j+1)^[t-u](a) binom(j+u,j) y_(a,j+u) = 0.

This uses (f^[j])^[u]=binom(j+u,j) f^[j+u], valid in small characteristic.
Choose the smallest A>=0 with U>n(ell-s). Require BOTH

    A+K-1 < n(ell-s),
    (n-Cguard)(ell-s) > A+K-1.

The first forces a message-dependent part: otherwise Q0 would have more
roots counted with multiplicity than its degree. The second forces the
specialized polynomial to be identically zero for EVERY codeword within
Cguard blocks of y. It is a strict integer inequality, not a numerical
radius fit. Invalid finite parameters are rejected.

Solve this polynomial identity as a linear coefficient system. Its affine
solution space V_y may contain far codewords, but includes every nearby one.
Choose the interpolant deterministically from y BEFORE consulting any pins.

## 3. Small-Characteristic Dimension Bound

For a nonzero operator L=sum_(j=0)^s A_j(X) D^[j], s<q, let

    h = max_j(deg A_j-j),
    R(t) = sum_(deg A_j-j=h) leading(A_j) binom(t,j).

The binomial polynomials for j<q are linearly independent over F_q.
Consequently R is nonzero, of degree at most s. Its value depends only on
t mod q, and has at most s zero residues.

Order unknown polynomial coefficients from highest degree to lowest.
The coefficient of X^(t+h) in L(f) has pivot R(t) on f_t; all other
potential contributions are from coefficients already considered.
Therefore

    dim ker L <= #{0<=t<K : R(t)=0} <= s*ceil(K/q).

If t+h<0, the corresponding pivot is zero automatically, so there is no
omitted negative-degree equation. Zero pivots need not be genuinely free;
the count is an upper bound, verified against actual matrix rank in controls.

**Essential falsifier:** over F_5, degree<17 solutions of f'=0 have basis
1,X^5,X^10,X^15, dimension FOUR, not the derivative order ONE.
Using ordinary large-characteristic dimension bounds would make this pass
invalid. The code retains these Frobenius directions.

## 4. Random Pins Resolve The Larger Space

Fix an error e, its syndrome, and the resulting affine space V_y containing
its polynomial f. Its homogeneous direction space W has dimension t at most
s*ceil(K/q). This space is fixed independently of R.

Every nonzero polynomial in W has a zero length-ell jet on at most

    z=floor((K-1)/ell) < n/2

evaluation points. Expose a uniform r-subset one point at a time.
While a nonzero direction space remains, choose any nonzero member of it.
Previously exposed points are already zeros of every remaining member.
Hence among the remaining points, the probability the next jet constraint
decreases dimension is at least 1/2. After t such decreases the space is zero.
A coupling with independent fair Bernoulli variables gives

    Pr[pins leave ambiguity] <= Pr[Bin(r,1/2)<t]
                            = 2^-r sum_(j=0)^(t-1) binom(r,j).

Also r>z forces uniqueness deterministically. The implemented bound takes
this into account. There is NO union bound over q^t enumerated candidates,
and no such enumeration in the algorithm. A sufficient budget is
r=O(t+b) for failure at most 2^-b. The implementation finds the smallest
r certified by this bound, using exact integer arithmetic.

The rank argument is deliberately conservative; a jet may remove many
dimensions at once. Do not replace its proven bound with observed
typical rank without a new theorem.

Algorithm: append the true pinned jets to the affine identity system,
solve it, and return a word ONLY if the affine solution is unique and
the reconstructed error satisfies the original syndrome, pins and guarded
distance. Otherwise return ABSTAIN. This can reject an error which is
uniquely decodable in the ball but not unique in the larger affine space.
That conservative rejection is included in the bound.

## 5. Coherent Composition And The Two-Block Guard

Compute the deterministic decoder reversibly on (G e,e_R). Accept exactly
when wt(e)<=d and its returned vector equals e. Uncompute all working
registers BEFORE measuring the herald. On acceptance, compute the augmented
syndrome, subtract the reconstructed error, and uncompute the decoder work.
This is a diagonal projection followed by an isometry on accepted labels.
It does not measure error values or use them as external classical advice.

Every accepted e is isolated among ALL errors in B_(d+2), because every
such competitor must belong to the same affine interpolation space.
This guard, not just uniqueness on B_d, is necessary for the score variance.
If x=e+a and y=f+b are single-block neighbors of accepted e,f and their
augmented syndromes collide, e and f+b-a are two members of B_(d+2) with
the same syndrome. Isolation implies x=y.

Thus the Fourier map is an isometry on the union of those neighbor supports.
For a score operator which changes at most one block, both first and second
compressed moments agree. No isometry on the full error space is asserted.

For the independent product source, define

    theta=lambda*(1-q^(-2ell)),
    delta <= exp(-2*(tau-lambda)^2*n) + 2^-b.

The first term is the source-weight tail, the second is the expected
diagonal rejection over independent R. This holds for arbitrary fixed
input tables: there is no random-instance source assumption.

Let mu be the ideal product score mean. It obeys

    mu/n >= 1/2 + sqrt(lambda*(1-lambda)) - 1/q.

The ideal variance is at most n/4. For unnormalized accepted source Phi,
the perturbation inequality gives, averaged over R,

    ||(M-mu)Phi||^2 <= n/2 + 2*n^2*delta.

Discarding auxiliary output coordinates loses at most r score terms.
With positive g=mu/n-alpha-r/n, the unconditional bad-output probability
is at most (1/(2n)+2*delta)/g^2. Add delta for herald failure and the TOTAL
circuit output-TV budget. This avoids conditioning on a possibly tiny
success probability for an individual R.

This argument is written, not independently certified. The code executes
the classical decoder and its finite inequalities, not a large coherent
streaming circuit.

## 6. Resource And Scaling Argument

For any fixed tau<1/2, choose a fixed s with

    (s+3)/(2*(s+2)) < 1-tau.

As ell grows, the interpolation agreement threshold divided by n tends to
the left-hand side. For sufficiently large ell and q the exact root
inequality, including the two extra blocks, holds.
Then t=O(s*ell), r=O(s*ell+log n), and r/n=o(1) for ell=q^a, a<1.
Choose lambda close enough to 1/2, still below tau, to reach any fixed
alpha<1 with a positive score gap.

The actual algorithms use polynomial-sized dense systems, not a compact
list oracle. Classical storage is O((q*ell)^2) field elements, and ordinary
elimination costs polynomial(q,ell) operations. A conservative reversible
implementation stores the polynomial-length computation history and then
uncomputes it; this is still polynomial space and time, NOT quadratic
space or the original linear-space theorem. More efficient reversible
elimination is optional and is not required for the polylog(N) consequence.

The stream source and its precision budget remain external components.
A conventional finite gate set must pay total synthesis error, including
accumulation across N arrivals; log(N) precision is polynomial(q,ell).
There is no second table pass and no QRAM assumption.

For fixed a>0, q=poly(log N). Choose a small enough that
kappa(alpha_classical)-C_alpha_classical*a remains positive in the external
classical lower bound. Then a polynomial-N classical space/pass product can
coexist with this proposed polylog(N) quantum upper bound.
This does not improve the lower bound or claim that constant ell gives
the same memory separation.

## Executed Controls

Producer: `theorems/hermite_pinned_decoder.py`.
Artifact: `research/reductions/hermite_pinned_decoder.json`.

- Native exact decoder: q=31, ell=24, n=30, K=360.
  Two distinct errors of block weight 8 have the SAME syndrome.
  Guaranteed unique-decoding radius is 7; guard radius is 10.
  The interpolant leaves dimension 1. Without pins the decoder abstains;
  with the same eight public pin positions it recovers either actual error.
  No support or polynomial is passed to the decoder. Both are accepted by
  the d=8 equality herald. These parameters do NOT certify high-score
  quantum performance.
- The residue duality is verified on the full native matrix. Additional
  small fields exercise right inverses, local jet identities, and ranks.
- Exhaustive pin-subset controls compare actual affine ambiguity with
  the rank-exposure bound. Exhaustive small syndromes reject false unique
  decodes. Wrong pins, missing guards, invalid characteristic/radii and
  source-cap violations are retained as negative controls.
- On the SAME native code, two weight-7 errors are each unique in B_7.
  A four-translation Hermitian one-block observable has second moment 8
  before the unpinned Fourier map but 12 afterwards. Norm and first moment
  still match. Thus checking only source-label injectivity would miss a
  concrete failure. The guarded pinned labels pass the corresponding
  exact character-Gram moment check. This computes sparse Fourier Gram
  entries by character orthogonality, not a full quantum gate simulation.
- A separate arithmetic ledger uses q=1000000007, ell=256, s=15,
  lambda=.42, tau=.43, b=40. Its worst-case affine dimension bound is 1920
  and 4301 pins suffice. This ledger DOES NOT construct matrices or execute
  a quantum circuit at those parameters. It is not a feasible experiment.

## Attempts To Falsify It

1. **False small-characteristic uniqueness:** explicitly disproved and
   replaced by the s*ceil(K/q) bound. Any counterexample to the pivot proof
   or exact rank bound kills the proposed decoder guarantee.
2. **Wrong dual code:** T is computed from residues and verified, not imported
   from scalar RS formulas. A failed G*T*G^T check stops the run.
3. **Pins chosen after seeing the solution:** forbidden. R must be independent
   of the input/source and interpolant. Changing this premise invalidates
   the source-weight failure bound.
4. **Hidden list enumeration:** absent. Dense linear systems and exact
   coordinate verification replace enumeration. This trades workspace,
   not an uncharged exponential search, for postprocessing time.
5. **Decoder only correct on likely support:** insufficient. Every competitor
   in B_(d+2) is included by the strict interpolation root bound.
6. **Classical dequantization:** this component IS classical. Its proposed
   quantum use is coherent label erasure in a separately specified
   one-pass source. It supplies no new classical access to the whole
   tables within small streaming space. Unrestricted storage changes
   the comparison and is not covered by the streaming lower bound.
7. **Circular use of a quantum advantage theorem:** the source/observable
   identities and classical lower bound are external premises, but the
   replacement decoder and its cost are independently specified. Review
   must check exactly this substitution rather than cite the original
   exponential decoder as an efficient one.
8. **Novelty:** not established. Search prior work on list decoding with
   side information, random coordinate restrictions, small-characteristic
   differential equations, and streaming DQI before making a novelty claim.
9. **Practical or Shor-scale relevance:** absent at present. The explicit
   stream can be enormous; this is a possible theoretical improvement in
   a restricted model. It merits review, not promotional framing.

## Next Decisive Work

First independently audit Sections 3--6, especially the small-characteristic
pivot count, R-independence, full B_(d+2) isolation and reversible workspace.
The native sparse neighbor-support moment check is now present, including
the radius-7 counterexample. A separate implementation or formal audit of
its general composition would be more useful than a larger dense simulation.
Search novelty before any theorem promotion. Do not respond by increasing
native q, adding seed campaigns, or building UI/registry wiring.
