# Rational Gaudin preparation: prefix-norm falsifier and classical counterpart

2026-11-07. CLOSED focused core review. The proposed deletion-prefix use
of the on-shell Gaudin norm determinant is refuted by an exact legal
two-root input. This does not exclude other off-shell formulas or other
Bethe-state preparation mechanisms. No numerical control or quantum
implementation was run for this review.

Read current STATE/TRAPS and the frozen primary snapshots
`audits/sources/bethe_prefix_admission/correlators.txt` (Theorems 2 and 5,
their stated hypotheses and surrounding formulas) and `gaudin.txt`
(the occupation-basis permanent and Cauchy determinant formulas,
equations 45--50). The source review of other preparation algorithms is
separate.

## 1. Native state and the proposed operation

For pairwise distinct real rational sites epsilon_i and distinct real
rational roots v_a, with no root-site coincidence, define

    B(v)=sum_i sigma_i^+/(v-epsilon_i),
    Psi=product_(a=1)^M B(v_a)|0>.

The given roots must satisfy the same rational equation value gamma:

    gamma=sum_i 1/(v_a-epsilon_i)
              -2 sum_(b!=a) 1/(v_a-v_b).

The state is promised nonzero. The proposed recursive preparation
would obtain every conditional occupation probability from prefix
norms, using the on-shell Gaudin determinant after deleting sites fixed
empty. The first empty-site projection does produce the same product
of B operators restricted to the remaining sites. It generally does
not preserve the Bethe equations on those sites.

The actual `correlators.txt` Theorem 2 explicitly requires the Bethe
equations. Its general Theorem 5 is a sum of M! determinants, not a
single unrestricted replacement determinant. That literal sum gives
no polynomial growing-M clock; it does not prove that no different
polynomial off-shell formula exists.

## 2. Exact two-root calculation

For M=2 let a_i=1/(v_1-epsilon_i), b_i=1/(v_2-epsilon_i), d=v_2-v_1,
and, for a set U of available sites, put

    A=sum_(i in U) a_i^2,  B=sum_(i in U) b_i^2,
    K=sum_(i in U) a_i b_i.

The coefficient of |i,j>, i<j, is a_i b_j+a_j b_i. Therefore the true
squared norm is

    Z_U=AB+K^2-2 sum_(i in U) a_i^2 b_i^2
       =AB+K^2-2(A+B)/d^2+4K/d^2,

where a_i-b_i=d a_i b_i was used in the second equality. The proposed
two-root Gaudin determinant is

    det [[A-2/d^2, 2/d^2], [2/d^2, B-2/d^2]]
       =AB-2(A+B)/d^2.

Their discrepancy is exactly K(K+4/d^2). On the full on-shell site
set, subtracting the two Bethe equations gives dK=-4/d, so K=-4/d^2
and the discrepancy vanishes. Deleting a site does not preserve this
identity.

Take the parent-proposed exact input

    epsilon=(1/2, 2, 1/5, 7/5),    (v_1,v_2)=(-1,1).

Then

    a=(-2/3,-1/3,-5/6,-5/12),
    b=(2,-1,5/4,-5/2).

The two equation values are both gamma=-5/4, all poles and roots are
distinct as required, and

    A=205/144, B=205/16, K=-1, d=2,
    Z_full=25625/2304>0.

For completeness, the six occupation amplitudes in order
(12,13,14,23,24,34) are

    (0, -5/2, 5/6, 5/12, 5/4, 25/16).

Delete the first site epsilon_1=1/2. The reduced values are

    A'=47/48, B'=141/16, K'=1/3,
    Z_empty-first=9625/2304,
    det G_deleted=8601/2304.

The discrepancy is 1024/2304=4/9, and the actual probability of an
empty first site is 77/205. The deleted system's two Bethe equation
values are -7/12 and -13/4, so it is visibly off-shell. This is a
falsifier of the proposed universal prefix recursion, not a defect in
the source's on-shell theorem.

An occupied-prefix branch has an additional issue: fixing a site j
occupied gives a sum over which root supplied that excitation,

    sum_a (v_a-epsilon_j)^(-1)
          product_(b!=a) B_remaining(v_b)|0>.

It is generally a superposition of different off-shell Bethe products,
whose norm contains cross terms. Simply deleting the site and one
arbitrarily chosen root does not describe it. The empty-prefix example
already suffices for the rejection.

The same example also refutes a particular single-state dual repair.
After that empty-first projection there are three remaining sites and
two excitations. A one-hole Cauchy dual C(w)|111>, up to a common
nonzero scalar kappa, would have amplitude kappa/(w-epsilon_i) for
the configuration missing site i. In the remaining-site order
(2,1/5,7/5), the actual missing-site amplitudes are

    (25/16, 5/4, 5/12),

so their reciprocals are (16/25,4/5,12/5). The slopes of the first
and second consecutive pairs as functions of epsilon are respectively
-4/45 and 4/3. They are unequal. But reciprocals of a single Cauchy
dual must be the affine function (w-epsilon)/kappa. Thus there is no
such finite w and scalar, even allowing complex values. The w-at-infinity
scaled limit would give constant amplitudes, which also fails. A
root-site pole limit could give a single supported configuration, not
these three nonzero amplitudes. This excludes only the stated one-hole
same-state Cauchy descriptor; it does not exclude sums of dual states,
other representations, or other off-shell norm algorithms.

## 3. Amplitudes are polynomial-BIT computable

For an occupied set S of size M, form the square Cauchy matrix
C_(a,j)=1/(v_a-epsilon_(S_j)). Expansion of the raising operators gives

    A(S)=per C=det(C entrywise-squared)/det C.

The second equality is Borchardt's identity. One can verify it by
induction as a rational function of the last root: both sides have
simple poles at the selected sites, with residues equal to the
corresponding smaller permanent; the apparent root-collision poles
of the determinant quotient cancel, and both sides vanish at infinity.
The Cauchy determinant is nonzero under the native distinctness and
no-pole assumptions. The source's equations 47 and 49--50 also give
the occupation permanent and a rational-model determinant evaluation.

Thus exact rational determinant arithmetic computes any occupation
amplitude, including its sign and whether it is zero, in polynomial
time in N, M and the rational input bit size. Exponentially small
amplitudes do not cause an unbounded precision debt: all rational
entries, determinants and ratios have polynomial bit size. A product
of the denominators of all NM entries supplies a common denominator
of polynomial bit length for every amplitude. Squaring it supplies
one for every prefix norm; summing at most 2^N nonnegative numerators
adds at most N bits to their magnitude. This is an output-size bound,
not an algorithm for those sums.

Borchardt evaluation alone does NOT give Born sampling. In particular
it does not turn this state into a Slater determinant with an already
paid determinantal point-process sampler.

## 4. A paid all-prefix norm routine would also pay classical sampling

Suppose a classical routine, from the native input and a binary
occupation prefix z, computes

    Z_z=sum_(S consistent with z) |A(S)|^2

exactly, or to the polynomial-bit accuracy required for the conditional
ratios, in polynomial time. Then classical sequential sampling chooses
the next bit with probability Z_(z1)/Z_z. Zero-weight prefixes are never
visited. This supplies Born samples with polynomial work; rational
Bernoulli draws can be capped with an allocated failure probability.
Polynomially accurate approximate conditional probabilities similarly
give total-variation error at most the sum of their per-step errors.
An inverse-polynomial additive error on unnormalized exponentially
small Z_z is not automatically enough; the premise must pay the
required precision, just as a coherent recursive preparer must.

Together with the exact amplitudes, this gives a classical estimator
for every efficiently row-sparse observable O with a supplied norm
bound ||O||<=Lambda. For X drawn from the Born law, let

    L_O(X)=sum_Y O_(X,Y) A(Y)/A(X).

The row is enumerated in polynomial time; samples have A(X)!=0.
Direct cancellation gives

    E L_O(X)=<Psi|O|Psi>/Z_full,
    E |L_O(X)|^2<=||O||^2<=Lambda^2.

Consequently additive-error estimation is polynomial in the sparse
row cost, Lambda, 1/epsilon and log(1/eta), with standard independent
sampling and a robust mean estimator. For an approximate sampler,
clip the estimator at R=O(Lambda^2/epsilon): the clipping bias is
O(Lambda^2/R), and total-variation error delta changes the clipped
mean by at most 2R delta. Thus polynomially small delta suffices.
Polynomial sums of bounded Pauli observables, including long strings,
fit this scope. A raw observable with exponentially large norm does
not acquire polynomial absolute-accuracy cost for free.

This is a conditional classical counterpart to the proposed ALL-prefix
norm mechanism. It does not classically simulate a different quantum
preparation algorithm, arbitrary subsequent quantum circuits, or the
whole Bethe-state family without a sampler. Existing specific local
form-factor formulas may give further direct classical readouts;
their full scope is left to the separate source audit.

## Disposition

The specified deletion-plus-Gaudin-determinant preparation route is
rejected. Exact polynomial-BIT amplitudes are accepted. A genuinely
paid all-prefix norm routine would enable both recursive quantum
preparation and the matched classical sampling/readout above. No
general Bethe-preparation no-go, generic off-shell formula exclusion,
hardness, novelty or quantum speedup claim follows.

## Proof-only addendum: one-site marginals are already paid

Fix a nonzero coupling G=-1/gamma and the Hamiltonian convention

    H=sum_i epsilon_i n_i-G sum_(i,j) sigma_i^+ sigma_j^-.

Write the Bethe equations as F_a=0, with

    F_a=sum_j (v_a-epsilon_j)^(-1)
        -2 sum_(b!=a)(v_a-v_b)^(-1)-gamma.

The elementary spin commutators give, with S^+=sum_i sigma_i^+,

    H Psi=(sum_a v_a)Psi
          -G sum_a F_a S^+ product_(b!=a) B(v_b)|0>.

Here the coefficient of each unwanted term is
-1-G sum_j(v_a-epsilon_j)^(-1)+2G sum_(b!=a)(v_a-v_b)^(-1)
=-G F_a, since 1+G gamma=0. This verifies the Hamiltonian sign and
the on-shell energy E=sum_a v_a without a normalization convention gap.

Their root Jacobian is minus the Gaudin matrix: the diagonal derivative
is -sum_j(v_a-epsilon_j)^(-2)+2sum_(b!=a)(v_a-v_b)^(-2), and the
off-diagonal derivative is -2(v_a-v_b)^(-2). At fixed G, hence fixed
gamma, the explicit epsilon_i derivative is the column

    (w_i)_a=(v_a-epsilon_i)^(-2).

When det Gaudin is nonzero, the implicit function theorem gives a
smooth local root branch and

    Gaudin * (dv/d epsilon_i)=w_i.

Hellmann--Feynman therefore yields the exact one-site occupation

    <n_i>=dE/d epsilon_i=1^T Gaudin^(-1) w_i.

An isolated energy eigenvalue is not needed once this differentiable
eigenvector branch exists: differentiating H Psi=E Psi and multiplying
by Psi^dagger cancels the vector-derivative terms using Hermiticity.
The nonzero Gaudin determinant supplies the required root branch;
singular roots, poles or a singular Jacobian are outside this argument.
One must keep G fixed; varying G introduces the derivative of the
interaction term and changes the claimed marginal formula.

For the retained rational example, the matrix and first-site column are

    Gaudin=[[133/144,1/2],[1/2,197/16]],
    w_1=(4/9,4)^T.

Exact algebra gives Gaudin^(-1)w_1=(64/205,64/205)^T. Hence the occupied
probability is 128/205 and the empty probability is 77/205, agreeing
with the independently derived prefix norm. No control was rerun.

For rational native data these matrix solves have polynomial BIT cost;
all N one-site marginals can share one factorization. This baseline
does not require a conditional-norm oracle. It applies to each site
of the original on-shell state, not to arbitrary conditional states
after a growing number of measurements. The first empty-site state
above is already off shell, so this formula does not repair the
rejected all-prefix recursion.
