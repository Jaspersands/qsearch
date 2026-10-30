# Research Decision: Zero Inverse Sum Is Not An Accepted Flat

2026-10-23. Exact counterexample and finite complete census. This does not
solve the native search problem, establish hardness, bound asymptotic
normality, or certify a quantum algorithm.

## The Scientific Question

The native relation is unchanged:

    H*x=0,  Tr(inv0(x_i))=b_i,

over F_(2^n), with the supplied distinct Vandermonde points, N=n^2,
K=floor(N/8), and fixed target bits. Existing subfield attacks cover broad
composite-degree cases. Prime-degree asymptotics and uniform sampling
remain unresolved. Existing scalar-normalized flat attacks already produce
FULL native finite witnesses, including n=17 and n=31; this pass does not
repeat those successes or mistake the harder residual interface for the
whole original search task.

A possible way to extend the classical attack is to find large affine
subsets of each acceptance set. If every coordinate has a certified
r-dimensional accepted flat, the restricted parity system has r*N binary
variables and n*K equations. The useful full-row-rank regime would require
r*N>=n*K, asymptotically r>=n/8. That inequality is only a necessary
dimension condition for universal syndrome coverage. It does not guarantee
rank, consistency, efficient flat construction, or uniform native sampling.

The existing `theorems/reciprocal_trace_flats.py` already constructs
logarithmic-dimensional flats and checks the resulting global rank. Do not
reimplement that routine as a new discovery. A new structural theorem,
not a longer finite search, would be needed to justify linear-dimensional
flats at large prime n.

## A Recent Paper Does Not Supply The Missing Implication

[Cheng, arXiv:2610.06445v1](https://arxiv.org/abs/2610.06445), submitted
2026-10-05, studies subspaces E satisfying

    S(E)=sum_(x in E, x!=0) x^-1=0.

Its announced counting/existence result concerns this vector sum. I have
not independently validated its full proof. Only the standard subspace-
polynomial identity below is used in our counterexample. The paper's
existence statement must not be imported as a constant-trace flat theorem.

Let L_E(X)=sum_(j=0..r) c_j X^(2^j), c_r=1, c_0!=0. Then

    S(E)=c_1/c_0.

For instance, expand the logarithmic derivative of L_E(X)/X at zero.
The condition c_1=0 removes the top Boolean-degree coefficient of the
VECTOR-valued inverse restricted to E. It does not force any given
Boolean component Tr(a/x) to be constant.

Likewise, [Carlet--Feukoua--Salagean, arXiv:2504.03307v2,
Section 3.2](https://arxiv.org/html/2504.03307v2#S3.SS2) concerns the degree
of the vectorial inverse under restriction. A high or slightly reduced
vectorial degree does not determine normality of one scalar component.
These distinctions prevent both an unjustified classical solver and an
unjustified hardness claim.

## The Exact Stronger Criterion

For a binary linear space E, put

    W_E = span_F2 {x^-1 : x in E, x!=0}.

For a nonzero scalar a, all points of E/a obey Tr(inv0(x))=0 precisely
when a lies in W_E's trace-pairing annihilator. Nondegeneracy of the
absolute trace pairing therefore gives the exact count

    #{nonzero a giving a trace-zero flat E/a} = 2^(n-dim W_E)-1.

Thus an inverse-span rank of n excludes EVERY scalar-rescaled trace-zero
flat from that E. This is stronger than checking that E itself has mixed
trace values. It does not exclude unrelated affine spaces or nonlinear
accepted families. A linear space includes zero and therefore cannot be
an all-one accepted flat under inv0(0)=0.

For a general affine space A avoiding zero, a similar necessary-and-
sufficient criterion uses the span of differences x^-1+x_0^-1:
constant trace b requires Tr(a*(x^-1+x_0^-1))=0 for all x in A, together
with Tr(a*x_0^-1)=b. We do not assert an efficient large-dimensional
construction or enumeration from this criterion.

## A Counterexample In Prime Degree Seven

Use F_128=F_2[z]/(z^7+z+1), with integers encoding polynomial coefficients
in little-endian binary. Let

    E = span_F2 {1, 18, 36, 8}.

The exact subspace polynomial, in this encoding, is

    L_E(X)=X^16 + 121*X^8 + 127*X^4 + 7*X.

The X^2 coefficient vanishes, so S(E)=0. However, the following seven
points and their inverses give a full-rank binary certificate:

    points:   1, 18,  19, 36, 37, 54, 55
    inverses: 1,  9, 112, 69, 22,  7, 62.

These seven inverse values are F_2-independent. Consequently W_E=F_128
and NO nonzero scalar a turns E/a into a trace-zero accepted flat. All
127 scalars also fail in direct predicate checks. The vectorial inverse
and its ordinary trace component both have restricted Boolean degree 3,
not degree zero.

The complete RREF census independently checks all 11,811 subspaces of
each relevant dimension:

| Dimension | Zero inverse sum | Their inverse-span ranks | Other subspaces |
| --- | ---: | --- | --- |
| 3 | 127 | All rank 6 | 7,112 rank 6; 4,572 rank 7 |
| 4 | 127 | All rank 7 | All 11,684 rank 7 |

In particular, EVERY four-dimensional linear subspace in this specific
field has full inverse span, whether or not its inverse sum vanishes.
This is a finite certified fact, not an asymptotic upper bound or a claim
about affine cosets. All field tables and exhaustive enumeration are
explicitly charged and capped at n<=8 in the diagnostic API.

## Rees Review And Research Triage

This pass first revisited the existing Rees proof and source contracts.
It found no new counterexample, which is NOT independent validation.
The recent [Morales, arXiv:2608.05321v2](https://arxiv.org/abs/2608.05321)
assumes a structured presentation for its quasi-Hamiltonian theorem.
That scope does not subsume arbitrary fixed-class nilpotent groups.
For example UT4(F_p), p>3, has class three but is not quasi-Hamiltonian:
the cyclic subgroups generated by I+E12 and I+E23 do not permute, as
their products in one order contain the cross-term E13 and in the other
order do not. Direct powers preserve this obstruction. This comparison
is not a novelty certificate; other literature or formulations may apply.

The review then tested the proposed connection from new inverse-sum
literature to the unresolved native classical attack. That implication
fails exactly, even after allowing a scalar normalization. No new solver
or speedup candidate should be registered from that connection.

## Next Action And Gemini Handoff

Keep the Rees result under independent proof/novelty review. Do not spend
another GPT pass extending scalar arithmetic test grids. The decisive
application work remains a costed native input bridge or a genuinely new
classical attack on the same inverse-trace relation.

For the latter, require either a CONSTRUCTIVE linear-dimension accepted
family with enough checked global syndrome rank, or an algorithm that
uses nonlinear families without reinstating an exponential search. A
zero inverse sum alone is not that evidence. Do not continue flat searches
by inertia, and do not infer hardness from this failed route.

After migration verification, Gemini may attach this receipt as a literature
scope counterexample and link the proof note. Do not overwrite earlier
native-success receipts, change candidate admission, or rerun a synthetic
oracle campaign. No moving source or staging files were changed here.
