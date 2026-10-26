# Central-Only Regular Source For The Nonlinear Receiver

EXTENSION UNDER REVIEW (2026-10-21): CLASS_THREE_MONOMIAL_FULL_JET.md
keeps an additional Fourier frequency quantum and retains the complete
Taylor jet. It gives a proposed class-three-normal translation/phase source
and GL combiner. The Weyl formulas and costs in this note remain specific
to its class-two-normal variant; the new weighted and residual degrees are
higher. Neither route is an independently validated full HSP algorithm.

2026-10-21. Constructive simplification UNDER REVIEW, not an admitted
algorithm, independent proof, novelty certificate or useful speedup.
This is now the preferred SOURCE route for NONLINEAR_JET_HSP_RECEIVER.md.
The old irreducible route remains a valid comparison and regression target;
it is not a necessary dependency of this replacement.

## 1. Question And Scope

Can the same Taylor-jet receiver use the normal group's central Fourier
transform alone? Yes at the written-derivation level: retain the entire
noncentral regular carrier instead of resolving irreducibles and tracing
their multiplicity rows. This removes variable radical dimensions, radical
characters, nonzero-label rejection, the selected-label equivariance
argument, and artificial mixed padding. It does not remove coherent oracle
access, the fixed-degree SDE theorem, public symplectic alignment, weighted
phase erasure, the second erasure, or the need for a useful application.

Use the same explicit Lie-coordinate input, fixed class c, class-two
derived algebra N, p>max(c,2(c-2)), and initially H intersect N=1.
Write N=W x Z in BCH coordinates, Z=Z(N), with multiplication

```
(v,c)*(v',c')=(v+v',c+c'+beta(v,v')/2),
B_lambda(v,v')=lambda(beta(v,v')).
```

The direct-source calculation works for any central Z containing [N,N].
However, choosing a smaller Z does NOT inherit the same bound
deg Q_W<=c-2. Retain Z=Z(N) for the stated whole-receiver scope. For
abelian N use the existing scalar route rather than claim a better bound
from this positive-width implementation.

Regular representations, central Fourier transforms and Weyl operators
are standard harmonic analysis, not inventions of this project. Compare
[Krovi--Roetteler](https://arxiv.org/abs/0810.3695) and the known
[nil-2 HSP algorithm](https://arxiv.org/abs/0707.1260). The contribution
under examination is their simpler interface to the proposed higher-class
Taylor-jet receiver. No search result certifies novelty of that receiver.

## 2. Direct Source Derivation, Without An Irrep Formula

Let the common proof-only potential be g(q)=(a(q),b(q)) in N. Its degree
and section-word properties are the same as before; g is NOT evaluated
by the receiver. The actual ordinary mixed coset kernel in normal-first
coordinates has support q'-q in U and n'=n*g(q)^(-1)*g(q'). Writing
n=(x,c), Delta=a(q')-a(q), the latter condition is

```
x'=x+Delta,
c'-c=b(q')-b(q)-beta(a(q),a(q'))/2+beta(x,Delta)/2.
```

Apply negative Fourier ONLY to c, measure lambda, and apply the PUBLIC
negation t=-x on the remaining W register. Keep every lambda, including
zero. There is no radical readout or representation-row trace. Directly
summing c,c' gives the unnormalized block

```
p^(-(m+w+z)) [q'-q in U] [t+a(q)=t'+a(q')]
 * omega^(lambda(b(q')-b(q)-beta(a(q),a(q'))/2
                  +beta(a(q')-a(q),t)/2)).
```

Its trace is p^(-z). After dividing by that probability it is

```
(p^m*p^w)^(-1) [q'-q in U] W_lambda(g(q))^dagger W_lambda(g(q')),
W_lambda(v,c)|t> = omega^(lambda(c)+beta_lambda(v,t)/2)|t+v>.
```

Each W_lambda is an actual unitary representation: multiplying two such
operators gives the BCH half-bracket phase. It is generally REDUCIBLE.
Completeness comes from the explicit unitary I_W tensor F_Z followed by
coordinate negation, not from Schur orthogonality or summing d^2 weights.
Using d=p^w in an irrep-sector d^2/|N| formula is invalid and can exceed
one. The direct physical outcome probability is p^(-z), independent of
lambda and rank, including lambda=0.

This source still uses fresh ordinary queries and traces the hiding-output
register. Conditional single-coset input is not substituted. Retaining the
carrier is essential: tracing it can erase all information about U in a
perfectly normalized example. There is no classical dequantization merely
because the public gauge is monomial; its unknown coefficients and the
coherent oracle were not supplied to a classical learner.

## 3. Injective Weyl Embedding And Weaker Cancellation

In the existing convention [u,v]=u_Z.v_X-u_X.v_Z, define

```
D_lambda v = (v,-B_lambda*v/2).
```

Then D_lambda^T Omega D_lambda=B_lambda and D_lambda is injective for
EVERY lambda because its X block is I_W. Its symmetric-Weyl half-phase
v.(-B_lambda*v/2)/2 is zero. Thus
`W_lambda(v,c)=omega^(lambda(c))*D(D_lambda v)` exactly.
No common-radical, maximal-rank or nonzero-label condition is needed for
this algebraic interface. Each source retains w field registers, not
half the rank of B_lambda. This can use more carrier registers than the
irrep version; it is still polynomial and these registers already exist
in the input. They are not free auxiliary purifications.

Set D=c-2 and use the same retained Taylor jet F with J coordinates.
After the fresh quotient shear, the top and retained displacement maps are

```
K_i=s_i^D D_lambda_i,
J_i=[s_i^k Y_i^alpha D_lambda_i]_(alpha,k).
```

For K isotropic, only `sum_i s_i^(2D) B_lambda_i=0` is required.
Let b=dim[N,N]. Evaluate each lambda on a public basis of the image of
beta. Solving degree-2D equations in these b coordinates is sufficient;
the full z-component label relation is unnecessarily strong here.
Central characters annihilating [N,N] need not cancel. Their contribution
to psi remains and is paid by the generic weighted degree bound
e=max(c,2D-1). Do not reuse the old class-four cubic-only resource formula.

Use a_(2D)(b) inputs per relation block; for b=0 choose one active input
without solving an equation. The implemented checker verifies the actual
commutator-form relation, not the stronger whole-label condition. It is
not an implementation of the general SDE solver.

## 4. Scalar Polynomial-Evaluation Rank, Conditional On Labels

Put ell=1+J/w=binom(m+D,m+1). Each active source contributes the scalar row

```
Phi_i=(s_i^D, (s_i^k*Y_i^alpha)_(alpha,k)).
```

Up to row/column order, the entire X block of [K J] is Phi tensor I_W.
Thus rank(Phi)=ell certifies rank[K J]=w*ell. It also implies the
physical carrier width R=(number of active inputs)*w is at least w+J.
The existing deterministic symplectic extension therefore needs NO mixed
padding for this sufficient design. It gives the same canonical nonlinear
jet, so the subsequent monomial contraction and two erasures are unchanged.

Divide a row by its nonzero s. Its entries are ALL monomials of total
degree <=D-1 in the m+1 variables (s,Y), in a fixed order. Now condition
on an arbitrary complete prior record of labels and valid witnesses.
Choose a nonzero coordinate in each disjoint block before fresh draws.
Multiply that block's witness by an independent uniform tau in F_p*.
Its selected s is uniform nonzero regardless of how labels biased the
witness. The new Y tuple is independent uniform by the matrix shear law.
For any fixed nonzero scalar coefficient vector, Schwartz--Zippel gives

```
Pr[selected row annihilates vector | prior labels/witnesses]
 <= (D-1)/(p-1).
```

With B independent rescalings and fresh outcomes, union-bound the scalar
kernel vectors, not w*ell-dimensional vectors:

```
Pr[rank Phi<ell | arbitrary prior labels/witnesses]
 <= (p^ell-1)*((D-1)/(p-1))^B,
B=(ell+1)*bit_length(p)+2  ==> bound <=1/(4p).
```

This removes the GL_z-equivariant label selector and common-radical
hyperplane argument. The witness can be any public verified choice made
before tau/Y. It need not come from canonical row space. It still cannot
inspect hidden quantum states, select after seeing Y, share rescalings,
reuse consumed sources or condition the bound on rank acceptance. The
bound holds conditional on the labels/witnesses, NOT on future tau or Y.
For a partial SDE solver one still needs a separate bounded success law;
validating one witness does not prove an efficient source supply.

## 5. Composition And Cost Changes

Use the Section 10 CQ induction of NONLINEAR_JET_HSP_RECEIVER.md, replacing
only the matrix-leaf procedure and its sufficient rank condition:

- Take T=B*a_(2D)(b) fresh queries per attempt. Keep all central labels.
  There is no zero-label rejection and no r_lambda multiplier.
- Collect disjoint relation blocks before the fresh block rescalings and
  common-q shear. Check the PUBLIC scalar feature rank before alignment.
- A regular source uses w carrier qudits. Compute D_lambda directly;
  there is no alternating-form decomposition, radical character, variable
  irrep layout, row trace, or artificial maximally mixed padding.
- Keep the same scalar parameter basis Q_W,Q_Z and their quadratic lift.
  The shared symbolic contraction checks the COMPLETE aligned X map
  against the common Taylor jet. Do not infer that identity from degree.

At most r_tau=ceil(log_p(8B)) field draws per multiplier give total
multiplier exhaustion <=1/8 per trial. Together with rank failure,
an ideal trial fails with probability <=1/8+1/(4p)<1/2. With the previous
M matrix leaves and R_trials=ceil(log_2(4M/eta)), the new source bound is

```
Q_image <= M*R_trials*T.
```

The same binary-sampling truncation, joint-instrument error and final
spanning bounds apply. Source/register/gate/SDE costs remain polynomial
only for fixed c and can be enormous. No practical speedup, native-gate
bound or improved asymptotic whole-algorithm exponent is asserted.

## 6. What The Implementation Actually Checks

`theorems/central_regular_jet.py` provides the fixed-width Weyl map,
scalar feature matrix, sufficient-rank geometry, conditional bound and
public symbolic scalar compiler. It reuses deterministic alignment and
the scalar-contraction helper factored from nonlinear_jet_erasure.py.
No H, pi, Q coefficients, oracle evaluator or generic SDE solver is input.
It prepares no quantum source and cannot certify consumed-copy ownership.

`tests/test_central_regular_jet.py` checks actual ordinary group cosets
against the COMPLETE central-only transform and every outcome, including
zero. Wrong sign and invalid irrep normalization have explicit controls.
Exact maps, Gram identities, cubic alignment and scalar phase tables are
checked at small primes and a 127-bit prime. A label supported outside
[N,N] verifies that central phase is retained, not silently cancelled.
Fixed-scale rank deficiency and malformed relations/maps are rejected.
These are proof falsifiers, not new oracle candidate problems.

No new Lean theorem is supplied. MatrixBatchShear and NonlinearJetChannel
can consume the resulting gauge/source at their abstract interfaces, but
the direct central transform has not been composed with them in Lean.

## 7. The Next Genuine Obstruction

This does NOT extend the receiver to class-three derived groups. In
UT_7(F_p), let x=I+E_13, y=I+E_35, z=I+E_57. All lie in G', while
`[x,y]=I+E_15` and `[[x,y],z]=I+E_17!=I` (using xyx^-1y^-1).
Thus [x,y] is noncentral in N=G'. After transforming only Z(N), its
regular action still permutes N/Z(N) nontrivially. A Weyl representation
has scalar commutators, so the unchanged constant-translation interface
cannot represent these actions. The exact matrix control checks this
boundary; it is not a no-go theorem for other algorithms.

The next constructive question is whether the resulting unknown-dependent
affine/polynomial PERMUTATIONS can be aligned without erasing their hidden
support. Another regular-source normalization lemma does not answer it.
Also keep the application gap explicit: sparse explicit-object symmetry
families remain subject to the previously established classical attacks.
