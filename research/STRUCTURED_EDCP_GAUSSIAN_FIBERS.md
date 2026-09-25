# Structured EDCP: A Native Gaussian Fiber Readout

Date: 2026-09-24. LOCAL DERIVATION / REVIEW PENDING.

This note specifies a constructive, precision-charged measurement for ONE
coefficient block. It does not supply a multi-block algorithm, a successful
LWE attack, a verified reduction, or a novelty claim. The construction is
derived below; bounded references check its identities but do not constitute
a gate implementation or an independent proof review.

## 1. Research Decision

Keep the coefficient registers of structured EDCP. Their one-block fibers
are tractable for a specific reason: carrying in base q gives a local chain.
Generic subset-sum fiber preparation is not necessary for this block.

The next high-upside target is the weighted modular fiber for independently
labeled blocks. TWO blocks give the first structural prototype, but are not
automatically information-sufficient. The follow-up in
`research/STRUCTURED_EDCP_INFORMATION_THRESHOLD.md` proves both a necessary
entropy bound and a constant-block sufficient-information bound in a scoped
growing regime. It rules out two-block full uniform-secret recovery in the
Gaussian regimes studied there. Retain this prototype only as a possible
composable operation or for an explicitly different secret prior. Merely
implementing the one-block readout is a baseline, not the research objective.

The source is Definition 22 of
[Wen and Zheng, ePrint 2026/155](https://eprint.iacr.org/2026/155.pdf).
Its reduction parameters remain subject to the audit in
`research/EDCP_CORRELATED_CENTER_AUDIT.md`. Optimal coset-state measurements
and the distinction between a measurement formula and its implementation
are established themes; see
[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
The elementary specialization below is proved directly rather than assumed
to follow from either citation.

## 2. Exact Finite Source

Let q>=3, d>=2, Q=q^d+1, and E(c)=sum_i q^i c_i mod Q. Use a known positive
amplitude h(c)=exp(-pi*||c||^2/sigma^2), sigma>=1. After the source's second
register is Fourier-measured, one block has the form

    |Psi_z> = G^(-1/2) sum_{c in [-R,R]^d} h(c) omega_Q^{z E(c)} |c>,
    G = (sum_{j=-R}^R exp(-2*pi*j^2/sigma^2))^d.

Here z=<a,s> mod Q, for the actual public label a. For the measurement
optimality statement, z is uniform in Z_Q. This is not automatically the
full secret s when its module rank is greater than one, and a nonuniform
secret prior requires a separate discrimination analysis.

R is a charged input truncation, not an oracle promise silently added to
the original source. Section 6 accounts for it. The amplitude must be known:
unknown-center or unknown-phase sources do NOT inherit this compiler.

SOURCE CONVENTION: sigma here is an AMPLITUDE width. The paper's Definition
22 uses sqrt(D_r), hence sigma=sqrt(2)*r under its Definition 10, whereas
its displayed reduction state (26) uses rho_r, hence sigma=r. The follow-up
information note records this discrepancy. Do not substitute widths without
tracking the convention through the source reduction.

## 3. Exact Carry Lattice

Let S be the signed cyclic shift on Z^d:

    S e_i = e_(i+1) for i<d-1; S e_(d-1)=-e_0.

Set B=q I-S. Its first d-1 columns are q e_i-e_(i+1), and its last column is
q e_(d-1)+e_0. Thus E(Bk)=0 mod Q and det(B)=q^d+1=Q. Since E is surjective,
these columns give the ENTIRE kernel lattice of E, not just a sublattice.

For residue u choose a canonical representative t(u): use its d ordinary
base-q digits when 0<=u<q^d; for u=q^d choose (-1,0,...,0). Then every fiber
element has the unique representation c=t(u)+Bk. In coordinates,

    c_0 = t_0 + q*k_0 + k_(d-1),
    c_i = t_i + q*k_i - k_(i-1), 1<=i<d.

The PLUS sign at the cyclic boundary is essential. Using a minus sign changes
the modulus to q^d-1. At q=3,d=2, (1,3) is a kernel vector modulo 10,
whereas (-1,3) is not.

Since ||S||_infinity=1, the convergent inverse series gives

    ||B^(-1)||_infinity <= 1/(q-1).

Consequently every supported carry satisfies

    ||k||_infinity <= (R+q-1)/(q-1).

Use K=ceil((R+q-1)/(q-1)). This bounds ALL relevant carries and does not
assume that the coefficient evaluation is injective.

There is also a direct exact inverse useful for uncomputation. Set r=c-t(u).
Then k_(d-1)=sum_i r_i q^i / Q is an integer, and recurse
k_(i-1)=q*k_i-r_i from i=d-1 down to 1. Finally check
r_0=q*k_0+k_(d-1). Arithmetic is polynomial in the register bit lengths.

## 4. Weighted Fiber Preparation

Define w(x)=exp(-2*pi*x^2/sigma^2) when |x|<=R, and zero otherwise. The
unnormalized probability mass in a fiber is

    F(u) = sum_{k in [-K,K]^d}
             w(t_0+q*k_0+k_(d-1))
             prod_{i=1}^{d-1} w(t_i+q*k_i-k_(i-1)).

Fix k_(d-1)=b. The remaining sum is a nearest-neighbor chain. A forward
dynamic program uses

    D_0(k) = w(t_0+q*k+b),
    D_i(k) = sum_h D_(i-1)(h) w(t_i+q*k-h).

At the final step restrict k=b. Sum the final weight over b. There are
O(d*(2K+1)^3) arithmetic operations. No array indexed by all Q residues is
needed; u is a binary input of O(d log q) bits.

Forward/backward chain messages also prepare the normalized pure fiber

    |phi_u> = F(u)^(-1/2) sum_{E(c)=u, |c_i|<=R} h(c)|c>.

First prepare b with amplitude equal to the square root of its chain weight
divided by F(u). Then prepare k_0,...,k_(d-2) using the successive conditional
probabilities from the backward messages, and set k_(d-1)=b. The amplitudes
telescope to h(t+Bk)/sqrt(F(u)). Compute c=t+Bk and erase k with the exact
inverse above. All work tables are known functions of u and can be uncomputed.

This describes a uniform coherent isometry V: |u>|0> -> |u>|phi_u>.
For F(u)=0, define an arbitrary fixed output branch; actual inputs have no
weight there. Compute support flags with exact integer predicates, not a
floating-point underflow test.

PRECISION: every nonempty fiber contains a term of weight at least
exp(-2*pi*d*R^2/sigma^2); there are at most (2K+1)^d terms. Hence polynomial
precision in d*R^2/sigma^2, d log(2K+1), and log(1/epsilon) suffices for
relative normalization and conditional rotations. Zero weights remain exact.
Reversible arithmetic and rotations add polynomial bit-complexity factors;
they are not free unit-cost real-number operations. The uniform error bound
must hold over supported u, including low-mass fibers. Because the operation
is controlled blockwise by u, there is no extra factor Q in its operator error.

For R=O(sigma*sqrt(log(d*sigma^2/eta))), the carry range is
O(1+(sigma/q)*sqrt(log(d*sigma^2/eta))). In particular, polynomial sigma/q
and polynomial parameter bit lengths give a polynomial-size compiler. This
is an arithmetic construction, not an executed quantum circuit or a claim
that arbitrary discrete Gaussian cosets are efficiently preparable.

## 5. Optimal One-Block Readout

Compute E(c) coherently into a new register. The supplied state becomes

    sum_u sqrt(p_u) omega_Q^{zu} |u>|phi_u>,  p_u=F(u)/G.

Apply V^dagger controlled by u. The coefficient register clears, leaving
sum_u sqrt(p_u) omega_Q^{zu}|u>. An inverse QFT over Q followed by measurement
identifies z with probability

    P_one = (sum_u sqrt(p_u))^2 / Q.

This is optimal for the uniform-z ensemble. Proof: average any POVM over the
known phase action. The seed effect then has diagonal entries 1/Q on occupied
fibers. Positivity bounds each off-diagonal magnitude by 1/Q, so its success
is at most the displayed expression. A rank-one Fourier seed attains it.
An equivalent dual certificate is diag(L*sqrt(p_u)/Q), where
L=sum_u sqrt(p_u); domination of |sqrt(p)><sqrt(p)|/Q follows from weighted
Cauchy-Schwarz. The prior's support and all source outcomes are retained.

Crucially, the compiler does not enumerate p_u or evaluate P_one. It only
computes fiber messages for the coherently supplied u. Enumerating all Q
values to report P_one is an exponential reference calculation, not the
claimed implementation.

Optimal measurement does NOT mean successful decoding. When 2R<=q-1,
evaluation is injective on the coefficient box: its integer range has width
less than Q and distinct base-q digit differences cannot cancel. Therefore

    P_one = kappa_R^d / (q^d+1),
    kappa_R = (sum_{j=-R}^R exp(-pi*j^2/sigma^2))^2
                / sum_{j=-R}^R exp(-2*pi*j^2/sigma^2)
            <= 2R+1.

If 2R+1<=(1-delta)*q for fixed delta>0, every one-block measurement has
exponentially small exact recovery probability. This is an exact finite-box
statement, not an uncharged asymptotic approximation to an infinite Gaussian.
It does not bound partial information or multi-block measurements.

## 6. Input Tails And Total Error

For the untruncated normalized product Gaussian, a union bound and a Gaussian
tail integral give, for integer R>=1,

    eta_actual = Pr[max_i |c_i|>R]
      <= d*sigma^2/(2*pi*R) * exp(-2*pi*R^2/sigma^2).

For example, R=ceil(sigma*sqrt(log(max(e,d*sigma^2/eta))/(2*pi))) makes the
right-hand side at most eta for sigma>=1, 0<eta<1. The support check is a
heralded projection with secret-independent acceptance. Conditioned on it,
the preceding compiler applies exactly in the ideal arithmetic model.

The original pure state and its normalized truncation differ in trace
distance sqrt(eta_actual), not eta_actual. Thus, with an additional circuit
error epsilon, this supplied measurement is within at most
sqrt(eta)+eta+epsilon of the optimal full one-block success. Any reduction
source error must be added separately. Tiny optimal successes cannot be
estimated reliably by ignoring a larger additive tail or arithmetic error.

## 7. The Actual Next Target: Two Independent Blocks

Consider scalar module rank one, and condition on an invertible first public
label. This is a checkable event whose probability must be charged under
the actual modulus. Renormalize the secret and write the second multiplier
as a. The desired joint fiber is

    E(c_1)+a*E(c_2)=u mod Q,
    amplitude proportional to h(c_1)h(c_2).

Write the canonical digits of a as a polynomial a(X), and let T_a be its
negacyclic multiplication matrix modulo X^d+1. Then

    E(T_a v)=a*E(v) mod Q,
    c_1=t(u)-T_a*c_2+B*k.

This is an exact Gaussian-weighted lattice fiber in variables (k,c_2):

    exp(-pi*(||t(u)-T_a*c_2+B*k||^2+||c_2||^2)/sigma^2).

For a natural random a, T_a is generally dense. The one-dimensional carry
chain proof no longer supplies a small dynamic program. Constructing this
coherent normalized fiber, with natural coverage and charged precision, is
the research question, not an assumed subroutine.

Both B and T_a are polynomials in S, so they commute and share the complex
Fourier eigenbasis of the signed cycle. This is exploitable algebraic
structure, but diagonalizing a REAL quadratic form does not factor its sum
over INTEGER vectors. That Fourier basis rotates the integer lattice; it
is not an integer-register relabeling. Any proposed Gaussian/Fourier solver
must preserve this lattice and its carries or explicitly charge the change.

EASY ALIGNMENT CONTROL: if a=q^j mod Q, then T_a is a signed coordinate
permutation. The orbit <q> has exactly 2d elements modulo Q. Given a uniform
second label, after conditioning on an invertible first label, its chance of
being in this orbit is 2d/Q. If also conditioning the second label to be a
unit, the chance is 2d/phi(Q). Selecting these pairs from polynomially many
natural inputs is not a free source of easy joint fibers. A signed rotation
of one existing state does not create another independent copy.

SUPPORT THRESHOLD, NOT SUFFICIENCY: L blocks with box support [-R,R]^d,
for a uniform rank-n secret in Z_Q^n, have optimal success at most
(2R+1)^(d*L)/Q^n by the dimension bound for a uniform pure-state ensemble.
For constant n and polynomial q,R, the necessary L can be constant.
This motivates attacking a few genuinely independent blocks. It does not
prove adequate natural information, an efficient measurement, or a valid
LWE parameter regime at that L.

FOLLOW-UP: `research/STRUCTURED_EDCP_INFORMATION_THRESHOLD.md` now supplies
a sufficient-information bound for constant L under explicit power-of-two
degree, digit-support, collision-entropy, and parity-rank premises. It also
strengthens this necessary bound to kappa^(d*L)/Q^n, which applies even to
untruncated Gaussian digits. Two blocks can be far below the necessary
information threshold. The joint compiler is still unsolved; the newer
information result does not retroactively supply it.

Classical baselines must include lattice decoding and weighted fiber search
on these SAME natural instances. A fast sampler that is already classical
can be useful, but does not by itself establish a quantum speedup. Nor does
an explicit optimal measurement imply a classical simulation of its unknown
quantum input.

## 8. Checks Actually Executed

Eight complete finite coefficient-box references were used:

| q | d | R | sigma | Occupied Fibers | P_one |
|---|---|---|---|---:|---:|
| 3 | 2 | 1 | 1.2 | 9 | 0.2146347738 |
| 3 | 2 | 3 | 2.0 | 10 | 0.6846378320 |
| 3 | 4 | 2 | 1.5 | 82 | 0.1918801926 |
| 5 | 2 | 1 | 1.2 | 9 | 0.0825518361 |
| 5 | 2 | 4 | 2.5 | 26 | 0.4653953707 |
| 5 | 4 | 1 | 1.3 | 81 | 0.0115784935 |
| 5 | 4 | 3 | 2.0 | 626 | 0.1000665716 |
| 7 | 2 | 2 | 1.8 | 25 | 0.1264109541 |

- Enumerated 3280 coefficient vectors and all 1456 residue fibers across
  these references. Carry dynamic programs matched direct positive sums
  with maximum residual 2.78e-17; normalization residual was 4.45e-16.
- Every one of those 3280 vectors passed exact carry inversion and the K
  bound. The wrong boundary sign failed the explicit modulus-10 control.
- Direct fiber inner products, compressed amplitudes and Fourier success
  matched for z=0,1,Q-1 in every reference. Maximum amplitude residual was
  2.23e-16. These were exact-table reference isometries, NOT a compiled
  sequential-rotation circuit. That circuit remains a Gemini task.
- A separate backward-message implementation checked all 3280 sequential
  conditional amplitudes in 868 nonempty fibers; the other 588 fibers were
  exactly empty. The smallest nonempty unnormalized mass was 3.7769248e-14.
  Maximum amplitude error was 1.00e-15 and normalization error 3.34e-16.
  This tests the proposed conditional probabilities, not a gate synthesis.
- In the cases Q<=50, the one-block dual matrices had minimum eigenvalues
  no less than -1.08e-17. The all-size optimality statement relies on the
  analytic positive-semidefinite argument, not finite eigenvalues.
- Checked 396 negacyclic multiplication identities at (q,d,R)=(3,2,1),
  (5,2,1),(3,4,1), with multipliers 1,2,floor(Q/2),Q-1. The multiplication
  matrices commuted with B and its determinant equaled Q.

For two blocks, exact positive convolution references exhausted every unit
multiplier at three parameter points. These tables enumerate the whole
residue space and are NOT scalable decoders:

| q,d,R,sigma | Unit Multipliers | Mean Optimal Success | Aligned Mean | Other Mean |
|---|---:|---:|---:|---:|
| 3,4,1,1.3 | 40 | 0.2305268447 | 0.1635605796 | 0.2472684110 |
| 5,4,1,1.3 | 312 | 0.0608052647 | 0.0265456596 | 0.0617068333 |
| 7,2,2,1.8 | 20 | 0.4637348103 | 0.2444013287 | 0.5185681807 |

The easier aligned fibers had less information in these references. This is
a scope control, not an asymptotic theorem or evidence of a speedup. No
production tests, CLI runs, registry acceptance, or new commit occurred.

## 9. Division Of Work

GEMINI: implement `theorems/structured_edcp_gaussian_fibers.py` and focused
tests. Start with exact carry coordinates, positive transfer messages,
sequential conditional amplitudes, and coherent small-reference uncomputation.
Do not allocate Q-sized tables in the claimed scalable path. Keep them only
in bounded tests. Include zero fibers, the exceptional representative u=q^d,
all boundary signs, tail mass, low-mass relative accuracy, and unknown-center
rejection. Record single-block optimality separately from recovery success.
Do not promote a candidate merely because the baseline matches dense tables.

MAIN MODEL: analyze the random-multiplier two-block lattice above and its
classical baselines, or find a different collective observable that avoids
full fiber preparation. Prove natural-instance information bounds before
interpreting small success values. Audit the full module-LWE parameter
connection before attaching a cryptographic or speedup conclusion.
