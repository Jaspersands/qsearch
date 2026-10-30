# Rees Descent As A Complete Coset-Pinching Channel

2026-10-23. Independent local reconstruction of the central step, plus a
bounded vector/permutation implementation. This is NOT independent external
review, formal verification, a new algorithm, or a natural hard source.

The prior terminal pass was progress: it proposed an explicit uniform bound
and added prime-power falsifiers. This pass instead attacks the central
Rees mechanism. The current repository and its faithful regular-algebra
tests were inspected first. No new defect in the claimed central identity
was found. The addition here is a reference-preserving channel formulation
and a physically distinct check, not a larger group-size benchmark.

## Exact Statement

Let G have a central elementary-abelian subgroup Z and let Q=G/Z. Let H
be the current hidden subgroup, stable under each nonzero public dilation
delta_s. On Z, delta_s acts as multiplication by s^d. Let sigma:Q->G be
any public section; it need not be a homomorphism. Set K=H intersect Z.

Prepare independent exact mixed coset states rho_H. On target i measure
the complete central-character instrument, retaining its label lambda_i.
For each positive-probability record tuple, compute any nonzero packet s
satisfying sum_i s_i^d lambda_i=0. All acquired targets stay charged, even
when their scale is zero. Perform controlled R(delta_(s_i)(sigma(q))) on
each target, where R(g)|x>=|xg^-1>, and DISCARD the targets afterwards.

For EVERY input density rho_AR on address A and an arbitrary reference R,
the resulting channel on A is exactly coset pinching for HZ/Z:

    Phi(rho)_q,q' = 1_[q^-1 q' in HZ/Z] * rho_q,q'.

Here entries are operators on the reference. The classical label tuple is
independent of the output: the full instrument is tau_labels tensor
(Phi tensor Id_R)(rho_AR), where tau_labels is the actual measurement law.
This holds for adaptive, label-dependent choices of s, pointwise in every
positive-probability record tuple. It requires neither conditioning on a
favorable tuple nor independence of the chosen scales from those labels.

The result is a channel obtained by discarding a label/target environment.
It is NOT a reusable coherent value oracle, does not provide an inverse,
and cannot be substituted for those interfaces without another proof.

## Reconstruction

The character projector is

    Pi_lambda = (1/|Z|) sum_z chi_lambda(-z) R(z).

Only labels trivial on K have positive probability. For such a normalized
conditioned state rho_lambda, direct regular traces give

    Tr(rho_lambda R(g)) = chi_lambda(z), if g=h*z with h in H,z in Z;
                       = 0,            if g not in HZ.

The value is well-defined because lambda annihilates K. This is the same
central trace identity used by the existing proof, not a new hypothesis.
Conditional independence of the targets follows from independent input
preparations and separate measurements before the adaptive classical choice.

For a q,q' matrix entry, controlled right translations multiply it by

    product_i Tr(rho_(lambda_i)
                 R(delta_(s_i)(sigma(q')^-1 sigma(q)))).

If q'^{-1}q is outside HZ/Z, the trace for every active target is zero.
At least one target is active. If it is inside, write the lifted difference
as h*z. Dilation invariance keeps delta_s(h) in H; the product of phases
is chi_(sum_i s_i^d lambda_i)(z)=1. A zero scale contributes1, not a call
to an inverse dilation. Thus the Schur multiplier is exactly the claimed
indicator. This proof applies to operator-valued reference blocks, not
only to a uniform address state.

Initial label probabilities do not depend on the address/reference, and
every branch is trace preserving on them after targets are discarded.
Hence the same identity holds separately in each unnormalized classical
record block. Complete-channel approximation can be propagated with
contractivity and hybrid bounds, without dividing by rare branch masses.
This observation does NOT by itself bound any actual hardware error.

## Independent Physical Control

The fixture is UT_3(F_3), order27, with multiplication
(x,y,z)(X,Y,Z)=(x+X,y+Y,z+Z+xY), and graded dilation (sx,sy,s^2 z).
Its hidden subgroup <X> is nonnormal but homogeneous. Oracle labels (y,z)
give actual fibers; the source is assembled as their normalized pure
vectors with the correct fiber probabilities. These numeric labels are
classically easy and make NO research-candidate or hardness claim.

The implementation applies central projectors as sums of actual
27-dimensional translation permutations. Controlled translations evolve
the vectors, and explicit inner products trace out the targets. It does
not import the repository's regular-coefficient descent formula or feed
the hidden subgroup into the channel. Independent expected output is
pinching the nine quotient addresses by their y-coordinate.

All27 positive triples of central labels are checked, with adaptive
nonzero square-moment solutions from an explicitly exhaustive3^3 TEST
solver. Every address pair is checked in each branch, both with the
standard section and a deliberately nonhomomorphic central twist.
Normalized Choi states and random inputs entangled with references of
dimensions1,3,9 are checked. Record probabilities sum to1 and are not
discarded in the complete classical-quantum comparison.

## Decisive Broken Controls

1. Reusing ONE target three times: for record lambda=1 and scales(1,1,1),
   the square moment vanishes in F_3. But R(sigma(q))^3=I because the group
   has exponent3. The address channel is identity, not coset pinching.
   The normalized Choi trace distance is exactly2/3. Fresh independent
   targets with the same three labels and scales give the correct channel.
   A moment equation is not a license to reuse a source register.
2. All-zero scales also give the identity channel. Nonzero support is an
   essential check, not merely a scalar-solver convention.
3. Solving the LINEAR moment instead of the square moment fails for a
   valid twisted section. The first test mistakenly expected failure even
   for the standard section; it passed because that section happens to
   eliminate the offending central phase on this hidden coset direction.
   The corrected test preserves that accidental success and demonstrates
   the failure after changing only the legal section. Do not claim every
   wrong moment fails on every fixture, or weaken the general moment gate.
4. Omitting the Rees lift for nonhomogeneous H=<X+Z> fails even with a
   correct square moment. Its supplied oracle fibers are still genuine
   cosets. The fault is the missing dilation-invariance premise.
5. Correct SINGLE-TARGET marginals, even after conditioning on all labels,
   do not certify the joint input. With trivial H, take the actual
   three-target state |Psi>=(1/sqrt(|G|)) sum_g |g,g,g>. Each raw marginal
   is the required rho_H=I/|G|. The positive central record(1,1,1) has
   probability1/9, and each conditional marginal equals the exact required
   rho_1. The scales(1,1,1) obey the square moment. Yet simultaneous right
   translations leave |Psi> invariant, and commute with the central
   projectors, so the conditioned bank gives the IDENTITY address channel.
   Required pinching for trivial H completely dephases the nine addresses.
   Their normalized Choi trace distance is exactly8/9. The control directly
   constructs the19683-dimensional joint vector, partial traces all three
   targets, and evolves actual permutations. Independent targets with
   identical labels give the correct channel. This is a falsifier of a
   weakened source contract, NOT a flaw in fresh oracle preparation.

The correlation failure is not confined to this small field. For ANY
finite G with central Z and trivial H, the two-target maximally entangled
state |Phi_G>=(1/sqrt(|G|)) sum_g |g,g> has both marginals I/|G| and is
invariant under R(a) tensor R(a) for every a. Central measurements return
(lambda,-lambda); their normalized marginals are the required conditioned
coset states, since Pi_lambda^T=Pi_(-lambda). The projectors commute with
simultaneous right translation, so this invariance survives conditioning.
Scales(1,1) satisfy every degree-d moment, but the output is the identity
channel rather than full quotient pinching. With D=|G/Z|, their normalized
Choi trace distance is exactly1-1/D. Extra independent targets with scale0
can pad any larger prescribed arity, and all their costs remain charged.
This is an explicit general counterexample to replacing joint freshness
by even perfect raw AND conditional one-copy guarantees.

Independence is a sufficient general contract; this audit does not claim
that every correlated bank is bad. It also does not validate the general
diagonal backend, opaque-group preprocessing, or whole algorithm merely
because this local channel identity survives the controls.

## Scientific Decision And Handoff

No gap was found in the core channel under its exact promises. Do not turn
this into a series of neighboring receiver variants or bigger matrices.
The main remaining issues are external scrutiny of the full proposed
theorem and a natural source that survives its recorded classical attacks.
The literature check also found no new classical solver for the compact
high-degree polynomial-stabilizer source. Shift-equivalence algorithms
cannot be transferred from degree/characteristic-restricted statements
without checking those restrictions; no hardness conclusion follows.

Files: physical_channel.py, test_physical_channel.py, replay.py,
rees_channel_receipt.json, and this note. All remain outside the actively
migrating source/staging repositories. Gemini can integrate these as
bounded independent controls after the move is verified. No UI, candidate
registry, commit, push, migration repair, or background job was added.

## Verification

12 dedicated tests PASS in0.51s. Across all six isolated bundles,
239 tests PASS in24.83s. All three new Python files pass py_compile.
Whitespace checks pass. The live receipt retains all27 adaptive records
and SHA256 hashes of the code, tests, replay and this proof note.

The complete fresh-bank instrument has mass1 to floating-point precision
and normalized classical-quantum Choi trace distance3.14e-16 from its
predicted channel. Broken-control distances are2/3 for target reuse,
about0.81650 for the wrong-degree/twisted-section control,1 for an unlifted
nonhomogeneous subgroup, and8/9 for the correlated three-target bank.
These numerical values verify finite controls, not the general theorem;
the preceding algebra supplies its exact statements.

Reproduce here with the external cache:

    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py
    PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python -m py_compile physical_channel.py test_physical_channel.py replay.py

Full-repository tests, qsearch.py validate and UI checks were not run during
the active migration. All owned test processes finished. Integration and
independent full-proof review remain outstanding.
