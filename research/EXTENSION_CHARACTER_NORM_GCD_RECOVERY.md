# Extension-field character recovery by two translated norms

2026-11-06. Constructive WRITTEN classical algorithm, independently derived;
actual-note mathematical review accepted. No novelty, universal cryptographic break,
quantum speedup or execution of the full decoder is claimed.

## Native question, selection and sources

The important question selected in this pass is whether the published
higher-degree extension-field Legendre task still needs search exponential
in the extension degree, when the characteristic is moderately sized. The
mechanism is to decode two translated prime-subfield norm polynomials and
intersect their root sets by a public polynomial gcd. It supplies a complete
classical competitor in a specified regime, rather than a new quantum
receiver or a new source assumption.

Input: an odd prime p, an explicit irreducible degree-r field model
K=F_(p^r), r>=2, a degree d>=1, and CHOSEN queries to

    F(x)=lambda_K(Q(x)),  lambda_K(0)=+1,

where Q in K[X] is an unknown monic SQUAREFREE polynomial of exact degree d.
Nonzero lambda_K is the quadratic character. Output all coefficients of Q,
or ABORT, with probability of ABORT at most eta. The field model and d are
public; neither full Q values nor factors nor Frobenius labels are supplied.
Passive counters, random examples, and quantum phase copies are different
sources and are not covered. Repeated factors are outside the key-recovery
claim because their even multiplicities are hidden by the character.

Let D=rd and0<eta<1. For

    p >= 65536 D²,                                           (1)

the algorithm below uses O(p log(1/eta)) chosen sign queries and classical
time polynomial in p,r,d,log(1/eta), including exact field arithmetic and
the entire prime-field decoder. Thus it is polynomial in the explicit
combined public-description and required-output length in regimes where p
is itself polynomially bounded in r,d. Polynomial dependence on d is
explicit; no polynomial dependence on a binary degree encoding is claimed.
It is NOT polynomial in logp for unrestricted p, nor a practical exponent
claim. The field q=p^r may still be exponential in the input parameters.

Corpus queries `extension field Legendre PRF higher degree norm line
factorization 2604.04833` and the corresponding baselines lookup were run
before the proposal. The latter found no matching catalog item; that is
not evidence of hardness. The retained HIDDEN_FIELD_CHARACTER_ADMISSION.md
already pays a Kopparty-based prime-line decoder, but its target is a
hidden linear field structure. Here multiplication in K is PUBLIC, Q is
arbitrary squarefree, and two translated norms directly recover Q.

Primary sources actually read:

- [Kopparty,2601.07137v1](https://arxiv.org/abs/2601.07137v1), Algorithm A
  and Theorem3.1, plus its exact model. Cached
  `audits/sources/legendre_prf/kopparty_noisy_2601_07137.*`.
- [Pandey,2604.04833v3](https://arxiv.org/abs/2604.04833v3), Sections1.3,
  4 and5.1--5.2. The native higher-degree function is exactly a monic
  polynomial over K followed by the quadratic character. Section5 discusses
  attacks remaining after its geometric collision method, rather than
  proving resistance to every classical algorithm. Cached
  `audits/sources/legendre_prf/pandey_extension_2604_04833.*` identifies v3
  in its PDF margin; v3 was confirmed current. No paper-error claim follows.

Comparators include full-field Kopparty decoding in poly(q), exhaustive
coefficient search, and the source paper's geometric collision method for
degree1 with O(q/M) WORK in addition to its M queries/storage. Its suggested
higher-degree searches are not lower bounds. Our p cost is charged in full.
The full decoder below is written, not executed in this pass.

Two independent alternatives were compared. The proposed semisimple f^r
integral-matrix decision algorithm is already subsumed by BHJ2202.03526v3,
Corollary9.16; its actual text was checked, preserving the old expanded-
conjugator caveat in INTEGRAL_SIMILARITY_OUTPUT_SIZE.md. An RSK-composition
proposal for normalized Kronecker sampling remains unadmitted; no equality
of its laws was established. Neither justifies a new subsystem here.

## 1. Norm labels are available on a paid translated subfield line

For a in K define, with coefficient Frobenius denoted by [p^i],

    H_a(T)=product_(i=0)^(r-1) Q^[p^i](T+a^(p^i)).           (2)

Coefficient Frobenius permutes these factors, so H_a lies in Fp[T]. It is
monic of exact degree D. For every t in Fp,

    H_a(t)=Norm_(K/Fp)(Q(t+a)),
    chi_p(H_a(t))=chi_K(Q(t+a)).                            (3)

The second identity also holds at zero. Therefore p native queries at
t+a give a complete padded character table for H_a; no norm values are
computed by the native algorithm. Padded zeros cause at most D trit errors.

Run Kopparty Algorithm A with degree bound D, epsilon=1/16 and error bound
e=D. Condition(1) implies D<=sqrtp/256 and D<=p/16, satisfying its actual
Theorem3.1 hypotheses. The decoder involves a PUBLIC polynomial of degree
O(Dp), so its factorization/work is polynomial in p, not free polylogp work.
The source explicitly permits p-dependent finite-field factoring; capped
verified randomized factoring is also sufficient. A malformed/zero/failed
output is rejected. Accept an output h only if it is monic, squarefree,
has EXACT degree D, and its complete trit character table disagrees with
the supplied padded table at at most D positions.

Every accepted h equals the actual H_a, including on initially bad lines.
Indeed, if h H_a is not a square, its character correlation is at least
p-4D by this check and at most(2D-1)sqrtp by Weil, contradicting(1).
If it is a square, squarefreeness of h forces h to divide H_a. Equal degree
and monicity then give h=H_a. In particular no nonsquarefree H_a can pass.
Conversely squarefree H_a is returned by the stated decoder theorem and
passes the check. No unknown leading-sign branch is needed.

## 2. Random translation makes the norm squarefree

In an algebraic closure, write the DISTINCT roots of Q as alpha_1,...,alpha_d.
The roots of H_a, with their original multiplicities/indexes, are

    beta_(i,j)(a)=alpha_j^(p^i)-a^(p^i),
       0<=i<r, 1<=j<=d.                                  (4)

For fixed i, these are distinct. For i!=k, an equality between two such
roots imposes a^(p^i)-a^(p^k)=constant. On K this nonzero Fp-linear map
has kernel cardinality p^gcd(r,|i-k|), at most p^floor(r/2).
If the constant is outside its image there are no solutions; otherwise
the solutions are one coset of that kernel. Uniform a therefore has each
collision with probability at most

    delta=p^(-ceil(r/2)).

Union bound over root-index pairs gives

    Pr[H_a not squarefree] <= binom(D,2)*delta.             (5)

This covers coefficients or factors of Q defined over proper subfields.
For example Q in Fp[X] gives H_0=Q^r, so the unshifted line can be entirely
uninformative. It is random translation, not an assumption of generic
secret coefficients, that removes this obstruction. If r>=2 and H_a is
squarefree, it actually has no Fp root: such a root would occur in all r
conjugate factors. The general D-error padding budget above remains safe.

## 3. A second translated norm removes every extra conjugate

For an accepted H_a form publicly in K[X]

    G_a(X)=H_a(X-a).

Its i=0 factor is Q(X), so Q divides G_a. Its indexed roots are

    gamma_(i,j)(a)=alpha_j^(p^i)+a-a^(p^i).                (6)

For independent uniform a,b, compare a root indexed(i,j) of G_a with
one indexed(k,l) of G_b. The pairs with i=k=0 are exactly the intended
roots of Q (j=l); distinct j,l give no equality. Every other pair has
i!=0 or k!=0. Conditioning on the other variable, a nonzero map
z->z-z^(p^i) or z->z-z^(p^k) remains. Its kernel has size at most
p^floor(r/2), so the probability of this particular equality is at most
delta. Union bound over at most D² pairs gives

    Pr[any extraneous cross-match] <= D²*delta.            (7)

On squarefree lines with no such match, gcd(G_a,G_b)=Q. More strongly,
for ANY two accepted lines the gcd contains Q, so accepting precisely when
its degree equals d is an EXACT certificate of the output. No probabilistic
secret-candidate verification or additional chosen queries are necessary.
This uses no factor matching, Frobenius alignment or hidden root labeling
in the algorithm; roots in(4)/(6) are analysis only.

Use fresh UNCONDITIONED pairs(a,b), rejecting a pair if either line fails
or the gcd degree is not d. The pair failure probability is bounded by

    [2 binom(D,2)+D²]*delta <2D²/p <=1/32768.              (8)

This is uniform over EVERY allowed Q. Conditioning independently sampled
lines on acceptance is unnecessary and is not used in the bound.

## 4. Finite clocks, cost and remaining scope

Take L=ceil(log2(2/eta)) independent attempts. Each uses at most2p queries;
the failure probability from(8) is at most2^-L<=eta/2. Sample each a,b
uniformly by sampling its r prime-field coordinates. With k=ceil(log2p),
k-bit rejection sampling accepts with probability at least1/2. Cap each
coordinate at B=ceil(log2(4Lr/eta)) trials. The union bound on2Lr coordinates
is at most eta/2. On success the sampled coordinates are exactly uniform.
All finite-field/decoder/gcd/verification work has polynomial bit cost in
p,r,d,log(1/eta); the exact specified algebraic routines can be used to
avoid another error budget. An implementation choosing randomized factoring
must allocate its own explicit budget or a verified fallback.

Thus the written algorithm is exact on every non-ABORT output, with overall
ABORT probability at most eta. It is not a polylogp algorithm or a recovery
from quantum copies. Fixed p with unbounded rd lies outside(1); characteristic2,
arbitrary repeated-factor keys, imperfect oracle labels, and passive/counter
access are outside the theorem. No large-p end-to-end runtime or practical
security estimate has been measured. Reuse of published polynomial-time
decoding is an explicit dependency, not an inferred fast subroutine.

## Decisive controls and next question

One bounded Sage control is COMPLETE and parent-inspected in
`classical_baselines/extension_norm_gcd_control.py/.json`: exact p7,r2
line norms and character identities, including a base-field Q with bad
unshifted norm, and a genuinely extension-defined Q. Enumerate ordered
shift pairs and verify exact gcd certificates. This directly tests the
translation/Frobenius algebra. It computes norms from Q ONLY as a diagnostic;
it is NOT an implementation of Kopparty or a native key-recovery execution,
and its small p does not satisfy the conservative decoder threshold(1).
With K=F7[w]/(w^2+6w+3), Q0=X^2+1 and Q1=X^2+w, all686 exact
trit/sign/padded-bit comparisons passed. H_a was squarefree for28/49 and
49/49 shifts respectively. Over ordered pairs with both norms squarefree,
gcd-degree histograms were {2:294,3:294,4:196} and {2:2058,4:343}.
Every gcd contained Q, and every degree-two result equaled Q exactly.
The bad unshifted H_0=Q0^2 was retained. One census only; no scaling claim.

The next scientific question is the classical baseline in the complementary
small-characteristic regime, or a quantum operation that removes the p
factor without assuming extra access. No repeated-factor/noisy variant,
parameter sweep, registry entry or new quantum subsystem is admitted now.
