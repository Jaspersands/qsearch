# Native RLWE: An All-Coset Classical Cover Certificate

Status: LOCAL DERIVATION / REVIEW PENDING. Finite-instance mathematical
certificate, not an asymptotic attack, security estimate, independent proof
verification, or quantum algorithm. The saved kernel has the conditional
native public-label law; the decoder controls do NOT sample the source
prior/noise laws.

## 1. Why This Changes The Research Target

The original endpoint is secret recovery from public records, not sampling
a particular Gaussian or hitting an arbitrary internal witness radius.
A classical method may use a LONGER witness if the original decoder still
works. Requiring every competitor to satisfy the Gaussian sampler's
internal `sigma*sqrt(d)` radius would create an artificial advantage.

One native d=64 kernel now has an exact classical all-coset certificate
covering both saved d^12 parameter lanes. This falsifies the need for a
quantum witness generator on this finite kernel. It does not settle larger
dimensions, earlier d^4/d^6 parameter families, average success, or worst
cases. Treat this family as a classical-baseline control until stronger
tests justify a harder target.

Nearest-plane and small-secret lattice attacks are established techniques;
this note specializes a sufficient certificate to the original ring
records. See [Albrecht's small-secret dual-attack paper](https://www.iacr.org/archive/eurocrypt2017/10210169/10210169.pdf).
The following certificate is a local derivation, not a novelty claim.

## 2. Public Kernel And Original Coordinates

Let `R=Z[X]/(X^d+1)` with power-of-two d. Write C_a for negacyclic
multiplication and use original public data

```
F = [C_a1^T, C_a2^T],  b = F^T s + e (mod q),
||s||_infinity <= R_s,  ||e||_2 <= E.
```

Condition on a1 being a unit modulo q. Normalize only the PUBLIC kernel:

```
F' = C_a1^-T F = [I,M],  M=C_(a2/a1)^T,
K = ker_mod_q(F') = ker_mod_q(F),  det(K)=q^d,
B = [qI, -M; 0, I]  (column basis).
```

The conditional uniform ratio law is not the planted small-f,g key law of
Falcon. Keep the original s,e,b. Do not replace them by a conveniently
transformed prior or noise model.

## 3. The Certificate Does Not Require Saturation

Suppose B' is an integer column basis of ANY full-rank sublattice of K.
Full rank is essential; index one is not. Let

```
Gamma(B') = sum_i ||b_i^*||_2^2
```

for its exact Gram-Schmidt vectors. Given ANY syndrome u, compute a public
integer section c0 with Fc0=u modulo q. Babai nearest plane subtracts a
lambda in the sublattice and returns c=c0-lambda, so

```
Fc=u (mod q),  4||c||_2^2 <= Gamma(B').
```

Proof: the final residual is a sum of orthogonal GS vectors with
coefficients in [-1/2,1/2]. This bounds its norm for EVERY target, not only
a Gaussian target. A sublattice may have a worse profile, but preserves the
syndrome. Its missing cosets matter for full-lattice distribution claims,
not this finite point-finding endpoint.

Take the predetermined original syndrome `u=t*e0`, where
`t=floor(q/(2R_s+1))`. Signed negacyclic rotations of c yield all d
equations. The corresponding convolution matrix W satisfies
`W F^T=t I (mod q)`. Each error coordinate has magnitude at most E||c||.
The secret residues have torus separation at least t. Thus a sufficient
global decoder certificate is

```
E^2 Gamma(B') < t^2.
```

Replace Gamma by an exact upper bound Q for an executable integer test.
The strict inequality matters. This is a correctness theorem conditional
on the original box/norm promises, not a guarantee that those promises
hold for every source sample.

### Necessary Geometric Headroom, Not A Hardness Bound

For a full-rank sublattice of index I, the 2d GS lengths have product
`det(B')=q^d I`. Arithmetic-geometric mean gives

```
Gamma(B') >= 2d q I^(1/d).
```

For a completion with determinant `(q delta)^d`, this is `2d q delta`.
Therefore its all-coset norm certificate is IMPOSSIBLE unless

```
2d q E^2 delta < t^2.
delta <= floor((t^2-1)/(2d q E^2))  (integer parameters, E>0).
```

The exact necessary delta budgets at the d^12 rows are:

| d | Spherical | Hidden elliptical |
| --- | ---: | ---: |
| 64 | 14469030 | 11446896 |
| 256 | 67991368616 | 69039767670 |
| 1024 | 414332082786856 | 696130223666429 |

These are NOT sufficient budgets. A bad profile can still fail by an
arbitrary factor. They also show why a large raw sublattice index alone
does not kill a point finder: the bound uses I^(1/d), not I.

With the spherical reference box/norm scalings, necessary all-coset
headroom requires q to exceed order d^5 log^5(d), up to constants.
Thus a q-near-d^4 version with those same promises cannot pass THIS
global Babai/box-norm certificate asymptotically, even with the best basis.
This does NOT exclude a particular short chosen coset, a moment/statistical
decoder, a sharper source-tail contract, primal recovery or a quantum
algorithm. Conversely q-near-d^12 gives huge geometric slack and may be
classically easy. Do not infer source hardness from either inequality.

## 4. Saved Native d64 Result

`certificates/native_rlwe_babai_profile_d64.json` stores the uniform ratio,
centered integer lift, 128-by-128 reduced row basis and unimodular transform.
Seed 290952; q=4722366484553272393819. Exact checks establish

```
R_reduced = U B^T,  det(U)=+/-1,  F' R_reduced^T=0 (mod q).
Q = 11618782031352898851890207.
```

Bareiss leading Gram determinants give exact squared GS lengths as
successive determinant ratios. Ceil each ratio and sum to obtain Q.
The final Gram determinant is q^(2d). No floating GS certificate is used.

| Lane | R_s | E | t | sqrt(t^2/(E^2 Q)), approximate |
| --- | ---: | ---: | ---: | ---: |
| Spherical | 183 | 4351 | 12867483609136981999 | 867.61 |
| Hidden elliptical | 197 | 4545 | 11955358188742461756 | 771.70 |

Both exact integer inequalities pass. These ratios are radius slack,
NOT speedup factors, success probabilities, or asymptotic exponents.
The optional FLINT LLL construction took about 59.71 seconds; that is LLL
time only, not total verification/decoding cost. The same seeded SymPy
calculation was stopped after the alternative delivered the verified
certificate; no completed SymPy result or timing comparison is claimed.

An independent original-coordinate control draws a unit a1, sets
a2=a1*m, and retains F,b. Witness construction uses only the public
kernel and the original predetermined syndrome. It checks exact
`Fc=t e0` and `WF^T=tI`, then decodes 128 coordinates across two lanes.
Its secrets/noise are deliberately within-contract controls, not source
distribution samples. Two out-of-contract records confidently decode the
wrong secret; fresh held-out original records reject those wrong secrets.
Retain these controls: a decoder certificate is not promise verification.

Equal-mod-q matrices are not interchangeable in an exact basis-transform
identity. The checker explicitly rejects the noncentered lift paired with
the centered transform. This caught and corrected a verifier error.

## 5. Reproduce And Falsify

From the repo root:

```sh
python research/certificates/native_rlwe_babai_profile_probe.py --backend flint --save
python research/certificates/native_rlwe_babai_original_input_probe.py --save
python research/certificates/native_rlwe_ntru_completion_probe.py
```

FLINT is optional for construction but required by the saved-artifact
decoder checker. `python-flint` 0.9.0 was installed in this session;
dependencies were not otherwise rewritten. Backend semantics are in the
[official fmpz_mat documentation](https://python-flint.readthedocs.io/en/latest/fmpz_mat.html).

Gemini implementation priorities:

1. Parameterize independent seeds/dimensions WITHOUT changing the native
   label distribution. Preserve exact basis, membership, profile, source
   version and original-coordinate checks in every artifact.
2. Separate profile-only certificates from actual source-law draws and
   held-out recovery. Verify prime/source assumptions independently.
3. Sweep d=64,256,1024 and the earlier source lanes. Record total cost,
   construction failures, retries and reduction strength, not only wins.
4. Compare direct primal/small-secret, scaled dual and module-aware
   baselines on identical public records. Charge shared preprocessing.
5. If a profile test fails, try a stronger classical method. Failure of
   this sufficient certificate is NOT hardness or quantum evidence.

Main-model work: seek a genuinely costed generator on an appropriately
harder distribution. The [balanced-relation target](NATIVE_RLWE_BALANCED_NTRU_TARGET.md)
makes the classical controlled-index completion and inverse-embedding debt
explicit. Its actual d64 single-relation completions pass both lanes too,
including an index-769^64 sublattice and a norm-gcd false negative corrected
by exact ideal HNF. Do
not promote this finite falsifier to an attack on the full source family.
