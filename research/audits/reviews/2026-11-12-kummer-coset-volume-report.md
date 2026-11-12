# Local Kummer coset-volume report: dispositions

2026-11-12. Independent review of the completed advisory report
`audits/claude_runs/2026-11-12-fast-kummer-attack/response.md` only.
Read current `STATE.md`, the seed/volume sections of
`LOCAL_HALVING_SATURATION.md`, and
`LOCAL_SATURATION_FINITE_PRECISION.md`. No Git, network, API, numerical
control, generic rank counterexample, or new algorithm search.
Interpreter, if required: `/opt/anaconda3/bin/python`.

The volume calculation is correct under the ledger's normalization. It
gives a necessary volume threshold for an everywhere-bad coset, not a
constructive conditioning bound. The finite-grid statement is a conditional
existence statement; the report does not supply ONE-HALF, an actual-point
certificate, or an algorithm to find a favorable representation. Several
quantifiers and its global tail domain need correction.

1. **Seed and lattice calculations: verified.** The stated coefficient
   bound gives `v2(L_k(t_i))>=N`, hence `log L subset 2^N Z2^g`.
   Since `F(t_i^2)=1 mod 16`, the selected square root and seed point are
   defined over `Q2`. With `d log_k=omega_k` and additive Haar measure
   normalized by `mu(Z2^g)=1`, the full-rank logarithm lattice has index
   `2^D0`. Therefore

   ```
   mu(L)=2^-D0,              mu(E)=2^-(D0+g),  E=2L.
   ```

   Smith normal form gives `2^D0 Z2^g subset log L`; consequently
   `J_(D0+1)=L intersect log^-1(2^(D0+1)Z2^g)` is contained in `E`.
   These use the previously reviewed injective formal logarithm and
   determinant formula, not a newly constructed integral model.

2. **Coset-volume transfer: verified; headline inference rejected.**
   For a Borel loss function and `B_K={P:beta(P)>=K}`, translation
   invariance gives exactly

   ```
   mu(B_K intersect (h+E))/mu(h+E)
       <= 2^(D0+g) mu(B_K).
   ```

   Equal coset volumes do NOT imply that a conditioning obstruction cannot
   be coset-specific. The bad set can contain one coset and omit others;
   the inequality then merely forces its global measure to be at least
   `mu(E)`. The report's statement excluding a coset-specific obstruction
   must be removed. No native bad family is constructed by this logical
   observation.

3. **Corollary 1: necessary threshold verified, with scope corrections.**
   If EVERY point of `h+E` has best-representation loss at least `K`,
   then `mu(B_K)>=2^-(D0+g)`. This is the valid corollary. Such a coset
   is itself an open set because `L` has full logarithmic rank. A
   measure-zero subset of the actual point group cannot contain it.
   A representation degeneracy counts here only if its image is proved
   measure zero in the actual point domain; being a proper subset of an
   unrelated ambient matrix/chart space is insufficient. The statement
   about tubes is only the same necessary volume threshold, not a proved
   tube-measure estimate.

   The report's phrase “every nonzero h” is false for a nonzero element
   `h in E`. The correct condition is `h notin E`, equivalently nonzero
   modulo `E`; only then is `(h+E) intersect J_(D0+1)` empty.

4. **The global tail assumption (S) has a domain defect.** Under the
   report's successful-halving definition, admissible data include the
   Stoll square root for the point being halved. For `P notin 2G` no
   such successful data exist, so the infimum over admissible data is
   `beta(P)=infinity`. Here `[G:2G]=2^(g+t)`, with
   `t=dim_F2 G[2]`, so this is a positive-volume set. A bound
   `mu_G{beta>=K}<=2^(A-K/D)` tending to zero cannot hold on ALL `G`.

   Repair the domain to `2G`, or explicitly define a different loss
   functional that includes a finite-cost nondivisibility outcome.
   Every reachable zero-Kummer input has `h+E subset 2G`, so the volume
   argument still applies using the tail on `2G`. For that repair the
   necessary `K=0` condition is `A>=log2 mu(2G)`, not necessarily
   `A>=log2 mu(G)`. The report's stronger upper-volume allowance remains
   sufficient but does not fix its original domain. This correction is
   not a new obstruction to ONE-HALF on its promised inputs.

5. **Corollary 2: conditional grid transfer verified, not an algorithm.**
   On the corrected domain, (S) and (L) give the asserted probability
   calculation. A Haar-uniform coefficient vector can be written
   `x=n+2^R z`, with `n` uniform modulo `2^R`. The difference between
   the Haar point and the exact finite-grid point is in

   ```
   2^(R+1)L subset J_(R+N+1).
   ```

   Thus `R>=K*+c'`, together with local stability (L), transfers Haar
   success at `K*=D(A+D0+g+sigma)` to grid loss at most `K*+c` with
   probability at least `1-2^-sigma`. This is conditional on the
   Borel/tail/stability assumptions; it proves no instance of (S) or (L).

   Materialization error merely in `J_(D0+1)` preserves the `E`-coset
   but need NOT preserve the good-loss event. To reuse this coupling,
   control that error at `J_(K*+c')` or another sufficiently deep
   stability scale, or provide a separate probability analysis. (M)
   cannot be replaced by the weaker coset-error condition alone.

6. **The infimum defining beta is not constructive representation data.**
   A finite bound on integer-valued `beta(P)` guarantees existence of
   admissible data at that loss; it does not find those data, bound their
   description size, or show that a fixed materialization procedure uses
   them. Accordingly, “run Stoll at precision K*+c+1” does not follow
   from the event alone. The accepted Smith-kernel lemma applies only
   after a specific exact matrix, a represented approximation, and the
   required bounds are supplied. If the minimal index `j` is unknown,
   the ledger must also bound the full matrix used to determine `j`, or
   all tested matrices. An existential bound for the unknown `M_j`
   alone does not pay rank discovery. The augmented `B_j` injectivity
   and doubled monic-normalization loss remain mandatory.

   A computed approximate vector must still represent an ACTUAL
   Jacobian point and give residual `2q-h in E`, by a proved coordinate
   schedule or an effective certificate. Approximate congruences or
   calling the procedure Monte Carlo do not supply that proof. These
   are exactly the unclosed materialization/precision obligations of
   the existing ledger.

7. **Seed-coset attack: valid group observation, unsupported support claim.**
   The first seed class is nonzero in `L/2L` and Kummer-trivial, so it
   is a legitimate initial saturation direction. For `P in L\2L`,
   `log P` cannot belong to `2^(D0+1)Z2^g`; hence at least one log
   coordinate has valuation at most `D0`. This rules out that particular
   claim of forced superpolynomial logarithmic depth. It does not bound
   Mumford coefficients, Smith invariants, or monic losses. Membership
   in the formal subgroup does not prove that every reduced support
   point lies near infinity or that every representation is nonintegral.
   Likewise `Q notin L+G[2]` implies
   `Q notin J_D0+G[2]` simply because `J_D0 subset L`; it supplies no
   missing coordinate-conversion estimate.

8. **One-variable monic sublevel template: verified with normalization.**
   Let `K/Q2` have ramification index `e_ram`, residue degree `f_res`,
   total degree `d=e_ram*f_res`, and `mu(O_K)=1`. Use the absolute
   valuation normalized by `v2(2)=1`, extended to the algebraic closure.
   For monic degree-`n` polynomial `F`,

   ```
   v2(F(x)) = sum_(j=1)^n v2(x-alpha_j).
   ```

   If this is at least `K0>=0`, one summand is at least `K0/n`.
   Each root-neighborhood intersection with `O_K` is empty or, after
   choosing one point in it, a ball of measure

   ```
   2^(-f_res ceil(e_ram K0/n)) <= 2^(-d K0/n).
   ```

   The union bound proves `mu{v2(F(x))>=K0}<=n*2^(-d K0/n)`.
   This also covers roots outside `K`. If instead the valuation is
   normalized by `v_K(uniformizer)=1`, the exponent uses `f_res`,
   not total degree. For a nonmonic polynomial the leading-coefficient
   valuation shifts the threshold and must be charged. None of this
   proves a tail for the actual multivariable Smith/normalization/root
   computations or for the existential functional `beta`.

9. **Remaining operational remarks need qualification.** The group identity
   `half(P+2e)=half(P)+e` is true up to the known 2-torsion choice. It
   does not prove that only reduced representatives can improve loss;
   other permitted bounded-degree non-reduced charts are not excluded.
   Factoring the fixed polynomial and precomputing ambient squareclass
   coordinates can be independent of the current point. Computing the
   actual Stoll square root
   `s^2=epsilon(a-a1 f1) mod f` depends on the point's representation,
   so its precision/materialization cost is not wholly precomputation.

The only changes to the next scientific action are these corrections:
restrict the tail domain, target a CONSTRUCTIVELY SELECTED representation
with a complete loss schedule, and preserve the good-conditioning scale
during materialization. Equal volumes do not justify abandoning a
coset-specific native attack. This report supplies neither that attack nor
the constructive bound. ONE-HALF and the complete native local Kummer
algorithm remain OPEN; hardness, speedup, and full Selmer conclusions stay
unpromoted. No further test or sweep is warranted by this report alone.
