# Structured EDCP: Sparse Block Moves And A Gaussian Tail Bottleneck

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

## 1. Decision

A natural next attempt is a Gibbs/Metropolis walk on the desired coefficient
fiber, updating one or a few entire blocks at a time. In the currently audited
large-modulus regime, this approach has a precise obstruction: with high
probability over the public labels, there are NO nontrivial such moves inside
the coefficient box. Truncating to that box makes the walk frozen. Extending
to the full Gaussian can reconnect it only through tiny stationary tail mass,
giving an exponentially small reversible-chain spectral gap on most fibers.

This is not a lower bound on arbitrary quantum algorithms. Nonlocal arithmetic
operations, changes of representation, and preparations allowed to leave the
fiber are not covered. It is a reason not to implement a generic local
conditional walk and assume that familiar quantum walk speedups solve the
missing core operation.

The proof uses an integer negacyclic norm, not a random-prime-modulus heuristic.
The power-of-two degree and composite modulus are explicit.

## 2. A Factorization-Free Bound On Sparse Kernel Relations

Let d>=2 be a power of two, q>=3, Q=q^d+1, L independent uniform scalar
labels a_l in Z_Q, and

    f(c)=sum_l a_l*E(c_l) mod Q,
    E(c_l)=sum_(i=0)^(d-1) q^i*c_(l,i).

Let Omega_R=[-R,R]^(d*L), with R a positive integer and 2R<=q-1.
A move from c to c' in this box that changes at most b blocks has difference
Delta_l in [-2R,2R]^d in at most b nonzero blocks, and must satisfy

    sum_l a_l*E(Delta_l)=0 mod Q.                            (1)

For any nonzero Delta in this coefficient range, multiplication by
Delta(X) on Z[X]/(X^d+1) has an integer d-by-d matrix T_Delta. Its columns
are signed rotations of Delta. Since X^d+1 is irreducible over Q for this
degree and deg Delta<d, det(T_Delta) is a NONZERO integer.

The adjugate identity gives an integer polynomial w such that
Delta*w=det(T_Delta) modulo X^d+1. Evaluating at q proves

    gcd(Q,E(Delta)) divides det(T_Delta).

Hadamard's determinant inequality then gives

    gcd(Q,E(Delta)) <= |det(T_Delta)|
                      <= ||Delta||_2^d
                      <= G_R=(4*R^2*d)^(d/2).               (2)

This exact integer bound does not factor Q or assume its residues form a
field. Nonzero evaluation for a single difference also follows from the
stated digit bound, but that alone would not bound its gcd with Q.

For a fixed nonzero multiblock difference, uniform labels make (1) hold with
probability gcd(Q,E(Delta_1),...,E(Delta_L))/Q <= G_R/Q. There are
N_R=(4R+1)^d-1 possible nonzero difference vectors per changed block.
A union bound therefore proves

    Pr[ANY nontrivial <=b-block move inside Omega_R]
      <= delta_move(b)
       = min(1, (G_R/Q)*sum_(j=1)^min(b,L) binom(L,j)*N_R^j). (3)

Count difference vectors, not every ordered pair of coefficient states.
Every possible within-box move is covered, not only moves near a chosen
starting point. On the complementary label event, every fiber-preserving
chain with this move support has no edges between distinct states of Omega_R.

The same upper bound remains valid if the FIRST label is fixed to a unit and
the rest are independent uniform: a relation using only that first block is
impossible; otherwise use any changed random block for the inhomogeneous
linear-equation bound. This does not justify fixing all labels arbitrarily.

For fixed L,b, q=d^(a+o(1)), R=d^(rho+o(1)), the leading exponent is

    log delta_move <= ((b+1)*rho+1/2-a+o(1))*d*log d

when this coefficient is negative. At the audited q approximately d^12,
R=d, all fixed b<=10 satisfy this eventually. Finite constants matter;
the actual finite certificates below do not yet reach b=10.

## 3. The Finite-Box Walk Is Frozen, Not Merely Slow

Use the actual finite Gaussian coefficient source on Omega_R, probability
proportional to exp(-pi*||c||^2/s_G^2), with s_G=sigma/sqrt(2). On the good
label event in (3), any exact-fiber transition changing <=b blocks is a
self-loop. It cannot mix between different supported witnesses of a fiber.

This is not vacuous because most source-weighted fibers have multiple
witnesses in the regime of interest. If

    Z_R=sum_(j=-R)^R exp(-pi*j^2/s_G^2),
    D=d*L,

the largest unconditional coefficient-vector mass is Z_R^(-D). There are
at most Q singleton fibers, so their total source mass is at most

    Q*Z_R^(-D).                                             (4)

This bound holds for every label choice. Thus a large amount of total
conditional entropy can coexist with zero local transitions. Counting that
entropy or seeing nearly uniform frequency weights does not establish a
usable Gibbs sampler.

The claim does not exclude a proposal that changes more than b blocks at
once or passes through other frequencies. Those are different transitions
whose implementation and correctness must be supplied.

## 4. Restoring Gaussian Tails Does Not Give A Fast Reversible Walk

Now let the coefficient prior be the untruncated product D_(Z,s_G)^D.
Its mass outside Omega_R is at most

    eta <= D*s_G^2/(pi*R)*exp(-pi*R^2/s_G^2).                (5)

Let r(u) be its frequency distribution and pi_u its conditional law on
f(c)=u. Averaging conditional tail probabilities gives exactly the prior
tail. Markov's inequality therefore shows

    Pr_(u~r)[pi_u(Omega_R^c)>sqrt(eta)] <= sqrt(eta).         (6)

If mu_max=theta(s_G)^(-D) is the largest prior atom, then

    Pr_(u~r)[max_c pi_u(c)>1/4] <= min(1,4*Q*mu_max).         (7)

Indeed such a fiber has r(u)<4*mu_max, and there are at most Q fibers.
This does not assume that r is pointwise uniform. The finite sum reference
can be avoided for an upper bound by using theta(s_G)>=s_G.

Fix good labels, a fiber obeying (6)-(7), and sqrt(eta)<=1/4. A greedy
subset A of its within-box states can be chosen with pi_u(A) in [1/4,1/2].
There are no distinct-state transitions within Omega_R. Hence every
transition from A to its complement goes to Omega_R^c. Stationarity bounds
the total incoming flow there by its stationary mass:

    flow(A,A^c) <= pi_u(Omega_R^c) <= sqrt(eta).

For ANY reversible discrete-time chain with stationary law pi_u and the
stated <=b-block exact-fiber move support, the indicator-function Rayleigh
quotient bounds its spectral gap gamma by

    gamma <= flow(A,A^c)/(pi_u(A)*(1-pi_u(A)))
           <= 8*sqrt(eta).                                  (8)

This includes chains with long arithmetic jumps INSIDE a changed block;
the restriction is the number of changed blocks, not a small step size.
If the chain is disconnected its gap is zero already. Laziness can be
imposed when translating spectral statements into ordinary mixing bounds.

Over labels and source-weighted fibers, the certificate holds except with
probability at most

    delta_move(b) + sqrt(eta) + 4*Q*theta(s_G)^(-D),           (9)

with vacuous probability bounds capped at one. At sigma=sqrt(d), R=d,
the tail is at most (L*d/(2*pi))*exp(-2*pi*d), so (8) is exponentially small.

An inverse-polynomial-gap assumption for a standard reversible or quantized
walk on THIS graph is therefore false. A generic square-root improvement in
gap dependence does not turn this certificate into a polynomial one. This
is not a lower bound on every quantum-walk algorithm: a different graph,
nonstationary preparation, non-fiber-preserving intermediate steps or a
separate analysis may avoid the premise. Warm-start access to the conditional
distribution must not be assumed in order to prepare that distribution.

## 5. Analytic Source References

Use q=nextprime(d^12), L=288, R=d, sigma=sqrt(d), as in the source audit.
Equation (3) uses exact integers; the displayed logarithms use 110-digit
reference arithmetic, not outward-rounded certified decimal enclosures.

| d | log10 delta_move(2) Upper | log10 delta_move(4) Upper | Largest Tested b With Nonvacuous Bound | log10 Gap Upper |
|---:|---:|---:|---:|---:|
| 64 | -881.3993 | -569.0959 | 7 | -84.6833 |
| 256 | -4850.1785 | -3304.8558 | 8 | -346.3425 |
| 1024 | -24655.5439 | -17253.3816 | 8 | -1393.8825 |

At d=64,b=8 the uncapped move-bound log is +54.4258, so that certificate
is vacuous, NOT evidence of a move or a negative probability. At d=256,b=8
it is -215.2958; at d=1024,b=8 it is -2450.1422. We tested b through 10.

The respective log10 tail bounds are -171.1728,-694.4912,-2789.5713.
The diffuse-fiber failure term 4*Q/s_G^D has log10 upper bounds approximately
-12483.7139,-70281.4731,-362506.9434. These are ideal mathematical source
certificates, not sampled quantum trajectories, actual runtime measurements
or cryptographic security estimates. Physical-source errors remain separate.

## 6. Checks And Countercontrols

All bounded references used seed 20260925, without production integration or
a full-suite run.

1. 270 exact integer multiplication matrices, d in {2,4,8}, R in {1,2,3},
   q in {3,5,17}, checked nonzero determinant, gcd divisibility, Hadamard's
   norm bound and (2). These include q,R combinations where the final move
   certificate would be vacuous; no invalid precision shortcut was used.
2. For d=2,R=1,L=2 and first label 1, solved every difference congruence
   exactly at q in {17,31,67,257}. Each had 94 bad second labels, giving
   probabilities 94/290,94/962,94/4490,94/66050. The first three union bounds
   were vacuous; the last bound was 0.07557911 against actual 0.00142316.
   At the first three moduli, independently enumerating all coefficient
   images at all 5,742 second labels exactly matched the congruence-derived
   bad-label sets. The largest modulus used congruence enumeration only.
3. Twelve finite reversible star-chain references checked stationarity,
   detailed balance, the exact spectral gap and the flow bound. They had
   4,8,16 typical states, no edges among them, and tail mass in
   {1e-2,1e-4,1e-8,1e-12}. After laziness, the actual gap was
   eta/(2*(1-eta)), below (8)'s pointwise 8*eta analogue. These are checks
   of the graph inequality, not replacement quantum-oracle problems.
4. Three growing source reports evaluated the integer union bound and the
   Gaussian-tail/diffuse-fiber inequalities, keeping nonvacuous and vacuous
   block counts distinct.

An essential failed-premise control: at d=3, Delta(X)=1+X and q=101,
gcd(q^3+1,Delta(q))=102, while ||Delta||_2^3=2*sqrt(2). Here X^3+1 is
reducible and the multiplication determinant is zero. Applying (2) without
the power-of-two/irreducibility premise is false.

Other escape routes are real, not missing caveats: larger-block moves,
different bases, broad coefficient widths, target-dependent global proposals,
non-fiber-preserving preparation, or a direct measurement not requiring
these conditional states. The result should eliminate only the specified
native local-walk architecture.

## 7. Research And Gemini Contract

FOLLOW-UP: `STRUCTURED_EDCP_OFF_FIBER_ANNEALING_AUDIT.md` now handles a
graded residual penalty with off-fiber moves. The key object is a low-residual
cell, not an isolated state after pivot normalization. A separate projected
encoding/QSVT audit is in `STRUCTURED_EDCP_POLAR_NORMALIZATION_AUDIT.md`.

Gemini should expose (2)-(9) as a scoped no-go checker, not implement a slow
walk merely to rediscover the theorem. Record d,q,R,L,b, exact-fiber support,
degree validity, source weights, tail/atom charges, and whether the claim is
finite-box freezing or an untruncated reversible-gap bound. Keep zero moves,
vacuous bounds and actual rejected premises distinct. Do not turn a gap
upper bound into an unconditional quantum runtime lower bound.

Next main-model work should investigate genuinely nonlocal target-dependent
operations or controlled off-fiber preparation, with explicit amplitude and
error accounting. If proposing a walk again, specify the move algebra and
show how it escapes (3) BEFORE implementing its runner. If proposing a tensor
method, specify how it escapes the physical-cut bound in
`STRUCTURED_EDCP_CONDITIONAL_CORE_BARRIERS.md`. The classical-readout
simulation remains the comparator for any route ending in local QFT data.

Local dependencies: `STRUCTURED_EDCP_GAUSSIAN_FIBERS.md` for negacyclic
evaluation and width conventions; `STRUCTURED_EDCP_JOINT_SOURCE_CONTRACT.md`
and `STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT.md` for actual source premises;
`STRUCTURED_EDCP_CONDITIONAL_CORE_BARRIERS.md` for the required coherent
conditional state. The determinant and conductance arguments are derived
above and remain subject to independent mathematical review.
