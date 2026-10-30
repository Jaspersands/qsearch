# Deterministic Zero-Target Subfield Correction

29 October 2026. Deduction by Einstein, independently checked by Hubble
and parent. AI review only; no novelty claim, general uniform sampler, or
new native-scale implementation. This removes randomized direction
generation from an existing classical SEARCH regime, not its target-count
promise. The previous general-degree construction and degree-three special
case remain in independent_review_2026_10_22/SUBFIELD_EXTENSION_ATTACK.md.

Implementation follow-up: Gemini subsequently added
`theorems/inverse_trace_subfield_derandomization.py`. Its general
mathematical argument survived independent review within the stated
promises, but the first code version changed the default check count and
had malformed-input and optimized-Python defects. The
[execution audit](audits/reviews/2026-10-29-gemini-execution-audit.md)
records those findings, repairs and verification scope. The original
implementation handoff at the end is historical, not an open request to
duplicate the backend. No uniform sampler follows from this search code.

## Contract

Let F=F_(2^n), n=e*m, k=F_(2^m), e>=3, and |k|>=e. Use the supplied
irreducible polynomial representation, arbitrary distinct public points
alpha_i, H[j,i]=alpha_i^j for 0<=j<K, and arbitrary public syndrome s.
At least eK coordinates must have target bit zero. Produce x satisfying

    Hx=s, Tr_F/F2(inv0(x_i))=b_i for every i.

No hidden advice, full-field enumeration or supplied witness is used.
In the native K=floor(N/8) regime the eK threshold limits the useful
relative degrees; this does not solve prime-degree or low-zero cases.

## Explicit Directions

Let theta be the supplied polynomial-basis generator. It generates F
over F2, so k(theta)=F and its relative degree is exactly e. Solve

    Tr_F/k(beta)=0, Tr_F/k(theta*beta)=0

for a nonzero beta. The relative trace pairing is nondegenerate, and
1,theta are k-independent, so this common kernel has k-dimension e-2.
This remains true for even e; Tr_F/k(1)=0 does not make the trace pairing
degenerate.

Choose e distinct elements t_1,...,t_e of k and put

    u_j=1/(beta*(theta+t_j)).

All denominators are nonzero. Each line u_j*k, including zero, lies in
the target-zero alphabet: for c!=0,

    Tr_F/k((u_j*c)^(-1))
      =c^(-1)*Tr_F/k(beta*(theta+t_j))=0.

Trace transitivity proves the absolute-trace predicate. To show the u_j
form a k-basis, multiply a hypothetical relation by
beta*product_j(theta+t_j). The resulting polynomial in theta has degree
at most e-1, so it vanishes identically. Evaluating at -t_j forces every
coefficient to be zero. This deliberately full-degree ratio resolves the
old composite-degree warning about arbitrary trace-zero pairs.

## Deterministic Full-Rank Choice

Choose exactly eK zero-target coordinates. At coordinate i offer the e
vectors u_j*H_i in F^K, regarded as a k-vector space. Their span is F*H_i.
For any subset I of these coordinates, Vandermonde independence gives

    dim_k span{u_j*H_i : i in I, 1<=j<=e}
      = e*min(K,|I|) >= |I|.

The independent-transversal criterion therefore applies. Intersect the
linear matroid on these vectors with the partition matroid allowing at
most one choice per coordinate. A maximum common independent set has
size eK. It is a basis of F^K over k, so the chosen lines solve every
residual syndrome. This uses an exchange algorithm, NOT greedy selection.
The standard constructive algorithm is in
[Goemans, matroid intersection, Section 5.2](https://math.mit.edu/~goemans/18433S11/matroid-intersect-notes.pdf).

Fix all other coordinates at any accepted values, subtract their syndrome,
then solve in the selected basis. For target one, choose a public binary
basis element with absolute trace one and invert it. Such an element
exists because absolute trace is a nonzero F2-linear functional.

## Actual Bit Operations

- Compute k as the binary kernel of x -> x^(2^m)-x.
- Compute the two relative-trace maps by Frobenius powering and binary
  elimination; choose a nonzero common-kernel vector.
- Construct e distinct t_j from the binary basis of k, without scanning F.
- The ground set has e^2*K candidates. For a k-rank query, expand each
  vector by the m public basis scalars of k and divide binary rank by m.
  The expanded matrices have at most nK rows and polynomially many columns.
- Run deterministic linear/partition matroid intersection, then an exact
  binary solve and verify the original parity and trace conditions.

Every step has polynomial bit complexity in the stated input and e<=n.
This is a constructive mathematical algorithm, not a claim that a new
production implementation has run. Existing expected-polynomial search
already covered the same zero threshold. No output-uniformity conclusion
follows from choosing one product of lines.

## Finite Evidence And Implementation Handoff

Einstein checked n8,e4,m2 with modulus0x11b, theta2,beta6 and directions
[176,41,200,98]. On N64,K8 with32 zero targets and syndrome[1,...,8], the
restricted rank was64 and the original equations verified. Hubble separately
checked the direction construction, kernel dimensions and full binary
basis rank in F256/F4. Parent checked the proof above, not a second full
matroid implementation. These are finite controls, not the reason for the
asymptotic guarantee.

Mechanical implementation work for Gemini: reuse the existing field and
matroid-intersection routines; add this full-degree direction constructor
without altering the native input or relying on random direction retries.
Test e=3,4,5 where |k|>=e; include composite e, even e, arbitrary nonzero
syndromes, and insufficient-zero rejection. Preserve an explicit failed
greedy control. Check original equations independently after the solve.
Do not describe the resulting solver as a uniform sampler. No new CLI,
registry promotion or large experiment is authorized by this note alone.
