# Full-Root Paired-Noise Lattice Decoder

LOCAL DERIVATION / REVIEW PENDING. A classical attack on quantum-produced
records, NOT classical simulation of the unknown source, a quantum advantage
or a general hardness result. This is different from the existing lattice
search for native-word collisions: the target here is the shared secret.

## Source And Attack

Keep the exact covariant receiver records at q=3^r:

    y1=a.s+e1, y2=c.s+e2 modq,
    nu(e1,e2)=|1+chi_q(e1)+chi_q(e2)|^2/(3*q^2).

The two errors from one original qutrit are correlated. No Gaussian, small
secret, chosen label, preparation inverse or narrow-error promise is granted.
Fresh original records are IID only under the physical source premise;
unique IDs do not prove it. The calibration samples the existing native law
offline, with its hidden secret excluded from the attack interface.

For a public subset of k WHOLE original pairs, stack m=2k frequency rows in
A. When rank(A mod3)=n, select n unit rows B USING LABELS ONLY and compute
B^-1 modq with the existing prime-field/Newton lift. The full code lattice is

    L=A Z^n+q Z^m = {x in Z^m: x modq=A*s for some s}.

An explicit systematic basis uses pivot-coordinate unit vectors extended by
A*B^-1, and q times each nonpivot-coordinate unit vector. Its determinant is
q^(m-n). This proves equality with L, not just containment. Rank failure is
retained as UNKNOWN; no subset of the secret is silently accepted.

Retain the correlation-aware integer embedding

    E(e1,e2)=(e1,e2,e1-e2).

Its metric is e1^2+e2^2+(e1-e2)^2, block determinant3. The rectangular
embedded basis has Gram determinant3^k*q^(2*(m-n)). Around zero this is the
quadratic Taylor surrogate for the native cosine score. It is NOT globally
the likelihood metric. The complete q9 torus countercontrol supplies a
closer point with a strictly WORSE native score, including minimization over
integer wraps. Thus even an exact Euclidean CVP oracle would not automatically
be an exact maximum-likelihood decoder. No Gaussian decoding-radius theorem
is imported onto this source.

IMPORTANT FOLLOW-UP: non-equivalence to likelihood does NOT disprove
statistical recovery with a copy surplus. The separate
[native CVP reduction](TERNARY_NATIVE_CVP_REDUCTION.md) derives an actual
uniform population margin for ORDINARY Euclidean distance and a sufficient
norm9/8 approximation factor, with its large original-copy budget charged.
That is not this paired metric, nor a proof that Babai attains the factor.

## Concrete Secret-Blind Algorithm

1. Before looking at outcomes, fix subsets of whole pairs from a public seed
   at sizes ceil(n/2)+1, n+1, and 2n+1, whenever complete caps permit them.
2. Compile each complete code lattice. Apply exact-gram LLL to its paired
   embedding with a fixed public basis-permutation menu.
3. Run exact rational Babai and the existing single-rounding-deviation list:
   1+2m paths, not all combinations of rounding errors.
4. Recover a candidate through B^-1 and verify EVERY full-modulus code
   equation. Check the unimodular LLL transform, embedding and determinant.
5. Deduplicate candidates and select by the original paired cosine score on
   ALL training records, not by the nearest-point surrogate or true secret.
   Use its equivalent sine-squared loss to avoid subtractive cancellation
   near perfect fit, and root-bit-length-dependent precision above256 bits.
6. Freeze ONE candidate, then acquire an independent held-out batch and run
   the existing threshold1/2 verifier with its one-candidate error ledger.

Classical records can be reused across subsets. This does not consume more
unknown states or manufacture independent noises; the original qutrit count
is charged once. No trial search over q values or q^n secrets is performed.
LLL, exact rational profiles and the public list work on integer bit lengths;
at polynomial subset/basis budgets this proposal generator has polynomial
arithmetic cost in n, r and record count. Its RECOVERY probability has no
such theorem. Finite caps and no-proposal branches are retained, and LLL has
no internal wall-clock deadline. Score evaluation is floating, with no claim
of certified precision or a hardware aggregate error bound.

## Precommitted Experiments And Falsifiers

The report fixes two seeds at each (n,r) in
(2,2),(2,8),(4,2),(4,8),(8,2),(8,8). Each has96 training originals and512
fresh originals, regardless of attack success. All public records, selected
subsets, lattice bases, transforms, paths, candidate scores and failures are
retained. These twelve controls are not population estimates, cryptographic
parameters or an asymptotic scaling theorem. Comparing roots at fixed n and
dimensions at fixed roots prevents a small-secret-space success from being
mistaken for scalable recovery. No positive seed was selected after testing.

Falsify correctness if the lattice has the wrong index, a transform is not
unimodular, a purported point violates a modular equation, a pair is split
and called independent, or hidden calibration truth enters proposal/selection.
Falsify an empirical recovery claim if the chosen candidate fails fresh
verification. Insufficient held-out confidence must remain visible.
Failure of this bounded LLL/Babai menu does NOT rule out BKZ, enumeration,
hybrid methods, nonlinear raw-sample inference or other quantum receivers.

## Primary Context And Next Decisions

Primal lattice attacks and Babai are existing techniques, not new algorithm
claims; compare the [hybrid-attack literature](https://eprint.iacr.org/2019/1019).
The [EDCP/LWE reduction](https://arxiv.org/abs/1710.08223) has its own source
and parameter conditions. Its Gaussian transfer does not follow from this
three-point envelope. This subsystem improves the baseline against which a
new receiver must compete; it does not establish an LWE attack.

If this inexpensive shortlist succeeds across growing dimensions on native
sources, strengthen it before investing in collective quantum receivers.
If it fails, examine whether true-secret torus distance, lack of lattice
coverage, or the surrogate/likelihood mismatch is responsible; do not infer
hardness. BKZ/embedding/list-decoding are meaningful next baselines only with
complete work and native-score accounting. External review remains required.

```
python theorems/ternary_measured_lattice_decoder.py --write
node research/certificates/ternary_measured_lattice_decoder_crosscheck.js
python -m pytest -q tests/test_ternary_measured_lattice_decoder.py
```

GPT owns scientific arithmetic, derivation and targeted tests.
Gemini/Antigravity owns CLI/registry integration, full production validation
and Git. Preserve the distinction between record postprocessing and source
dequantization. No speedup candidate is accepted by this subsystem.
