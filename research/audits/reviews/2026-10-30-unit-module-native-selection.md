# Unit-Module Construction And Native-Application Selection

30 October 2026. Five-agent research pass; automated review only.
No human endorsement, novelty certificate, external contact or submission.

## Roles And Disposition

- Averroes independently checked classical explicit-matrix stabilizer
  algorithms, their log-p dependence and the succinct-representation limit.
- Anscombe examined a concrete public constraint-system symmetry route,
  deriving an orbit-label obstruction rather than substituting an oracle.
- Chandrasekhar adversarially reviewed the unit-cube probability argument,
  pilot/source accounting, mixed-order lift and conditional tree bounds.
- Leibniz implemented only the unit-mode arithmetic and its independent
  tests. This was not an independent proof review.
- Meitner independently checked the later generic semantic-label hardness
  reduction, including its always-nonzero repair and complexity qualifications.
- Parent derived the mixed-module policy, integrated certified coordinates,
  original-degree lifting and ambient verification, checked primary sources,
  and retained executable counterexamples.

All agents were closed after completing their assignments. The constructive output is
[unit-power module cancellation](../../UNIT_POWER_MODULE_CANCELLATION.md).
No examined native problem became a justified new quantum application.

## Constructive Result And Review Corrections

For actual IID character labels, require all coefficients of a power-valued
kernel vector to be nonzero. Full intrinsic bank rank then implies full
Jacobian rank after conversion to the original exponent. Existing regular
lifting supplies a mixed-order witness; certified pilot coordinates and
verification in the original ambient module avoid hidden advice.

With rank<=u-1, class<=u and p>=16u^2, 4u pilots plus 4u bank sources
give raw arity 8u per grade. Classical rejection remains exponential in u
but does not resample the measured bank. The reviewed conditional source
tree has cost 2^O(u log u), not a complete all-prime ring HSP guarantee.

Chandrasekhar found no fatal error and checked the tree constants. The
review added decisive exclusions: original degree divisible by p need not
lift, and derived cyclic rank one need not bound ring nilpotency class.
Both now have exact regressions. The whole-source law, pointwise conversion,
mixed-ring quantum compilation and useful application remain separate.

The first parent CLI regression failed due to a missing pytest import in
the test, not an arithmetic mismatch. The import was corrected and the
connected tests rerun. Final commands/counts are in the latest handoff.

## Reconfirmed Explicit-Matrix Classical Baseline

[Luks, Theorem 3.2](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf) supplies
membership, vector-stabilizer and subspace-stabilizer algorithms polynomial
in matrix dimension, log field size and the largest non-characteristic
prime divisor of group order. For a promised p-group over F_p, that last
parameter is absent. Thus explicit vector/tensor actions are covered without
a large-characteristic or module-Lazard guard. The generated GROUP must be
a p-group; individual unipotent generators do not certify that promise.

This confirms the existing [tensor-train reduction](../../TENSOR_TRAIN_CLASSICAL_FILTER.md),
not a new classical theorem. Its small prefix-support representations also
fall within the published algorithm. The repository's narrower logarithm
backend still lacks that general fallback; UNSUPPORTED is not hardness.
Expanding an arbitrary succinct circuit's exponential representation would
not yield polynomial circuit-size cost, so this is not a universal circuit
stabilizer algorithm.

## A Specific Native Lead That Fails

Finite-field constraint systems are genuine classical inputs in arithmetic
circuit verification; [Pailoor et al.](https://www.cs.utexas.edu/~isil/qed.pdf)
give one concrete application domain. Consider the following research
ensemble, not a claim about that paper's input distribution.

Choose p>3, D>=4 and a uniform w in F_p^D with w_4!=0. Independently choose
D+2 quadratic polynomials' nonconstant coefficients uniformly and set
their constants to vanish at w. Publish only the polynomials Q_i, discarding
w. Put S={x:all Q_i(x)=0} and

    F_Q(x)=product_i(1-Q_i(x)^(p-1)).

This is a polynomial-size circuit computing the BASE-FIELD indicator of S;
binary powering costs polynomially in log p. For each x!=w, one nonzero
linear-coordinate difference makes Q_i(x) uniform given Q_i(w)=0. Hence
the chance that all equations vanish at x is p^(-D-2), and a union bound
gives Pr[S={w}]>=1-p^-2.

Let UT4(F_p) act on the first four coordinates. The task is to recover the
semantic set stabilizer H={g:gS=S}. Its group dimension is six, class three,
derived dimension three; on the singleton event H has codimension three.
Writing upper entries (a,b,c,d,e,f) and alpha=w_2/w_4,beta=w_3/w_4 gives

    f=0,       e=-d*beta,       c=-a*alpha-b*beta.

These determine a nonnormal subgroup of order p^3. Its output reveals the
two ratios, not the complete witness. Useful symmetry information should
not be inflated into solving arbitrary constraints.

### Fixed Evaluation Banks Fail

A candidate label l_Z(g)=(F_Q(g^-1 z_j))_j is inexpensive per query, but
the singleton orbit contains p^3 DISTINCT point indicators. Every bank
point distinguishes at most one. All unqueried indicators share the zero
label. Therefore global orbit separation requires M>=p^3-1 bank points,
even optimally chosen ones. Random domain points are worse: two orbit
functions disagree on only 2/p^D of the domain.

This excludes that label construction in poly(D,log p) cost. It does not
exclude a symbolic canonicalizer exploiting the public equations or prove
hardness for the public-input problem. Predicate-only competitors would
be an unfairly weakened classical baseline.

### Raw Extension Fingerprints Also Fail

For v=e4 use the nonzero singleton predicate
F_v=product_(i=1..4)(1-(x_i-v_i)^(p-1)). The shear h=I+E12 fixes v, so
F_v(h^-1 x)=F_v(x) on F_p^4. On x=(0,t,0,1), however, their formal
difference is t^(2(p-1))-t^(p-1), not the zero polynomial. At p=5 and
t^2=3 in F25 it equals 2. Thus raw extension evaluation splits a genuine
semantic stabilizer coset. This elementary family is a counterexample to
the GENERAL repair; it is not claimed to be a typical sampled Q-system.

Reducing modulo the field equations before canonicalization might repair
the semantics, but no polynomial-size orbit-separating construction was
established. Merely stabilizing the supplied quadratic span changes the
problem unless that span is proved sufficient.

## Decision And Next Test

No candidate promotion. A proposed repair must give one jointly canonical
label for all these orbit objects at polynomial total cost while preserving
the exact semantic cosets. The sparse bank and extension tests are now in
`tests/test_native_constraint_orbit_labels.py`. Recovering w first already
gives H classically, so it cannot be a free step in the quantum reduction.

Matched competitors get the same public equations: algebraic elimination,
XL and finite-field SMT, such as [Hader--Kaufmann--Kovacs](https://arxiv.org/abs/2305.00028).
No asymptotic performance claim for this ensemble is established. No SMT
benchmark or vulnerability search was run in this pass. The tests are
falsifiers of specific reductions, not evidence of hard instances.

## Generic Canonicalization Is Already A Hard Problem

Parent derived the following stronger worst-case obstruction; Meitner
independently checked the nonzero construction. It does NOT establish
hardness for the random planted ensemble above.

Fix p=5 and G=UT4(F5), a CONSTANT group. Given arbitrary quadratic equations
Q_i(x)=0, define chi_Q as above and delta(y)=1[y=e4]. Add a selector z,
fixed by G, and the polynomial-size circuit

    Ftilde(x,y,z)=(1-z^4)+(1-(z-1)^4)*chi_Q(x)*delta(y).

As a base-field FUNCTION it is the indicator of two disjoint branches:
all (x,y) at z=0, and solutions x with y=e4 at z=1. It is ALWAYS nonzero.
If the equations are infeasible its stabilizer is G. Otherwise restricting
to any solution x and z=1 shows that its stabilizer is exactly G_e4.

Quadratic feasibility over F5 encodes Boolean circuit satisfiability:
u(u-1)=0 constrains each wire, w-uv=0 represents AND, w+u-1=0 represents
NOT, and the output is constrained to one. These are polynomial-size
quadratic systems. Therefore generic semantic stabilizer recovery already
decides SAT in this constant-group, class-three setting.

In particular, suppose a uniform deterministic polynomial-time procedure
constructs EXACT orbit labels l_F(g), with efficient evaluation and ordinary
equality comparison. Comparing l_F(I) with l_F(I+E14) decides feasibility.
Such a generic procedure would imply P=NP. Merely returning circuits whose
semantic equality remains hard is NOT such a label. Bounded-error
randomized comparison with one shared constructed map instead gives
NP contained in BPP, not P=NP. An end-to-end bounded-error quantum solution
would give NP contained in BQP; that containment is not known impossible.

For the STANDARD normalized coset source there is also a direct quantum
source barrier, independently checked by Meitner. Write N=|G|, h=|H| and
rho_H=(1/N)*sum_g |gH><gH| with normalized coset vectors. Its overlap with
the known uniform-group projector |G+><G+| is h/N. The two cases above
give 1 and 1/125. A uniform polynomial-time factory producing these states
within trace distance 1/10 would already decide feasibility in BQP using
that fixed-group measurement, without Rees. Constant measurement error can
also be charged while keeping total error below 1/3. Preparation must be
end-to-end and paid; unbounded postselection does not qualify. This claim
is specific to these coset states, not arbitrary distinguishable-looking
orbit states.

This is a qualification on the source problem, not a new algorithmic
candidate, a barrier for every restricted family, or a proof that all
useful applications are impossible. It explains why reducing the Rees
receiver's cost cannot by itself supply a generic semantic canonicalizer.
