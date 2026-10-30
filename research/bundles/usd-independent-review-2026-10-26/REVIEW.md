# Independent Adversarial Review: Exact USD Transfer

Date: 2026-10-26. Scope: the retained-label transfer lemma, full-support
signed-pair/Schur decoder, implementation evidence, precision, and prior art.
No review of the AG parameter/tower discussion in Section 5 was performed.

## Verdict

**The ideal theorem is correct under the stated exact-unambiguity hypothesis.**
The squared fidelity of the full postselected state with the target including
blank decoder workspace is exactly `p_bar/lambda_s`. Unequal `p_c` and arbitrary
additive syndrome characters do not invalidate it. The ideal signed pair map
followed by unique-solution-or-failure relinearization really is unambiguous on
the quantum ensemble, not only on sampled classical transcripts.

Consequently, the bound `(1-E)/(1+A_tail) >= (1-E)/(1+E)` is a valid
worst-syndrome bound for an output after successful retained-label acceptance
when `E<1`. This is a sharper analysis of the existing circuit under a stronger
decoder hypothesis, not an implementation, a uniform sampler, or a quantum
advantage result. I found no counterexample satisfying all the hypotheses.

There are two important qualifications to make explicit before promotion:
workspace cleanup is not a universal all-zero-workspace claim, and the cost of
obtaining a verified witness is not merely the cost of an accepted decode.
Novelty is unresolved and the underlying USD ingredients are established prior art.
The latest listed primary version, **2610.00502v2**, was also checked; the
relevant reduction and quantum-decoder sections are unchanged from v1.

## Findings

### F1: Clarify Workspace And Fidelity Semantics

Location: [USD_REDUCTION.md:63](/Users/jaspersands/Developer/qsearch-research-work/unambiguous-reduction-2026-10-26/USD_REDUCTION.md:63),
especially the wording at [line 134](/Users/jaspersands/Developer/qsearch-research-work/unambiguous-reduction-2026-10-26/USD_REDUCTION.md:134).
Severity: P2 wording/implementation-contract issue, not a counterexample to (3).

Only the *external retained label* must be erased before applying `U^dagger`.
Pair outcomes, decoder output, intermediate arithmetic, and any coherent coins
belonging to `U` must remain available to its inverse. They must not be measured,
discarded, or reset prematurely. After projection onto success, `U^dagger` need
not return every work register to zero. The equations correctly include the
blank workspace in the *target*, but the surrounding cleanup sentence is too broad.

An explicit feasible two-state USD has

```text
G = [[1,1/2],[1/2,1]],   (p_0,p_1)=(1/4,1/2),   p_bar=3/8.
characters (+,+), (+,-): lambda = 3/2, 1/2;
joint squared fidelities = 1/4, 3/4;
probabilities of NONBLANK workspace after the inverse = 2/3, 2/9.
```

For an explicit realization, use columns
`Phi=[[(sqrt(3)/2),(sqrt(3)/2)],[1/2,-1/2]]` in the Fourier eigenbasis,
put `D=diag(1/4,1/2)` and `K=sqrt(D)*Phi^(-1)`, and embed inputs as
`[phi_c;0]`. The unitary dilation

```text
U = [[K, sqrt(I-K*K^dagger)],
     [sqrt(I-K^dagger*K), -K^dagger]]
```

has the first two output basis states as success labels. `G-D` is positive
definite, so the square roots are well defined. After acceptance and inversion,
the squared norm in blank workspace is
`z^dagger D G^(-1) D z/(2*p_bar)`, giving `1/3,7/9` for the two characters.
The `q=5` pair fixture
also produces nonblank ancilla amplitude for nonzero syndromes, depending on
the chosen unitary extension.

The lower bound on valid data measurement remains correct: the projector onto
valid data, tensored with identity on work, contains the joint target ray.
After tracing out work, fidelity with the data target is **at least**, not
necessarily equal to, `p_bar/lambda_s`. Use "squared joint-state fidelity"
explicitly; root fidelity is its square root. Do not normalize again after
silently projecting onto blank workspace.

### F2: Separate Acceptance Cost From Verified-Witness Cost

Location: [USD_REDUCTION.md:110](/Users/jaspersands/Developer/qsearch-research-work/unambiguous-reduction-2026-10-26/USD_REDUCTION.md:110).
Severity: P2 resource-accounting qualification.

The quoted `1/p0` restart cost obtains one accepted decoder branch. It does not
by itself obtain a valid relation output with constant probability. If
`L >= lambda_s` is known and `p_bar >= p0`, that accepted output's validity
probability is only lower-bounded by `p0/L`. Straight repetition plus the final verifier
therefore has a sufficient expected raw-trial bound `L/p0^2`, and a cap
`ceil((L/p0^2)*ln(1/eta))` suffices for ideal failure at most `eta` when treating
each raw trial as either a verified witness or failure. This is an upper bound
from this analysis, not a lower bound or an optimality claim.

In the full-support specialization one may take `L=1+A_tail <= 1+E<2`.
Thus an inverse-polynomial known margin `p0<=1-E` suffices for polynomial
repetition; `E<1` alone does not give a polynomial-time guarantee. The source
already asks for this margin later, but it belongs in the main resource statement.
The published local pair-unitary construction costs polynomial in `q`, not automatically in
the binary field-description length `log(q)`.

### F3: Controls Are Not A Compiled General Decoder

Location: [usd_reduction.py:28](/Users/jaspersands/Developer/qsearch-research-work/unambiguous-reduction-2026-10-26/usd_reduction.py:28),
[line 50](/Users/jaspersands/Developer/qsearch-research-work/unambiguous-reduction-2026-10-26/usd_reduction.py:50),
and [test_usd_reduction.py:8](/Users/jaspersands/Developer/qsearch-research-work/unambiguous-reduction-2026-10-26/test_usd_reduction.py:8).
Assurance gap, not a claim that the supplied controls are incorrect.

The source implements fixed `F_3` repetition-code statevector checks and a
scalar bound helper. It does not implement a uniform reversible Gaussian
eliminator, general-field pair synthesis, retained-label register circuit,
or gate-level compilation/error budget. Its repetition fixtures have equal
`p_c`, no extension-field trace characters, and no nontrivial local ancilla.
The integer accepted-Gram check is useful, but Gram orthogonality alone does
not certify that a decoder assigns the *correct* output label; the
transcript-to-unique-label argument is also needed. The independent controls
below explicitly inspect wrong-label amplitudes.

The general algorithm is justified by the mathematical construction and
standard reversible implementation, not by these test files. No compiled
general implementation or practical gate-count claim was verified.

## Independent Proof Of The Transfer Identity

All states in this section include the initially blank work registers. Let
`Pi=sum_c Pi_c` be the projector onto all nonfailure decoder labels and define

```text
P = U^dagger Pi U.
```

This is an orthogonal projector on the *full* Hilbert space. Exact unambiguity
implies `Pi U|phi_c> = |eta_c>`. Orthogonality of the output sectors gives

```text
<phi_d|P|phi_c> = delta_dc p_c.
```

For any unit-modulus coefficients `z_c`, put

```text
|a> = (1/sqrt(N)) sum_c z_c |phi_c>,     lambda=||a||^2.
```

Then `||P a||^2=<a|P|a>=p_bar`. In the retained-label circuit the acceptance
probability is `p_bar`, since the retained labels are still orthogonal when
the equality bit is tested. Erasing the retained register with the decoded
label and applying `U^dagger` gives exactly `|b>=P|a>/sqrt(p_bar)`. Therefore

```text
<a/sqrt(lambda)|b> = p_bar/sqrt(lambda*p_bar),
|<a/sqrt(lambda)|b>|^2 = p_bar/lambda.
```

This also proves normalization, handles `p_c=0` for individual labels, and
does not require equal `p_c`, a covariant decoder, or a Gram inverse. It actually
works for any equal-modulus phase vector, not just a group character. The
Fourier character is needed to make the target a specified syndrome fiber.

Equivalently, the failure vectors have Gram matrix `G-diag(p_c)`, which is
positive semidefinite. Every normalized character vector has entries of
modulus `1/sqrt(N)`, so positivity gives `lambda_s-p_bar>=0`. A zero eigenvalue
at any character forces `p_bar=0`. For this transitive ensemble one cannot
evade the empty-fiber obstruction by decoding only some labels successfully.

### Arbitrary Syndromes And Extension Fields

Take `B` to have `k` independent rows; otherwise first reduce to an independent
row basis and translate the syndrome consistently. An inconsistent syndrome
for a redundant original matrix is not represented by a character of `V`.
For `q=p^r`, write `c=uB` and use the convention

```text
F|x> = q^(-m/2) sum_y exp(2*pi*i*Tr(x.y)/p)|y>,
chi_s(uB) = exp(-2*pi*i*Tr(u.s)/p).
```

Character orthogonality gives the exact identity

```text
F|a_s> = sqrt(N) sum_{y:By=s} A_y |y>,
lambda_s = N sum_{y:By=s} |A_y|^2.
```

Here `|A>=sum_y A_y|y>` may have nonuniform or complex amplitudes. For a uniform
set source this becomes the claimed normalized fiber mass. Over extension
fields, using an ordinary `q`-th-root phase on integer encodings instead of
the field-trace pairing is generally wrong. No such error occurs in the
source's `F_3` fixtures. All target norms and characters here are for the
original relation, with no change to its promises or verifier.

## Quantum Unambiguity Of The Signed Pair Decoder

Fix any total ordering of the field labels. In the unordered-pair basis, the
zero-exclusion local map has the following action on the input ensemble:

```text
|phi_c> -> (1/sqrt(q-1)) sum_{b!=c} epsilon(c,b)|{c,b}>,
epsilon(c,b)=+1 if c<b and -1 otherwise.
```

Its diagonal Gram entries are one and off-diagonal entries are
`-1/(q-1)`, exactly those of `X^c F^dagger|F_q minus {0}>`. Equality of Gram
matrices supplies an isometry on the input span, including when that span is
singular, and a unitary extension with ancillas. Dropping signs gives a
different Gram matrix and is not the same measurement implemented coherently.

In the tensor product, a transcript `t=({a_i,b_i})_i` has nonzero amplitude on
the state labeled `d` only if `d_i in {a_i,b_i}` for every coordinate. Define
the affine solution set

```text
L_t = {(v,w) in V x W : w-(a+b)*v+a*b=0},
W = span{v*v' : v,v' in V}.
```

Whenever the transcript has nonzero amplitude on `d`, `(d,d*d)` belongs to
`L_t`. If `L_t` has a unique solution, its `v` component must be `d`; otherwise
the decoder returns failure. Also, `w` is determined by `v`, so testing
uniqueness of the pair or of `v` is equivalent.

Implement that deterministic function reversibly while retaining `t` and
all its computation work. For `c!=d`, every basis transcript that is labeled
`c` has zero amplitude in the input ensemble member `d`. Consequently
`Pi_c U|phi_d>=0` as a vector identity. This is stronger than cancellation
between transcripts or an empirical statement about measured outcomes.
There is no assumption that the entire ensemble is classical.

Unsupported transcripts can be assigned failure or any unitary-compatible
decoder output without affecting this ideal identity. Approximate pair maps
can put amplitude there; those errors must be bounded relative to the ideal
coherent circuit, not declared unambiguous.

For completeness, a second relaxation solution yields a nonzero difference
`h in V` and `z in W` with `z=(a+b)*h`. Thus `z` vanishes on `Z(h)`. For fixed
`h,z`, each nonzero coordinate of `h` imposes one value on an independent
uniform partner sum having `q-1` possibilities. Its probability is at most
`(q-1)^(-wt(h))`. Summing over the `q^dim(W[Z(h)])` possible `z` and nonzero
`h` gives `E`, uniformly for each true label, and hence `p_bar>=1-E`.

The full-support Gram is a translation convolution with entries
`(-1/(q-1))^wt(c-d)`. Bounding the nonidentity terms of each character sum
by absolute values gives `lambda_s<=1+A_tail`. Since each shortening factor
in `E` is at least one, `A_tail<=E`. Combining these independently derived
facts proves the specialization. No enumeration of `V` is needed in the
actual circuit; a numerical value supplied to `transfer_bound` is not a
certificate that a particular code satisfies the required bound.

## Compilation And Abort Accounting

The asymptotic precision prescription in the source is sound when its error
is **total coherent trace-distance/channel error**, not average decoding
error or per-basis-state error. One explicit allocation is as follows.
Choose `0<epsilon<1`, known `p0<=p_bar`, and let the compiled state before the
equality test differ from the ideal joint state by trace distance at most
`alpha=epsilon*p0/16`. This must cover label/source preparation, character
phases, shifts, decoder synthesis, and equality-test operations.

The actual acceptance probability is at least `p0-alpha >=15*p0/16`, and
the conditioned-state distance is at most

```text
alpha/(p_bar-alpha) <= epsilon/15.
```

Allocate another `epsilon/16` total error to retained-label erasure,
`U^dagger`, the final Fourier transform, and remaining operations. The output
probability changes by less than `epsilon/4`. A cap
`ceil((2/p0)*ln(4/epsilon))` on raw trials has abort probability at most
`epsilon/4`. Taking aborted output as failure gives unconditional success
at least `p_bar/lambda_s-epsilon/2`; in particular the stated ideal bound
minus `O(epsilon)` is justified. This capped procedure produces one candidate,
not necessarily one verified witness. For witness amplification use F2 and
choose approximation error smaller than its guaranteed success margin.

If `J` approximate primitives are used before acceptance, operator-norm
error at most `alpha/O(J)` per primitive suffices by telescoping. Charge
`log J + log(1/epsilon) + log(1/p0)` precision dependence, polynomial workspace,
reversible field arithmetic, and the inverse decoder. There is no `N`-factor
error amplification once a uniform coherent bound has been established.
No robustness to arbitrary physical noise or merely small misclassification
probability follows from this argument.

## Counterexamples And Failed Attacks

1. **Remove exact unambiguity:** reproduced the source's real orthogonal
   eight-state decoder with `p_bar=5/8`, `lambda=1`, fidelity `1/10`.
   Strengthened it to `U=diag(I_r,I_r-2J_r/r)` on `2r` orthonormal inputs.
   For the uniform target,
   `p_bar=1-2/r+2/r^2` while fidelity is `1/(r^2*p_bar)`.
   At `r=100`, these are `4901/5000` and `1/9802`; as `r` grows they tend to
   one and zero respectively. The average correct-answer rate can be almost
   perfect and the proposed USD conclusion still fail. This family is not a
   small operator-norm compilation perturbation of the ideal decoder.
2. **Unequal successes:** no counterexample. The exact two-state example and
   explicit nine-state and four-state unitary dilations obey the identity for
   every character, despite deliberately unequal `p_c`.
3. **Require blank final work:** false, with exact dirty-work probabilities
   `2/3` and `2/9` above. This refutes an overstrong cleanup interpretation,
   not the joint-state theorem.
4. **Measure the label:** two orthogonal inputs and a perfect decoder give
   fidelity one if coherent, but `1/2` after reading and forgetting the label
   for the uniform target. Correct classical labels alone are insufficient.
5. **Discard pair signs:** for `q=3`, the local off-diagonal Gram becomes
   `+1/2` instead of `-1/2`; no isometry implements the claimed replacement.
6. **Exploit an empty fiber:** for the length-one ternary orbit the all-ones
   coefficient vector is an exact Gram null vector. PSD of the failure Gram
   forces every `p_c=0`, so there is no accepted branch to normalize.

## Primary Literature And Novelty

The following comparisons were checked from primary texts, not search-result
summaries. They are a scoped prior-art review, not an exhaustive priority search.

### Latest-Version Check

On 2026-10-26, [arXiv's version history](https://arxiv.org/abs/2610.00502)
listed **v2, submitted 2026-10-02 at 15:23:05 UTC**, as current. I downloaded
its version-pinned HTML and compared mathematical content as well as prose.
After replacing MathML with its LaTeX representation and normalizing whitespace,
Section 3.2, Sections 5.1-5.3, and the entire Section 5 are each identical to v1.

In particular, [v2 Theorem 5.4](https://arxiv.org/html/2610.00502v2#S5.SS3)
still states failure at most `2|V|E+epsilon`; Theorem 3.30 retains its generic
code-size loss. V2 does **not** incorporate the USD overlap sharpening in those
results. The theorem and decoder verdict above is unchanged. Absence there
does not establish originality elsewhere. No AG tower claims were reviewed.

The comparison is reproducible with `python -B version_check.py`; pinned HTML
and [version-comparison.json](/Users/jaspersands/Developer/qsearch-research-work/usd-independent-review-2026-10-26/version-comparison.json)
record source and normalized-section hashes.

### Earlier USD And Related Work

- [Ragavan-Shutty, 2610.00502v1, Section 3.2 and Sections 5.1-5.3](https://arxiv.org/html/2610.00502v1#S3.SS2):
  Theorem 3.30 describes the retained-label/equality/inverse circuit and uses
  a generic code-size-loss bound. Lemma 5.2 supplies the signed pair isometry;
  Lemma 5.3 and Theorem 5.4 use unique-solution-or-failure relinearization.
  Thus the ideal decoder here has the extra property required by this review.
  I did not find the exact USD-specialized `p_bar/lambda_s` identity stated
  there. This observation is not a claim of originality or a correction to
  the published, valid generic theorem.
- [Chailloux-Tillich, 2310.20651v1, Section 4.1](https://arxiv.org/html/2310.20651v1#S4.SS1)
  gives symmetric/translation-ensemble USD bounds, including the averaging
  argument and finite-abelian generalization. Its
  [Section 6.2](https://arxiv.org/html/2310.20651v1#S6.SS2) already uses coherent
  USD and label erasure in Regev reductions, with a particular erasure/shortening
  algorithm. Section 6.3 warns that a successful quantum decoder can behave
  badly in a reduction. Those are direct antecedents, not the identical general
  retained-label formula proved above.
- [Chefles-Barnett, quant-ph/9807023v1, Sections II-III](https://arxiv.org/html/quant-ph/9807023v1):
  exact discrimination with a failure outcome, reciprocal states, and optimal
  success for equally likely symmetric pure states are classical USD results.
  The Gram-positivity obstruction and spectral bottleneck here are not new
  discrimination phenomena. An information-theoretic reciprocal-state POVM
  does not establish an efficient implementation over exponentially many labels.
- [Dalai-Girardi-Lami, 2601.09786v1, Lemma 3](https://arxiv.org/html/2601.09786v1#S2.SS1):
  the diagonally dominant Gram factorization into rows supported on at most
  two labels is prior art for the pair measurement, already cited by
  Ragavan-Shutty. The signed pair mechanism should not be claimed as new.
- [Buzet-Chailloux, 2510.07298v2, Sections 1.1 and 1.4](https://arxiv.org/html/2510.07298v2#S1.SS1):
  fine-grained unambiguous measurements are prior art. Their distinction
  between recovering parities without using a code and exploiting a known
  code's structure matters: their code-independent restrictions are not a
  blanket impossibility theorem for this code-dependent Schur decoder.
- [Horinaga-Yamakawa, 2607.14650v2, Theorem 5.1](https://arxiv.org/pdf/2607.14650v2):
  checked the current October 22 version, printed pages 28-30 and the overview.
  It uses a particular list decoder and target-norm controls for worst-case
  target overlap, not this exact error-free-or-failure hypothesis. It neither
  directly proves this lemma nor contradicts it. Root-fidelity conventions
  there differ from the squared fidelity used here.

**Novelty verdict:** valid short deduction using established USD geometry and
an existing circuit. Whether this precise specialization and resulting
parameter improvement have appeared elsewhere remains unresolved. No new
quantum-algorithm primitive or advantage is established by this bundle.

## Independent Controls And Provenance

Reproduction command, run from this review directory:

```sh
/opt/anaconda3/bin/python -B independent_controls.py
```

The runner disables bytecode and pytest plugin/cache writes, sets pytest's
root and temporary directory here, and records SHA-256 hashes of all seven
source-bundle files before and after. It does not execute the original
`verify_usd.py --write`, modify its receipt, or inspect the unrelated AG bundle.

| Control | Result |
| --- | --- |
| Original scoped test suite | 19 passed; output in `source-pytest.txt` |
| Exact rational unequal-USD/ancilla calculation | Fidelities `1/4,3/4`; dirty-work probabilities `2/3,2/9` |
| Nine-state `F_3^2` orbit, nonuniform complex source, unequal success probabilities | All nine characters agree with the formula; explicit unitary dilation checked |
| Four-state `F_4` trace-character orbit | All four syndromes agree; uses `F_2[x]/(x^2+x+1)`, not integer-mod-four phases |
| Non-repetition ternary code, generator rows `111111` and `001122` | All 729 pair transcripts inspected; Schur dimension 3; `p_bar=1/2`; zero wrong-label integer amplitudes; all nine syndromes checked |
| Quinary length-three repetition code | All 1000 pair transcripts inspected; `p_bar=15/16`, `E=5/16`; zero wrong-label integer amplitudes; all five syndromes checked |
| Wrong-answer, sign-loss, measured-label, singular-orbit controls | Exact rational/symbolic identities checked |
| Source immutability | All seven SHA-256 hashes unchanged across the run |

The ternary non-repetition fixture has `E=135/32`, so its union bound is
vacuous. It tests exact unambiguity, not the sufficiency of `E<1`. The quinary
fixture has target fidelities one at syndrome zero and `12/13` otherwise.
All floating checks use absolute tolerance `2e-11`; tiny negative residual
probabilities around `1e-15` in raw output are roundoff, not probabilities.
The proof above, not finite green tests, justifies the general verdict.

Artifacts:

- [independent_controls.py](/Users/jaspersands/Developer/qsearch-research-work/usd-independent-review-2026-10-26/independent_controls.py)
- [controls.json](/Users/jaspersands/Developer/qsearch-research-work/usd-independent-review-2026-10-26/controls.json)
- [source-pytest.txt](/Users/jaspersands/Developer/qsearch-research-work/usd-independent-review-2026-10-26/source-pytest.txt)
- [version_check.py](/Users/jaspersands/Developer/qsearch-research-work/usd-independent-review-2026-10-26/version_check.py)
- [version-comparison.json](/Users/jaspersands/Developer/qsearch-research-work/usd-independent-review-2026-10-26/version-comparison.json)
- Downloaded primary HTML/PDF copies and the two inspected theorem-page PNGs
  are in this directory for reproducibility.

All writes were confined to this new review directory. No earlier bundle,
Git state, registry, or UI was edited. No independent subagent tool was
available; this is one independent review, not a multi-reviewer consensus.

## Unresolved Claims

- A scalable compiled implementation and verified gate/workspace costs.
- Any polynomial-in-`log(q)` replacement for the current polynomial-in-`q`
  local-unitary construction.
- Formal proof-assistant verification and exhaustive literature priority.
- A useful asymptotic input family, matched classical baselines, and actual
  quantum advantage. The unrelated AG work was deliberately not audited.
- A uniform conditional-output distribution. The overlap bound does not
  provide one, and no such claim should be added.
