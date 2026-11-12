# Cyclic case of HSP(H_3(Z)): proofs of C1–C4 (2026-11-12)

**Status: AI-checked by one Claude Code helper session, pending an independent hostile referee
and human review.** No API agents, no git, no network. No existing file was edited. Claim gates
are unchanged (`speedup_claim_allowed`, `novelty_established` stay false). No novelty, priority
or speedup claim is made. Scripts and outputs are in
`research/audits/reviews/2026-11-12-rees-h3z-cyclic-proof/`. They run with
`nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python` (fpylll lives only in that env). Finite
checks only falsify (TRAPS 7).

Context read: `2026-11-12-rees-h3z-qzs-attack.md` (the "QZS note", Theorem C and C1–C4),
`2026-11-12-rees-h3z-infinite-index.md` (the "II note": §§0–4, Lemma C, Theorem A, Prop N) and
its scripts `twist_check.py` and `h3z_struct.py`, plus `qzs_lattice.py` and `e2e_qzs.py`. I did not
read the hardness note beyond its use in the II note. §§1–4 of the QZS note are being refereed
separately; this note is constructive.

## Verdict

| Item | Status | Section |
|---|---|---|
| C1 (QZS solution ⇒ twisted samples obey the strip relation) | **PROVED** (elementary). There is an explicit TV bound to an exact ideal law P*_α, and the good-strip mass is ≥ 1 − 2^{-7} − 2^{-14} under P*_α. | §2 |
| C2 (decoding, certification, generator) | **PROVED given cited theorems**: the LLL bounds (LLL 1982, Props 1.6, 1.12) and Shor/Kitaev period finding. Optional Las Vegas certification also uses Shor factoring. **The route differs from the QZS note**: the twisted samples give only the direction v of π(h), and c then comes from an abelian HSP in A_v. Decoding X₃ = 2c − ab directly from the twisted samples (QZS note Thm C step 3) stays **CONDITIONAL** on an unproved anti-concentration of α. It is not needed. | §4 |
| C3 (Lemma P) | **PROVED given cited theorems** (Rosser–Schoenfeld 1962 prime bounds; LLL). The recalled "Gallagher-type" overlap is replaced by an exact Parseval bound. SDA-ISO is changed to enumerate *all* q ∈ [Q, 2Q] (expected O(K) lattice points). Success per pair of coset states is ≥ 0.22, for every K ≥ 66. | §3 |
| C4 (truncation and window bounds) | **PROVED**, with explicit integer parameters (`common.params`). Every register and the oracle box exponent B are O(b) bits; namely B = max(18b + O(log b), 20b + 11), e.g. 278, 369, 441 and 1163 at b = 1, 6, 10 and 50. | §5 |
| **Theorem C′** (cyclic case H = ⟨h⟩, H ∩ Z = 1, and H = 1) | **PROVED given cited theorems** (the list in §6), in the II note's model (§0 there), with poly(b, log 1/ε) queries and poly(b, w, log 1/ε) gates. **Not promoted**: one AI session wrote it; it needs the hostile referee and a human. | §6 |
| decode_sim (acceptance ≥ 90% at b = 10) | **met**: 300/300 at each b = 6..10 (finite; falsification only). | §7 |

Combined with Theorem A (II note §2), Theorem C′ would give a quantum polynomial-time algorithm for
*every* subgroup of H_3(Z) in that model. That is ePrint 2026/2678 §10 open problem 5. Because the
consequence is large, the bar for acceptance is the referee pass, not this note. Prior art was not
searched in this pass.

## 0. Conventions

* G = H_3(Z) with (a,b,c)(a′,b′,c′) = (a+a′, b+b′, c+c′+ab′), as in the II note.
* h = (a,b,c) with w = (a,b) ≠ 0. The promise gives |a|, |b| < 2^b and |c| < 2^{2b+1} (II note §3;
  re-derived: |kc + C(k,2)ab| < 2^b with |ka|, |kb| < 2^b forces |c| < 2^b + 2^{2b−1}).
* X := (a, b, X₃) with X₃ = 2c − ab, so |X₃| < 2^{2b+3}.
* K = HZ = π^{-1}(Zw) is abelian and normal.
* e(x) = exp(2πix), and ‖x‖ is the distance to Z. C(n,2) = n(n−1)/2.
* Write w = d·v with v primitive and d = gcd(a,b).
* N₀ is the central-character denominator (the QZS note's M), and θ_i = ρ_i/N₀.
* Mb is the stage-1 Fourier box, Mb = 2^{3b+26}.
* All moduli (N₀, Mb, F_A, Q_pf) are powers of 2. P and R are rounded up to powers of 2, so the
  uniform superpositions are exact.

## 1. The algorithm CYC(b, ε)

Parameters (all explicit in §5): η_s = 2^{-10}; Mb = 2^{3b+26}; γ₁ = 2^{-(2b+19)}; K = 6b+67;
ε_S = 2^{-(K+1)}; Q = ⌈2ε_S^{-2} ln ε_S^{-2}⌉; μ_max = ⌈(4Q/√3)^{1/2}⌉; P, N, R, N₀ as in §5;
F_A = 2^{4b+30}; γ₂ = 2^{-(2b+21)}; Q_pf = 2^{2b+2}.

**Stage 0.** Run Theorem A step 1 (II note). If it accepts some r, then H ∩ Z ≠ 1, so run Theorem A
and stop. Otherwise continue; this branch is wrong with probability ≤ ε/4.

**Stage 1 sample TS.** Repeat (a)–(c) until SDA-ISO′ succeeds.
* (a) Prepare the uniform superposition over D = [−P,P)² × [−R,R) and query f. Measure the label,
  which leaves a coset state of gH ∩ D.
* (b) Apply QFT_{N₀} to the central register (N₀ ≥ 2R, so [−R,R) embeds in Z_{N₀} with no
  leftover high bits). Measure ρ. Do (a)–(b) twice, giving ρ₁, ρ₂.
* (c) Run SDA-ISO′(ρ₁, ρ₂) (§3). On failure, discard both states.
* (d) For each i, adjoin the window ξ_i = N^{-1/2}Σ_{0≤r<N} e(−θ_i r)|r⟩. Read the pair
  (π-register, window) as an element (p, r) of G.
* (e) Prepare Mb^{-1}Σ_{u∈[0,Mb)²}|u⟩. Controlled on u, apply right translation
  R_{x_i(u)}: |g⟩ ↦ |g·x_i(u)⟩ to factor i, with x_i(u) = δ_{μ_i}(u₁,u₂,0) = (μ_iu₁, μ_iu₂, 0).
* (f) Apply QFT_{Mb}^{⊗2} to u (|u⟩ ↦ Mb^{-1}Σ_y e(⟨y,u⟩/Mb)|y⟩) and measure y.
* Output (y, α), with α = A/N₀ and A = Σ_i ρ_i C(μ_i,2) mod N₀.

**Stage 1 decode.** Take m₁ = 4 TS samples and run the Lemma D decoder with d_X = 3 (§4). Output a
primitive v ∈ Z² (up to sign).

**Stage 2 (abelian, in A_v).** Use ι(t,s) = (tv₁, tv₂, s + C(t,2)v₁v₂), a homomorphism Z² → A_v.
* Take m₂ = 4 Fourier samples of (t,s) ↦ f(ι(t,s)) over [0,F_A)².
* Run the Lemma D decoder with d_X = 2. This outputs a primitive ℓ̂ ∈ Z².
* Run period finding (Shor/Kitaev) on j ↦ f(ι(jℓ̂)) over [0, Q_pf).
* Accept a candidate r (a continued-fraction denominator, or an lcm of two) only if f(ι(rℓ̂)) = f(1).
  Let ĝ be the gcd of the accepted values.
* Optionally certify: for each prime p | ĝ (Shor factoring), replace ĝ by ĝ/p while
  f(ι((ĝ/p)ℓ̂)) = f(1).
* Output h_out = ι(ĝℓ̂).

**Repetition.** Run up to T = ⌈log₁₀(4/ε)⌉ independent batches (stage 1 + stage 2). Output the
first verified h_out. If no batch produces one, output "H = 1".

## 2. C1: the twisted measurement (PROVED)

**Lemma 2.1 (coset states; PROVED).** Call the measured coset *good* if every element of gH whose
π-image lies in the square [−P,P)² has central coordinate in [−R,R). Then:
1. P(bad) ≤ V/R per coset, with V := 4P² + 2^{2b+3}P ≤ 5P² for P ≥ 2^{2b+3}.
2. On a good coset, gH ∩ D = {g h^t : t ∈ I}, where I is the integer interval
   {t : π(g) + tw ∈ [−P,P)²}.
3. ρ is exactly uniform on Z_{N₀} and independent of the coset.
4. After step (b) the π-register holds χ = |I|^{-1/2}Σ_{t∈I} e(θ c_t)|π(g)+tw⟩, where c_t is the
   central coordinate of g h^t.

*Proof.*
* Along a coset over the square, g h^t = g h^{t*}·h^Δ with |Δ| ≤ 2P/|w|_∞. The central coordinate
  changes by (h^Δ)₃ + (gh^{t*})₁Δb, whose absolute value is at most
  2P·2^{2b+1} + 2P² + P2^b + 2P² ≤ V.
* So bad cosets need |y₃| ≥ R − V for the uniformly random y ∈ D whose coset is measured, which
  has probability ≤ V/R.
* The amplitudes after the QFT are e(ρc_t/N₀)/√(|I|N₀) on the distinct basis states |π_t, ρ⟩. So
  P(ρ) = Σ_t 1/(|I|N₀) = 1/N₀ for every coset. ∎

Write ψ = χ ⊗ ξ, read as a function on G: ψ(p_t, r) = e(θ(c_t − r))/√(|I|N) for t ∈ I and
0 ≤ r < N.

**Lemma 2.2 (exact Gram law of the physical factor; PROVED).** For k = h^τ z^σ ∈ K,
⟨ψ|R_kψ⟩ = e(θσ)·A(τ,σ), with

  A = (|I|N)^{-1} Σ_{t∈I∩(I+τ)} (N − |δ_t|)₊, where δ_t = σ + τc + C(τ,2)ab + p_{t−τ,1}·τb.

So 1 − A ≤ |τ|/|I| + max_t |δ_t|/N. For k ∉ K, ⟨ψ|R_kψ⟩ = 0 exactly.

*Proof.*
* Write (R_kψ)(y) = ψ(yk^{-1}). For y = (p_t, r) = g h^t z^{r−c_t}, we have
  yk^{-1} = g h^{t−τ} z^{r−c_t−σ}.
* So conj(ψ(y))·ψ(yk^{-1}) = e(θσ)/(|I|N) exactly when t, t−τ ∈ I, r ∈ [0,N) and
  r − δ_t ∈ [0,N), where δ_t = c_t − c_{t−τ} + σ.
* The term c_t − c_{t−τ} is the central coordinate of gh^{t−τ}·h^τ minus that of gh^{t−τ}. This
  gives the stated formula.
* ψ is supported on gK, and R_kψ on gkK. These cosets differ when k ∉ K. ∎

**Lemma 2.3 (phase and support; PROVED, and also verified symbolically by
`sigma_identity_check.py`).** Let u′ = u + tw with t ∈ Z. Then
δ_μ(σ(u′))·δ_μ(σ(u))^{-1} = h^{μt} z^{σ}, where

  σ = −μ² S(u,t) + C(μ,2)·t·X₃ and S(u,t) = t a u₂ + C(t,2)ab + tc ∈ Z.

If gcd(μ₁, μ₂) = 1, then the set {Δ : μ_iΔ ∈ Zw for i = 1, 2} equals Zw.

*Proof.*
* σ(u′)σ(u)^{-1} = (Δ, −Δ₁u₂) with Δ = tw. Since δ_μ is an endomorphism, the left side is
  (μtw, −μ²ta u₂).
* Equating with h^{μt}z^σ gives σ = −μ²tau₂ − μtc − C(μt,2)ab. The identity
  C(μt,2) = μ²C(t,2) + C(μ,2)t and μ² − μ = 2C(μ,2) rearrange this into the stated form.
* For the support claim, Bezout gives Δ = xμ₁Δ + yμ₂Δ ∈ Zw. ∎

The Gauss-reduced output μ of SDA-ISO always has gcd(μ₁,μ₂) = 1. Suppose instead μ = kν with
k ≥ 2:
* if q ∤ k, then ν lies in the lattice Λ_r and is shorter;
* if q | k, then |μ| ≥ q > ((2/√3)q)^{1/2}, contradicting Lemma Q.

**Theorem C1 (PROVED).** Fix a successful SDA-ISO′ output: integers ρ₁, ρ₂, μ with
gcd(μ₁,μ₂) = 1, μ₁² + μ₂² ≤ μ_max², and ‖Θ‖ ≤ 2^{-K}, where Θ = Σθ_iμ_i². Let α = A/N₀. Define
the ideal law on Z_{Mb}²

  P*_α(y) = Mb^{-4} Σ_{lines r} F_{L_r}(ζ(y)),  where ζ(y) = ⟨y,w⟩/Mb + αX₃ and
  F_L(x) = |Σ_{0≤t<L} e(tx)|².

The sum runs over the lines of [0,Mb)² in direction w, and L_r is the length of line r. Then:
* (i) P*_α depends on y only through ⟨y,w⟩ mod Mb (**fiber uniformity**).
* (ii) The law of the output y, conditioned on (ρ₁, ρ₂), is within total variation
  η + 2V/R of P*_α, where

  η² = 2Σ_i (1.2|μ_i|Mb/P + D_i/N) + 4π²(2^{-K}·2.5Mb²)²,
  D_i = 4.5μ_i²Mb² + 2P|μ_i|Mb.

* (iii) P*_α(‖ζ‖ > γ) ≤ 2^b/(γMb) + 2^{2b}/(γ²Mb²) for every γ > 0. At γ₁Mb = 2^{b+7} this is
  ≤ 2^{-7} + 2^{-14}.

*Proof.*
* **Reference state.** Write Ψ(u) = ⊗_i R_{x_i(u)}ψ_i and Φ = Mb^{-1}Σ_u|u⟩Ψ(u). For each line
  r ∩ [0,Mb)², let r also denote its first point, and put Ψ*(r + tw) := e(αtX₃)Ψ(r) for
  0 ≤ t < L_r. Set Φ* = Mb^{-1}Σ_u|u⟩Ψ*(u).
* **Gram of Ψ.** ⟨R_xψ|R_{x′}ψ⟩ = ⟨ψ|R_{x′x^{-1}}ψ⟩. By Lemmas 2.2 and 2.3 with
  x′x^{-1} = h^{μ_it}z^{σ_i},
  ⟨Ψ(r)|Ψ(r+tw)⟩ = e(Σθ_iσ_i)·ΠA_i = e(−ΘS(r,t) + αtX₃)·ΠA_i.
  Since S ∈ Z, e(−ΘS) = e(−Θ′S), where Θ′ is Θ minus its nearest integer.
* **Distance to the reference.**
  ‖Ψ(u) − Ψ*(u)‖² = 2 − 2ΠA_i cos(2πΘ′S) ≤ 2Σ(1 − A_i) + 4π²Θ′²S².
* **Bounds on S and on the window shifts.** For |t| < Mb/|w|_∞ and base points in the box,
  |S| < 1.5Mb² + 2^{2b+1}Mb ≤ 2.5Mb². Also |τ_i| ≤ |μ_i|Mb/|w|_∞ and
  |σ_i| ≤ μ_i²(|S| + |tX₃|) ≤ 3.5μ_i²Mb², because |C(μ,2)| ≤ μ² and Mb ≥ 2^{2b+3}. Hence
  max|δ_t| ≤ D_i.
* **Line-length average.** Over the size-biased good coset,
  E[1/|I|] ≤ (2P(|a|+|b|) + d)(2R + 2V)/(8P²R(1 − V/R)) ≤ 1.1|w|_∞/P. This counts the cosets
  meeting D: at most 2R + 2V per line, and at most 2P(|a|+|b|) + d lines meet the square.
  Hence E|τ_i|/|I| ≤ 1.2|μ_i|Mb/P, and E‖Φ − Φ*‖² ≤ η².
* **Orthogonality across lines.** Ψ(r) ⊥ Ψ(r′) for different lines r, r′: then r′ − r ∉ Zw, so
  by Lemma 2.3 some factor's translation lies outside K, and Lemma 2.2 gives exact 0.
* **Ideal law.** Hence ‖Φ*‖ = 1 and Φ* measures to
  Mb^{-4}Σ_r|Σ_{t<L_r}e(t(⟨y,w⟩/Mb + αX₃))|² = P*_α(y).
* **Conclusion of (ii).** For unit vectors, TV ≤ ‖Φ − Φ*‖. Jensen bounds the expectation over
  cosets, and bad cosets add ≤ 2V/R.
* **(i)** is visible from the formula for P*_α.
* **(iii).** The map y ↦ ⟨y,w⟩ mod Mb has image gZ_{Mb}, where g = gcd(a,b,Mb). Each value has
  Mb·g preimages, and L_r ≤ Mb/g, so each line contributes a Fejér sum over the grid
  (1/N′)Z + αX₃, with N′ = Mb/g.
  * Use F_L(x) ≤ 1/(4‖x‖²).
  * The off-strip grid points have distances ≥ γ, γ + 1/N′, …, so their sum is
    ≤ 1/(2γ²) + N′/(2γ).
  * The number of lines is ≤ Mb(|a|+|b|) + d ≤ Mb·2^{b+1}. Summing gives the bound. ∎

**Corollary C1 (the relation the QZS note asked for).** Conditioned on α:

  P(‖⟨y,w⟩/Mb + αX₃‖ ≤ γ₁) ≥ 1 − 2^{-7} − 2^{-14} − 2η_s ≥ 0.990.

Here α = Σρ_iC(μ_i,2)/N₀ is known exactly. Given ⟨y,w⟩ mod Mb, y is uniform on its fiber
(exactly under P*_α, and up to the same TV for the real law).

**What the QZS note's argument lacked (now fixed).**
1. It needed the support lattice to equal Zw. This requires gcd(μ₁, μ₂, d) = 1. Otherwise the
   support is a coarser lattice Z(d′v) ⊋ Zw, with d′ = d/gcd(d, μ₁, μ₂), and with a different
   phase. gcd(μ₁, μ₂) = 1 holds automatically for SDA-ISO (above).
2. N₀ must be ≥ the central range 2R. Otherwise the high bits of the central coordinate stay
   entangled with the chirp state as garbage. The QZS note's Lemma R says "M ≥ range", so this is
   consistent with it.
3. The physical window sits in the *absolute* central coordinate, not relative to c_t as in the II
   note's ψ_θ(a). So N must exceed the t-dependent shift P|τ||b|. This is where the term 2P|μ|Mb in
   D_i comes from.
4. No mechanism failed. Sufficiency of QZS for the template is now a theorem, given the decoding
   of §4.

## 3. C3: success probability of SDA-ISO′ (PROVED given cited theorems)

**SDA-ISO′.**
* Input: ρ₁, ρ₂ ∈ Z_{N₀}, with ε = ε_S and Q as in §1.
* LLL-reduce Λ_θ = rows (W, ρ₁, ρ₂), (0, N₀, 0), (0, 0, N₀), with W = ⌊2εN₀/Q⌋.
* Enumerate all lattice vectors in the ball of radius √3·εN₀ around (1.5QW, 0, 0). The ball
  contains every q ∈ [Q,2Q] with |qρ_i − c_iN₀| ≤ εN₀.
* For each such q, test, in any order:
  1. q is an odd prime (AKS or BPSW);
  2. c₁c₂ ≢ 0 (mod q);
  3. −c₂c₁^{-1} is a square mod q.
* Take any q that passes (the code takes the smallest). Set r = √(−c₂/c₁) mod q
  (Tonelli–Shanks, Las Vegas), and output the Gauss-reduced shortest vector μ of
  {μ₁ ≡ rμ₂ (mod q)}.
* Lemma Q (QZS note, rechecked) then gives |μ|² ≤ (2/√3)q and ‖Θ‖ ≤ (2/√3)ε < 2^{-K}.

**Lemma P′ (PROVED given Rosser–Schoenfeld).** Let θ₁, θ₂ be independent and uniform on
(1/N₀)Z/Z, with N₀ ≥ 600Q/ε² and K ≥ 66. Then P(SDA-ISO′ finds a valid q) ≥ 0.22.

*Proof.* Let 𝒬 be the primes in [Q,2Q] and E_q the event that q passes.

(a) *One prime.* Consider a residue x ≢ 0 (mod q). The ρ with |qρ/N₀ − c| ≤ ε for the integer
c ≡ x number between 2εN₀/q − 1 and 2εN₀/q + 1, because q is odd and N₀ is a power of 2. The
admissible (c₁, c₂) classes number (q−1)²/2. So

  P(E_q) ≥ ((q−1)²/(2q²))·(2ε − q/N₀)² ≥ 2ε²(1 − 1/Q)²(1 − Q/(εN₀))².

(b) *Overlap* (this replaces the recalled estimate). Let A_q = {θ : ‖qθ‖ ≤ ε}. The indicator of
‖x‖ ≤ ε has Fourier coefficients ĝ(0) = 2ε and |ĝ(k)| ≤ 1/(π|k|). The indicator of A_q has
coefficients ĝ(n/q) on qZ. By Parseval, for distinct primes q, q′,

  λ(A_q ∩ A_{q′}) = Σ_j ĝ(jq′)ĝ(jq) ≤ 4ε² + 2Σ_{j≥1} 1/(π²j²qq′) = 4ε² + 1/(3qq′).

Each A_q-interval meets at most 3 of the A_{q′}-intervals (q′/q ≤ 2, ε ≤ 1/6). So the discrete
version satisfies P_ρ(‖qθ‖ ≤ ε, ‖q′θ‖ ≤ ε) ≤ λ + 3q/N₀. By the independence of θ₁ and θ₂,

  P(E_q ∧ E_{q′}) ≤ (4ε² + 1/(3Q²) + 6Q/N₀)².

(c) *Second moment.* Let Z = Σ_{q∈𝒬} 1_{E_q} and S₁ = EZ.
* By Rosser–Schoenfeld 1962 (π(x) > x/ln x for x ≥ 17, and π(x) < 1.25506x/ln x),
  |𝒬| ≥ 0.72Q/ln Q for Q ≥ 2^{100} (0.725 there). The proof only uses 0.68.
* With Q = ⌈2ε^{-2}ln ε^{-2}⌉ and K ≥ 66, Q/ln Q ≥ 1.89ε^{-2}. So S₁ ≥ 2.57.
* Also E Z² ≤ S₁ + 4.03S₁². The relative error terms are 1/(12ε²Q²) and 6Q/(ε²N₀) ≤ 1/100.
* Cauchy–Schwarz gives P(Z > 0) ≥ S₁²/EZ² ≥ 1/(1/S₁ + 4.03) ≥ 0.226. ∎

**Enumeration cost (PROVED, elementary).** Take an LLL-reduced basis b_j in dimension 3.
* The orthogonality defect gives Π‖b_j‖ ≤ 2^{1.5}det (LLL Prop 1.6). So any v in the ball has
  coordinates |z_j − z_j(center)| ≤ 2^{1.5}r/‖b_j‖.
* So the box in LLL coordinates has Π_j(5.66x_j + 1) points, with x_j = r/‖b_j‖.
* Λ ∩ B(0,r) contains Π_{j: x_j≥1}(2⌊x_j/3⌋ + 1) ≥ Π x_j/3 distinct points.
* Hence cost ≤ 8000·#(Λ ∩ B(0,r)).
* For uniform θ, E#(Λ ∩ B(0,r)) ≤ 1 + 1.74Q(2√3ε + 2Q/N₀)² ≤ 1 + 42 ln ε^{-2} = O(K).
* Capping the work at 20× this expectation loses ≤ 1/20 (Markov). So the success probability per
  pair is ≥ 0.17 after the cap, and the time is poly(K) in the worst case.
* The implementation uses Fincke–Pohst on the same ball (identical output set). Its measured
  lattice-point count matches 8 ln ε^{-2} (box points 1,153 at b = 6, against 8·ln 2^{208} = 1,153).

**Replaced alternative (not needed).** One could instead factor q by Shor and use CRT square roots.
I did not pursue this: the prime-q version is already proved.

## 4. C2: decoding (PROVED given LLL and Shor period finding)

**Lemma D (direction decoder).**

*Setup.*
* Unknown X ∈ Z^{d_X} (d_X ∈ {2,3}) with |X_j| < B_j. Its first two coordinates are
  w ≠ 0.
* There are m independent samples (y_k, α_k), with α_k ∈ (1/Den)Z/Z arbitrary and fixed before
  y_k is drawn. y_k ∈ Z_F² is drawn from a law that is fiber-uniform (it depends on y only through
  ⟨y,w⟩ mod F) and puts mass ≥ 1 − p_bad on ‖⟨y,w⟩/F + α_kX₃‖ ≤ γ (with X₃ := 0 when d_X = 2).
  Here F | Den, both powers of 2.

*Decoder.*
* Let n = d_X + m. Take the lattice with rows (ω_j e_j | c_{1j}, …, c_{mj}) for j ≤ d_X, and
  (0 | Den·e_k) for k ≤ m.
* The weights are ω_j = γDen/B_j. The coefficients are c_k = (y_{k1}Den/F, y_{k2}Den/F, A_k)
  with α_k = A_k/Den.
* LLL-reduce. Output the primitive part of (X′₁, X′₂) for the first of b₁, b₂ with
  (X′₁, X′₂) ≠ 0. Here X′(b) = (b_j/ω_j)_j are the first d_X coordinates of b.

*Claim.* Suppose:
* 2^{2(n−1)}·n·γ·2B₃ < 1 (only for d_X = 3, the no-wrap condition);
* 2^{n−1}√n·γ < 1.

Then the decoder outputs ±w/gcd(w) with probability at least

  1 − m·p_bad − Π_j(2^n√n B_j + 1)·(2^n√n(γ + B₁B₂/F))^m.

*Proof.*
* **True vector.** Every sample is good with probability ≥ 1 − m·p_bad. Then the lattice vector
  of X has norm ≤ R_t := √n γDen. LLL gives ‖b₁‖ ≤ 2^{(n−1)/2}λ₁ ≤ 2^{(n−1)/2}R_t (LLL Prop 1.12).
* **The event E.** Let E be: "every X′ ∈ Z^{d_X} with |X′_j| ≤ 2^{n−1}√nB_j, (X′₁, X′₂) ∉ Qw,
  fails some sample at tolerance γ′ = 2^{n−1}√nγ".
* **Bound on P(E fails).** Fix X′ and condition on α_k and on the fiber value. Then ⟨y_k, w′⟩ mod F
  is uniform on a coset of a subgroup S ≤ Z_F. Since (w₂, −w₁) lies in the fiber group, S contains
  ω(w,w′) ≠ 0. So |S| ≥ F/|ω| ≥ F/(2^n√nB₁B₂), and
  P(‖⟨y_k,w′⟩/F + α_kX′₃‖ ≤ γ′) ≤ 2γ′ + 1/|S|. Independence across k and a union bound over the
  box give the stated failure term.
* **Under E, b₁.** Every lattice vector of norm ≤ ρ_max := 2^{n−1}R_t has X′ ∈ Qw × Z. b₁ is one
  of them. A vector with X′ = 0 has norm ≥ Den > ρ_max, so X′(b₁) ≠ 0.
* **Under E, b₂.** If d_X = 3 and (X′₁, X′₂)(b₁) = 0, then b₁ ↔ (0,0,D₁). The true vector is
  independent of b₁, so λ₂ ≤ 2^{(n−1)/2}R_t and ‖b₂‖ ≤ ρ_max. If b₂ ↔ (0,0,D₂) as well, then
  D₂b₁ − D₁b₂ has X′ = 0 and norm ≤ 2ρ_max²/ω₃ < Den. That forces it to be 0, contradicting the
  independence of b₁ and b₂. ∎

**Stage-1 instance (PROVED).** d_X = 3, m = 4, n = 7, Den = N₀, F = Mb = 2^{3b+26},
γ = 2^{-2b-19}, B = (2^b, 2^b, 2^{2b+3}).
* No-wrap: 2^{12}·7·2^{-2b-19}·2^{2b+4} = 2^{-0.19} < 1. ✓
* p_bad ≤ 2^{-7} + 2^{-14} by Theorem C1(iii), and fiber uniformity is C1(i). Lemma D applies to
  the ideal law with α_k = A_k/N₀.
* The union term Π_j(2^7√7B_j + 1)·(2^7√7(2^{-2b-19} + 2^{-b-26}))⁴ is ≤ 2^{-18} for every b ≥ 1.
  It is computed for b ≤ 200, with the maximum at b = 1. Beyond that the expression decreases
  to 2^{-42}, since the 4b terms cancel and the residual 4log₂(1 + 2^{7−b}) decreases.
* So P(correct v | ideal) ≥ 1 − 4(2^{-7} + 2^{-14}) − 2^{-18} ≥ 0.968. Counting the TV of 4
  samples, ≥ 0.968 − 8η_s ≥ 0.960.

**Stage 2 (PROVED).** For a correct v, H ⊆ A_v (Lemma C), and ι^{-1}(H) = Zℓ with ℓ = (d, s₀),
s₀ = c − C(d,2)v₁v₂, |d| < 2^b and |s₀| < 2^{2b+2}.
* The coset states of f∘ι on [0,F_A)² are exact line segments. Their Fourier law is *exactly*
  P*_0 for ℓ (no truncation error), and it is fiber-uniform.
* Lemma D with d_X = 2, m = 4, n = 6, γ₂ = 2^{-2b-21}, F = Den = F_A = 2^{4b+30} and
  B = (2^b, 2^{2b+2}) applies:
  * p_bad ≤ 0.0044;
  * the union term is ≤ 2^{-43} (computed for b ≤ 200, maximum at b = 1);
  * so P(ℓ̂ = ±ℓ/g) ≥ 0.98, where g = gcd(d,s₀) < 2^b.
* j ↦ f(ι(jℓ̂)) hides exactly gZ. Shor/Kitaev period finding over Q_pf = 2^{2b+2} ≥ 2g² returns g
  per run with probability Ω(1/log log g) (Shor 1997; Mosca–Ekert §§2, 4.2; cited, as in Theorem A).
* **Certification.** Every accepted r is a multiple of g, because f(ι(rℓ̂)) = f(1) ⟺ g | r. So
  ĝ is a multiple of g whenever some r is accepted.
  * The prime-by-prime reduction ends exactly at g. If ĝ = jg with j ≠ 1, a prime p | j passes the
    test.
  * So h_out = ι(gℓ̂) = h^{±1}, a **certified generator**.
  * Without factoring, h_out is still always in H, and it is a generator with high probability.
* **Wrong v.** If v is wrong, H ∩ A_v ⊆ H ∩ Z = 1, so no r ≥ 1 is ever accepted. A non-trivial
  output is never wrong.

**Signs.**
* v, ℓ̂ and h_out are determined only up to sign. A_v = A_{−v}, and h^{−1} generates H.
* The QFT sign convention cannot hurt stage 1: replacing α by −α maps the short vector (w, X₃) to
  (w, −X₃), with the same direction.
* The first decode_sim run used "decoder given −α" as a control. It still recovered h 150/150, so
  it is not a control (it is kept in `decode_sim_run1_signcontrol.out`). The real control uses an
  unrelated α′ (§7).

**Direct decoding of X₃ (QZS note Thm C step 3; CONDITIONAL, not used).** Decoding X from the
twisted samples alone also needs rejection of X′ = (λw, X′₃) with X′₃ ≠ λX₃. That requires
anti-concentration of α_k at scale γ, i.e. P(‖Dα_k‖ ≤ 2γ′) ≤ 1 − κ for all 0 < |D| < 2^{2b+5}.
* The model is α ≈ j/q with 2j ≡ −c₁r(1−r)μ₂ (mod q). This suggests j is near-uniform on Z_q^*
  given (q, r).
* But the selection of q by SDA-ISO′ correlates with c₁ mod q, so the property is **UNKNOWN**
  (not proved).
* Empirically, X = ±X′(b₁ or b₂) in 1,480/1,500 first batches (§7, seed 2027) and in 1,462/1,500
  with seed 2026.

## 5. C4: explicit parameters (PROVED)

All of the following are integers, rounded up (`common.params`, with η_s = 2^{-10}):

| Quantity | Choice | Forced by |
|---|---|---|
| Mb | 2^{3b+26} | Lemma D stage 1 (union term, no-wrap) with γ₁Mb = 2^{b+7} |
| K | 6b + 67 | phase term 4π²(2^{-K}·2.5Mb²)² ≤ η_s²/2 |
| ε_S, Q | 2^{-(K+1)}, ⌈2ε_S^{-2}ln ε_S^{-2}⌉ | Lemma Q, Lemma P′ |
| μ_max | ⌈(4Q/√3)^{1/2}⌉ | Lemma Q |
| P | ⌈19.2μ_maxMb/η_s²⌉ (≥ 2^{2b+3}) | 4·1.2μ_maxMb/P ≤ η_s²/4 |
| N | 16D/η_s², D = 4.5μ_max²Mb² + 2Pμ_maxMb | window term ≤ η_s²/4 |
| R | 10P²/η_s | 2V/R ≤ η_s |
| N₀ | 2^{n₀} ≥ max(2R, 600Q/ε_S², Mb) | Lemma 2.1 (no garbage), Lemma P′ |
| F_A, Q_pf | 2^{4b+30}, 2^{2b+2} | Lemma D stage 2, period finding |
| B | max(log₂R + 1, 10b + 62, 20b + 11) | the oracle box |

`params_table.py` → `params_table.out` gives exact bit sizes:

| b | log₂Mb | K | log₂Q | log₂μ_max | log₂P | log₂N | log₂R | log₂N₀ | B |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 29 | 73 | 155.7 | 78.4 | 131.7 | 264.2 | 276.7 | 313 | 278 |
| 6 | 44 | 103 | 216.2 | 108.7 | 177.0 | 354.6 | 367.2 | 434 | 369 |
| 10 | 56 | 127 | 264.5 | 132.8 | 213.1 | 426.9 | 439.5 | 530 | 441 |
| 50 | 176 | 367 | 746.0 | 373.6 | 573.9 | 1148.5 | 1161.1 | 1492 | 1163 |

The sizes are linear in b: log₂N₀ ≈ 24b + 290 and log₂R ≈ 18b + 260 (plus O(log b), from the ln ε^{-2} factor in Q). **B = O(b) for the cyclic
case.** (Theorem A still needs B = poly(b) because of Kuperberg's step.)

Per-sample budget at b = 10 (computed):
* phase term 2.3·10^{-7};
* truncation term ≤ 4.8·10^{-7};
* bad cosets 9.8·10^{-4};
* so TV ≤ 1.82·10^{-3} ≤ 2η_s.

State preparation is exact: uniform superpositions over power-of-2 boxes, QFTs over powers of 2,
and windows of exact length N (a power of 2 after rounding).

## 6. Theorem C′ and its status

**Theorem C′ (PROVED given cited theorems; AI-checked, pending referee and human review).**

*Statement.*
* Model: the II note §0. The oracle f is coherent on matrices with entries in (−2^B, 2^B),
  B = params(b)['B'] = max(⌈log₂R⌉ + 1, 10b + 62, 20b + 11) = max(18b + O(log b), 20b + 11)
  (§5). Left cosets.
* Promise: H has a generating set with entries < 2^b, and H ∩ Z = 1, so H = ⟨h⟩ or H = 1.
* Guarantee: CYC(b, ε) outputs either h^{±1}, certified (always in H, and a generator), or
  "H = 1".
* Error: when H ≠ 1, "H = 1" is output with probability ≤ ε/2.
* Cost: O(log 1/ε) batches. Each batch uses about 8/0.17 + 4 + O(log b) queries in expectation
  (capped), and poly(b, w) gates.

*Cited theorems.*
* LLL 1982 (Props 1.6, 1.12);
* Rosser–Schoenfeld 1962 (prime-counting bounds);
* Shor/Kitaev period finding (Mosca–Ekert §§2, 4.2);
* Tonelli–Shanks; primality testing (AKS);
* optionally Shor factoring for certification.

Together with Theorem A this covers every subgroup. Theorem A carries its own imports (Kuperberg
Thm 1.5/7.1, cor:utz), and its step 1 is what certifies H ∩ Z = 1.

*Proof.* Assemble §§2–5.
1. **Per batch.** Stage 1 succeeds with probability ≥ 0.960 (Lemma D and C1). Stage 2 gives the
   direction with probability ≥ 0.98. Period finding succeeds with probability ≥ 0.99 after
   O(log log 2^b) runs with lcm pairs; the constant comes from the cited Ω(1/log log g) bound. So each batch succeeds with probability ≥ 0.93, and
   0.07^T ≤ ε/4.
2. **Soundness.** Outputs are verified by f, so a non-trivial output is never wrong.
3. **Uniformity.** The SDA retries consume fresh coset pairs. ρ is independent of the coset
   (Lemma 2.1), so conditioning on success does not bias the coset law. ∎

What is *not* covered: other access models (e.g. a box without signed entries), and an unknown b
(doubling is unsound, as for Theorem A).

## 7. Simulations (falsification only)

**c1_explicit.py → c1_explicit.out (independent of the Part-B law).**
* Construction: explicit physical states ψ_i = χ_i ⊗ ξ_i on explicit coset segments. The Gram
  entries ⟨R_xψ|R_{x′}ψ⟩ are computed *from the group law only*: an explicit sum over t, and an
  exact r-sum.
* Settings: Mb = 8, N₀ = 2^{24}, μ found by brute force with ‖Θ‖ ≤ 2^{-14}. Eight instances.
* Results:
  * cross-line overlaps are exactly 0;
  * TV(P, P*) ≤ ‖Φ − Φ*‖ ≤ the analytic bound in every instance ("ALL INEQUALITIES HOLD");
  * with long segments (|I| = 2–3·10⁴, N = 10^{12}), TV(P, P*) = 0.0010 and 0.0007, and the strip
    masses agree to 0.001.
* The tiny-size rows have large truncation terms (|μ|Mb/|I| ≈ 0.1–0.8), and the bound tracks the
  explicit distance closely.

| h | μ | log₂\|Θ′\| | \|I\| | N | TV(P,P*) | ‖Φ−Φ*‖ | bound | strip 1/8: P / P* |
|---|---|---|---|---|---|---|---|---|
| (0,3,5) | (12,−1) | −14.2 | 2000 | 1e6 | 0.0256 | 0.298 | 0.299 | 0.571 / 0.592 |
| (3,1,−10) | (18,−35) | −21.4 | 400 | 1e9 | 0.0527 | 0.431 | 0.441 | 0.510 / 0.557 |
| (−1,0,5) | (14,−19) | −14.5 | 6000 | 1e9 | 0.0128 | 0.196 | 0.196 | 0.966 / 0.974 |
| (0,−3,0) | (8,−33) | −15.0 | 20000 | 1e12 | 0.0010 | 0.060 | 0.060 | 0.814 / 0.815 |
| (−2,1,3) | (6,−19) | −14.8 | 30000 | 1e12 | 0.0007 | 0.045 | 0.045 | 0.638 / 0.639 |

(Three further rows are in the .out file.)

`sigma_identity_check.py` checks Lemma 2.3 on 200,000 random large integer cases (0 mismatches),
and sympy confirms it as a polynomial identity.

**decode_sim.py → decode_sim.out.**
* Sampling: the samples are drawn exactly from P*_α (sampler self-test: TV to the exact law equals
  the null TV of an exact draw, 4 cases). α comes from running the full SDA-ISO′ at the *real*
  parameter sizes (N₀ up to 2^{530}).
* Stage 2 uses the exact abelian law. Shor's outcome law is simulated exactly, and acceptance goes
  through the membership oracle only.
* Trials: 300 random h per b, half with |c| < 2^b and half with |c| < 2^{2b}.

| b | log₂Mb | K | log₂N₀ | trials | h recovered, 1st batch | h recovered, ≤ 3 batches | direction ok / batches | SDA tries per sample | off-strip samples (bound 0.0079) | direct X decode, 1st batch (heuristic) | s/trial |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 44 | 103 | 434 | 300 | 300/300 | 300/300 | 300/300 | 1.017 | 1/1200 | 295/300 | 0.17 |
| 7 | 47 | 109 | 458 | 300 | 300/300 | 300/300 | 300/300 | 1.028 | 1/1200 | 297/300 | 0.18 |
| 8 | 50 | 115 | 482 | 300 | 300/300 | 300/300 | 300/300 | 1.015 | 1/1200 | 294/300 | 0.19 |
| 9 | 53 | 121 | 506 | 300 | 300/300 | 300/300 | 300/300 | 1.023 | 0/1200 | 299/300 | 0.20 |
| 10 | 56 | 127 | 530 | 300 | 300/300 | 300/300 | 300/300 | 1.027 | 0/1200 | 295/300 | 0.22 |
| control: decoder given an unrelated uniform α′, b = 10 | | | | 150 | 0/150 | 0/150 | 0/450 | | | 0/150 | |

Reading the table:
* **Acceptance test (≥ 90% at b = 10): met, 300/300.**
* SDA-ISO′ succeeds on about 98% of pairs, against the proved ≥ 0.22.
* The off-strip rate is 3/6000, within the bound 0.0079.
* The direct-X₃ route succeeds 1,480/1,500, consistent with the unproved anti-concentration.
* The control fails completely, so the relation with the true α is what carries the decoding.
* Run 1 (seed 2026; `decode_sim_run1_signcontrol.out`) gave the same 300/300 rows, with direct
  decoding 1,462/1,500. Its "−α" control succeeded 150/150, which is why it is not a control.
* `common.params` was switched from float to integer arithmetic between the two runs; all bit sizes
  are unchanged.
* The table reports `decode_sim.py 300 2027 6 10`.

Margins (`margins.py` → `margins.out`, b = 10, stage-1 box shrunk below the proved 2^{3b+26} with
γ = 2^{b+7}/Mb):

| log₂Mb | log₂γ | trials | direction ok, 1st batch | h recovered, 1st batch |
|---|---|---|---|---|
| 18 (b+8) | −1 | 100 | 0/100 | 0/100 |
| 20 (b+10) | −3 | 100 | 0/100 | 0/100 |
| 26 (2b+6) | −9 | 100 | 16/100 | 16/100 |
| 32 (2b+12) | −15 | 100 | 100/100 | 100/100 |
| 56 (3b+26, proved) | −39 | 100 | 100/100 | 100/100 |

The decoder breaks where the counting predicts. With m = 4 samples, it needs about
4·log₂(1/γ) > 4b + 3 bits (the size of X); at 2b+6 this is 36 < 43. The proved box is about 24 bits
more conservative than needed. The failures at small Mb show the decoder is not succeeding
trivially.

## 8. Adversarial self-check

* **Too easy?** The QZS note did the hard step (SDA-ISO). Everything here is bookkeeping plus one
  design change: decode only the direction, then go abelian. The step most likely to hide an
  error is Theorem C1. Its ingredients are each checked:
  * the Gram law of the *physical* state (Lemma 2.2), derived from the group law and matched by
    c1_explicit with explicit states;
  * the σ identity (symbolic);
  * cross-line orthogonality (exact zeros);
  * the reference-state argument (two lines of algebra; TV ≤ ‖Φ − Φ*‖ held in every instance).
* **Hidden circularity in ε, K, |μ|?** None. μ_max depends on Q, hence on K, hence on Mb. P, N, R
  depend on μ_max and Mb. N₀ depends on R and Q. Nothing depends on N₀ except the uniformity
  argument, which needs N₀ ≥ 2R. This works, but it is a real ordering: N₀ is the largest
  parameter (24b + 290 bits) and must be chosen last.
* **Does a large N₀ hurt SDA?** No. Lemma P′ only needs N₀ ≥ 600Q/ε², and a larger N₀ only
  shrinks the error terms.
* **Lemma D independence.** The α_k are fixed before y_k is drawn (ρ is measured first). The
  union bound is over a fixed candidate box, and fiber uniformity is exact for P*. The real law
  is only TV-close, and that is paid per sample.
* **Is stage 2 cheating, i.e. does it need v?** It uses only the decoded v. A wrong v makes f∘ι
  injective, and no candidate passes. The simulation models this with uniform samples. That is the
  exact law for an injective f, since the coset states are single points.
* **Things I could have got wrong.**
  * The size-biased coset average E[1/|I|]. It is bounded through the coset count, and the
    constant 1.1 assumes P ≥ 10 and V/R ≤ 0.05; both hold by a wide margin.
  * Whether C(μ,2) ≤ μ² covers negative μ. It does: |μ|(|μ|+1)/2 ≤ μ² for |μ| ≥ 1.
  * The Rosser–Schoenfeld constant 0.72 at Q ≥ 2^{100}. This was recomputed:
    2/(1 + ln 2/ln Q) − 1.25506 ≥ 0.725. Recalled from the 1962 paper; not re-read here (TRAPS 10:
    a human should confirm the two inequalities).
  * Lemma D's no-wrap margin is tight: 2^{-0.19} < 1. It holds but leaves little room. Shrinking γ
    by a factor 2 would give comfort, at the cost of one more bit of Mb.
* **Finite evidence.** 300/300 at every b only falsifies. The margins table shows the decoder
  succeeding about 24 bits below the proved box and failing, as counting predicts, at
  log₂Mb ≤ 2b + 6. So the proved constants are conservative. The simulation samples the *ideal*
  law P*_α, so it does not test C1: it tests C2 and C3 at real sizes. C1 is tested only by
  c1_explicit at toy sizes, where Mb = 8 and |μ| ≤ 40, far from the real |μ| ≈ 2^{133}.
* **Controls.** "Decoder given −α" succeeded 150/150 and is not a control (X₃ ↦ −X₃). The real
  control (unrelated α′) failed 0/150 (§7).
* **Not claimed:**
  * novelty or priority (no literature search in this pass; the result is large enough that a
    prior or simultaneous solution must be checked);
  * a speedup;
  * that the survey problem is "solved" before the referee pass.
* **The direct-X₃ route** stays CONDITIONAL and is not used.

## 9. Next

* **Next hard question:** does Theorem C1 survive the hostile referee? In particular Lemma 2.2,
  i.e. the absolute-window state actually prepared, and the reference-state construction. Does
  Lemma D's union bound hold for the exact P*?
* **Next command:** give an independent referee only §§1–6 of this note, plus `common.py` and
  `c1_explicit.py`. The obligation: confirm or refute Theorem C1 (ii) with the stated η, and
  Lemma D's claim.
* **Artifact:** `2026-11-12-rees-h3z-cyclic-proof-referee.md`.
* **Acceptance test:** every lemma is CORRECT or CORRECT WITH FIXES, with no GAP in C1 or Lemma D.
  After that, a prior-art search ("quantum algorithm discrete Heisenberg group infinite cyclic
  hidden subgroup") goes before any STATE row moves.
