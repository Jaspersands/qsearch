# Exact finite-group saturation and actual-point identities

2026-11-13. Focused independent review of the final sections of
`LOCAL_KUMMER_NATIVE_END_TO_END.md`, after current STATE,
`LOCAL_HALVING_SATURATION.md`, and the retained finite-quotient lemma in
`LOCAL_SATURATION_FINITE_PRECISION.md`. No Git, network, external API,
implementation or sweep. Commands used `/opt/anaconda3/bin/python`.

## Verdict

ACCEPT the finite-group initialization, exact index-two updates and complete-
image stopping rule, conditional on the candidate's certified point/label/
half subroutines. These claims do not need an equality oracle on J(Q2).

For a completely explicit operation clock, retain a triangular presentation
instead of repeatedly changing the point generators by HNF/SNF. Every
relation has coefficients in {-1,0,2}, and every selected halving input is
a 0/1 sum of existing generators. This schedule needs at most

    kappa*q + kappa*(kappa-1)/2

binary-addition/ONE-HALF calls, where q=g+t<=3g. The proposed quartic cap
is therefore safe for this schedule after replacing the UNKNOWN exact kappa
by its COMPUTABLE native upper bound K:

    T0=4(K+3g+10)^4.                                   (1)

The review does not certify the separate local-field backend or the
operation-by-operation numerical DAG refinement losses. It does certify
which exact identities that DAG must preserve and how many group calls are
needed. Parent owns shared notes.

## 1. Independent initialization of A[2]

Let G be the maximal pro-2 subgroup of J(Q2). Let P_1,...,P_g be the
independently proved formal seeds, and L their closed Z2 span. Its nonzero
logarithmic determinant proves that L is free of rank g and torsion-free.
Keep E=2L fixed for the entire run, and put

    A=G/E,       T=G[2],       t=dim_F2 T,       q=g+t.

For x in G, the condition `2x in E` means `2x=2l` for some l in L.
Thus x-l lies in T. Since L meets T trivially,

    A[2]=(L/E) direct-sum T.                           (2)

The g seed classes are a basis of L/E. If a combination of seed classes
and rational 2-torsion lies in E, its torsion part lies in L and is zero;
then seed independence modulo 2L forces all seed coefficients to vanish.
This establishes independence without using any Kummer labels. Initial
labels are allowed to be zero.

For completeness, the factor-divisor initialization of T is independent too.
If f has r irreducible local factors, their branch classes have the single
total-sum relation, and t=r-1. The odd degree makes the branch augmentation
quotient split equivariantly, so passing to Galois invariants introduces no
extra rational 2-torsion. One may omit any one factor. Equivalently, a
nonempty proper union of factor roots, or its complement, has degree between
1 and g; its pair [a,0] is a nonzero reduced 2-torsion class. Thus no proper
nonempty subset of the r factor classes sums to zero. Replacing a factor
by its complement preserves its 2-torsion class and keeps degree <=g.

The native local-factor computation and its finite certificates are a
separate backend obligation. Once supplied by that computation, these
branch points and the seeds initialize

    B_0=A[2] ~= (Z/2)^q

with its exact elementary-2 presentation. No basis of the unknown A is used.

All actual represented points remain in G. The seeds, rational 2-torsion
and shifts in E lie there. If `2Q in G`, then Q is also in G, because the
quotient J(Q2)/G has odd order and no nonzero element killed by two.

## 2. Every selected vector produces an exact doubling

Kummer descends to a map

    lambda:A -> L_algebra^*/L_algebra^{*2}

whose kernel is exactly 2A. Here `L_algebra=Q2[x]/f` is distinct from the
seed lattice L. Indeed E is contained in 2G, so `A/2A=G/2G`, and the
ordinary local Kummer map is injective on that quotient. Its dimension is
q=g+t, equivalently the dimension of A[2].

Suppose B is an exactly presented subgroup of A containing A[2]. Then
`B[2]=A[2]`, so `dim_F2(B/2B)=q`. If its label rank is below q, there is
a NONZERO CLASS h in B/2B with zero label. For any q_new in A satisfying

    2q_new=h in A,

one has q_new outside B; otherwise h would belong to 2B. Its class in A/B
has order exactly two. Therefore

    [B+<q_new>:B]=2.                                  (3)

Any two quotient halves differ by A[2], which is already in B. The enlarged
subgroup is independent of the chosen half.

The abstract presentation obtained by adjoining one generator and the
single relation `2q_new=h` has order exactly 2|B|: its old B embeds, and
its quotient by B is cyclic of order two. It surjects onto the actual
subgroup in (3), which has the same order. Hence that presentation is
EXACT. There are no further unknown relations to discover and no need to
test exact equality of p-adic points.

The premise is a nonzero class in B/2B, not merely a nonzero vector of
generator coefficients. For example in A=Z/4, retain generators b_0=2 and
b_1=1 with relation 2b_1=b_0. The nonzero coefficient vector (1,0) has zero
Kummer label but is zero in B/2B when B=A; halving it gives an old element.
The algorithm below explicitly removes such relation vectors.

## 3. A triangular presentation with no point recombinations

Retain all generators immutably. At step i there are `s=q+i` generators,
and an s-by-s relation matrix R_s. Initialize `R_q=2I_q`. When a new
generator is adjoined, append its row

    (-v_1,...,-v_s,2),       v_j in {0,1}.              (4)

The old rows acquire a zero last entry. Thus R_s stays lower triangular
with diagonal 2, and all entries lie in {-1,0,2}. It presents a group of
order 2^s, exactly the embedded B by Section 2.

Let W_s be the row span of R_s modulo 2. Let Lambda_s be the binary label
matrix whose columns are the labels of the s actual generators. Then

    B/2B=F2^s/W_s,       W_s subset ker Lambda_s.       (5)

At initialization W_q=0. If label rank is below q, ordinary F2 elimination
finds

    v in ker Lambda_s but not in W_s.

Choose its 0/1 representative and assemble `h=sum v_j b_j`. After the half
call, append (4). Its reduction modulo 2 is independent of the old row
span precisely because v was outside W_s. Thus the quotient in (5) retains
dimension q. These are finite exact linear-algebra decisions.

No Smith-form generator change, large-exponent point operation, or equality
oracle is required. The presentation can be converted to HNF/SNF using
integer arithmetic if desired, but that is unnecessary for either the next
halving input or the output label basis. If converted, its invariant-factor
exponent bit lengths are at most `log2|A|=kappa+q`; the point representatives
need not be converted with it.

This is a redundant list WITH its complete relation lattice. A redundant
list and its label kernel alone would be insufficient.

## 4. Original-E identities carried by the actual-point DAG

Associate each generator with an immutable DAG naming an actual point P_j.
Initial relation certificates are

    2P_j in 2L=E                 for a seed,
    2T_j=0                       for branch 2-torsion.

The latter follows from the divisor of its factor polynomial; complements
give the same 2-torsion class. These are mathematical identities, not tests
that an approximate coordinate vector is zero.

For every successful binary canonical group operation, the certified
divisor identities in the candidate give

    P_out=P_left+P_right+2sigma(z).                    (6)

Negation replaces b by -b exactly. Since sigma(z) belongs to the proved
subgroup U contained in the ORIGINAL E, every error in (6) belongs to E.
Assemble the 0/1 sum by binary operations. Its actual DAG output H satisfies

    H=sum_j v_j P_j+e_asm,       e_asm in E.            (7)

Here e_asm is an explicitly recorded sum of certified sampler terms; no
membership oracle for a newly defined lattice is used. In this schedule it
is even a sum of 2sigma terms, hence lies in 2U, but the weaker inclusion
in the fixed E is enough.

The half routine's exact identity is

    2Q=H+2sigma(z_half).

Combining it with (7) gives the new relation certificate

    2Q-sum_j v_j P_j=e_asm+2sigma(z_half) in E.         (8)

Equation (8) is exactly relation (4) in A. It need not vanish as an actual
point of J(Q2). In particular a representative of a finite-order coset may
have infinite actual order. Treating the finite presentation as literal
torsion relations in J would be wrong.

Labels are unchanged by the allowed shifts because E is contained in 2G.
The zero-label input H therefore lies in 2G and meets the half routine's
divisibility promise. A shift that merely preserves labels, but does not
belong to E, would not suffice for (8); the candidate uses the stronger,
proved sigma identity.

During refinement, retain the same sampler parameters, selected local
factors, root balls and certified algebraic branches. A shared DAG then
names the same actual points when digits are recomputed or discarded.
Relations are attached to those exact cosets and identities. Replacing a
node by an unrelated nearby point is not authorized by this argument.
The sampler/error certificates themselves can remain DAGs; they need not
be expanded into a long sum or explicit Z2 coordinates in the seed lattice.

## 5. Stopping, call count and precise remaining scope

If label rank is q, then `B+2A=A`. The finite 2-group A/B satisfies
`2(A/B)=A/B`, which forces A/B=0. Conversely B=A gives rank q. Thus

    label rank q  <=>  B=A.                            (9)

Since `|A|=2^(kappa+q)` and `|B_0|=2^q`, exactly kappa successful
enlargements occur. At the last stage choose pivot columns of Lambda_s.
They are labels of actual represented points and form a basis of the
COMPLETE local image. No sampled-witness inference or enumeration of A
enters this conclusion.

Use the computable bound, for example

    K=D0+2g(4D+12)+g(2ceil(log2 g)+4)+3g >= kappa.      (10)

The subtraction of t in the sharper proved bound is optional. K is
polynomial in the native parameters; the exact kappa is not input advice.
At iteration i, the selected vector has weight at most q+i. Its sum needs
at most q+i-1 binary additions, followed by one ONE-HALF call. Hence

    N_add <= kappa(q-1)+kappa(kappa-1)/2,
    N_half = kappa,
    N_add+N_half <= K(q+K).                            (11)

There are q initial label computations and one new label per half. A half
call internally includes its one shifted-input materialization and scalar
pencil draw. Even counting these separately changes (11) only by O(K+q).
An intermediate sum's label is the known binary sum of its input labels,
because its certified shift lies in E; it needs no fresh backend label call.
Thus (1) comfortably bounds these scheduled high-level calls and sampling
stages. It is a justified cap for this explicit algorithm; no unspecified
HNF/SNF point-recombination policy is needed to justify the fourth power.

Binary compression after each sum keeps the actual divisor degree bound:
two stored graph pairs contribute at most 2g, and 2sigma contributes 4g,
so each addition has m<=6g. A half's shifted input has m<=5g. The growing
number s of presentation generators is never expanded into a single large
divisor operation. No large exponent is expanded into repeated divisors.

The shared point DAG has q initial point nodes and O(1) new group nodes per
call in (11), with polynomially many arithmetic nodes per supplied subroutine.
Exact relation
and error certificates add only polynomially many references. This pays the
group-level DAG size. The separate precision audit must still verify that
reevaluating each such subroutine to P digits costs only P plus its stated
polynomial guard, and must charge the native label/root backend.

Conditional on those numerical subroutine guarantees, fresh failure
allowances bounded by eta/(10T0), together with the separately charged
backend allowances, admit the adaptive union bound: the current incoming
point is fixed conditional on the past, and the supplied success estimates
are uniform in that point. Exceeding K or failing a fixed local clock returns
ABORT; a partial basis is never returned as the complete image.
