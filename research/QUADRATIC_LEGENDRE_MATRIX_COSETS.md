# Quadratic Legendre matrix cosets: a paid source and a failed readout

5 November 2026. Independent adversarial review accepted the statements
below, including the source, subgroup counts and postprocessing. The source
reduction below is constructive. The tested additive-Fourier receiver is
refuted exactly. No polynomial-time reconstruction, hardness, novelty or
separation claim follows.

## Selection and hypothesis

The question remains recovery of a hidden monic irreducible quadratic
f(X)=X^2+bX+c over growing F_p from ORIGINAL bit-output coherent queries
g(x)=chi(f(x)); input size log p, output b,c with fresh verification. The
phase-only extension of the earlier subexponential algorithm remains valid,
but this new projective source is stated only for the original bit oracle.
No extension-field queries or values of f are supplied.

The concrete proposal was to fingerprint the projective coloring, obtain
cosets of its matrix stabilizer, and use additive matrix Fourier sampling
to recover the quadratic form. Its intended cost was poly(log p), against
the retained expected O(sqrt(p)polylog p) classical chosen-query baseline.
The latter already ran on six fixed keys; this unchanged native input
does not justify rerunning it. The moment baseline and the reviewed
2^O(sqrt(log p)) quantum composition also remain in force.

Corpus been-tried and baselines queries for quadratic Legendre/PGL2 hidden
nonsplit tori returned no matching solved receiver; this is no evidence of
hardness or novelty. The relevant primary comparison is
[Ivanyos, Sections 3.1-3.2](https://arxiv.org/pdf/1105.4416): its additive
matrix Fourier algorithm uses a BOREL subgroup and extracts a fixed kernel
from singular matrices. Its proof does not apply to the subgroup here.
The full source is saved under audits/sources/legendre_prf/.

An independent alternative was the fixed-F1019 AG low-degree parity
selector. The existing contract needs n=2e-11, below g=5e+1 by3e+12;
ordinary RR reduction to degree g does not meet it. The actual genus-six
seed has Kummer rank12 and Schoof margin4, proving an infinite split
tower. Neither that theorem nor the arbitrary successive quadratic choices
bound full rational r2=dim Jac(F1019)/2Jac by C log g. The existing marked-
point obstruction persists. No new selector or rank theorem emerged, so
no higher-level backend or finite rank sweep is warranted. Sources:
AG_SMALL_PARITY_SELECTOR.md; bundles/small-prime-tower-2026-10-27/RESULT.md;
bundles/constructive-tower-review-2026-10-27/REVIEW.md (the last still names
the earlier F100003 source, not an executed F1019 rank computation).

For the matrix proposal, obligations are exact subgroup fibers, charged
coherent homogeneous queries, global fingerprint error, and an informative
efficient readout after averaging the random coset. The last obligation
has a decisive negative answer for the specified measurement.

## Paid native coset source

Assume p>=41 and set Q(u,v)=u^2+buv+cv^2, an anisotropic binary form.
The value h([u:v])=chi(Q(u,v)) is well-defined on P^1(F_p). For v!=0 it
equals g(u/v); at infinity it equals1. A homogeneous bit query needs ONE
native XOR query: compute the finite affine argument reversibly, route
the data target into an auxiliary |+> register on the infinity branch,
query unconditionally, then undo routing and arithmetic. The auxiliary
returns clean because XOR fixes |+>. There is no controlled black-box call.

Let G=GL_2(F_p), with order D=p(p-1)^2(p+1), and let

    H_Q={h in G : Q(hv)=lambda Q(v) for some square lambda in F_p^*}.

This is the full stabilizer of the coloring for p>=41. Indeed, two
nonproportional anisotropic binary quadratics have a squarefree quartic
product on the finite affine chart. The ordinary Weil bound, with the
extra infinity term, bounds their projective correlation by3sqrt(p)+1.
Consequently their agreement fraction is at most

    rho=(1+(3sqrt(p)+1)/(p+1))/2 <=3/4.

Proportional forms differ either by a square, giving identical colorings,
or by a nonsquare, giving opposite colorings. Thus there are no accidental
additional stabilizers in this range. Small primes are outside this source
statement and can be handled by constant-size direct reconstruction.

Identify the quadratic space with F_(p^2), with Q a scalar multiple of
the norm. Its similarities are z->alpha z and z->alpha conjugate(z).
Preserving the coloring requires Norm(alpha) square. Therefore

    |H_Q|=p^2-1;    |(H_Q)_v|=2 for every v!=0.

The second identity also follows explicitly: the only stabilizers of v
are identity and z->(v/conjugate(v))conjugate(z). All these descriptions
are proofs, not supplied secret coordinates or preprocessing advice.

Choose L independent uniform PUBLIC points v_j in P^1(F_p) and define
F(A)=(h(A v_j))_j. Equal full functions occur exactly on right cosets H_Q A.
There are D/|H_Q|=p(p-1) such functions. A union bound shows that the ONE
fixed fingerprint list separates every coset except with probability
at most p^4(3/4)^L. Thus L=O(log p+log(1/delta)) gives global error delta.
This is not a per-query independence assertion.

Query F(A^-1) to obtain left cosets A H_Q. Reversible field arithmetic,
uniform GL2 preparation (reject singular matrices with constant success),
and L homogeneous queries have expected polynomial-logarithmic cost.
For bounded execution, cap preparation attempts and charge its ABORT
probability; the success branch remains uniform. Workspace,
output bits and circuit precision are charged. Conditional on the good
list, discarding the fingerprint register gives the exact standard coset
density operator. Approximate gate errors are budgeted separately.

If an efficient HSP algorithm actually supplied generators for H_Q, b,c
could be recovered by polynomial-logarithmic linear algebra. A non-scalar
commutator belongs to its norm-one rotation subgroup. Such a commutator
occurs among generator pairs: if all were scalar, H_Q would have class at
most2, whereas its derived subgroup is cyclic of order(p+1)/2>2 and a
reflection inverts it. The FULL norm-one torus has order p+1. The
non-scalar commutator has eigenvalues different from
plus/minus1, so its invariant symmetric forms form the single line F_p Q.
Solve R^T S R=S in the three entries of S and normalize S_11=1 to obtain
b=2S_12,c=S_22. This is a paid POSTPROCESSING implication, not an HSP solver.

## Exact additive-Fourier falsifier

Discard the fingerprint register and take independent uniform cosets.
For left cosets the density matrix is

    rho_H=(1/D) sum_(x in G,h in H) |x><x h|.

Apply the additive Fourier transform of the FOUR matrix entries, with
kernel p^-2 exp(2pi i tr(Y^T X)/p), and measure the entire matrix Y. Define

    S(T)=sum_(x in G) exp(2pi i tr(Tx)/p).

By invertible row/column changes its value depends only on rank(T):

    S_0=D,    S_1=-p(p-1),    S_2=p.

For completeness, S_1 follows by counting the first diagonal entry:
p(p-1)^2 matrices give zero, and p^2(p-1) give each specified nonzero
entry. For S_2, sum over ordered independent columns u,v. For u on the
first-coordinate line, the v sum of exp(2pi i v_2/p) is -p and the sum
of exp(2pi i u_1/p) over nonzero u is -1; for every other u the v sum is0.
The result is p. This fixes both signs without a character-table oracle.

The measured probability is

    Pr(Y)= [sum_(h in H) S((I-h)Y^T)]/(p^4 D).

For rank(Y)=1, write Y^T=u v^T with u,v nonzero. Exactly two elements h
fix u, giving rank0; all other |H|-2 give rank1. For invertible Y, h=I
gives rank0, exactly p+1 elements give rank1, and p^2-p-3 give rank2.
The rank1 count follows by counting (h,v) with h!=I, v!=0 and hv=v:
there are p^2-1 pairs, and each rank1 element fixes p-1 nonzero vectors.
Thus, for EACH matrix of the specified rank,

    rank0: Pr(Y)=(p^2-1)/p^4;
    rank1: Pr(Y)=[2D-p(p-1)(p^2-3)]/(p^4 D);
    rank2: Pr(Y)=[D-p^2-2p]/(p^4 D).

There are respectively1, (p-1)(p+1)^2, and D such matrices; the total
probability is1: the total masses are respectively (p^2-1)/p^4,
(p+1)(p^2+1)/p^4, and1-1/p-2/p^2-1/p^3. Every expression is independent
of b,c, including the
distribution of the full matrix entries. Arbitrarily many independent
samples of this specified readout therefore contain no secret information
on the good-fingerprint event. Finite fingerprint errors do not turn this
into an efficient robust reconstruction mechanism.

This directly refutes the proposed transfer of the Borel additive-Fourier
receiver. It does NOT refute algorithms retaining the oracle label,
coherent Fourier outputs, a nonabelian GL2 transform, a nonuniform input,
or collective measurements. No general native-oracle lower bound follows.

## Decision and next experiment

Park this receiver. The paid matrix-coset reduction can be reused only
when a different explicit recovery operation warrants it. The earlier
native subexponential quantum and expected-sqrt(p) classical bounds stand.
No matrix scan, HSP framework, larger simulation or registry promotion is
needed to establish this exact falsifier.

Before another Legendre receiver pass, independently compare motivated
directions and require a concrete new operation. For a proposed matrix
receiver, the first acceptance test must exhibit a secret-dependent
observable under the actual random-coset source, with retained labels and
workspace explicitly specified, and a poly(log p) implementation. An
observable proved independent as above fails before implementation.
