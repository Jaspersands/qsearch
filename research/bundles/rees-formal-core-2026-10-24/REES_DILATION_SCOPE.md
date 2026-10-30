# Concrete Graded Lie Automorphisms

2026-10-24. This closes a specifically named formal proof obligation in
the Rees mechanism. It does not supply a natural hard application, BCH
group construction, complete quantum algorithm or novelty certification.

## Research Decision

The preceding HDQI pass rejected a fixed-sign transfer shortcut. Returning
to Rees applications did not produce a new independently motivated hard
family. The existing succinct-polynomial audit already includes derivative,
Frobenius-lift, orbit-module and Moore-gradient classical filters. Their
failure is not evidence of hardness. No synthetic candidate was created.

The recent sparse shift-equivalence result concerns explicit sparse inputs,
with its stated rational/large-characteristic scope; it does not by itself
solve arbitrary compact-circuit, nonabelian stabilizers.
[Blaser et al., 2610.27168](https://arxiv.org/abs/2610.27168).
The earlier circuit shift algorithm also has degree and characteristic
restrictions, as well as a different action.
[Dvir--Oliveira--Shpilka](https://arxiv.org/abs/1401.3714).
This targeted check is not an exhaustive novelty review or hardness proof.

Instead, this pass addresses the unformalized automorphism used by the
existing Rees algorithm. The old dilation_membership_iff only concerns
submodule membership under scalar powers. It is not a bracket or inverse
proof for the actual cover.

## Construction And Proof

Use the cover in REES_LIE_SCOPE.md. Put C_j=gamma_(j+1)(L), assume C_n=0,
and choose n distinct nonzero field points s_i. Let

    V={v: v_j in C_j}, E(v)_i=sum_j s_i^(j+1) v_j,
    D_a(v)_j=a^(j+1)v_j, delta_a=E o D_a o E^-1.

Here E^-1 is the checked inverse evaluation matrix, not hidden advice.
recoverLinear, scaleCoefficients and dilationLinear implement these maps.
The evaluation points need NOT be closed under multiplication by a.
There is no assumed permutation of the chosen points.

dilation_mem proves the image remains in the constructed cover. The key
dilation_lie theorem expands both inputs into monomials of positive
degrees r,s. Their bracket has coefficient in gamma_(r+s)(L). When
r+s<=n, a^(r+s)=a^r a^s proves compatibility. When r+s>n, the coefficient
is ZERO by nilpotence and the checked lower-central bracket theorem.
No nonzero term is discarded by a truncation convention. Bilinearity
then proves the full Lie identity.

dilationHom is an actual LieHom. The composition law delta_a delta_b =
delta_(ab) and identity delta_1=id are checked. For a!=0, dilationEquiv
constructs a LieEquiv with inverse delta_(a^-1), proving both inverse
identities. Invertibility and bracket preservation are not premises.

dilation_hidden_membership_iff proves for EVERY original submodule h:

    all evaluations of delta_a(x) lie in h
        iff all evaluations of x lie in h.

It uses recovered coefficients and the older membership lemma. No
homogeneity assumption on h in an original grading of L is added.

## Receiver Controls

The highest monomial grade is proved central, and its dilation is exactly
scalar a^n, as required by that grade's central moment equation. This is
NOT a claim about the whole center: lower-grade central elements can have
different scaling powers.

Zero scaling erases all coefficients in the actual evaluation realization.
It is a Lie endomorphism, not the nonzero-scalar automorphism needed by
the receiver. No inverse at zero is constructed.

A universal obstruction rejects ordinary uniform scalar multiplication:
over a field, a!=0,1 and [x,y]!=0 imply

    a[x,y] != [ax,ay]=a^2[x,y].

This is a checked theorem, not a finite example. For F_2 its nontrivial
scalar premise is empty; no unavailable scalar is assumed.

## Scope And Handoff

ReesDilation.lean adds 13 theorems and 5 definitions. The expanded audit
recompiles three modules and checks all59 items:44 theorems and15
definitions/instances. It includes the LieHom and LieEquiv constructors.
Only propext, Classical.choice and Quot.sound are permitted; missing
declarations, diagnostics, sorryAx and assumed automorphisms are rejected.
The original snapshot and earlier proof statements remain unchanged.

The result holds over any field under explicit distinct-point and
nilpotence assumptions. BCH/Lazard group functoriality and its separate
characteristic/class restrictions remain unformalized. So do normalized
quantum instruments, adaptive fresh-copy composition, SDE runtime, Fourier
recovery, precision, gate complexity and application hardness.

Noncomputable Lean definitions are not an extracted algorithm or a bit-cost
certificate. The pinned toolchain and imported mathlib proof binaries
remain trusted. The full algorithm is NOT FORMALLY VERIFIED. The authorized
independent reviewer was not reused and no new reviewer was spawned.

After verified migration, integrate ReesDilation.lean, its module entry,
audit manifest and verifier changes into the real formal project. Retain
the source snapshot and rerun all59 checks under the final module paths.
Mark only the graded Lie-automorphism obligation checked. No new candidate,
UI change or circuit-search work is needed. This is not repo-wide validation.

Next substantive proof work: BCH/Lazard compatibility or the complete
normalized all-record quantum channel. A genuine natural source or a
same-input classical attack would have higher application value than
additional nearby algebra fixtures. A failed filter is not a hard family.
