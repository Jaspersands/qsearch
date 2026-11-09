# Folded chain: closed source and classical-baseline review

2026-11-07. Read STATE/TRAPS and `FOLDED_CHAIN_COHERENT_TRANSFORM.md`.
Interpreter `/opt/anaconda3/bin/python`. No network/API/Git, new control or
implementation. Four primary texts are relied on below; hashes are in
`audits/sources/bethe_transform_selection/source.json`. The retained f_basis
and adiabatic PDFs are UNUSED selection leads, not theorem authorities.

**Disposition: CLOSED at the source scope.** Bond/token squeezing and the
coefficient-preserving folded/free-fermion relation are established prior art.
The parent's all-sector terminal-bit bookkeeping, coherent label extraction
and arbitrary-input binary-time evolution need their separate core/resource
proof. The opened sources neither invalidate that contract nor certify its
novelty. No classical separation or quantum execution is established.

## Four actual-source interfaces

All source paths below are under `audits/sources/bethe_transform_selection/`.

**folded.txt, arXiv2411.15132.** Lines371–409 give the EXACT native open
Hamiltonian, Eq3.1, on N+2 spins with frozen boundary spins. Global spin flip
and explicit N+1/N+3 fragment correspondences reduce its specified-state
discussion to boundary00; this is not permission to erase coherent boundary
labels. Eq3.6 at419–443 maps a reduced-chain XX eigenstate to a specified
folded eigenstate by a UNITARY made of permutations and bit flips that do
not alter coefficients. The source itself credits earlier hard-rod results.
Lines469–507 give the Slater determinant/coordinate shift;648–698 and Eq3.30
give the domain-wall extension. Section4.2,770–857, gives the reversible
contact-repulsion circuit;4.3,860–882 and1033–1055, explicitly treats physical,
auxiliary/count/reset registers. Ancilla reset is part of that construction.
Eq4.1,719–727, includes the free seed's explicit normalization; its raw plane-
wave determinant is not already a normalized state.

There is a REAL source normalization discrepancy: Eq3.1 at375–383 has the
native prefactor -1/8, but Eq3.16 at511–516 prints energy `-2 sum cos(p_a)`.
The latter was visually checked in the actual PDF, printed page9/PDF page10.
For the stated Pauli Hamiltonian the allowed spin exchange is -1/2:
`(-1/8)*2*2=-1/2`. Consequently the open squeezed hopping has single-particle
energies `-cos(pi*k/(ell+1))`. Use this direct normalization, not Eq3.16 as
an authority for the phase circuit. This discrepancy is not a counterexample
to the parent's Hamiltonian or token-conjugacy proof.

The paper also discusses superpositions of reference fragments at1490–1496;
do not claim it only handles a single isolated fragment. Nevertheless its
specified seed/magnon/domain-wall circuits are not, by themselves, a complete
reversible extraction of all varying-length labels from an arbitrary unknown
input. Its general XXZ preparation difficulty is explicitly a DIFFERENT seed
problem (1428–1437), not hardness of the folded Slater-permutation states.

**solvable_dynamics.txt, arXiv2105.02252.** The native kinetic normalization
and exchange amplitude -1/2 are135–157. SectionVI,881–908, already gives
the equal/different-spin BOND transformation and `011 <-> 110`. Keeping the
left spin removes its global-spin-flip ambiguity. SectionVII,1020–1039,
already scans left to right using `0->1,11->2,10->3`, equivalent to the
parent's C,A,B tokens. It explicitly leaves the last lone bullet/finite-open-
boundary completion unresolved at1030–1037. The varying length and conserved
species order are1041–1058 and1086–1104. The MM hopping operator is Eq111,
1073–1091. Its equivalence is explicitly stated to be BULK ONLY at1113–1118;
periodic twists cannot be imported into the open-path sine spectrum.

**dimers.txt, cond-mat/9703059.** Lines239–249 give the SAME rewrite rule.
The left-first deletion convention is445–463. Lines534–560 explicitly state
`A->11,B->10,C->0`, A exchanges with B or C, and B/C order is conserved.
They also explicitly flag an unpaired terminal1 for free boundaries and fix
the last bit0 to avoid it (546–554). Thus the token relabeling is not new;
the parent's explicit D label repairs an acknowledged boundary issue.
Lines811–825 further identify the squeezed binary string once the conserved
B/C word is known.

Crucially this paper evolves a STOCHASTIC process: its master equation and
imaginary-time Hamiltonian are594–629, including the escape-rate diagonal.
The interaction/potential term is visible in Eq5.5,655–669. The squeezed
generator is therefore HEISENBERG, Eq6.7 at827–838, not the parent's pure
hopping XX Hamiltonian. One cannot transfer that diagonal or its spectrum
merely because the off-diagonal configuration graph is the same.

**tractable_states.txt, arXiv0911.1624.** Definition1,344–358, requires
efficient computational-basis sampling AND amplitude computation, with an
explicit extension to m-bit precision in polynomial(n,m) time. The matchgate
example419–422 covers computational-basis seeds evolved by a known Gaussian
circuit. Lemma2,437–458, preserves CT under an efficiently computable basis
permutation, requiring BOTH forward and inverse maps. This applies to the
coefficient-permuted Slater states once the parent's complete bijection is
proved; no local-observable simplification or closed-form correlator is needed.

Theorem3,525–527, gives classical ADDITIVE polynomial-accuracy expectations
for bounded-norm ECS operators; row AND column neighbor enumeration is
required (490–511,613–622). For Hermitian observables one supplied row
enumerator supplies the column one by adjunction. Its proof568–626 uses
bounded probability-comparison ratios; the finite-precision extension is
627–638. This is safer than treating an unbounded naive amplitude ratio as
numerically free. It does not promise exact or exponentially accurate global
expectations, and it requires a known classical CT description.

## Matched consequence and remaining boundary

For a COMPUTATIONAL-BASIS input, its sector is classically known. Open-path
Gaussian evolution remains Slater, and the complete inverse token map is a
basis permutation. Hence amplitude evaluation, computational-basis sampling,
and additive bounded-ECS readouts have the known CT classical match. Binary
time does not defeat it: one-body phases can be evaluated to the required
precision with polynomial dependence on the bit length of t. The same match
holds for the specified determinant-based folded eigenbasis states. Absence
of a closed-form correlator in the physics discussion is not evidence against
this additive Monte Carlo baseline.

“Every eigenstate” must be read as the specified EIGENBASIS construction, not
every arbitrarily described vector in a highly degenerate eigenspace. An
arbitrary superposition of exponentially many such states is not automatically
CT or efficiently preparable. Conversely the classical match above does not
simulate arbitrary UNKNOWN quantum input entangled with an external reference.
That is the proper scope of the parent's coherent all-sector transform and
fast-forwarding target. No general XXZ hardness, advantage over the strongest
matched classical readout, or theorem-priority conclusion is imported.
