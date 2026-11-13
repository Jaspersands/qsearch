# Audit: zero-quotient composition step in DYADIC_NONFULL_SPINOR_TRANSPORT.md

**Scope.** I take the local nonfull-H two-move theorem as hypothesis **(H2M)**: legality of the word 12(x),23(z), plus polynomial coordinate constructibility. I audit only the new composition and the interfaces it changes. The evidence is three supplied notes and one review. I have no source access, and nothing was executed.

## 0. Verdict

- **Zero-quotient sufficiency is proved.** It is a direct consequence of the idelic proper-spinor-genus criterion already used in the split composition. No step of the S-unit/ray test, its completeness proof, or the class/properness reduction uses a transporter at a place with H_P = F*/F*².
- **No hidden full-H transporter was found** in the global relation, the orientation handling, or the choice of offsets.
- **General DECISION does not yet follow from the supplied evidence.** The shortcut moves all dyadic local work onto native BONG, defect, Hilbert-symbol and H computations at arbitrary (e,f). The split composition never paid for these. It used F2-idempotents plus a constant 2^81 seed search valid only over Q2. They are named "already charged" but no reviewed locator is supplied. One of them, exact computation of H, is a **soundness** dependency, not just a cost item: a wrong "full" verdict produces a silent false YES.
- **Status:** a conditional written composition, conditional on H2M plus obligations O1–O7 in §6.
- **No integral witness** is produced or approached.

## 1. Cheapest decisive attack: is a zero quotient enough?

**Setup (from the split review §4).** Fix the global rational map F with FᵀAF = B. For each finite P with L_P ≅ M_P, choose a proper local integral transporter Y_P and set g_P = Y_P F⁻¹ ∈ O⁺(V_P). Kirschmer 5.4.5/5.4.6, as used there, says M is in the proper spinor genus of L iff there is c ∈ K* with:
- c ∈ θ(g_P)·H_P·K_P*² at every finite P, and
- the stated sign conditions at definite real places.

**Proof that a full-H place drops out.**
1. If H_P = F*/F*², the local condition at P is satisfied by every c and every g_P. So it does not constrain c.
2. Existence of some proper g_P is all that is needed. Since rank 3 is odd, L_P ≅ M_P gives a proper transporter by replacing Y with −Y. Its value is never used.
3. The test vector space is V = ⊕_{P∈T} K_P*/(K_P*² H_P) ⊕ F2^{definite}. At such P the summand is 0, so both the offset coordinate and every unit-image coordinate vanish there. Deleting the summand gives the same F2-membership problem.
4. The T-unit descent (c → c/d², using Cl(O_K,T) = 0) touches only valuations at places outside T. All dyadic places lie in T, since T contains every prime above rational primes up to the bound, which includes 2. So the completeness proof is unchanged.
5. Kirschmer 5.4.10 (indefinite rank 3: spinor genus = class) and the −I step (odd rank: class = proper class) never reference local transporters.

**Independence of choice at proper-H places.** For two choices Y, Y′, the map Y′Y⁻¹ lies in O⁺(M_P). Spinor norms are invariant under transport by isometries, so θ(O⁺(M_P)) = θ(O⁺(L_P)) = H_P. Hence the offset is well defined modulo H_P exactly where it is needed.

**Conclusion.** The attack fails. Zero-quotient sufficiency holds, given exactly:
- (a) a correct Boolean verdict on L_P ≅ M_P, and
- (b) a correct verdict that H_P is all of F*/F*², not merely containing the unit classes.

## 2. Search for a secretly required full-H transporter

| Step | Uses Y at a full-H place? | Finding |
|---|---|---|
| Rational invariants and global F | No | Unchanged, via the expanded-norm note. |
| Local genus test at a dyadic P | Previously yes: the Q2 seed was both genus test and transporter | Now replaced by Boolean Beli/O'Meara invariants. This is an **interface change**, not a hidden dependency. |
| H_P computation | No | H_P depends on L_P alone. |
| Orientation/properness | Only where an offset is computed | Full places need no orientation. |
| Precision β = s(W⁻¹)+s(F⁻¹)+s(W) | Only at proper-H places | W is now the BONG basis there (O6). |
| Ray membership and T-unit completeness | No | See §1. |
| Strong approximation and −I | No | — |
| Odd places | No | Unchanged. Odd transporters exist anyway. |

**The three-word falsifier** (full image; gaps 0,3; e = 2) is consistent with this table. The note correctly does not infer a general local transporter algorithm from skipping that place.

**Case coverage of H2M.** As stated, its cases exhaust all isometric pairs with proper H:
- If R1 = R3, then m+n = 0. With m,n ≥ −2e, this excludes m > 2e or n > 2e, so case 3 is disjoint from case 1.
- If R1 < R3, the pair falls under case 1 or case 2.

I do not audit the internal correctness of those cases.

## 3. Interfaces changed by the shortcut (native access, precision, error)

The split composition paid local access through:
- O_K/2O_K ≅ F2ⁿ,
- idempotent lifting e → e²(3−2e), and
- reading rank-one components into Z/2^M.

None of this applies when e > 1 or f > 1. Idempotent lifting still splits O_K⊗Z2 = ∏O_P, but each component is no longer rank one over Z/2^M. The shortcut also needs, at **every** isometric dyadic place (full or not):

1. **A native model of O_P/P^N:**
   - prime(s) above 2 and a uniformizer;
   - e and f;
   - a model of the residue field F_{2^f}; square roots there are Frobenius-inverse, so deterministic;
   - images of the Gram entries, at a precision N proved polynomial.
2. **Good BONGs of L_P and M_P from Gram coordinates:**
   - a norm-generator choice and successive projections;
   - goodness R_i ≤ R_{i+2};
   - common-R check;
   - explicit pole bounds of the BONG basis.
3. **Quadratic defect d(·) and dyadic Hilbert symbols,** polynomial in (e, f, precision):
   - an explicit F2-basis of F*/F*² of size ef+2;
   - the U_t filtration;
   - the pairing matrix.

   The note itself forbids importing Magma's OnePlusPowerOfP squareclass enumeration. It points to "already charged native filtration/Hilbert basis algorithms" without a file or locator in the evidence.
4. **The exact lattice-isometry criterion** (O'Meara 93:28 via Beli's BONG translation) as an exact Boolean, with stated precision. Squareclasses need relative precision 2e+1 above the valuation, and defects up to 2e.
5. **H_P as an F2-subspace:**
   - the G(·) sets;
   - the property-A test R1 < R3;
   - the Theorem 3 test (all classes vs unit classes) when A fails.

**Error budget.** These local routines can be made deterministic, so the global η-split is unchanged. That is only true if items 1–5 are indeed deterministic polynomial, which is unproved here.

## 4. Proper-H branch: what the composition needs from H2M

Treating legality and constructibility as given, the composition still needs a coordinate interface that H2M only gestures at:

1. **Build Y in Gram coordinates.** Y is the linear map sending the moved orthogonal BONG of L_P to the BONG of M_P. This requires:
   - unit square-root rescalings b_i/(moved a_i), including b2/(a2·x·z);
   - the result expressed in the original Gram coordinates.
2. **Pin down the precision.** Give explicit pole bounds for W, W⁻¹ and the BONG bases. These feed:
   - β and the precision N = β+4e+1;
   - the determinant-ratio orientation at precision e+1;
   - the four-chart trace selection.
3. **Pin the cited sources.** The "reviewed quadratic-order unit-norm compiler" and "sub-BONG lemma" need locators. The sub-BONG replacement must provably keep the BONG good for L itself, not merely for an isometric lattice.
4. **Self-check (recommended).** Run the existing finite verifier: test YᵀAY ≡ B mod P^{s_B+2e+3}. Then any H2M or coordinate bug becomes a detected ABORT rather than a wrong offset.

**Asymmetry with H.** The H_P verdict has no such self-check. An undetected error in O5 is the main residual soundness risk.

## 5. Deciding isometry versus outputting a witness

**What the composition outputs.** One bit, with failure ≤ η under the retained GRH backends:
- **Incomplete S-units** can only produce a false NO or an ABORT.
- **Wrong local data** can produce either error:
  - a wrong "full H" gives a false YES;
  - a wrong nonisometry verdict gives a false NO.
- **No certificate** is produced for YES or NO.

**What an integral U ∈ GL3(O_K) would additionally require (none of it supplied):**
- actual transporters at **every** place in T, including full-H dyadic places, which the shortcut deliberately skips;
- a global element realizing the spinor correction;
- constructive strong approximation with bit-size control;
- the integral gluing.

**Effect of the shortcut on witnesses.** It widens the decision/witness gap: the decision becomes cheaper exactly by not constructing what a witness needs. It is not evidence for, or against, polynomial witness construction.

## 6. Exact unresolved obligations

- **O1 – Native dyadic completion.** From the expanded table, deterministically compute all P | 2, uniformizers, e, f, the residue-field model, and maps O_K → O_K/P^N. Prove N ≤ poly(native bits) suffices for all subsequent invariants, using determinant valuations + 2e + constant slack.
- **O2 – Good-BONG compiler.** Polynomial in (e, f, valuations) for ternary dyadic lattices. Output coordinates and pole bounds; check goodness; no residue or squareclass enumeration.
- **O3 – Defect and Hilbert symbols.** Polynomial routines over arbitrary dyadic F with explicit precision. Provide a pinned reviewed locator, or a proof here.
- **O4 – Local isometry Boolean.** A source locator for the exact ternary BONG isometry criterion (O'Meara 93:28 / Beli translation) valid for all dyadic fields. Show it is evaluated correctly on O2's output.
- **O5 – H_P computation (soundness-critical).**
  - Exact F2-subspace computation from Beli's thesis.
  - An exact full/proper verdict, including Lemma 1.4.11 / Section 1.7 / Theorem 3 at the pages cited.
  - A cross-check that H(L_P) = H(M_P) computed independently; a mismatch must cause ABORT.
- **O6 – Proper-H coordinates.** As listed in §4: Y in Gram coordinates, β, precision N, orientation, verifier check.
- **O7 – Clock.** At most n dyadic places, each with poly(e, f, log precision) work. Show the total feeds the existing clock without a fixed-field constant.
- **Outside this audit:** independent verification of H2M itself. The YES/NO correctness at proper-H places depends on it, mitigated to ABORT by the O6 verifier for the legality part only.

## 7. Falsifiers (any one breaks the general claim)

1. A dyadic field family where O2, O3 or O5 provably needs squareclass or residue enumeration that is exponential in ef. This breaks the polynomial claim, not the composition.
2. A source exception to the Section 1.7 dichotomy, or an isometric pair whose H is misclassified as full. Either gives a false YES.
3. An isometric proper-H pair where the H2M word is illegal, or where its coordinates fail the verifier.
4. Any step of the ray-test proof shown to need θ(g_P) at a full place. I found none; §1 argues it cannot.
5. A split-Q2 instance where the new local verdicts disagree with the reviewed 2^81 seed method. A useful finite control, but passing it proves nothing in general.

## 8. Claims boundary

- **The new step is wholly classical.** The global backends are the retained GRH class/unit/norm routines, and they are unchanged.
- **The strongest classical comparator is the same reduction** with classical class/unit/norm arithmetic.
- **Supplied quadratic towers** still reduce classically to integer factoring under the relevant-Hecke ERH. They supply no evidence of further quantum advantage.
- **Not claimed:** novelty, Shor-level advantage, classical hardness, unconditional (non-GRH) backends, universal BONG connectivity, or a local transporter at full-H places.