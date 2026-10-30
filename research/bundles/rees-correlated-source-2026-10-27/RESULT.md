# Opposite Labels From One Native Source Do Not Supply Two Targets

2026-10-27. A scoped test of a concrete escape from the destructive Rees
source-tree bound. This is not an HSP lower bound, a new hard oracle
problem, a novelty claim, or a change to the fixed-class theorem.
One completed independent mathematical review accepts the scoped argument
and weak-Fourier corollary. The parent read the review in full and applied
its scope qualifications; see the sibling review and VERIFICATION.md.
The review does not audit code or establish novelty.

## Question And Native Construction

Can a cheap correlated source replace the independent targets consumed by
the existing central-cancellation receiver? Opposite measured labels alone
are insufficient. There is a legal construction producing them with one
lifted hiding query, but the tested receiver loses the desired information.

Let G be a finite group, H a hidden subgroup, and

    rho_H[g,g'] = 1/|G| * 1{g^-1 g' in H}.
    V|g> = |G|^(-1/2) sum_y |g y, y>.
    Theta_H = V rho_H V^*.

V is an isometry: prepare a uniform y register and reversibly multiply.
Equivalently query the ordinary lifted hiding function on x y^-1 in a
uniform pair (x,y), clean the argument workspace, and discard its output.
No subgroup knowledge, conjugate-state oracle, or postselection is used.
One lifted query costs two original queries in the class-two Rees example
below. Ideal uniform preparation is an explicit circuit primitive, not a
claim of exact synthesis in a fixed finite gate set.

Write R_a|g>=|g a>; this convention is an anti-representation. For a central
element z, (R_z tensor I)V=V R_z and (I tensor R_z)V=V R_(z^-1).
Consequently measuring both central characters gives (lambda,-lambda)
with certainty. If rho_H,lambda is the normalized first sector, the JOINT
conditional state is V rho_H,lambda V^*, not a tensor product of sectors.

## Exact Receiver Law

For arbitrary a,b in G, direct substitution gives

    V^*(R_a tensor R_b)V
      = |G|^(-1) sum_y R_(y a b^-1 y^-1).

Define k_H,lambda(u)=Tr(rho_H,lambda R_u). The overlap available to the
standard controlled-right-translation-and-discard receiver is therefore

    C_H,lambda(a b^-1)
      = |G|^(-1) sum_y k_H,lambda(y a b^-1 y^-1).

For controlled choices a(q), b(q), the control density entry (q,q') is
the initial control entry times

    C_H,lambda(a(q) a(q')^-1 b(q') b(q)^-1).

This allows arbitrary public choices of the two translations, not merely
dilations. Equal right translations act as the IDENTITY on V's image.
The operator identity, rather than label arithmetic, is the relevant test.

The state itself has not lost all information about H. V is reversible on
its image. Different target observables, retained target information, or
left/mixed actions require a different analysis. Multiple retained controls
alone do not evade the restriction. The result below applies only to the
specified observable algebra and ultimately discarded targets.

## General Interpretation: Only Weak Fourier Information

This restriction has a precise information-theoretic characterization for
ANY finite group, not just the example below. Let A be the operator algebra
spanned by R_a tensor R_b. It is closed under products and adjoints. The
compression identity shows

    V^* A V is contained in the center of span{R_g : g in G}.

Indeed every compressed basis element is a conjugacy-class average. Let
Pi_pi be the orthogonal central projectors for the irreducible representation
types in the regular representation. Every POVM effect E in A compresses to

    V^* E V = sum_pi e_pi Pi_pi,  0<=e_pi<=1.

Completeness gives sum_outcomes e_pi=1. Its outcome distribution on V rho V^*
is a classical postprocessing of the weights Tr(rho Pi_pi), namely weak
Fourier information. Conversely the central projector Pi_pi on the first
target satisfies V^*(Pi_pi tensor I)V=Pi_pi, so those weights are accessible
in this operator interface. This is a STATISTICAL equivalence, not an
efficient nonabelian-QFT implementation or an efficient classical simulator.

Ancillas, joint controls, adaptive control measurements and repeated right
actions followed by target discard do not enlarge this algebra: expand
their induced effects in its basis. The analogous tensor-product argument
applies to fresh independent copies. A measured central-character projector
already belongs to this algebra and does not evade the conclusion. Other
target measurements, a second native oracle invocation on existing targets,
left actions and retained target information are explicitly excluded.
Compose the receiver effects in the original algebra BEFORE compression:
E -> V^* E V is generally not multiplicative.

Thus the proposed construction has quietly replaced a strong coset-state
receiver by an interface with only weak Fourier information. Proving label
cancellation is not enough to prove a useful source conversion. The Rees
example gives an explicit exponential-in-log(p) consequence of that loss;
the general compression identity is the reusable diagnostic.

## An Actual Rees Counterexample

Take the ordinary Heisenberg Lie algebra L=<X,Y,W>, [X,Y]=W over F_p,
for odd prime p. Its positive lower-central Rees algebra has coordinates
(x,y,w,z), with grade one X,Y,W and grade two Z=t^2 W. Its group law is

    (x,y,w,z)*(x',y',w',z') =
    (x+x', y+y', w+w', z+z'+(x*y'-y*x')/2).

Use the actual lifted subgroups H_X=exp(<t X>) and H_Y=exp(<t Y>).
They come from legitimate native Heisenberg hidden lines and are graded,
nonnormal, and disjoint from Z=<t^2 W>. All references to central labels
below mean this SELECTED GRADE, not the rank-two full center <tW,t^2W>.
This is a failure control for an
already-solvable class-two problem, not a proposed research candidate.
Every central label lambda in F_p has probability 1/p. With
chi_lambda(z)=exp(2*pi*i*lambda*z/p),

    k_H,lambda(u) = chi_lambda(z0) if u=h*(0,0,0,z0), h in H;
                   0 otherwise.

Conjugation changes z by a nonzero linear form in the conjugator whenever
(x,y) != (0,0). Character orthogonality gives, for EVERY nonzero lambda,

    C_H_X,lambda(x,y,w,z) = C_H_Y,lambda(x,y,w,z)
      = chi_lambda(z) if x=y=w=0;
        0 otherwise.

At lambda=0, conjugation preserves H Z, so C_H,0=1_(H Z).
Thus every nonzero-label branch of this receiver is identical for the two
different required answers. The rare zero-label branch carries the useful
quotient information. In particular, a(q)=section(q), b(q)=1, for a UNIFORM
control q in G/Z, yields the correct quotient coset state at lambda=0 and
the maximally mixed control state for EVERY other label. For a nonuniform
initial control, the latter channel is dephasing, not necessarily a
maximally mixed state.

## Resource Consequence And Limits

Consider at most T fresh independent copies of this specified MIXED source,
with measured central labels and eventual target discard. Initial controls
and advice are H-independent. No hiding outputs, accessible source
purifications, additional hiding queries, or other H-dependent side
information are provided. Targets interact with retained systems only
through their right-action algebra; controls may be processed jointly and
adaptively, and the same targets may be used repeatedly before discard. On the
event that every label is nonzero the complete retained state and label
record are H_X/H_Y independent. Labels are IID uniform before selection;
adaptive choices do not manufacture new independent acquisitions.
For a capped protocol, padding unused potential sources gives

    Pr[any zero among T padded potential labels] = 1-(1-1/p)^T <= T/p.
    Pr[an actually observed zero label] <= 1-(1-1/p)^T.
    Pr[correct binary answer, equal prior]
      <= 1/2 + (1-(1-1/p)^T)/2.

Success >=2/3 therefore requires T>=p/3, a necessary rather than sufficient
bound. This is exponential in log(p). The statement is NOT a quantum query
lower bound: nil-2 HSP already has polynomial-time algorithms, the usual
independent-target cancellation remains valid, and operations outside the
specified receiver can use information still present in Theta_H.

The hypothetical opposite-label PRODUCT bank in the earlier source-tree
review is a genuinely different resource. This construction does not
prepare it. The second marginal is a left-coset version of the native
state, while the first is a right-conjugation twirl; they are not the two
correct right-coset marginals that example requires. In the unconditioned
source these marginals have entries, respectively,

    Theta_second[y,y'] = 1/|G| * 1{y*y'^-1 in H},
    Theta_first[x,x'] = |G|^(-2) sum_y 1{y*x^-1*x'*y^-1 in H}.

Measuring the second register in its group basis instead of its central
Fourier label and undoing the known right translation returns one original
coset state. This is an explicit recovery of surviving information, not a
way to obtain two independent sector targets.

There is an even simpler excluded observable. Write L_s|g>=|s g>. Then

    (I tensor L_s)V = V R_(s^-1).

For a=X and s=a^-1, its expectation in every normalized label sector is
1 for H_X and 0 for H_Y. A Hadamard test distinguishes the binary promise
with success 3/4 in one source. This left action lies outside the tested
algebra and recovers one native source's information, not two targets.
Moreover this specific binary promise is classically decided with only
two original queries: compare f(e) and f(exp X). There is no unrestricted
hardness claim for the control example.

## Research Decision And Decisive Falsifiers

Reject the specific proposal: replace an independent cancellation bank by
the one-query relative-product source and leave the right-translation
receiver unchanged. Do not confuse its perfect opposite labels with a
sample-complexity improvement. The earlier c! source-tree result is NOT
extended to all correlated sources by this counterexample.

Falsifiers are an error in V's native implementation or compression law,
a nonzero-label distinguishing kernel for these two graded Rees lines, or
a receiver within the stated interface that retains hidden-line information
on an all-nonzero record. Exact group/character controls and a separately
built small density matrix test these interfaces below. Finite checks do
not prove the all-prime statement or a quantum speedup.

Do not continue by enumerating more correlated-source failures. Reusing THIS
source requires an observable outside its right-action restriction to
distinguish the all-nonzero sectors. A DIFFERENT source could be informative
under the same right-action algebra; it must supply a paid preparation and
a verified joint kernel. Paid multi-output constructions remain open.
Otherwise return to the main theorem's specialist
review/application question. General SDE optimization alone still does
not remove the growing-class destructive-composition obstruction.

Comparison: Ivanyos, Sanselme and Santha,
[An efficient quantum algorithm for the hidden subgroup problem in nil-2
groups](https://www.irif.fr/~santha/Papers/iss12.pdf), Theorem 1, already
provides an efficient nil-2 HSP algorithm. Their independent-target
automorphism method is not replaced or disproved by this control.
