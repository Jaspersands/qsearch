# Attack on QZS, the quadratic zero-sum obstacle in the cyclic case of HSP(H_3(Z)) (2026-11-12)

**Status: AI-checked, pending human review.** One Claude Code helper session, no API agents, no
git, no network. No existing file was edited. Claim gates are unchanged
(`speedup_claim_allowed`, `novelty_established` stay false). Scripts and outputs are in
`research/audits/reviews/2026-11-12-rees-h3z-qzs-attack/`. They run with
`nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python` (fpylll lives only in that env, TOOLBOX).
Finite checks can only falsify (TRAPS 7). Context read: `2026-11-12-rees-h3z-infinite-index.md`
(the "infinite-index note", §§3, 4, 7, 9) and `2026-11-12-rees-h3z-hardness.md` (the "hardness
note", §§7, 10), plus their scripts `twist_check.py`, `h3z_struct.py`, `e2e_fourier.py`.

## Verdict

**The QZS obstacle is not a barrier. In the regime the template needs, QZS has a
classical polynomial-time algorithm** (heuristic in one place; rigorous up to a recalled
metric Diophantine lemma, §2). One gets n = 2 and |μ| ≈ 2^{K+7} with ‖θ₁μ₁² + θ₂μ₂²‖ ≤ 2^{-K},
using a 3-dimensional LLL plus a 2-dimensional Gauss reduction. It works for every K tested up to
300, in under 0.05 s per instance, on 100 trials per K (table in §3).

Consequence (CONDITIONAL, §4): the cyclic case H = ⟨h⟩, H ∩ Z = 1, of HSP in H_3(Z) gets a
**candidate quantum polynomial-time algorithm** in the ISS-type twist template. It rests on four
named conditions:
* (C1) sufficiency of QZS in the template, which the infinite-index note argues but does not prove;
* (C2) the final decoding step (or import I1);
* (C3) the success-probability lemma for the auxiliary modulus;
* (C4) the truncation bookkeeping.

**This is not a theorem**, and nothing here solves the survey's open problem. It removes the
specific obstruction both earlier notes named. The hardness question B is therefore moot for QZS
in this regime (§6).

The reason the earlier analysis missed this: both notes worked modulo the character denominator
N (or W). There the isotropic lattice has minimum about √N, exactly the truncation limit. The fix
is to work modulo an **auxiliary modulus q ≪ N** chosen by simultaneous Diophantine
approximation. The residual error then scales as ε·|μ|²/q, which is independent of q.

## 1. The problem and the regime actually needed

QZS (infinite-index note §4): given n i.i.d. exactly uniform θ_i = ρ_i/M ∈ (1/M)Z/Z, find
μ ∈ Z^n∖0 with ‖Σθ_iμ_i²‖ ≤ 2^{-K}. Here K = Θ(b + log 1/ε) is the phase precision, set by the
Fourier box, about 3b + O(1).

**Lemma R (regime; PROVED from the note's §3 construction, bookkeeping only).** The template
imposes only these constraints on μ:
* T ≫ n·|μ|·t_max, where T is the coset-line length;
* N ≫ n·μ²·σ_max, where N is the re-appended central window;
* M ≥ the central-coordinate range of the step-1 coset segment, about T²|ab| + T|c| (needed for
  the step-2 QFT to give an exactly uniform θ).

T, N and M are all chosen by the algorithm with poly(b) bits. M may exceed the range, because the
register is just larger and P(ρ) = 1/M still holds for distinct π-points. So any |μ| ≤ 2^{poly(b)}
is admissible.

The note's phrase "|μ| ≪ √N" is the constraint |μ| ≪ T ≤ √(M/|ab|). It binds only if one insists
on solving the congruence modulo M itself.

So the needed regime is: denominator free (poly bits), |μ| ≤ 2^{poly}, precision 2^{-K}. In the
hardness note's construction (window W = denominator), the analogous constraint μ²s_max ≪ W is
met by taking log W = 3K + O(b).

## 2. Algorithm SDA-ISO (n = 2)

Input: θ_i = ρ_i/M (i = 1, 2) with M ≥ 2^{3(K+2+s)}, where s is a slack parameter.
1. **SDA.** LLL-reduce the rows (W, ρ₁, ρ₂), (0, M, 0), (0, 0, M), with W = M·ε₀³ and
   ε₀ = 2^{-(K+2+s)}. A lattice vector is (qW, qρ₁ − c₁M, qρ₂ − c₂M), i.e. q and c_i with
   e_i := qθ_i − c_i. Enumerate small combinations of the reduced basis and keep those with
   |e_i| ≤ ε := 2^{-(K+2)}.
2. **Auxiliary modulus.** Keep the first such q that is prime, with q ∤ c₁ and t := −c₂c₁^{-1} a
   square mod q.
3. **Isotropic line.** Set r = √t mod q (Tonelli–Shanks). Gauss-reduce the lattice
   Λ = {(μ₁, μ₂) : μ₁ ≡ rμ₂ mod q}, which has determinant q, and output its shortest vector μ.

**Lemma Q (PROVED; elementary).** Suppose q, c, r are as in steps 1–3. Then μ ≠ 0,
μ₁² + μ₂² ≤ (2/√3)q, and ‖θ₁μ₁² + θ₂μ₂²‖ ≤ (2/√3)ε < 2^{-K}.

*Proof.*
* Since c₁r² ≡ −c₂ (mod q), we get c₁μ₁² + c₂μ₂² ≡ μ₂²(c₁r² + c₂) ≡ 0 (mod q).
* Hence θ₁μ₁² + θ₂μ₂² = (c₁μ₁² + c₂μ₂²)/q + (e₁μ₁² + e₂μ₂²)/q, where the first term is an integer.
* The second term has absolute value at most ε(μ₁² + μ₂²)/q.
* Hermite's constant in dimension 2 gives λ₁(Λ)² ≤ (2/√3)det Λ.

∎

Every output in §3 is also verified with exact rational arithmetic (`Fraction`).

**Lemma P (success probability; CONDITIONAL on a recalled Gallagher-type overlap estimate).**
Fix ε and Q = Cε^{-2}·ln(ε^{-2}). For a prime q ∈ [Q/2, Q], let E_q be the event "‖qθ₁‖, ‖qθ₂‖ ≤ ε,
q ∤ c₁, and −c₂/c₁ is a square mod q". For uniform θ we have P(E_q) = 4ε²·(q−1)/(2q). This holds
because, given the hit, the c_i are uniform mod q: each residue owns one interval of length 2ε/q.
So Σ_q P(E_q) ≈ C.

Recalled (not re-read): for coprime q ≠ q′, λ({‖qθ‖ ≤ ε} ∩ {‖q′θ‖ ≤ ε}) ≤ 4ε² + O(ε/max(q,q′)).
This is (1 + o(1))·(2ε)² when ε ≫ 1/Q, which holds here (ε ≈ Q^{-1/2}). Independence of θ₁ and θ₂
and the second-moment (Chung–Erdős) inequality then give P(∪E_q) ≥ 1/4 − o(1). The QR condition
is not needed in the second moment, because P(E_q ∧ E_q′) ≤ P(hit_q ∧ hit_q′).

All lattice points with q ≤ Q and |e_i| ≤ ε are enumerated from the LLL basis (Fincke–Pohst in
dimension 3). Their expected number is O(ε²Q) = O(log Q). So the algorithm runs in time
poly(K) and succeeds with constant probability per sample pair. Fresh pairs boost this.

The implemented enumeration (combinations with coefficients ≤ 5) is a heuristic stand-in for the
full enumeration. A quantum variant could replace "q prime" by Shor-factoring q; its success
density 2^{-ω(q)} is also heuristic.

Output size: q ≈ 2^{2K+O(1)} and |μ| ≈ 2^{K+O(1)}. Counting suggests n = 2 solutions exist from
|μ| ≈ 2^{K/2}. The method loses a factor 2 in the exponent, which is irrelevant for polynomial
time.

## 3. Success rate against K (`qzs_lattice.py 100 7` → `qzs_lattice.out`)

Each row is 100 independent random (ρ₁, ρ₂) with M = 2^m. "≤ 3 pairs" retries with fresh
samples, each pair being two coset states. The dist column is log₂‖Θ‖ for the worst success.
LIN is the baseline requested by the infinite-index note: Coppersmith-style linearization, i.e.
LLL on (A, B, m) with θ₁A + θ₂B ≈ m, then combinations searched for square A and B.

| K | m | first pair | ≤ 3 pairs | max log₂\|μ\| | max log₂ dist | mean q tried | s / instance | LIN |
|---|---|---|---|---|---|---|---|---|
| 20 | 118 | 100/100 | 100/100 | 27.2 | −23.8 | 76 | 0.006 | 0/100 |
| 30 | 148 | 100/100 | 100/100 | 37.1 | −34.0 | 111 | 0.004 | 0/100 |
| 40 | 178 | 99/100 | 100/100 | 47.3 | −43.3 | 116 | 0.006 | 0/100 |
| 50 | 208 | 99/100 | 100/100 | 56.8 | −53.7 | 154 | 0.006 | not run |
| 60 | 238 | 97/100 | 100/100 | 67.2 | −63.7 | 189 | 0.006 | not run |
| 80 | 298 | 91/100 | 100/100 | 87.9 | −82.9 | 202 | 0.006 | not run |
| 100 | 358 | 89/100 | 100/100 | 107.2 | −103.3 | 211 | 0.007 | not run |
| 150 | 508 | 85/100 | 99/100 | 157.7 | −153.4 | 246 | 0.010 | not run |
| 200 | 658 | 70/100 | 97/100 | 207.4 | −203.4 | 253 | 0.019 | not run |
| 300 | 958 | 53/100 | 89/100 | 307.4 | −303.0 | 269 | 0.042 | not run |

The slow decline at large K comes from the fixed enumeration radius (R = 5, slack s = 4). The
prime density among candidates is about 1/(1.4K), and the radius was not scaled with K. Lemma P's
full enumeration, or more sample pairs, removes it.

LIN fails everywhere, as the note predicted: short linearized vectors are not squares.

**The acceptance test of infinite-index note §9 is met.** That test asked for success at
precision 2^{-K} with |μ| ≤ 2^{K} in poly(K) time for K ≥ 60. Here |μ| ≤ 2^{K+7.4}, which is
within the 2^{poly} the template admits (Lemma R). With |μ| ≤ 2^{K} read literally, the run needs
ε₀ smaller by 2^{-8}, which changes nothing material. That exact constant was not rerun.

## 4. Does the QZS solution make the template work? (finite check, then a conditional theorem)

`e2e_qzs.py` → `e2e_qzs.out` simulates the template with φ_i = δ_{μ_i} and the QZS μ from §2
(K = 24, |μ| ≈ 2^{28–30}). It uses exact Gram matrices from the twist_check Part-B law, the box
Mb = 16, and windows T, N = ∞.

Prop N predicts a residual character e(βt) on K, with β = Σθ_i(μ_i² − μ_i)c′ and
c′ = c − ab/2. The Fourier law should then be the untwisted law with ⟨y,w⟩/Mb shifted by −β.
This is elementary: group u = r + tw over coset representatives.

| h | strip mass at predicted −β | ideal (θ₂ = −θ₁, μ = 1) at 0 | random μ, best strip | single factor | uniform |
|---|---|---|---|---|---|
| (2,3,5) | 0.649 | 0.659 | 0.305 | 0.279 | 0.188 |
| (1,−2,7) | 0.862 | 0.829 | 0.426 | 0.340 | 0.188 |
| (3,1,−4) | 0.724 | 0.727 | 0.455 | 0.272 | 0.188 |

Strip means ‖⟨y,w⟩/Mb − β‖ ≤ 0.1. "Best strip" maximizes over β, which biases it upward. The
predicted offset is confirmed, including the half-integer c′ case (3,1,−4); a first run of the
script that used c′ mod 1 got that case wrong and was fixed.

This is a toy-size falsification test, not asymptotics. It reuses the Part-B law, so it is not
independent of that law.

**Conditional Theorem C (CONDITIONAL on C1–C4; not proved).**
1. Detect H ∩ Z = 1 with Theorem A, step 1.
2. Then repeat the following O(b + log 1/ε) times:
   * prepare two central-character states with M = 2^{3K+O(log K)};
   * run SDA-ISO (retry on failure);
   * form Ψ(u) = ψ_{θ₁}·δ_{μ₁}(σ(u)) ⊗ ψ_{θ₂}·δ_{μ₂}(σ(u));
   * Fourier-sample y_k over [0,Mb)² and record α_k = Σρ_i((μ_i² − μ_i)/2)/M mod 1.
3. Each sample satisfies ⟨y_k, w⟩/Mb + α_k·(2c′) ≈ 0 mod 1, where X = (w₁, w₂, 2c − ab) is an
   unknown integer vector with |X| < 2^{2b+3}. Recover X by lattice decoding (C2). This gives
   h = (w, (X₃ + w₁w₂)/2).
4. Verify f(h) = f(1) with one classical query.

A non-trivial output is therefore always correct. "H = 1" is wrong with probability ≤ ε. The cost
would be poly(b, log 1/ε) queries and gates.

Conditions:
* (C1) Prop N sufficiency for the template. It is argued in the note and consistent with the toy
  check above, not proved.
* (C2) Decoding X from approximate dual samples with per-sample known offsets. This is standard in
  shape (dimension-3 dual-lattice recovery), but its error and precision analysis was not written.
  The alternative is the note's I1 route: get the direction, restrict to A_v, run Kuperberg on Z².
* (C3) Lemma P (a recalled overlap estimate), or the heuristic enumeration.
* (C4) Lemma R windows: T ≫ |μ|·t_max and N ≫ μ²σ_max with hybrid errors summed. Only sketched.

## 5. Other routes in the brief

* **A(2) Multi-variable.** An n-variable version (SDA in dimension n+1 plus a maximal isotropic
  subspace mod q) works but only gives |μ| ≈ ε^{-n/2}, so n = 2 is best.
  * Without a square root mod q, a Pollard–Schnorr-only chain reaches isotropic dimension
    ⌊(n−1)/2⌋. That gives |μ|² ≈ q^{1+1/n}, and the error ε·q^{1/n} ≈ 2^{n/4} is no longer small.
  * So exactly one square root mod q is the essential ingredient (PROVED for these lattice
    shapes by determinant count; not a general statement).
* **Rational-target relaxation (PROVED, small).** Θ only needs to be within δ of a rational j/d,
  since restricting to π^{-1}(dZ²) then hides H⟨z^d⟩, which meets Z. But the window scales by d².
  The measure gained is a factor of about ln D, so this buys only O(log log D) bits. Not useful.
* **A(3) BCvD two-copy PGM.** Write the two chirp-line states and Fourier-transform both
  π-registers. Implementing the PGM coherently means enumerating the solutions (t₁, t₂) of an
  approximate real binary quadratic equation θ₁q(t₁) + θ₂q(t₂) ≈ λ. That is a QZS-type instance
  with a right-hand side, needed coherently.
  * Whether polynomial precision suffices is **NOT decided**.
  * It is superseded by §2, which needs no entangled measurement.
* **A(4) Avoiding QZS altogether.** Not pursued, since QZS is no longer the bottleneck.

## 6. B: hardness

**There is no barrier for QZS in the needed regime** (§2–3). Hardness is plausible only in
restricted regimes the template does not need:
* binary μ (BZS = random subset sum mod 1; Wagner/BKW, [recalled]);
* |μ| close to the counting threshold 2^{K/2} at n = 2;
* a fixed denominator with |μ| ≪ √M (the setting of the earlier notes).

None of these was shown hard (UNKNOWN). The hardness note's "quadratic SIS with |j| ≤ W^{1/4}" is
easy here whenever W ≥ 2^{4K+O(1)}, which the algorithm may choose. That rests on the same
argument as above, with the linear row turned into the character of Prop N, and it was not run
separately.

## 7. What would close or reopen polynomial time

* **Closes (gives a theorem):** a written proof of C1, C2 and C4, plus Lemma P with the overlap
  estimate checked in a source (e.g. Harman, *Metric Number Theory*, ch. 2–3; not read here). The
  quickest piece is C2 by simulation at a box with Mb ≈ 2^{b+4}, b = 6–10, using the per-sample
  law of §4.
* **Reopens the obstruction:** any of the following.
  * A flaw in Lemma R, for example a hidden requirement that M (or W) equal the coset-line range.
    I found none: M only needs to be at least that range.
  * Failure of the δ_μ Gram law at |μ| ≫ T in the hybrid error accounting.
  * Proof that Prop N's residual character cannot be decoded, i.e. that the per-sample α_k are
    insufficient.

## 8. Adversarial self-check

* **Too easy?** Both earlier notes called QZS the barrier. The gap is that they implicitly fixed
  the modulus to the character denominator. Lemma Q is three lines and every output was checked
  with exact rationals. Sanity checks:
  * n = 1 fails, because c₁μ² ≡ 0 forces q | μ², so |μ| ≥ √q in the squarefree case and the error
    is about εq. This is consistent with Heilbronn's problem being hard.
  * n = 2 needs exactly the one square root. No contradiction found.
* **Is |μ| ≈ 2^{K+7} really allowed?** It is allowed only if T, N, M can grow independently with
  poly bits (Lemma R). The note's own §3 parameters (N, T, N₀ chosen by the algorithm) support
  this. I did not re-derive the state-preparation step 3 of the note; I took its truncation law as
  given (twist_check Part B).
* **e2e check limits.** It is toy size (Mb = 16), with windows = ∞ and the Gram law reused rather
  than independent. It also does not test decoding.
* **Lemma P** uses a recalled lemma, so it is labelled CONDITIONAL. The table's enumeration is
  heuristic, and its success rate decays at large K for a known, fixable reason.
* **Not claimed:** a speedup, novelty, or a solution of the survey's problem 5. Theorem C is
  CONDITIONAL, and an independent referee is required before any STATE row moves.

## 9. Next command

Referee §§1–4 independently. Then write `decode_sim.py` in this folder: it samples from the
§4 law at b = 6–10 with Mb = 2^{b+4}, decodes X = (w, 2c′) by LLL from O(b) samples, and verifies
f(h) = f(1).

* **Artifact:** `decode_sim.out` with a success-against-b table.
* **Acceptance test:** at least 90% recovery of h at b = 10 from O(b) samples. Failure would
  isolate C2 as the remaining gap. Success is only evidence (TRAPS 7).
