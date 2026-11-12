# Referee of the QZS attack (H_3(Z), cyclic case H = ⟨h⟩, H ∩ Z = 1) (2026-11-12)

**Status: AI-checked, pending human review.** One hostile-referee Claude Code helper session.
No API agents, no git, no network. No existing file was edited; the attack note is unchanged.
Claim gates (`speedup_claim_allowed`, `novelty_established`) stay false. Target:
`2026-11-12-rees-h3z-qzs-attack.md` §§1–4 (the "attack"), its scripts `qzs_lattice.py`,
`e2e_qzs.py` and outputs. Background read: `2026-11-12-rees-h3z-infinite-index.md` §§3, 4, 9
(the "infinite-index note") and `2026-11-12-rees-h3z-hardness.md` §§6–7 (the "hardness note").
My checks are in `2026-11-12-rees-h3z-qzs-referee/` and run with
`nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python referee_checks.py [part]` (fpylll and
cypari2 live in that env). Finite checks can only falsify (TRAPS 7).

## Verdict

**CORRECT WITH FIXES for the QZS algorithm (§§1–3); Theorem C stays CONDITIONAL, now
essentially on one gap (C2, decoding).**

* The barrier really was an artifact. Solving the quadratic congruence modulo the character
  denominator forces |μ|² ≈ denominator, which the truncation forbids. An auxiliary modulus
  q ≈ 2^{2K}, found by simultaneous Diophantine approximation, avoids this.
* Lemma Q is CORRECT as stated. I re-derived it exactly, and every reported success is
  verified in exact integer arithmetic.
* Lemma P was CONDITIONAL on a recalled overlap estimate. **It can be proved.** I give an
  elementary Parseval proof of a sharper overlap bound, |λ(A_p ∩ A_p′) − 4ε²| ≤
  gcd(p,p′)²/(3pp′). With M ≥ 2^{4K+O(log K)} and a polynomial-delay enumeration (Lenstra's
  fixed-dimension integer programming, recalled), the result is: QZS(n = 2, precision
  2^{-K}, |μ| ≤ 2^{K+O(log K)}) on exactly uniform samples is solved classically in expected
  poly(K) time. A sample pair succeeds with probability ≥ 0.2. This is **PROVED given cited
  standard theorems** (Lenstra 1983 and a prime count in [Q/2, Q]; both recalled).
* In Theorem C, C1 is not an independent gap. It follows from Prop N's per-factor law, the
  hardness note's closed form (Lemma 7.1) and primitivity of μ. C4 reduces to explicit
  parameter inequalities, all satisfiable with poly(b, K) bits (sketch below). **C2 remains
  the genuine open step.** C2 is: recover X = (w, 2c − ab) from Fourier samples of a
  finite-box, character-twisted rank-1 law with known per-sample offsets α_k.
* Gaps the attack did not list (all fixable):
  * (G1) The physical state of the infinite-index note §3 has a t-dependent window drift. The
    Part-B law, used by `e2e_qzs.py` and Lemma R, omits it. Part 5 shows the omission is
    real: overlap 0.34 where the Part-B law says 1.00.
  * (G2) μ must be primitive.
  * (G3) The claim "a non-trivial output is always correct" is overstated.
  * (G4) The literal §9 acceptance test (|μ| ≤ 2^K) is not met by SDA-ISO. The attack's
    remark about it has the direction wrong.
* No circularity: SDA-ISO uses only the measured ρ_i, and every window is fixed a priori from
  b, K and ε.

Not claimed: a theorem for HSP(H_3(Z)), a speedup, or novelty. Theorem C must not move a STATE
row until C2 is written and refereed.

## Table

| # | Item | Verdict | Fix / counterexample |
|---|---|---|---|
| 1 | Lemma R: barrier is an artifact of working mod the denominator | CORRECT | Exact solution mod the denominator D gives |μ|² ≈ D, but truncation needs μ²S ≪ window ≤ poly·D. SDA-ISO moves the congruence to q ≪ D. |
| 1 | Lemma R: T, N, M free with poly bits; costs stay poly | CORRECT WITH FIXES | T is not directly free. It is the coset-segment length, set by the box exponent B (free, poly(b)) and the random coset, so the constraint is on B and on the segment-length distribution (C4′). The §3 preparation also needs N ≫ \|τ\|·max_t\|c_{t+1} − c_t\| ≈ μ·Mb·2^{B+b+1} (drift, G1; Part 5). The cleaner fix is the ISS-Lemma-4 preparation (hardness note §7, window = denominator W, no drift; Part 5 confirms its closed form). Then J ≫ μMb/η and W ≫ μ²S/η. Every bound is a lower bound with poly bits, and queries and gates stay poly. |
| 2 | Lemma Q: ‖θ₁μ₁²+θ₂μ₂²‖ ≤ (2/√3)ε | CORRECT | Exact re-derivation below. Checked exactly on all 947 Part-1 outputs, with 0 violations of 3(μ₁²+μ₂²)² ≤ 4q² and of ‖Θ‖q ≤ \|e₁\|μ₁² + \|e₂\|μ₂². |
| 2 | Composite q, non-square | CORRECT WITH FIXES | With gcd(c₁c₂, q) = 1, q odd and t a square mod every p^e ∥ q, Hensel plus CRT give r, and Lemma Q holds verbatim (index q). Factoring q (Shor, since the algorithm is quantum anyway) works and raises the success rate (Part 1: 99–100% against 78–88% for primes only). But the shortest vector **need not be primitive** for composite q: 9–20 of 200 outputs per K (Part 1), and this breaks exact orthogonality (G2). Fix: require gcd(μ₁, μ₂) = 1, otherwise take the next q. For prime q primitivity is automatic (proof below). Classically, stay with primes: a square root mod an unfactored composite is as hard as factoring (Rabin, recalled). A non-square means taking the next q. |
| 2 | P(E_q) formula | minor slip | The correct value is 4ε²·(q−1)(q+1)/(2q²), since t = 0 also works (the code accepts it). Immaterial. |
| 2 | "§9 acceptance test met; \|μ\| ≤ 2^K needs ε₀ smaller by 2^{-8}" | WRONG (wording) | A smaller ε₀ makes q and μ *larger*. SDA-ISO needs q ≳ ε^{-2}·(prime and QR density)^{-1}, so \|μ\| ≈ 2^{K + ½log₂K + O(1)}. The literal test (\|μ\| ≤ 2^K at precision 2^{-K}) is not met, only its 2^{poly} relaxation, which is all Lemma R needs. |
| 3 | Lemma P (success probability) | GAP → FIXED (PROVED given Lenstra 1983 and a prime count in [Q/2,Q], both recalled) | The needed estimate is the pairwise overlap λ(A_p∩A_p′) ≤ 4ε² + 1/(3pp′) for coprime p, p′. It is proved here by Parseval (Lemma O). It is stronger than the recalled 4ε² + O(ε/max) and is of the classical Duffin–Schaeffer / Gallagher / Pollington–Vaughan type, e.g. Harman, *Metric Number Theory*, ch. 2–3 [recalled; exact lemma number not checked]. Two further points: discretization needs M ≫ Q/ε², i.e. M ≥ 2^{4K+O(log K)}, not 2^{3K}; and the Fincke–Pohst cost is not bounded by the expected point count, so it is replaced by Lenstra bisection. Finite: 0 violations in 360 exact cases (Part 2); hit counts match 2ε²Q within 1% (Part 1). |
| 3 | θ exactly uniform, θ₁ ⊥ θ₂ | CORRECT | P(ρ \| a) = 1/M for every coset a, because the segment points are distinct (non-central h). Distinct preparations are independent. For dyadic M and odd q, the hit count is exactly 2⌊εM⌋+1 and c mod q is uniform to ±1 (Part 3). The same holds for the ISS preparation (P(k \| a) = 1/W). |
| 4 | `qzs_lattice.py` reproduction and exactness | CORRECT | Seed 7 reproduces every row exactly except timings (`rerun_seed7.out`); seed 11 is similar (`rerun_seed11.out`). θ is never a float: ρ and M are integers, LLL runs on exact integer matrices, and success uses `Fraction`. An imperfect fpylll reduction can cost successes, never soundness. |
| 4 | `e2e_qzs.py` | CORRECT, weak | The output agrees with the note (0.649/0.862/0.724). An independent reimplementation from the exact formula (Part 6, Mb = 32) puts 0.86–0.88 of the mass within 0.1 of ⟨y,w⟩/Mb = −γ, against 0.06–0.07 at +γ. This tests only the phase algebra (β formula, sign, half-integer c′) under the idealized law with N = T = ∞. Box 16 resolves offsets to 1/16 and ‖Θ‖ only down to about 2^{-10}. It cannot see truncation, drift (G1) or decoding. One of my three h's is degenerate (2c = ab gives γ = 0). |
| 5 | Theorem C: chain complete except C1–C4? | CONDITIONAL; GAPs G1–G3 added | C1 reduces to Lemma H below (PROVED given hardness-note Lemma 7.1 and primitive μ). C4 becomes explicit inequalities (sketch), plus C4′, the segment-length distribution and two-interval segments when ab ≠ 0. **C2 is the one substantive open step.** K must grow with the Mb that C2 needs (K ≥ 2log₂Mb + 2b + log 1/η, still Θ(b)). G3: f(h) = f(1) certifies only h ∈ H. Fix: run the root test below. |
| 5 | Circularity | none | SDA-ISO uses only ρ₁, ρ₂, K, M. The a priori bound \|μ\|² ≤ (2/√3)Q fixes B, J, W and N before any state is prepared. |

## 1. Lemma R (obligation 1)

*Why the old barrier was an artifact.* In both earlier notes the character denominator D (N₀,
or W) was also the modulus of the congruence. Solving c₁μ₁² + c₂μ₂² ≡ 0 mod D exactly gives a
lattice of determinant D, so |μ|² ≈ D. The twisted factor shifts the window by
σ_i = μ_i²(s₀+tΩ) + ((μ_i²−μ_i)/2)(2c−ab)t (Part 4, 300/300 exact for |μ| up to 2^{90}), and
this must be ≪ the window. In the ISS preparation the window equals D, so exact solutions are
excluded. In the §3 preparation, D ≥ the central register range ≥ T²|ab|, so |μ| ≈ √D violates
J ≫ |μ|Mb. With an auxiliary q ≈ 2^{2K}, one only needs |μ|² ≈ 2^{2K} ≪ window, plus D ≥
2^{3K} for the SDA. This is CORRECT.

*Corrected constraint list (replacement text for Lemma R).* Use the ISS-Lemma-4 preparation
(hardness note §7):
* measure f on the box (−2^B, 2^B)³, which gives a segment {a h^j : j ∈ I} with |I| = J;
* append Σ_{s<W}|s⟩ and multiply by z^{-s};
* QFT the s register over Z_W and measure k.

This gives χ = Σ_{j∈I, s<W} e(−ks/W)|a h^j z^s⟩, with k exactly uniform and independent of a.
The closed form ⟨χ|χ·h^m z^σ⟩ = (1−|m|/J)(1−|σ|/W)e(kσ/W) is confirmed on explicit vectors in
Part 5 (phase error ≤ 2e-15). Then the template with φ_i = δ_{μ_i} on the Fourier box [0,Mb)²
needs:
* (R1) J_i ≥ |μ_i|·Mb/(|w|_∞η) for both factors;
* (R2) W ≥ max_i(μ_i²S + |μ_i²−μ_i|·2^{2b+2}·Mb)/η, where
  S := max|s₀ + tΩ| ≤ Mb²·2^{b+2} + Mb·2^{2b+2};
* (R3) ‖Θ‖·S ≤ η, i.e. K ≥ log₂S + log₂(1/η);
* (R4) W ≥ 2^{4K+O(log K)} (Lemma P′ below);
* (R5) B ≥ 2log₂(max J) + 2b + O(1), so typical segments are long enough (C4′).

Every one is a lower bound with poly(b, K, log 1/η) bits, so the oracle box, the registers,
the QFTs and the group arithmetic are all poly.

If one keeps the infinite-index note's §3 preparation (absolute central window r ∈ [0,N)), the
overlap is
⟨ψ|ψ·h^τz^σ⟩ = e(θσ)·(1/(TN))·Σ_{t′} max(0, N − |σ + c_{t′} − c_{t′−τ}|),
where c_t is the central coordinate of ah^t. Part 5 confirms this exactly: for example
a = (400, 11, −30), τ = 1, σ = 0, N = 2000 gives 0.344, while the Part-B law says 1.000. So it
additionally needs N ≫ |τ|·max_t|c_{t+1} − c_t| ≈ |μ|·Mb·2^{B+b+1}/η. That is still
polynomial, but it is missing from Lemma R and from the Part-B law (G1). The ISS preparation
avoids it.

## 2. Lemma Q (obligation 2), exact re-derivation

Data: a prime q, integers c_i, and e_i := qθ_i − c_i with |e_i| ≤ ε. Also q ∤ c₁, r² ≡ −c₂c₁^{-1}
(mod q), Λ = {μ : μ₁ ≡ rμ₂ mod q} with [Z²:Λ] = q, and μ a shortest nonzero vector of Λ. Then:
1. c₁μ₁² + c₂μ₂² ≡ μ₂²(c₁r² + c₂) ≡ 0 (mod q).
2. Θ := θ₁μ₁² + θ₂μ₂² = (c₁μ₁² + c₂μ₂²)/q + (e₁μ₁² + e₂μ₂²)/q, and the first term is an integer.
   So ‖Θ‖ ≤ (|e₁|μ₁² + |e₂|μ₂²)/q ≤ ε|μ|²/q.
3. Hermite: |μ|² ≤ γ₂·det Λ = (2/√3)q. So ‖Θ‖ ≤ (2/√3)ε, which is < 2^{-K} for ε = 2^{-(K+2)}.
4. |μ|_∞ ≤ (2q/√3)^{1/2}.

The SDA error enters only through |e_i| ≤ ε. The size of q enters only through |μ|. **CORRECT.**

*Primitivity (G2, PROVED for prime q).* Suppose μ = gν with g > 1. If q ∤ g, then ν ∈ Λ and ν is
shorter, a contradiction. If q | g, then |μ| ≥ q > (2q/√3)^{1/2}. So gcd(μ₁, μ₂) = 1.

*Why primitivity matters.* If d := content(w) and g_i := gcd(d, μ_i), then a single factor
fails to separate u from u + (d/g_i)w₀. Part 4 gives h = (4,6,1), μ = 6, where
δ_μ(σ(w/2)) ∈ K. The product separates them iff gcd(g₁, g₂) = 1, which gcd(μ₁, μ₂) = 1
guarantees.

*Composite q (CORRECT WITH FIXES).* Let q = Πp^e be odd, with gcd(c₁c₂, q) = 1 and t a QR mod
every p. Tonelli–Shanks mod p, Hensel to p^e and CRT give r with r² ≡ t (mod q). Λ has index q,
and steps 1–4 hold verbatim, but primitivity can fail. Part 1 finds 9–20 non-primitive outputs
per 200 trials, all for composite q and none for prime q. Fix: discard and take the next hit.

Factoring q:
* Quantumly, Shor makes every hit usable, with success density about 2^{-ω(q)}. Its average is
  ≍ 1/√(log q) (Selberg–Delange [recalled]), against 1/(2 ln q) for primes.
* Classically, use primes only. Without the factorization, square roots mod q are as hard as
  factoring (Rabin [recalled]).

Neither route is needed for polynomial time.

## 3. Lemma P (obligation 3): replacement, PROVED given cited standard results

**Lemma O (overlap; PROVED).** Let A_p = {x ∈ R/Z : ‖px‖ ≤ ε} with ε < 1/2, and let p ≠ p′ with
d = gcd(p,p′). Then |λ(A_p ∩ A_p′) − 4ε²| ≤ d²/(3pp′).

*Proof.* g = 1_{[−ε,ε]} on R/Z has ĝ(k) = sin(2πkε)/(πk) and ĝ(0) = 2ε. 1_{A_p}(x) = g(px) has
Fourier coefficient ĝ(n/p) when p | n and 0 otherwise. By Parseval,
λ = Σ_{L|n} ĝ(n/p)ĝ(n/p′) with L = pp′/d. That equals 4ε² + Σ_{m≠0} ĝ(mp′/d)ĝ(mp/d), whose
absolute value is ≤ 4ε² + Σ_{m≠0} d²/(π²m²pp′) = 4ε² + d²/(3pp′). ∎

[computed] Part 2: 360 exact cases (Fractions; coprime and non-coprime pairs, four ε regimes)
give 0 violations; the maximum of |err|/bound is 0.735.

**Discretization.** θ = ρ/M. Then A_p ∩ A_p′ is a union of fewer than p + p′ intervals. Each
interval's grid count differs from M·length by at most 1, so the discrete measure is within
(p+p′)/M of λ. For dyadic M and odd q, ρ ↦ qρ is a bijection mod M. So P(‖qθ‖ ≤ ε) =
(2⌊εM⌋+1)/M exactly, and given a hit, c ≡ −xM^{-1} (mod q) is uniform up to q/(2εM)
(Part 3 exact). Independence of θ₁ and θ₂ makes c₁ and c₂ independent.

**Lemma P′ (PROVED given (a) Lenstra 1983, integer feasibility in fixed dimension in polynomial
time [recalled], and (b) #primes in [Q/2,Q] = (1+o(1))Q/(2 ln Q) [PNT, recalled]).**

Setup:
* ε = 2^{-(K+2)}, Q = ⌈Cε^{-2} ln(ε^{-2})⌉ with C ≥ 2;
* θ₁, θ₂ i.i.d. uniform on (1/M)Z/Z with M = 2^m ≥ K·Q·ε^{-2};
* E_p = {‖pθ_i‖ ≤ ε for i = 1, 2, gcd(c₁c₂, p) = 1, and −c₂/c₁ a QR mod p}, for p prime in
  [Q/2,Q].

Second moment:
* P(E_p) = 2ε²(1+o(1)), so S₁ := Σ_p P(E_p) = (1+o(1))ε²Q/ln Q ≥ (1+o(1))C/2.
* For p ≠ p′, P(E_p ∧ E_p′) ≤ (λ_M(A_p∩A_p′))² ≤ 16ε⁴(1+o(1)), by Lemma O and
  ε²pp′ ≥ ε²Q²/4 → ∞.
* So S₂ ≤ 4S₁²(1+o(1)), and Chung–Erdős gives P(∪E_p) ≥ S₁/(1+4S₁) − o(1) ≥ 0.2 for C ≥ 4.

Algorithm:
* List all hits q ∈ [Q/2,Q] in increasing order. Bisect on q with the Lenstra feasibility test
  for {(q, c₁, c₂) ∈ Z³ : q ∈ [lo,hi], |qρ_i − c_iM| ≤ εM}. Since ε < 1/2, c_i is unique given q.
* Each hit costs O(log Q) feasibility calls. E[#hits] = (Q/2)(2ε)²(1+o(1)) = O(K).
* Abort after 100·E[#hits]; by Markov this loses ≤ 0.01.
* For each prime hit, run BPSW or AKS, Euler's criterion, Tonelli–Shanks (Las Vegas) and Gauss
  reduction.

Total: expected poly(K) time, success ≥ 0.19 per pair, and fresh pairs boost it.

[computed] Part 1 (full Fincke–Pohst enumeration, M = 2^{4K+40}, C = 2; 200 trials per K, 150
at K = 200):

| K | mean #hits [pred 2ε²Q] | P(good prime) | CE bound | 1−e^{−S₁} | incl. composite | max log₂\|μ\| |
|---|---|---|---|---|---|---|
| 20 | 121.6 [122.0] | 166/200 | 0.219 | 0.828 | 200/200 | 24.9 |
| 40 | 233.0 [232.9] | 156/200 | 0.220 | 0.843 | 200/200 | 45.5 |
| 60 | 343.8 [343.8] | 177/200 | 0.221 | 0.848 | 199/200 | 65.7 |
| 100 | 564.9 [565.6] | 168/200 | 0.221 | 0.854 | 199/200 | 106.0 |
| 200 | 1118.1 [1120.1] | 131/150 | 0.222 | 0.859 | 149/150 | 206.4 |

The success rate sits near the Poisson guess, well above the proved bound, with no decay in K.
The attack's decay at large K comes from its fixed-radius heuristic, as it says. Primality is
proved (PARI `isprime`) for K ≤ 60 and BPSW for K ≥ 100; composites were partially factored
to 2^{22} (unfactored ones were skipped, so the composite column is a lower bound).

## 4. Scripts (obligation 4)

* `qzs_lattice.py 100 7` reran in 13 s. All ten rows are identical to `qzs_lattice.out`
  except timing.
* Exactness: ρ and M are Python integers. The lattice entries (up to 2^{958}) go to fpylll as
  an exact IntegerMatrix. c_i is recovered by exact division, and success is
  `dist_int(Fraction(ρ₁μ₁² + ρ₂μ₂², M)) ≤ 1/2^K`. Floats appear only in the printed log₂. No
  precision issue at K = 300.
* `e2e_qzs.py` (read, not rerun): its phases are exact mod M (`(rho*d[1]) % M`) before the
  float division, which is fine.
* The check is a consistency test of the Prop N residual character under the idealized law,
  not of truncation, so it is not independent of twist_check Part B (the attack says so).
* Part 6 is an independent reimplementation from the exact σ formula of Part 4, and confirms the
  offset sign.

## 5. Theorem C (obligation 5): replacement text

**Lemma H (sufficiency; PROVED given hardness-note Lemma 7.1, for interval segments).**
Take χ_i from the ISS preparation (denominator W, segment length J_i, measured k_i). Let μ be
primitive, Θ = Σk_iμ_i²/W and γ = Σ(k_i/W)((μ_i²−μ_i)/2)(2c−ab). Put
Ψ(u) = ⊗_iχ_i·δ_{μ_i}(σ(u)) on u ∈ [0,Mb)². Then:
* ⟨Ψ(u)|Ψ(u′)⟩ = 0 if u′−u ∉ Zw;
* ⟨Ψ(u)|Ψ(u+tw)⟩ = e(tγ + Θ(s₀+tΩ(u)))·Π_i(1−|μ_it|/J_i)(1−|σ_i|/W).

So, entrywise, the Gram matrix is within η_e := 2π‖Θ‖S + Σ_i(|μ_i|Mb/J_i + max|σ_i|/W) of the
ideal block-rank-one Gram e(tγ). The ideal Gram is PSD, with blocks the Zw-lines in the box,
each of length L ≤ Mb+1. Block-diagonal trace-norm counting gives
TV(y-law, ideal law) ≤ (L/2)η_e. Under (R1)–(R3) with η ≤ ε/Mb, the TV is ≤ ε.

The ideal law depends on y only through ⟨y,w⟩ mod Mb. It is a Fejér-type law in
⟨y,w⟩/Mb + γ mod 1.

**Theorem C′ (CONDITIONAL on C2 and C4′).**
1. Step 1 of Theorem A reports H ∩ Z = 1 (wrong with probability ≤ ε/4).
2. Repeat k = O(b + log 1/ε) times:
   * prepare two ISS states with W = 2^{4K+O(log K)};
   * run SDA-ISO (Lemma P′; fresh pairs on failure; discard non-primitive μ);
   * Fourier-sample y_k from Ψ;
   * record α_k = Σ(k_i/W)(μ_i²−μ_i)/2 mod 1.
3. (C2) Recover X = (w, 2c−ab) ∈ Z³, |X| < 2^{2b+3}, from the pairs (y_k/Mb, α_k), each
   satisfying ⟨y_k,w⟩/Mb + α_kX₃ ≈ 0 mod 1, with error at most ~|w|/Mb from the Fejér law.
   Set h = (w, (X₃ + w₁w₂)/2).
4. Verify f(h) = f(1) (one query).
5. **Root test (fixes G3).** For each prime ℓ | gcd(w₁,w₂), factored with Shor or by trial
   division, compute the unique ℓ-th root of h in H_3(Z) if it exists, query it, and replace h
   by any root that passes; iterate. Then the output generates H whenever H is cyclic.

Every non-trivial output is a subgroup of H. It equals H with probability ≥ 1 − ε.

Cost: poly(b, log 1/ε) queries and gates, given C2 and C4′.

* **C2 (open, the real gap).** Unknown bits ≈ 4b+3, and a wrong X′ ∉ ZX has uniform residual
  on the strip. So O(b) samples suffice information-theoretically even at constant noise
  (argued). A polynomial decoder (LLL in dimension 3+k) with a noise and precision analysis is
  not written. It will force Mb = 2^{cb}, and K grows with Mb through (R3) but stays Θ(b).
  α_k ≈ −(c₁μ₁+c₂μ₂)/(2q) mod 1 is equidistributed only heuristically. If it is concentrated,
  the fallback is the note's I1 route (direction only, then Kuperberg on A_v).
* **C4′ (bookkeeping).** When ab ≠ 0, {j : ah^j ∈ box} can be two intervals; the overlap is
  still ≥ 1 − 2|m|/J_min. The length-weighted coset distribution must give
  P(J_i < J_min) = O(J_min/J_typ). Not written.
* C1 and C3 are discharged: C1 by Lemma H, C3 by Lemma P′.

## 6. Adversarial self-check

* **Did I just accept the attack?** No. I checked every lemma independently and found three
  gaps it missed:
  * G1, the drift, demonstrated in Part 5;
  * G2, primitivity, with a counterexample in Part 4 and frequent failures for composite q in
    Part 1;
  * G3, the correctness overclaim.

  I also found the §9 acceptance-test wording error. None of them reopens the barrier: each fix
  is a poly-bit parameter choice or a cheap extra test.
* **Is Lemma O too good?** Its error, 1/(3pp′), is far smaller than 4ε² in this regime. That is
  standard: for coprime moduli the two hit sets are close to independent once ε ≫ 1/p. The
  exact interval computation in Part 2 found no violation. The proof is two lines of Parseval;
  a human should still check the coefficient formula and the gcd case.
* **Hidden reliance on recalled results.** Lemma P′ uses Lenstra (fixed-dimension IP) and the
  prime number theorem, both standard and recalled, not re-read. Composite-q remarks use
  Rabin and Selberg–Delange [recalled], but nothing depends on them. Everything else is
  elementary.
* **Is the ISS preparation really available here?** Its closed form is the hardness note's
  Lemma 7.1, and my explicit vectors in Part 5 match it. It needs the segment to be an
  interval (C4′). I did not check that its uniformity P(k|a) = 1/W survives two-interval
  segments, though it should, since the points are still distinct.
* **Finite checks.** All of them can only falsify. The Part 1 table is not a proof of Lemma P′;
  the proof is the second-moment argument. The e2e checks, both theirs and mine, use the
  idealized law.
* **What would reopen the obstruction.** Either a proof that C2 fails, i.e. that the per-sample
  offsets α_k carry too little information or cannot be decoded efficiently, or a flaw in
  Lemma H's orthogonality for some h. Neither was found.
* **Claim gates** stay false. Theorem C′ is CONDITIONAL. The QZS algorithm (Lemmas Q + P′) is
  PROVED given cited standard theorems: AI-checked, pending human review.

## 7. Next command

Write `decode_sim.py` (the attack's §9) against the **ideal Fejér law** of Lemma H, plus α_k
drawn from real SDA-ISO outputs, at b = 6–10 and Mb = 2^{3b+4}. The decoder is LLL on the
(3+k)-dimensional embedding.
* **Artifact:** a success-against-b table.
* **Acceptance test:** at least 90% recovery of X at b = 10 from k ≤ 4b samples. A pass is only
  evidence; it still needs the written C2 proof.

Files:
* `2026-11-12-rees-h3z-qzs-referee/referee_checks.py`
* `checks_2to6.out` (Parts 2–6)
* `checks_part1_K20-60.out`, `checks_part1_K100.out`, `checks_part1_K200.out`
* `rerun_seed7.out`, `rerun_seed11.out`
