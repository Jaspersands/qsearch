# Arbitrary Mask Tails and Environmental Information Loss

Status: derived, review pending. No independent/formal verification, novelty
determination, efficient classical sampler, or new quantum algorithm.

This supplements, rather than replaces, the sharper uniform-mask theorem in
[TYPICAL_MASK_OBSTRUCTION.md](TYPICAL_MASK_OBSTRUCTION.md). It removes the
uniform-overlap penalty for a large class of nonuniform masks. It does NOT
rule out every mask: the low-occupation regime remains unresolved.

## Exact Scope and Bound

Keep the earlier assumptions: G=S_n, even n>=8, D=n!, M=(n-1)!!,
L=n(n-1)/2; standard mixed coset inputs, ONE shared hidden h uniform on its
class, one common group-algebra unitary independent of h, classical source
labels from a fixed irrep partition into r categories, and all physical data
discarded. There is no hidden-correlated prior transcript or side information.

Prepare ANY normalized PURE selector alpha=sum_s alpha_s |s>, independently
of h AND the observed source labels. Arbitrary complex amplitudes and
asymmetric dependence on the mask positions are allowed. For integer 0<=t<=k,
let pi bound sum_(|s|<t)|alpha_s|^2. Then the derived claim is

    E_h T(Omega_(alpha,0),Omega_(alpha,h)) <=
        2k sqrt(r/M) + 2sqrt(pi)
        + D min(1,12/sqrt(L))^(t/2)
        + 4sqrt(D) min(1,2/sqrt(L))^(t/2).                 (1)

The operational decision distance T(Omega_(alpha,0),E_h Omega_(alpha,h))
is no larger and is also bounded by the existing raw-copy cap
(1/2)sqrt((2^k-1)/M). Only this decision distance may use the raw cap.

There is NO division by alpha's uniform-mask overlap. In particular, for
polynomial k and t>=3n, masks whose mass below t is superpolynomially small
are obstructed asymptotically, including masks concentrated on weight 3n
out of k=n^2 positions. These have exponentially small uniform overlap.
This sufficient threshold is conservative, not an optimized transition.

## The Positive Comparison Transfers Without Postselection

The commuting comparison Q_eta from the earlier proof has a classical law
q_eta(J,z) in the source/Walsh basis. Consider the SAME preparation channel
for either hypothesis:

    (J,z) -> |J><J| tensor Z^z |alpha><alpha| Z^z.

Its output is precisely the arbitrary-mask coset-diagonal comparison
Q_(alpha,eta). To check the identity, each local Walsh variable has the
unnormalized probabilities (q_jeta +/- p_jeta(g))/2; its parity moment
is q_jeta when s_i=t_i and p_jeta(g) otherwise. Thus the prepared (s,t)
entry is alpha_s conjugate(alpha_t) times the coset-diagonal product kernel.
No operation is asserted to efficiently sample q_eta or implement the
comparison as the actual algorithm.

Trace-distance contractivity gives

    E_h T(Q_(alpha,0),Q_(alpha,h)) <= 2k sqrt(r/M).          (2)

This applies to ALL fixed alpha but only to the positive COMPARISON.
Discarding its signed remainder would be incorrect.

## Cross Operators as Environmental Fidelities

Fix eta and a source tuple J. For each nonzero source mass q_jeta, purify
the normalized state sigma_jeta/q_jeta and put

    |psi_(j,g)> = (R_g tensor I)|sqrt(sigma_jeta/q_jeta)>.

The reference vector is psi_(j,e); elements of H_eta fix it. Its pairwise
inner products are p_jeta(g^-1 l)/q_jeta. Zero-mass blocks contribute zero
and are never normalized.

For a coefficient index g define the normalized joint branch

    |chi_g> = sum_s alpha_s |s> tensor_i |psi_(j_i,g^(s_i))>.

The reduced cross operator C_(u,v)=Tr_environment |chi_v><chi_u| has
trace norm equal to ROOT fidelity F(tau_u,tau_v), where

    tau_g = sum_s |alpha_s|^2 tensor_i
                    |psi_(j_i,g^(s_i))><psi_(j_i,g^(s_i))|.

This is the standard purification/trace-norm duality consequence of
Uhlmann's theorem, not a new identity. Fidelity cannot decrease under a
measurement channel. See [Watrous, Chapter 3, Theorems 3.22 and 3.27](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.3.pdf).
The convention is root fidelity, NOT its square. The environment includes
the input purification; it is a proof device, not available algorithmic data.

## Bulk Pairs

Suppose u,v,u^-1v are all outside H_eta. At site j let a_j be the squared
projection of psi_(j,u) onto span{psi_(j,e),psi_(j,v)}. Measure the
orthogonal complement of this span at every site. Under tau_v, detection
has probability zero. Under tau_u, an active site avoids detection with
probability a_j. Inactive sites always avoid it. Therefore

    ||C_(u,v)||_1 <= sqrt(sum_s |alpha_s|^2
                                  product_(i:s_i=1) a_(j_i)).            (3)

Let x=<e,u>, y=<e,v>, z=<v,u> for the local normalized vectors. If |y|<=1/2,
the Gram inverse of {e,v} has norm <=2, so a_j<=2(|x|^2+|z|^2).
If |y|>1/2, use a_j<=1<=2|y| instead. This avoids an inverse at a singular
Gram matrix. In both cases a_j<=min(1,2(|x|+|y|+|z|)). Hence

    A = sum_j q_jeta a_j
      <= min(1,2 sum_j (|p_jeta(u)|+|p_jeta(v)|+|p_jeta(v^-1u)|))
      <= min(1,12/sqrt(L)).                              (4)

The last step is the earlier category-independent character-column bound.
Each non-coset translated element is nonidentity, so the alternative's
two character terms cost at most 2/sqrt(L) per argument. The null needs
only half the constant; using the alternative constant bounds both.

Sum (3) over ALL ordered source tuples with their natural product masses.
Jensen and independence of the fixed mask from J give

    sum_J product_i q_(j_i,eta) ||C_(u,v)[J]||_1
        <= sqrt(sum_s |alpha_s|^2 A^|s|) <= A^(t/2)        (5)

when alpha has no mass below t. There is no category-count factor here.

## Endpoint Pairs

If u is in H_eta and v is not, tau_u is the single pure reference product.
Its root fidelity with tau_v is exactly the square root of
sum_s |alpha_s|^2 product_(i:s_i=1)|p_(j_i,eta)(v)/q_(j_i,eta)|^2.
The source-weighted local coefficient obeys

    A_endpoint = sum_(j:q_jeta>0) p_jeta(v)^2/q_jeta
               <= sum_j |p_jeta(v)| <= min(1,2/sqrt(L)).

The other endpoint orientation follows by exchanging u and v. Thus (5)
holds with A_endpoint. Both endpoints cannot lie in H_eta off the coset
diagonal. No one-sided selector-support shortcut is used.

## Low-Weight Mass and Coefficient Sums

For arbitrary alpha, project onto weights >=t. Both actual output states
have discarded mass pi, independent of h and the source record, because
every controlled subset operation is unitary. The same unnormalized
gentle comparison as before costs 2sqrt(pi) across the two actual states.
Keep the comparisons projected; their distance remains bounded by (2).

For an unnormalized retained mask of squared norm m<=1, the sharper form
of (5) is sqrt(m sum_(|s|>=t)|alpha_s|^2 A^|s|), at most A^(t/2).
This accounts for subnormalization without division by m or pi.

Triangle inequality bounds the summed projected remainders. Across the
two hypotheses, including the half-trace-norm factors, the bulk coefficient
weight is <=D and the endpoint coefficient weight is <=4sqrt(D), exactly
as in the previous proof. Substituting (4)-(5) gives (1).

For t>=3n, sqrt(L)>=n/2 and D<=n^n give a bulk bound at most
n^n(24/n)^(3n/2)=exp(-Omega(n log n)); the endpoint decays faster.
The mixture is negligible at polynomial k using r<=2^(n-1) and M>=(n/2)!.
The tail term is negligible only when pi is superpolynomially small.

## Adversarial Checks and Failure Modes

`theorems/coset_mask_tail_fidelity.py` checks the environmental identity and
both remainder inequalities using complex, orthogonal, nearly collinear,
and exactly coincident local vectors. It retains a rare source of mass
1/1000. Twelve controls evaluate 48 thresholds and enumerate ordered sources.
The nearly singular cases test the projection fallback, not a Gram inverse.

Six independent regular-basis S3 controls use a dense noncentral unitary,
all hidden members, all ordered irrep tuples and three asymmetric/complex
mask families at k=2,3. The direct physical channel agrees with the local
kernel. The positive comparison equals the stated preparation-channel image,
contracts the Walsh comparison distance, and is NOT the actual output.
Small-degree controls do not prove the asymptotic statement.

Two genuine countercontrols preserve essential assumptions:

- Orthogonal local environments and a mask with weight-zero mass 3/10
  retain cross norm 3/10 even though A=0. Dropping pi would falsely predict
  zero. High expected Hamming weight alone is insufficient.
- With two equally likely source categories having local failure 0 or 1,
  a source-dependent mask can choose one failing site among three. Its
  averaged cross norm is 7/8, exceeding the fixed-mask bound sqrt(1/2).
  Thus moving the mask choice inside the source average is invalid.

An attempted S3 countercontrol for unpermuted source-multiset compression
did NOT separate its scalar trace distance from full ordered enumeration.
This is not evidence permitting that shortcut for arbitrary masks: a source
permutation generally permutes alpha too. All new controls enumerate ordered
tuples and do not rely on this unestablished symmetry.

Exact integer evaluations, not large physical simulations: at n=1024,
k=n^2, t=3n, pi=0 the decision bound is 2^-311. At n=4096 it is 2^-5373;
allowing pi<=2^-4096 weakens it to 2^-2045. Setting t=0 leaves a vacuous
certificate, as required. All implementation assumptions are declarations,
not an automatic proof of an arbitrary program's compliance.

## Prior Art and What Remains

[Hallgren et al., Limitations of Quantum Coset States for Graph Isomorphism](https://arxiv.org/html/quant-ph/0511148v1)
constrain the joint measurement size needed for useful information. That
does not by itself establish this bound at large k after this specific
channel. The raw-copy prefix is elementary existing sample-information
reasoning, not a novelty claim.

[Moore, Russell and Sniady, Section 3](https://arxiv.org/html/quant-ph/0612089v3)
define adaptive pair-combination and representation-measurement sieves.
A common coherent overlapping-subset query is not automatically such a
measured sieve. Conversely, this proof does not cover those adaptive sieves.
This scope comparison does NOT establish novelty. A broader literature
search and independent expert review are still required.

A positive counterweight is [Moore and Russell, Sections 3 and 5](https://arxiv.org/html/quant-ph/0504067):
their missing-harmonic construction measures the SPAN of subset subspaces
and can distinguish the promised cases with constant probability at enough
copies. Projecting onto an individual subset subspace is not the same as
projecting onto that span, whose efficient implementation they leave open.
Our discard-after-one-common-query theorem must not be misreported as
ruling out this information-theoretic measurement. Any proposed connection
requires an actual physical implementation or reduction, not shared use of
the word "subset."

The next meaningful unresolved part of this architecture is a specified
low-occupation mask, or useful physical retention, source adaptation or
multiple coherent queries. Do not promote a mask merely because its overlap
with the uniform state is exponentially small. Nor may a mask of weight t
be replaced by t raw copies without proving that reduction: it can coherently
address many different subsets of a much larger input collection.

## Verification Record

2026-09-14: the seven-file integration run passed 251 tests, with one obsolete
mutation-wording assertion failing. Its updated scoped assertion and all new
tests passed in the 32-test follow-up (overlapping coverage). Python compilation,
JS syntax and diff checks passed. All live binary/synthesis/dequantization/proof/
conjecture/mutation workflows completed, and registry validation has no issues.
The fresh full-suite attempt passed 65 before stopping on the existing missing
character-moment scaling write at `tests/test_character_moment_obstruction.py:73`.
The complete repository test suite is not green. No independent proof or
novelty review is implied by these checks.
