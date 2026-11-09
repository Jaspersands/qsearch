# Reduced norm: compact Amitsur map and construction certificate

2026-11-07. Focused actual-source/resource review of Section4 of
`research/REDUCED_NORM_PRESCRIBED_FIELD.md`, after STATE/TRAPS. Interpreter
`/opt/anaconda3/bin/python`; no Git/network/API, implementation or new tests.

**Verdict:** the proposed EXACT positive certificate is viable under the
explicit format below. It needs neither expansion of huge units nor general
arithmetic-circuit PIT. Section4's current qualitative description must retain
these checks and finite clocks. This is not approval of the preceding field
construction, the whole algorithm, a minimal-module algorithm, or expanded
output bounds. Finite controls are not used as theorem evidence.

## Actual imported sources and their limits

Locators in `audits/sources/global_isotropy/amitsur.txt` (KM v3):

- Fact2.1,201–206: number-field maximal orders in polynomial quantum time,
  via classical round2 with integer factoring. This is NOT a maximal-order
  oracle for a central simple algebra.
- Algorithm1,670–694; Theorem3.10/proof727–744: expanded étale presentation
  and expanded linear isomorphism from its Amitsur algebra to the input CSA.
  The cocycle is obtained by linear algebra. Lemma3.9,704–726, gives the
  determinant/Schwartz–Zippel sampling argument for its expanded front end.
- Definition3.3,462–469; Remark3.5,546–562: twisted multiplication and the
  untwisted trace map `r tensor s -> (z -> r Tr(s z))`.
  Corollary3.7,593–601, transports associated cocycles by multiplication
  with a cochain (direction/inversion must follow the chosen coboundary).
- Algorithm2,1103–1132; Theorem4.12/proof1135–1163: compute a trivializing
  cochain by S-unit coordinates and integer equations. The support uses
  ramification, class generators and the cocycle's finite support. GRH is
  explicit. The internal tensor products are decomposed into number fields,
  not a normal closure.
- Theorem4.13,1164–1173: takes a number field and a PROMISED SPLIT algebra
  over it; its polynomial statement is not restricted to a fixed base field.
  Its theorem statement does not by itself bound expanded splitting-map
  height. Preserve the compact cochain representation, as in the existing
  `AMITSUR_ARITHMETIC_REUSE_AUDIT.md`32–82,121–134, including its warning to
  use the corrected arbitrary-degree S-unit analysis. No compact-to-small
  normalization is imported here.

For LS, `audits/sources/monomial_descent/lenstra_silverberg.txt`33–38 fixes
the EXPANDED rational structure-constant/coordinate-vector input model.
Theorem1.10,212–219, supplies all field factors and maps in deterministic
polynomial time. Theorem1.11(i),230–235, supplies the FULL integral relation
kernel and unit testing;1.11(ii),237–240, supplies subgroup membership.
Algorithm8.3,819–852, and proof877–886 establish the full kernel; Algorithm8.4,
854–873, and proof887–890 establish membership. This is deterministic
polynomial BIT time in the entire algebra, tuple and coordinate input sizes,
not only in their count. It requires neither supplied class/unit advice nor
integer factoring/GRH. It does NOT accept arbitrary arithmetic circuits as
algebra-element inputs.

## Exact certificate format: the verifier reconstructs the computation

Use F for the prescribed degree-n field over K, and H for KM's auxiliary
rank-n étale algebra over F. Put B=A tensor_K F, U=H tensor_F H and
T=H tensor_F H tensor_F H. Their Q-dimensions are respectively
`[K:Q] n^3`, `[K:Q] n^3`, `[K:Q] n^4`; all are polynomial. The expanded
tables, maps, trace, presentation cocycle c and presentation map Phi must
have polynomial coordinate heights, from the expanded front end and
polynomial-size exact linear algebra. Verify these data rather than trust a
claimed compact matrix representation. Specifically:

1. Check compatible expanded F/K data, theta and `Norm_F/K(theta)=a` (or
   its stated degree-n characteristic polynomial and constant term). Check
   H is étale, Phi:U->B is invertible and intertwines the expanded twisted
   multiplication defined by c with B multiplication, on basis pairs.
   All these operations concern expanded polynomial-size data.
2. Alpha is a polynomial list of SMALL expanded unit atoms in U with binary
   exponents of polynomial length. Component-field atoms must be lifted as
   units `1-e_i+e_i u`, not as the nonunit `e_i u`. Expand each SMALL atom's
   inverse once if needed; its height remains polynomial by linear algebra.
   Negative powers thereafter use these expanded inverse atoms and ordinary
   binary powering, not an inverse gate on a large compact sum.
3. Apply the three expanded insertion maps epsilon to these atoms into T.
   Run LS1.11(i) on the resulting expanded atoms and c. Check that the
   exponent vector expressing `(delta alpha)c^-1` lies in the computed
   integral kernel. The verifier runs LS itself; an unverified claimed
   relation basis is insufficient. Unit testing rejects malformed atoms/c.
   This proves EXACTLY `c=delta(alpha)` without evaluating alpha's huge
   expanded coordinates. The source tuple has polynomial total bit size.
4. Rebuild the map, using the established convention
   `c_ijk=alpha_jk alpha_ik^-1 alpha_ij`:
   `rho = trace_map o multiplication_by_alpha o Phi^-1`.
   Indeed `alpha_ij c_ikj=alpha_ik alpha_kj`; this fixes its orientation.
   Thus rho is an algebra isomorphism B->M_n(F). Do not accept an arbitrary
   submitted matrix-map circuit merely because its name is rho.
5. Given the small integer vector w, rebuild the n^2-square K-matrix B_w
   with columns rho(b_i)w and the expanded vector theta*w. Build D=det(B_w)
   and Cramer numerators by a canonical POLYNOMIAL-SIZE DIVISION-FREE
   determinant circuit (e.g. Berkowitz applied also to the minors/replaced
   matrices). The sole final division is by D. A factorial Leibniz expansion
   or unverified Gaussian-elimination pivot inverses do not meet this format.
6. Verify an exact modular evaluation of this rebuilt D, with every rational
   denominator invertible modulo the supplied prime, and D nonzero in the
   FULL finite K algebra. It need not be a field; one nonzero coordinate is
   enough to prove D!=0 in K. If inverses are evaluated modulo this algebra,
   require their elements to be UNITS, tested by multiplication determinants.
   Rebuilding as above avoids such compact intermediate inverses entirely.
   In particular a nonzero K-coordinate modulo p proves D!=0 in the FIELD
   K, even if D is not a unit modulo p. The canonical K-inverse circuit uses
   its multiplication adjugate divided by Norm_K/Q(D); this latter scalar
   is mathematically nonzero because D!=0. Its final inverse need not be
   evaluated modulo p for the certificate. Alternatively require D to be a
   modular unit and charge the bad primes dividing Norm_K/Q(D).
7. Rebuild/compare the output DAG syntactically with the prescribed Cramer
   DAG. General semantic equivalence of arbitrary submitted circuits is not
   claimed. Syntactic checking, the coboundary equality and D!=0 suffice.

With these checks, x=B_w^-1(theta*w) is defined exactly. The identification
`A -> V, b -> rho(b)w` is an isomorphism of left A-modules. Scalar theta
commutes with A and therefore corresponds to RIGHT multiplication by x.
Its K-characteristic polynomial is `P^n`, while regular right multiplication
has characteristic polynomial `redchar_x^n`. Monicity gives redchar_x=P
and hence Nrd(x)=a. The verifier need not compute this compact norm or test
any further circuit equality. Positive soundness is unconditional, given
the native field/CSA promises; GRH concerns the search procedure.

## Heights, primes, finite clocks and failures

The number of matrix/coordinate gates is polynomial: binary powers have
polynomial exponent-bit length; all tensor dimensions above and determinant
circuits are polynomial. Expand field operations conceptually to a rational
scalar +,-,* DAG, with T gates and H-bit constants (including tables and
small inverses). Each unreduced numerator/denominator has bit length at
most `B0=2^(T+2)(H+1)`. This is EXPONENTIAL expanded length, not a polynomial
expanded-output claim.

For fixed w with D!=0, rational denominators plus a nonzero coordinate
numerator of D have at most `(T+1)B0` distinct bad rational prime divisors.
Using an explicit standard dyadic prime-count bound, a sufficient bit length
is `b=2[T+ceil(log2(H+1))+ceil(log2(T+1))+ceil(log2(1/delta))+32]`.
A uniformly chosen b-bit prime is bad with probability <delta. Generate it
by uniform b-bit integers and deterministic polynomial-time primality tests;
the prime density gives a capped O(b log(1/delta_gen)) trial clock. The
accepted prime is uniform, conditional on generation success. Modular
evaluation then costs polynomial BIT time. A successful evaluation is an
EXACT nonzero certificate, not a one-sided or two-sided PIT acceptance.

Choose source atoms and w BEFORE a fresh prime. Conditional on a valid rho,
the nonzero degree-n^2 determinant polynomial in w gives cyclic-w probability
at least3/4 on the stated grid. Taking prime-bad and prime-generation
probabilities each<=1/8 leaves per-trial acceptance >1/2. A capped
`ceil(log2(4/eta))` independent trial clock makes this stage's exhaustion
probability <=eta/4. Every prime/test height bound is uniform over the small
w grid. Do not reuse a modulus for new expressions chosen adaptively from it.

Reserve separate error budgets for the factoring/unit-source/front-end calls
and their capped clocks. A source failure cannot make this deterministic
positive verifier accept a false certificate; it may cause rejection or
exhaustion. Those events are ABORT/failure, not the mathematical NO answer.
NO requires the independently paid existence criterion. Completeness of an
S-unit list is needed for finding a witness, not for certifying one returned
alpha. This review does not independently repay that source's entire quantum
pipeline or the field-construction obligations handled by the other reviews.
