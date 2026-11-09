# Verdict

**Not proved either way.** No constructive polynomial-BIT bound for Stoll Prop 5.1 inside this saturation loop exists in the supplied material, and no superpolynomial family is proved. What I can prove: (i) the candidate's own generator family forces *every* halving into the regime Stoll's paragraph (lines 899–910) warns about, so "rare in practice" is unavailable; (ii) the constant-`h` chart repair has an explicit polynomial resultant bound; (iii) the remaining gap is one precise unpaid dictionary, stated below.

# 1. Cheapest decisive attack: the candidate starts inside the failure mode

**Proved deduction.** With `f` monic (`c=1`), `a = x − x_i`, Stoll's map gives `μ(P_i) = (−1)^1 (θ − x_i) = x_i(1 − θ/x_i)`. `x_i = 2^{-2N} i^{-2}` is a square in `Q_2`; `θ` is integral; so `v_2(θ/x_i) ≥ 2N ≥ 4 > 3`, and `1+u` with `v_2(u) ≥ 3` is a square in every component of `L` (binomial series converges: term valuation `≥ 3n − 2n`). Hence **`μ(P_i) = 0` for every `i`**, i.e. all free generators already lie in `2J(Q_2)`. Consistency check via Stoll (3.1)–(3.2): `P_i ∈ K_{N+v(i)} = 2^{N+v(i)−2} K_2`.

**Consequences (proved from the candidate's own loop).**
- The initial Kummer rank from `H` is `r−1`; all `g` free directions require halving, and by the candidate's own determinant valuation (`Ng² + Σv(i) + Σv(j²−i²)` versus `2g` for `log K_2 = (4Z_2)^g`) the loop performs `Θ(Ng²)` halvings. Polynomial in count, but each is a Prop 5.1 call on a point deep in the formal group (`deg a < g`, non-integral `x_i`, "close to infinity") whose output lies in `T + K_{m−1}`, i.e. near 2-torsion or near `0`: the "near-branch" and "lower-degree divisor" cases. This is the generic case for this procedure, not an exceptional one.
- So the obligation cannot be discharged by Stoll's remark that problems "occur fairly rarely". Any BIT bound must address the degenerate regime directly.

**Illustrative deduction (g=2, not a general proof).** The formal half of `φ(t)` is not `φ(t')`: `g=1` gives `t' = t/2 + O(t³)`, but for `g=2` power sums force `t'_{1,2} = t(1 ± √5)/4` with `√5 ∉ Q_2` (unramified) and `v(t') = v(t) − 2`. Depth is lost per halving and the support leaves `Q_2`; Mumford coefficients stay in `Q_2` but the resultant/discriminant valuations of `w` grow with each round. Whether the loss is `O(log g)` or worse per round for general `g` is **unproved**.

# 2. Bit accounting of Prop 5.1 over `Q_p` (component by component)

Inputs: `f ∈ Z[x]`, `(a,b)` and `s` at absolute precision `M` (bits), plus a maximal order of `L`.

**(a) Maximal order / factorization of `L`.** Needed to test squareclasses and compute `s`. *Assumption:* polynomial-time maximal-order (Round-4/Montes-type) algorithms for `Q_p[x]/f` with `v_p(disc f) ≤ poly(g,B)`; the repo must cite a specific statement. Not verified here.

**(b) Square root `s`.** Given `v_j(a(θ_j))` in each component `L_j` (ramification `e_j`), squareness is decided by `2e_j+1` uniformizer digits beyond the valuation; Hensel loses `≤ 2e_j+1 ≤ 4g+3` digits. **Proved-standard, polynomial, conditional on knowing `v(Res(a,f))`.**

**(c) Chart repair `a' = c − 2hb − h²a` (constructive, proved bound).** From `f − b² = ac`: at a root `θ_j` with `a(θ_j) ≠ 0`,
`a'(θ_j) = −(b + ha)(θ_j)² / a(θ_j)`.
The set `{h ∈ Z_p : v_j((b+ha)(θ_j)) ≥ v_j(a(θ_j)) + e_j m'}` is contained in one class mod `p^{m'}`. With `m' = ⌈log_p(2g+2)⌉` the ≤`2g+1` bad classes do not cover `{0,…,p^{m'}−1}`, so some constant `h` of `O(log g)` bits gives
`−v(Res(a,f)) ≤ v(Res(a',f)) ≤ v(Res(a,f)) + 2(2g+1)·m'`,
with `d' = 1`, `deg a' ≤ 2g+1`. Finding `h` needs no exact zero test: try all `p^{m'} = O(g)` candidates, keep one whose resultant valuation (computed at working precision `> v(Res(a,f)) + 2(2g+1)m'`) meets the bound. **This repairs the near-branch input issue polynomially, provided `v(Res(a,f))` itself is polynomially bounded.** Squarefreeness of `a'` is not proved (Stoll: "probably"); state as obligation.

**(d) Exact gcd tests.** `d = gcd(a,f)`, `d₁ = gcd(u,w)`, `d_f`, `d_a`, and "minimal-degree `w`" are exact tests on `p`-adic data. Partial repair: for points built from generators, the Weierstrass part of `a` is known *by construction* (`a = d·a₁` with `d` an exact `Q_p`-factor of `f` carried symbolically), so `d` needs no detection. **Not repaired:** `d₁`, `d_f`, `d_a` on the *output*, and the rank determination selecting minimal `deg w`. Precision loss in solving (5.1) is bounded by the valuation of a maximal nonzero minor `Δ` of the `O(g)×O(g)` system; nothing in the excerpt bounds `v(Δ)`. In the candidate's first round (`a = x−x_i`, `s ≈ 2^{-N}i^{-1}(1+O(2^{2N−2}))`) the system is nearly degenerate with `v(Δ)` plausibly `≈ g(2N−2)` — polynomial, but this is a heuristic estimate, not a proof.

**(e) Output accuracy → Néron neighborhood.** What is needed: `Q'` with `Q' − Q ∈ 2J(Q_p)` (`⊇ K_3` at `p=2`, from (3.2)). **Proved:** `μ(Q)` is determined by `w` to absolute precision `max_j v_j(w(θ_j))/e_j + 3`, i.e. `v(Res(w,f)) + O(1)` digits suffice for the Kummer label. **Unproved:** any bound on `v(Res(w,f))` for halves, and any model-free translation "Mumford precision `M` ⇒ `K_m`-membership". Two structural reasons this is not automatic:
- `Sym^g C → J` is **not** a local isomorphism at `g·∞`: the fibre over `0` is `|g∞|`, of dimension `⌊g/2⌋ ≥ 1` for `g ≥ 2`. So the `∞`-disk (the only model-free disk, Stoll (3.1)) does not give formal-group coordinates in general-position Mumford form; points of `K_m` can be represented by divisors `P + ιP'` with `P' → ιP` and unbounded `b`-coefficients. Stoll's "lower degree/infinity" warning is exactly this.
- Near Weierstrass points with bad/dyadic reduction, residue disks of the (unsupplied) regular model subdivide `{v(x−θ_j) > 0}`; the relation between `v(x−θ_j)` and `K_m` depends on that model.

**(f) Lattice bookkeeping.** `log K_2` is defined via the Néron formal group; the candidate's `L_k` use standard differentials. The index of the standard lattice in the Néron lattice is unpaid (candidate concedes). Plausibly `≤ v(disc f)`-type, hence polynomial, but no citation.

# 3. Proof obligations (to close this obligation positively)

1. Polynomial bound on `v(Res(a,f))` and `v(Res(w,f))` for every input/output of the loop (needs (e)).
2. Bound `v(Δ)` for (5.1), or prove the solution space is 1-dimensional whenever `w` is coprime to `f` with a computable pivot bound; replace minimal-degree selection by a certified construction.
3. Model-free dictionary: `Q'` within `p^{-M}` of `Q` in Mumford coordinates ⇒ `Q' − Q ∈ K_m`, with `M = m + poly(g,B)`, uniformly at `p=2`.
4. Squarefreeness of `a'` for some `h` in the `O(g)` candidate set.
5. Citations for (a) and (f).

# 4. Falsifiers / controls

- **Decisive control family:** `f = ∏_{i=1}^{2g+1}(x − 4i)` over `Q_2` (`L = Q_2^{2g+1}`, no extension arithmetic, `r = 2g+1`, target rank `3g`). Run the loop with the candidate's `P_i` at `N=2,3`; record working precision needed per halving versus `g`. Growth faster than any fixed polynomial in `g` on this family falsifies the candidate as stated; polynomial growth is evidence only, not proof.
- **Falsifier of my §1:** exhibit `i` with `μ(P_i) ≠ 0` for `N ≥ 2` (would refute the square-root argument).
- **Falsifier of repair (c):** an `(a,b,f)` where every `h` in the candidate set yields `v(Res(a',f))` above the stated bound, or `a'` never squarefree.

# 5. What remains unproved

Polynomial BIT cost of ONE half, for arbitrary bad/dyadic `f` and growing `g`, is unproved; the specific gap is obligation 3 (Mumford↔Néron precision dictionary near `0` and near Weierstrass points) feeding obligations 1–2. No family requiring superpolynomial precision is proved. The excerpt's "chart replacement" is shown here to be polynomially bounded for the near-branch input case only; the "lower degree / near infinity" cases, which this candidate hits at every step, are not repaired by it.