# Conditional Elliptic Corollary By Doubling

2026-10-25. Deduction from the proposed surface source, not an independently
reviewed theorem or executed quantum algorithm. Novelty remains UNRESOLVED.

## Statement With Dependencies

Assume the complete prime-only geometric-source construction in
PRIME_ONLY_SOURCE.md is correct, uniformly polynomial-time and coherently
compilable with its stated error budget. Import the existing explicit
Sp4 receiver and the fixed-dimension PPAV algorithms with their exact
model, field and marking contracts.

Then a separable degree-ell elliptic weak isogeny phi:E->E', with ell an
odd prime different from p>3, reduces to that construction: its original
kernel line and annihilator ideal can be recovered in quantum polynomial
time in the PAID input lengths and log ell. The input must include the full
evaluable End(E), its integral quaternion dictionary, a compatible abstract
split modulo ell, the ORIGINAL modeled E', and the sufficient fixed
odd-prime weak evaluations and fields specified by the source plan.

There is no assertion that this input is available from two bare curves.
No efficient weak representation of an unknown isogeny is synthesized.
No classical lower bound or unconditional new quantum result is claimed.

## Reduction

Set A=E^2, B=(E')^2 with PRODUCT polarizations and Phi=phi x phi. Then

    Phi^dagger Phi=[ell],  Phi Phi^dagger=[ell],
    ker Phi=L direct-sum L,  L=ker phi.

The geometric degree of Phi is ell^2; its POLARIZATION multiplier is ell.
Confusing these is fatal to both the lift congruence and resource plan.
The known source order is M_2(End(E)). The public product construction
supplies the target model from the given E'; it does not require a hidden
isogeny, unknown decomposition or target endomorphism ring.

At each required prime r, ask for phi on an ordered basis (P,Q) ONCE.
Embed the SAME pair of returned points into both factors. The resulting
four images have the single common scalar required for Phi. Do not make
two separately randomized calls and silently assume their masks agree.
Reusing classical points is legal; no unknown quantum state is cloned.
Mixed source points are evaluated by group addition from these data.

All weak queries are made in classical preprocessing at the fixed levels.
Subsequent coherent group queries use the stored arithmetic data and
reversible geometric computations. A quantum-superposition interface to
the weak phi evaluator is not an additional input requirement. Fixed random
tapes, bounded clocks and uncomputation are still required for that latter
compilation; no such circuit is implemented here.

Run the existing Sp4 procedure, whose correct output W is L direct-sum L
in the paired source coordinates. Project W to the first E factor to recover
L. This is ordinary finite-field linear algebra and is independent of the
receiver's basis for W. Check rank two, rank-one projections and equality
of those projections before accepting this special postprocessing path.
Such checks do NOT certify that W was recovered from the genuine source;
the receiver's original source certificate remains necessary.

No new proof of the quantum receiver is supplied by doubling. This is a
reduction of an existing native input to the already proposed source, not
an invented oracle separation or a new quantum primitive.

## Correct Ideal And Existing Output Conversion

For the specified split rho:O/ell O -> M_2(F_ell), form

    I_L={a in O : rho(a)L=0}.

This is a LEFT O-ideal: (ba)L=b(aL)=0. Its quotient condition has dimension
two in the four-dimensional matrix algebra, so [O:I_L]=ell^2 and its
reduced norm is ell. It contains ell O. Its common geometric kernel is
exactly L: containment follows from the definition, and modulo ell the
common kernel of all matrices annihilating L is L. There is no extra
large-prime point basis or interpolation in this lattice computation.

Use a basis (v,w) of F_ell^2 with v spanning L. The allowed matrices are
those whose first column is zero in that domain basis. Pull back their
two-dimensional span through rho, adjoin ell O, and compute column HNF.
The local implementation does just this, in fixed lattice dimension four.

This ideal is NOT the right module of maps whose IMAGE is contained in L.
For L=span(e1), E11 has image in L but does not annihilate L. The tests
retain this counterexample and verify left-ideal closure and index.

Known output conversion: Proposition 4 of
[Herledan Le Merdy--Wesolowski, 2502.17010v2](https://arxiv.org/html/2502.17010v2)
converts a left ideal with a known full source dictionary to an efficient
isogeny representation unconditionally, using dimension-eight geometry.
It therefore supplies phi_I:E->E/E[I_L], conditional on having first
recovered I_L. Its kernel is the original L. Matching its elliptic codomain
to the original E' is a bounded-degree elliptic-isomorphism computation,
with field extensions explicitly charged. The right order gives the full
target order abstractly. Producing effective target-order maps additionally
uses dual evaluation and integer-isogeny division (their Proposition 3),
not an assumed free target-order oracle. None of these geometric output
conversions is executed by the local HNF tests.

## Prior Art And What Might Actually Improve

[Chen et al., 2305.19897v1](https://arxiv.org/html/2305.19897v1)
already give a quantum hidden-stabilizer approach to IsERP. Their weak
representation definition permits common order-dependent scalar masks.
Section 5 uses powersmooth quaternion lifts with Heuristics 5.2 and 5.3;
the special-order setup also invokes GRH. Section 5.4 moves those lifts to
precomputation but still calls Theorem 5.1 to obtain them. Thus its phrase
about being heuristic-free AFTER preprocessing does not unconditionally
bound that preprocessing.

[Chen--Petit, Leuven Isogeny Days 6 slides](https://www.esat.kuleuven.be/cosic/projects/isocrypt/wp-content/uploads/sites/4/2025/11/leuven-isogeny-days-6.pdf)
explicitly label the old and generalized PQLP/IsERP theorems heuristic
(pages 4 and 11). The indexed page 3 of their
[2025 accepted manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/392160/3/suborder_to_endomorphism_ring.pdf)
also labels Theorems 1 and 3 heuristic. Theorem 3 covers general isogeny
degrees, so prime-degree scope is not new. Direct retrieval of the complete
manuscript failed at both university mirrors in this pass; only its indexed
statement and the authors' complete slides were inspected. This is useful
scope evidence, not a comprehensive novelty audit of that later proof.

Our possible improvement is the SOURCE: bounded integral elementary
automorphisms of E^2 plus odd-trace smooth repolarization, rather than a
prescribed powersmooth norm lift inside End(E). No PQLP subroutine or
special-order search appears in the written construction. A potential
assumption removal is worth reviewing, but should not be advertised as
the first efficient quantum algorithm for this already studied problem.
The new source's own validity, uniform geometric implementation and prior
art must be settled before advertising even that narrower improvement.

## Adversarial Checks And Falsifiers

- Product-target classical attacks do not contradict the reduction. Here
  Phi^dagger e_i Phi=ell e_i, so their mod-ell images vanish. The established
  product dichotomy returns two copies of the original elliptic problem,
  not a solution. It cannot be counted as two independent hard instances.
- The full weak evaluator in prior work is stronger than a short transcript.
  Only a transcript containing THIS fixed plan suffices for this proposal.
  It need not contain large-prime ell-torsion points or prime-square data.
- Independent masks on the two factors conjugate mixing operators
  incorrectly. The arithmetic control explicitly falsifies this shortcut.
- A polynomial classical algorithm for the SAME weak elliptic input,
  including any use of genuine geometric labels beyond equality, would
  remove the claimed quantum separation. An equality-only sqrt(ell)
  baseline is not a lower bound on that stronger classical input.
- A source-model mismatch, nonuniform geometric clock, incorrect joint
  canonicalization or wrong field descent invalidates the corollary even
  when every local ideal test passes.
- Previously published stabilization or lifting results may already imply
  this assumption removal. Limited searches have not certified novelty.

The new implementation only maps a SUPPLIED doubled plane to its kernel
line and integral annihilator ideal. It does not recover a secret, run
theta geometry, implement IdealToIsogeny or establish a speedup.
