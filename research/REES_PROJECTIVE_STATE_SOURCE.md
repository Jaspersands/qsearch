# Phase-Free Rees Sources From Unknown State Copies

2026-10-22. New local source-conversion argument and checked public design
compiler. The full quantum algorithm and novelty remain UNDER REVIEW.
No natural hard state family, classical separation, independent proof,
formal verification, or Shor-level application is asserted.

Noise scope: REES_NOISY_STATE_SOURCE.md now composes known streaming
purification with this receiver for a separately promised PRINCIPAL
EIGENSTATE target. Full-rank noise destroys state-dependent exact scalar-
support symmetry; finite purification does not restore it exactly. The
new route uses a complete-circuit hybrid to the ideal principal state,
with spectral gap, IID copies, rejected copies and a global abort cap paid.
It is not arbitrary noise correction or a change to the mixed-state task here.

## 1. Scientific Question And Decision

Can the positive Rees cover learn a state's RAY stabilizer from fresh
copies and controlled group action, without conjugate copies, an inverse
state preparation, or the older character-normalizer recursion?

The proposed answer is yes for explicit exponent-p Lazard groups of ANY
FIXED class c<p and LINEAR representation action. The new step is a
public finite-field evaluation design with zero power moments. It erases
every possible hidden character at once while retaining enough distinct
evaluations to identify the lifted subgroup. There is no character oracle.

The design requires at most (c+1)! fresh copies per block, independent of
the numeric prime p. Often fewer suffice: class nine at p=43 and at the
127-bit prime 2^127-1 has an exactly verified 14-point design. These are
algebraic controls, not measured state-family performance. The subsequent
Rees receiver still has an enormous sufficient source-tree bound.

This replaces the preferred COPY-ONLY composition for this input model,
not the correctness status of its quantum receiver. The older
TWISTED_STATE_SYMMETRY_RECEIVER.md needed a derived-class restriction and
character-preserving normalizers. Neither is needed in the present written
composition. Keep its prior falsifiers and other access models intact.

## 2. Exact Input Contract

Supply a genuine n-dimensional Lie algebra L over odd prime F_p, fixed
nilpotency class c<p, and its public BCH group G=exp(L). Supply efficient
controlled action of a LINEAR unitary representation R of G, plus fresh
IID copies of a density operator rho. Copy acquisition and action costs
are part of the original input model. Promise an inverse-polynomial gap
gamma>0, or charge its inverse explicitly:

    H = {g : |Tr(rho R(g))|=1},
    |Tr(rho R(g))| <= 1-gamma for every g outside H.

Unit-modulus expectation implies R(h)rho=chi(h)rho: each occupied vector
has the SAME eigenphase. Thus H is a subgroup and chi is a character. For
pure rho this is its ray stabilizer. For mixed rho it is SCALAR ACTION ON
THE SUPPORT, not general conjugation symmetry. For example, I/d commutes
with every unitary, but a nontrivial traceless unitary has expectation zero.

Since G has exponent p, write chi(exp(v))=omega^ell(v), omega=exp(2pi*i/p).
The functional ell on h=log H is F_p-linear and kills [h,h]. Indeed, group
powering gives scalar multiplication; the inverse-BCH addition word differs
from a product only by commutator corrections, which every character kills.
This uses the same Lazard correspondence as REES_HSP_REDUCTION.md.

No ordinary hiding function, unknown-state preparation inverse, purification,
conjugate-state supply, Gram-matrix oracle, or measured hidden coefficient
is assumed. A projective R is not automatically a linear R: a costed linear
central extension would require a separate group/scope argument. Small
characteristic c>=p, growing c, and arbitrary mixed-state conjugation are
not covered. A global gap cannot be certified from a handful of overlaps.

## 3. A Public Zero-Moment Design

Find a multiset S of NONZERO elements of F_p such that

    sum_(s in S) s^r = 0 for r=1,...,c,
    S contains at least c distinct points.

Multiplicities count actual fresh state copies; they are not free field
weights. Negative multiplicities would require a different physical resource.

Here is a uniform construction. For each r=1,...,c find a nonzero solution
to the ONE scalar equation

    x_(r,1)^r + ... + x_(r,r+1)^r = 0.

For r=1 use (1,-1). For r>=2 the deterministic polynomial-time scalar
solver is a published dependency: van de Woestijne's result, stated as
Fact 2 of [Ivanyos--Santha](https://arxiv.org/pdf/1503.09016). This is not
the larger many-equation SDE solver used by the receiver. Remove zero
entries from each row and take the multiset of all products choosing one
remaining entry from each row. For any k<=c its kth power sum factors as

    sum_(s in S) s^k = product_(r=1..c) (sum_j x_(r,j)^k) = 0,

because factor r=k vanishes. Each row retains a nonzero entry, so S is
nonempty and nonzero. Its size M is at most product_(r=1..c)(r+1)=(c+1)!.

**Coverage is not an extra assumption.** If c<p-1 then M is a product
of positive integers <=c+1<p, so p does not divide M. Suppose S had
m<=c distinct nonzero points u_j, with integer multiplicities a_j.
The first m moment equations form an invertible nonzero Vandermonde
system in a_j modulo p. All a_j would be zero modulo p, contradicting
M=sum_j a_j not being divisible by p. Thus there are at least c+1
distinct points. If c=p-1, the partial product of rows 1 through p-2
already has all p-1 nonzero points by the preceding argument. Multiplying
by any one nonzero entry in the last row preserves full coverage.
Therefore every allowed c has at least c separating evaluations.

**Implemented paths.** design_from_scalar_rows checks every supplied
PUBLIC scalar certificate, constructs the product multiset and verifies
moments/coverage again. find_moment_design first tries a capped small
m>c dividing p-1. An exactly verified element of order m supplies all
m roots of unity, which annihilate the first c moments. Only the small
candidate m is factored, not the large integer p-1.

The fallback uses (1,-1) for odd degrees. When gcd(r,p-1)=2, it obtains
a^2+b^2+1=0 and converts the powers by r*e=2 mod(p-1). It uses FLINT
modular square roots, exact witness checks and a capped random search.
For a uniform a, more than half admit b; an exhausted cap is ABORT.
The remaining scalar Fermat rows now use the verified backend in
SCALAR_FERMAT_DESIGN_BACKEND.md. For sufficiently large p, a Weil-bound
argument gives success at least 1/(2r) per random prefix followed by a
checked polynomial root. The other regime proves p<16(r-1)^4 before using
a small-field dynamic program; there is no unrestricted field-sized fallback.
Every row is checked, and the final design checks moments and coverage.
Sampling is capped with an explicit ABORT bound; FLINT root runtime is
still an expected-time, not locally clocked dependency. Seeded examples
are reproducible diagnostics, not probability certificates. The receiver's
general MANY-EQUATION SDE solver is still not implemented.

## 4. The Unknown Character Cancels Exactly

Form the public positive cover A=sum_(r=1..c) t^r gamma_r(L), with
evaluation homomorphisms E_s:A->L and D=dim A<=cn. For a in exp(A), use

    T(a) = tensor_(s in S) R(exp(E_s(log a))).

Every factor is a genuine representation because E_s is a group
homomorphism. This is the distinction from the generally invalid map
R(g) tensor R(g^-1) on a nonabelian group. In particular E_(-1) is not
minus E_1 on all grades; even grades have the same sign.

For C=log(a)=sum_r C_r t^r, unit modulus of the tensor expectation is
equivalent to every E_s(C) belonging to h. The c distinct evaluations and
F_p-linearity of h make this equivalent to C_r in h for every r. Hence
the scalar-support stabilizer is exactly

    H_tilde = exp(sum_r t^r (h intersect gamma_r(L))).

For a in that subgroup its character on rho^tensor(M) is

    product_s chi(exp(E_s(C)))
      = omega^(sum_r (sum_s s^r) ell(C_r)) = 1.

Thus its scalar-support stabilizer is already its BOSE stabilizer. No
phase has been estimated, and no p-fold tensor power is needed. Outside
H_tilde, at least one evaluation lies outside H, so

    |Tr(rho^tensor(M) T(a))| <= 1-gamma.

The original gap survives; there is no M-dependent gap shrinkage. This
statement holds for arbitrary h, including nonnormal and nonabelian h.
Neither h nor ell appears in the public compiler.

## 5. Actual Source And Whole-Run Resources

Prepare a uniform address a in exp(A). For every s in S, apply the public
evaluation-controlled R to a FRESH copy of rho, clean the evaluation
workspace and discard that copy. Repeat the entire block k times. The
exact address density has entries

    sigma[a,b] = (product_s Tr(rho R(E_s(b^-1*a))))^k / N,
    N=|exp(A)|=p^D.

Here E_s on group elements abbreviates the BCH evaluation homomorphism.
On equal H_tilde cosets the entry is exactly 1/N. Else its modulus is
at most (1-gamma)^k/N. Comparing with the ideal mixed coset source tau:

    ||sigma-tau||_F <= (1-gamma)^k,
    TD(sigma,tau) <= sqrt(N)*(1-gamma)^k/2.

Copies can be processed sequentially on the SAME retained address. This
does not reuse any target copy; processing all evaluations on one target
would multiply the operators rather than their independent overlaps and
can invent symmetries. No exponentially large tensor state or density
matrix needs to be stored by the proposed source procedure.

Feed these fresh reduced sources DIRECTLY into graded central descent on
A. Do not construct a second Rees cover. H_tilde is already homogeneous,
and its final grade-one image is all h. Thus the proposed core recovers
the original projective/scalar-support H without character-normalizer
recursion or an ordinary hiding oracle. It consumes only the address
registers; no discarded labels are subsequently read or inverted.

Let B be the complete leaf count from recovery_budget with receiver error
epsilon/2. It counts every discarded child in the whole fresh-source tree.
Use plan_orbit_state_transfer with order bound N, gap gamma, use cap B,
and error parameter epsilon. Its conservative

    k = O((log N+log B+log(1/epsilon))/gamma)

makes the source replacement hybrid <=epsilon/4. At gamma=1 use k=1.
Total fresh copies and controlled action calls are M*k*B. Allocate
epsilon/(4*M*k*B) to each copy-preparation-plus-controlled-action channel,
and include uniform-address/receiver errors in their existing instrument
budget. The total is <=epsilon. These are complete-channel bounds with
records/ABORT, not errors conditioned on rare outcomes.

The exact planner projective_source_budget performs this accounting for
an ALREADY CERTIFIED design. To include design-generation ABORT, allocate
epsilon/2 to public preprocessing and use that planner with epsilon/2.
The scalar backend note provides a union-bound sampling cap for all rows;
any root-runtime clock requires an additional separately paid allowance. The
gap, source independence and controlled-action implementation remain input
obligations; the planner cannot certify them. Query/source bounds are not
native gate counts. Outputting a phase character or its Bose kernel is an
optional additional Fourier-learning task, not included in this budget.

## 6. Decisive Falsifiers

- A moment-balanced list with insufficient distinct points loses subgroup
  information. The compiler checks BOTH conditions, and the general
  construction proves both. p repeated copies of one evaluation are
  rejected when c>1 even though all their moments vanish.
- Ordinary evaluation points 1,...,c need not erase characters on even
  grades. A central-character UT3 control has correct overlap moduli but
  the wrong density until the new design is used.
- Reusing one target for all six evaluations in the p=3 control returns
  the unchanged state even for an address outside the hidden subgroup.
  With independent copies the same overlap is zero. A valid moment
  certificate does not excuse a false source-access contract.
- The UT4 control uses actual sparse regular-action vectors of a proper
  NONABELIAN, NONNORMAL hidden subgroup, with a nontrivial character.
  Tensor-product Gram entries match the full coset-fiber criterion.
- Nonorthogonal regular-action orbit states test the complete density
  error bound and amplification, not just entry magnitudes or marginals.
- I/d shows why arbitrary mixed-state conjugation symmetry is not learned.
  Generic projective R and absent controlled action are separate failures.

These fixtures test a universal conversion lemma. Their planted states
are not candidates, natural hard families, or speedup evidence. No central
registry admission is made. The receiver remains unimplemented and under
review; so does the complete application theorem depending on it.

## 7. Prior Art, Impact And Next Decision

Tensor orbit amplification and the earlier copy-only source comparison
are reused from STATE_SYMMETRY_COSET_TRANSFER.md. Scalar diagonal solving
is published mathematics. [Holt--Subramanian, Sections 9.1--9.2](https://arxiv.org/html/2609.38085v2#S9)
relate tensor linearisations to codes, including zero-sum constraints, for
abelian projective representations. Their outlook explicitly identifies
nonabelian powering not being a homomorphism as an obstacle. Our proposed
route starts with LINEAR R and replaces powering by actual Rees evaluation
homomorphisms. It is not a general nonabelian projective-representation
linearisation, and the paper's optimal-rate code bounds are not contradicted.
The novelty of this particular composition has not been independently checked.

The [abelian StateHSP access-model results of Liu et al.](https://arxiv.org/abs/2609.35656)
already distinguish copy and preparation-unitary access. This proposal
does not improve their optimal abelian sample bounds or obtain their
inverse-access gap dependence from copies alone. At c=1, the two-point
design (1,-1) is the familiar abelian phase cancellation, not new.

If the full Rees receiver survives review, the new consequence would be
a time-efficient scalar-support/ray-symmetry learner for fixed-class
large-prime nonabelian actions on unknown quantum inputs. That is a more
specific research contribution than a synthetic oracle benchmark. It is
still not a factoring-style classical-input speedup or a demonstrated
useful laboratory application. Explicit sparse states, stabilizer states,
low-width tensor networks and low-degree phase states need their existing
learners checked before any advantage claim.

Next: independently attack character linearity, product-design coverage,
the physical source contraction, and the complete receiver composition.
Then seek a motivated quantum-input problem whose symmetry action really
uses the higher-class nonabelian scope. Do not generate more planted
states or spend GPT effort wiring a new UI campaign.
