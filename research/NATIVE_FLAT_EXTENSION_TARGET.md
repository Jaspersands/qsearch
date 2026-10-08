# Next Mathematical Target: Costed Native Flat Extension

LOCAL CONDITIONAL DERIVATION / REVIEW PENDING. The EXACT supplied-certificate
verifier and classical extractor are now implemented in
`theorems/ternary_flat_character_certificate.py`; read
`research/TERNARY_FLAT_CHARACTER_CERTIFICATE.md`. The argument below remains
the original specification. A completion solver and robust native approximate
certificate are NOT implemented. It is not an accepted algorithm candidate.

## Why This Target

`TERNARY_OBSERVABLE_MOMENT_LIFT.md` gives exact higher-rank native PSD
matrices satisfying ALL sparse translation equalities without a positive
distribution over secrets. Its observable-basis repair proves tightness of
a particular diagnostic, not native noisy recovery. The next representation
must certify a character distribution, not just rank, fit or PSD.

The primary [Laurent--Mourrain paper](https://arxiv.org/abs/0812.2563) studies
flat extensions on monomials and their border. We do not silently apply its
hypotheses here. The following group-specific argument uses Gram translation
identities directly and still needs independent review and implementation.

## Exact Finite Certificate

Let G=Z_q^n, q=3^r. Let V contain0 and every frequency used by the native
objective/current matrix. A public unit difference basis d_1,...,d_n
identifies G; a deficient basis remains UNKNOWN here.

Compile an offset set S containing0, each d_i, each d_i+d_j, and every
operand/result in binary doubling/accumulation for q*d_i=0 and for every
f in V from its canonical coefficients f*D^-1 moduloq. Keep INTEGER operation
traces, not just endpoints. Then

    |S|=O(n^2+(|V|+1)*n*log q).

Use the frequency-deduplicated set W=V+S, with size<=|V|*|S|. Its dense matrix
and complete equal-difference audit have O(|W|^2) entries; this enlargement
must be charged. Require original V-block retention and EXACT:

- Hermitian PSD M_W, diagonal1.
- Equality of ALL entries having the same actual G difference.
- rank(M_W)=rank(M_V)=R, not an eigenvalue-threshold estimate.

This is rank FLATNESS, not arbitrary low rank. Classically finding such a
completion can be nonconvex/hard; polynomial size grants no solver.

## Conditional Representation Proof

Use the usual inner product conjugate-linear in its first argument, with
M_uv=<g_v,g_u>. Flatness puts every g_w in H=span{g_v:v in V},
dim H=R. For s in S define U_s*g_v=g_(v+s). Full translation gives the same
base Gram matrix after shifting: the map respects all dependencies and is
isometric. Its image spans H, because the shifted base Gram rank isR, so
U_s is unitary and U_0=I.

Whenever s,t,s+t are in S, for v,z in V translation gives

    <U_s*g_z,g_(v+s+t)>=<g_z,g_(v+t)>.

The base vectors span H, hence U_s^* g_(v+s+t)=g_(v+t)=U_t*g_v and
U_s*U_t=U_(s+t). Generator pair sums certify commutation; binary integer
q-loops certify U_(d_i)^q=I. Each row reconstruction certifies
U_f=product_i U_(d_i)^(coefficient_i(f)) and g_f=U_f*g_0.
These facts need the specified translates; anchored circuit identities alone
do not suffice.

Common character eigenspaces of these commuting finite-order unitaries give
nonnegative weights p_s summing to1 with

    M_uv=sum_s p_s*chi_q((u-v).s), u,v in V.

At mostR characters have positive mass. The retained native partition
counterexamples cannot admit this certificate: unit-basis pair moments1
force secret0, inconsistent with anchors0. A verifier must reject them,
not replace their original block or reinterpret rank failure as success.

## Extraction And Dequantization

Exact algebraic Gram/basis operations reconstruct the R-dimensional U_(d_i).
Use an independent base Gram block as the positive inner-product metric;
matrix inversion recovers shifted coordinates without introducing arbitrary
square-root field extensions for an explicit Euclidean Gram factor.
Common eigenspaces can be refined one generator at a time using

    P_(i,t)=(1/q)*sum_(k=0)^(q-1) chi_q(-t*k)*U_(d_i)^k.

At every stage at mostR nonzero orthogonal branches survive, not q^n.
Scanning q eigenvalues per generator is polynomial in n,q,R and represented
arithmetic costs, NOT in log q. Joint eigenvalue tuples recover secret
coordinates using D^-1; weights are squared projections of g_0. Exact zero
and normalization checks, coefficient bit heights and basis conditioning
cannot be hidden. The cyclotomic field degree at q=3^r is2q/3. The stated
extractor is potentially polynomial at q=poly(n), not at exponentialq.

A LINEAR represented objective is the weighted average of extracted
character scores. Some support character therefore attains that objective
value or better. Efficient CLASSICAL construction of the exact flat completion
would give a classical decoder for that score, checked against independent
held-out native samples, not a quantum advantage. Native harmonic score is
linear; full product/log likelihood is not magically the same objective.
Quantum state supply also does not grant a free classical moment matrix:
charge tomography/completion and distinguish the access models.

## Try To Falsify It

Flat completion may be inaccessible under native noise. A positive posterior
on all q^n secrets generally has full rank on the full group. Concentration
may give small EFFECTIVE rank but does not imply exact flatness. Tiny
eigenvalues cannot be deleted without a certified perturbation and held-out
error law. The existing saturation bound is often vacuous at noise harmonic
1/3; its residual gate is NOT an approximate flat-extension theorem.

Even polynomial W can be much more costly than the records. Solver
convergence or an empirical gap is not an extraction proof. The high-upside
question is whether native source structure permits a recoverable small-rank
representation or a quantum transform without classical matrix construction.
This certificate is a falsifier/dequantization gate, not that answer.

## Next Implementation Order

1. Compile S,W and integer traces with whole-object caps; retain the original
   block and audit complete actual differences.
2. Verify exact algebraic rank/isometries on supplied certificates. Test honest
   mixtures and the retained native nonextension falsifiers.
3. Reconstruct commuting finite-order translations and extract at mostR
   genuine secrets without q^n enumeration; charge q/field/bit costs.
4. Only then study native-source completion or approximate certificates.
   Reuse native noise and held-out gates; do not rebuild identifiability.

Steps1-3 now have an exact implementation, native-label calibration and
independent cyclotomic checks; this does not supply step4 or independent
mathematical review. `research/TERNARY_TRANSLATION_STABILITY.md` now retains
both a known topological falsifier for naive approximate operator rounding
and a conditional q-dependent pair repair. Its many-generator precision
bound does not establish a native approximate decoder. Gemini owns routine
CLI/registry wiring and production validation.
