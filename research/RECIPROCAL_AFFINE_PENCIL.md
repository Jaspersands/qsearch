# Reciprocal-Affine Pencils: An Exact Classical Baseline

2026-10-22. Local derivation and implementation, REVIEW PENDING. Restricted
classical attack, not a general solver, hardness proof, novelty claim, or
quantum speedup. No central-registry admission.

## Decision

Before building a quantum decoder for BALANCED_CODEWORD_FILTER.md, test
the same native task classically. The projective-line check in that note
was too narrow. A more general attack can exhaust a supplied affine line
in the RECIPROCAL coordinates in polynomial work, without enumerating
the exponentially large field. A matching partial-fraction argument also
classifies fixed, formally code-valued inverse-affine parameterizations.

This does not kill the candidate. It removes a weak baseline and precisely
states where a natural classical linearization stops being automatic.
Selecting useful pencils adaptively remains an unresolved attack, not a
hardness result. Do not spend effort on a generic GS backend on the strength
of this negative evidence alone.

## Native Input And Attack

The input is exactly the earlier explicit-input task: q=2^n in a public
polynomial basis, distinct points alpha_i, H[j,i]=alpha_i^j for 0<=j<K,
and arbitrary b_i in F_2. Seek

    Hx=0,  Tr(inv0(x_i))=b_i,  inv0(0)=0.

The public coefficients a_i,c_i specify one attack pencil, not witness
advice promised by the problem. For u in F_q set

    y_i(u)=a_i*u+c_i,  x_i(u)=inv0(y_i(u)).

Since inv0 is an involution, ALL trace constraints become the binary
linear equations Tr(a_i*u)=b_i+Tr(c_i), including when y_i=0. Solve them
first. An inconsistent system excludes only this pencil.

For every a_i!=0 write r_i=c_i/a_i, v_i=1/a_i. Group equal poles r_i.
The constant coordinates a_i=0 have values inv0(c_i). Each parity check
away from the poles is the rational function

    F_j(U)=C_j + sum_r R[j,r]/(U+r),
    C_j=sum_(a_i=0) alpha_i^j*inv0(c_i),
    R[j,r]=sum_(r_i=r) alpha_i^j/a_i.

With P(U)=product_r(U+r), compute

    Q_j(U)=C_j*P(U)+sum_r R[j,r]*P(U)/(U+r).

There are g<=N distinct poles, deg(P)=g and deg(Q_j)<=g. Repeated poles
are grouped BEFORE forming this square-free common denominator. All
operations are exact native-field polynomial arithmetic.

### Nonidentity Case

If some Q_j is nonzero, compute G=gcd_j Q_j. Every regular solution is
a base-field root of G. Factor/root-find at degree at most N, then check
the original trace AND parity conditions for each regular root. Also
check EVERY pole r directly using inv0. There are at most 2N parameter
checks, even if q is exponential in the input parameter n.

Denominator clearing is not equivalent at poles. Over F_8, take N=3,K=1,
y=(u,u+1,1), and b=(0,1,1). Then u=0 gives x=(0,1,1), a valid native
answer. The cleared numerator U^2+U+1 has NO root in F_8. Discarding poles
would falsely report an empty pencil. The implementation records this
countercontrol rather than silently excluding zero coordinates.

Completeness of the returned root list is itself checked:

    product_(distinct returned roots r) (U-r)
      = monic(gcd(G, U^q-U)).

U^q is computed MODULO G with binary powering, never expanded to degree q.
This certificate detects missing, duplicate and extraneous roots, including
inseparable G. A failed certificate raises an error; it is not a research
negative. Every accepted output is separately checked against native input.

The algorithm uses ordinary finite-field gcd/root routines. The implementation
uses the documented [python-flint polynomial API](https://python-flint.readthedocs.io/en/latest/fq_default_poly.html).
Field representation, arithmetic, binary elimination and finite-field root
finding are charged. The standard randomized factorization dependency is
not a deterministic worst-case runtime theorem; this adapter has no local
backend timeout. No truth table or coherent oracle is supplied or generated.

### Identity Case

If all Q_j vanish as POLYNOMIALS, reducing Q_j modulo U+r forces R[j,r]=0
for every pole, because all other factors are nonzero at r. Then C_j=0.
Thus each pole group's residue vector is independently a codeword of ker H,
and the constant vector is another codeword. The finite-field x(u) lies in
ker H for EVERY u, including poles: at a pole the entire corresponding
kernel vector is set to zero. No illegal division or pole rejection remains.

The exact solution set is therefore the binary affine trace system. Return
its RREF, a particular solution, and count 2^(n-rank), not an exponential
list. This includes the all-zero codeword when the target permits it.

Formal rational identity must not be inferred from finite agreement. For
example, with N=q=4, K=1, a_i=1 and c_i running over the whole field, every
finite parameter is a pole and sum_i inv0(u+c_i)=0. The rational function
nevertheless has nonzero residues. The code takes the nonidentity branch
and checks all four poles. The rigidity statement below does NOT apply to
this example.

## Fixed Multi-Parameter Rigidity

This local proposition concerns formal parameterizations, not all algorithms.
Let u=(u_1,...,u_r) have any number of field parameters. Fix affine-linear
forms y_i(u). Suppose the rational vector x_i=1/y_i for nonconstant y_i,
with constant coordinates handled by inv0, satisfies Hx=0 as an identity
over F_q(u_1,...,u_r). Group nonconstant y_i up to nonzero scalar multiple:

    y_i=a_i*ell_g(u),  x_i=a_i^(-1)/ell_g(u).

Distinct nonproportional affine-linear forms are distinct irreducible
polynomials. After multiplying by their product and reducing modulo one
ell_g, the quotient polynomial ring is an integral domain. The other forms
remain nonzero, so the constant residue vector for this group must have
zero syndrome. The constant part must also have zero syndrome.

Every K columns of a K-row Vandermonde matrix on distinct points are
independent. Each nonconstant group consequently occupies at least K+1
coordinates. Therefore

    number of nonconstant groups <= floor(N/(K+1)).

The output target bits are affine binary functions of the group values
ell_g(u), regardless of how many formal parameters were introduced. Hence

    binary rank of target image <= min(N, n*floor(N/(K+1))).

For a SINGLE FIXED family, its fraction of covered uniformly random targets
is at most 2^(min(N,n*floor(N/(K+1)))-N). At N=n^2,K=floor(N/8), the
recorded n=17,31,61 budgets are respectively 2^-170, 2^-744, 2^-3294.
These are exact restricted-image counts, NOT probabilities for adaptive
search and NOT lower bounds for the original problem. A target-dependent
family may be easy to construct despite every fixed family's small image.

The original projective line is one group with ell=u. Multiple disjoint
kernel groups fit this classification. The theorem excludes neither
nonconstant rational numerators, nonlinear denominators, nor solving parity
only at selected parameters. In particular, the nonidentity pencil branch
above deliberately searches such selected parameters.

## Attack Audit And Remaining Risks

1. The existing odd-prime quadratic-character norm attack uses a difference
   of two squares with prescribed character cosets. Reciprocal trace is an
   Artin-Schreier constraint, not that predicate. No transfer is established.
   A rational norm construction with the correct native degree budget remains
   a potentially decisive attack; calling this an obstruction would be false.
2. Setting x_i*y_i=1 and Tr(y_i)=b_i gives a structured bilinear system ONLY
   on nonzero coordinates. Zero-coordinate strata are essential. Generic
   constant-factor variable surplus does not by itself imply polynomial-time
   solvability of the resulting Boolean equations.
3. A chosen reciprocal pencil now has an exact solver. Choosing a family
   after seeing b, using more parameters without a formal identity, or
   exploiting the RS evaluation geometry are the actual unresolved steps.
   Repeated failures of arbitrary lines do not constitute useful hardness
   evidence. No seed campaign is justified by the image-count bound.
4. Local cryptographic nonlinearity is a poor proxy for this codeword task.
   [Feng and Gong, published abstract](https://link.springer.com/article/10.1007/s11424-016-5208-z)
   give inverse-trace algebraic immunity ceil(2*sqrt(n))-2 and describe fast
   algebraic weaknesses. The abstract was verified; the full proof was not
   available in this pass. This is a reason to investigate low-degree
   annihilators, NOT an imported attack on the coupled native code problem.

The next substantive test should derive an actual target-adaptive algebraic
attack (including the last item) or independently scrutinize the coherent
support-mask proof. Do not equate the earlier quantum construction's
per-instance success argument with classical hardness. It still has no
established standard-problem reduction, cryptanalytic application, complete
reversible decoder, or independent proof review.

## Files And Replay

- `theorems/reciprocal_affine_pencil.py`: exact pencil attack, root completeness,
  fixed-family rank budgets, standalone artifact workflow.
- `tests/test_reciprocal_affine_pencil.py`: exhaustive small-field comparisons,
  exceptional/constant/repeated-pole controls, corrupted root certificates,
  and 17/31/61-bit field operations without field enumeration.
- `research/classical_baselines/reciprocal_affine_pencil.json`: source/proof
  hashes, complete restricted certificates, witnesses and explicit scope.

Run `python -m theorems.reciprocal_affine_pencil --write` and the two test
files `test_reciprocal_affine_pencil.py` / `test_balanced_codeword_filter.py`.
The finite controls are algebraic regression tests, not evidence for a
scaling advantage. Use the repository's external PYTHONPYCACHEPREFIX in
this workspace; do not repair cloud sync to replay unrelated old artifacts.
