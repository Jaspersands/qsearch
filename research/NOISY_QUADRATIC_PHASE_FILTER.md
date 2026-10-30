# A stronger direct competitor for noisy quadratic phases

Date: 2026-10-30. Status: constructive mathematical competitor with bounded
measurement controls, not a scalable executed learner or established novelty.
Derived by reviewer Beauvoir during the
[exterior phase-source audit](EXTERIOR_NOISY_PHASE_LEARNING.md).
Reviewer Boole independently checked both candidate/verifier proofs, their
resource scaling, and explicit counterexamples to overgeneralizations.

**Follow-up:** [peak-weight and unknown-basis learning](PEAKED_PHASE_NOISE_LEARNING.md)
extends the SWAP-verified method to full-rank noise and arbitrary unknown
stabilizer bases under a stronger quantitative peak promise. The
sample-only flat validator is not automatically extended.

## Exact source and target

The input consists of IID copies of

    rho = sum_(b in B) w_b |psi_(q+b.x)><psi_(q+b.x)|,
    q(x) = x^T A x/2 + ell.x,  A symmetric over F_p, p odd.

Recover A, not the unidentifiable linear phase ell. There is no conjugate
copy, chosen latent error, evaluation oracle, or source inverse.

Two alternative promises suffice:

- Exact uniform weights on known rank r with p not dividing r.
- Arbitrary weights and a known support upper bound R < p.

Ranks are polynomially bounded. All p dependence must be polynomial in its
bit length. This is a quantum-input learning problem, not ordinary classical
LWE. Quantum measurements below are paid, even when all later computation
is classical.

## Ordinary Bell sampling is not the argument

Absorb ell into the unknown labels for this paragraph. With the Bell basis
|Bell_(y,z)> = p^(-n/2) sum_x omega^(z.x)|x,x+y>, independent components
with labels b,c give

    Pr(y,z | b,c) = p^(-n-rank(A))
                    1_(z-Ay-b-c in image(A)).

For invertible A it is completely uniform. Differences of two independent
ordinary Bell outputs remain uninformative. Supplying a conjugated second
copy would change the equation, but that is not the input model.

This is consistent with the known odd-prime limitations in
[Allcock et al., Sections 3 and 4.2](https://arxiv.org/html/2405.06357v1).

## Legal four-copy regression instrument

Choose one public nonzero vector a in F_p^4 satisfying

    sum_i a_i = 0,    sum_i a_i^2 = 0.

For example, a=(1+h,1-h,-1+k,-1-k) with h^2+k^2=-2. The conic has p+/-1
solutions; randomized field sampling and square roots find one in expected
polynomial time in log p. Cap the search under a separate failure budget
and verify the two equations. In odd characteristic this construction
cannot produce the zero vector. Fix a throughout candidate and validation
sampling; changing its distribution would invalidate the rational-count
argument below.

Acquire FOUR fresh copies, with independent unobserved labels b_i. Append
a uniform n-variable t register, reversibly map x_i to x_i-a_i t, and
measure those four registers as mu_i. The mu_i are jointly uniform even
conditional on all labels, because the full premeasurement amplitudes
have uniform modulus. The retained phase is

    sum_i [q(mu_i+a_i t)+b_i.(mu_i+a_i t)]
      = constant + t.(A sum_i a_i mu_i + sum_i a_i b_i).

The quadratic and common linear-in-t nuisance terms cancel. An inverse
Fourier measurement therefore yields the paid classical sample

    y = sum_i a_i mu_i,    z = A y + e,    e = sum_i a_i b_i.

y is uniform and independent of e. In particular,

    Pr(e=0) >= sum_b w_b^4 >= R^-3.

The first inequality counts the event that all four independent labels
happen to coincide. The algorithm does not request or herald that event.
With uniform rank r replace R by r. Any zero a_i is still a consumed input
in this conservative four-copy account.

## Candidate verification by paid SWAP tests

For each candidate (y,z), implement the KNOWN Pauli W=Z_z X_y. Let
f=z-Ay, a quantity used only in the proof, never given to the verifier.
With w extended by zero to F_p^n,

    Tr(rho W rho W^dagger) = sum_b w_b w_(b-f),
    Tr(rho^2)-Tr(rho W rho W^dagger)
      = (1/2) sum_b (w_b-w_(b-f))^2.

Both traces can be estimated using fresh input pairs and controlled SWAPs.
In the uniform case the difference is zero for f=0 and at least 1/r^2
otherwise: equality at f!=0 would make B invariant under a translation of
order p, forcing p to divide r. Estimate to a small constant fraction of
this gap, including a separately estimated purity when necessary.

For arbitrary weights with support <=R<p, put
E_f=sum_b(w_b-w_(b-f))^2. Every supported point reaches a zero within at
most R steps along nonzero f. Telescoping and Cauchy-Schwarz give
w_b <= sqrt(R E_f). Summing over at most R points gives
1 <= R sqrt(R E_f), so E_f >= R^-3. Thus the trace gap is at least
1/(2R^3), independent of the smallest positive weight.

Take T=O(R^3(n+log(1/delta))) independent candidates. Chernoff gives enough
zero-error candidates with high probability. Their y values remain
independent uniform vectors; n+O(log(1/delta)) span F_p^n with high
probability. Verify all T candidates to accuracy O(R^-3) with
O(R^6 log(T/delta)) trials each, then solve A=Z Y^-1 from a basis of
accepted columns. A wrong acceptance or rank failure is charged globally.

Conservative original-copy cost is O-tilde(R^9(n+log(1/delta))). For exact
uniform noise the stronger verifier gap gives O-tilde(r^7(n+log(1/delta))).
Bit arithmetic, controlled Paulis/SWAPs, register sizes, Fourier precision,
and the conic-search clock must also be paid. These are loose polynomial
bounds, not practical performance estimates.

## Uniform case: entirely classical validation after the instrument

The exact uniform promise yields another competitor which uses no new
quantum verification queries. Generate a separate independent validation
batch (Y,Z) from the SAME fixed four-copy instrument. For a candidate (y,z)
compute its symplectic pairing with each validation sample:

    y^T Z - z^T Y = y^T E - (z-Ay)^T Y.

Symmetry of A is essential. If z!=Ay, this scalar is exactly uniform in
F_p, since Y is uniform and independent of E. Its zero probability is 1/p.
If z=Ay, its zero probability is k/r^4 for an integer k, and is at least
r^-3. Because p does not divide r, it cannot equal 1/p. Quantitatively,

    |Pr(pairing=0) - 1/p| >= 1/(2r^7).

If p>2r^3 use the atom >=r^-3. Otherwise use the rational separation
1/(p r^4)>=1/(2r^7). The correct-candidate probability may be on either
side of 1/p; test absolute deviation, not a one-sided excess.

A shared INDEPENDENT batch of O(r^14 log(T/delta)) samples estimates all
T fixed candidate probabilities simultaneously by Hoeffding and a union
bound. Classify at half the separation and solve A by Gaussian elimination.
Reusing the validation batch is legal: condition on the whole independent
candidate set first. Adaptively proposing candidates from the validation
outcomes is not justified by this bound.

The source cost is 4(T+L) for L validation samples, NOT 4TL. Straightforward
classical validation still costs O(nTL) field operations. This is a loose
polynomial existence bound, not an efficient practical implementation.

This is polynomial classical postprocessing of a paid four-copy quantum
instrument. It is NOT a classical dequantization of the original source.
Arbitrary real weights destroy the rational-denominator separation and
require the SWAP verifier or another proved method.

Two explicit falsifiers make these qualifications substantive. At p=3,
B={0,1}, a=(2,0,2,2), and true candidate y=1, uniform weights give zero
probability 1/4<1/3: a one-sided test would reject a correct candidate.
Weights (1/3,2/3) instead give probability 1/3, indistinguishable from
wrong candidates by this statistic. The weighted SWAP verifier survives
that example; the sample-only zero-frequency verifier does not.

## Falsifiers and prior-art boundary

- If p divides r, periodic supports can hide the quadratic phase entirely.
- Arbitrary weights with R>=p can approach such periodic supports by an
  arbitrarily small tail; no weight-independent rank-only guarantee follows.
- Arbitrary nonsymmetric regression matrices do not satisfy the symplectic
  cancellation used for sample-only verification.
- Coherently reused latent noise, non-IID copies, higher-degree phases,
  unknown computational coordinates, and approximate model violations are
  outside this proof.
- Finite success cannot establish novelty or an advantage for a useful
  classical-input problem. This removes a candidate application for Rees;
  it does not invalidate the general Rees theorem.

Quadratic cancellation and pure-qudit learning are established techniques.
[Tang and Steckmann, Section VI](https://arxiv.org/html/2610.03307v1#S6)
provides a close candidate-verifier precedent for noisy qubit stabilizer
structure. An exact primary-source subsumption of the growing-prime,
finite-support theorem above has not been established in this audit.
Do not advertise a priority claim based on an unsuccessful literature search.

`tests/test_exterior_phase_learning.py` checks the actual ordinary-Bell
failure, the four-copy amplitude/Fourier law, weighted density-matrix
overlaps, centroid decoupling and exact classical-verifier probabilities.
It does not execute a scalable full noisy learner or an external experiment.
