# Resource And Prior-Art Check After Composition

2026-10-24. Mathematical deductions and literature comparison, not an
additional Lean theorem or independently reviewed end-to-end algorithm.

## Conditional Copy Bound

Assume the intended prime-field input: a public m-dimensional nilpotent Lie
algebra of class c<p, its compatible Lazard group and subgroup correspondence,
and the original charged independent-source acquisition contract. Let
r_j=dim gamma_j(L), with grades j=1,...,c. The central kernel at the step
A_j -> A_(j-1) has dimension r_j, NOT dim(gamma_j/gamma_(j+1)). The Rees cover
has dimension sum_j r_j. Using the smaller associated-graded dimensions here
would undercount the diagonal equations and invalidate the resource claim.

For each j>=2, choose M_j sufficient for the degree-j diagonal system in
r_j equations. Theorem 3 of [Ivanyos--Santha, v2](https://arxiv.org/html/1503.09016v2)
supplies a deterministic polynomial-time solver for fixed j above its stated
variable threshold. A deliberately loose integer envelope is

    M_j = (j^(j^3)+1) * (r_j+1)^(j^2).

It strictly exceeds j^(j^2 log j)*(r_j+1)^(j log j), using log base two or
natural log. The extra constant avoids rounding and strict-threshold issues.
This is a sufficient bound, not an optimized implementation or a lower bound.
When r_j=0, one active target and the trivial character suffice instead.
The quadratic/cubic special cases and reduction to gcd(j,p-1) can reduce
these arities, but no such saving is needed for the following deduction.

The checked source tree consumes L=product_(j=2..c) M_j top-stage copies per
terminal copy. If each top-stage source costs c original preparations,
k terminal samples cost c*k*L originals. The formal recursion proves L;
the native lift and final receiver remain separate premises here.

For fixed c, r_j<=m gives

    L <= C_c * (m+1)^E_c,
    C_c = product_(j=2..c) (j^(j^3)+1),
    E_c = sum_(j=2..c) j^2.

This establishes a conditional polynomial COPY envelope in m at fixed c.
The constants and degree are terrible. It must not be advertised as a
practical resource estimate, or as polynomial when c grows with the input.
The diagonal routine's classical restarts operate on retained labels; they
do not by themselves require discarding and repreparing the quantum packet.
Every returned witness can be checked classically before use.

## Terminal Recovery And Error Budget

Suppose ideal Fourier sampling of the terminal additive source produces
independent uniform elements of h-perp, of dimension r<=m. With k=m+t
samples, failure to span is at most

    ((p^r-1)/(p-1))*p^(-k) < p^(-t)/(p-1).

Reason: a proper span lies in a hyperplane; each of the (p^r-1)/(p-1)
hyperplanes contains every sample with probability p^(-k). For r=0, failure
is zero. Taking the nullspace of the sampled linear forms recovers h when
the span is complete. This is an elementary union bound, not a machine-
checked final Fourier implementation or an exact-success algorithm.

The required precision does not hide inverse rare-branch probabilities.
Let delta be the trace-distance error per independent native source,
eta_lift a full lift-channel error, and eta_j the full stage-instrument
diamond-distance error (all records and failure flags included, using the
same half-norm convention). In one terminal source tree, stage j occurs

    N_j = product_(ell=2..j-1) M_ell

times. Tensor-product telescoping, channel contractivity and composition
give the full k-copy error bound

    k * (c*L*delta + L*eta_lift + sum_(j=2..c) N_j*eta_j).

Local aborts must be included in eta, or bounded separately by a union
bound; do not silently condition them away or count them twice. This bound
assumes fresh independent native preparations and a uniform full-channel
error guarantee. Correct local marginals or per-success normalized-branch
estimates do not imply it. The new correlated-input control falsifies that
shortcut. The trace/diamond argument is not yet formalized in this bundle.

Thus inverse-polynomial precision suffices at fixed c, provided each
primitive is actually uniformly implementable with polynomial precision
overhead. Efficient arithmetic, source preparation and central Fourier
measurement still need their own implementation/resource certificates.

## Newer Comparison Case

[Morales, arXiv:2608.05321v2](https://arxiv.org/html/2608.05321v2), revised
2026-09-28, treats scalar-action semidirect products under bounded-rank and
relative-exponent conditions, and quasi-Hamiltonian groups with supplied
structural coordinates. Its structured-input qualification matters.
This is relevant prior art, not evidence that arbitrary nilpotent HSP is
solved. No independent verification of that paper is claimed here.

Two direct scope deductions prevent confusing its families with the intended
nonabelian exponent-p Lazard input:

- A scalar p-power-order action on an elementary abelian p-group must be
  trivial: its scalar order divides both p-1 and a power of p. A semidirect
  product of this scalar type cannot give a nonabelian exponent-p example.
- In the stated odd-p quasi-Hamiltonian structural form, conjugation on A
  is a^(1+p^s). With exponent p this is the identity; A is abelian and the
  remaining generator commutes with it. Such a group is abelian as well.

These are family-comparison deductions, NOT a novelty proof. Other earlier
algorithms, reductions and input models still require comparison. The
bounded-prime qualification in [Imran--Ivanyos](https://arxiv.org/html/2304.08376v1)
must also remain explicit. The literature search was targeted, not exhaustive.

## Adversarial Decision

The composition and resource arithmetic no longer justify treating this
route as merely a one-stage identity. It is a coherent conditional
fixed-class proposal worth checking. However, the intended assumptions
exclude the characteristic-two, growing-class dihedral route; neither the
new resource calculation nor the newer paper supplies a DHSP solution.

The biggest research risk is now impact, not another nearby matrix identity.
An exposed small orbit module, bounded-degree polynomial, power product or
guarded pencil norm remains subject to the existing classical filters.
Formal degree, a large orbit and failure of a few attacks are not hardness.

Next: close native source/terminal recovery at the same access model, then
require either a genuinely new algorithmic theorem after specialist novelty
review or a natural application surviving matched classical analysis. A
growing-rank class-three family is a cleaner scope test than another fixed
tiny group, but an oracle-only test is not the desired application.

Do not build another generic workbench, extrapolate finite fixtures, or
integrate a speedup status from this note. Gemini can wire the already
checked artifacts once repository migration is verified; the unresolved
application and novelty questions need further mathematical work.
