# Native RLWE Graph Kernels and Quaternion Orders

2026-10-05. LOCAL DERIVATION / REVIEW PENDING. No independent theorem review,
new quantum algorithm, efficient quaternion generator, novelty or speedup claim.

SELF-CRITIQUE FOLLOW-UP: [the conductor-order audit](NATIVE_RLWE_CONDUCTOR_ORDER_AUDIT.md)
constructs a different fractional ideal encoding that preserves the ORIGINAL
metric exactly. Its direct PIP route fails instead through global principality,
and extension to an ambient overorder erases the generic source's level data.
The metric-lift obstruction here must not be generalized to that construction.

## Research Question

Can the actual native rank-two kernel acquire useful quaternionic structure,
rather than merely invoke number-field principal ideals on one existing line?
Yes, it admits an explicit label-adaptive definite quaternion order. But the
encoding changes the metric, has no general principality promise, and supplies
no generator algorithm. An alternative always-principal encoding supplies its
own generator, which need not be short. These are distinct constructions.

This is an algebraic audit, not a proof that quaternion methods cannot work.
The potentially valuable remaining primitive is a costed, source-valid short
element algorithm for the definite order, with transfer to the ORIGINAL metric.

## 1. Actual Native Input

Let R=Z[X]/(X^d+1), d a power of two, K=Q(zeta_(2d)), and bar complex
conjugation. Coefficient vectors satisfy

```
bar(a)=(a_0,-a_(d-1),...,-a_1), C_bar(a)=C_a^T.
Lambda_M={(g,f) in R^2: g=Mf mod q}.
B=[qI,C_M;0,I], det(B)=q^d.
```

The saved d64 Babai certificate instead uses public matrix [I,C_m^T] and
columns [qI,-C_m^T;0,I]. Set M=bar(m) and (g,f)=(x,-y). This is an exact
signed isometry, not a metric approximation. All 128 saved reduced basis rows
are checked after this map. No LLL rerun or favorable source reroll is used.

## 2. Strong Original-Metric Gate

Assume q is prime, q=3 mod8, and d>=4. Consider ANY K-conjugate-semilinear
operator J on K^2 satisfying J^2=-I, preserving both Lambda_M and its original
product coefficient metric. The operator may depend on M. Then

```
Such a J exists if and only if M*bar(M)=-1 mod q.
```

Proof sketch, including integrality rather than just a fixed-axis test:

1. Write J=Z composed with conjugation. The coefficient norm is the normalized
   field trace of the Hermitian norm. Polarization over K implies Z is unitary.
   From Z*bar(Z)=-I and Z^-1=bar(Z)^T, obtain Z^T=-Z. Thus
   Z=[0,h;-h,0], h*bar(h)=1. This includes rational, nonintegral adaptive h.
2. Applying J to (M,1) gives h*(1+M*bar(M)) in qR. Write beta=1+M*bar(M).
   Norm_K(h)=1, so integrality forces q^d to divide Norm_K(beta).
3. In this CRT regime R/qR is E x E, |E|=q^(d/2), with conjugation swapping
   the two factors. Its conjugation-fixed subring is a FIELD E. Since beta is
   real, any nonzero residue is a unit in R/qR, contradicting that divisibility.
   Hence beta=0 mod q. This argument also covers nonunit original ratios.
4. Now M is a unit modulo q. Applying J to (q,0) first gives qh in R and
   Mqh in qR, hence h in R. The identity h*bar(h)=1 forces coefficient norm
   squared one, so h is a signed monomial. There is no free rational phase.
5. Conversely J_0(g,f)=(-bar(f),bar(g)) is an original-metric isometry with
   square -I and preserves the graph exactly when beta=0 mod q.

For IID full-ring public ratios the compatible count is |E|-1 among |E|^2.
Its probability is (q^(d/2)-1)/q^d < q^(-d/2); conditioned on a unit ratio it
is 1/(q^(d/2)-1). The existing d12 source parameters give conservative dyadic
upper exponents 2304,12288,61440 at d64,256,1024. Primality is an explicit
external certificate obligation, NOT established by this module's congruence
test. The d2 Gaussian case is different: q3 has four eligible ratios out of
nine. Low-CRT q=1 mod8 is also outside this probability formula.

Scope: K-conjugate-semilinear Hamilton structure preserving the stated metric
and R-action. NOT arbitrary Q-linear structures, different R-actions, weighted
orders, all quantum algorithms, RLWE security, or a general lattice lower bound.

## 3. An Explicit Definite Quaternion Order

Choose a real, totally positive rho in R with rho=-M*bar(M) mod q. Define

```
O_rho=R + R*j, j*a=bar(a)*j, j^2=-rho.
(g,f)*(h,k)=(gh-rho*f*bar(k), gk+f*bar(h)).
nrd(g,f)=g*bar(g)+rho*f*bar(f).
J_rho(g,f)=(-rho*bar(f),bar(g)), J_rho^2=-rho I.
```

Lambda_M is a LEFT O_rho ideal because rho+M*bar(M)=0 mod q. Right closure
is not automatic: a d2/q3/M=1+i countercontrol rejects two-sided treatment.
The construction uses R directly; it does not assume an unjustified integral
decomposition O_K=O_F[i] for a CM field.

Actual positive lift: center the coefficients of -M*bar(M) modulo odd q,
then add a scalar q-multiple until rho_0-sum_(i>0)|rho_i|>=1. Centering
preserves conjugation. C_rho is real symmetric. Gershgorin gives exact bounds
L=rho_0-sum|rho_i| and U=rho_0+sum|rho_i|. Therefore

```
||g||^2+||f||^2 <= ||g||^2+f^T C_rho f
                    <= max(1,U)*(||g||^2+||f||^2).
```

The lift is polynomial-bit and genuinely definite. But its distortion can
grow with q. A weighted-short output is not automatically sufficiently short
for native decoding or for the reciprocal-energy completion criteria. Ideal
principality is unproved in general. In the special case where this parameter
equals the next principal construction, principality IS known; do not suppress
that easy positive branch. Neither case supplies a new quantum primitive.

## 4. Always Principal Does Not Mean Useful

Instead choose rho=q-M*bar(M) and alpha=(M,1). Then nrd(alpha)=q. Right
multiplication by alpha has the exact column basis

```
[C_M,-C_rho;I,C_M^T].
C_M*C_M^T+C_rho=qI.
```

It lies in the graph and has determinant q^d, so Lambda_M=O_rho*alpha.
The generator is ALREADY KNOWN; PIP does not have a hidden generator to find.
This rho is not necessarily positive. If rho=0 the algebra is degenerate,
not a central-simple quaternion algebra or a legitimate quaternion-PIP input.
The d4/q3/M=(1,1,0,1) control has precisely this degeneracy.

Exact shortness countercontrol: d2, q257, M128. The known generator has
physical norm squared 16385, while (-1,2) belongs to the kernel with norm
squared 5. Here rho=257-128^2<0. Every principal generator must have reduced
norm +/-257, because the center is Q and its multiplication determinant is
the square of that norm. A generator with f=0 is impossible: g is divisible
by q. For f!=0 its coefficient norm obeys

```
||g||^2 = nrd + (128^2-257)*||f||^2 >= 128^2-2*257=15870.
```

Thus EVERY principal generator is much longer than the available relation,
not just an unfortunate choice of generator. This is a structured d2 transfer
counterexample, not a native-average or growing-degree hardness theorem.

## 5. Distortion Is Unavoidable For This Entire Lift Class

The simple positive lift is not uniquely at fault. Let r be the coefficient-
centered real residue of -M*bar(M), and S=||r||^2. For EVERY real totally
positive lift rho=r mod q, centering minimizes each coefficient magnitude,
so ||rho||^2>=S. Also trace(C_rho^2)/d=||rho||^2. Consequently

```
lambda_max(C_rho)^2 >= S,
condition_number(diag(I,C_rho))^2 >= S.
```

The identity block matters: this is not cured by uniformly rescaling the norm.
It is a worst-case metric distortion bound, NOT a bound on every vector or on
the success of every weighted-short algorithm. Different coordinate maps and
algorithms giving stronger output guarantees remain outside the statement.

For the high-CRT IID source, M=(a,b) with independent uniform a,b in E; its
real norm a*b is exactly a mixture of a uniform real residue with weight
alpha=1-1/|E| and a point mass at zero with weight 1/|E|. Uniform centered
real residues have h=d/2 independent integer coordinates: one with weight one
and h-1 with weight two; the middle coefficient is zero. Put

```
mu2=(q^2-1)/12, mu4=(q^2-1)*(3q^2-7)/240,
mu=E_uniform(S)=(d-1)*mu2,
v=Var_uniform(S)=(2d-3)*(mu4-mu2^2).
```

The native moments are alpha*mu and alpha*(v+mu^2), not the naive uniform
moments. Chebyshev and the exact mixture imply

```
Pr_native[S>=mu/2] >= alpha*max(0,1-4v/mu^2).
```

Thus with probability 1-O(1/d)-1/|E|, EVERY positive congruence lift in these
graph coordinates has metric condition number at least
sqrt((d-1)*(q^2-1)/24). At d64 the conservative bound exceeds 0.89.
Complete finite-source moments are independently checked alongside counts.
The d2 distribution is deliberately excluded. These facts strengthen the
metric-transfer proof obligation, not a universal quantum impossibility claim.

## 6. Norm-One Units Do Not Improve Fixed-Norm Generators Here

For the ACTUALLY CONSTRUCTED order, C_rho>=I. If u=(g,f) has nrd(u)=1,
taking the normalized trace gives ||g||^2+f^T C_rho f=1. Integrality then
forces exactly one block to be a signed monomial and the other zero. The
f-only branch has reduced norm rho, so is possible only when rho=1.

Hence norm-one units are exactly the 2d signed R monomials if rho!=1,
and those plus their j multiples (4d total) if rho=1. Their actions preserve
original physical length. Outside the rho=1 branch they preserve the same
R-projective direction as well. Two generators of the same principal left
ideal with the SAME reduced norm differ by such a norm-one unit: write
alpha_2=u*alpha_1 using equality of the ideals and use multiplicativity.
Thus searching these units cannot shorten a fixed-reduced-norm generator.

This is not a classification of units with other reduced norms, maximal
overorders with fractional coordinates, every positive lift, or quaternion
algorithms that find non-generating short elements. Those routes remain open.
Bounded d2 controls enumerate the actual norm-one units and fixed-norm orbits;
the enumeration is exponential calibration, not a purported fast search.

## 7. Literature and Remaining Obligations

[EPRINT-2025-287](https://eprint.iacr.org/2025/287) gives a rank-two module-LIP
reduction to a quaternion principal-ideal variant, nonuniform in general and
uniform for Hawk. That is not a native random graph-kernel SVP reduction or an
efficient quaternion generator algorithm. Current primary abstract was checked;
the earlier full [2024/1147 PDF](https://eprint.iacr.org/2024/1147.pdf) was read,
not the merged 2025 full proof. Preserve that version distinction.

The earlier full-paper audit of
[EPRINT-2025-1095](https://eprint.iacr.org/2025/1095) notes that quaternion
generator discovery remains unresolved and that exhaustive ideal/four-square
enumeration does not supply an efficient algorithm. The PDF endpoint currently
returns 403 on a refresh. This is not a cryptographic hardness theorem.

Highest-value next work:

1. Study the definite LEFT ideal as an actual short-element problem; prove its
   source distribution, order presentation cost and metric distortion. Do not
   assume principality or a known reduced-norm promise where none is supplied.
2. A different positive lift ALONE cannot evade the bound above. Seek a new
   coordinate construction, or a short-element guarantee strong enough to
   overcome that distortion on the actual source. Prove rather than assume
   the source and geometric transfer of either alternative.
3. Any proposed quantum generator must specify a physical input, precision,
   gate/query complexity, success probability and final original-metric output.
4. Try to kill the output with native lattice reduction and ordinary short
   element baselines. Successful bounded algebra identities are not advantage.
5. For a new useful relation, charge its existing kernel-ideal completion,
   projective direction, index, Gram height and reciprocal-energy obligations.

## 8. Verification and Handoff

Module/tests: `theorems/native_rlwe_quaternion_kernel.py` and
`tests/test_native_rlwe_quaternion_kernel.py`. Report:
`research/reductions/native_rlwe_quaternion_kernel.json`. Independent BigInt
checker: `research/certificates/native_rlwe_quaternion_kernel_crosscheck.js`.
Finite identities and two implementations are NOT independent theorem review.

Gemini owns production CLI/registry/full-suite integration. The research
contract is unaccepted; keep negative conclusions scoped to their hypothesis
class, keep positive encoding separate from generator success, and do not
promote source-gate or small-control evidence to a speedup claim.
