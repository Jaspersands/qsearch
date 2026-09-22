# DCP Label Information: Prior-Work Barrier And Joint-Slice Audit

Status: physical finite controls and a derived extension, REVIEW PENDING.
No decoder, novelty claim, general DCP impossibility or formal verification.

## Why This Changes The Next Experiment

Gupte, Ragavan and Zhandry, [ePrint 2026/1693](https://eprint.iacr.org/2026/1693),
Theorem 1.1, bound the parity distinguishability left after the standard
low-subset-sum measurement when each Fourier label is replaced by a fixed
small digest. Their argument is information-theoretic: an inefficient optimal
measurement cannot recover information that has already been discarded.
The paper also applies this to Simon's proposed DCP algorithm, not merely to
an independence assumption in its analysis. Hence repairing that older proof
gap is not the next constructive task without first escaping the newer bound.

The downloaded ten-page PDF has SHA256
`66757d5e7ac99b4d30a4d6e7926185c370bcbcc7362fc0ae2f85caa65410c50d`.
The accompanying [Lean repository](https://github.com/sragavan99/lean-ePrint-2026-1591-refutation)
was inspected at commit `6de8c1dbffec10b4b44b2cae3aeadeb1cf0cfc83`.
The local machine has no Lean toolchain; this pass did NOT replay its proofs.
Absence of `sorry` in a source scan is not a verification claim. The inspected
main theorem is coordinatewise; it does not certify the extension below.

## Physical Experiment And Scope

Let N=2^n, m independent uniform public labels y_i in Z_N, and b in {0,1}^m.
Prepare the supplied DCP phase states. Compute f_y(b)=sum_i y_i b_i mod N,
measure its low n-1 bits z, and retain b and h, its highest bit.
For secret parity d, the branch vector has amplitudes (-1)^(d h).
The global factor depending on z cancels in each density matrix.

Retain a deterministic classical summary H(y), fixed before seeing labels,
measurements or the secret. H may depend jointly on ALL labels. The observer
has H(y), z and the physical quantum registers b,h. It has no other
label-dependent workspace, oracle, side information or later label access.
Public independent randomness can be conditioned on and averaged, but is not
silently treated as a hidden selector. All failures have their Born mass.

The cq state is the sum of the unnormalized outer products in each
(H(y),z) block, divided by 2^m N^m. It is NOT the uniform average of
individually normalized z branches. Computationally dephasing every b bit
makes this state independent of d.

## Conditional-Slice Extension

This is a direct adaptation of the paper's dephasing proof, not a claimed
novel result. For coordinate i and fixed other labels u=y_-i define

    c_(i,u,a) = |{t in Z_N : H(u with coordinate i=t)=a}|,
    beta_i = E_u [sum_a sqrt(c_(i,u,a)) / N].

Then, for normalized trace distance T,

    T(rho_d, dephase_i(rho_d)) <= beta_i / 2,
    T(rho_0,rho_1) <= min(1, sum_i beta_i).

Proof: reveal y_-i in an extra classical register; forgetting it is a channel.
Fix its value u. For each z,a block the off-diagonal part between b_i=0 and
b_i=1 factors as |v_0><v_1| plus its adjoint. The vector v_0 is independent
of y_i, hence independent of which digest fiber was selected. The vector v_1
sums over y_i in that fiber. For fixed z, different y_i terms in v_1 have
disjoint computational support: equal b,h,z with b_i=1 determines y_i.
Consequently

    sum_z ||v_0||^2 = 2^(m-1),
    sum_z ||v_1(a)||^2 = c_(i,u,a) 2^(m-1).

The trace norm of each off-diagonal block is 2||v_0||||v_1||. Applying
Cauchy--Schwarz over z, dividing by 2^m N and averaging u bounds its trace
norm by beta_i, or normalized distance by beta_i/2. Earlier dephasings
contract subsequent differences. Telescope all coordinates for each secret
and use their common fully dephased endpoint. This gives sum_i beta_i, with
no missing factor of two. Retaining z throughout is essential to the proof.

For at most K_i values on every slice, beta_i<=sqrt(K_i/N). For fixed
coordinatewise k_i-bit digests this reproduces sum_i 2^((k_i-n)/2).
The fiber-size expression can be strictly sharper for unbalanced digests.
A joint digest's GLOBAL alphabet alone may give a valid but useless bound;
do not divide its total bit length among the m coordinates. For example,
H(y)=sum_i y_i mod N has N singleton fibers on EVERY slice. Its beta_i=1,
even though it records only n bits total. The present bound is vacuous there.
That is not evidence that this summary enables useful decoding.

## Refinement: Dependence On The Measured Low Sum

Trying to falsify the extension exposed an overly cautious proposed scope
limit. A summary H(y,z) depending on the ALREADY MEASURED low sum can also be
bounded, but not by silently reusing the fiber-size formula above.

Fix i,u. Let A_u(z) count assignments with b_i=0 and low sum z; these do not
depend on y_i and sum to 2^(m-1). Let

    K_i(u,z) = |{H(u with coordinate i=t,z) : t in Z_N}|,
    gamma_i = E_u sqrt(sum_z A_u(z) K_i(u,z) / (2^(m-1) N)).

Then T(rho_d,dephase_i(rho_d))<=gamma_i/2 and the two-parity distance is at
most min(1,sum_i gamma_i). To see this, form v_1(a,z) with the z-specific
fibers. Distinct y_i terms still have disjoint support. Although its old
per-a norm identity no longer holds, the complete partition obeys

    sum_(a,z) ||v_1(a,z)||^2 = N 2^(m-1),
    sum_(a,z) ||v_0(z)||^2 = sum_z K_i(u,z) A_u(z).

One Cauchy--Schwarz inequality over the PAIRS (a,z), followed by the same
normalization and hybrid, proves the bound. Empty v_1 blocks merely loosen
the estimate. A uniform slice-range cap K still gives m*sqrt(K/N), including
coordinatewise small digests whose functions depend on z. This is a separate
review-pending derivation, NOT a statement imported from the inspected Lean
theorem. Random z-dependent joint maps and independent complex preparations
check the refined physical law and every coordinate estimate.

This does not permit arbitrary later measurement records: a measured
Hadamard string or retained label-sensitive quantum workspace changes the
experiment. The original algorithm's later adaptive partition is not repaired
by this observation; the paper's separate reconstruction argument must be
analyzed on its own terms.

## Independent Controls And Failure Modes

The workbench constructs all physical cq blocks with integer counts. Its
source normalization and fully dephased equality are exact. Eigenvalue-based
trace norms are numerical, explicitly not proof certificates. A separate
test prepares complex DCP phase vectors before the low-bit measurement and
compares the resulting block matrices, including an odd secret other than 1.
Bounds use outward dyadic square roots of exact fiber counts; the scaling
formula uses integer arithmetic and is not fitted to small experiments.

Controls include discarded labels, coordinate high bits, a joint high-bit
sum, the complete joint sum, full labels, uneven fibers and arbitrary random
joint tables. They check the SINGLE-coordinate estimate as well as the final
parity bound. Full-label matrices provide a data-processing comparison, not
an efficient decoder or classical sampler. Exhaustive source enumeration is
exponential; only a finite diagnostic is implemented by that path.

The derivation would be invalid if:

- The labels were correlated, nonuniform, selected or silently conditioned.
- H depended on z but used the old per-a fiber identity rather than the
  separate conditional-range proof; or H depended on a later measurement
  outcome for which the source law and b register had changed.
- A retained quantum workspace had already used label information absent
  from H, or later operations could access those labels again.
- The low-bit subset sum remained coherent, or the physical prefix changed.
- Success were normalized on a rare branch without charging its probability.
- An ideal optimized trace distance were described as an efficient readout.

The scope checker requires explicit literal-true premises; it does not prove
that a supplied circuit really factors through the declared summary. Keeping
an unused full-label register also does not rescue a procedure whose output
factors through a lossy digest. Conversely, this audit does NOT require every
DCP algorithm to follow this prefix or to store all labels separately.

An explicit excluded-prefix control confirms that the caveat is substantive:
before measuring the low sum, discard the label of one DCP qubit. Secret 0
gives |+><+| and secret 1 gives I/2, at distance 1/2, which exceeds the
post-prefix cap 1/sqrt(N) for N>4. This is a fixed-pair calibration, NOT a
parity solver for a uniformly unknown secret. The obstruction cannot be
transferred to a different physical prefix simply because labels are lost.

## Constructive Next Target

Do not continue variants of the old proposal using only stable high-bit
summaries unless an explicit operation falls outside the factorization.
The next candidate needs a full-label-sensitive coherent matching or
uncomputation rule, with its actual circuit, source-average success and cost.
Dependence on the measured low sum alone is NOT a sufficient escape. More
general measurement-dependent joint summaries need a new physical argument,
not an automatic positive classification. A next experiment must account for
their computation and demonstrate surviving parity information on natural
input laws. Compare with the existing generic quantum sieve and same-access
classical baselines. The repaired witness reduction supplies no uniform-fiber
requirement and no automatic construction from a classical witness finder.

Run `python qsearch.py dcp-label-digest-audit` or
`python qsearch.py run EXP-DHS-DCP-LABEL-DIGEST-AUDIT`.
