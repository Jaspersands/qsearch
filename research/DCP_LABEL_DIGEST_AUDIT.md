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

## Exact Complete-Joint-Sum Case (2026-09-23)

NEW LOCAL DERIVATION / REVIEW PENDING. The general slice bound above remains
vacuous for H(y)=sum_i y_i mod N; do not change its formula or its regression
test to disguise that limitation. A different, exact physical calculation
settles this specific digest. It does NOT settle arbitrary joint summaries.

Use precisely the earlier prefix and source law, retaining only

    S=sum_i y_i mod N, z, and the quantum registers b,h.

No other label-sensitive workspace or later label access is available. Let
M=2^m, q=M-2, v=M-4, with m>=2 and N=2^n. The parity trace distance is

    T = 2/(M*N^3) * [sqrt(v^2+2*N^2*q)
                     +(2*N-4)*sqrt(v^2+N^2*q)
                     +(N^2-3*N+3)*v + N^2 + q*N^2/2].      (J1)

In particular, for EVERY batch size,

    T <= min(1, 4/N).                                      (J2)

For m=1, S is the full single label and T=1/N directly. For N=2 the formula
gives T=1-1/M; (J2) is then only the trivial cap. The useful claim concerns
growing n. Even an optimal inefficient measurement has equal-prior success
at most 1/2+2/N after this digest/prefix. Independently repeating this exact
lossy experiment polynomially many times cannot restore constant advantage:
the trace distance of a product of R repetitions is at most R*T.

### Count The Physical Off-Diagonal Block

For fixed (S=s,z), let C_(s,z)[b,c] count label tuples satisfying

    sum_i y_i=s,    b dot y=z,    c dot y=z+N/2    (mod N).

These are the h=0 to h=1 entries. Their physical normalization is M*N^m;
the parity distance is 2*sum_(s,z)||C_(s,z)||_1/(M*N^m), not a uniform
average of normalized branches.

If the column patterns (b_i,c_i) contain at least three of the four Boolean
pairs, the three equations have a unit 3-by-3 minor. Their solution count is
N^(m-3), for every right-hand side. The remaining cases are exactly equal
rows, complementary rows, or a constant row. Equal rows cannot satisfy the
two distinct frequency values. Nonconstant complementary rows have count
N^(m-2) precisely when s=2z+N/2 mod N, and otherwise zero.

Remove b=0 and b=1^m from the core, leaving q indices. Let P exchange each
nonconstant bit string with its complement, J be the all-ones matrix, and
I_D the indicator of s=2z+N/2 mod N. Set a=N^(m-3). The core is

    a * [J - I + (N*I_D-1)*P].

Its uniform-vector eigenvalue is a*(q-2+N*I_D). On the uniform-orthogonal
P=+1 subspace the eigenvalue is a*(N*I_D-2), with multiplicity q/2-1;
on P=-1 it is -a*N*I_D, with multiplicity q/2.

All boundary couplings touch only the uniform core vector. In row/column
order (0,1^m,uniform core), the remaining small block, divided by a, is

    [ 0, N^2*[z=0,s=N/2], N*sqrt(q)*[z=0]       ]
    [ 0, 0,                 N*sqrt(q)*[s=z]       ]
    [ 0, N*sqrt(q)*[s=z+N/2], q-2+N*I_D          ].

Brackets denote indicators. The zero first column reflects the impossibility
of a zero bit string having h=1. This boundary is not negligible at small m.
For m=2 the generic three-pattern case is absent; the same expression works
algebraically with a=1/N because J-I-P is zero. Actual counts remain integers.

For N>=4, the trace norms, divided by a, fall into six cases:

| Branch | Multiplicity | Norm / a |
|---|---|---|
| z=0, s=0 | 1 | sqrt(v^2+2*N^2*q)+v |
| z=0, s=N/2 | 1 | N^2+q*N |
| z=0, other s | N-2 | sqrt(v^2+N^2*q)+v |
| z>0, s=2z+N/2 mod N | N/2-1 | q*N |
| z>0, s=z or s=z+N/2 | 2*(N/2-1) | sqrt(v^2+N^2*q)+v |
| z>0, all other s | (N/2-1)*(N-3) | 2*v |

Adding the table gives (J1). For N=2 only the z=0 cases are needed and give
the stated separate simplification. Bounding each square root by the sum
of its nonnegative components gives

    T <= [3*M-8+4*sqrt(M-2)]/(M*N) < 4/N,

where 4*sqrt(M-2)<=M+2 follows by completing a square. This proves (J2)
without extrapolating finite data. No lower bound on arbitrary DCP circuits
or on measurements retaining the original labels follows.

### Focused Verification And Interpretation

The existing physical-observation counter was used as an independent
enumerator, without changing production code or running its pipeline. Every
off-diagonal count matrix matched the above rank/case formula exactly.
Summed singular values then matched (J1) within 1e-12:

| n | m | Exact-count numerical T |
|---|---|---|
| 2 | 2 | .489276695296637 |
| 3 | 3 | .339843750000000 |
| 4 | 3 | .184731558212827 |
| 2 | 5 | .621066735070988 |
| 3 | 4 | .356198332987874 |

The n=3,m=3 closed form simplifies to 87/256. Twenty additional evaluations
of (J1) at n=4,8,16,32 and m=2,4,8,16,32 checked arithmetic consistency with
(J2); these were analytic formula evaluations, NOT large source simulations.

Four additional physical boundary controls give T=3/4 and 7/8 at N=2 with
m=2 and 3, and T=1/4 and 1/8 for m=1 at N=4 and 8. A separate complete
enumeration of the 4096 label tuples at n=3,m=4, RETAINING ALL LABELS,
gives optimal parity distance .7894538335103001, greater than 4/N=.5.
This deliberately violates the checksum-only premise and confirms that the
specialized upper bound cannot be transferred to full-label measurements.

This calculation closes the complete-checksum example that the slice proof
could not address. Its reason is not an illicit division of the n retained
bits among coordinates. The conditional fiber sizes of that old proof still
equal one, so every old beta_i remains one. A compact joint digest can evade
one bound without actually preserving useful information.

Gemini follow-up: add this exact specialized certificate to the existing
digest report, with its own evidence/status fields. Keep the slice cap and
the specialized cap separate. Reproduce the integer off-diagonal blocks,
boundary cases, Born normalization, m=1/N=2 controls and the full-label
countercontrol. Use outward-rounded roots for certified numerical caps.
Do not add a new candidate or broadly reject other joint digests, adaptive
summaries, retained workspace, or algorithms with a different physical prefix.

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
