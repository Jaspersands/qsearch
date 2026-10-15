# Public Classical Attack Bridge: Corrected Claims And Exact Certificates

CORRECTED2026-10-15. The earlier large-q LLL-success monotonicity, incorrect
LLL constant, constant-memory and theorem-verification claims are withdrawn.
The useful public RREF attack remains. No speedup or general hardness claim.

Run `python qsearch.py planted-qary-classical-attack-threshold-bridge` and
`node research/certificates/planted_qary_classical_attack_threshold_bridge_crosscheck.js`.

## What The Source Controls Actually Establish

Six small public q-ary kernel controls are attacked by signed-column checks,
FLINT LLL and projective free-coordinate enumeration. All finite LLL/RREF
recoveries are replayed from their PUBLIC H matrices. Private plants appear
only in separate forward-calibration fields, never as solver inputs.

Nonzero ternary kernel vectors have free support

    max(1,s-m) <= s_F <= min(s,n-m).

The lower bound1 follows because invertible pivot columns cannot annihilate
a nonzero vector supported entirely on pivots when q>=3. The other bounds
count coordinates. Absence of unit/signed-column-pair relations is verified
directly in each control; it is not a hardness certificate.

## The Correct LLL Statement

For size-reduction parameter eta and Lovasz parameter delta, with
eta^2<delta<=1, define alpha=1/(delta-eta^2). Size reduction and Lovasz imply

    ||b_(i+1)*||^2 >= (delta-eta^2)||b_i*||^2,
    ||b_1||^2 <= alpha^(n-1)||u||^2

for every nonzero integer lattice vector u. For the second inequality, choose
the largest nonzero coefficient i in u's basis expansion; its orthogonal
projection has norm at least||b_i*||. The recurrence bounds||b_1*|| by that
projection. A minimum-norm returned row is no longer than b_1.

At delta3/4,eta1/2, alpha is TWO, not4/3. The old code's4/3 ceiling was not
the advertised theorem. The current finite returned bases are independently
verified at delta3/4,eta51/100, giving alpha10000/4899. Exact rational
Gram-Schmidt checks ALL size-reduction and Lovasz inequalities, rather than
assuming them from a library call or its defaults. The parameters of FLINT's
call itself are not silently relabeled.

Recovering +/-u from this approximation criterion additionally requires
primitive u and lambda2>alpha^((n-1)/2)||u||. Those lambda2 premises are NOT
certified for the six generated controls. Their observed recoveries are finite
facts, not verification of a growing-family isolation theorem.

## Determinant Growth Does Not Supply A Successive-Minimum Gap

For ANY prime q>=7, use the public modular constraint matrix

    H = [(1,-1,0,0,0),
         (0,0,1,-1,0),
         (1,0,-1,0,-2)] mod q.

Its full-rank modular kernel lattice has determinant q^3. Its ordinary
integer nullspace is generated, over INTEGERS, by

    u=(1,1,1,1,0), v=(1,1,-1,-1,1).

Indeed the rows force x0=x1, x2=x3 and x0-x2=2*x4.
Write b=x4 and a=x2+b to get x=a*u+b*v, with a,b integers. Orthogonality
gives||x||^2=4a^2+5b^2. Every vector with norm<=sqrt5 satisfies
|H_i x|<=sqrt30<q, so modular zero means ORDINARY zero in this ball.

Therefore lambda1^2=4 with unique primitive shortest pair+/-u, and
lambda2^2=5 for EVERY prime q>=7. The squared successive gap is constantly5/4,
while q^(3/5)/2 diverges. Exact q7,11,101,1009 certificates bind public H,
prime proofs, index, witnesses and parameter arithmetic. This is a counterexample
to deriving successive-gap growth from determinant growth, not a distributional
theorem about every planted generator or a lower bound on LLL.

The earlier assertion of strictly increasing LLL effectiveness had no specified
coupling/distribution or success-probability proof and is removed. Determinant
normalization remains an explicitly labeled proxy, never lambda2.

## Polynomial-Space RREF Baseline

For the public RREF pivot/free split, enumerate ternary u_F whose first
nonzero coordinate is+1; reconstruct pivot coordinates uniquely as centered
residues of-C*u_F. Keep only ternary pivots. This checks EXACTLY
(3^(n-m)-1)/2 assignments, and independently reproduces the minimum-norm
sign-canonical ternary vector without plant advice.

There is no exponential hash table, but working storage is NOT constant.
The copied centered m by(n-m) block, current vectors, enumeration state and
best vector require O(m*(n-m)+n) integer slots in addition to the supplied
problem. Integer bit costs depend on log q. For m>=ceil(n/2), the assignment
count is smaller than the ambient MITM half-state sum; per-assignment arithmetic,
hashing, early termination and memory costs differ, so this is not a wall-time
dominance theorem. A cap returns UNKNOWN before exponential enumeration,
not a negative result.

## Independent Replay And Remaining Obligations

The JS checker now certifies primes and full modular rank, reconstructs public
RREF, verifies lattice index and U*B=L with det(U)=+/-1, recomputes rational
Gram-Schmidt, checks the correct approximation bound, enumerates the complete
public free-coordinate search, and verifies the determinant-gap counterfamily.
It no longer treats recovery booleans as independent proof.

Finite controls still do not supply actual lambda2 isolation, a hard natural
source, stronger BKZ/SIS experiments, or any end-to-end quantum speedup.
