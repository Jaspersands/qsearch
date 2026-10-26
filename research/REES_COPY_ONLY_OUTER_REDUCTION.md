# Rees HSP: Copy-Only Outer Reduction

2026-10-22. Conditional written extension, NOT an implemented receiver,
independent review, formal proof, novelty verdict or speedup admission.

## 1. Correction And Conditional Statement

The earlier whole-proof audit imposed an unnecessary inverse-access
restriction on the bounded-error small-prime branch. The EXACT theorem
does require a source-preparation inverse. The forward-only bounded-error
route does not: see [Imran--Ivanyos, Proposition 3 and Lemma 2](https://arxiv.org/pdf/2304.08376).
Their Section 2.4 also already supplies subgroup-state restriction and
quotient channels. These source conversions are prior art, not new here.

The resulting proposed scope is:

> Conditional on the Rees receiver, hidden subgroups of uniquely encoded
> finite nilpotent groups of any FIXED class can be recovered in bounded-error
> quantum polynomial time from fresh mixed coset-state copies, supplied
> generators, and coherent public group operations. Neither an ordinary
> hiding function nor an inverse of the unknown source is required.

All public-group preprocessing is paid. This includes quantum order finding,
factoring, presentation acquisition and the additive-coordinate kernel
learning on the acquired-chart route in REES_WHOLE_PROOF_SCOPE_AUDIT.md.
The local exponent-p alternative in FREE_LAZARD_PULLBACK.md avoids that
last dependency by retaining unknown relations in a larger public hidden
preimage. It does not remove the other preprocessing. Public circuits may be
reversed. This is not an inverse of a device producing unknown rho_H.
Unique encodings, uniform-address preparation, fixed class and complete-channel
precision remain essential premises. The receiver consumes independent inputs;
Section 2a below weakens the RAW input contract to a coset-diagonal bank that
can be refreshed into those inputs. Correct one-copy marginals, or separability
alone, still do not suffice.

## 2. One-Copy Transport Without A Decoder

Fix R_g|x> = |x*g^-1>. The standard mixed coset density satisfies

    rho_H = (1/|G|) sum_(h in H) R_h,
    Tr(rho_H R_g) = 1_H(g).

Let Q be a public finite address set with efficient uniform preparation,
and sigma:Q->G an efficient forward representative computation. Prepare
|Q> and one fresh rho_H. Apply controlled R_sigma(q), clean sigma's
workspace while keeping q, and discard the original source register.
The reduced address density is exactly

    out[q,r] = Tr(rho_H R_(sigma(r)^-1 sigma(q)))/|Q|
             = 1_H(sigma(r)^-1 sigma(q))/|Q|.

This follows from the controlled unitary and partial trace, not a hidden
membership test. No access to H, a coset label, or sigma^-1 is used by
the operation. Leaving a distinguishable representative workspace behind
would destroy the desired coherences and is not allowed.

For a public S<=G, set Q=S and sigma the inclusion. The output is
rho_(H intersect S) over S. There is NO factor [G:S] in the copy cost.
This channel is not computational-basis postselection onto S.

For K normal in S with KNOWN K<=H, set Q=S/K and choose public coset
representatives. Then sigma(r)^-1 sigma(q) belongs to H precisely when
r^-1 q belongs to (H intersect S)/K. This is independent of the section,
even if the section is nonhomomorphic. If K is not contained in H, this
independence fails. K normal in all of G is unnecessary; normality in
the current S suffices.

Nested restriction/quotient maps can be composed into a SINGLE forward
representative circuit to original G. Each requested local source still
uses one original copy, not one copy per layer and not an index-sized bank.
Costs of all representative computations, controls and cleanup are paid.

The same kernel identity holds for a single fixed pure left-coset state
|aH>. The original IID contract is sufficient, but the coset-diagonal bank
extension below also works. Correct individual marginals do not certify
the required joint law. The older Bell-bank falsifier remains valid, and
the new separable character-bank falsifier shows that entanglement is not
the only possible problem.

## 2a. Correlated Coset Centers Can Be Refreshed

This is a source-contract correction using ordinary group twirling and the
existing transport channel, NOT a new HSP algorithm or a novelty claim.
The finite checks are independent NumPy controls in
tests/test_coset_bank_refresh.py, not a replay of the cloud-dependent receiver.

For fixed unknown H, suppose the M supplied registers and side information E
have the joint state

    Omega = sum_a (tensor_(j=1..M) |a_j H><a_j H|) tensor E_a,

where E_a are positive subnormalized operators with sum_a Tr(E_a)=1.
The coset choices may be biased, identical across all registers, or arbitrarily
classically correlated. E need not be classical and its conditional operators
need not commute. No coset representative or decomposition is given to the
algorithm. This is a PROMISE on the entire supplied state, not something inferred
from observing its marginals. All M physical registers must actually be supplied;
this does not clone or reuse a consumed state.

Define L_g|x>=|g*x> and the public channel

    T(sigma) = (1/|G|) sum_g L_g sigma L_g^dagger.

Uniform left multiplication permutes all left cosets transitively, each equally
often. Hence T(|aH><aH|)=rho_H for every a, without knowing H. Linearity gives

    (T^tensor M tensor id_E)(Omega) = rho_H^tensor M tensor sum_a E_a.

Thus even side information about the correlated centers is decoupled from the
refreshed registers. Independent private uniform group elements suffice to
implement T, using one public left multiplication per register and no source
inverse, hidden membership oracle, extra source copies or index postselection.
Uniform group sampling and public multiplication are paid prerequisites. In
explicit Lie coordinates, sample all coordinates uniformly in F_p. For the
black-box extension, use the paid public presentation/group-sampling interface;
do not silently assume a free sampler for an opaque encoding.

The randomization records must be ignored/discarded, not fed to subsequent
adaptive choices. Conditional on a particular g, an output from a fixed coset
is still a pure coset state, not rho_H. Reusing the SAME random g for the whole
bank also fails to erase correlations. Nor may g be chosen from coins already
correlated with the incoming source. These are operational requirements, not
an additional measurement/postselection step.

Equivalently, the existing uniform-address controlled-right-action channel
with address set G and sigma(q)=q IS T. For every operator S,

    T(S)[q,r] = (1/|G|) sum_z S[z*q,z*r]
              = Tr(S R_(r^-1*q))/|G|.

This equality includes complex off-diagonal inputs, not only densities. It
means the earlier transport mechanism already supplies a coherent refresh
implementation if uniform quantum addresses are available. It consumes one
source and discards it, retaining one group-sized output register. Furthermore,
each existing multi-target lift has the same output on EVERY product of pure
coset states, because each right-action contraction is the same 0/1 indicator.
It therefore already ignores classical correlations of coset centers. Explicit
refresh is a sufficient modular way to reuse the IID proof, not a new required
source multiplier in the previous resource envelopes.

The exact general criterion is broader than coset diagonality:

    T^tensor M(Omega) = rho_H^tensor M
    iff Tr(Omega tensor_j R_gj) = product_j 1_H(g_j) for every tuple (g_j).

This follows by comparing every output matrix entry with the displayed kernel.
For decoupling from E, the analogous E-valued partial-trace identities are
needed. Neither this exponential list of identities nor H is available as
a free certificate. Coset diagonality is a transparent sufficient promise,
not claimed to characterize every repairable source.

### A Separable Bank That Defeats Independent Refresh

Let G=C_p for odd prime p and H={0}. Write |chi_k> for its Fourier basis and
take two evaluation maps a->a and a->2a. Supply

    Omega_bad = (1/p) sum_k |chi_k><chi_k|
                              tensor |chi_(-k/2)><chi_(-k/2)|.

Both marginals are EXACTLY I/p=rho_H. The state is explicitly separable and
only classically correlated in the Fourier basis. Independent left translations
leave each character projector invariant, so T^tensor2 cannot repair it. In the
two-target lift the phases cancel for every address: k*a+2*(-k/2)*a=0.
The output is |G><G|, whereas independent inputs give I/p. Their trace distance
is 1-1/p. This is a false whole-group signal, not successful recovery of H.
The example uses a class-one input with a valid class bound two and distinct
nonzero evaluation points; it directly tests the source contract of the lift.

The old entangled Bell example is therefore not the complete boundary. A
separability test or perfect one-copy tomography would still not certify a
usable bank. Fixed coherent phase errors are not coset-center randomness.

### Approximation And Verification Scope

If the JOINT supplied bank is within trace distance delta of a promised bank,
and independent sampler j has total-variation error epsilon_j from uniform,
the retained output is within delta+sum_j epsilon_j of the ideal independent
bank (and is of course at most distance1). This follows from channel
contractivity, convexity and a channel hybrid argument, including side
information and any explicit abort flags. It is a joint error requirement,
not a bound obtained from marginal errors. A mixture with Omega_bad can have
zero marginal error but a nonzero wrong-lift probability contribution.

Nine finite tests pass: all64 complex matrix units for the channel identity;
all8 fixed D8 cosets; a correlated D8 bank with nonorthogonal quantum side
information; the existing joint-action contraction; wrong-side, shared-coin
and retained-record countercontrols; two separable character-bank controls
at p3/p5; and a joint-error mixture. The wrong-side D8 trace distance is
1/4, not the initially guessed test threshold greater than0.4; that assertion
was corrected before the passing run. These tests check finite identities,
not the whole Rees theorem, source availability, or an asymptotic speedup.

## 3. Feeding The Rees Lift Directly

After public exponent-p chart acquisition, let A be the positive Rees
cover and E_1,...,E_c its nonzero evaluation homomorphisms. For each
evaluation use a distinct fresh source and controlled right action at
sigma(E_i(a)), where sigma is the flattened original-group section.
All targets are discarded; one common address register is retained.
The resulting matrix is

    rho_lift[a,b] = product_i 1_(H_local)(E_i(b)^-1 E_i(a)) / |A|.

The existing Vandermonde argument identifies this with the exact coset
density for h_tilde = sum_r t^r (h intersect gamma_r(L)). No projective
moment design or overlap amplification is needed: the original character
is already the exact 0/1 subgroup indicator. Each Rees leaf costs c copies.

Alternatively use the public free Lie domain F and its generally
noninjective surjection Phi to the local group. Replace each action by
sigma(Phi(E_i(a))). The same identity gives the Rees lift of the FULL
hidden preimage in F, still at c original copies per leaf. No kernel
learning, kernel-index penalty or inverse map is introduced. Project the
eventually recovered full preimage back through Phi. Use the larger free
dimension and ranks in all resource bounds; the b-based chart budget below
does not apply unchanged. This alternative is detailed and tested at its
public-map/channel interface in FREE_LAZARD_PULLBACK.md, not as a complete
receiver. A natural free grading alone need not preserve that preimage.

The graded central descent then consumes only these reduced states and
public actions. Its final abelian step uses Fourier samples and classical
linear algebra, not an exact coherent HSP algorithm calling a source inverse.
This does NOT reconstruct a reusable ordinary f oracle or a preparation
unitary for rho_H. It supplies a stream of consumed quantum states.

## 4. Small Primes Without A Lazard Substitution

The public semi-elementary descent must use the COMPLETE preimage of
A[p] for A=K/(K' H0), retaining K' H0. Top powers of an arbitrary generator
list are insufficient, even with exact orders. The constructive relation-
lattice repair and hidden-intersection proof are in
[SEMI_ELEMENTARY_TORSION_REPAIR.md](SEMI_ELEMENTARY_TORSION_REPAIR.md).
Its public presentation acquisition is paid and not implemented here.
K' H0 is not assumed contained in H: this arithmetic quotient is NOT
itself a legal copy-source quotient. Only the resulting restriction to L
and the later quotient by known H0 use the source-transport channel.

For p<=c, use the known semi-elementary HSMC reduction: recover HG'/G'
from a central-erasure chain and abelian Fourier samples, then recover H
by the published outer normalizer procedure. In this branch the elementary
central layers have at most c-1 stages. No exponent-p Lie chart is assumed.

An explicit conservative zero-sum arity can reuse the fixed-degree diagonal
solver already imported by the Rees proof. For labels lambda_i in F_p^r,
solve

    sum_i x_i^(p-1) lambda_i = 0,    some x_i != 0.

Fermat gives x_i^(p-1)=1 on the nonzero support and 0 elsewhere. Thus the
support is a nonempty zero-sum subset, exactly the central-erasure witness.
Take S_p(r)=B_(p-1)(r) using the existing sufficient SDE arity; S_2(r)=r+1.
This is polynomial in r for FIXED p, not uniformly efficient in p.
Using p<=c is essential. This is a conservative application of a known
solver, not an improvement to published zero-sum algorithms.

The code checks supplied witnesses, including p=2, but does not implement
the general diagonal solver. Returning arbitrary linear-dependence weights
is wrong for odd p: the central operation selects targets, not signed or
weighted copies. Empty support is also invalid, even when its sum is zero.

The D8 physical control covers p=2, class 2 and exponent 4, outside the
Rees core's c<p input. Every positive-mass central-label tuple gives the
right quotient source after a binary zero-sum selection. Forbidden labels
are not normalized. This checks the source identity, not the full solver.

## 5. Whole Original-Copy Budget

Let b>=1 bound the unique encoding width, c>=1 be fixed, and 0<epsilon<1.
Use the imported public-group outer interface from
[Ivanyos--Sanselme--Santha, Section 3](https://www.irif.fr/~santha/Papers/iss12.pdf).
The large-prime branch uses its order-p reduction and exponent-p restriction;
the small-prime branch uses the forward-only HSMC reduction above.

Set B=b(b+1), t=ceil(log2(12B/epsilon)), M=b+t. A conservative pair of
SEPARATE clocks allows at most B large-prime local calls and B small-prime
HSMC calls across their respective Sylows. On correct histories each
Sylow of composition length r needs at most r(r+1) calls; the sum is
bounded by B. Abort on clock exhaustion even after an incorrect answer.

Put S=max_(prime p<=c) B_(p-1)(b). If there are no such primes, Q_small=0.
Otherwise the following counts ALL original hidden-source reads:

    Q_large <= B*c*M*product_(d=2..c) B_d(b),
    Q_small <= B*M*S^(c-1),
    Q_total <= Q_large+Q_small.

Every coordinate/presentation call uses PUBLIC group operations, not a
copy of unknown rho_H. These counts therefore cover hidden-source inputs,
but are NOT whole gate bounds or numerical costs for preprocessing.
They also do not claim a physical quantum backend exists in this repo.

Reserve epsilon/4 each for public preprocessing, all large-prime chart
acquisitions, all large-prime cores and all small-prime HSMC calls. Each
local call receives epsilon/(4B); its Fourier rank failure is at most
2^-t, leaving room for solver/circuit allowances. Amplify public kernel
learning within the chart allocation. All local algorithms have polynomial
clocks on arbitrary histories. Condition on no earlier error and use a
first-error union bound; never assume adaptive inputs are independently
correct. Approximate COMPLETE instruments, including records and ABORT.
This budget assumes exact IID input copies; noisy sources require a
separate global hybrid allowance, not an uncharged change of promise.

The sufficient copy exponents in b, at fixed c,epsilon, are

    a_large = 3 + sum_(d=2..c) d*ceil(log2(d+1)),
    a_small = 3 + (c-1)*max_(prime p<=c) (p-1)*ceil(log2(p)).

For c=8 they are 111 and129, so ignoring small primes can understate even
this COPY exponent. For c=9 both are147. Neither number is the exponent
of total runtime. These impractical ceilings are not observed scaling.

## 6. Refutations, Baselines And Remaining Work

- Wrong action orientation fails for nonnormal H; public group inverses
  remain necessary even though source-preparation inverses do not.
- Quotienting by a subgroup not known to lie in H gives section-dependent
  output. A plausible generator is not a certified correct adaptive history.
- Correlated source banks can defeat the product kernel despite perfect
  one-copy marginals. No free copy reuse or cloning is permitted.
- An exact-algorithm theorem cannot be invoked from a bag of mixed copies.
  This argument deliberately uses bounded-error final Fourier sampling.
- Public group preprocessing must not be silently renamed free access.
  Forward representative circuits replace a decoder, not their gate cost.
- Fixed c is essential. No DCP, graph-isomorphism, code-equivalence or
  cryptanalytic implication follows for growing-class families.
- Measuring original coset copies in the computational basis is uniform
  and discards H, but defeating that weak baseline is not a separation.
  A quantum-input theorem alone does not exhibit a hard classical problem.

The Rees core, general diagonal backend, outer quantum implementation,
formal proof and independent correctness/novelty review remain open. This
pass removes a false access blocker; it does not solve those obligations.
The multistage central-descent follow-up below tests one missing composition
step. Independent scrutiny of the full proof is still needed; another
source-noise wrapper is not the next priority.

Implementation: black_box_copy_budget and binary_zero_sum_support in
theorems/rees_hsp_reduction.py; falsifiers in tests/test_rees_copy_only_outer.py.
Generate the live copy-only envelope with
`python -m theorems.rees_hsp_reduction --write`. All discovery flags stay false.

## 7. Follow-Up: Two Actual Central Instruments

tests/test_multistage_graded_descent.py adds a class-three control with
625 group elements, not another class-two single-stage example. The group
over F5 has second-kind coordinates (x,y,z,w) and multiplication

    (x,y,z,w)*(X,Y,Z,W)
      = (x+X, y+Y, z+Z+xY, w+W+xZ+(x^2/2)Y).

It is the semidirect action exp(xD) on (y,z,w), D(y,z,w)=(0,y,z).
An independent affine-matrix embedding checks the multiplication. The
commutator [X,[X,Y]] is nontrivial in W, with further commutators zero;
the group has class three, not just three coordinate labels. The tested
dilation scales (x,y,z,w) by (s,s,s^2,s^3).

The first physical instrument projects the central W character, then
uses a public cubic SDE witness and controlled right actions to discard W.
Its ACTUAL reduced density is fed into a second physical instrument,
which projects the remaining central Z character and uses a quadratic
witness. Both use literal P*rho*P^dagger and target partial traces, not
a predicted kernel substituted as the output. The sections setting the
last coordinate to zero are nonhomomorphic, and those cross terms remain
in the public group multiplication.

The following homogeneous hidden subgroups cover changing intersections:

| Hidden subgroup | Positive first-stage tuples | Positive second-stage tuples |
| --- | ---: | ---: |
| X | 25 | 125 |
| X,W | 1 | 125 |
| X,Z,W | 1 | 1 |
| Z | 25 | 1 |

X is nonnormal; X,Z,W is nonabelian. Every positive tuple gives the correct
next source and total record probability is one. Two first-stage inputs
and three second-stage inputs mean six ORIGINAL copies per final packet.
This finite arity is not the general sufficient-arity theorem. In particular,
the quadratic p5 witness is found by bounded exhaustive TEST enumeration;
the production quadratic backend does not support that prime. The cubic
bijective-power case uses the existing supported solver and its real API.

The decisive countercontrol is the valid but NONHOMOGENEOUS hidden line

    H = {(t,0,0,t): t in F5}.

It is not invariant under dilation. In a conditional source, acting at
scale s leaves a phase lambda*(s^3*w-s*t). Cubic cancellation removes the
w term but NOT the residual -t*sum_i lambda_i*s_i. For a nonzero pair
(lambda_1,lambda_2), this residual vanishes precisely when their ratio
is +1 or -1. Eight of the 25 equally likely tuples therefore fail.

The code checks failure probability8/25 and complete record-averaged
output trace distance8/25 from the desired quotient density. This is not
an inference from a normalized rare branch. It falsifies bare cubic
erasure without homogenization; it is NOT a no-go theorem for alternate
multi-moment constructions, including older linear-plus-cubic cancellation.

Finally, X, XW and XZW have different subgroup orders5,25,125 but identical
final abelian-image sources. Central erasure alone is HSMC, not full HSP
recovery. The positive Rees cover retains original derived directions in
grade one; the ordinary graded group in this fixture does not. Consequently
this test checks a genuine two-stage receiver COMPONENT, not the entire
arbitrary-H Rees lift, final reconstruction, black-box reduction or runtime.
No fixture is admitted as a new algorithm candidate.
