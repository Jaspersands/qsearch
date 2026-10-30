# A Square-Root Classical Baseline For The Surface Receiver

2026-10-23. Proposed proof, exact controls and executable equality-only
algorithm. Independent review and prior-art comparison remain pending.

## Decision

The earlier random-transvection baseline is too weak for rank two. It
requires roughly p^2 queries to obtain hidden-plane vectors. The algorithm
here recovers the same hidden Lagrangian in Sp_4(F_p) with

    O(sqrt(p)) oracle calls,
    O(sqrt(p)) stored labels,

and polynomial-in-log(p) field arithmetic per call, deterministically.
Hash-table costs are standard expected costs; a balanced search tree adds
only a logarithmic factor if worst-case dictionary time is required.
Here p denotes the ODD PRIME FIELD SIZE of the receiver, i.e. the large
isogeny prime ell in the geometric source, NOT its curve characteristic.

This is still exponential in the input bit length. It does not dequantize
the proposed polynomial-time quantum receiver. It does remove an inflated
classical comparison. If the existing opaque-label lower-bound proof is
sound, its Omega(sqrt(p)) bound is now matched at constant error for rank
two. That lower bound still does not apply automatically to geometric labels.

This module is a baseline for the existing native source contract, not a
new toy-oracle candidate or a random-label search campaign. The included
oracles are exact proof controls. No geometric source has been run here.

## 1. Exact Access Contract

The algorithm receives ONLY p and a callable f on Sp_4(F_p) such that

    f(g)=f(h) iff gW=hW,

for one unknown Lagrangian plane W. These are LEFT stabilizer cosets. It
uses equality/hashing of labels, not their contents, and never receives W
or graph coefficients. A right-coset interface must first invert queries.
The implementation validates and counts every actual symplectic query,
including verification and repeated queries. The cost of evaluating f
itself is additional, not normalized to one unit of arithmetic.

All matrices in the implementation use paired coordinates
(x1,y1,x2,y2), with J=diag(J2,J2). For the proof it is convenient to group
the x and y coordinates and write

    D(A)=diag(A,A^(-T)),
    T_t=[[1,t],[0,1]],       R=diag(-1,1).

D(T_t R) is a symplectic involution with two nondegenerate two-dimensional
eigenspaces. It is not a determinant-minus-one map queried illegally in
one symplectic plane: its complete Levi embedding is in Sp_4.

## 2. Deterministic Meet-In-The-Middle Difference Cover

Put m=ceil(sqrt(p)), s=ceil(p/m), and use

    A={0,...,m-1},        B={0,m,2m,...,(s-1)m} mod p.

Every residue occurs as b-a: the integer intervals
[jm-m+1,jm] cover at least p consecutive integers. Thus if two functions
have a collision condition b-a=t for some hidden t, m+s evaluations find
a collision without a birthday-success heuristic. Store the first branch
in a dictionary and scan the second. No discrete logarithm is involved.

## 3. Find A Stabilizing Involution

For each of eight fixed public frames C in Sp_4 described below, use
f_C(g)=f(CgC^(-1)). Query the two branches

    f_C(D(T_a)),          f_C(D(T_b R)).

A collision gives D(T_(b-a) R) in the stabilizer of C^(-1)W. Conjugating
back produces a KNOWN involution stabilizing W. This inference is sound
even when the following graph-chart argument does not apply.

To guarantee finding one, suppose C^(-1)W is the graph
of a symmetric S=[[a,b],[b,c]] in grouped coordinates [S;I]. Its stabilizer
contains D(T_t R) exactly when

    (T_t R) S (T_t R)^T = S.

If c!=0, this holds at t=2b/c: the off-diagonal equation is tc=2b, and
the remaining quadratic equation is then automatic. No algorithm step
is supplied b or c; this calculation proves a collision exists.

Start with the four frames that independently apply either I or the
rotation [[0,-1],[1,0]] on each coordinate symplectic plane. At least one
gives an invertible bottom projection of C^(-1)W. Indeed, in paired
coordinates the six Plucker minors of a basis satisfy

    P12+P34=0,
    P12*P34-P13*P24+P14*P23=0.

If all four cross minors vanished, these identities would force P12 and
P34 to vanish too, contradicting rank two. The four frames select all
four cross minors as bottom projections, up to sign.

For each frame C, also try C'=C*T_(-1) where T_(-1) acts only on the
second coordinate symplectic plane. Then C'^(-1)W has graph matrix
S+diag(0,1), so one of c and c+1 is nonzero. These eight known frames
therefore guarantee a collision. No sampling or retry probability enters
the solver. Bad-chart inputs can also succeed without compromising soundness.

A deliberately truncated chart budget can return ABORT, not a negative
result about the kernel or a fabricated recovery. The uniform symplectic
sampler retained in this module is used only to generate test inputs.

## 4. Split Into Two Hidden Lines

Let h be the recovered involution, with eigenspaces V_- and V_+.
They are orthogonal: <v_-,v_+>=-<v_-,v_+>, and p is odd. Nondegeneracy
of the ambient form makes each eigenplane symplectic. Since h stabilizes W,

    W=(W intersect V_-) direct_sum (W intersect V_+).

Each intersection has dimension at most one by isotropy. Their dimensions
sum to two, so both are lines. Compute a public symplectic basis of each
eigenplane. In the resulting known coordinates, the oracle restricted to
Sp_2 acting on one plane hides that line; the other line is unchanged.

## 5. Recover Each Line In Square-Root Queries

First compare the label of the plane's T_1 with f(I). Equality means the
line is the unique fixed projective point infinity, spanned by (1,0).
Otherwise write it as span(z,1).

For p>3 let A0=diag(2,2^(-1)), which has determinant one. Compare

    f(T_a on this plane),      f(T_b A0 on this plane).

Their projective images are z+a and 4z+b. A collision therefore gives

    z=(a-b)/3.

The difference cover guarantees a collision. All queries are symplectic
and fix the other eigenplane. The special prime p=3 needs no division by
3: enumerate its four projective points with the transvection test below.
That is a constant-size exception, not an exhaustive large-p algorithm.

## 6. Final Certificate

For a nonzero v, the symplectic transvection tau_v=I+v v^T J satisfies

    tau_v W=W iff v in W.

If <v,W>=0 then v lies in W^perp=W. Otherwise some w in W has nonzero
pairing with v, so invariance implies v is a scalar multiple of
(tau_v-I)w in W. The reverse direction is immediate.

The two reconstructed independent vectors are checked using this test
against the ORIGINAL oracle. If both pass, their span is exactly W under
the source promise. This certificate uses two new calls, with f(I) cached.
It is a FIELD argument, not a claim about arbitrary lifted ring modules.

## 7. Accounting And Adversarial Scope

Let B=m+ceil(p/m). With a chart budget 1<=r<=8, the implementation
charges no more than

    r B + 2 max(B+1,4) + 3

queries. The default r=8 is a complete deterministic cover. The dictionary has at most m entries at
one time. Its labels have the source's actual output width; that width and
geometric evaluation cost must be multiplied into the memory/time budget.

Attempts to break the construction include p=3, a hidden line at infinity,
bad graph charts, all 40 Lagrangians over F_3, arbitrary fresh opaque labels,
and budget exhaustion. Every successful return is checked against the
reference subspace in tests. The production solver receives no reference
subspace. Passing these controls is not a proof of the asymptotic theorem.

The principal limitations are:

- This is not polynomial in log p; do not record DEQUANTIZED.
- The bound is for rank two at an odd prime, not arbitrary rank or rings.
- A malformed/noninjective source oracle can defeat the mathematical
  promise; the final certificate does not certify that whole promise.
- Real geometric labels may reveal much more than equality. This baseline
  deliberately ignores that information, so it cannot establish hardness
  of the explicit weak-isogeny input.
- Meet-in-the-middle and affine hidden-shift ideas are standard. This is a
  project-specific composition; novelty is unverified. Related classical
  Borel methods appear in [Chen et al., Section 3.1](https://arxiv.org/html/2305.19897).
  We do not claim the entire baseline as a new discovery.

## Research Consequence

Use this baseline, rather than random transvection sampling, in any future
surface-source comparison. The next decisive classical attack should exploit
the geometry or the actual weak input, because the equality-only query model
already has a square-root upper bound matching the proposed lower bound.
Do not spend another pass merely benchmarking larger opaque instances.
